"""
WP2 / LAYER-B-1 — Layer B → Layer C narrative input payload (Path B).

Formal handoff object ahead of Sprint 3. Does not duplicate ReportV1 medical definitions.
LAYER-B-1 extends the brief with section intents, evidence boundaries, score hierarchy,
and future LLM translation constraints.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.report_v1 import ReportTopFindingV1, ReportV1
from core.contracts.root_cause_v1 import RootCauseV1

NARRATIVE_PAYLOAD_SCHEMA_VERSION = "v1.1"


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
        default=True,
        description="Whether a future LLM translator may rephrase this section within constraints.",
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
    may_translate_section_ids: List[str] = Field(default_factory=list)


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

DEFAULT_LLM_PROHIBITED_ACTIONS: List[str] = [
    "reason_independently",
    "inspect_raw_biomarkers_outside_brief",
    "decide_findings_or_hierarchy",
    "decide_confidence_or_next_steps",
    "expose_raw_pass3_hypotheses",
    "expose_contradiction_markers_unless_governed",
    "expose_confirmatory_tests_unless_governed",
]

WAVE1_HIDDEN_SUBSYSTEM_FORBIDDEN_AS_SCORE_BASIS: List[str] = [
    "wave1_cv_homocysteine_pathway",
    "wave1_cv_vascular_strain",
    "wave1_met_insulin_metabolic",
    "wave1_liv_enzyme_pattern",
    "wave1_liv_processing_context",
]
