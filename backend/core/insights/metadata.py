"""
Insight metadata and result models for modular insights engine.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class InsightMetadata:
    """Metadata for insight modules including ID, version, and requirements."""
    
    insight_id: str  # lowercase snake_case, immutable once released
    version: str     # SemVer format (v1.2.0)
    category: str
    required_biomarkers: List[str]
    optional_biomarkers: List[str] = None
    description: str = ""
    author: str = "HealthIQ Team"
    created_at: str = ""
    updated_at: str = ""


@dataclass
class InsightResult:
    """Structured result from insight analysis with full provenance tracking."""
    
    insight_id: str
    version: str
    manifest_id: str
    result_key: Optional[str] = None  # For sub-insights to avoid overwrites
    drivers: Optional[Dict[str, Any]] = None    # Standardized drivers JSONB
    evidence: Optional[Dict[str, Any]] = None   # Standardized evidence JSONB
    biomarkers_involved: Optional[List[str]] = None
    confidence: Optional[float] = None
    severity: Optional[str] = None
    recommendations: Optional[List[str]] = None  # Personalized recommendations
    latency_ms: Optional[float] = None  # Processing time in milliseconds
    error_code: Optional[str] = None
    error_detail: Optional[str] = None
