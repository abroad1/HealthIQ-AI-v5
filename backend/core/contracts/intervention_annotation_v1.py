"""
KB-S48e parallel intervention annotation contract v1.

Separate from RootCauseHypothesisV1 / root_cause_v1 — annotation-only runtime output
derived from user intervention records + intervention-effects registry.
"""

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

EffectTypeV1 = Literal[
    "interpretation_confounder",
    "expected_biomarker_effect",
    "monitoring_relevance",
    "caveat_only",
]

ExpectedDirectionV1 = Literal["lower", "raise", "variable", "mixed", "context_dependent"]


class InterventionAnnotationEffectV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    effect_type: EffectTypeV1
    biomarker_ids: List[str] = Field(default_factory=list)
    expected_direction: ExpectedDirectionV1
    monitoring_relevance: Optional[str] = Field(default=None, max_length=500)


class InterventionAnnotationResolvedV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_record_id: str
    entered_label: str = Field(max_length=500)
    intervention_class_id: str
    effects: List[InterventionAnnotationEffectV1] = Field(default_factory=list)


class InterventionAnnotationUnresolvedV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    intervention_record_id: str
    entered_label: str = Field(max_length=500)
    note: str = Field(
        default=(
            "Not mapped to a canonical intervention class; registry interpretation "
            "effects were not applied."
        ),
        max_length=300,
    )


class InterventionAnnotationsV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: Literal["v1"] = "v1"
    registry_id: str = "intervention_effects_registry_v1"
    registry_schema_version: str = ""
    resolved: List[InterventionAnnotationResolvedV1] = Field(default_factory=list)
    unresolved: List[InterventionAnnotationUnresolvedV1] = Field(default_factory=list)
