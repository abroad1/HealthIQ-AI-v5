"""
Unit tests for deterministic signal registry and evaluator.
"""

from pathlib import Path

import pytest

from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry


def _write_signal_library(path: Path, signal_id: str, primary_metric: str = "glucose") -> None:
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
                '      - when: "ignored_in_kb_s14"',
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
                    {"state": "at_risk", "any_of": [{"metric_id": "crp", "operator": ">=", "value": 3.0}]}
                ],
                "output": {"supporting_markers": ["insulin", "glucose"]},
            },
            {
                "signal_id": "signal_beta",
                "system": "inflammation",
                "primary_metric": "crp",
                "supporting_metrics": [],
                "thresholds": [{"severity": "at_risk", "operator": ">=", "value": 3.0}],
                "override_rules": [],
                "output": {"supporting_markers": []},
            },
        ]


def test_signal_evaluator_uses_thresholds_without_override_rules():
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


def test_signal_evaluator_lab_normal_but_flagged_paths():
    evaluator = SignalEvaluator(_StubRegistry())
    results = evaluator.evaluate_all(
        signal_biomarkers={},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    assert len(results) == 1
    assert results[0].signal_id == "signal_alpha"
    assert results[0].lab_normal_but_flagged is True

    results_outside = evaluator.evaluate_all(
        signal_biomarkers={},
        signal_derived={"tyg_index": 9.3},
        lab_ranges={"tyg_index": {"min": 8.0, "max": 9.0}},
    )
    assert results_outside[0].signal_state == "at_risk"
    assert results_outside[0].lab_normal_but_flagged is False

    results_no_ranges = evaluator.evaluate_all(
        signal_biomarkers={},
        signal_derived={"tyg_index": 8.9},
        lab_ranges={},
    )
    assert results_no_ranges[0].lab_normal_but_flagged is False
