"""
User models - immutable Pydantic v2 models for user data.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    """Immutable user model."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    user_id: str = Field(..., description="Unique user identifier")
    email: Optional[str] = Field(default=None, description="User email address")
    age: Optional[int] = Field(default=None, description="User age in years")
    gender: Optional[str] = Field(default=None, description="User gender")
    height: Optional[float] = Field(default=None, description="Height in cm")
    weight: Optional[float] = Field(default=None, description="Weight in kg")
    ethnicity: Optional[str] = Field(default=None, description="User ethnicity")
    medical_history: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Medical history and conditions"
    )
    medications: list[str] = Field(
        default_factory=list, 
        description="Current medications"
    )
    lifestyle_factors: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Lifestyle factors (smoking, exercise, etc.)"
    )
    created_at: Optional[str] = Field(default=None, description="User creation timestamp")
    updated_at: Optional[str] = Field(default=None, description="Last update timestamp")


class UserContext(BaseModel):
    """Immutable user context for analysis."""
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    user: User = Field(..., description="User information")
    analysis_preferences: Dict[str, Any] = Field(
        default_factory=dict, 
        description="User analysis preferences"
    )
    risk_factors: list[str] = Field(
        default_factory=list, 
        description="Identified risk factors"
    )
    health_goals: list[str] = Field(
        default_factory=list, 
        description="User health goals"
    )
