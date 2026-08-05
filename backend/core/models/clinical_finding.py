"""
CLIN-PRIORITY-CORE-1 — Canonical clinical finding models.

Frozen Pydantic models for ConsolidatedConcernSet / ClinicalFinding per
contract v0.6.3 and ARCH-HARDEN identity recommendations.
"""

from __future__ import annotations

import hashlib
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CLINICAL_FINDING_CONTRACT_VERSION = "0.6.3"
CLINICAL_FINDING_RULESET_VERSION = "0.5"

UrgencyTimeBand = Literal["same_day", "within_days", "within_weeks", "routine"]
ConcernTier = Literal[0, 1, 2, 3]
FindingRole = Literal[
    "principal_concern",
    "co_lead",
    "independent_secondary",
    "supporting_evidence",
    "modifier",
    "contextual",
    "insufficient_data",
    "indeterminate_severity",
    "reclassified",
]
PresentationState = Literal["principal", "co_lead", "no_forced_lead", "nested_supporting"]
ReleaseGateStatus = Literal["SPECIFICATION_ONLY", "RELEASE_AUTHORISED"]
SeriousResultState = Literal[
    "not_applicable",
    "tier_0_classified",
    "tier_0_withheld",
]
MissingDataState = Literal[
    "none",
    "not_assessable",
    "insufficient_data",
    "indeterminate_severity",
]


def make_finding_id(
    domain: str,
    finding_type: str,
    constituent_activation_keys: List[str],
) -> str:
    """Deterministic finding identity over domain + type + sorted activation keys."""
    keys = sorted({str(k).strip() for k in constituent_activation_keys if str(k).strip()})
    payload = f"{domain}|{finding_type}|{'|'.join(keys)}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{domain}:{finding_type}:{digest}"


class RuleCitation(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    rule_id: str = Field(..., min_length=1)
    evidence_label: Optional[str] = Field(
        default=None,
        description="[E]/[C]/[J] evidence grade; [U] only as provenance for unset items",
    )
    source_document: Optional[str] = None
    source_version: Optional[str] = None


class FindingProvenance(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    clinical_rule_ids: List[str] = Field(default_factory=list)
    adjudication_ids: List[str] = Field(default_factory=list)
    contract_version: str = CLINICAL_FINDING_CONTRACT_VERSION
    ruleset_version: str = CLINICAL_FINDING_RULESET_VERSION
    compile_run_id: Optional[str] = None
    source_document: Optional[str] = None
    rule_citations: List[RuleCitation] = Field(default_factory=list)


class FindingRelationship(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    related_finding_id: str
    relationship_type: Literal[
        "supporting",
        "contextual",
        "independent_secondary",
        "nested_constituent",
        "co_lead",
    ]
    rationale_codes: List[str] = Field(default_factory=list)


class ClinicalFinding(BaseModel):
    """Governed clinical finding constructed above the signal estate."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    finding_id: str = Field(..., min_length=1)
    domain: str = Field(..., min_length=1)
    finding_type: str = Field(..., min_length=1, description="Taxonomy id e.g. HEP-F1")
    label: str = Field(..., min_length=1)

    constituent_activation_keys: List[str] = Field(
        ...,
        min_length=1,
        description="Required provenance — never drop activation keys after consolidation",
    )
    constituent_biomarker_ids: List[str] = Field(default_factory=list)

    urgency_time_band: UrgencyTimeBand
    severity_band: Optional[str] = None
    severity_indeterminate: bool = False
    concern_tier: ConcernTier
    role: FindingRole
    presentation_state: PresentationState = "principal"

    clinical_significance: Optional[str] = None
    actionability: Optional[str] = None
    interpretive_confidence: Optional[str] = None

    missing_data_state: MissingDataState = "none"
    missing_data_notes: List[str] = Field(default_factory=list)
    caveats: List[str] = Field(default_factory=list)
    prohibited_behaviours_asserted: List[str] = Field(default_factory=list)

    serious_result_state: SeriousResultState = "not_applicable"
    release_gate_status: ReleaseGateStatus = "RELEASE_AUTHORISED"
    withheld: bool = False

    provenance: FindingProvenance = Field(default_factory=FindingProvenance)
    relationships: List[FindingRelationship] = Field(default_factory=list)
    nested_constituent_labels: List[str] = Field(default_factory=list)

    quarantine_flags: List[str] = Field(default_factory=list)
    dependency_flags: List[str] = Field(default_factory=list)

    @field_validator("constituent_activation_keys")
    @classmethod
    def _keys_non_empty_sorted_unique(cls, value: List[str]) -> List[str]:
        cleaned = sorted({str(k).strip() for k in value if str(k).strip()})
        if not cleaned:
            raise ValueError("constituent_activation_keys must retain at least one key")
        return cleaned

    @model_validator(mode="after")
    def _finding_id_matches_identity(self) -> "ClinicalFinding":
        expected = make_finding_id(
            self.domain, self.finding_type, list(self.constituent_activation_keys)
        )
        if self.finding_id != expected:
            raise ValueError(
                f"finding_id mismatch: got {self.finding_id!r}, expected {expected!r}"
            )
        return self


class ConsolidatedConcernSet(BaseModel):
    """Ordered clinical concern set for one analysis snapshot."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    contract_version: str = CLINICAL_FINDING_CONTRACT_VERSION
    ruleset_version: str = CLINICAL_FINDING_RULESET_VERSION
    compile_run_id: Optional[str] = None
    prioritisation_package_version: Optional[str] = None
    prioritisation_package_hash: Optional[str] = None

    findings: List[ClinicalFinding] = Field(default_factory=list)
    lead_finding_ids: List[str] = Field(default_factory=list)
    co_lead_finding_ids: List[str] = Field(default_factory=list)
    presentation_mode: PresentationState = "principal"
    no_forced_lead: bool = False

    no_concern: bool = False
    no_concern_notes: List[str] = Field(default_factory=list)
    domain_notes: List[str] = Field(default_factory=list)

    fib_4_computed: bool = False
    fib_4_displayed: bool = False
    quarantine_notes: List[str] = Field(default_factory=list)
