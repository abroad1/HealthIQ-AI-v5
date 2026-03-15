"""
KB-S32 Report Compiler Contract v1.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from core.contracts.root_cause_v1 import RootCauseV1


class ReportTopFindingV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority_rank: int
    signal_id: str
    system: str
    signal_state: str
    confidence: float
    confidence_reasons: List[str] = Field(default_factory=list)
    primary_metric: str
    supporting_markers: List[str] = Field(default_factory=list)
    why_it_matters: str = Field(max_length=200)


class ReportTopChainV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    priority_rank: int
    chain_id: str
    confidence: float
    signals_involved: List[str] = Field(default_factory=list)
    summary_tokens: List[str] = Field(default_factory=list)
    summary_text: str = Field(max_length=200)


class ReportInterventionV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_id: str
    title: str
    body: str
    why_this_matters: str = Field(max_length=200)
    signal_refs: List[str] = Field(default_factory=list)
    chain_refs: List[str] = Field(default_factory=list)
    evidence_strength: str
    evidence_summary: str
    safety_class: str
    escalation_required: bool
    contraindications: Optional[List[str]] = None
    retest_guidance: Optional[str] = None


class ReportActionsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    interventions: List[ReportInterventionV1] = Field(default_factory=list)
    clinician_referrals: List[ReportInterventionV1] = Field(default_factory=list)
    monitoring: List[ReportInterventionV1] = Field(default_factory=list)


class ReportMetaV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_registry_version: str
    signal_registry_hash_sha256: str
    interaction_map_revision: str
    safety_contract_version: str
    generated_at: str


class ReportV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    report_version: str = Field(default="v1")
    top_findings: List[ReportTopFindingV1] = Field(default_factory=list)
    top_chains: List[ReportTopChainV1] = Field(default_factory=list)
    actions: ReportActionsV1
    meta: ReportMetaV1
    root_cause_v1: Optional[RootCauseV1] = None
