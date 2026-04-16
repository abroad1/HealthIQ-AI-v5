"""
BE-IDL-1 — Interpretation Display Layer (IDL) v1 contract.

Governed display metadata for Section 5 pattern cards; sole retail taxonomy authority.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

ScientificClassV1 = Literal["phenotype", "risk_construct", "organ_pattern", "syndrome_state"]

FrontendAllowedTermV1 = Literal["phenotype_allowed", "clinical_only"]

SeverityStateV1 = Literal["not_observed", "watch", "attention", "strong_signal"]


class InterpretationDisplayRecordV1(BaseModel):
    """Single interpretation entity for retail/clinical display (IDL v1)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    internal_id: str = Field(..., description="Canonical ph_* interpretation id")
    scientific_class: ScientificClassV1
    clinical_display_label: str
    retail_display_label: str
    subtitle: str
    why_it_matters: str
    severity_state: SeverityStateV1
    supporting_biomarkers_summary: str
    frontend_allowed_term: FrontendAllowedTermV1
    display_order_priority: int = Field(..., ge=1, le=999)
    enabled_for_frontend: bool

    supporting_systems_summary: Optional[str] = None
    user_safe_description: Optional[str] = None
    future_commercial_domain: Optional[str] = None
    display_caveat: Optional[str] = None


class InterpretationDisplayLayerBundleV1(BaseModel):
    """Versioned IDL bundle attached to analysis results."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = Field(default="1.0.0", description="IDL bundle schema version")
    records: List[InterpretationDisplayRecordV1] = Field(default_factory=list)
