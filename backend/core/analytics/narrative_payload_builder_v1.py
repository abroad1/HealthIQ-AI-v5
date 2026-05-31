"""
Deterministic builder: ReportV1 (+ optional annotations) → NarrativePayloadV1 (WP2 / LAYER-B-1).

Builds a governed narrative brief with section intents, evidence boundaries, score hierarchy,
and future LLM translation constraints. No LLM.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.narrative_payload_v1 import (
    DEFAULT_LLM_PROHIBITED_ACTIONS,
    DEFAULT_PROHIBITED_CLAIM_PATTERNS,
    WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS,
    NarrativeClaimBoundaryV1,
    NarrativeClaimStrengthV1,
    NarrativeEvidenceBoundaryV1,
    NarrativeIntentCodeV1,
    NarrativeLlmTranslationConstraintsV1,
    NarrativePayloadV1,
    NarrativeScoreHierarchyV1,
    NarrativeSectionIdV1,
    NarrativeSectionIntentV1,
    NarrativeSectionVisibilityV1,
)
from core.contracts.report_v1 import ReportTopFindingV1, ReportV1


def _lead_finding(report_v1: ReportV1) -> Optional[ReportTopFindingV1]:
    tfs = list(report_v1.top_findings or [])
    return tfs[0] if tfs else None


def _lead_has_low_confidence(lead: Optional[ReportTopFindingV1]) -> bool:
    if lead is None:
        return True
    try:
        return float(lead.confidence) < 0.55
    except (TypeError, ValueError):
        return False


def _root_cause_present(report_v1: ReportV1) -> bool:
    rc = report_v1.root_cause_v1
    return rc is not None and bool(getattr(rc, "findings", None))


def _default_score_hierarchy() -> NarrativeScoreHierarchyV1:
    return NarrativeScoreHierarchyV1(
        guidance_lines=[
            "System domain scores summarise Wave 1 health-system context; they do not replace the ranked primary finding.",
            "Individual marker scores support detail sections and must not dominate the hero or primary finding.",
            "Evidence completeness on domain cards qualifies confidence; limited coverage must be stated when relevant.",
            "Hidden or support subsystems must not be described as the visible score basis.",
            "Overall score, when shown, provides context and must not compete with the primary finding headline.",
        ],
    )


def _default_llm_constraints(section_ids: List[str]) -> NarrativeLlmTranslationConstraintsV1:
    consumer_sections = [
        NarrativeSectionIdV1.retail_summary.value,
        NarrativeSectionIdV1.lead_narrative.value,
        NarrativeSectionIdV1.body_overview.value,
        NarrativeSectionIdV1.next_steps_narrative.value,
        NarrativeSectionIdV1.hero_main_finding.value,
    ]
    return NarrativeLlmTranslationConstraintsV1(
        prohibited_actions=list(DEFAULT_LLM_PROHIBITED_ACTIONS),
        must_preserve_fields=[
            "top_findings[0].signal_id",
            "top_findings[0].primary_metric",
            "score_hierarchy",
            "evidence_boundaries",
            "required_caveats",
        ],
        may_translate_section_ids=[sid for sid in section_ids if sid in consumer_sections],
    )


def _evidence_boundary(
    section_id: NarrativeSectionIdV1,
    *,
    allowed: List[str],
    forbidden_basis: Optional[List[str]] = None,
    must_not: Optional[List[str]] = None,
) -> NarrativeEvidenceBoundaryV1:
    return NarrativeEvidenceBoundaryV1(
        section_id=section_id,
        allowed_evidence_sources=list(allowed),
        forbidden_as_score_basis=list(forbidden_basis or []),
        must_not_claim=list(must_not or []),
    )


def _build_section_intents(
    report_v1: ReportV1,
    *,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1],
) -> Dict[str, NarrativeSectionIntentV1]:
    lead = _lead_finding(report_v1)
    low_conf = _lead_has_low_confidence(lead)
    has_rc = _root_cause_present(report_v1)
    has_intervention = intervention_annotations_v1 is not None

    retail_intent = (
        NarrativeIntentCodeV1.express_uncertainty
        if low_conf or lead is None
        else NarrativeIntentCodeV1.prioritise
    )
    lead_intent = (
        NarrativeIntentCodeV1.express_uncertainty
        if low_conf or not has_rc
        else NarrativeIntentCodeV1.explain_mechanism
    )

    return {
        NarrativeSectionIdV1.hero_main_finding.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.hero_main_finding,
            intent_code=retail_intent,
            purpose="Surface the single lead interpretation without competing score families.",
            permitted_source_fields=[
                "interpretation_display_layer_v1",
                "narrative_report_v1.retail_summary",
                "clinician_report_v1.sections.page1",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.primary_finding_why.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.primary_finding_why,
            intent_code=lead_intent,
            purpose="Explain why the primary finding leads the report using structured evidence only.",
            permitted_source_fields=[
                "clinician_report_v1.sections.page1",
                "report_v1.top_findings",
                "report_v1.root_cause_v1",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.retail_summary.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.retail_summary,
            intent_code=retail_intent,
            purpose="Consumer-safe lead summary from ranked findings.",
            permitted_source_fields=["report_v1.top_findings", "idl_bundle"],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.lead_narrative.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.lead_narrative,
            intent_code=lead_intent,
            purpose="Mechanism and structured hypothesis context for the lead pattern.",
            permitted_source_fields=[
                "report_v1.top_findings",
                "report_v1.root_cause_v1",
                "insight_graph.signal_results",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.body_overview.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.body_overview,
            intent_code=NarrativeIntentCodeV1.reassure,
            purpose="Wider deterministic snapshot without overriding the primary finding.",
            permitted_source_fields=[
                "report_v1.top_findings",
                "interpretation_entities_v1",
                "functional_interpretation_v1",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.whats_working_well.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.whats_working_well,
            intent_code=NarrativeIntentCodeV1.reassure,
            purpose="Balanced reassurance from governed balanced-systems read.",
            permitted_source_fields=["balanced_systems_v1"],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.health_systems_context.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.health_systems_context,
            intent_code=NarrativeIntentCodeV1.contextualise_domains,
            purpose="Wave 1 domain cards provide health-system context distinct from the primary finding.",
            permitted_source_fields=["consumer_domain_scores"],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.patterns_across_body.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.patterns_across_body,
            intent_code=NarrativeIntentCodeV1.explain_mechanism,
            purpose="IDL-visible patterns across the panel without re-ranking the lead finding.",
            permitted_source_fields=["interpretation_display_layer_v1"],
            default_visibility=NarrativeSectionVisibilityV1.collapsed_default,
        ),
        NarrativeSectionIdV1.marker_evidence.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.marker_evidence,
            intent_code=NarrativeIntentCodeV1.contextualise_domains,
            purpose="Marker-level evidence supports detail; must not become the main narrative headline.",
            permitted_source_fields=["biomarkers", "wave1_aligned_drivers"],
            default_visibility=NarrativeSectionVisibilityV1.detail_only,
        ),
        NarrativeSectionIdV1.missing_evidence_limitations.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.missing_evidence_limitations,
            intent_code=NarrativeIntentCodeV1.surface_limitations,
            purpose="Surface missing markers and confidence limitations proportionately.",
            permitted_source_fields=[
                "clinician_report_v1.data_quality",
                "consumer_domain_scores.evidence_completeness",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.next_steps_narrative.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.next_steps_narrative,
            intent_code=NarrativeIntentCodeV1.frame_next_steps,
            purpose="Frame clinician discussion and follow-up without treatment prescriptions.",
            permitted_source_fields=[
                "report_v1.actions",
                "report_v1.top_findings",
                "pathway_explainers_v1",
            ],
            default_visibility=NarrativeSectionVisibilityV1.visible_default,
        ),
        NarrativeSectionIdV1.technical_clinician_detail.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.technical_clinician_detail,
            intent_code=NarrativeIntentCodeV1.support_clinician_fast_read,
            purpose="Structured clinician detail; reserved for professional context.",
            permitted_source_fields=["clinician_report_v1", "narrative_report_v1.clinician_synthesis"],
            default_visibility=NarrativeSectionVisibilityV1.collapsed_default,
            future_llm_may_rewrite=False,
        ),
        NarrativeSectionIdV1.clinician_synthesis.value: NarrativeSectionIntentV1(
            section_id=NarrativeSectionIdV1.clinician_synthesis,
            intent_code=NarrativeIntentCodeV1.support_clinician_fast_read,
            purpose="Fast-read clinician synthesis from governed report slices.",
            permitted_source_fields=[
                "report_v1",
                "idl_bundle",
                "interpretation_entities_v1",
            ],
            default_visibility=NarrativeSectionVisibilityV1.collapsed_default,
            future_llm_may_rewrite=False,
        ),
    }


def _build_evidence_boundaries() -> Dict[str, NarrativeEvidenceBoundaryV1]:
    hidden = list(WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS)
    hidden_claim = ["homocysteine pathway as score basis", "insulin resistance as scored subsystem"]
    return {
        NarrativeSectionIdV1.health_systems_context.value: _evidence_boundary(
            NarrativeSectionIdV1.health_systems_context,
            allowed=["consumer_domain_scores", "wave1_visible_subsystems"],
            forbidden_basis=hidden,
            must_not=hidden_claim,
        ),
        NarrativeSectionIdV1.hero_main_finding.value: _evidence_boundary(
            NarrativeSectionIdV1.hero_main_finding,
            allowed=[
                "interpretation_display_layer_v1",
                "narrative_report_v1.retail_summary",
                "report_v1.top_findings",
            ],
            forbidden_basis=hidden,
        ),
        NarrativeSectionIdV1.marker_evidence.value: _evidence_boundary(
            NarrativeSectionIdV1.marker_evidence,
            allowed=["biomarkers", "wave1_aligned_drivers", "consumer_domain_scores.marker_evidence"],
            must_not=["marker score dominates headline"],
        ),
        NarrativeSectionIdV1.missing_evidence_limitations.value: _evidence_boundary(
            NarrativeSectionIdV1.missing_evidence_limitations,
            allowed=[
                "clinician_report_v1.data_quality",
                "consumer_domain_scores.evidence_completeness",
                "consumer_domain_scores.evidence_limitations_line",
            ],
        ),
    }


def _default_report_story_priority() -> List[str]:
    return [
        NarrativeSectionIdV1.hero_main_finding.value,
        NarrativeSectionIdV1.primary_finding_why.value,
        NarrativeSectionIdV1.whats_working_well.value,
        NarrativeSectionIdV1.health_systems_context.value,
        NarrativeSectionIdV1.patterns_across_body.value,
        NarrativeSectionIdV1.marker_evidence.value,
        NarrativeSectionIdV1.missing_evidence_limitations.value,
        NarrativeSectionIdV1.next_steps_narrative.value,
        NarrativeSectionIdV1.technical_clinician_detail.value,
    ]


def _required_caveats(report_v1: ReportV1) -> List[str]:
    caveats = [
        "Interpretation is descriptive and non-diagnostic; discuss results with a clinician.",
        "Domain scores summarise panel context and do not replace the ranked primary finding.",
    ]
    if not _root_cause_present(report_v1):
        caveats.append(
            "Structured root-cause hypotheses were limited on this panel; lead copy stays proportionate."
        )
    return caveats


def build_narrative_payload_v1(
    *,
    analysis_id: str,
    report_v1: ReportV1,
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None,
) -> NarrativePayloadV1:
    ia = intervention_annotations_v1
    if ia is None:
        ia = report_v1.intervention_annotations_v1

    section_intents = _build_section_intents(report_v1, intervention_annotations_v1=ia)
    boundaries = NarrativeClaimBoundaryV1(
        allowed_claim_strength=NarrativeClaimStrengthV1.pattern_and_association_only,
        prohibited_claim_patterns=list(DEFAULT_PROHIBITED_CLAIM_PATTERNS),
        clinician_only_reserved=True,
    )

    return NarrativePayloadV1(
        analysis_id=analysis_id,
        report_v1=report_v1,
        top_findings=list(report_v1.top_findings),
        root_cause_v1=report_v1.root_cause_v1,
        intervention_annotations_v1=ia,
        report_story_priority=_default_report_story_priority(),
        section_intents=section_intents,
        evidence_boundaries=_build_evidence_boundaries(),
        score_hierarchy=_default_score_hierarchy(),
        required_caveats=_required_caveats(report_v1),
        claim_boundaries=boundaries,
        future_llm_translation_constraints=_default_llm_constraints(
            list(section_intents.keys())
        ),
    )
