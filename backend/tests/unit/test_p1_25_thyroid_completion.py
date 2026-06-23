"""P1-25 — Thyroid MR-v2 activation completion tests."""

from __future__ import annotations

from pathlib import Path

import yaml

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.runtime_context_evaluator import build_runtime_context_snapshot
from core.analytics.signal_evaluator import SignalEvaluator
from core.analytics.wave1_subsystem_evidence import assemble_wave1_subsystem_evidence
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

THYROID_LAB_RANGES = {
    "free_t3": {"min": 2.0, "max": 4.4},
    "free_t4": {"min": 0.8, "max": 1.8},
    "tsh": {"min": 0.4, "max": 4.5},
    "tpo_ab": {"min": 0.0, "max": 34.0},
}

PROHIBITED_TPOAB_WORDS = (
    "hashimoto",
    "autoimmune thyroid disease",
    "immune system is attacking",
    "thyroid will fail",
    "you have hypothyroidism",
)


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
    raise AssertionError(f"signal {signal_id} not found in {path}")


def _evaluate(signal: dict, biomarkers: dict, *, runtime_context=None, lab_ranges=None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or THYROID_LAB_RANGES,
        runtime_context=runtime_context,
    )


def _ft3_full_context(*, pregnant: bool = False):
    return build_runtime_context_snapshot(
        questionnaire_responses={
            "long_term_medications": [],
            "chronic_conditions": [],
            "pregnancy_status": pregnant,
        },
        lifestyle_factors={"calorie_restriction": False, "fasting": False},
    )


def _tpo_ab_context(*, pregnant: bool | None = None):
    responses: dict = {"long_term_medications": []}
    if pregnant is not None:
        responses["pregnancy_status"] = pregnant
    return build_runtime_context_snapshot(questionnaire_responses=responses)


def _minimal_graph(*, signal_results: list | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="p1-25",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"hormonal": 0.8}),
    )


def _full_scoring_fixture() -> dict:
    return {
        "health_system_scores": {
            "cardiovascular": {"overall_score": 80.0, "missing_biomarkers": []},
            "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
            "liver": {"overall_score": 80.0, "missing_biomarkers": []},
            "kidney": {"overall_score": 80.0, "missing_biomarkers": []},
            "cbc": {"overall_score": 80.0, "missing_biomarkers": []},
            "hormonal": {
                "overall_score": 72.0,
                "missing_biomarkers": [],
                "biomarker_scores": [
                    {"biomarker_name": "tsh"},
                    {"biomarker_name": "free_t4"},
                ],
            },
        }
    }


def _base_panel() -> set[str]:
    return {"tsh", "free_t4", "free_t3", "tpo_ab", "hemoglobin", "creatinine", "glucose"}


def test_ft3_low_on_thyroid_launch_allowlist():
    from core.analytics import domain_score_assembler as dsa

    assert "signal_free_t3_low" in dsa._THYROID_LAUNCH_SIGNAL_IDS
    assert "signal_free_t3_low" not in dsa._THYROID_EXCLUDED_SIGNAL_IDS


def test_tpo_ab_high_on_thyroid_launch_allowlist():
    from core.analytics import domain_score_assembler as dsa

    assert "signal_tpo_ab_high" in dsa._THYROID_LAUNCH_SIGNAL_IDS


def test_ft3_low_suppresses_without_runtime_context():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=None,
    )
    assert results == []


def test_ft3_low_fires_with_full_gates():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=_ft3_full_context(),
    )
    assert {row.signal_id for row in results} == {"signal_free_t3_low"}


def test_ft3_low_suppresses_without_tsh():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "free_t4": 1.2},
        runtime_context=_ft3_full_context(),
    )
    assert results == []


def test_ft3_low_suppresses_without_ft4():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 2.0},
        runtime_context=_ft3_full_context(),
    )
    assert results == []


def test_ft3_low_suppresses_when_tsh_below_lab_range():
    signal = _load_package_signal("pkg_kb47_free_t3_low_low_t3_syndrome", "signal_free_t3_low")
    results = _evaluate(
        signal,
        {"free_t3": 1.5, "tsh": 0.2, "free_t4": 1.2},
        runtime_context=_ft3_full_context(),
    )
    assert results == []


def test_ft3_low_psi_avoids_diagnostic_low_t3_syndrome_framing():
    path = REPO_ROOT / "knowledge_bus/packages/pkg_kb47_free_t3_low_low_t3_syndrome/promoted_signal_intelligence.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    signal = payload["signals"][0]
    consumer_fields = []
    for key in ("primary_metric", "supporting_markers", "contradiction_markers", "missing_data"):
        value = signal.get(key)
        if value:
            consumer_fields.append(yaml.dump(value))
    text = "\n".join(consumer_fields).lower()
    assert "low t3 syndrome" not in text
    assert "hypothyroidism" not in text


def test_tpo_ab_high_fires_when_gates_satisfied():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "tsh": 5.0, "free_t4": 1.2},
        runtime_context=_tpo_ab_context(),
    )
    assert {row.signal_id for row in results} == {"signal_tpo_ab_high"}


def test_tpo_ab_high_suppresses_when_tsh_within_range():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "tsh": 2.0, "free_t4": 1.2},
        runtime_context=_tpo_ab_context(),
    )
    assert results == []


def test_tpo_ab_high_suppresses_when_tsh_absent():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "free_t4": 1.2},
        runtime_context=_tpo_ab_context(),
    )
    assert results == []


def test_tpo_ab_high_suppresses_when_tsh_suppressed():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "tsh": 0.2, "free_t4": 1.2},
        runtime_context=_tpo_ab_context(),
    )
    assert results == []


def test_tpo_ab_high_suppresses_when_ft4_absent():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "tsh": 5.0},
        runtime_context=_tpo_ab_context(),
    )
    assert results == []


def test_tpo_ab_override_escalates_with_low_ft4():
    signal = _load_package_signal(
        "pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern",
        "signal_tpo_ab_high",
    )
    results = _evaluate(
        signal,
        {"tpo_ab": 50.0, "tsh": 5.0, "free_t4": 0.5},
        runtime_context=_tpo_ab_context(),
    )
    assert len(results) == 1
    assert results[0].signal_state == "at_risk"


def test_tpo_ab_psi_has_no_prohibited_wording():
    path = (
        REPO_ROOT
        / "knowledge_bus/packages/pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern/promoted_signal_intelligence.yaml"
    )
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    signal = payload["signals"][0]
    consumer_fields = []
    for key in ("primary_metric", "supporting_markers", "contradiction_markers", "missing_data"):
        value = signal.get(key)
        if value:
            consumer_fields.append(yaml.dump(value))
    text = "\n".join(consumer_fields).lower()
    for phrase in PROHIBITED_TPOAB_WORDS:
        assert phrase not in text


def test_thyroid_card_includes_p1_25_source_specs():
    artefact = get_card_evidence_artefact("wave1_thy_hormonal_axis")
    assert artefact.compile_manifest_ref.endswith("p1_25_thyroid_completion_card_evidence.yaml")
    assert "inv_free_t3_low_low_t3_syndrome" in artefact.source_spec_ids
    assert "inv_tpo_ab_high_autoimmune_hypothyroid_pattern" in artefact.source_spec_ids


def test_thyroid_card_includes_tpo_ab_contextual_marker():
    artefact = get_card_evidence_artefact("wave1_thy_hormonal_axis")
    by_id = {m.marker_id: m for m in artefact.markers}
    assert "tpo_ab" in by_id
    tpo = by_id["tpo_ab"]
    assert tpo.marker_role == "contextual_marker"
    assert tpo.relationship_kind == "contextual_support"
    assert tpo.presence_policy == "optional_on_panel"


def test_thyroid_subsystem_evidence_uses_p1_25_manifest():
    panel = {"tsh", "free_t4", "free_t3", "tpo_ab"}
    rows = assemble_wave1_subsystem_evidence(
        domain_id="wave1_thyroid",
        panel_biomarker_ids=panel,
        rail_biomarker_scores=[
            {"biomarker_name": "tsh"},
            {"biomarker_name": "free_t4"},
        ],
    )
    assert len(rows) == 1
    assert "p1_25_thyroid_completion_card_evidence.yaml" in rows[0].compile_manifest_ref


def test_tpo_ab_high_fires_in_thyroid_domain_allowlist():
    signals = [
        {
            "signal_id": "signal_tpo_ab_high",
            "signal_state": "at_risk",
            "primary_metric": "tpo_ab",
            "system": "endocrine",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_full_scoring_fixture(),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids=_base_panel(),
    )
    thy = [row for row in rows if row.domain_id == "wave1_thyroid"][0]
    assert thy.active_signal_ids == ["signal_tpo_ab_high"]
