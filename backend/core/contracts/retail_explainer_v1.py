"""
FE-VISUALISATION-B1A — governed retail / educational explainer contracts (v1).

These content classes are intentionally separate from:
  - BiomarkerScore.interpretation (engine scoring / lab mechanics; personalised path)
  - clinician_report_v1 (structured clinical interpretation)
  - symptom relevance (explicitly deferred)

See docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


RETAIL_EXPLAINER_SCHEMA_VERSION = "1.0.0"


class BiomarkerEducationalExplainerV1(BaseModel):
    """
    Reusable, non-personalised educational copy for a biomarker (retail-safe baseline).
    Must not assert patient-specific conclusions.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = Field(default=RETAIL_EXPLAINER_SCHEMA_VERSION)
    content_class: Literal["biomarker_education"] = "biomarker_education"
    biomarker_id: str = Field(..., description="Canonical biomarker id this block applies to")
    title: str = Field(..., max_length=500)
    body: str = Field(
        ...,
        max_length=8000,
        description="Plain-language educational text; not individual medical advice",
    )


class SystemEducationalExplainerV1(BaseModel):
    """
    Reusable educational context for a body-system / cluster-schema grouping.
    Separable from personalised proof; must read as general education.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = Field(default=RETAIL_EXPLAINER_SCHEMA_VERSION)
    content_class: Literal["system_education"] = "system_education"
    system_key: str = Field(
        ...,
        description="Cluster schema / SSOT system key (e.g. metabolic), not a user id",
    )
    title: str = Field(..., max_length=500)
    body: str = Field(..., max_length=8000)


class ContributionContextV1(BaseModel):
    """
    Bounded, non-speculative linkage context (e.g. cluster membership facts).
    Must not infer diagnosis, symptoms, or causal mechanism beyond explicit grouping.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = Field(default=RETAIL_EXPLAINER_SCHEMA_VERSION)
    content_class: Literal["contribution_context"] = "contribution_context"
    relationship_kind: Literal["cluster_membership"] = "cluster_membership"
    factual_statement: str = Field(..., max_length=500)


class RetailExplainerRegistryV1(BaseModel):
    """Validated SSOT payload for retail explainer registry file."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    registry_version: str = Field(default=RETAIL_EXPLAINER_SCHEMA_VERSION)
    biomarkers: dict[str, dict[str, str]] = Field(
        default_factory=dict,
        description="biomarker_id -> {title, body}",
    )
    systems: dict[str, dict[str, str]] = Field(
        default_factory=dict,
        description="system_key -> {title, body}",
    )
