"""
LabOrigin model - deterministic lab provider/source metadata.

Sprint 2 - Lab Header Detection. Minimal, serialisable.
"""

from typing import Optional
from pydantic import BaseModel, Field


class LabOrigin(BaseModel):
    """Lab provider/source detected during ingestion."""

    lab_provider_id: str = Field(
        ...,
        description="Canonical token; 'unknown' if none",
    )
    lab_provider_name: Optional[str] = Field(
        default=None,
        description="Display name from registry",
    )
    detection_method: str = Field(
        ...,
        description="header_regex | footer_regex | filename | manual | unknown",
    )
    detection_confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="0.0–1.0",
    )
    raw_evidence: Optional[str] = Field(
        default=None,
        description="Short matched string",
    )

    def to_dict(self) -> dict:
        """Serialise for API responses."""
        return {
            "lab_provider_id": self.lab_provider_id,
            "lab_provider_name": self.lab_provider_name,
            "detection_method": self.detection_method,
            "detection_confidence": self.detection_confidence,
            "raw_evidence": self.raw_evidence,
        }


def lab_origin_unknown() -> LabOrigin:
    """Factory for unknown lab origin."""
    return LabOrigin(
        lab_provider_id="unknown",
        lab_provider_name=None,
        detection_method="unknown",
        detection_confidence=0.0,
        raw_evidence=None,
    )
