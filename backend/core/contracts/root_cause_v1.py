"""
KB-S33 Root Cause output contract v1.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field


class RootCauseEvidenceItemV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    item: str = Field(max_length=120)
    marker_refs: List[str] = Field(default_factory=list)


class RootCauseMissingItemV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    marker_id: str
    reason: str = Field(max_length=120)


class RootCauseConfirmatoryTestV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    test_id: str
    display_name: str
    rationale: str = Field(max_length=120)


class RootCauseHypothesisV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str
    title: str
    summary: str = Field(max_length=200)
    hypothesis_confidence: float
    evidence_for: List[RootCauseEvidenceItemV1] = Field(default_factory=list)
    evidence_against: List[RootCauseEvidenceItemV1] = Field(default_factory=list)
    missing_data: List[RootCauseMissingItemV1] = Field(default_factory=list)
    confirmatory_tests: List[RootCauseConfirmatoryTestV1] = Field(default_factory=list)
    safety_class: str


class RootCauseFindingV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    signal_id: str
    primary_metric: str
    signal_state: str
    signal_confidence: float
    hypotheses: List[RootCauseHypothesisV1] = Field(default_factory=list)


class RootCauseV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = Field(default="v1")
    findings: List[RootCauseFindingV1] = Field(default_factory=list)
