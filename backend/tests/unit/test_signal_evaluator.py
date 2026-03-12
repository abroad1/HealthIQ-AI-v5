"""
Unit tests for deterministic signal registry and evaluator.
"""

import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4

import pytest
import yaml

from core.contracts.signal_contract import (
    ACTIVATION_MODE_LAB_RANGE,
    ACTIVATION_MODE_THRESHOLD,
    ALLOWED_SIGNAL_STATES,
    STATE_RANK,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from tools.run_golden_panel import run_golden_panel


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

_KB_S22_SIGNAL_NO_TRIGGER_CASES = {
    "signal_iron_deficiency_context": {
        "biomarkers": {
            "ferritin": 80.0,
            "hemoglobin": 100.0,
            "hematocrit": 0.34,
            "mcv": 76.0,
            "mch": 25.0,
            "rdw_cv": 15.0,
            "iron": 8.0,
            "transferrin": 4.0,
        },
        "ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_iron_overload_context": {
        "biomarkers": {"ferritin": 200.0, "iron": 45.0, "alt": 70.0, "ast": 55.0},
        "ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_b12_deficiency_context": {
        "biomarkers": {"vitamin_b12": 450.0, "mcv": 102.0, "folate": 5.0, "hemoglobin": 110.0},
        "ranges": {"vitamin_b12": {"min": 200.0, "max": 900.0}},
    },
    "signal_inflammation_crp_context": {
        "biomarkers": {"crp": 2.0, "neutrophils": 8.0, "lymphocytes": 0.8, "nlr": 5.0},
        "ranges": {"crp": {"min": 0.0, "max": 3.0}},
    },
    "signal_hepatic_alt_context": {
        "biomarkers": {"alt": 30.0, "ast": 55.0, "ggt": 90.0, "alp": 150.0, "bilirubin": 22.0},
        "ranges": {"alt": {"min": 0.0, "max": 40.0}},
    },
    "signal_glucose_dysregulation_hba1c_context": {
        "biomarkers": {"hba1c": 5.2, "glucose": 6.8, "triglycerides": 2.0, "insulin": 12.0},
        "ranges": {"hba1c": {"min": 4.0, "max": 5.6}},
    },
    "signal_thyroid_tsh_context": {
        "biomarkers": {"tsh": 2.0, "free_t4": 26.0, "free_t3": 7.5},
        "ranges": {"tsh": {"min": 0.4, "max": 4.5}},
    },
}

_KB_S22_PACKAGE_PATHS = [
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_iron_deficiency_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_iron_overload_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_b12_deficiency_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_inflammation_crp_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_hepatic_alt_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_glucose_dysregulation_hba1c_context",
    _REPO_ROOT / "knowledge_bus" / "packages" / "pkg_thyroid_tsh_context",
]

_KB_S24_PACKAGE_DIRS = [
    "pkg_s24_alt_high_hepatocellular_injury",
    "pkg_s24_creatinine_high_renal",
    "pkg_s24_crp_high_inflammation",
    "pkg_s24_ferritin_high_overload",
    "pkg_s24_ferritin_low_iron_deficiency",
    "pkg_s24_hba1c_high_glycaemia",
    "pkg_s24_ldl_high_dyslipidaemia",
    "pkg_s24_triglycerides_high_metabolic",
    "pkg_s24_tsh_high_hypothyroidism",
    "pkg_s24_tsh_low_hyperthyroidism",
]

_KB_S24_SIGNAL_CASES = {
    "signal_alt_high": {
        "no_trigger_biomarkers": {"alt": 30.0, "bilirubin": 12.0, "alp": 100.0},
        "baseline_biomarkers": {"alt": 70.0, "bilirubin": 12.0, "alp": 100.0},
        "escalation_biomarkers": {"alt": 70.0, "bilirubin": 25.0, "alp": 100.0},
        "lab_ranges": {"alt": {"min": 0.0, "max": 40.0}},
    },
    "signal_creatinine_high": {
        "no_trigger_biomarkers": {"creatinine": 90.0, "egfr": 90.0, "potassium": 4.5},
        "baseline_biomarkers": {"creatinine": 140.0, "egfr": 90.0, "potassium": 4.5},
        "escalation_biomarkers": {"creatinine": 140.0, "egfr": 90.0, "potassium": 5.8},
        "lab_ranges": {"creatinine": {"min": 50.0, "max": 110.0}},
    },
    "signal_crp_high": {
        "no_trigger_biomarkers": {"crp": 2.0, "white_blood_cells": 7.0, "neutrophils": 4.0, "albumin": 42.0},
        "baseline_biomarkers": {"crp": 6.0, "white_blood_cells": 7.0, "neutrophils": 4.0, "albumin": 42.0},
        "escalation_biomarkers": {"crp": 6.0, "white_blood_cells": 13.0, "neutrophils": 8.0, "albumin": 42.0},
        "lab_ranges": {"crp": {"min": 0.0, "max": 3.0}},
    },
    "signal_ferritin_high": {
        "no_trigger_biomarkers": {"ferritin": 200.0},
        "baseline_biomarkers": {"ferritin": 450.0},
        "escalation_biomarkers": {"ferritin": 1200.0},
        "lab_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_ferritin_low": {
        "no_trigger_biomarkers": {"ferritin": 80.0, "hemoglobin": 130.0, "mcv": 90.0},
        "baseline_biomarkers": {"ferritin": 20.0, "hemoglobin": 130.0, "mcv": 90.0},
        "escalation_biomarkers": {"ferritin": 20.0, "hemoglobin": 110.0, "mcv": 90.0},
        "lab_ranges": {"ferritin": {"min": 30.0, "max": 300.0}},
    },
    "signal_hba1c_high": {
        "no_trigger_biomarkers": {"hba1c": 5.2, "triglycerides": 1.2, "hdl_cholesterol": 1.3},
        "baseline_biomarkers": {"hba1c": 6.2, "triglycerides": 1.2, "hdl_cholesterol": 1.3},
        "escalation_biomarkers": {"hba1c": 6.2, "triglycerides": 2.2, "hdl_cholesterol": 0.8},
        "lab_ranges": {"hba1c": {"min": 4.0, "max": 5.6}},
    },
    "signal_ldl_cholesterol_high": {
        "no_trigger_biomarkers": {"ldl_cholesterol": 2.5, "non_hdl_cholesterol": 4.0},
        "baseline_biomarkers": {"ldl_cholesterol": 4.5, "non_hdl_cholesterol": 4.0},
        "escalation_biomarkers": {"ldl_cholesterol": 5.2, "non_hdl_cholesterol": 4.0},
        "lab_ranges": {"ldl_cholesterol": {"min": 0.0, "max": 3.0}},
    },
    "signal_triglycerides_high": {
        "no_trigger_biomarkers": {"triglycerides": 1.2, "hba1c": 30.0},
        "baseline_biomarkers": {"triglycerides": 3.0, "hba1c": 30.0},
        "escalation_biomarkers": {"triglycerides": 11.0, "hba1c": 30.0},
        "lab_ranges": {"triglycerides": {"min": 0.0, "max": 1.7}},
    },
    "signal_tsh_high": {
        "no_trigger_biomarkers": {"tsh": 2.0, "free_t4": 16.0},
        "baseline_biomarkers": {"tsh": 6.0, "free_t4": 16.0},
        "escalation_biomarkers": {"tsh": 11.0, "free_t4": 16.0},
        "lab_ranges": {"tsh": {"min": 0.4, "max": 4.5}},
    },
    "signal_tsh_low": {
        "no_trigger_biomarkers": {"tsh": 2.0, "free_t4": 16.0, "free_t3": 5.0},
        "baseline_biomarkers": {"tsh": 0.2, "free_t4": 16.0, "free_t3": 5.0},
        "escalation_biomarkers": {"tsh": 0.2, "free_t4": 24.0, "free_t3": 5.0},
        "lab_ranges": {"tsh": {"min": 0.4, "max": 4.5}},
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
    # Escalation-only invariant
    assert STATE_RANK[escalated[0].signal_state] >= STATE_RANK[baseline[0].signal_state]


@pytest.mark.parametrize("signal_id", sorted(_KB_S22_SIGNAL_NO_TRIGGER_CASES.keys()))
def test_kbs23_investigation_signals_do_not_trigger_when_primary_in_range(signal_id: str):
    evaluator = _single_signal_evaluator(signal_id)
    case = _KB_S22_SIGNAL_NO_TRIGGER_CASES[signal_id]
    out = evaluator.evaluate_all(
        signal_biomarkers=case["biomarkers"],
        signal_derived={},
        lab_ranges=case["ranges"],
    )
    assert out == []


def test_kbs23_tsh_lab_range_directionality_low_and_high_trigger_suboptimal():
    evaluator = _single_signal_evaluator("signal_thyroid_tsh_context")
    lab_range = {"tsh": {"min": 0.4, "max": 4.5}}

    low_out = evaluator.evaluate_all(
        signal_biomarkers={"tsh": 0.2, "free_t4": 16.0, "free_t3": 4.5},
        signal_derived={},
        lab_ranges=lab_range,
    )
    high_out = evaluator.evaluate_all(
        signal_biomarkers={"tsh": 6.0, "free_t4": 16.0, "free_t3": 4.5},
        signal_derived={},
        lab_ranges=lab_range,
    )
    assert len(low_out) == 1 and low_out[0].signal_state == "suboptimal"
    assert len(high_out) == 1 and high_out[0].signal_state == "suboptimal"


def _normalise_panel_fixture_for_golden_runner(panel_payload: dict) -> dict:
    """
    Adapt legacy panel fixture variants into golden-runner input contract.
    Leaves canonical fixtures unchanged.
    """
    payload = dict(panel_payload)
    biomarkers = payload.get("biomarkers")

    # Legacy panels store biomarkers as list[{name,value,unit,...}]
    if isinstance(biomarkers, list):
        mapped = {}
        for row in biomarkers:
            if not isinstance(row, dict):
                continue
            name = str(row.get("name", "")).strip()
            if not name:
                continue
            mapped[name] = {
                "value": row.get("value"),
                "unit": row.get("unit", ""),
                "reference_range": row.get("reference_range"),
            }
        payload["biomarkers"] = mapped

    # Keep user shape compatible with orchestrator paths used by golden runner.
    user = payload.get("user")
    if not isinstance(user, dict):
        user = {}
    if "gender" not in user:
        if isinstance(user.get("biological_sex"), str):
            user["gender"] = user["biological_sex"]
        else:
            user["gender"] = "female"
    user.setdefault("age", 40)
    user.setdefault("user_id", str(uuid4()))
    payload["user"] = user
    return payload


def test_kbs23_catalogue_panel_harness_runs_all_panel_fixtures(tmp_path):
    panel_root = _REPO_ROOT / "backend" / "tests" / "fixtures" / "panels"
    panel_paths = sorted(panel_root.glob("*.json"))
    assert panel_paths, "No panel fixtures found in backend/tests/fixtures/panels"

    for panel_path in panel_paths:
        raw_payload = json.loads(panel_path.read_text(encoding="utf-8"))
        fixture_payload = _normalise_panel_fixture_for_golden_runner(raw_payload)
        prepared_fixture = tmp_path / f"{panel_path.stem}_golden_compatible.json"
        prepared_fixture.write_text(
            json.dumps(fixture_payload, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        run_dir, analysis_result = run_golden_panel(
            fixture_path=prepared_fixture,
            output_root=tmp_path,
            run_id=f"kb-s23-{panel_path.stem}",
            write_narrative=False,
        )

        assert run_dir.exists()
        assert isinstance(analysis_result, dict)
        assert analysis_result
        meta = analysis_result.get("meta", {})
        ig = meta.get("insight_graph", {}) if isinstance(meta, dict) else {}
        assert isinstance(ig.get("signal_results"), list)


def _collect_metric_ids_from_signal_library(path: Path) -> set[str]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    metric_ids: set[str] = set()
    for signal in payload.get("signals", []):
        if not isinstance(signal, dict):
            continue
        primary = signal.get("primary_metric")
        if isinstance(primary, str) and primary.strip():
            metric_ids.add(primary)
        for sm in signal.get("supporting_metrics", []):
            if isinstance(sm, str) and sm.strip():
                metric_ids.add(sm)
        deps = signal.get("dependencies", {})
        if isinstance(deps, dict):
            for bm in deps.get("biomarkers", []):
                if isinstance(bm, str) and bm.strip():
                    metric_ids.add(bm)
        for rule in signal.get("override_rules", []):
            if not isinstance(rule, dict):
                continue
            for cond in rule.get("conditions", []):
                if not isinstance(cond, dict):
                    continue
                metric_id = cond.get("metric_id")
                if isinstance(metric_id, str) and metric_id.strip():
                    metric_ids.add(metric_id)
    return metric_ids


def test_kbs23_kbs22_investigation_metric_ids_are_ssot_canonical():
    ssot_path = _REPO_ROOT / "backend" / "ssot" / "biomarkers.yaml"
    ssot_payload = yaml.safe_load(ssot_path.read_text(encoding="utf-8")) or {}
    canonical_keys = set((ssot_payload.get("biomarkers") or {}).keys())
    assert canonical_keys, "Failed to load canonical biomarker keys from SSOT"

    unknown_by_package = {}
    for package_path in _KB_S22_PACKAGE_PATHS:
        signal_library_path = package_path / "signal_library.yaml"
        metric_ids = _collect_metric_ids_from_signal_library(signal_library_path)
        unknown = sorted(metric_ids - canonical_keys)
        if unknown:
            unknown_by_package[str(package_path)] = unknown

    assert not unknown_by_package, (
        "Unknown metric_id values found in KB-S22 investigation packages: "
        f"{unknown_by_package}"
    )


def _kbs24_signal_specs() -> list[tuple[str, dict]]:
    specs: list[tuple[str, dict]] = []
    for package_dir in _KB_S24_PACKAGE_DIRS:
        signal_library_path = _REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
        payload = yaml.safe_load(signal_library_path.read_text(encoding="utf-8")) or {}
        signals = payload.get("signals", [])
        assert isinstance(signals, list) and len(signals) == 1
        signal = dict(signals[0])
        specs.append((signal["signal_id"], signal))
    return specs


@pytest.mark.parametrize("package_dir", _KB_S24_PACKAGE_DIRS)
def test_kbs24_packages_validate_with_no_errors(package_dir: str):
    cmd = [
        sys.executable,
        str(_REPO_ROOT / "backend" / "scripts" / "validate_knowledge_package.py"),
        "--package-dir",
        str(_REPO_ROOT / "knowledge_bus" / "packages" / package_dir),
    ]
    proc = subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "signal_validation: PASS" in proc.stdout


def test_kbs24_signal_libraries_parse_and_use_lab_range_activation():
    for package_dir in _KB_S24_PACKAGE_DIRS:
        signal_library_path = _REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
        payload = yaml.safe_load(signal_library_path.read_text(encoding="utf-8")) or {}
        signals = payload.get("signals", [])
        assert isinstance(signals, list) and signals, f"No signals in {signal_library_path}"
        for signal in signals:
            assert signal.get("activation_logic") == ACTIVATION_MODE_LAB_RANGE


@pytest.mark.parametrize("signal_id", sorted(_KB_S24_SIGNAL_CASES.keys()))
def test_kbs24_signals_no_trigger_when_primary_in_range(signal_id: str):
    evaluator = _single_signal_evaluator(signal_id)
    case = _KB_S24_SIGNAL_CASES[signal_id]

    out = evaluator.evaluate_all(
        signal_biomarkers=case["no_trigger_biomarkers"],
        signal_derived={},
        lab_ranges=case["lab_ranges"],
    )
    assert out == []


@pytest.mark.parametrize("signal_id", sorted(_KB_S24_SIGNAL_CASES.keys()))
def test_kbs24_signals_trigger_suboptimal_then_escalate(signal_id: str):
    evaluator = _single_signal_evaluator(signal_id)
    case = _KB_S24_SIGNAL_CASES[signal_id]

    baseline = evaluator.evaluate_all(
        signal_biomarkers=case["baseline_biomarkers"],
        signal_derived={},
        lab_ranges=case["lab_ranges"],
    )
    assert len(baseline) == 1
    assert baseline[0].signal_state == "suboptimal"

    escalated = evaluator.evaluate_all(
        signal_biomarkers=case["escalation_biomarkers"],
        signal_derived={},
        lab_ranges=case["lab_ranges"],
    )
    assert len(escalated) == 1
    assert escalated[0].signal_state == "at_risk"
    assert STATE_RANK[escalated[0].signal_state] >= STATE_RANK[baseline[0].signal_state]
