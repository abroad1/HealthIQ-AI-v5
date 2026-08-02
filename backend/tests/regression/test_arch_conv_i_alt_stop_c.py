"""ARCH-CONV-I — ALT compiled-WHY identity resolution runtime proof."""

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
ALT = "signal_alt_high::inv_alt_high_r_value_hepatocellular_biochemical_pattern"
ALT_MIXED = "signal_alt_high::inv_alt_high_r_value_mixed_biochemical_pattern"
ALT_CHOL = "signal_alt_high::inv_alt_high_r_value_cholestatic_alp_predominant_context"
ALT_MUSCLE = "signal_alt_high::inv_alt_high_muscle_source_or_exertional_contribution"
ALT_MASLD = "signal_alt_high::inv_alt_high_metabolic_masld_context"
HEPATIC = "signal_hepatic_alt_context::inv_alt_context"
ALP = "signal_alp_high::inv_alp_high_bone_biliary"
GGT = "signal_ggt_high::inv_ggt_high_hepatic"
HBA1C = "signal_hba1c_high::inv_hba1c_high_glycaemia"

LAB_RANGES = {
    "alt": {"min": 10.0, "max": 45.0},
    "ast": {"min": 10.0, "max": 40.0},
    "alp": {"min": 30.0, "max": 130.0},
    "ggt": {"min": 10.0, "max": 55.0},
    "bilirubin": {"min": 0.0, "max": 20.0},
    "creatine_kinase": {"min": 0.0, "max": 200.0},
    "triglycerides": {"min": 0.0, "max": 1.7},
    "hdl_cholesterol": {"min": 1.0, "max": 2.0},
    "hba1c": {"min": 20.0, "max": 42.0},
}

PROHIBITED = (
    "you have hepatitis",
    "you have masld",
    "diagnosed with masld",
    "fibrosis stage",
    "start medication",
    "pharmacological management",
    "inflammatory coupling",
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


def test_canonical_alt_resolves_compiled_morphology_context():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_alt_high",
        activation_key=ALT,
    )
    assert mode == "compiled"
    assert row is not None
    assert row["why_role"] == "morphology_context"
    assert "conditional_why_role" not in row

    # High ALT with low-normal ALP → hepatocellular R band when ALP present.
    findings = _compiled_findings({"alt": 200.0, "alp": 40.0, "ast": 50.0})
    assert ALT in findings
    assert findings[ALT].why_role == "morphology_context"
    assert (
        findings[ALT].hypotheses[0].hypothesis_id
        == "hyp_alt_hepatocellular_biochemical_pattern_context"
    )
    text = _joined_summaries(findings, {ALT})
    assert "non-causal" in text
    _assert_bounded(text)


def test_legacy_hepatic_alt_context_skips_for_why_ownership():
    mode, row = resolve_frame_why_authority(
        signal_id="signal_hepatic_alt_context",
        activation_key=HEPATIC,
    )
    assert mode == "skip"
    assert row["authority_state"] == "LEGACY_RETIRED"
    assert row["artefact_path"] is None

    root = compile_root_cause_v1(
        signal_results=[
            {
                "signal_id": "signal_hepatic_alt_context",
                "activation_key": HEPATIC,
                "source_spec_id": "inv_alt_context",
                "signal_state": "at_risk",
                "confidence": 0.8,
                "primary_metric": "alt",
            }
        ],
        biomarker_context={"alt": 95.0, "crp": 4.0},
        input_reference_ranges=LAB_RANGES,
    )
    assert root is None


def test_sibling_frames_skip_why_but_remain_activatable():
    for key in (ALT_MIXED, ALT_CHOL, ALT_MUSCLE, ALT_MASLD):
        mode, row = resolve_frame_why_authority(
            signal_id="signal_alt_high",
            activation_key=key,
        )
        assert mode == "skip"
        assert row["authority_state"] == "LEGACY_RETIRED"
        assert row["artefact_path"] is None


def test_no_crp_and_no_hardcoded_thresholds_in_artefact():
    artefact = (
        REPO
        / "knowledge_bus/compiled/hypotheses/inv_alt_high_r_value_hepatocellular_biochemical_pattern.yaml"
    ).read_text(encoding="utf-8").lower()
    assert "crp" not in artefact
    assert "inflammatory-coupling" in artefact or "inflammatory coupling" in artefact
    for needle in (">45", ">60", ">130", "ast>45", "ggt>60"):
        assert needle not in artefact


def test_alp_ggt_and_hba1c_authority_unchanged():
    assert authority_row_for(ALP)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(GGT)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(HBA1C)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(HBA1C)["why_role"] == "morphology_context"


def test_no_runtime_research_file_read_introduced():
    compiler = (
        REPO / "backend/core/analytics/root_cause_compiler_v1.py"
    ).read_text(encoding="utf-8")
    authority = (REPO / "backend/core/knowledge/why_authority_v1.py").read_text(
        encoding="utf-8"
    )
    for needle in (
        "investigation_specs",
        "ALT_High_Hepatic_Pattern_Classification",
        "inv_alt_high_r_value_hepatocellular_biochemical_pattern.yaml",
    ):
        assert needle not in compiler
        assert needle not in authority


def test_register_delta_and_exclusions():
    assert authority_row_for(ALT)["authority_state"] == "COMPILED_ACTIVE"
    assert authority_row_for(HEPATIC)["authority_state"] == "LEGACY_RETIRED"
    for key in (ALT_MIXED, ALT_CHOL, ALT_MUSCLE, ALT_MASLD):
        assert authority_row_for(key)["authority_state"] == "LEGACY_RETIRED"
    assert (
        authority_row_for("signal_alt_high::inv_alt_high_hepatocellular_injury") is None
    )


def test_deterministic_repeatability():
    biomarkers = {"alt": 200.0, "alp": 40.0, "ast": 50.0}
    first = _joined_summaries(_compiled_findings(biomarkers), {ALT})
    second = _joined_summaries(_compiled_findings(biomarkers), {ALT})
    assert first == second
    assert first


def test_source_hash_stable():
    raw = (
        REPO
        / "knowledge_bus/research/investigation_specs/multi_llm_research/ALT_High_Hepatic_Pattern_Classification_ARCH_CONV_E_Pass_3.json"
    ).read_bytes()
    assert (
        hashlib.sha256(raw).hexdigest().upper()
        == "7F20BF9A06B3427217AD7F753C4D9304E5D5A2C46C484699257778844B9D3267"
    )
