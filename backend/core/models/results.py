"""
Analysis results models - immutable Pydantic v2 models for analysis results.
"""

from typing import List, Dict, Any, Optional, TYPE_CHECKING
from pydantic import BaseModel, ConfigDict, Field

from core.models.biomarker import BiomarkerCluster, BiomarkerInsight
from core.models.context import AnalysisContext

if TYPE_CHECKING:
    pass


class BiomarkerScore(BaseModel):
    """Immutable biomarker scoring result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    biomarker_name: str = Field(..., description="Canonical biomarker name")
    value: Any = Field(..., description="Biomarker value")
    unit: str = Field(default="", description="Unit of measurement")
    score: float = Field(..., description="Normalized score (0-1)")
    percentile: Optional[float] = Field(default=None, description="Population percentile")
    status: str = Field(..., description="Status (normal, elevated, low, etc.)")
    reference_range: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Reference range information"
    )
    interpretation: str = Field(default="", description="Clinical interpretation")


class AnalysisResult(BaseModel):
    """Immutable analysis result containing clusters and insights."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    context: AnalysisContext = Field(..., description="Analysis context")
    biomarkers: List[BiomarkerScore] = Field(
        default_factory=list, 
        description="Individual biomarker results with scores and status"
    )
    clusters: List[BiomarkerCluster] = Field(
        default_factory=list, 
        description="Biomarker clusters"
    )
    insights: List[BiomarkerInsight] = Field(
        default_factory=list, 
        description="Generated insights"
    )
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
    risk_assessment: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Risk assessment results"
    )
    recommendations: List[str] = Field(
        default_factory=list, 
        description="General recommendations"
    )
    created_at: str = Field(..., description="Result creation timestamp")
    result_version: str = Field(default="1.0.0", description="Result schema version for DTO parity")
    processing_time_seconds: Optional[float] = Field(
        default=None, 
        description="Total processing time"
    )


class AnalysisSummary(BaseModel):
    """Immutable analysis summary for quick overview."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    user_id: str = Field(..., description="User identifier")
    status: str = Field(..., description="Analysis status")
    total_biomarkers: int = Field(default=0, description="Number of biomarkers analyzed")
    clusters_found: int = Field(default=0, description="Number of clusters identified")
    insights_generated: int = Field(default=0, description="Number of insights generated")
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
    created_at: str = Field(..., description="Analysis creation timestamp")
    completed_at: Optional[str] = Field(default=None, description="Analysis completion timestamp")


class ClusterHit(BaseModel):
    """Immutable cluster hit result."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    cluster_id: str = Field(..., description="Cluster identifier")
    name: str = Field(..., description="Cluster name")
    biomarkers: List[str] = Field(default_factory=list, description="Biomarkers in cluster")
    confidence: float = Field(..., description="Confidence score (0-1)")
    severity: str = Field(..., description="Severity level")
    description: str = Field(default="", description="Cluster description")


class InsightResult(BaseModel):
    """Immutable insight result with provenance tracking."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    # Core insight data
    insight_id: str = Field(..., description="Insight identifier")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    category: str = Field(..., description="Insight category (maintained for frontend compatibility)")
    confidence: float = Field(..., description="Confidence score (0-1)")
    severity: str = Field(..., description="Severity level")
    biomarkers: List[str] = Field(default_factory=list, description="Related biomarkers")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    
    # Provenance fields (Sprint 9c)
    version: str = Field(default="v1.0.0", description="Insight version")
    manifest_id: str = Field(default="legacy_v1", description="Manifest identifier")
    experiment_id: Optional[str] = Field(default=None, description="Experiment identifier")
    drivers: Optional[Dict[str, Any]] = Field(default=None, description="Insight drivers")
    evidence: Optional[Dict[str, Any]] = Field(default=None, description="Supporting evidence")
    error_code: Optional[str] = Field(default=None, description="Error code if failed")
    error_detail: Optional[str] = Field(default=None, description="Error details if failed")
    latency_ms: int = Field(default=0, description="Processing latency in milliseconds")


class AnalysisDTO(BaseModel):
    """Immutable analysis data transfer object."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    biomarkers: List[BiomarkerScore] = Field(default_factory=list, description="Biomarker results")
    clusters: List[ClusterHit] = Field(default_factory=list, description="Cluster hits")
    insights: List[InsightResult] = Field(default_factory=list, description="Insight results")
    status: str = Field(..., description="Analysis status")
    created_at: str = Field(..., description="Creation timestamp")
    overall_score: Optional[float] = Field(default=None, description="Overall health score")
