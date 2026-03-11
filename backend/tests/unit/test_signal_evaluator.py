"""
Unit tests for deterministic signal registry and evaluator.
"""

from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from core.contracts.signal_contract import (
    ACTIVATION_MODE_LAB_RANGE,
    ACTIVATION_MODE_THRESHOLD,
    ALLOWED_SIGNAL_STATES,
    STATE_RANK,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry


def _write_signal_library(
    path: Path,
    signal_id: str,
    *,
    primary_metric: str = "glucose",
    override_threshold: float = 120.0,
) -> None:
    path.write_text(
        "\n".join(
            [
                "library:",
                "  package_id: test",
                "signals:",
                f'  - signal_id: "{signal_id}"',
                '    system: "metabolic"',
                f'    primary_metric: "{primary_metric}"',
                "    supporting_metrics: []",
                "    dependencies: []",
                "    optional_dependencies: []",
                "    thresholds:",
                '      - severity: "suboptimal"',
                '        operator: "range"',
                "        min_value: 90",
                "        max_value: 99",
                '      - severity: "at_risk"',
                '        operator: ">="',
                "        value: 100",
                "    activation_logic: {}",
                "    override_rules:",
                '      - rule_id: "override_high_glucose"',
                "        conditions:",
                f'          - metric_id: "{primary_metric}"',
                '            operator: ">="',
                f"            value: {override_threshold}",
                '            condition_type: "any_of"',
                '        resulting_state: "at_risk"',
                '    output:',
                f'      signal_value: "{primary_metric}"',
                "      supporting_markers: []",
            ]
        ),
        encoding="utf-8",
    )


def test_signal_registry_excludes_pkg_example():
    registry = SignalRegistry()
    ids = [item["signal_id"] for item in registry.get_all_signals()]
    assert "signal_example_metabolic" not in ids


def test_signal_registry_is_deterministic_across_instances():
    a = SignalRegistry()
    b = SignalRegistry()
    assert [s["signal_id"] for s in a.get_all_signals()] == [s["signal_id"] for s in b.get_all_signals()]
    assert a.version == b.version
    assert a.package_hash == b.package_hash


def test_signal_registry_duplicate_signal_ids_resolve_deterministically(monkeypatch, tmp_path):
    p1 = tmp_path / "a.yaml"
    p2 = tmp_path / "b.yaml"
    _write_signal_library(p1, signal_id="dup_signal")
    _write_signal_library(p2, signal_id="dup_signal", primary_metric="insulin")
    monkeypatch.setattr(SignalRegistry, "_iter_signal_library_paths", lambda self: [p1, p2])

    registry = SignalRegistry()
    loaded = {row["signal_id"]: row for row in registry.get_all_signals()}
    assert loaded["dup_signal"]["primary_metric"] == "insulin"


class _StubRegistry:
    version = "stub-version"
    package_hash = "stub-hash"

    @staticmethod
    def get_all_signals():
        return [
            {
                "signal_id": "signal_alpha",
                "system": "metabolic",
                "primary_metric": "tyg_index",
                "supporting_metrics": ["insulin", "glucose"],
                "thresholds": [
                    {"severity": "suboptimal", "operator": "range", "min_value": 8.6, "max_value": 9.1},
                    {"severity": "at_risk", "operator": ">=", "value": 9.2},
                ],
                "override_rules": [
                    {
                        "rule_id": "high_crp_override",
                        "conditions": [
                            {"metric_id": "crp", "operator": ">=", "value": 3.0, "condition_type": "any_of"}
                        ],
                        "resulting_state": "at_risk",
                    }
                ],
                "output": {"supporting_markers": ["insulin", "glucose"]},
                "explanation": {
                    "mechanism": "TyG elevation suggests insulin signalling strain.",
                    "interpretation": "Metabolic dysregulation context.",
                },
            },
            {
                "signal_id": "signal_beta",
                "system": "inflammation",
                "primary_metric": "crp",
                "supporting_metrics": [],
                "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 3.0}],
                "override_rules": [
                    {
                        "rule_id": "severe_inflammation",
                        "conditions": [
                            {"metric_id": "sii", "operator": ">=", "value": 800.0, "condition_type": "any_of"}
                        ],
                        "resulting_state": "at_risk",
                    }
                ],
                "output": {"supporting_markers": []},
            },
        ]


def test_override_rule_any_of_fires_and_changes_state():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={"crp": 3.2},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    by_id = {r.signal_id: r for r in results}
    assert by_id["signal_alpha"].signal_state == "at_risk"


def test_override_rule_any_of_not_met_preserves_threshold_result():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={"crp": 1.2},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    by_id = {r.signal_id: r for r in results}
    assert by_id["signal_alpha"].signal_state == "suboptimal"
    assert by_id["signal_alpha"].confidence is None
    assert by_id["signal_alpha"].supporting_markers == ["insulin", "glucose"]
    assert by_id["signal_alpha"].explanation == {
        "mechanism": "TyG elevation suggests insulin signalling strain.",
        "interpretation": "Metabolic dysregulation context.",
    }


def test_override_rule_all_of_requires_all_conditions_true():
    class _AllOfRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_all_of",
                    "system": "hepatic",
                    "primary_metric": "tyg_index",
                    "supporting_metrics": [],
                    "thresholds": [{"severity": "suboptimal", "operator": ">=", "value": 8.5}],
                    "override_rules": [
                        {
                            "rule_id": "hepatic_override",
                            "conditions": [
                                {"metric_id": "ast_alt_ratio", "operator": ">=", "value": 2.0, "condition_type": "all_of"},
                                {"metric_id": "alt", "operator": ">=", "value": 33.0, "condition_type": "all_of"},
                            ],
                            "resulting_state": "at_risk",
                        }
                    ],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_AllOfRegistry())
    one_true = evaluator.evaluate_all(
        signal_biomarkers={"alt": 20.0},
        signal_derived={"tyg_index": 8.9, "ast_alt_ratio": 2.2},
        lab_ranges={},
    )
    assert one_true[0].signal_state == "suboptimal"

    both_true = evaluator.evaluate_all(
        signal_biomarkers={"alt": 35.0},
        signal_derived={"tyg_index": 8.9, "ast_alt_ratio": 2.2},
        lab_ranges={},
    )
    assert both_true[0].signal_state == "at_risk"


def test_multiple_override_rules_highest_rank_wins_deterministically():
    class _MultiOverrideRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_multi",
                    "system": "metabolic",
                    "primary_metric": "tyg_index",
                    "supporting_metrics": [],
                    "thresholds": [{"severity": "optimal", "operator": "<", "value": 8.0}],
                    "override_rules": [
                        {
                            "rule_id": "to_suboptimal",
                            "conditions": [
                                {"metric_id": "crp", "operator": ">=", "value": 2.0, "condition_type": "any_of"}
                            ],
                            "resulting_state": "suboptimal",
                        },
                        {
                            "rule_id": "to_at_risk",
                            "conditions": [
                                {"metric_id": "glucose", "operator": ">=", "value": 5.6, "condition_type": "any_of"}
                            ],
                            "resulting_state": "at_risk",
                        },
                    ],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_MultiOverrideRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={"crp": 3.0, "glucose": 6.0},
        signal_derived={"tyg_index": 7.2},
        lab_ranges={},
    )
    assert len(results) == 1
    assert results[0].signal_state == "at_risk"


def test_override_condition_with_absent_metric_is_false_fail_safe():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={},
    )
    assert len(results) == 1
    assert results[0].signal_id == "signal_alpha"
    assert results[0].signal_state == "suboptimal"


def test_signal_skipped_when_primary_metric_absent():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={"crp": 2.0},
        signal_derived={},
        lab_ranges={},
    )
    assert results == []


def test_no_threshold_match_omits_signal():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={"crp": 0.8},
        signal_derived={"tyg_index": 8.1},
        lab_ranges={},
    )
    assert results == []


def test_duplicate_loading_keeps_deterministic_override_behavior(monkeypatch, tmp_path):
    p1 = tmp_path / "a.yaml"
    p2 = tmp_path / "b.yaml"
    _write_signal_library(p1, signal_id="dup_signal", primary_metric="glucose", override_threshold=200.0)
    _write_signal_library(p2, signal_id="dup_signal", primary_metric="glucose", override_threshold=100.0)
    monkeypatch.setattr(SignalRegistry, "_iter_signal_library_paths", lambda self: [p1, p2])

    registry_a = SignalRegistry()
    registry_b = SignalRegistry()
    evaluator_a = SignalEvaluator(registry_a)
    evaluator_b = SignalEvaluator(registry_b)

    out_a = evaluator_a.evaluate_all(
        signal_biomarkers={"glucose": 110.0},
        signal_derived={},
        lab_ranges={"glucose": {"min": 70.0, "max": 99.0}},
    )
    out_b = evaluator_b.evaluate_all(
        signal_biomarkers={"glucose": 110.0},
        signal_derived={},
        lab_ranges={"glucose": {"min": 70.0, "max": 99.0}},
    )
    assert len(out_a) == len(out_b) == 1
    assert out_a[0].signal_state == out_b[0].signal_state == "at_risk"


def test_lab_normal_but_flagged_recomputed_after_override_paths():
    evaluator = SignalEvaluator(_StubRegistry())
    in_range = evaluator.evaluate_all(
        signal_biomarkers={"crp": 3.5},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    assert in_range[0].signal_state == "at_risk"
    assert in_range[0].lab_normal_but_flagged is True

    outside_range = evaluator.evaluate_all(
        signal_biomarkers={"crp": 3.5},
        signal_derived={"tyg_index": 9.3},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    assert outside_range[0].signal_state == "at_risk"
    assert outside_range[0].lab_normal_but_flagged is False

    no_ranges = evaluator.evaluate_all(
        signal_biomarkers={"crp": 3.5},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={},
    )
    assert no_ranges[0].signal_state == "at_risk"
    assert no_ranges[0].lab_normal_but_flagged is False


def test_threshold_operator_greater_than_activates_deterministically():
    class _UpperOnlyRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_upper_only",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "thresholds": [{"severity": "at_risk", "operator": ">", "value": 100.0}],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_UpperOnlyRegistry())
    out_a = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 101.0},
        signal_derived={},
        lab_ranges={},
    )
    out_b = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 101.0},
        signal_derived={},
        lab_ranges={},
    )
    assert len(out_a) == 1
    assert out_a[0].signal_state == "at_risk"
    assert [r.model_dump() for r in out_a] == [r.model_dump() for r in out_b]


def test_threshold_operator_less_than_activates_deterministically():
    class _LowerOnlyRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_lower_only",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "thresholds": [{"severity": "suboptimal", "operator": "<", "value": 70.0}],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_LowerOnlyRegistry())
    out_a = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 65.0},
        signal_derived={},
        lab_ranges={},
    )
    out_b = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 65.0},
        signal_derived={},
        lab_ranges={},
    )
    assert len(out_a) == 1
    assert out_a[0].signal_state == "suboptimal"
    assert [r.model_dump() for r in out_a] == [r.model_dump() for r in out_b]


def test_threshold_bidirectional_sides_activate_independently():
    class _BidirectionalRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_bidirectional",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "thresholds": [
                        {"severity": "suboptimal", "operator": "<", "value": 70.0},
                        {"severity": "at_risk", "operator": ">", "value": 100.0},
                    ],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_BidirectionalRegistry())
    low_out = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 65.0},
        signal_derived={},
        lab_ranges={},
    )
    high_out = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 105.0},
        signal_derived={},
        lab_ranges={},
    )
    assert len(low_out) == 1
    assert low_out[0].signal_state == "suboptimal"
    assert len(high_out) == 1
    assert high_out[0].signal_state == "at_risk"


def test_threshold_bidirectional_within_range_does_not_activate():
    class _BidirectionalRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_bidirectional",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "thresholds": [
                        {"severity": "suboptimal", "operator": "<", "value": 70.0},
                        {"severity": "at_risk", "operator": ">", "value": 100.0},
                    ],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_BidirectionalRegistry())
    within = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 85.0},
        signal_derived={},
        lab_ranges={},
    )
    assert within == []


def test_corrected_homocysteine_signal_bare_lab_exceedance_is_suboptimal():
    class _HomocysteineCorrectedRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_homocysteine_elevation_context",
                    "system": "vascular",
                    "primary_metric": "homocysteine",
                    "activation_logic": "lab_range_exceeded",
                    "activation_config": {
                        "upper_bound_state": "suboptimal",
                        "enable_lower_bound": False,
                        "lower_bound_state": "suboptimal",
                    },
                    "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 9999.0}],
                    "override_rules": [
                        {
                            "rule_id": "hcy_context_b_vitamin_or_transport_deficit",
                            "conditions": [
                                {"metric_id": "vitamin_b12", "operator": "<", "value": 350.0, "condition_type": "any_of"},
                                {"metric_id": "folate", "operator": "<", "value": 7.0, "condition_type": "any_of"},
                                {"metric_id": "transferrin", "operator": "<", "value": 2.0, "condition_type": "any_of"},
                            ],
                            "resulting_state": "at_risk",
                        }
                    ],
                    "output": {"supporting_markers": ["vitamin_b12", "folate", "transferrin", "mcv", "crp"]},
                }
            ]

    evaluator = SignalEvaluator(_HomocysteineCorrectedRegistry())
    out = evaluator.evaluate_all(
        signal_biomarkers={"homocysteine": 15.0, "vitamin_b12": 420.0, "folate": 10.0, "transferrin": 2.5, "crp": 1.0},
        signal_derived={},
        lab_ranges={"homocysteine": {"min": 4.0, "max": 14.0}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "suboptimal"


def test_corrected_homocysteine_signal_override_escalates_to_at_risk():
    class _HomocysteineCorrectedRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_homocysteine_elevation_context",
                    "system": "vascular",
                    "primary_metric": "homocysteine",
                    "activation_logic": "lab_range_exceeded",
                    "activation_config": {
                        "upper_bound_state": "suboptimal",
                        "enable_lower_bound": False,
                        "lower_bound_state": "suboptimal",
                    },
                    "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 9999.0}],
                    "override_rules": [
                        {
                            "rule_id": "hcy_context_b_vitamin_or_transport_deficit",
                            "conditions": [
                                {"metric_id": "vitamin_b12", "operator": "<", "value": 350.0, "condition_type": "any_of"},
                                {"metric_id": "folate", "operator": "<", "value": 7.0, "condition_type": "any_of"},
                                {"metric_id": "transferrin", "operator": "<", "value": 2.0, "condition_type": "any_of"},
                            ],
                            "resulting_state": "at_risk",
                        }
                    ],
                    "output": {"supporting_markers": ["vitamin_b12", "folate", "transferrin", "mcv", "crp"]},
                }
            ]

    evaluator = SignalEvaluator(_HomocysteineCorrectedRegistry())
    out = evaluator.evaluate_all(
        signal_biomarkers={"homocysteine": 15.0, "vitamin_b12": 300.0, "folate": 10.0, "transferrin": 2.5, "crp": 1.0},
        signal_derived={},
        lab_ranges={"homocysteine": {"min": 4.0, "max": 14.0}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "at_risk"


def test_signal_evaluator_uses_shared_state_rank_constant():
    assert SignalEvaluator._STATE_RANK == STATE_RANK


def test_shared_contract_state_rank_is_ordered():
    assert STATE_RANK["optimal"] < STATE_RANK["suboptimal"] < STATE_RANK["at_risk"]


def test_deterministic_threshold_activation_uses_threshold_path():
    class _ThresholdPathRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_threshold_path",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "activation_logic": ACTIVATION_MODE_THRESHOLD,
                    "thresholds": [{"severity": "at_risk", "operator": ">", "value": 100.0}],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_ThresholdPathRegistry())
    # Value is above threshold but still within lab range; threshold path must still activate.
    out = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 110.0},
        signal_derived={},
        lab_ranges={"glucose": {"min": 70.0, "max": 200.0}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "at_risk"


def test_lab_range_activation_uses_lab_range_path():
    class _LabRangePathRegistry:
        @staticmethod
        def get_all_signals():
            return [
                {
                    "signal_id": "signal_lab_range_path",
                    "system": "metabolic",
                    "primary_metric": "glucose",
                    "activation_logic": ACTIVATION_MODE_LAB_RANGE,
                    "activation_config": {
                        "upper_bound_state": "suboptimal",
                        "enable_lower_bound": False,
                        "lower_bound_state": "suboptimal",
                    },
                    # If threshold path were used, this would not activate.
                    "thresholds": [{"severity": "at_risk", "operator": ">", "value": 9999.0}],
                    "override_rules": [],
                    "output": {"supporting_markers": []},
                }
            ]

    evaluator = SignalEvaluator(_LabRangePathRegistry())
    out = evaluator.evaluate_all(
        signal_biomarkers={"glucose": 150.0},
        signal_derived={},
        lab_ranges={"glucose": {"min": 70.0, "max": 100.0}},
    )
    assert len(out) == 1
    assert out[0].signal_state == "suboptimal"


def test_shared_contract_state_keys_match_allowed_states():
    assert set(STATE_RANK.keys()) == set(ALLOWED_SIGNAL_STATES)


_REPO_ROOT = Path(__file__).resolve().parents[3]
_KB_S22_PACKAGE_DIRS = [
    "pkg_iron_deficiency_context",
    "pkg_iron_overload_context",
    "pkg_b12_deficiency_context",
    "pkg_inflammation_crp_context",
    "pkg_hepatic_alt_context",
    "pkg_glucose_dysregulation_hba1c_context",
    "pkg_thyroid_tsh_context",
]
_KB_S22_SIGNAL_CASES = {
    "signal_iron_deficiency_context": {
        "baseline_biomarkers": {
            "ferritin": 10.0,
            "hemoglobin": 130.0,
            "hematocrit": 0.42,
            "mcv": 86.0,
            "mch": 29.0,
            "rdw_cv": 13.0,
            "iron": 15.0,
            "transferrin": 3.0,
        },
        "baseline_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
        "escalation_biomarkers": {
            "ferritin": 10.0,
            "hemoglobin": 110.0,
            "hematocrit": 0.35,
            "mcv": 86.0,
            "mch": 27.0,
            "rdw_cv": 13.5,
            "iron": 15.0,
            "transferrin": 3.0,
        },
        "escalation_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_iron_overload_context": {
        "baseline_biomarkers": {"ferritin": 450.0, "iron": 25.0, "alt": 30.0, "ast": 28.0},
        "baseline_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
        "escalation_biomarkers": {"ferritin": 450.0, "iron": 40.0, "alt": 30.0, "ast": 28.0},
        "escalation_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_b12_deficiency_context": {
        "baseline_biomarkers": {"vitamin_b12": 150.0, "mcv": 90.0, "folate": 10.0, "hemoglobin": 130.0},
        "baseline_ranges": {"vitamin_b12": {"min": 200.0, "max": 900.0}},
        "escalation_biomarkers": {"vitamin_b12": 150.0, "mcv": 100.0, "folate": 10.0, "hemoglobin": 130.0},
        "escalation_ranges": {"vitamin_b12": {"min": 200.0, "max": 900.0}},
    },
    "signal_inflammation_crp_context": {
        "baseline_biomarkers": {"crp": 6.0, "neutrophils": 5.0, "lymphocytes": 1.5, "nlr": 2.0},
        "baseline_ranges": {"crp": {"min": 0.0, "max": 3.0}},
        "escalation_biomarkers": {"crp": 6.0, "neutrophils": 5.0, "lymphocytes": 1.5, "nlr": 4.0},
        "escalation_ranges": {"crp": {"min": 0.0, "max": 3.0}},
    },
    "signal_hepatic_alt_context": {
        "baseline_biomarkers": {"alt": 70.0, "ast": 28.0, "ggt": 35.0, "alp": 100.0, "bilirubin": 12.0},
        "baseline_ranges": {"alt": {"min": 0.0, "max": 40.0}},
        "escalation_biomarkers": {"alt": 70.0, "ast": 28.0, "ggt": 85.0, "alp": 100.0, "bilirubin": 12.0},
        "escalation_ranges": {"alt": {"min": 0.0, "max": 40.0}},
    },
    "signal_glucose_dysregulation_hba1c_context": {
        "baseline_biomarkers": {"hba1c": 6.2, "glucose": 5.5, "triglycerides": 1.2, "insulin": 8.0},
        "baseline_ranges": {"hba1c": {"min": 4.0, "max": 5.6}},
        "escalation_biomarkers": {"hba1c": 6.2, "glucose": 6.5, "triglycerides": 1.2, "insulin": 8.0},
        "escalation_ranges": {"hba1c": {"min": 4.0, "max": 5.6}},
    },
    "signal_thyroid_tsh_context": {
        "baseline_biomarkers": {"tsh": 6.0, "free_t4": 16.0, "free_t3": 4.5},
        "baseline_ranges": {"tsh": {"min": 0.4, "max": 4.5}},
        "escalation_biomarkers": {"tsh": 6.0, "free_t4": 25.0, "free_t3": 4.5},
        "escalation_ranges": {"tsh": {"min": 0.4, "max": 4.5}},
    },
}


def _load_signal_definition(signal_id: str) -> dict:
    registry = SignalRegistry()
    for signal in registry.get_all_signals():
        if signal.get("signal_id") == signal_id:
            return dict(signal)
    raise AssertionError(f"Signal not found in registry: {signal_id}")


def _single_signal_evaluator(signal_id: str) -> SignalEvaluator:
    signal = _load_signal_definition(signal_id)

    class _SingleSignalRegistry:
        @staticmethod
        def get_all_signals():
            return [signal]

    return SignalEvaluator(_SingleSignalRegistry())


@pytest.mark.parametrize("package_dir", _KB_S22_PACKAGE_DIRS)
def test_kbs22_packages_validate_with_no_errors(package_dir: str):
    cmd = [
        sys.executable,
        str(_REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"),
        "--package-dir",
        str(_REPO_ROOT / "knowledge_bus" / "packages" / package_dir),
    ]
    proc = subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "signal_validation: PASS" in proc.stdout


def test_kbs22_signal_libraries_parse_and_use_lab_range_activation():
    for package_dir in _KB_S22_PACKAGE_DIRS:
        signal_library_path = _REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
        payload = yaml.safe_load(signal_library_path.read_text(encoding="utf-8")) or {}
        signals = payload.get("signals", [])
        assert isinstance(signals, list) and signals, f"No signals in {signal_library_path}"
        for signal in signals:
            assert signal.get("activation_logic") == ACTIVATION_MODE_LAB_RANGE


@pytest.mark.parametrize("signal_id", sorted(_KB_S22_SIGNAL_CASES.keys()))
def test_kbs22_new_signals_evaluate_without_error(signal_id: str):
    evaluator = _single_signal_evaluator(signal_id)
    case = _KB_S22_SIGNAL_CASES[signal_id]
    out = evaluator.evaluate_all(
        signal_biomarkers=case["baseline_biomarkers"],
        signal_derived={},
        lab_ranges=case["baseline_ranges"],
    )
    assert len(out) == 1
    assert out[0].signal_id == signal_id


@pytest.mark.parametrize("signal_id", sorted(_KB_S22_SIGNAL_CASES.keys()))
def test_kbs22_new_signals_trigger_suboptimal_then_escalate_to_at_risk(signal_id: str):
    evaluator = _single_signal_evaluator(signal_id)
    case = _KB_S22_SIGNAL_CASES[signal_id]

    baseline = evaluator.evaluate_all(
        signal_biomarkers=case["baseline_biomarkers"],
        signal_derived={},
        lab_ranges=case["baseline_ranges"],
    )
    assert len(baseline) == 1
    assert baseline[0].signal_state == "suboptimal"

    escalated = evaluator.evaluate_all(
        signal_biomarkers=case["escalation_biomarkers"],
        signal_derived={},
        lab_ranges=case["escalation_ranges"],
    )
    assert len(escalated) == 1
    assert escalated[0].signal_state == "at_risk"
