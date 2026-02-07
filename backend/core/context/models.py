"""
Context Models for Analysis Context Factory

This module defines the Pydantic models used by the ContextFactory for structured
data validation and context creation.
"""

from typing import Dict, Any, Optional, Union, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator, model_validator


class Sex(str, Enum):
    """Sex enumeration for user context."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class BiomarkerContext(BaseModel):
    """Context for a single biomarker value."""
    
    name: str = Field(..., description="Biomarker name")
    value: float = Field(..., description="Biomarker value")
    unit: str = Field(default="unknown", description="Unit of measurement")
    measured_at: Optional[datetime] = Field(default=None, description="When the biomarker was measured")
    reference_range: Optional[Dict[str, Any]] = Field(default=None, description="Reference range data")
    notes: Optional[str] = Field(default=None, description="Additional notes")
    
    @field_validator('value')
    @classmethod
    def validate_value(cls, v):
        """Validate that value is numeric."""
        if not isinstance(v, (int, float)):
            try:
                v = float(v)
            except (ValueError, TypeError):
                raise ValueError(f"Biomarker value must be numeric, got {type(v)}")
        return v
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate biomarker name is not empty."""
        if not v or not v.strip():
            raise ValueError("Biomarker name cannot be empty")
        return v.strip().lower()


class BiomarkerPanel(BaseModel):
    """Panel containing multiple biomarkers with metadata."""
    
    name: str = Field(..., description="Panel name")
    biomarkers: Dict[str, BiomarkerContext] = Field(..., description="Biomarkers in this panel")
    collected_at: datetime = Field(..., description="When the panel was collected")
    laboratory: Optional[str] = Field(default=None, description="Laboratory that processed the panel")
    panel_type: str = Field(default="custom", description="Type of panel")
    notes: Optional[str] = Field(default=None, description="Additional panel notes")
    
    @field_validator('biomarkers')
    @classmethod
    def validate_biomarkers(cls, v):
        """Validate biomarkers dictionary is not empty."""
        if not v:
            raise ValueError("Panel must contain at least one biomarker")
        return v


class ScoringMetrics(BaseModel):
    """Scoring metrics for analysis results."""
    
    raw_scores: Dict[str, float] = Field(default_factory=dict, description="Raw scoring values")
    weighted_scores: Dict[str, float] = Field(default_factory=dict, description="Weighted scoring values")
    cluster_scores: Dict[str, float] = Field(default_factory=dict, description="Cluster scoring values")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    computed_at: datetime = Field(default_factory=datetime.now, description="When metrics were computed")


class UserContext(BaseModel):
    """Context for user demographic and lifestyle data."""
    
    user_id: str = Field(..., description="Unique user identifier")
    sex: Sex = Field(..., description="User's sex")
    chronological_age: int = Field(..., ge=0, le=150, description="User's age in years")
    height_cm: float = Field(..., ge=0, le=300, description="Height in centimeters")
    weight_kg: float = Field(..., ge=0, le=1000, description="Weight in kilograms")
    waist_cm: Optional[float] = Field(default=None, ge=0, le=300, description="Waist circumference in centimeters")
    stress_level: int = Field(default=5, ge=1, le=10, description="Stress level (1-10 scale)")
    sleep_hours: float = Field(default=8.0, ge=0, le=24, description="Average sleep hours per night")
    physical_activity_minutes: int = Field(default=0, ge=0, le=1440, description="Physical activity minutes per day")
    fluid_intake_frequency: str = Field(default="moderate", description="Fluid intake frequency")
    alcohol_units_per_week: int = Field(default=0, ge=0, le=100, description="Alcohol units per week")
    exercise_days_per_week: int = Field(default=0, ge=0, le=7, description="Exercise days per week")
    smoking_status: str = Field(default="never", description="Smoking status")
    medical_conditions: List[str] = Field(default_factory=list, description="List of medical conditions")
    medications: List[str] = Field(default_factory=list, description="List of medications")
    family_history: Dict[str, Any] = Field(default_factory=dict, description="Family medical history")
    created_at: Optional[datetime] = Field(default=None, description="When the user context was created")
    updated_at: Optional[datetime] = Field(default=None, description="When the user context was last updated")
    
    
    @field_validator('sex')
    @classmethod
    def validate_sex(cls, v):
        """Validate sex field."""
        if isinstance(v, str):
            v = v.lower().strip()
            if v not in [e.value for e in Sex]:
                raise ValueError(f"Invalid sex value: {v}. Must be one of: {[e.value for e in Sex]}")
            return Sex(v)
        return v


class AnalysisContext(BaseModel):
    """Main analysis context containing all validated data."""
    
    # Support both old and new structure for backward compatibility
    biomarkers: Optional[Dict[str, BiomarkerContext]] = Field(default=None, description="Validated biomarker data (legacy)")
    biomarker_panel: Optional[BiomarkerPanel] = Field(default=None, description="Biomarker panel with metadata")
    user: UserContext = Field(..., description="Validated user context")
    questionnaire: Optional[Dict[str, Any]] = Field(default=None, description="Optional questionnaire data")
    scoring_metrics: Optional[ScoringMetrics] = Field(default=None, description="Scoring metrics for analysis")
    analysis_id: Optional[str] = Field(default=None, description="Analysis identifier")
    created_at: Optional[datetime] = Field(default=None, description="When the analysis context was created")
    
    @field_validator('biomarkers')
    @classmethod
    def validate_biomarkers(cls, v):
        """Validate biomarkers dictionary is not empty if provided."""
        if v is not None and not v:
            raise ValueError("Analysis context biomarkers must contain at least one biomarker")
        return v
    
    @field_validator('biomarker_panel')
    @classmethod
    def validate_biomarker_panel(cls, v):
        """Validate biomarker panel if provided."""
        if v is not None and not v.biomarkers:
            raise ValueError("Biomarker panel must contain at least one biomarker")
        return v
    
    @model_validator(mode='after')
    def set_defaults(self):
        """Set default values for analysis_id and created_at if not provided."""
        if self.analysis_id is None:
            import uuid
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            self.analysis_id = f"analysis_{timestamp}_{unique_id}"
        
        if self.created_at is None:
            self.created_at = datetime.now()
        
        return self
    
    def validate_analysis_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate analysis context against specific requirements.
        
        Args:
            requirements: Dictionary of requirements to validate against
            
        Returns:
            Dictionary with validation results
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Get biomarker data from either structure
        biomarker_data = {}
        if self.biomarker_panel:
            biomarker_data = self.biomarker_panel.biomarkers
        elif self.biomarkers:
            biomarker_data = self.biomarkers
        
        # Check minimum biomarker count
        min_biomarkers = requirements.get('min_biomarkers', 1)
        if len(biomarker_data) < min_biomarkers:
            result['valid'] = False
            result['errors'].append(f"Analysis requires at least {min_biomarkers} biomarkers, got {len(biomarker_data)}")
        
        # Check required biomarkers
        required_biomarkers = requirements.get('required_biomarkers', [])
        missing_biomarkers = []
        for biomarker in required_biomarkers:
            if biomarker.lower() not in biomarker_data:
                missing_biomarkers.append(biomarker)
        
        if missing_biomarkers:
            result['valid'] = False
            result['errors'].append(f"Missing required biomarkers: {', '.join(missing_biomarkers)}")
        
        # Check user age requirements
        min_age = requirements.get('min_age', 0)
        max_age = requirements.get('max_age', 150)
        if not (min_age <= self.user.chronological_age <= max_age):
            result['warnings'].append(f"User age {self.user.chronological_age} outside recommended range {min_age}-{max_age}")
        
        return result
