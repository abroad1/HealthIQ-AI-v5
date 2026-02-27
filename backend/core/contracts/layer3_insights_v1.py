"""
Sprint 22 — Layer 3 Insight Assembly contract v1.0.0.

Deterministic, rule-based user-facing insight artifact.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

LAYER3_INSIGHTS_SCHEMA_VERSION = "1.0.0"

SYSTEM_CARD_IDS = (
    "cardiovascular__system_pressure",
    "metabolic__system_pressure",
    "hepatic__system_pressure",
    "immune__system_pressure",
    "renal__system_pressure",
    "hormonal__system_pressure",
    "hematological__system_pressure",
    "musculoskeletal__system_pressure",
    "nutritional__system_pressure",
    "autonomic__system_pressure",
    "thyroid__system_pressure",
)


class EvidenceBiomarker(BaseModel):
    """Biomarker evidence entry."""

    model_config = ConfigDict(extra="forbid")

    biomarker_id: str = Field(..., description="Canonical biomarker name")
    value: float = Field(..., description="Value")
    unit: str = Field(default="", description="Unit")
    reference_min: Optional[float] = Field(default=None, description="Lab reference min")
    reference_max: Optional[float] = Field(default=None, description="Lab reference max")
    score: Optional[float] = Field(default=None, description="Normalized score 0-1")


class EvidenceDerived(BaseModel):
    """Derived marker evidence entry."""

    model_config = ConfigDict(extra="forbid")

    marker_id: str = Field(..., description="Derived marker name")
    value: float = Field(..., description="Value")


class EvidenceLifestyle(BaseModel):
    """Lifestyle modifier evidence entry."""

    model_config = ConfigDict(extra="forbid")

    input_name: str = Field(..., description="Lifestyle input")
    modifier: float = Field(..., description="Applied modifier")
    capped_modifier: float = Field(..., description="Capped modifier")


class EvidenceSystemBurden(BaseModel):
    """System burden evidence entry."""

    model_config = ConfigDict(extra="forbid")

    system_id: str = Field(..., description="System identifier")
    base_burden: float = Field(..., description="Base burden 0-1")
    adjusted_burden: float = Field(..., description="Adjusted burden 0-1")


class EvidenceBlock(BaseModel):
    """Evidence block. Omit sections that are empty."""

    model_config = ConfigDict(extra="forbid")

    biomarkers: Optional[List[EvidenceBiomarker]] = Field(default=None)
    derived_markers: Optional[List[EvidenceDerived]] = Field(default=None)
    lifestyle: Optional[List[EvidenceLifestyle]] = Field(default=None)
    system_burdens: Optional[List[EvidenceSystemBurden]] = Field(default=None)


class InsightCard(BaseModel):
    """Single insight card. No timestamp fields."""

    model_config = ConfigDict(extra="forbid")

    insight_id: str = Field(..., description="Stable deterministic ID")
    system_id: str = Field(..., description="System identifier")
    title: str = Field(..., description="Title")
    severity: Literal["action", "watch", "info"] = Field(...)
    confidence: Literal["high", "medium", "low"] = Field(...)
    evidence: EvidenceBlock = Field(...)
    interpretation: str = Field(..., description="Deterministic interpretation text")
    next_steps: List[str] = Field(default_factory=list)
    flags: Optional[List[str]] = Field(default=None)


class Layer3InsightsV1(BaseModel):
    """Layer 3 insight assembly root. schema_version must be exactly 1.0.0."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0.0"] = Field(
        default="1.0.0",
        description="Contract version. Do not auto-increment.",
    )
    insights: List[InsightCard] = Field(default_factory=list)
    summary: Optional[Dict[str, Any]] = Field(default=None)
