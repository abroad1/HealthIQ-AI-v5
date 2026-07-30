"""ARCH-CONV-B Phase 2 — renal WHY and end-to-end role enforcement."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from core.analytics.report_compiler_v1 import (
    TOP_FINDINGS_RANKING_POLICY_VERSION,
    _normalise_root_cause_finding,
    compile_clinician_report_v1,
)
from core.analytics.root_cause_compiler_v1 import (
    _compile_compiled_hypothesis_finding,
    compile_root_cause_v1,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.compiled_hypothesis import (
    get_compiled_hypothesis_artefact_for_activation_key,
)
from core.knowledge.why_authority_v1 import (
    authority_row_for,
    clear_why_authority_cache,
)


REPO = Path(__file__).resolve().parents[3]
CREAT = "signal_creatinine_high::inv_creatinine_high_renal"
UREA = "signal_urea_high::inv_urea_high_renal"
CREAT_PASS3 = (
    "signal_creatinine_high::inv_creatinine_high_reduced_glomerular_filtration"
)
UREA_PASS3 = (
    "signal_urea_high::inv_urea_high_prerenal_volume_depletion_or_catabolic_load"
)
EGFR_KEYS = {
    "signal_egfr_low::inv_egfr_low_chronic_kidney_function_reduction",
    "signal_egfr_low::inv_egfr_low_hemodynamic_filtration_drop",
}
URATE = "signal_urate_high::inv_uric_acid_high_metabolic"

RENAL_RANGES = {
    "creatinine": {"min": 45.0, "max": 105.0},
    "urea": {"min": 2.5, "max": 7.8},
    "egfr": {"min": 60.0, "max": 120.0},
    "hemoglobin": {"min": 120.0, "max": 170.0},
}

PROHIBITED = (
    "you have ckd",
    "you have aki",
    "kidney failure",
    "renal failure",
    "gastrointestinal bleeding is present",
    "start medication",
    "stop medication",
)


def _evaluate_rows(biomarkers: dict[str, float]) -> list[dict]:
    clear_why_authority_cache()
    return [
        row.model_dump()
        for row in SignalEvaluator(SignalRegistry()).evaluate_all(
            signal_biomarkers=biomarkers,
            signal_derived={},
            lab_ranges=RENAL_RANGES,
        )
    ]


def _renal_root(biomarkers: dict[str, float]):
    root = compile_root_cause_v1(
        signal_results=_evaluate_rows(biomarkers),
        biomarker_context=biomarkers,
        input_reference_ranges=RENAL_RANGES,
    )
    assert root is not None
    return root


def _renal_findings(biomarkers: dict[str, float]) -> dict:
    return {
        finding.activation_key: finding
        for finding in _renal_root(biomarkers).findings
        if finding.activation_key
    }


def _joined_summaries(findings: dict) -> str:
    return " ".join(
        hypothesis.summary.lower()
        for finding in findings.values()
        for hypothesis in finding.hypotheses
    )


def _assert_bounded(text: str) -> None:
    for phrase in PROHIBITED:
        assert phrase not in text, f"prohibited phrase present: {phrase!r}"


def _clinician_report_for_renal_panel(biomarkers: dict[str, float]):
    root = _renal_root(biomarkers)
    report_payload = {
        "meta": {
            "ranking_signal_id_fallback_invoked": False,
            "ranking_policy_version": TOP_FINDINGS_RANKING_POLICY_VERSION,
        },
        "top_findings": [
            {
                "signal_id": "signal_creatinine_high",
                "activation_key": CREAT,
                "signal_state": "suboptimal",
                "confidence": 0.85,
                "primary_metric": "creatinine",
                "why_it_matters": "Creatinine is above range.",
                "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
                "supporting_markers": [],
            },
            {
                "signal_id": "signal_urea_high",
                "activation_key": UREA,
                "signal_state": "suboptimal",
                "confidence": 0.75,
                "primary_metric": "urea",
                "why_it_matters": "Urea is above range.",
                "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
                "supporting_markers": [],
            },
        ],
        "top_chains": [],
        "root_cause_v1": root.model_dump(),
    }
    clinician = compile_clinician_report_v1(
        report_v1_payload=report_payload,
        biomarker_rows=[],
    )
    assert clinician is not None
    return clinician


def test_creatinine_narrowed_causal_and_urea_context_only():
    findings = _renal_findings({"creatinine": 140.0, "urea": 10.0})
    assert findings[CREAT].why_role == "causal"
    assert findings[UREA].why_role == "morphology_context"
    assert (
        findings[CREAT].hypotheses[0].hypothesis_id
        == "hyp_creatinine_possible_reduced_renal_clearance"
    )
    assert (
        findings[UREA].hypotheses[0].hypothesis_id
        == "hyp_urea_non_specific_renal_hydration_protein_context"
    )
    causal_keys = {key for key, finding in findings.items() if finding.why_role == "causal"}
    assert CREAT in causal_keys
    assert UREA not in causal_keys
    text = _joined_summaries(findings)
    assert "does not confirm ckd or aki" in text
    assert "does not establish renal impairment" in text
    _assert_bounded(text)


def test_context_only_role_survives_clinician_and_serialised_output():
    clinician = _clinician_report_for_renal_panel({"creatinine": 140.0, "urea": 10.0})
    by_key = {finding.activation_key: finding for finding in clinician.sections.root_causes}
    assert by_key[CREAT].why_role == "causal"
    assert by_key[UREA].why_role == "morphology_context"
    assert UREA not in {
        key for key, finding in by_key.items() if finding.why_role == "causal"
    }

    # This is the structured payload exposed to consumers/frontend. The role is
    # data from backend authority; no medical role inference is needed downstream.
    payload = clinician.model_dump(mode="json")
    serialised = {
        finding["activation_key"]: finding["why_role"]
        for finding in payload["sections"]["root_causes"]
    }
    assert serialised == {CREAT: "causal", UREA: "morphology_context"}


@pytest.mark.parametrize("role", [None, "", "unknown", "context_only", "CAUSAL"])
def test_missing_or_unsupported_clinician_why_role_fails_closed(role):
    row = {
        "signal_id": "signal_urea_high",
        "activation_key": UREA,
        "source_spec_id": "inv_urea_high_renal",
        "authority_scope": "frame_specific",
        "signal_state": "suboptimal",
        "signal_confidence": 0.8,
        "primary_metric": "urea",
        "hypotheses": [],
    }
    if role is not None:
        row["why_role"] = role
    with pytest.raises(ValueError, match="why_role"):
        _normalise_root_cause_finding(row)


@pytest.mark.parametrize("role", [None, "", "unknown", "CONTEXT_ONLY_NON_CAUSAL"])
def test_missing_or_unsupported_compiled_why_role_fails_closed(role):
    target = {
        "signal_id": "signal_urea_high",
        "activation_key": UREA,
        "source_spec_id": "inv_urea_high_renal",
        "signal_state": "suboptimal",
        "confidence": 0.8,
        "primary_metric": "urea",
    }
    if role is not None:
        target["why_role"] = role
    with pytest.raises(ValueError, match="why_role"):
        _compile_compiled_hypothesis_finding(
            target=target,
            artefact=get_compiled_hypothesis_artefact_for_activation_key(UREA),
            tests_by_id={},
            marker_present={"urea"},
        )


def test_deferred_package_only_frames_skip_without_fallback():
    rows = [
        {
            "signal_id": "signal_creatinine_high",
            "activation_key": CREAT_PASS3,
            "source_spec_id": "inv_creatinine_high_reduced_glomerular_filtration",
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "primary_metric": "creatinine",
        },
        {
            "signal_id": "signal_urea_high",
            "activation_key": UREA_PASS3,
            "source_spec_id": "inv_urea_high_prerenal_volume_depletion_or_catabolic_load",
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "primary_metric": "urea",
        },
    ]
    root = compile_root_cause_v1(
        signal_results=rows,
        biomarker_context={"creatinine": 140.0, "urea": 10.0},
        input_reference_ranges=RENAL_RANGES,
    )
    assert root is None
    assert authority_row_for(CREAT_PASS3)["artefact_path"] is None
    assert authority_row_for(UREA_PASS3)["artefact_path"] is None


def test_egfr_and_urate_authority_remain_outside_arch_conv_b():
    for key in EGFR_KEYS | {URATE}:
        assert authority_row_for(key) is None
    compiled_names = {
        path.name for path in (REPO / "knowledge_bus/compiled/hypotheses").glob("*.yaml")
    }
    assert "inv_egfr_low_chronic_kidney_function_reduction.yaml" not in compiled_names
    assert "inv_egfr_low_hemodynamic_filtration_drop.yaml" not in compiled_names
    assert "inv_uric_acid_high_metabolic.yaml" not in compiled_names

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_urate_high",
                "signal_state": "suboptimal",
                "confidence": 0.8,
                "primary_metric": "urate",
            }
        ],
        biomarker_context={"urate": 480.0},
        input_reference_ranges={"urate": {"min": 150.0, "max": 420.0}},
    )
    assert root is not None
    ids = {hyp.hypothesis_id for finding in root.findings for hyp in finding.hypotheses}
    assert "urate_elevated_serum_hyperuricaemia_v1" in ids


def test_existing_thyroid_and_lipid_roles_unchanged():
    rows = [
        {
            "signal_id": "signal_tsh_high",
            "activation_key": "signal_tsh_high::inv_tsh_high_hypothyroidism",
            "source_spec_id": "inv_tsh_high_hypothyroidism",
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "primary_metric": "tsh",
        },
        {
            "signal_id": "signal_ldl_cholesterol_high",
            "activation_key": "signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia",
            "source_spec_id": "inv_ldl_high_dyslipidaemia",
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "primary_metric": "ldl_cholesterol",
        },
    ]
    root = compile_root_cause_v1(
        signal_results=rows,
        biomarker_context={"tsh": 5.0, "ldl_cholesterol": 4.0},
        input_reference_ranges={},
    )
    assert root is not None
    roles = {finding.activation_key: finding.why_role for finding in root.findings}
    assert roles["signal_tsh_high::inv_tsh_high_hypothyroidism"] == "morphology_context"
    assert roles["signal_ldl_cholesterol_high::inv_ldl_high_dyslipidaemia"] == "causal"


def test_renal_compile_and_report_are_repeat_run_deterministic():
    biomarkers = {"creatinine": 140.0, "urea": 10.0}
    first = _renal_root(biomarkers).model_dump(mode="json")
    second = _renal_root(biomarkers).model_dump(mode="json")
    assert first == second
    assert (
        _clinician_report_for_renal_panel(biomarkers).model_dump(mode="json")
        == _clinician_report_for_renal_panel(biomarkers).model_dump(mode="json")
    )


def test_canonical_source_hashes_and_embedded_identity_are_stable():
    expected = {
        "inv_creatinine_high_renal_v1.yaml": (
            "b53c0d924fde540c08226bf61a4d5b6b24eee9c10e1f8646f5d3a7861482163c"
        ),
        "inv_urea_high_renal.yaml": (
            "3c8d3d2e8c8138021981f4adfb9545c858d10354bf6a6c93a70f85d70a6abf60"
        ),
    }
    root = REPO / "knowledge_bus/research/investigation_specs"
    for name, digest in expected.items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
    assert not any(
        key.endswith("inv_creatinine_high_renal_v1")
        for key in _renal_findings({"creatinine": 140.0, "urea": 10.0})
    )
