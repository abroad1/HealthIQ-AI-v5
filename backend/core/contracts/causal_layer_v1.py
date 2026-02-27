"""
v5.3 Phase 3 Sprint 4 - CausalLayer_v1 contract.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict

CAUSAL_LAYER_V1_VERSION = "1.0.0"


class CausalEdgeNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    edge_id: str
    from_system_id: str
    to_system_id: str
    edge_type: Literal["driver", "amplifier", "constraint"]
    priority: int
    rationale_codes: List[str]


class CausalLayerStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    causal_layer_version: str
    causal_layer_hash: str


def canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
