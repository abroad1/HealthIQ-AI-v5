"""
v5.3 Sprint 2 - Multi-Marker State Engine v1 Contract.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Literal

from pydantic import BaseModel, ConfigDict

STATE_ENGINE_V1_VERSION = "1.0.0"


class SystemStateNode(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_id: str
    state_codes: List[str]
    rationale_codes: List[str]
    transition_summary_codes: List[str]
    confidence_bucket: Literal["high", "moderate", "low", "insufficient"]


class StateEngineStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    state_engine_version: str
    state_engine_hash: str


def canonical_json_sha256(payload: Dict[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
