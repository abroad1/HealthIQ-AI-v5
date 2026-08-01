"""ARCH-CONV-H — HbA1c compiled-WHY authority runtime proof."""

from __future__ import annotations

import hashlib
from pathlib import Path

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.why_authority_v1 import (
    authority_row_for,
    clear_why_authority_cache,
    resolve_frame_why_authority,
)


REPO = Path(__file__).resolve().parents[3]
HBA1C = "signal_hba1c_high::inv_hba1c_high_glycaemia"
HBA1C_DIABETES = "signal_hba1c_high::inv_hba1c_high_diabetes_range_hyperglycemia"
URATE = "signal_urate_high::inv_uric_acid_high_metabolic"

LAB_RANGES = {
    "hba1c": {"min": 20.0, "max": 42.0},
    "glucose": {"min": 3.9, "max": 5.5},
    "triglycerides": {"min": 0.0, "max": 1.7},
    "hdl_cholesterol": {"min": 1.0, "max": 2.0},
    "alt": {"min": 0.0, "max": 40.0},
    "urate": {"min": 150.0, "max": 420.0},
}

PROHIBITED = (
    "you have diabetes",
    "diagnosed with diabetes",
    "type 1 diabetes",
    "type 2 diabetes",
    "metabolic syndrome diagnosis",
    "you have metabolic syndrome",
    "retinopathy",
    "neuropathy",
    "start medication",
    "pharmacological management",
    "lifestyle intervention",
    "requires lifestyle",
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


def test_canonical_hba1c_resolves_compiled_morphology_context():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_hba1c_high",
        activation_key=HBA1C,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["why_role"] == "morphology_context"
    assert "conditional_why_role" not in row

    findings = _compiled_findings({"hba1c": 45.0})
    assert HBA1C in findings
    assert findings[HBA1C].why_role == "morphology_context"
    assert (
        findings[HBA1C].hypotheses[0].hypothesis_id
        == "hyp_hba1c_elevated_glycaemia_context"
    )
    text = _joined_summaries(findings, {HBA1C})
    assert "non-causal" in text
    assert "does not establish diabetes" in text
    _assert_bounded(text)


def test_competing_diabetes_range_frame_skips_for_why_ownership():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_hba1c_high",
        activation_key=HBA1C_DIABETES,
    )
    assert mode == "skip"
    assert row["authority_state"] == "LEGACY_RETIRED"
    assert row["artefact_path"] is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hba1c_high",
                "activation_key": HBA1C_DIABETES,
                "source_spec_id": "inv_hba1c_high_diabetes_range_hyperglycemia",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "hba1c",
            }
        ],
        biomarker_context={"hba1c": 52.0},
        input_reference_ranges=LAB_RANGES,
    )
    assert root is None


def test_no_dual_serving_hba1c_why_ownership():
    findings = _compiled_findings(
        {"hba1c": 52.0, "triglycerides": 2.5, "hdl_cholesterol": 0.8}
    )
    hba1c_keys = [k for k in findings if k.startswith("signal_hba1c_high::")]
    assert hba1c_keys == [HBA1C]
    assert HBA1C_DIABETES not in findings


def test_diabetes_range_override_is_concern_requiring_confirmation_only():
    rows = _evaluate_rows({"hba1c": 52.0})
    hba1c_signal = next(r for r in rows if r.get("activation_key") == HBA1C)
    assert hba1c_signal.get("signal_state") == "at_risk"

    findings = _compiled_findings({"hba1c": 52.0})
    assert findings[HBA1C].why_role == "morphology_context"
    text = _joined_summaries(findings, {HBA1C})
    assert "clinical confirmation" in text
    assert "does not establish diabetes" in text
    _assert_bounded(text)


def test_tg_hdl_override_is_subordinate_metabolic_pattern_only():
    rows = _evaluate_rows(
        {"hba1c": 45.0, "triglycerides": 2.5, "hdl_cholesterol": 0.8}
    )
    hba1c_signal = next(r for r in rows if r.get("activation_key") == HBA1C)
    assert hba1c_signal.get("signal_state") == "at_risk"

    findings = _compiled_findings(
        {"hba1c": 45.0, "triglycerides": 2.5, "hdl_cholesterol": 0.8}
    )
    text = _joined_summaries(findings, {HBA1C})
    assert "metabolic syndrome" not in text or "does not establish" in text
    assert "you have metabolic syndrome" not in text
    _assert_bounded(text)


def test_missing_tg_hdl_still_emits_basic_hba1c_context():
    findings = _compiled_findings({"hba1c": 45.0})
    assert HBA1C in findings
    assert findings[HBA1C].why_role == "morphology_context"
    text = _joined_summaries(findings, {HBA1C})
    assert "non-causal" in text
    _assert_bounded(text)


def test_adjacent_identities_unchanged_in_register():
    for key in (
        "signal_hba1c_pct_high::inv_hba1c_pct_high_chronic_hyperglycemia_diabetes",
        "signal_hba1c_pct_high::inv_hba1c_pct_high_red_cell_turnover_bias_or_iron_deficiency",
        "signal_glucose_dysregulation_hba1c_context::inv_dysregulation_hba1c_context",
    ):
        assert authority_row_for(key) is None


def test_urate_compiled_authority_unchanged():
    urate = authority_row_for(URATE)
    assert urate["authority_state"] == "COMPILED_ACTIVE"
    assert urate["why_role"] == "morphology_context"

    findings = _compiled_findings({"hba1c": 45.0, "urate": 480.0})
    assert findings[HBA1C].why_role == "morphology_context"
    assert findings[URATE].why_role == "morphology_context"


def test_no_runtime_research_file_read_introduced():
    compiler = (
        REPO / "backend/core/analytics/root_cause_compiler_v1.py"
    ).read_text(encoding="utf-8")
    authority = (REPO / "backend/core/knowledge/why_authority_v1.py").read_text(
        encoding="utf-8"
    )
    for needle in (
        "investigation_specs",
        "Batch_6_Pass_3",
        "inv_hba1c_high_glycaemia.yaml",
    ):
        assert needle not in compiler
        assert needle not in authority


def test_register_delta_and_exclusions():
    assert authority_row_for(HBA1C)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(HBA1C_DIABETES)["authority_state"] == "LEGACY_RETIRED"
    for key in (
        "signal_ferritin_low::inv_ferritin_low_iron_store_depletion",
        "signal_alt_high::inv_alt_high_hepatocellular_injury",
    ):
        assert authority_row_for(key) is None


def test_deterministic_repeatability():
    biomarkers = {"hba1c": 52.0, "triglycerides": 2.5, "hdl_cholesterol": 0.8}
    first = _joined_summaries(_compiled_findings(biomarkers), {HBA1C})
    second = _joined_summaries(_compiled_findings(biomarkers), {HBA1C})
    assert first == second


def test_source_hash_stable():
    raw = (
        REPO / "knowledge_bus/research/investigation_specs/inv_hba1c_high_glycaemia_v1.yaml"
    ).read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest().upper()
        == "2CFA335DEBBA2F430C12E2F0605823B9752A3AD78389F32A7D978B8286501247"
    )
