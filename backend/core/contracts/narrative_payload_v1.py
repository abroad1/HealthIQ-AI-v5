"""
WP2 — Layer B → Layer C narrative input payload (Path B).

Formal handoff object ahead of Sprint 3. Does not duplicate ReportV1 medical definitions.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from core.contracts.intervention_annotation_v1 import InterventionAnnotationsV1
from core.contracts.report_v1 import ReportTopFindingV1, ReportV1
from core.contracts.root_cause_v1 import RootCauseV1

NARRATIVE_PAYLOAD_SCHEMA_VERSION = "v1"


class NarrativeIntentCodeV1(str, Enum):
    reassure = "reassure"
    prioritise = "prioritise"
    explain_mechanism = "explain_mechanism"
    express_uncertainty = "express_uncertainty"
    frame_next_steps = "frame_next_steps"
    support_clinician_fast_read = "support_clinician_fast_read"


class NarrativeSectionIdV1(str, Enum):
    retail_summary = "retail_summary"
    lead_narrative = "lead_narrative"
    body_overview = "body_overview"
    next_steps_narrative = "next_steps_narrative"
    clinician_synthesis = "clinician_synthesis"


class NarrativeClaimStrengthV1(str, Enum):
    """Bounded consumer claim posture — descriptive only."""

    pattern_and_association_only = "pattern_and_association_only"


class NarrativeSectionIntentV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    section_id: NarrativeSectionIdV1
    intent_code: NarrativeIntentCodeV1
    permitted_source_fields: List[str] = Field(default_factory=list)
    fallback_rule: Literal["omit_section_if_sources_missing"] = "omit_section_if_sources_missing"


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


class NarrativePayloadV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload_schema_version: str = Field(default=NARRATIVE_PAYLOAD_SCHEMA_VERSION)
    analysis_id: str
    report_v1: ReportV1
    top_findings: List[ReportTopFindingV1] = Field(default_factory=list)
    root_cause_v1: Optional[RootCauseV1] = None
    intervention_annotations_v1: Optional[InterventionAnnotationsV1] = None
    section_intents: Dict[str, NarrativeSectionIntentV1] = Field(default_factory=dict)
    claim_boundaries: NarrativeClaimBoundaryV1


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
