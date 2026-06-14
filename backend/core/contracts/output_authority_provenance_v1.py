"""
ARCH-COMPLETION-2 — Compiled output authority provenance contract v1.

Additive metadata for day-one governed analytical output traceability.
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class OutputElementAuthorityV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    output_element_id: str
    output_element_type: str
    source_signal_ids: List[str] = Field(default_factory=list)
    source_package_ids: List[str] = Field(default_factory=list)
    source_biomarker_ids: List[str] = Field(default_factory=list)
    source_context_keys: List[str] = Field(default_factory=list)
    source_root_cause_ids: List[str] = Field(default_factory=list)
    authority_register_ref: str = ""
    authority_status: str
    wording_strength: str = "informational"
    generated_by: str


class OutputAuthorityProvenanceBundleV1(BaseModel):
    model_config = ConfigDict(extra="forbid")

    version: str = Field(default="v1")
    authority_model_ref: str
    root_cause_register_ref: str
    card_register_ref: str
    governed_elements: List[OutputElementAuthorityV1] = Field(default_factory=list)
    quarantined_elements: List[OutputElementAuthorityV1] = Field(default_factory=list)
