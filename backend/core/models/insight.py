"""
Insight models - immutable Pydantic v2 models for synthesized insights.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class Insight(BaseModel):
    """Immutable synthesized insight result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    id: str = Field(..., description="Unique insight identifier")
    category: str = Field(..., description="Insight category (e.g., metabolic, cardiovascular)")
    summary: str = Field(..., description="Brief insight summary")
    evidence: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Supporting evidence and data"
    )
    confidence: float = Field(
        default=0.0, 
        ge=0.0, 
        le=1.0, 
        description="Confidence score (0-1)"
    )
    severity: str = Field(
        default="info", 
        description="Severity level (info, warning, critical)"
    )
    recommendations: List[str] = Field(
        default_factory=list, 
        description="Actionable recommendations"
    )
    biomarkers_involved: List[str] = Field(
        default_factory=list, 
        description="Biomarkers that contributed to this insight"
    )
    lifestyle_factors: List[str] = Field(
        default_factory=list, 
        description="Lifestyle factors that influenced this insight"
    )
    tokens_used: int = Field(
        default=0, 
        ge=0, 
        description="Number of tokens used to generate this insight"
    )
    latency_ms: int = Field(
        default=0, 
        ge=0, 
        description="Latency in milliseconds for insight generation"
    )
    created_at: str = Field(..., description="Insight creation timestamp")


class InsightSynthesisResult(BaseModel):
    """Immutable result of insight synthesis process."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    insights: List[Insight] = Field(
        default_factory=list, 
        description="Generated insights"
    )
    synthesis_summary: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Synthesis process summary"
    )
    total_insights: int = Field(default=0, description="Total number of insights generated")
    categories_covered: List[str] = Field(
        default_factory=list, 
        description="Health categories covered by insights"
    )
    overall_confidence: float = Field(
        default=0.0, 
        ge=0.0, 
        le=1.0, 
        description="Overall confidence in synthesis"
    )
    processing_time_ms: int = Field(default=0, description="Processing time in milliseconds")
    created_at: str = Field(..., description="Synthesis completion timestamp")


class InsightTemplate(BaseModel):
    """Immutable insight generation template."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    template_id: str = Field(..., description="Unique template identifier")
    name: str = Field(..., description="Template name")
    category: str = Field(..., description="Health category this template covers")
    prompt_template: str = Field(..., description="Prompt template for LLM")
    required_biomarkers: List[str] = Field(
        default_factory=list, 
        description="Required biomarkers for this template"
    )
    required_lifestyle_factors: List[str] = Field(
        default_factory=list, 
        description="Required lifestyle factors for this template"
    )
    output_format: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Expected output format specification"
    )
    version: str = Field(default="1.0", description="Template version")
    is_active: bool = Field(default=True, description="Whether template is active")


class InsightGenerationRequest(BaseModel):
    """Immutable request for insight generation."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    context_data: Dict[str, Any] = Field(..., description="Analysis context data")
    biomarker_scores: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Biomarker scoring results"
    )
    clustering_results: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Clustering analysis results"
    )
    lifestyle_profile: Dict[str, Any] = Field(
        default_factory=dict, 
        description="User lifestyle profile"
    )
    questionnaire_responses: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Questionnaire responses"
    )
    requested_categories: List[str] = Field(
        default_factory=list, 
        description="Specific categories to generate insights for"
    )
    max_insights_per_category: int = Field(
        default=3, 
        ge=1, 
        le=10, 
        description="Maximum insights per category"
    )
