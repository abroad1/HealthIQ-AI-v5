"""
Sprint 11 - Deterministic Explainability Report v1 contract.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field

EXPLAINABILITY_REPORT_V1_VERSION = "1.0.0"


class ExplainabilityRunMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    report_version: str = Field(default=EXPLAINABILITY_REPORT_V1_VERSION)
    run_id: str = Field(default="")
    scenario_id: str = Field(default="")
    git_commit_short: str = Field(default="")
    generated_at_utc: str = Field(default="")


class ExplainabilityConflictItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conflict_type: str = Field(default="")
    conflict_id: str = Field(default="")
    from_system_id: str = Field(default="")
    to_system_id: str = Field(default="")
    severity: str = Field(default="")
    rationale_codes: List[str] = Field(default_factory=list)


class ExplainabilityPrecedenceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    precedence_tier: int = Field(default=0)
    rule_id: str = Field(default="")
    conflict_id: str = Field(default="")
    conflict_type: str = Field(default="")
    from_system_id: str = Field(default="")
    to_system_id: str = Field(default="")
    rationale_codes: List[str] = Field(default_factory=list)


class ExplainabilityDominanceEdgeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    from_system_id: str = Field(default="")
    to_system_id: str = Field(default="")
    edge_id: str = Field(default="")
    source: str = Field(default="")


class ExplainabilityCycleCheck(BaseModel):
    model_config = ConfigDict(extra="forbid")
    has_cycle: bool = Field(default=False)
    status_code: str = Field(default="")


class ExplainabilityDominanceResolution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    cycle_check: ExplainabilityCycleCheck
    direct_edges: List[ExplainabilityDominanceEdgeItem] = Field(default_factory=list)
    transitive_edges: List[ExplainabilityDominanceEdgeItem] = Field(default_factory=list)


class ExplainabilityCausalEdgeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    edge_id: str = Field(default="")
    from_system_id: str = Field(default="")
    to_system_id: str = Field(default="")
    edge_code: str = Field(default="")
    priority: int = Field(default=0)
    source_conflict_ids: List[str] = Field(default_factory=list)


class ExplainabilityArbitrationDecisions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    primary_driver_system_id: str = Field(default="")
    supporting_systems: List[str] = Field(default_factory=list)
    decision_trace: List[str] = Field(default_factory=list)
    tie_breakers: List[str] = Field(default_factory=list)


class ExplainabilityCalibrationImpact(BaseModel):
    model_config = ConfigDict(extra="forbid")
    system_id: str = Field(default="")
    final_calibration_tier: str = Field(default="")
    reasons: List[str] = Field(default_factory=list)


class ExplainabilityReplayStamps(BaseModel):
    model_config = ConfigDict(extra="forbid")
    conflict_registry_version: str = Field(default="")
    conflict_registry_hash: str = Field(default="")
    arbitration_registry_version: str = Field(default="")
    arbitration_registry_hash: str = Field(default="")
    arbitration_version: str = Field(default="")
    arbitration_hash: str = Field(default="")
    explainability_hash: str = Field(default="")


class ExplainabilityReportV1(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_metadata: ExplainabilityRunMetadata
    conflict_summary: List[ExplainabilityConflictItem] = Field(default_factory=list)
    precedence_summary: List[ExplainabilityPrecedenceItem] = Field(default_factory=list)
    dominance_resolution: ExplainabilityDominanceResolution
    causal_edges: List[ExplainabilityCausalEdgeItem] = Field(default_factory=list)
    arbitration_decisions: ExplainabilityArbitrationDecisions
    calibration_impact: ExplainabilityCalibrationImpact
    replay_stamps: ExplainabilityReplayStamps
