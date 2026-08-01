"""ARCH-CONV-F — haematology compiled-WHY authority runtime proof."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.why_authority_v1 import (
    authority_row_for,
    clear_why_authority_cache,
    resolve_frame_why_authority,
)


REPO = Path(__file__).resolve().parents[3]
FERRITIN = "signal_ferritin_high::inv_ferritin_high_overload"
FERRITIN_INFLAM = "signal_ferritin_high::inv_ferritin_high_inflammatory_hyperferritinemia"
FERRITIN_OVERLOAD_CTX = "signal_ferritin_high::inv_ferritin_high_iron_overload_context"
HGB = "signal_hemoglobin_low::inv_hgb_low_anemia"
HGB_NORMOCYTIC = "signal_hgb_low::inv_hgb_low_normocytic_underproduction_context"

LAB_RANGES = {
    "ferritin": {"min": 30.0, "max": 300.0},
    "hemoglobin": {"min": 120.0, "max": 170.0},
    "crp": {"min": 0.0, "max": 5.0},
    "alt": {"min": 0.0, "max": 40.0},
    "iron": {"min": 10.0, "max": 30.0},
    "transferrin_saturation": {"min": 15.0, "max": 50.0},
    "mcv": {"min": 80.0, "max": 100.0},
    "rdw_cv": {"min": 11.0, "max": 15.0},
}

PROHIBITED = (
    "you have haemochromatosis",
    "you have hemochromatosis",
    "you have iron overload",
    "causal iron overload",
    "you need a transfusion",
    "recommend transfusion",
    "venesection",
    "start medication",
    "stop medication",
    "underproduction",
)


def _evaluate_rows(biomarkers: dict[str, float]) -> list[dict]:
    clear_why_authority_cache()
    return [
        row.model_dump()
        for row in SignalEvaluator(SignalRegistry()).evaluate_all(
            signal_biomarkers=biomarkers,
            signal_derived={},
            lab_ranges=LAB_RANGES,
        )
    ]


def _compiled_findings(biomarkers: dict[str, float]) -> dict:
    root = compile_root_cause_v1(
        signal_results=_evaluate_rows(biomarkers),
        biomarker_context=biomarkers,
        input_reference_ranges=LAB_RANGES,
    )
    findings = root.findings if root else []
    return {finding.activation_key: finding for finding in findings if finding.activation_key}


def _joined_summaries(findings: dict, keys: set[str] | None = None) -> str:
    selected = findings if keys is None else {k: findings[k] for k in keys if k in findings}
    return " ".join(
        hypothesis.summary.lower()
        for finding in selected.values()
        for hypothesis in finding.hypotheses
    )


def _assert_bounded(text: str) -> None:
    for phrase in PROHIBITED:
        assert phrase not in text, f"prohibited phrase present: {phrase!r}"


def _assert_no_causal_diagnosis_claim(text: str) -> None:
    lowered = text.lower()
    for phrase in (
        "you have haemochromatosis",
        "you have hemochromatosis",
        "diagnosed with haemochromatosis",
        "diagnosed with hemochromatosis",
        "you have iron overload",
        "causal iron overload",
    ):
        assert phrase not in lowered, f"causal diagnosis claim present: {phrase!r}"


def test_hemoglobin_resolves_compiled_and_emits_anaemia_causal():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_hemoglobin_low",
        activation_key=HGB,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["why_role"] == "causal"

    findings = _compiled_findings({"hemoglobin": 105.0, "mcv": 90.0, "rdw_cv": 13.0})
    assert HGB in findings
    assert findings[HGB].why_role == "causal"
    assert (
        findings[HGB].hypotheses[0].hypothesis_id
        == "hyp_hemoglobin_anaemia_reduced_oxygen_carrying"
    )
    text = _joined_summaries(findings, {HGB})
    assert "anaemia" in text or "oxygen-carrying" in text
    assert "morphology context only" in text
    _assert_bounded(text)


def test_mcv_rdw_remain_subordinate_and_cannot_emit_independent_aetiology():
    findings = _compiled_findings({"hemoglobin": 105.0, "mcv": 90.0, "rdw_cv": 16.0})
    assert HGB in findings
    assert findings[HGB].why_role == "causal"
    text = _joined_summaries(findings, {HGB})
    assert "do not establish aetiology" in text
    assert "underproduction" not in text
    # No independent underproduction competitor emits WHY.
    assert HGB_NORMOCYTIC not in findings
    # Canonical haemoglobin frame remains the owning anaemia WHY lane.
    assert findings[HGB].hypotheses[0].hypothesis_id == (
        "hyp_hemoglobin_anaemia_reduced_oxygen_carrying"
    )


def test_normocytic_underproduction_competitor_skips_for_why_ownership():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_hgb_low",
        activation_key=HGB_NORMOCYTIC,
    )
    assert mode == "skip"
    assert row is not None
    assert row["authority_state"] == "LEGACY_RETIRED"
    assert row["artefact_path"] is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hgb_low",
                "activation_key": HGB_NORMOCYTIC,
                "source_spec_id": "inv_hgb_low_normocytic_underproduction_context",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "hemoglobin",
            }
        ],
        biomarker_context={"hemoglobin": 105.0, "mcv": 90.0},
        input_reference_ranges=LAB_RANGES,
    )
    assert root is None


def test_ferritin_resolves_compiled_as_flat_morphology_context():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_ferritin_high",
        activation_key=FERRITIN,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["why_role"] == "morphology_context"
    assert "conditional_why_role" not in row


@pytest.mark.parametrize(
    "biomarkers",
    [
        {"ferritin": 450.0},
        {"ferritin": 450.0, "crp": 2.0},
        {"ferritin": 450.0, "crp": 12.0},
        {"ferritin": 450.0, "alt": 80.0},
        {"ferritin": 450.0, "iron": 40.0},
        {"ferritin": 450.0, "transferrin_saturation": 70.0},
        {"ferritin": 450.0, "crp": 12.0, "alt": 80.0, "iron": 40.0, "transferrin_saturation": 70.0},
        {"ferritin": 1200.0, "crp": 2.0},
    ],
)
def test_ferritin_never_causal_under_any_input_combination(biomarkers):
    findings = _compiled_findings(biomarkers)
    assert FERRITIN in findings
    assert findings[FERRITIN].why_role == "morphology_context"
    causal = [k for k, f in findings.items() if f.why_role == "causal"]
    assert FERRITIN not in causal
    text = _joined_summaries(findings, {FERRITIN})
    assert "non-causal" in text
    assert "does not establish systemic iron overload" in text
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)


def test_normal_crp_never_creates_causal_iron_overload_authority():
    findings = _compiled_findings({"ferritin": 450.0, "crp": 2.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    text = _joined_summaries(findings, {FERRITIN})
    _assert_no_causal_diagnosis_claim(text)
    _assert_bounded(text)


def test_elevated_crp_and_alt_enrich_context_only():
    artefact = authority_row_for(FERRITIN)
    assert artefact["why_role"] == "morphology_context"
    findings = _compiled_findings({"ferritin": 450.0, "crp": 12.0, "alt": 90.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    hyp = findings[FERRITIN].hypotheses[0]
    assert hyp.hypothesis_id == "hyp_ferritin_elevated_non_causal_context"
    # Context enrichment is encoded in the compiled artefact caveats/evidence, not a role upgrade.
    compiled = REPO / "knowledge_bus/compiled/hypotheses/inv_ferritin_high_overload.yaml"
    body = compiled.read_text(encoding="utf-8").lower()
    assert "elevated crp may support reactive or inflammatory context" in body
    assert "elevated alt may support hepatic or metabolic context" in body
    text = _joined_summaries(findings, {FERRITIN})
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)


def test_serum_iron_alone_never_produces_overload_attribution():
    findings = _compiled_findings({"ferritin": 450.0, "iron": 40.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    text = _joined_summaries(findings, {FERRITIN})
    assert "does not establish systemic iron overload" in text
    body = (
        REPO / "knowledge_bus/compiled/hypotheses/inv_ferritin_high_overload.yaml"
    ).read_text(encoding="utf-8").lower()
    assert "insufficient alone" in body
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)


def test_transferrin_saturation_enriches_but_never_upgrades_to_causal():
    findings = _compiled_findings({"ferritin": 450.0, "transferrin_saturation": 70.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    assert authority_row_for(FERRITIN).get("conditional_why_role") is None
    text = _joined_summaries(findings, {FERRITIN})
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)


def test_missing_corroborators_fail_closed_to_bare_elevation_wording():
    findings = _compiled_findings({"ferritin": 450.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    text = _joined_summaries(findings, {FERRITIN})
    assert "non-causal" in text
    assert "does not establish systemic iron overload" in text
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)


def test_ferritin_extreme_and_hemoglobin_severe_are_concern_escalation_only():
    ferritin_rows = _evaluate_rows({"ferritin": 1200.0})
    ferritin_signal = next(
        r for r in ferritin_rows if r.get("activation_key") == FERRITIN
    )
    assert ferritin_signal.get("signal_state") == "at_risk"

    hgb_rows = _evaluate_rows({"hemoglobin": 70.0})
    hgb_signal = next(r for r in hgb_rows if r.get("activation_key") == HGB)
    assert hgb_signal.get("signal_state") == "at_risk"

    findings = _compiled_findings({"ferritin": 1200.0, "hemoglobin": 70.0})
    assert findings[FERRITIN].why_role == "morphology_context"
    assert findings[HGB].why_role == "causal"
    text = _joined_summaries(findings, {FERRITIN, HGB})
    _assert_bounded(text)
    _assert_no_causal_diagnosis_claim(text)
    assert "transfusion" not in text
    assert "you have haemochromatosis" not in text
    assert "you have hemochromatosis" not in text


def test_all_three_competing_kb52c_frames_skip_for_why_ownership():
    for signal_id, key in (
        ("signal_ferritin_high", FERRITIN_INFLAM),
        ("signal_ferritin_high", FERRITIN_OVERLOAD_CTX),
        ("signal_hgb_low", HGB_NORMOCYTIC),
    ):
        mode, row = resolve_frame_why_authority(signal_id=signal_id, activation_key=key)
        assert mode == "skip"
        assert row["authority_state"] == "LEGACY_RETIRED"
        assert row["artefact_path"] is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_ferritin_high",
                "activation_key": FERRITIN_INFLAM,
                "source_spec_id": "inv_ferritin_high_inflammatory_hyperferritinemia",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "ferritin",
            },
            {
                "signal_id": "signal_ferritin_high",
                "activation_key": FERRITIN_OVERLOAD_CTX,
                "source_spec_id": "inv_ferritin_high_iron_overload_context",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "ferritin",
            },
            {
                "signal_id": "signal_hgb_low",
                "activation_key": HGB_NORMOCYTIC,
                "source_spec_id": "inv_hgb_low_normocytic_underproduction_context",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "hemoglobin",
            },
        ],
        biomarker_context={"ferritin": 450.0, "hemoglobin": 105.0},
        input_reference_ranges=LAB_RANGES,
    )
    assert root is None


def test_register_delta_and_unrelated_authority_unchanged():
    clear_why_authority_cache()
    assert authority_row_for(FERRITIN)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(HGB)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(FERRITIN_INFLAM)["authority_state"] == "LEGACY_RETIRED"
    assert authority_row_for(FERRITIN_OVERLOAD_CTX)["authority_state"] == "LEGACY_RETIRED"
    assert authority_row_for(HGB_NORMOCYTIC)["authority_state"] == "LEGACY_RETIRED"

    # Excluded / unrelated signals remain outside this register cohort.
    for key in (
        "signal_ferritin_low::inv_ferritin_low_iron_store_depletion",
        "signal_transferrin_high::inv_transferrin_high_iron_deficiency_transport_upregulation",
        "signal_urate_high::inv_uric_acid_high_metabolic",
        "signal_hba1c_high::inv_hba1c_high_glycaemia",
        "signal_alt_high::inv_alt_high_hepatocellular_injury",
    ):
        assert authority_row_for(key) is None


def test_no_runtime_research_file_read_introduced():
    compiler = (
        REPO / "backend/core/analytics/root_cause_compiler_v1.py"
    ).read_text(encoding="utf-8")
    authority = (REPO / "backend/core/knowledge/why_authority_v1.py").read_text(encoding="utf-8")
    forbidden = (
        "investigation_specs",
        "Batch_4_Pass_3",
        "Batch_6_Pass_3",
        "inv_ferritin_high_overload_v1.yaml",
        "inv_hgb_low_anemia.yaml",
    )
    for needle in forbidden:
        assert needle not in compiler
        assert needle not in authority


def test_deterministic_repeatability():
    biomarkers = {
        "ferritin": 450.0,
        "hemoglobin": 105.0,
        "crp": 12.0,
        "mcv": 90.0,
    }
    first = _joined_summaries(_compiled_findings(biomarkers), {FERRITIN, HGB})
    second = _joined_summaries(_compiled_findings(biomarkers), {FERRITIN, HGB})
    assert first == second


def test_source_hashes_stable():
    ferritin = (
        REPO / "knowledge_bus/research/investigation_specs/inv_ferritin_high_overload_v1.yaml"
    ).read_bytes()
    hgb = (REPO / "knowledge_bus/research/investigation_specs/inv_hgb_low_anemia.yaml").read_bytes()
    assert (
        hashlib.sha256(ferritin).hexdigest().upper()
        == "758A939E08A0B816D8E995EA1BBBE3AED5F1868112E5D2345ED40A0E4F713E03"
    )
    assert (
        hashlib.sha256(hgb).hexdigest().upper()
        == "9FE3A27CED4FB977C928B64EC0F0AB173CC5BC39D61DD3A33DC274C64AB390F4"
    )
