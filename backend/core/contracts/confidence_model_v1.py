"""
Sprint 8 - Confidence Model v1 Contract.

Deterministic confidence and missing-data model. Layer B only.
LLM receives structured confidence; no inference from absence.

PRD §4.3, §4.4; Delivery Plan Sprint 8.
"""

from typing import Dict, List
from pydantic import BaseModel, ConfigDict, Field

# Version stamp for replay determinism
CONFIDENCE_MODEL_V1_VERSION = "1.0.0"


class ConfidenceModelV1(BaseModel):
    """
    Deterministic confidence model — Layer B output only.

    No timestamps. No dynamic weighting. Purely deterministic from Layer B outputs.
    """

    model_config = ConfigDict(frozen=False, extra="forbid")

    model_version: str = Field(
        default=CONFIDENCE_MODEL_V1_VERSION,
        description="Contract version",
    )

    # 0.0–1.0; equal-weighted average of cluster_confidence
    system_confidence: float = Field(
        default=0.0,
        description="Weighted average of cluster confidence (equal weighting)",
    )

    # Per-cluster: proportion of required markers present (0.0–1.0)
    cluster_confidence: Dict[str, float] = Field(
        default_factory=dict,
        description="cluster_id -> confidence (0–1)",
    )

    # Per-biomarker: 1.0 if present and valid, 0.0 if required but missing
    biomarker_confidence: Dict[str, float] = Field(
        default_factory=dict,
        description="biomarker_id -> confidence (0 or 1)",
    )

    # Union of all required biomarkers that are missing (deterministic order)
    missing_required_biomarkers: List[str] = Field(
        default_factory=list,
        description="Required biomarkers not present",
    )

    # Clusters with at least one missing required biomarker
    missing_required_clusters: List[str] = Field(
        default_factory=list,
        description="Cluster IDs with incomplete required coverage",
    )

    # Schema version references (for replay)
    cluster_schema_version: str = Field(default="", description="From cluster schema")
    cluster_schema_hash: str = Field(default="", description="From cluster schema")
    ratio_registry_version: str = Field(default="", description="From ratio registry")
