"""
Unit tests for deterministic signal registry and evaluator.
"""

from pathlib import Path

import pytest

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
