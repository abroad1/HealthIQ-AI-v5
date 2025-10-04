"""
Analysis context models - immutable Pydantic v2 models for analysis context.
"""

from typing import Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field

from core.models.biomarker import BiomarkerPanel
from core.models.user import User


class AnalysisContext(BaseModel):
    """Immutable analysis context containing all data needed for analysis."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Unique analysis identifier")
    user: User = Field(..., description="User information")
    biomarker_panel: BiomarkerPanel = Field(..., description="Normalized biomarker data")
    questionnaire_responses: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Questionnaire responses from the 58-question form"
    )
    lifestyle_factors: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Mapped lifestyle factors from questionnaire responses"
    )
    medical_history: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Mapped medical history from questionnaire responses"
    )
    analysis_parameters: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Analysis configuration parameters"
    )
    created_at: str = Field(..., description="Analysis creation timestamp")
    version: str = Field(default="1.0", description="Analysis context version")


class AnalysisPhase(BaseModel):
    """Immutable analysis phase information."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    phase: str = Field(..., description="Phase name")
    status: str = Field(..., description="Phase status (pending, running, complete, error)")
    progress: float = Field(default=0.0, description="Progress percentage (0-100)")
    message: Optional[str] = Field(default=None, description="Phase status message")
    started_at: Optional[str] = Field(default=None, description="Phase start timestamp")
    completed_at: Optional[str] = Field(default=None, description="Phase completion timestamp")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")


class AnalysisEvent(BaseModel):
    """Immutable analysis event for SSE streaming."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    analysis_id: str = Field(..., description="Analysis identifier")
    phase: str = Field(..., description="Current phase")
    progress: float = Field(default=0.0, description="Overall progress (0-100)")
    status: str = Field(..., description="Current status")
    message: Optional[str] = Field(default=None, description="Status message")
    updated_at: str = Field(..., description="Event timestamp")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional event data")
