"""
N-8 — Deterministic narrative report contract v1.

Authoritative compiled narrative sections (architecture §5). Separate from ReportV1 / ClinicianReportV1.
"""

from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, ConfigDict, Field

NARRATIVE_REPORT_V1_VERSION = "1.0.0"


class NarrativeReportV1(BaseModel):
    """Compiled deterministic narrative sections for API/runtime consumption."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    narrative_report_version: str = Field(default=NARRATIVE_REPORT_V1_VERSION)
    retail_summary: str = Field(default="", description="Lay-readable summary (v1 may be empty)")
    body_overview: str = Field(default="", description="Cross-system posture (v1 bounded)")
    lead_narrative: str = Field(default="", description="Lead pathway / pattern narrative blocks")
    secondary_narratives: str = Field(default="", description="Secondary pattern narrative blocks")
    longitudinal_narrative: str = Field(default="", description="Direction-of-travel narrative")
    secondary_systems: str = Field(default="", description="Non-lead systems worth noting")
    next_steps_narrative: str = Field(default="", description="Prioritised follow-up narrative")
    clinician_synthesis: str = Field(default="", description="Richer clinician-facing synthesis")
    meta: Dict[str, Any] = Field(
        default_factory=dict,
        description="Compiler stamps, asset resolution notes, skip reasons (inspectable, deterministic)",
    )
