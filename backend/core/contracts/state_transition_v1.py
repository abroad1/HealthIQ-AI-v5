"""
v5.3 Sprint 1 - StateTransition v1 Contract.

Deterministic longitudinal status transition metadata for replay and depth.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

STATE_TRANSITION_V1_VERSION = "1.0.0"

TransitionCode = Literal[
    "improving",
    "worsening",
    "stable_normal",
    "stable_abnormal",
    "volatile",
    "insufficient_history",
    "unknown",
]
StatusCode = Literal["low", "normal", "high", "unknown"]


class BiomarkerTransitionNode(BaseModel):
    """Code-only longitudinal transition for one biomarker."""

    model_config = ConfigDict(extra="forbid")

    biomarker_id: str = Field(..., min_length=1)
    from_status: StatusCode
    to_status: StatusCode
    transition: TransitionCode
    evidence_codes: List[str] = Field(default_factory=list)


class StateTransitionStamp(BaseModel):
    """Version/hash stamp used for replay determinism."""

    model_config = ConfigDict(extra="forbid")

    state_transition_version: str
    state_transition_hash: str


def canonical_json_sha256(obj: object) -> str:
    """Stable SHA-256 hash of canonical JSON payload."""
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
