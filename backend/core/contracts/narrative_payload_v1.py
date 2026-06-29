"""
WP2 / LAYER-B-1 — Layer B → Layer C narrative input payload (Path B).

Formal handoff object ahead of Sprint 3. Does not duplicate ReportV1 medical definitions.
LAYER-B-1 extends the brief with section intents, evidence boundaries, score hierarchy,
and future LLM translation constraints.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Literal, Optional, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.report_v1 import ReportTopFindingV1, ReportV1
from core.contracts.root_cause_v1 import RootCauseV1

NARRATIVE_PAYLOAD_SCHEMA_VERSION = "v1.1"

# Governed source key for P2-2+P2-3 missing-marker caution pack (permitted_source_fields / evidence).
MISSING_MARKER_EVIDENCE_SOURCE_KEY = "missing_marker_explainers_v1"


class NarrativeIntentCodeV1(str, Enum):
    reassure = "reassure"
    prioritise = "prioritise"
    explain_mechanism = "explain_mechanism"
    express_uncertainty = "express_uncertainty"
    frame_next_steps = "frame_next_steps"
    support_clinician_fast_read = "support_clinician_fast_read"
    surface_limitations = "surface_limitations"
    contextualise_domains = "contextualise_domains"


class NarrativeSectionIdV1(str, Enum):
    """Governed results-page sections — compiler-backed and render-only surfaces."""

    retail_summary = "retail_summary"
    lead_narrative = "lead_narrative"
    body_overview = "body_overview"
    next_steps_narrative = "next_steps_narrative"
    clinician_synthesis = "clinician_synthesis"
    hero_main_finding = "hero_main_finding"
    primary_finding_why = "primary_finding_why"
    whats_working_well = "whats_working_well"
    health_systems_context = "health_systems_context"
    patterns_across_body = "patterns_across_body"
    marker_evidence = "marker_evidence"
    missing_evidence_limitations = "missing_evidence_limitations"
    technical_clinician_detail = "technical_clinician_detail"


# Sections that must never appear on the LLM translation allowlist.
LLM_CLINICIAN_RESERVED_SECTION_IDS: frozenset[str] = frozenset(
    {
        NarrativeSectionIdV1.clinician_synthesis.value,
        NarrativeSectionIdV1.technical_clinician_detail.value,
    }
)


class NarrativeSectionVisibilityV1(str, Enum):
    visible_default = "visible_default"
    collapsed_default = "collapsed_default"
    detail_only = "detail_only"


class NarrativeClaimStrengthV1(str, Enum):
    """Bounded consumer claim posture — descriptive only."""

    pattern_and_association_only = "pattern_and_association_only"


class NarrativeSectionIntentV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: NarrativeSectionIdV1
    intent_code: NarrativeIntentCodeV1
    purpose: str = Field(default="", max_length=400)
    permitted_source_fields: List[str] = Field(default_factory=list)
    default_visibility: NarrativeSectionVisibilityV1 = NarrativeSectionVisibilityV1.visible_default
    fallback_rule: Literal["omit_section_if_sources_missing"] = "omit_section_if_sources_missing"
    future_llm_may_rewrite: bool = Field(
        default=False,
        description=(
            "Whether a future LLM translator may rephrase this section within constraints. "
            "Defaults deny rewrite; only wording/presentation surfaces should opt in explicitly. "
            "Co-authoritative with NarrativeLlmTranslationConstraintsV1.may_translate_section_ids."
        ),
    )


class NarrativeClaimBoundaryV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    allowed_claim_strength: NarrativeClaimStrengthV1 = NarrativeClaimStrengthV1.pattern_and_association_only
    allowed_consumer_wording: str = Field(
        default="non_diagnostic_pattern_language",
        max_length=120,
        description="Governed wording tier for consumer copy — not free prose.",
    )
    prohibited_claim_patterns: List[str] = Field(
        default_factory=list,
        description="Substring patterns (lower snake/phrasing) unsafe for Layer C consumer copy.",
    )
    clinician_only_reserved: bool = Field(default=True)


class NarrativeEvidenceBoundaryV1(BaseModel):
    """Defines what evidence each section may cite and what must not be score basis."""

    model_config = ConfigDict(extra="forbid")

    section_id: NarrativeSectionIdV1
    allowed_evidence_sources: List[str] = Field(default_factory=list)
    forbidden_as_score_basis: List[str] = Field(
        default_factory=list,
        description="Subsystem or pathway ids that must not be described as the score basis.",
    )
    must_not_claim: List[str] = Field(
        default_factory=list,
        description="Substring patterns this section must not assert.",
    )


class NarrativeScoreHierarchyV1(BaseModel):
    """Layer B score precedence guidance — does not change score calculations."""

    model_config = ConfigDict(extra="forbid")

    domain_scores_are_domain_summaries: bool = True
    marker_scores_must_not_dominate_main_narrative: bool = True
    evidence_completeness_modulates_confidence: bool = True
    limited_coverage_must_be_surfaced: bool = True
    hidden_support_evidence_must_not_be_score_basis: bool = True
    overall_score_must_not_compete_with_primary_finding: bool = True
    guidance_lines: List[str] = Field(default_factory=list)


class NarrativeLlmTranslationConstraintsV1(BaseModel):
    """Future LLM boundary — translation only, no independent reasoning."""

    model_config = ConfigDict(extra="forbid")

    llm_role: Literal["translate_governed_brief_only"] = "translate_governed_brief_only"
    prohibited_actions: List[str] = Field(default_factory=list)
    must_preserve_fields: List[str] = Field(default_factory=list)
    may_translate_section_ids: List[str] = Field(
        default_factory=list,
        description=(
            "Allowlist of section_ids the LLM may rephrase. "
            "Empty list means deny-all: no sections may be LLM-translated."
        ),
    )

    @field_validator("may_translate_section_ids")
    @classmethod
    def _validate_translate_section_ids(cls, values: List[str]) -> List[str]:
        valid = {member.value for member in NarrativeSectionIdV1}
        for section_id in values:
            if section_id not in valid:
                raise ValueError(f"invalid may_translate_section_id: {section_id}")
        return values


class NarrativePayloadV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload_schema_version: str = Field(default=NARRATIVE_PAYLOAD_SCHEMA_VERSION)
    analysis_id: str
    report_v1: ReportV1
    top_findings: List[ReportTopFindingV1] = Field(default_factory=list)
    root_cause_v1: Optional[RootCauseV1] = None
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None
    report_story_priority: List[str] = Field(
        default_factory=list,
        description="Ordered section ids for report-level narrative precedence.",
    )
    section_intents: Dict[str, NarrativeSectionIntentV1] = Field(default_factory=dict)
    evidence_boundaries: Dict[str, NarrativeEvidenceBoundaryV1] = Field(default_factory=dict)
    score_hierarchy: Optional[NarrativeScoreHierarchyV1] = None
    required_caveats: List[str] = Field(default_factory=list)
    claim_boundaries: NarrativeClaimBoundaryV1
    future_llm_translation_constraints: Optional[NarrativeLlmTranslationConstraintsV1] = None
    missing_marker_caution_refs: Optional[List[str]] = Field(
        default=None,
        description=(
            "Optional governed missing-marker caution refs (missing_marker_id values). "
            "Populated when P2-2+P2-3 caution fields are surfaced on the brief."
        ),
    )

    @field_validator("report_story_priority")
    @classmethod
    def _validate_report_story_priority(cls, values: List[str]) -> List[str]:
        valid = {member.value for member in NarrativeSectionIdV1}
        for section_id in values:
            if section_id not in valid:
                raise ValueError(f"invalid report_story_priority section_id: {section_id}")
        return values

    @model_validator(mode="after")
    def _validate_brief_safety_constraints(self) -> Self:
        constraints = self.future_llm_translation_constraints
        may_translate = list(constraints.may_translate_section_ids) if constraints else []
        any_rewrite_flag = any(
            intent.future_llm_may_rewrite for intent in self.section_intents.values()
        )

        if may_translate and constraints is None:
            raise ValueError(
                "future_llm_translation_constraints required when may_translate_section_ids is non-empty"
            )
        if any_rewrite_flag and constraints is None:
            raise ValueError(
                "future_llm_translation_constraints required when any section has future_llm_may_rewrite=True"
            )
        if self.section_intents and not self.required_caveats:
            raise ValueError("required_caveats must be non-empty when section_intents are present")

        for reserved in LLM_CLINICIAN_RESERVED_SECTION_IDS:
            if reserved in may_translate:
                raise ValueError(
                    f"clinician-reserved section {reserved} must not appear in may_translate_section_ids"
                )

        return self


DEFAULT_PROHIBITED_CLAIM_PATTERNS: List[str] = [
    "diagnosis",
    "diagnoses",
    "diagnostic",
    "confirms",
    "confirmed",
    "rules out",
    "guarantees",
    "treatment recommendation",
    "medication recommendation",
    "supplement recommendation",
]

DEFAULT_REQUIRED_CAVEATS: List[str] = [
    "non_diagnostic_interpretation",
    "general_education_only",
]

DEFAULT_LLM_PROHIBITED_ACTIONS: List[str] = [
    "reason_independently",
    "inspect_raw_biomarkers_outside_brief",
    "decide_findings_or_hierarchy",
    "decide_confidence_or_next_steps",
    "expose_raw_pass3_hypotheses",
    "expose_contradiction_markers_unless_governed",
    "expose_confirmatory_tests_unless_governed",
    # Explicit no-new-findings guard (also partially covered by reason_independently).
    "introduce_findings_not_in_governed_brief",
]

# MED-REV-1 hidden_v1 subsystems — must not be described as visible score basis.
# Aligns with WAVE1_MED_REV1_HIDDEN_SUBSYSTEM_IDS in health_system_card_evidence.py.
WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS: List[str] = [
    "wave1_cv_homocysteine_pathway",
    "wave1_cv_vascular_strain",
    "wave1_met_insulin_metabolic",
    "wave1_liv_enzyme_pattern",
    "wave1_liv_processing_context",
]

GOVERNED_BRIEF_CORE_SECTION_INTENT_IDS: frozenset[str] = frozenset(
    {
        NarrativeSectionIdV1.retail_summary.value,
        NarrativeSectionIdV1.lead_narrative.value,
        NarrativeSectionIdV1.body_overview.value,
        NarrativeSectionIdV1.next_steps_narrative.value,
        NarrativeSectionIdV1.clinician_synthesis.value,
        NarrativeSectionIdV1.missing_evidence_limitations.value,
        NarrativeSectionIdV1.health_systems_context.value,
    }
)
