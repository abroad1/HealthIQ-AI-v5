"""P1-26 — MR-v2 iron and homocysteine activation tests."""

from __future__ import annotations

import inspect
from pathlib import Path

import yaml

from core.analytics.domain_score_assembler import assemble_consumer_domain_scores_v1
from core.analytics.signal_evaluator import SignalEvaluator
from core.contracts.confidence_model_v1 import ConfidenceModelV1
from core.contracts.insight_graph_v1 import InsightGraphV1
from core.knowledge.health_system_card_evidence import get_card_evidence_artefact
from core.knowledge.signal_activation_identity_v1 import resolve_activation_identity

REPO_ROOT = Path(__file__).resolve().parents[3]

IRON_LAB_RANGES = {
    "iron": {"min": 10.0, "max": 30.0},
    "ferritin": {"min": 30.0, "max": 400.0},
    "transferrin_saturation": {"min": 20.0, "max": 50.0},
    "crp": {"min": 0.0, "max": 5.0},
    "alt": {"min": 7.0, "max": 55.0},
}

HCY_LAB_RANGES = {
    "homocysteine": {"min": 5.0, "max": 15.0},
    "active_b12": {"min": 37.5, "max": 188.0},
    "folate": {"min": 3.0, "max": 20.0},
    "creatinine": {"min": 60.0, "max": 110.0},
}

IRON_PROHIBITED = (
    "iron deficiency diagnosis",
    "anaemia of inflammation",
    "haemochromatosis",
)

HCY_PROHIBITED = (
    "methylation impairment",
    "kidney disease",
    "cardiovascular risk",
    "vascular risk",
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


def _evaluate(signal: dict, biomarkers: dict, *, lab_ranges: dict | None = None):
    evaluator = SignalEvaluator(_SingleSignalRegistry(signal))
    return evaluator.evaluate_all(
        signal_biomarkers=biomarkers,
        signal_derived={},
        lab_ranges=lab_ranges or IRON_LAB_RANGES,
    )


def _consumer_psi_text(package_dir: str) -> str:
    path = REPO_ROOT / "knowledge_bus" / "packages" / package_dir / "promoted_signal_intelligence.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    signal = payload["signals"][0]
    chunks = []
    for key in ("primary_metric", "supporting_markers", "contradiction_markers", "missing_data"):
        if signal.get(key):
            chunks.append(yaml.dump(signal[key]))
    return "\n".join(chunks).lower()


def _minimal_graph(*, signal_results: list | None = None) -> InsightGraphV1:
    return InsightGraphV1(
        analysis_id="p1-26",
        signal_results=signal_results or [],
        system_capacity_scores={},
        confidence=ConfidenceModelV1(cluster_confidence={"cbc": 0.8, "cardiovascular": 0.8}),
    )


def _bio_scoring_fixture() -> dict:
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
                ],
            },
        }
    }


def test_iron_low_signal_in_blood_iron_oxygen_allowlist_after_p1_26():
    from core.analytics import domain_score_assembler as dsa

    assert "signal_iron_low" in dsa._BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS


def test_iron_high_signal_in_blood_iron_oxygen_allowlist_after_p1_26():
    from core.analytics import domain_score_assembler as dsa

    assert "signal_iron_high" in dsa._BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS


def test_transferrin_high_remains_in_blood_iron_oxygen_allowlist():
    from core.analytics import domain_score_assembler as dsa

    assert "signal_transferrin_high" in dsa._BLOOD_IRON_OXYGEN_LAUNCH_SIGNAL_IDS


def test_homocysteine_assembler_routing_unchanged():
    from core.analytics import domain_score_assembler as dsa

    source = inspect.getsource(dsa._is_wave1_cardiovascular)
    assert '"homocysteine" in sid' in source
    assert '"non_hdl" in primary' in source


def test_iron_low_absolute_fires_with_ferritin_low_and_tsat_low():
    signal = _load_package_signal(
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "signal_iron_low",
    )
    results = _evaluate(signal, {"iron": 8.0, "ferritin": 20.0, "transferrin_saturation": 15.0, "crp": 2.0})
    assert {row.signal_id for row in results} == {"signal_iron_low"}


def test_iron_low_absolute_suppresses_without_tsat():
    signal = _load_package_signal(
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "signal_iron_low",
    )
    results = _evaluate(signal, {"iron": 8.0, "ferritin": 20.0, "crp": 2.0})
    assert results == []


def test_iron_low_functional_fires_with_crp_high_and_ferritin_normal():
    signal = _load_package_signal(
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "signal_iron_low",
    )
    results = _evaluate(
        signal,
        {"iron": 8.0, "ferritin": 100.0, "transferrin_saturation": 15.0, "crp": 10.0},
    )
    assert {row.signal_id for row in results} == {"signal_iron_low"}


def test_iron_low_functional_suppresses_when_ferritin_low():
    signal = _load_package_signal(
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "signal_iron_low",
    )
    results = _evaluate(
        signal,
        {"iron": 8.0, "ferritin": 20.0, "transferrin_saturation": 15.0, "crp": 10.0},
    )
    assert results == []


def test_iron_high_overload_fires_with_tsat_high_and_ferritin_above_range():
    signal = _load_package_signal(
        "pkg_kb52c_iron_high_iron_overload_context",
        "signal_iron_high",
    )
    results = _evaluate(
        signal,
        {"iron": 35.0, "ferritin": 500.0, "transferrin_saturation": 60.0, "alt": 20.0},
    )
    assert {row.signal_id for row in results} == {"signal_iron_high"}


def test_iron_high_overload_suppresses_without_tsat():
    signal = _load_package_signal(
        "pkg_kb52c_iron_high_iron_overload_context",
        "signal_iron_high",
    )
    results = _evaluate(signal, {"iron": 35.0, "ferritin": 500.0, "alt": 20.0})
    assert results == []


def test_iron_high_overload_ctr_alt_high_weakens_overload_interpretation():
    text = _consumer_psi_text("pkg_kb52c_iron_high_iron_overload_context")
    assert "ctr_alt_high" in text or "liver injury" in text


def test_homocysteine_b_vitamin_fires_with_active_b12_and_folate_present():
    signal = _load_package_signal(
        "pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment",
        "signal_homocysteine_high",
    )
    results = _evaluate(
        signal,
        {"homocysteine": 20.0, "active_b12": 80.0, "folate": 8.0, "mcv": 95.0},
        lab_ranges=HCY_LAB_RANGES,
    )
    assert {row.signal_id for row in results} == {"signal_homocysteine_high"}


def test_homocysteine_renal_fires_with_creatinine_high():
    signal = _load_package_signal(
        "pkg_kb52c_homocysteine_high_renal_clearance_reduction",
        "signal_homocysteine_high",
    )
    results = _evaluate(
        signal,
        {"homocysteine": 20.0, "creatinine": 130.0, "folate": 8.0, "active_b12": 80.0},
        lab_ranges=HCY_LAB_RANGES,
    )
    assert {row.signal_id for row in results} == {"signal_homocysteine_high"}


def test_homocysteine_no_methylation_impairment_wording_in_consumer_fields():
    text = _consumer_psi_text("pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment")
    assert "methylation impairment" not in text


def test_homocysteine_no_primary_cardiovascular_risk_framing():
    text = _consumer_psi_text("pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment")
    assert "cardiovascular risk" not in text
    assert "vascular risk" not in text


def test_homocysteine_no_kidney_disease_diagnosis_wording():
    text = _consumer_psi_text("pkg_kb52c_homocysteine_high_renal_clearance_reduction")
    assert "kidney disease" not in text


def test_iron_packages_no_prohibited_wording_in_consumer_fields():
    for package_dir in (
        "pkg_kb52c_iron_low_absolute_iron_deficiency",
        "pkg_kb52c_iron_low_functional_iron_restriction_inflammation",
        "pkg_kb52c_iron_high_iron_overload_context",
    ):
        text = _consumer_psi_text(package_dir)
        for phrase in IRON_PROHIBITED:
            assert phrase not in text, f"{phrase} found in {package_dir}"


def test_wave1_bio_oxygen_card_includes_iron_source_specs():
    artefact = get_card_evidence_artefact("wave1_bio_oxygen_carrying_capacity")
    assert artefact.compile_manifest_ref.endswith("p1_26_iron_homocysteine_card_evidence.yaml")
    assert "inv_iron_low_absolute_iron_deficiency" in artefact.source_spec_ids
    assert "inv_iron_low_functional_iron_restriction_inflammation" in artefact.source_spec_ids
    assert "inv_iron_high_iron_overload_context" in artefact.source_spec_ids
    assert "inv_transferrin_high_iron_deficiency_transport_upregulation" in artefact.source_spec_ids


def test_wave1_cv_homocysteine_card_updated_to_kb52c_packages():
    artefact = get_card_evidence_artefact("wave1_cv_homocysteine_pathway")
    assert artefact.compile_manifest_ref.endswith("p1_26_iron_homocysteine_card_evidence.yaml")
    assert "inv_homocysteine_high_b_vitamin_related_methylation_impairment" in artefact.source_spec_ids
    assert "inv_homocysteine_high_renal_clearance_reduction" in artefact.source_spec_ids
    refs = artefact.provenance.get("package_refs", [])
    assert "pkg_s24" not in str(refs)
    assert "pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment" in refs


def test_iron_low_fires_in_blood_iron_oxygen_domain_allowlist():
    signals = [
        {
            "signal_id": "signal_iron_low",
            "signal_state": "at_risk",
            "primary_metric": "iron",
            "system": "hematologic",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result=_bio_scoring_fixture(),
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"hemoglobin", "hematocrit", "iron", "ferritin"},
    )
    bio = [row for row in rows if row.domain_id == "wave1_blood_iron_oxygen"][0]
    assert "signal_iron_low" in bio.active_signal_ids


def test_homocysteine_high_routes_to_cardiovascular_domain():
    signals = [
        {
            "signal_id": "signal_homocysteine_high",
            "signal_state": "at_risk",
            "primary_metric": "homocysteine",
            "system": "metabolic",
        },
    ]
    rows, _ = assemble_consumer_domain_scores_v1(
        scoring_result={
            "health_system_scores": {
                "cardiovascular": {"overall_score": 70.0, "missing_biomarkers": []},
                "metabolic": {"overall_score": 80.0, "missing_biomarkers": []},
                "liver": {"overall_score": 80.0, "missing_biomarkers": []},
                "kidney": {"overall_score": 80.0, "missing_biomarkers": []},
                "cbc": {"overall_score": 80.0, "missing_biomarkers": []},
            }
        },
        insight_graph=_minimal_graph(signal_results=signals),
        idl_bundle=None,
        derived_ratios_meta=None,
        panel_biomarker_ids={"homocysteine", "ldl_cholesterol"},
    )
    cv = [row for row in rows if row.domain_id == "wave1_cardiovascular"][0]
    assert "signal_homocysteine_high" in cv.active_signal_ids
