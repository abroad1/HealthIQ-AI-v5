"""
Sprint 10 - RelationshipRegistry v1 Contract.

Schema-driven deterministic biomarker relationship definitions and runtime detections.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

RELATIONSHIP_REGISTRY_V1_VERSION = "1.0.0"


class RelationshipRuleCondition(BaseModel):
    """Single deterministic condition against safe status/score views."""

    model_config = ConfigDict(extra="forbid")

    biomarker: Optional[str] = None
    derived_marker: Optional[str] = None
    status_in: Optional[List[Literal["low", "normal", "high", "unknown"]]] = None
    score_gte: Optional[float] = None
    present: Optional[bool] = None
    evidence_code: str

    @model_validator(mode="after")
    def validate_selector(self) -> "RelationshipRuleCondition":
        selected = int(bool(self.biomarker)) + int(bool(self.derived_marker))
        if selected != 1:
            raise ValueError("condition must define exactly one of biomarker or derived_marker")
        return self


class RelationshipRuleGroup(BaseModel):
    """Recursive deterministic logic group."""

    model_config = ConfigDict(extra="forbid")

    all: Optional[List["RelationshipRuleNode"]] = None
    any: Optional[List["RelationshipRuleNode"]] = None

    @model_validator(mode="after")
    def validate_group(self) -> "RelationshipRuleGroup":
        selected = int(self.all is not None) + int(self.any is not None)
        if selected != 1:
            raise ValueError("logic group must define exactly one of all/any")
        return self


class RelationshipRuleNode(BaseModel):
    """Union wrapper for recursive model parsing."""

    model_config = ConfigDict(extra="forbid")

    all: Optional[List["RelationshipRuleNode"]] = None
    any: Optional[List["RelationshipRuleNode"]] = None
    biomarker: Optional[str] = None
    derived_marker: Optional[str] = None
    status_in: Optional[List[Literal["low", "normal", "high", "unknown"]]] = None
    score_gte: Optional[float] = None
    present: Optional[bool] = None
    evidence_code: Optional[str] = None

    @model_validator(mode="after")
    def validate_node(self) -> "RelationshipRuleNode":
        is_group = (self.all is not None) or (self.any is not None)
        is_condition = bool(self.biomarker or self.derived_marker or self.evidence_code)
        if is_group == is_condition:
            raise ValueError("rule node must be either a logic group or a condition")
        if is_condition and not self.evidence_code:
            raise ValueError("condition node must include evidence_code")
        if is_condition:
            selected = int(bool(self.biomarker)) + int(bool(self.derived_marker))
            if selected != 1:
                raise ValueError("condition node must define exactly one of biomarker/derived_marker")
        return self


class RelationshipDefinition(BaseModel):
    """Registry definition loaded from relationships.yaml."""

    model_config = ConfigDict(extra="forbid")

    relationship_id: str
    version: str
    biomarkers: List[str] = Field(min_length=2, max_length=2)
    uses_derived_markers: Optional[List[str]] = None
    logic: RelationshipRuleNode
    classification_code: str
    severity: Literal["low", "moderate", "high"]
    description_short: str

    @model_validator(mode="after")
    def validate_description(self) -> "RelationshipDefinition":
        if len(self.description_short) > 140:
            raise ValueError("description_short must be <= 140 chars")
        return self


class RelationshipDetection(BaseModel):
    """Runtime relationship detection output for InsightGraph."""

    model_config = ConfigDict(extra="forbid")

    relationship_id: str
    version: str
    biomarkers: List[str] = Field(min_length=2, max_length=2)
    classification_code: str
    severity: Literal["low", "moderate", "high"]
    triggered: bool
    evidence: List[str] = Field(default_factory=list)


class RelationshipRegistryStamp(BaseModel):
    """Version/hash stamp used for replay determinism."""

    model_config = ConfigDict(extra="forbid")

    relationship_registry_version: str
    relationship_registry_hash: str


def canonical_json_sha256(obj: object) -> str:
    """Stable SHA-256 hash of canonical JSON payload."""
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


RelationshipRuleNode.model_rebuild()
