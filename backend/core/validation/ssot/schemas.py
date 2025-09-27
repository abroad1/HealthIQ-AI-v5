"""
Pydantic schemas for SSOT YAML validation.

This module defines the data models for validating SSOT YAML files
including biomarkers, reference ranges, and unit definitions.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator


class BiomarkerDefinition(BaseModel):
    """Schema for individual biomarker definitions."""
    
    aliases: List[str] = Field(..., min_length=1, description="List of biomarker aliases")
    unit: str = Field(..., min_length=1, description="Primary unit for the biomarker")
    description: str = Field(..., min_length=1, description="Human-readable description")
    category: str = Field(..., min_length=1, description="Biomarker category")
    data_type: str = Field(..., description="Data type for the biomarker")
    
    @field_validator('data_type')
    @classmethod
    def validate_data_type(cls, v):
        """Validate data type is one of the allowed values."""
        allowed_types = ['numeric', 'categorical', 'boolean']
        if v not in allowed_types:
            raise ValueError(f"data_type must be one of {allowed_types}")
        return v
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """Validate category is one of the allowed values."""
        allowed_categories = [
            'cardiovascular', 'metabolic', 'kidney', 'liver', 
            'inflammatory', 'cbc', 'hormone', 'vitamin', 'other'
        ]
        if v not in allowed_categories:
            raise ValueError(f"category must be one of {allowed_categories}")
        return v
    
    @field_validator('aliases')
    @classmethod
    def validate_aliases(cls, v):
        """Validate aliases are unique and non-empty."""
        if not v:
            raise ValueError("aliases cannot be empty")
        if len(set(v)) != len(v):
            raise ValueError("aliases must be unique")
        return v


class ReferenceRange(BaseModel):
    """Schema for individual reference range definitions."""
    
    min: float = Field(..., description="Minimum value for the range")
    max: float = Field(..., description="Maximum value for the range")
    unit: str = Field(..., min_length=1, description="Unit for the range")
    population: str = Field(..., min_length=1, description="Target population")
    
    @field_validator('max')
    @classmethod
    def validate_max_greater_than_min(cls, v, info):
        """Validate max is greater than min."""
        if info.data and 'min' in info.data and v <= info.data['min']:
            raise ValueError("max must be greater than min")
        return v
    
    @field_validator('population')
    @classmethod
    def validate_population(cls, v):
        """Validate population is one of the allowed values."""
        allowed_populations = [
            'general_adult', 'male_adult', 'female_adult', 'pediatric',
            'geriatric', 'fasting_adult', 'pregnant', 'athlete'
        ]
        if v not in allowed_populations:
            raise ValueError(f"population must be one of {allowed_populations}")
        return v


class UnitDefinition(BaseModel):
    """Schema for individual unit definitions."""
    
    name: str = Field(..., min_length=1, description="Display name of the unit")
    description: str = Field(..., min_length=1, description="Human-readable description")
    category: str = Field(..., min_length=1, description="Unit category")
    si_equivalent: str = Field(..., min_length=1, description="SI equivalent unit")
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """Validate category is one of the allowed values."""
        allowed_categories = [
            'concentration', 'ratio', 'enzyme_activity', 'count',
            'pressure', 'temperature', 'time', 'volume', 'mass'
        ]
        if v not in allowed_categories:
            raise ValueError(f"category must be one of {allowed_categories}")
        return v


class ConversionFactor(BaseModel):
    """Schema for unit conversion factors."""
    
    from_unit: str = Field(..., min_length=1, description="Source unit")
    to_unit: str = Field(..., min_length=1, description="Target unit")
    factor: float = Field(..., description="Conversion factor")
    description: str = Field(..., min_length=1, description="Conversion description")
    
    @field_validator('factor')
    @classmethod
    def validate_factor_non_zero(cls, v):
        """Validate conversion factor is not zero."""
        if v == 0:
            raise ValueError("conversion factor cannot be zero")
        return v


class BiomarkersSchema(BaseModel):
    """Schema for the complete biomarkers YAML file."""
    
    biomarkers: Dict[str, BiomarkerDefinition] = Field(..., min_length=1, description="Biomarker definitions")
    
    @field_validator('biomarkers')
    @classmethod
    def validate_biomarker_keys(cls, v):
        """Validate biomarker keys are valid identifiers."""
        for key in v.keys():
            if not key.replace('_', '').isalnum():
                raise ValueError(f"biomarker key '{key}' must be alphanumeric with underscores")
        return v


class RangesSchema(BaseModel):
    """Schema for the complete reference ranges YAML file."""
    
    reference_ranges: Dict[str, Dict[str, ReferenceRange]] = Field(..., min_length=1, description="Reference ranges by biomarker")
    
    @field_validator('reference_ranges')
    @classmethod
    def validate_range_structure(cls, v):
        """Validate reference ranges structure."""
        for biomarker, ranges in v.items():
            if not ranges:
                raise ValueError(f"biomarker '{biomarker}' must have at least one reference range")
            for range_name, range_def in ranges.items():
                if not range_name.replace('_', '').isalnum():
                    raise ValueError(f"range name '{range_name}' must be alphanumeric with underscores")
        return v


class UnitCategory(BaseModel):
    """Schema for unit category definitions."""
    
    description: str = Field(..., min_length=1, description="Category description")
    units: List[str] = Field(..., min_length=1, description="Units in this category")


class UnitsSchema(BaseModel):
    """Schema for the complete units YAML file."""
    
    model_config = {"extra": "ignore"}
    
    units: Dict[str, Any] = Field(..., min_length=1, description="Unit definitions and metadata")
    
    @field_validator('units')
    @classmethod
    def validate_units_structure(cls, v):
        """Validate units structure and separate unit definitions from metadata."""
        unit_definitions = {}
        for key, value in v.items():
            if key in ['conversions', 'categories']:
                # Skip metadata keys
                continue
            if isinstance(value, dict) and all(field in value for field in ['name', 'description', 'category', 'si_equivalent']):
                # This is a unit definition
                unit_definitions[key] = UnitDefinition(**value)
            else:
                raise ValueError(f"Invalid unit definition for '{key}': missing required fields")
        
        if not unit_definitions:
            raise ValueError("No valid unit definitions found")
        
        return unit_definitions
