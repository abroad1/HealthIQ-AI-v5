"""ARCH-CONV-A Wave 2 STOP C — lipid Gate 1 / Gate 2 runtime proof."""

from __future__ import annotations

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.why_authority_v1 import clear_why_authority_cache


LAB_RANGES = {
    "ldl_cholesterol": {"min": 0.0, "max": 3.0},
    "hdl_cholesterol": {"min": 1.0, "max": 2.5},
    "triglycerides": {"min": 0.0, "max": 1.7},
    "total_cholesterol": {"min": 0.0, "max": 5.0},
    "non_hdl_cholesterol": {"min": 0.0, "max": 4.0},
    "apob": {"min": 0.0, "max": 1.0},
    "hba1c": {"min": 20.0, "max": 42.0},
}

LDL = "signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia"
HDL = "signal_hdl_cholesterol_low::inv_hdl_low_cardiovascular"
TG = "signal_triglycerides_high::inv_triglycerides_high_metabolic"
TG_PASS3 = "signal_triglycerides_high::inv_triglycerides_high_insulin_resistant_hypertriglyceridemia"
LDL_V1 = "signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia_v1"
TG_V1 = "signal_triglycerides_high::inv_triglycerides_high_metabolic_v1"
TC = "signal_total_cholesterol_high"
APOA1 = "signal_apoa1_cardio_risk"
LIPID_TRANSPORT = "signal_lipid_transport_dysfunction"

PROHIBITED_PHRASES = (
    "your arteries are blocked",
    "you have heart disease",
    "you have familial hypercholesterolaemia",
    "you have familial hypercholesterolemia",
    "you have metabolic syndrome",
    "you are insulin resistant",
    "you need a statin",
    "start medication",
    "stop medication",
    "start a statin",
    "fibrates",
    "omega-3",
)


def _evaluate_rows(biomarkers: dict[str, float]):
    clear_why_authority_cache()
    return [
        row.model_dump()
        for row in SignalEvaluator(SignalRegistry()).evaluate_all(
            signal_biomarkers=biomarkers,
            signal_derived={},
            lab_ranges=LAB_RANGES,
        )
    ]


def _compiled_findings(biomarkers: dict[str, float]):
    rows = _evaluate_rows(biomarkers)
    root = compile_root_cause_v1(
        signal_results=rows,
        biomarker_context=biomarkers,
        input_reference_ranges=LAB_RANGES,
    )
    findings = root.findings if root else []
    return {finding.activation_key: finding for finding in findings if finding.activation_key}


def _joined_summaries(findings: dict) -> str:
    parts = []
    for finding in findings.values():
        for hyp in finding.hypotheses:
            parts.append(hyp.summary.lower())
    return " ".join(parts)


def _assert_no_prohibited(text: str) -> None:
    for phrase in PROHIBITED_PHRASES:
        assert phrase not in text, f"prohibited phrase present: {phrase!r}"


def test_ldl_high_alone_signal_and_bounded_atherogenic_why():
    biomarkers = {"ldl_cholesterol": 4.2, "hdl_cholesterol": 1.4, "triglycerides": 1.2}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == LDL for r in rows)
    findings = _compiled_findings(biomarkers)
    assert LDL in findings
    assert findings[LDL].why_role == "causal"
    assert findings[LDL].hypotheses[0].hypothesis_id == "hyp_atherogenic_ldl_cholesterol_burden"
    text = _joined_summaries(findings)
    assert "contributes to long-term" in text
    _assert_no_prohibited(text)
    assert "does not confirm" in text
    assert HDL not in findings
    assert TG not in findings


def test_hdl_low_alone_signal_context_only_no_causal_why():
    biomarkers = {"ldl_cholesterol": 2.4, "hdl_cholesterol": 0.7, "triglycerides": 1.2}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == HDL for r in rows)
    findings = _compiled_findings(biomarkers)
    assert HDL in findings
    assert findings[HDL].why_role == "morphology_context"
    text = _joined_summaries(findings)
    assert "risk-marker context" in text
    assert "does not prove" in text
    _assert_no_prohibited(text)
    causal = [f for f in findings.values() if f.why_role == "causal"]
    assert causal == []
    assert LDL not in findings
    assert TG not in findings


def test_triglycerides_high_alone_bounded_metabolic_risk_why():
    biomarkers = {"ldl_cholesterol": 2.4, "hdl_cholesterol": 1.4, "triglycerides": 3.5}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == TG for r in rows)
    findings = _compiled_findings(biomarkers)
    assert TG in findings
    assert findings[TG].why_role == "causal"
    assert findings[TG].hypotheses[0].hypothesis_id == "hyp_triglyceride_rich_lipoprotein_metabolic_risk"
    text = _joined_summaries(findings)
    assert "triglyceride-rich" in text or "metabolic-risk" in text
    assert "single cause" in text
    _assert_no_prohibited(text)
    assert TG_PASS3 not in findings


def test_ldl_high_plus_hdl_low_coherent_hierarchy():
    biomarkers = {"ldl_cholesterol": 4.5, "hdl_cholesterol": 0.6, "triglycerides": 1.1}
    findings = _compiled_findings(biomarkers)
    assert LDL in findings
    assert HDL in findings
    assert findings[LDL].why_role == "causal"
    assert findings[HDL].why_role == "morphology_context"
    causal = [k for k, f in findings.items() if f.why_role == "causal"]
    assert causal == [LDL]
    _assert_no_prohibited(_joined_summaries(findings))


def test_triglycerides_high_plus_hdl_low_integrated_adverse_pattern():
    biomarkers = {"ldl_cholesterol": 2.5, "hdl_cholesterol": 0.6, "triglycerides": 4.0}
    findings = _compiled_findings(biomarkers)
    assert TG in findings
    assert HDL in findings
    assert findings[TG].why_role == "causal"
    assert findings[HDL].why_role == "morphology_context"
    causal = [k for k, f in findings.items() if f.why_role == "causal"]
    assert causal == [TG]
    _assert_no_prohibited(_joined_summaries(findings))


def test_ldl_tg_hdl_combined_no_three_causal_narratives():
    biomarkers = {"ldl_cholesterol": 4.8, "hdl_cholesterol": 0.55, "triglycerides": 3.8}
    findings = _compiled_findings(biomarkers)
    assert LDL in findings
    assert TG in findings
    assert HDL in findings
    assert findings[LDL].why_role == "causal"
    assert findings[TG].why_role == "causal"
    assert findings[HDL].why_role == "morphology_context"
    causal = [k for k, f in findings.items() if f.why_role == "causal"]
    assert set(causal) == {LDL, TG}
    assert len(causal) == 2
    text = _joined_summaries(findings)
    _assert_no_prohibited(text)


def test_no_v1_duplicate_activation_identities():
    biomarkers = {"ldl_cholesterol": 4.2, "hdl_cholesterol": 0.7, "triglycerides": 3.2}
    rows = _evaluate_rows(biomarkers)
    keys = {r.get("activation_key") for r in rows}
    assert LDL_V1 not in keys
    assert TG_V1 not in keys
    findings = _compiled_findings(biomarkers)
    assert LDL_V1 not in findings
    assert TG_V1 not in findings


def test_blocked_wave2_targets_not_introduced():
    biomarkers = {
        "ldl_cholesterol": 4.2,
        "hdl_cholesterol": 0.7,
        "triglycerides": 3.2,
        "total_cholesterol": 7.5,
    }
    findings = _compiled_findings(biomarkers)
    for blocked in (TC, APOA1, LIPID_TRANSPORT):
        assert blocked not in findings
        assert not any(blocked == (k or "").split("::")[0] for k in findings)
    # No Wave 2 authority for total-cholesterol / ApoA1 / lipid-transport composites.
    assert not any("total_cholesterol_high" in (k or "") for k in findings)
    assert not any("apoa1" in (k or "") for k in findings)
    assert not any("lipid_transport" in (k or "") for k in findings)


def test_pass3_parallel_ldl_hdl_keys_skip_why():
    biomarkers = {"ldl_cholesterol": 4.5, "hdl_cholesterol": 0.6, "triglycerides": 1.1}
    findings = _compiled_findings(biomarkers)
    assert LDL in findings
    assert HDL in findings
    assert "signal_ldl_high::inv_ldl_high_atherogenic_ldl_burden" not in findings
    assert "signal_ldl_high::inv_ldl_high_familial_hypercholesterolemia_context" not in findings
    assert "signal_hdl_low::inv_hdl_low_atherogenic_dyslipidemia" not in findings
    assert "signal_hdl_low::inv_hdl_low_hypertriglyceridemic_insulin_resistance_pattern" not in findings
    text = _joined_summaries(findings)
    assert "familial hypercholesterolemia" not in text
    assert "insulin resistant" not in text
    _assert_no_prohibited(text)


def test_wave1_thyroid_boundaries_unchanged_on_lipid_panel():
    # Lipid panel must not invent thyroid compiled WHY.
    biomarkers = {"ldl_cholesterol": 4.2, "hdl_cholesterol": 0.7, "triglycerides": 3.2}
    findings = _compiled_findings(biomarkers)
    thyroid_keys = [
        k for k in findings if k.startswith("signal_tsh_") or k.startswith("signal_free_t")
    ]
    assert thyroid_keys == []
