"""ARCH-CONV-G — urate compiled-WHY authority runtime proof."""

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
URATE = "signal_urate_high::inv_uric_acid_high_metabolic"
URATE_GOUT = "signal_urate_high::inv_urate_high_gout_crystal_deposition_risk"
CREAT = "signal_creatinine_high::inv_creatinine_high_renal"
UREA = "signal_urea_high::inv_urea_high_renal"

LAB_RANGES = {
    "urate": {"min": 150.0, "max": 420.0},
    "creatinine": {"min": 45.0, "max": 105.0},
    "urea": {"min": 2.5, "max": 7.8},
    "egfr": {"min": 60.0, "max": 120.0},
    "triglycerides": {"min": 0.0, "max": 1.7},
}

PROHIBITED = (
    "you have gout",
    "diagnosed with gout",
    "you have ckd",
    "chronic kidney disease",
    "renal failure",
    "you need treatment",
    "start medication",
    "stop medication",
    "justify renal review",
    "gout-focused assessment",
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


def test_canonical_urate_resolves_compiled_morphology_context():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_urate_high",
        activation_key=URATE,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["why_role"] == "morphology_context"
    assert "conditional_why_role" not in row

    findings = _compiled_findings({"urate": 480.0})
    assert URATE in findings
    assert findings[URATE].why_role == "morphology_context"
    assert (
        findings[URATE].hypotheses[0].hypothesis_id
        == "hyp_urate_elevated_non_causal_context"
    )
    text = _joined_summaries(findings, {URATE})
    assert "non-causal" in text
    assert "does not establish gout" in text
    _assert_bounded(text)


def test_competing_gout_frame_skips_for_why_ownership():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_urate_high",
        activation_key=URATE_GOUT,
    )
    assert mode == "skip"
    assert row["authority_state"] == "LEGACY_RETIRED"
    assert row["artefact_path"] is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_urate_high",
                "activation_key": URATE_GOUT,
                "source_spec_id": "inv_urate_high_gout_crystal_deposition_risk",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "urate",
            }
        ],
        biomarker_context={"urate": 480.0},
        input_reference_ranges=LAB_RANGES,
    )
    assert root is None


def test_no_dual_serving_urate_why_ownership():
    findings = _compiled_findings({"urate": 480.0, "creatinine": 140.0, "egfr": 45.0})
    urate_keys = [k for k in findings if k.startswith("signal_urate_high::")]
    assert urate_keys == [URATE]
    assert URATE_GOUT not in findings


def test_egfr_override_is_concern_escalation_only():
    rows = _evaluate_rows({"urate": 480.0, "egfr": 45.0})
    urate_signal = next(r for r in rows if r.get("activation_key") == URATE)
    assert urate_signal.get("signal_state") == "at_risk"

    findings = _compiled_findings({"urate": 480.0, "egfr": 45.0})
    assert findings[URATE].why_role == "morphology_context"
    text = _joined_summaries(findings, {URATE})
    assert "chronic kidney disease" not in text
    assert "renal failure" not in text
    _assert_bounded(text)


def test_missing_egfr_still_emits_basic_urate_context():
    findings = _compiled_findings({"urate": 480.0})
    assert URATE in findings
    assert findings[URATE].why_role == "morphology_context"
    rows = _evaluate_rows({"urate": 480.0})
    urate_signal = next(r for r in rows if r.get("activation_key") == URATE)
    assert urate_signal.get("signal_state") in {"suboptimal", "at_risk"}
    # Without low eGFR, renal-risk override should not be required for emission.
    text = _joined_summaries(findings, {URATE})
    assert "non-causal" in text
    _assert_bounded(text)


def test_creatinine_and_urea_compiled_authority_unchanged():
    creat = authority_row_for(CREAT)
    urea = authority_row_for(UREA)
    assert creat["authority_state"] == "COMPILED_ACTIVE"
    assert creat["why_role"] == "causal"
    assert urea["authority_state"] == "COMPILED_ACTIVE"
    assert urea["why_role"] == "morphology_context"

    findings = _compiled_findings({"creatinine": 140.0, "urea": 10.0, "urate": 480.0})
    assert findings[CREAT].why_role == "causal"
    assert findings[UREA].why_role == "morphology_context"
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
        "Batch_7_Pass_3",
        "inv_uric_acid_high_metabolic.yaml",
    ):
        assert needle not in compiler
        assert needle not in authority


def test_register_delta_and_exclusions():
    assert authority_row_for(URATE)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(URATE_GOUT)["authority_state"] == "LEGACY_RETIRED"
    for key in (
        "signal_hba1c_high::inv_hba1c_high_glycaemia",
        "signal_ferritin_low::inv_ferritin_low_iron_store_depletion",
        "signal_alt_high::inv_alt_high_hepatocellular_injury",
    ):
        assert authority_row_for(key) is None


def test_deterministic_repeatability():
    biomarkers = {"urate": 480.0, "creatinine": 140.0, "triglycerides": 2.5}
    first = _joined_summaries(_compiled_findings(biomarkers), {URATE})
    second = _joined_summaries(_compiled_findings(biomarkers), {URATE})
    assert first == second


def test_source_hash_stable():
    raw = (
        REPO / "knowledge_bus/research/investigation_specs/inv_uric_acid_high_metabolic.yaml"
    ).read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest().upper()
        == "A7EDEF6EE3C28A4DA8BE1D79A2F5E36B0F80F7AF5C7B7E5A140418208FC078CD"
    )
