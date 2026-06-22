"""P1-22 — Thyroid activation pack tests."""

from __future__ import annotations

from pathlib import Path

import yaml

import core.analytics.scoring_policy_registry as scoring_policy_registry
from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.scoring_policy_registry import load_scoring_policy
from core.analytics.signal_evaluator import SignalEvaluator
from core.analytics.wave1_subsystem_evidence import WAVE1_DOMAIN_IDS
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity
from core.scoring.engine import ScoringEngine
from core.scoring.rules import ScoringRules, UNSCORED_REASON

REPO_ROOT = Path(__file__).resolve().parents[3]

THYROID_LAB_RANGES = {
    "tsh": {"min": 0.4, "max": 4.5},
    "free_t4": {"min": 12.0, "max": 22.0},
    "free_t3": {"min": 3.5, "max": 6.5},
}


class _SingleSignalRegistry:
    def __init__(self, signal: dict) -> None:
        self._signal = dict(signal)

    def get_all_signals(self) -> list[dict]:
        return [dict(self._signal)]


def _load_package_signal(package_dir: str, signal_id: str) -> dict:
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
    raise AssertionError(f"signal {signal_id} not found")


def _minimal_graph(*, signal_results: list | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="p1-22",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"hormonal": 0.8}),
    )


def _full_scoring_fixture(*, hormonal_score: float = 72.0) -> dict:
    return {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 80.0, "missing_biomarkers": []},
            "cbc": {"overall_score": 80.0, "missing_biomarkers": []},
            "hormonal": {
                "overall_score": hormonal_score,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "tsh"},
                    {"biomarker_name": "free_t4"},
                ],
            },
        }
    }


def _base_panel() -> set[str]:
    return {
        "tsh",
        "free_t4",
        "free_t3",
        "hemoglobin",
        "creatinine",
        "egfr",
        "alt",
        "glucose",
        "hba1c",
        "ldl_cholesterol",
    }


def test_wave1_domain_ids_include_thyroid():
    assert "wave1_thyroid" in WAVE1_DOMAIN_IDS


def test_production_hormonal_rail_has_lab_range_only_thyroid_markers():
    scoring_policy_registry._policy_cache = None
    policy = load_scoring_policy()
    hormonal = policy.raw["systems"]["hormonal"]
    assert hormonal["system_weight"] == 0.1
    assert hormonal["min_biomarkers_required"] == 1
    assert set(hormonal["biomarkers"]) == {"tsh", "free_t4", "free_t3"}
    for marker_id in ("tsh", "free_t4", "free_t3"):
        spec = policy.raw["biomarkers"][marker_id]
        assert spec["scoring_type"] == "lab_range_only"
        assert "bands" not in spec


def test_tsh_lab_range_only_scoring_without_hardcoded_bands():
    scoring_policy_registry._policy_cache = None
    rules = ScoringRules()
    score, _, reason = rules.calculate_biomarker_score(
        "tsh",
        2.0,
        input_reference_range=THYROID_LAB_RANGES["tsh"],
        value_unit="mIU/L",
    )
    assert reason is None
    assert score > 0
    missing_score, _, missing_reason = rules.calculate_biomarker_score("tsh", 2.0)
    assert missing_reason == UNSCORED_REASON


def test_hormonal_system_orchestration_scores_tsh_from_lab_range():
    scoring_policy_registry._policy_cache = None
    rules = ScoringRules()
    engine = ScoringEngine(rules=rules)
    result = engine._score_health_system(
        "hormonal",
        {"tsh": 2.0},
        None,
        None,
        None,
        input_reference_ranges={"tsh": THYROID_LAB_RANGES["tsh"]},
    )
    assert len(result.biomarker_scores) == 1
    assert result.biomarker_scores[0].unscored_reason is None


def test_ft3_high_requires_tsh_suppressed_companion_gate():
    signal = _load_package_signal(
        "pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis",
        "signal_free_t3_high",
    )
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    blocked = evaluator.evaluate_all(
        signal_biomarkers={"free_t3": 7.0, "tsh": 2.0},
        signal_derived={},
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert blocked == []
    allowed = evaluator.evaluate_all(
        signal_biomarkers={"free_t3": 7.0, "tsh": 0.2},
        signal_derived={},
        lab_ranges=THYROID_LAB_RANGES,
    )
    assert len(allowed) == 1
    assert allowed[0].signal_id == "signal_free_t3_high"


def test_ft3_low_not_in_thyroid_domain_allowlist():
    signals = [
        {
            "signal_id": "signal_free_t3_low",
            "signal_state": "at_risk",
            "primary_metric": "free_t3",
            "system": "hormonal",
        },
        {
            "signal_id": "signal_tsh_high",
            "signal_state": "at_risk",
            "primary_metric": "tsh",
            "system": "hormonal",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_full_scoring_fixture(),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    thy = rows[5]
    assert thy.domain_id == "wave1_thyroid"
    assert thy.active_signal_ids == []


def test_thyroid_domain_includes_ft4_high_when_active():
    signals = [
        {
            "signal_id": "signal_free_t4_high",
            "signal_state": "suboptimal",
            "primary_metric": "free_t4",
            "system": "hormonal",
        },
        {
            "signal_id": "signal_tsh_low",
            "signal_state": "at_risk",
            "primary_metric": "tsh",
            "system": "hormonal",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_full_scoring_fixture(hormonal_score=55.0),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    thy = rows[5]
    assert thy.active_signal_ids == ["signal_free_t4_high"]
    joined = " ".join(
        [
            thy.headline_sentence or "",
            thy.contributor_sentence or "",
            thy.consequence_sentence or "",
        ]
    ).lower()
    assert "hypothyroid" not in joined
    assert "hyperthyroid" not in joined
    assert "kb52c" not in joined


def test_assembler_emits_six_launch_core_domains():
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_full_scoring_fixture(),
        insight_graph=_minimal_graph(),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    assert len(rows) == 6
    assert rows[5].domain_id == "wave1_thyroid"
    assert rows[5].consumer_label == "Thyroid / energy regulation"
    assert rows[5].contributing_system_keys == ["hormonal"]
