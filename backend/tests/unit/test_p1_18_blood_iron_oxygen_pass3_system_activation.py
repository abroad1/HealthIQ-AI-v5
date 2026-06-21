"""P1-18 — Blood/iron/oxygen Pass 3 system activation tests."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.signal_evaluator import SignalEvaluator
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

TRANSFERRIN_LAB_RANGES = {
    "transferrin": {"min": 200.0, "max": 360.0},
    "ferritin": {"min": 30.0, "max": 400.0},
    "mch": {"min": 27.0, "max": 33.0},
    "rdw_cv": {"min": 11.5, "max": 14.5},
    "transferrin_saturation": {"min": 20.0, "max": 50.0},
}


class _SingleSignalRegistry:
    def __init__(self, signal: dict) -> None:
        self._signal = dict(signal)

    def get_all_signals(self) -> list[dict]:
        return [dict(self._signal)]


def _load_transferrin_high_signal() -> dict:
    package_dir = "pkg_kb61_transferrin_high_iron_deficiency_transport_upregulation"
    signal_id = "signal_transferrin_high"
    path = REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "signal_library.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for item in payload.get("signals", []):
        if item.get("signal_id") == signal_id:
            activation_key, source_spec_id, package_id = resolve_activation_identity(
                signal_id=signal_id,
                signal_library_path=path,
            )
            compiled = dict(item)
            compiled["activation_key"] = activation_key
            compiled["source_spec_id"] = source_spec_id
            compiled["package_id"] = package_id
            return compiled
    raise AssertionError("signal_transferrin_high not found in pkg_kb61 signal library")


def _minimal_graph(*, signal_results: list | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="p1-18",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"cbc": 0.8}),
    )


def _scoring_fixture() -> dict:
    return {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 80.0, "missing_biomarkers": []},
            "cbc": {
                "overall_score": 65.0,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "hemoglobin"},
                    {"biomarker_name": "hematocrit"},
                    {"biomarker_name": "transferrin"},
                ],
            },
        }
    }


def _base_panel() -> set[str]:
    return {
        "hemoglobin",
        "hematocrit",
        "ferritin",
        "transferrin",
        "mch",
        "rdw_cv",
        "transferrin_saturation",
        "creatinine",
        "egfr",
        "alt",
        "glucose",
        "hba1c",
        "ldl_cholesterol",
    }


def test_transferrin_high_signal_fires_on_lab_range_exceeded():
    signal = _load_transferrin_high_signal()
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    results = evaluator.evaluate_all(
        signal_biomarkers={
            "transferrin": 420.0,
            "ferritin": 25.0,
            "mch": 26.0,
            "rdw_cv": 15.0,
            "transferrin_saturation": 12.0,
        },
        signal_derived={},
        lab_ranges=TRANSFERRIN_LAB_RANGES,
        runtime_context=None,
    )
    assert len(results) == 1
    assert results[0].signal_id == "signal_transferrin_high"
    assert results[0].signal_state in {"suboptimal", "at_risk"}


def test_transferrin_within_range_does_not_fire():
    signal = _load_transferrin_high_signal()
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    results = evaluator.evaluate_all(
        signal_biomarkers={"transferrin": 300.0},
        signal_derived={},
        lab_ranges=TRANSFERRIN_LAB_RANGES,
        runtime_context=None,
    )
    assert results == []


def test_transferrin_high_missing_primary_metric_fails_safely():
    signal = _load_transferrin_high_signal()
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    results = evaluator.evaluate_all(
        signal_biomarkers={"ferritin": 25.0},
        signal_derived={},
        lab_ranges=TRANSFERRIN_LAB_RANGES,
        runtime_context=None,
    )
    assert results == []


def test_lab_provided_transferrin_saturation_accepted_as_biomarker_input():
    signal = _load_transferrin_high_signal()
    deps = signal.get("dependencies", {})
    assert "transferrin_saturation" in deps.get("biomarkers", [])
    assert "transferrin_saturation" not in deps.get("derived_metrics", [])
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    results = evaluator.evaluate_all(
        signal_biomarkers={
            "transferrin": 420.0,
            "transferrin_saturation": 12.0,
        },
        signal_derived={},
        lab_ranges=TRANSFERRIN_LAB_RANGES,
        runtime_context=None,
    )
    assert len(results) == 1


def test_domain_includes_transferrin_high_in_active_signal_ids():
    signals = [
        {
            "signal_id": "signal_transferrin_high",
            "signal_state": "suboptimal",
            "primary_metric": "transferrin",
            "system": "hematologic",
        },
        {
            "signal_id": "signal_hemoglobin_low",
            "signal_state": "at_risk",
            "primary_metric": "hemoglobin",
            "system": "hematologic",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_scoring_fixture(),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    bio = rows[4]
    assert bio.active_signal_ids == ["signal_transferrin_high"]


def test_domain_control_panel_excludes_transferrin_high_when_inactive():
    signals = [
        {
            "signal_id": "signal_transferrin_high",
            "signal_state": "not_observed",
            "primary_metric": "transferrin",
            "system": "hematologic",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_scoring_fixture(),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    bio = rows[4]
    assert bio.active_signal_ids == []
