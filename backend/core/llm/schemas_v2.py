"""
LLM Output Schemas v2 - Strict Pydantic validation for LLM responses.

Sprint 17: Compute-only implementation (not wired to runtime).
Defines strict schemas with extra-forbid and post-validations.
"""

from typing import List, Literal
from pydantic import BaseModel, ConfigDict, Field, confloat, conint, conlist, field_validator, model_validator


class InsightNarrativeV2(BaseModel):
    """Strict schema for individual insight narrative."""
    
    model_config = ConfigDict(frozen=False, extra="forbid")
    
    id: str = Field(..., description="Insight identifier")
    title: str = Field(..., description="Insight title")
    severity: Literal["low", "moderate", "high"] = Field(..., description="Severity level")
    evidence: List[str] = Field(..., description="Evidence references (biomarker/cluster ids)")
    actions: List[str] = Field(..., description="Actionable recommendations (no medical diagnosis)")
    red_flags: List[str] = Field(default_factory=list, description="Red flag identifiers")
    confidence: confloat(ge=0.0, le=1.0) = Field(..., description="Confidence score 0-1")


class LLMResultV2(BaseModel):
    """Strict schema for complete LLM response."""
    
    model_config = ConfigDict(frozen=False, extra="forbid")
    
    insights: conlist(InsightNarrativeV2, min_length=1, max_length=10) = Field(
        ..., 
        description="List of insight narratives (1-10)"
    )
    tokens_used: conint(ge=0) = Field(..., description="Number of tokens used")
    latency_ms: conint(ge=0) = Field(..., description="Processing latency in milliseconds")

