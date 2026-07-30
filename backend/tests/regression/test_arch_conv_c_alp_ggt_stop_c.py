"""ARCH-CONV-C Phase 2 — ALP/GGT WHY authority and cholestatic-source policy."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from core.analytics.report_compiler_v1 import (
    TOP_FINDINGS_RANKING_POLICY_VERSION,
    compile_clinician_report_v1,
)
from core.analytics.root_cause_compiler_v1 import (
    _governed_compiled_why_role,
    compile_root_cause_v1,
)
from core.analytics.signal_authority_collision_resolver import (
    apply_signal_authority_collision_policy,
    load_signal_authority_collision_model,
)
from core.analytics.signal_evaluator import SignalEvaluator, SignalRegistry
from core.knowledge.why_authority_v1 import (
    authority_row_for,
    clear_why_authority_cache,
)

REPO = Path(__file__).resolve().parents[3]
ALP = "signal_alp_high::inv_alp_high_bone_biliary"
GGT = "signal_ggt_high::inv_ggt_high_hepatic"
DEFERRED = {
    "signal_alp_high::inv_alp_high_cholestatic_pattern",
    "signal_alp_high::inv_alp_high_high_bone_turnover_pattern",
    "signal_ggt_high::inv_ggt_high_hepatobiliary_cholestatic_context",
    "signal_ggt_high::inv_ggt_high_alcohol_or_enzyme_induction_context",
}

LIVER_RANGES = {
    "alp": {"min": 30.0, "max": 120.0},
    "ggt": {"min": 0.0, "max": 55.0},
    "bilirubin": {"min": 0.0, "max": 20.0},
    "alt": {"min": 0.0, "max": 40.0},
    "mcv": {"min": 80.0, "max": 96.0},
    "calcium": {"min": 2.1, "max": 2.6},
}

PROHIBITED = (
    "you have cholestasis",
    "alcohol misuse",
    "medicine-induced liver injury",
    "metabolic steatotic liver disease",
    "primary biliary cholangitis",
    "primary sclerosing cholangitis",
    "malignancy",
    "high bone turnover",
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
            lab_ranges=LIVER_RANGES,
        )
    ]


def _liver_rows(biomarkers: dict[str, float]) -> list[dict]:
    return [
        row
        for row in _evaluate_rows(biomarkers)
        if row["signal_id"] in {"signal_alp_high", "signal_ggt_high"}
    ]


def _root(biomarkers: dict[str, float]):
    root = compile_root_cause_v1(
        signal_results=_liver_rows(biomarkers),
        biomarker_context=biomarkers,
        input_reference_ranges=LIVER_RANGES,
    )
    assert root is not None
    return root


def _joined_summaries(root) -> str:
    return " ".join(
        hypothesis.summary.lower()
        for finding in root.findings
        for hypothesis in finding.hypotheses
    )


def _clinician_report(biomarkers: dict[str, float]):
    root = _root(biomarkers)
    top_findings = [
        {
            "signal_id": finding.signal_id,
            "activation_key": finding.activation_key,
            "signal_state": finding.signal_state,
            "confidence": finding.signal_confidence,
            "primary_metric": finding.primary_metric,
            "why_it_matters": "Governed ALP/GGT source context.",
            "confidence_reasons": ["PRIMARY_METRIC_PRESENT"],
            "supporting_markers": [],
        }
        for finding in root.findings
    ]
    clinician = compile_clinician_report_v1(
        report_v1_payload={
            "meta": {
                "ranking_signal_id_fallback_invoked": False,
                "ranking_policy_version": TOP_FINDINGS_RANKING_POLICY_VERSION,
            },
            "top_findings": top_findings,
            "top_chains": [],
            "root_cause_v1": root.model_dump(),
        },
        biomarker_rows=[],
    )
    assert clinician is not None
    return clinician


def test_ratified_authority_rows_and_deferred_frames_are_explicit():
    alp = authority_row_for(ALP)
    ggt = authority_row_for(GGT)
    assert alp is not None and alp["authority_state"] == "COMPILED_ACTIVE"
    assert alp["why_role"] == "causal"
    assert alp["conditional_why_role"]["otherwise"] == "morphology_context"
    assert ggt is not None and ggt["authority_state"] == "COMPILED_ACTIVE"
    assert ggt["why_role"] == "morphology_context"
    for key in DEFERRED:
        row = authority_row_for(key)
        assert row is not None
        assert row["authority_state"] == "LEGACY_RETIRED"
        assert row["artefact_path"] is None


def test_named_cholestatic_source_axis_is_explicit_and_ratified():
    model = load_signal_authority_collision_model()
    axis = next(
        group
        for group in model["authority_groups"]
        if group["authority_group_id"] == "liver_injury_axis"
    )
    assert axis["biological_axis"] == "cholestatic_source_axis"
    assert axis["status"] == "adjudicated_runtime_enforced"
    assert axis["runtime_policy_id"] == "cholestatic_source_axis_v1"
    assert axis["primary_activation_key"] == ALP
    assert axis["supporting_activation_keys"] == [GGT]
    assert axis["gate1_reference"] == "ARCH-CONV-C-GATE1-HMR-2026-07-30"
    assert axis["gate2_reference"] == "ARCH-CONV-C-GATE2-ANTHONY-2026-07-30"


@pytest.mark.parametrize(
    ("biomarkers", "expected_key"),
    [
        ({"alp": 160.0, "ggt": 80.0}, ALP),
        ({"alp": 160.0, "ggt": 30.0}, ALP),
        ({"alp": 160.0}, ALP),
        ({"alp": 100.0, "ggt": 80.0}, GGT),
        ({"ggt": 80.0}, GGT),
    ],
)
def test_axis_emits_only_ratified_activation_key(
    biomarkers: dict[str, float],
    expected_key: str,
):
    assert {row["activation_key"] for row in _liver_rows(biomarkers)} == {expected_key}


def test_concordant_alp_ggt_emits_one_alp_causal_candidate():
    root = _root({"alp": 160.0, "ggt": 80.0})
    assert [(finding.activation_key, finding.why_role) for finding in root.findings] == [
        (ALP, "causal")
    ]
    text = _joined_summaries(root)
    assert "with high ggt" in text
    assert "possible cholestatic or hepatobiliary biochemical pattern" in text


@pytest.mark.parametrize("biomarkers", [{"alp": 160.0, "ggt": 30.0}, {"alp": 160.0}])
def test_alp_without_high_ggt_fails_closed_to_non_causal_context(
    biomarkers: dict[str, float],
):
    finding = _root(biomarkers).findings[0]
    assert finding.activation_key == ALP
    assert finding.why_role == "morphology_context"
    assert "source remains non-specific" in finding.hypotheses[0].summary.lower()


@pytest.mark.parametrize("biomarkers", [{"alp": 100.0, "ggt": 80.0}, {"ggt": 80.0}])
def test_ggt_without_high_alp_remains_context_only(biomarkers: dict[str, float]):
    finding = _root(biomarkers).findings[0]
    assert finding.activation_key == GGT
    assert finding.why_role == "morphology_context"
    assert "non-specific hepatic-source context" in finding.hypotheses[0].summary.lower()


def test_deferred_pass3_frames_emit_no_why_or_fallback():
    rows = [
        {
            "signal_id": key.split("::", 1)[0],
            "activation_key": key,
            "source_spec_id": key.split("::", 1)[1],
            "signal_state": "suboptimal",
            "confidence": 0.8,
            "primary_metric": "alp" if key.startswith("signal_alp") else "ggt",
        }
        for key in sorted(DEFERRED)
    ]
    assert (
        compile_root_cause_v1(
            signal_results=rows,
            biomarker_context={"alp": 160.0, "ggt": 80.0},
            input_reference_ranges=LIVER_RANGES,
        )
        is None
    )


def test_conditional_role_metadata_fails_closed_when_invalid():
    base = {
        "why_role": "causal",
        "conditional_why_role": {
            "policy_id": "cholestatic_source_axis_v1",
            "causal_when": [{"metric_id": "ggt", "boundary": "above_max"}],
            "otherwise": "morphology_context",
        },
    }
    assert (
        _governed_compiled_why_role(
            auth_row=base,
            biomarker_context={"ggt": 80.0},
            reference_ranges=LIVER_RANGES,
        )
        == "causal"
    )
    assert (
        _governed_compiled_why_role(
            auth_row=base,
            biomarker_context={},
            reference_ranges=LIVER_RANGES,
        )
        == "morphology_context"
    )
    for mutation in (
        {"why_role": ""},
        {"why_role": "causal", "conditional_why_role": {}},
        {
            "why_role": "causal",
            "conditional_why_role": {
                "policy_id": "cholestatic_source_axis_v1",
                "causal_when": [],
                "otherwise": "causal_by_default",
            },
        },
    ):
        with pytest.raises(ValueError, match="why_role|conditional"):
            _governed_compiled_why_role(
                auth_row=mutation,
                biomarker_context={"ggt": 80.0},
                reference_ranges=LIVER_RANGES,
            )


def test_roles_survive_clinician_serialisation_without_frontend_inference():
    concordant = _clinician_report({"alp": 160.0, "ggt": 80.0}).model_dump(mode="json")
    discordant = _clinician_report({"ggt": 80.0}).model_dump(mode="json")
    assert concordant["sections"]["root_causes"][0]["why_role"] == "causal"
    assert discordant["sections"]["root_causes"][0]["why_role"] == "morphology_context"


def test_collision_selection_is_input_order_independent():
    raw = SignalEvaluator(SignalRegistry()).evaluate_all(
        signal_biomarkers={"alp": 160.0, "ggt": 80.0},
        signal_derived={},
        lab_ranges=LIVER_RANGES,
    )
    first = apply_signal_authority_collision_policy(
        raw,
        signal_biomarkers={"alp": 160.0, "ggt": 80.0},
        signal_derived={},
        lab_ranges=LIVER_RANGES,
    )
    second = apply_signal_authority_collision_policy(
        list(reversed(raw)),
        signal_biomarkers={"alp": 160.0, "ggt": 80.0},
        signal_derived={},
        lab_ranges=LIVER_RANGES,
    )
    assert [row.model_dump() for row in first] == [row.model_dump() for row in second]


def test_alt_ast_bilirubin_hyperbilirubinemia_and_alp_low_have_no_new_why_rows():
    register = yaml.safe_load(
        (REPO / "knowledge_bus/governance/compiled_why_authority_register_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    excluded = {
        "signal_alt_high",
        "signal_hepatic_alt_context",
        "signal_ast_high",
        "signal_bilirubin_high",
        "signal_hyperbilirubinemia",
        "signal_alp_low",
    }
    assert not any(row["signal_id"] in excluded for row in register["frames"])


def test_liver_card_and_score_contributor_boundaries_are_unchanged():
    card = yaml.safe_load(
        (REPO / "knowledge_bus/compiled/health_system_cards/wave1_liver_flat_v1.yaml").read_text(
            encoding="utf-8"
        )
    )
    roles = {
        row["marker_id"]: row["marker_role"]
        for row in card["markers"]
        if row["marker_id"] in {"alt", "ast", "alp", "ggt"}
    }
    assert roles == {
        "alt": "score_contributor",
        "ast": "score_contributor",
        "alp": "confidence_contributor",
        "ggt": "confidence_contributor",
    }


def test_output_is_bounded_and_repeat_run_deterministic():
    biomarkers = {"alp": 160.0, "ggt": 80.0}
    first = _root(biomarkers).model_dump(mode="json")
    second = _root(biomarkers).model_dump(mode="json")
    assert first == second
    text = _joined_summaries(_root(biomarkers))
    for phrase in PROHIBITED:
        assert phrase not in text


def test_source_and_output_hash_lineage_is_complete():
    expected_sources = {
        "inv_alp_high_bone_biliary.yaml": (
            "1a8e2da95d4aeae0505897da445709632f5ea4c39c34d4aaf906ef3462eb61ef"
        ),
        "inv_ggt_high_hepatic.yaml": (
            "3e2cc6cf074dcb73b825e9a97fe93b43c4f50dc874a0c85cbaa34b754d46c8a1"
        ),
    }
    source_root = REPO / "knowledge_bus/research/investigation_specs"
    for filename, digest in expected_sources.items():
        assert hashlib.sha256((source_root / filename).read_bytes()).hexdigest() == digest

    for manifest_name in ("arch_conv_c_alp_high.yaml", "arch_conv_c_ggt_high.yaml"):
        manifest = yaml.safe_load(
            (REPO / "knowledge_bus/compiled/manifests" / manifest_name).read_text(
                encoding="utf-8"
            )
        )
        output = manifest["outputs"][0]
        output_path = REPO / output["output_path"]
        assert hashlib.sha256(output_path.read_bytes()).hexdigest() == output["output_hash"]
