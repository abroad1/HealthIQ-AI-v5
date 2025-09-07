"""
Biomarker models - immutable Pydantic v2 models for biomarker data.
"""

from typing import Dict, List, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class BiomarkerDefinition(BaseModel):
    """Immutable definition of a canonical biomarker."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    name: str = Field(..., description="Canonical biomarker name")
    aliases: List[str] = Field(default_factory=list, description="Alternative names/aliases")
    unit: str = Field(default="", description="Standard unit of measurement")
    description: str = Field(default="", description="Human-readable description")
    category: str = Field(default="", description="Biomarker category")
    data_type: str = Field(default="numeric", description="Data type (numeric, categorical, etc.)")


class BiomarkerValue(BaseModel):
    """Immutable biomarker measurement value."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    name: str = Field(..., description="Canonical biomarker name")
    value: Any = Field(..., description="Measured value")
    unit: str = Field(default="", description="Unit of measurement")
    timestamp: Optional[str] = Field(default=None, description="Measurement timestamp")


class BiomarkerPanel(BaseModel):
    """Immutable collection of biomarker values."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    biomarkers: Dict[str, BiomarkerValue] = Field(
        default_factory=dict, 
        description="Map of canonical biomarker names to values"
    )
    source: str = Field(default="", description="Data source identifier")
    version: str = Field(default="1.0", description="Panel version")
    created_at: Optional[str] = Field(default=None, description="Panel creation timestamp")


class ReferenceRange(BaseModel):
    """Immutable reference range for a biomarker."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    biomarker_name: str = Field(..., description="Canonical biomarker name")
    age_min: Optional[float] = Field(default=None, description="Minimum age for range")
    age_max: Optional[float] = Field(default=None, description="Maximum age for range")
    gender: Optional[str] = Field(default=None, description="Gender-specific range")
    normal_min: Optional[float] = Field(default=None, description="Normal range minimum")
    normal_max: Optional[float] = Field(default=None, description="Normal range maximum")
    unit: str = Field(default="", description="Unit of measurement")
    population: str = Field(default="", description="Population description")


class BiomarkerCluster(BaseModel):
    """Immutable biomarker cluster result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    cluster_id: str = Field(..., description="Unique cluster identifier")
    name: str = Field(..., description="Cluster name")
    biomarkers: List[str] = Field(default_factory=list, description="Biomarkers in cluster")
    description: str = Field(default="", description="Cluster description")
    severity: str = Field(default="normal", description="Severity level")
    confidence: float = Field(default=0.0, description="Confidence score (0-1)")


class BiomarkerInsight(BaseModel):
    """Immutable biomarker insight result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    insight_id: str = Field(..., description="Unique insight identifier")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Detailed insight description")
    biomarkers: List[str] = Field(default_factory=list, description="Related biomarkers")
    category: str = Field(default="", description="Insight category")
    severity: str = Field(default="info", description="Severity level")
    confidence: float = Field(default=0.0, description="Confidence score (0-1)")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")
