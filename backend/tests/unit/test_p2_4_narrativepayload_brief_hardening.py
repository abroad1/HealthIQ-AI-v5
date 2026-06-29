"""P2-4 — NarrativePayloadV1 brief contract hardening and sufficiency tests."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from core.analytics.narrative_payload_builder_v1 import build_narrative_payload_v1
from core.analytics.narrative_report_compiler_v1 import compile_narrative_report_v1
from core.contracts.narrative_payload_v1 import (
    DEFAULT_LLM_PROHIBITED_ACTIONS,
    DEFAULT_PROHIBITED_CLAIM_PATTERNS,
    DEFAULT_REQUIRED_CAVEATS,
    GOVERNED_BRIEF_CORE_SECTION_INTENT_IDS,
    LLM_CLINICIAN_RESERVED_SECTION_IDS,
    MISSING_MARKER_EVIDENCE_SOURCE_KEY,
    WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS,
    NarrativeClaimBoundaryV1,
    NarrativeEvidenceBoundaryV1,
    NarrativeIntentCodeV1,
    NarrativeLlmTranslationConstraintsV1,
    NarrativePayloadV1,
    NarrativeSectionIdV1,
    NarrativeSectionIntentV1,
)
from core.contracts.report_v1 import (
    ReportActionsV1,
    ReportMetaV1,
    ReportTopFindingV1,
    ReportV1,
)
from core.knowledge.health_system_card_evidence import WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS


def _minimal_report() -> ReportV1:
    meta = ReportMetaV1(
        signal_registry_version="reg_v1",
        signal_registry_hash_sha256="0" * 64,
        interaction_map_revision="imap_v1",
        safety_contract_version="safe_v1",
        generated_at="2026-06-29T00:00:00Z",
    )
    tf = ReportTopFindingV1(
        priority_rank=1,
        signal_id="signal_glucose_high",
        system="metabolic",
        signal_state="suboptimal",
        confidence=0.72,
        primary_metric="glucose",
        why_it_matters="Elevated glycaemic markers warrant contextual interpretation.",
    )
    return ReportV1(
        actions=ReportActionsV1(),
        meta=meta,
        top_findings=[tf],
        root_cause_v1=None,
        intervention_annotations_v1=None,
    )


def test_p2_4_core_section_intents_present_on_builder_payload() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a1", report_v1=_minimal_report())
    keys = set(payload.section_intents.keys())
    assert GOVERNED_BRIEF_CORE_SECTION_INTENT_IDS.issubset(keys)
    assert len(keys) >= 12


def test_p2_4_report_story_priority_is_valid_section_ids() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a2", report_v1=_minimal_report())
    valid = {member.value for member in NarrativeSectionIdV1}
    for section_id in payload.report_story_priority:
        assert section_id in valid


def test_p2_4_invalid_report_story_priority_rejected() -> None:
    report = _minimal_report()
    payload = build_narrative_payload_v1(analysis_id="p2-4-a3", report_v1=report)
    data = payload.model_dump()
    data["report_story_priority"] = ["not_a_real_section"]
    with pytest.raises(ValidationError, match="invalid report_story_priority"):
        NarrativePayloadV1.model_validate(data)


def test_p2_4_claim_and_evidence_boundary_fields_present() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a4", report_v1=_minimal_report())
    assert payload.claim_boundaries.prohibited_claim_patterns
    assert payload.claim_boundaries.clinician_only_reserved is True
    boundary = payload.evidence_boundaries[NarrativeSectionIdV1.health_systems_context.value]
    assert boundary.forbidden_as_score_basis


def test_p2_4_prohibited_claim_patterns_include_diagnosis_guard() -> None:
    assert "diagnosis" in DEFAULT_PROHIBITED_CLAIM_PATTERNS
    payload = build_narrative_payload_v1(analysis_id="p2-4-a5", report_v1=_minimal_report())
    for pattern in ("diagnosis", "treatment recommendation"):
        assert pattern in payload.claim_boundaries.prohibited_claim_patterns


def test_p2_4_llm_prohibited_actions_include_no_new_findings() -> None:
    assert "introduce_findings_not_in_governed_brief" in DEFAULT_LLM_PROHIBITED_ACTIONS
    payload = build_narrative_payload_v1(analysis_id="p2-4-a6", report_v1=_minimal_report())
    constraints = payload.future_llm_translation_constraints
    assert constraints is not None
    assert "introduce_findings_not_in_governed_brief" in constraints.prohibited_actions


def test_p2_4_future_llm_constraints_non_none_on_builder_payload() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a7", report_v1=_minimal_report())
    assert payload.future_llm_translation_constraints is not None
    assert payload.future_llm_translation_constraints.llm_role == "translate_governed_brief_only"


def test_p2_4_empty_may_translate_section_ids_is_deny_all() -> None:
    constraints = NarrativeLlmTranslationConstraintsV1(may_translate_section_ids=[])
    assert constraints.may_translate_section_ids == []


def test_p2_4_clinician_reserved_sections_not_on_llm_allowlist() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a8", report_v1=_minimal_report())
    constraints = payload.future_llm_translation_constraints
    assert constraints is not None
    allowlist = set(constraints.may_translate_section_ids)
    for reserved in LLM_CLINICIAN_RESERVED_SECTION_IDS:
        assert reserved not in allowlist


def test_p2_4_clinician_sections_default_deny_llm_rewrite() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a9", report_v1=_minimal_report())
    for reserved in LLM_CLINICIAN_RESERVED_SECTION_IDS:
        intent = payload.section_intents[reserved]
        assert intent.future_llm_may_rewrite is False


def test_p2_4_may_translate_allowlist_rejects_clinician_reserved() -> None:
    report = _minimal_report()
    payload = build_narrative_payload_v1(analysis_id="p2-4-a10", report_v1=report)
    constraints = payload.future_llm_translation_constraints
    assert constraints is not None
    data = payload.model_dump()
    data["future_llm_translation_constraints"] = constraints.model_dump()
    data["future_llm_translation_constraints"]["may_translate_section_ids"] = list(
        constraints.may_translate_section_ids
    ) + [NarrativeSectionIdV1.clinician_synthesis.value]
    with pytest.raises(ValidationError, match="clinician-reserved"):
        NarrativePayloadV1.model_validate(data)


def test_p2_4_wave1_hidden_subsystems_cover_med_rev1_hidden_set() -> None:
    hidden = set(WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS)
    forbidden = set(WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS)
    assert hidden == forbidden


def test_p2_4_required_caveats_non_empty_when_section_intents_present() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a11", report_v1=_minimal_report())
    assert payload.required_caveats
    assert payload.section_intents


def test_p2_4_default_required_caveats_constant_defined() -> None:
    assert DEFAULT_REQUIRED_CAVEATS
    assert "non_diagnostic" in DEFAULT_REQUIRED_CAVEATS[0]


def test_p2_4_missing_marker_caution_representable_via_contract_fields() -> None:
    """P2-2+P2-3 caution fields map to permitted sources and optional refs without new runtime."""
    missing_id = "missing_ferritin_iron_context_v1"
    intent = NarrativeSectionIntentV1(
        section_id=NarrativeSectionIdV1.missing_evidence_limitations,
        intent_code=NarrativeIntentCodeV1.surface_limitations,
        permitted_source_fields=[
            MISSING_MARKER_EVIDENCE_SOURCE_KEY,
            f"{MISSING_MARKER_EVIDENCE_SOURCE_KEY}.{missing_id}.caution_when_absent",
            f"{MISSING_MARKER_EVIDENCE_SOURCE_KEY}.{missing_id}.interpretive_limit",
            f"{MISSING_MARKER_EVIDENCE_SOURCE_KEY}.{missing_id}.interpretive_caution",
        ],
    )
    boundary = NarrativeEvidenceBoundaryV1(
        section_id=NarrativeSectionIdV1.missing_evidence_limitations,
        allowed_evidence_sources=[MISSING_MARKER_EVIDENCE_SOURCE_KEY],
        must_not_claim=["diagnosis", "order tests", "start treatment"],
    )
    assert MISSING_MARKER_EVIDENCE_SOURCE_KEY in intent.permitted_source_fields
    assert "caution_when_absent" in intent.permitted_source_fields[1]
    assert boundary.must_not_claim


def test_p2_4_wave1_health_systems_section_supports_domain_context() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a12", report_v1=_minimal_report())
    hs = payload.section_intents[NarrativeSectionIdV1.health_systems_context.value]
    assert hs.intent_code.value == "contextualise_domains"
    assert "consumer_domain_scores" in hs.permitted_source_fields


def test_p2_4_layer_c_compiler_accepts_builder_payload() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a13", report_v1=_minimal_report())
    nr = compile_narrative_report_v1(
        analysis_id="p2-4-a13",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert nr.meta.get("narrative_payload_v1_present") is True
    digest = nr.meta.get("narrative_payload_v1_digest") or {}
    assert digest.get("llm_constraints_present") is True


def test_p2_4_no_gemini_activation_in_narrative_compiler_path() -> None:
    """Contract path remains deterministic — compile does not enable live Gemini."""
    from core.insights.narrative_runtime_policy import resolve_narrative_llm_allow_llm

    payload = build_narrative_payload_v1(analysis_id="p2-4-a14", report_v1=_minimal_report())
    nr = compile_narrative_report_v1(
        analysis_id="p2-4-a14",
        meta={},
        insight_graph={},
        idl_bundle=None,
        narrative_payload_v1=payload,
    )
    assert nr.meta.get("narrative_payload_v1_present") is True
    assert resolve_narrative_llm_allow_llm(orchestrator_explicit_allow_llm=False).synthesizer_allow_llm is False


def test_p2_4_llm_role_constrained_to_translation_only() -> None:
    payload = build_narrative_payload_v1(analysis_id="p2-4-a15", report_v1=_minimal_report())
    constraints = payload.future_llm_translation_constraints
    assert constraints is not None
    assert constraints.llm_role == "translate_governed_brief_only"
    assert "reason_independently" in constraints.prohibited_actions


def test_p2_4_payload_requires_constraints_when_rewrite_flag_set() -> None:
    report = _minimal_report()
    base = build_narrative_payload_v1(analysis_id="p2-4-a16", report_v1=report)
    data = base.model_dump()
    retail_key = NarrativeSectionIdV1.retail_summary.value
    data["section_intents"][retail_key]["future_llm_may_rewrite"] = True
    data["future_llm_translation_constraints"] = None
    with pytest.raises(ValidationError, match="future_llm_translation_constraints required"):
        NarrativePayloadV1.model_validate(data)
