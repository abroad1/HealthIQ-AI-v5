"""
v5.3 Phase 3 Sprint 7 - Arbitration Depth v1 contracts.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

ARBITRATION_V1_VERSION = "1.0.0"


class ConflictItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conflict_id: str
    system_a: str
    system_b: str
    conflict_type: str
    rationale_codes: List[str] = Field(default_factory=list)


class DominanceEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_system_id: str
    to_system_id: str
    rule_id: str
    conflict_id: str
    conflict_type: str
    precedence_tier: int
    rationale_codes: List[str] = Field(default_factory=list)


class CausalEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_id: str
    from_system_id: str
    to_system_id: str
    edge_type: Literal["driver", "amplifier", "constraint"]
    priority: int
    rationale_codes: List[str] = Field(default_factory=list)
    source_conflict_ids: List[str] = Field(default_factory=list)


class ArbitrationNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_driver_system_id: str
    tie_breaker_codes: List[str] = Field(default_factory=list)
    rationale_codes: List[str] = Field(default_factory=list)


class ArbitrationStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    arbitration_version: str
    arbitration_hash: str


def canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
