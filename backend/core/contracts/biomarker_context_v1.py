"""
Sprint 11 - BiomarkerContext v1 Contract.

Deterministic, code-only explanatory context for safe Layer C prompting.
"""

import hashlib
import json
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

BIOMARKER_CONTEXT_V1_VERSION = "1.0.0"


class BiomarkerContextNode(BaseModel):
    """Safe explanatory context node for a single biomarker."""

    model_config = ConfigDict(extra="forbid")

    biomarker_id: str
    status: str  # low | normal | high | unknown
    score: Optional[float] = None
    reason_codes: List[str] = Field(default_factory=list)
    missing_codes: List[str] = Field(default_factory=list)
    relationship_codes: List[str] = Field(default_factory=list)


class BiomarkerContextStamp(BaseModel):
    """Version/hash stamp for deterministic replay."""

    model_config = ConfigDict(extra="forbid")

    biomarker_context_version: str
    biomarker_context_hash: str


def canonical_json_sha256(obj: object) -> str:
    """Stable SHA-256 hash of canonical JSON payload."""
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
