"""
v5.3 Sprint 3 - Interaction Precedence Engine v1 contract.
"""

from __future__ import annotations

import hashlib
import json
from typing import List

from pydantic import BaseModel, ConfigDict

PRECEDENCE_ENGINE_V1_VERSION = "1.0.0"


class DominantEdge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    from_system_id: str
    to_system_id: str
    rule_id: str


class PrecedenceOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    primary_driver_system_id: str
    dominant_edges: List[DominantEdge]
    conflicts_resolved: List[str]
    rationale_codes: List[str]


class PrecedenceStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    precedence_engine_version: str
    precedence_engine_hash: str


def canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
