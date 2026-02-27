"""
Sprint 16 - EvidenceRegistry v1 Contract.

Provenance scaffold: sources, rationale, review ownership for inference assets.
"""

from __future__ import annotations

import hashlib
import json
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

EVIDENCE_REGISTRY_V1_VERSION = "1.0.0"

SourceType = Literal["guideline", "paper", "textbook", "expert_consensus", "internal_policy"]
QualityGrade = Literal["high", "moderate", "low", "unknown"]


class EvidenceItem(BaseModel):
    """Single evidence provenance item from evidence_registry.yaml."""

    model_config = ConfigDict(extra="forbid")

    evidence_id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    source_type: SourceType
    source_ref: str = Field(..., min_length=1)
    quality_grade: QualityGrade
    last_reviewed: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    notes: Optional[str] = None


class EvidenceRegistryStamp(BaseModel):
    """Version/hash stamp used for replay determinism."""

    model_config = ConfigDict(extra="forbid")

    evidence_registry_version: str
    evidence_registry_hash: str


def canonical_json_sha256(obj: object) -> str:
    """Stable SHA-256 hash of canonical JSON payload."""
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
