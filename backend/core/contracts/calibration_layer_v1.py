"""
v5.3 Phase 3 Sprint 5 - OutcomeCalibrationLayer_v1 contract.
"""

from __future__ import annotations

import hashlib
import json
from typing import List, Literal

from pydantic import BaseModel, ConfigDict, Field

CALIBRATION_LAYER_V1_VERSION = "1.0.0"


class CalibrationItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    system_id: str
    priority_tier: Literal["p0", "p1", "p2", "p3"]
    urgency_band: Literal["urgent", "soon", "routine", "monitor"]
    action_intensity: Literal["high", "medium", "low", "info"]
    stability_flag: Literal["stable", "unstable", "insufficient"]
    explanation_codes: List[str] = Field(default_factory=list)
    applied_rule_ids: List[str] = Field(default_factory=list)


class CalibrationStamp(BaseModel):
    model_config = ConfigDict(extra="forbid")

    calibration_version: str
    calibration_hash: str


def canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
