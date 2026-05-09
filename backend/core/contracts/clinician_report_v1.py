from __future__ import annotations

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal


# ----------------------------
# Core leaf structures
# ----------------------------

class EvidenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item: str = Field(..., min_length=1)
    marker_refs: List[str] = Field(default_factory=list)


class MissingDataItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    marker_id: str
    reason: str


class ConfirmatoryTestItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    test_id: str
    display_name: str
    rationale: str


class HypothesisV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hypothesis_id: str
    title: str
    summary: str
    hypothesis_confidence: float = Field(..., ge=0.0, le=1.0)

    # Deterministic single-line rationale (compiler-generated)
    ranking_rationale: str = Field(..., min_length=1, max_length=220)

    evidence_for: List[EvidenceItem] = Field(default_factory=list)
    evidence_against: List[EvidenceItem] = Field(default_factory=list)
    missing_data: List[MissingDataItem] = Field(default_factory=list)

    confirmatory_tests: List[ConfirmatoryTestItem] = Field(default_factory=list)

    safety_class: Literal["monitoring", "clinician_referral", "lifestyle"]


class RootCauseFindingV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    signal_id: str
    signal_state: str
    signal_confidence: float = Field(..., ge=0.0, le=1.0)
    primary_metric: str
    hypotheses: List[HypothesisV1] = Field(default_factory=list)


# ----------------------------
# Clinician report sections
# ----------------------------

class ClinicianHeaderV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_version: Literal["v1"] = "v1"

    disclaimer_top: str = Field(..., min_length=20, max_length=400)
    footer_line: str = Field(..., min_length=10, max_length=160)


class DataQualityV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    # Always render; used to increase trust even when "all good"
    panel_completeness_present: int = Field(..., ge=0)
    panel_completeness_expected: int = Field(..., ge=0)

    lab_range_quality_by_primary_metric: List[str] = Field(default_factory=list)
    confidence_caveat: str = Field(..., min_length=1, max_length=220)

    data_quality_passed: bool = Field(...)


class Page1SummaryBlockV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    primary_concern: str = Field(..., min_length=1, max_length=160)
    key_findings: List[str] = Field(default_factory=list, max_length=5)
    chains: List[str] = Field(default_factory=list, max_length=2)
    top_hypothesis_line: str = Field(..., min_length=1, max_length=220)
    confidence_and_missing_data: str = Field(..., min_length=1, max_length=220)
    # KB-S54B Phase 2b — ranked ambiguity / policy honesty (PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY v1)
    primary_concern_mode: Literal["distinct_lead", "near_tie_ambiguity", "technical_tiebreak_lead"] = (
        "distinct_lead"
    )
    co_primary_signal_ids: List[str] = Field(default_factory=list, max_length=4)
    ranking_policy_version: str = Field(default="", max_length=220)
    # BE-W2-RQ2 — ranked runner-up from deterministically ordered top_findings[1] (not co_primary_signal_ids alone)
    runner_up_signal_id: str = Field(default="", max_length=120)
    runner_up_topic_line: str = Field(default="", max_length=220)
    runner_up_why_not_lead_line: str = Field(default="", max_length=280)
    intervention_annotation_context: str = Field(
        default="",
        max_length=420,
        description="LC-S2: deterministic Layer B statin annotation summary (registry-derived)",
    )


class ClinicianSectionsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    page1: Page1SummaryBlockV1
    root_cause: Optional[RootCauseFindingV1] = None

    # In clinician report, confirmatory tests are consolidated list (post-suppression)
    confirmatory_tests: List[ConfirmatoryTestItem] = Field(default_factory=list)


class ClinicianReportV1(BaseModel):
    """
    Output contract produced by a deterministic compiler.
    Frontend renderer must not compute selection/suppression logic.
    """
    model_config = ConfigDict(extra="forbid")

    header: ClinicianHeaderV1
    data_quality: DataQualityV1
    sections: ClinicianSectionsV1

    # Audit trail requirements
    suppressed_confirmatory_tests: List[str] = Field(default_factory=list)

    # MEDICATION-CAVEAT-B — bounded interpretation caveat from questionnaire medical representation only
    medication_supplement_interpretation_caveat: Optional[str] = Field(
        default=None,
        max_length=280,
        description="Deterministic caveat from self-reported medication/supplement context; null when not applicable.",
    )
