from __future__ import annotations

from core.analytics.root_cause_compiler_v1 import compile_root_cause_v1
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.why_authority_v1 import clear_why_authority_cache


LAB_RANGES = {
    "tsh": {"min": 0.4, "max": 4.5},
    "free_t4": {"min": 12.0, "max": 22.0},
    "free_t3": {"min": 3.5, "max": 6.5},
}

TSH_HIGH = "signal_tsh_high::inv_tsh_high_hypothyroidism"
TSH_LOW = "signal_tsh_low::inv_tsh_low_hyperthyroidism"
FT3_HIGH = "signal_free_t3_high::inv_free_t3_high_t3_predominant_thyrotoxicosis"
FT4_HIGH = "signal_free_t4_high::inv_free_t4_high_thyrotoxicosis_context"
FT4_LOW = "signal_free_t4_low::inv_free_t4_low_thyroid_hormone_deficiency"


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


def test_tsh_high_with_low_ft4_routes_to_primary_deficiency_only():
    findings = _compiled_findings({"tsh": 8.1, "free_t4": 9.0, "free_t3": 4.2})
    assert FT4_LOW in findings
    assert TSH_HIGH not in findings
    assert findings[FT4_LOW].why_role == "causal"
    assert findings[FT4_LOW].hypotheses[0].hypothesis_id == "hyp_primary_thyroid_hormone_deficiency_pattern"


def test_tsh_high_with_normal_ft4_routes_to_context_only():
    findings = _compiled_findings({"tsh": 7.4, "free_t4": 16.0, "free_t3": 4.6})
    assert TSH_HIGH in findings
    assert FT4_LOW not in findings
    assert findings[TSH_HIGH].why_role == "morphology_context"
    assert "confirm thyroid disease" in findings[TSH_HIGH].hypotheses[0].summary.lower()


def test_tsh_high_with_high_ft4_fails_closed_for_ordinary_hypothyroid_why():
    findings = _compiled_findings({"tsh": 7.0, "free_t4": 25.0, "free_t3": 5.2})
    assert TSH_HIGH not in findings
    assert FT4_LOW not in findings


def test_low_tsh_with_high_ft4_and_high_ft3_serves_single_broader_thyrotoxic_lane():
    findings = _compiled_findings({"tsh": 0.1, "free_t4": 25.0, "free_t3": 7.3})
    assert FT4_HIGH in findings
    assert FT3_HIGH not in findings
    assert TSH_LOW not in findings
    assert findings[FT4_HIGH].why_role == "causal"


def test_low_tsh_with_normal_hormones_routes_to_context_only():
    findings = _compiled_findings({"tsh": 0.2, "free_t4": 16.0, "free_t3": 4.8})
    assert TSH_LOW in findings
    assert FT4_HIGH not in findings
    assert FT3_HIGH not in findings
    assert findings[TSH_LOW].why_role == "morphology_context"


def test_low_tsh_with_low_ft4_signal_present_but_no_primary_deficiency_why():
    biomarkers = {"tsh": 0.2, "free_t4": 9.5, "free_t3": 4.0}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == FT4_LOW for r in rows)
    findings = _compiled_findings(biomarkers)
    assert TSH_LOW not in findings
    assert FT4_HIGH not in findings
    assert FT3_HIGH not in findings
    assert FT4_LOW not in findings


def test_ft4_low_with_normal_tsh_signal_present_but_no_primary_deficiency_why():
    biomarkers = {"tsh": 2.0, "free_t4": 9.0, "free_t3": 4.2}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == FT4_LOW for r in rows)
    findings = _compiled_findings(biomarkers)
    assert FT4_LOW not in findings


def test_ft4_low_with_high_tsh_signal_and_primary_deficiency_why():
    biomarkers = {"tsh": 8.1, "free_t4": 9.0, "free_t3": 4.2}
    rows = _evaluate_rows(biomarkers)
    assert any(r.get("activation_key") == FT4_LOW for r in rows)
    findings = _compiled_findings(biomarkers)
    assert FT4_LOW in findings
    assert findings[FT4_LOW].why_role == "causal"


def test_t3_predominant_lane_requires_low_tsh_and_non_elevated_ft4():
    findings = _compiled_findings({"tsh": 0.2, "free_t4": 18.0, "free_t3": 7.1})
    assert FT3_HIGH in findings
    assert FT4_HIGH not in findings
    assert TSH_LOW not in findings
    summary = findings[FT3_HIGH].hypotheses[0].summary.lower()
    assert "identify the cause" in summary
    assert "graves" not in summary
