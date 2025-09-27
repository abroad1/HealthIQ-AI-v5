"""
Pydantic schemas for SSOT YAML validation
HealthIQ-AI v5 Backend
"""

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator
import re
import logging

logger = logging.getLogger(__name__)


class BiomarkerDefinition(BaseModel):
    """Schema for individual biomarker definitions in biomarkers.yaml"""
    
    aliases: List[str] = Field(..., min_length=1, description="List of biomarker aliases")
    unit: str = Field(..., min_length=1, description="Primary unit for this biomarker")
    description: str = Field(..., min_length=1, description="Human-readable description")
    category: str = Field(..., min_length=1, description="Biomarker category")
    data_type: str = Field(..., pattern="^(numeric|categorical|boolean)$", description="Data type")
    
    @field_validator('aliases')
    @classmethod
    def validate_aliases(cls, v):
        """Ensure aliases are non-empty strings"""
        if not v:
            raise ValueError("At least one alias is required")
        for alias in v:
            if not alias or not alias.strip():
                raise ValueError("Aliases cannot be empty or whitespace")
        return v
    
    @field_validator('unit')
    @classmethod
    def validate_unit(cls, v):
        """Validate unit format"""
        if not v or not v.strip():
            raise ValueError("Unit cannot be empty")
        return v.strip()
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """Validate category is from allowed list"""
        allowed_categories = [
            "cardiovascular", "metabolic", "inflammatory", "hormonal", 
            "liver", "kidney", "thyroid", "vitamin", "mineral", "cbc", "other"
        ]
        if v not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return v


class ReferenceRange(BaseModel):
    """Schema for individual reference range definitions in ranges.yaml"""
    
    min: float = Field(..., description="Minimum value for this range")
    max: float = Field(..., description="Maximum value for this range")
    unit: str = Field(..., min_length=1, description="Unit for this range")
    population: str = Field(..., min_length=1, description="Target population")
    
    @field_validator('min', 'max')
    @classmethod
    def validate_range_values(cls, v):
        """Ensure min/max are valid numbers"""
        if not isinstance(v, (int, float)):
            raise ValueError("Range values must be numeric")
        return float(v)
    
    @field_validator('max')
    @classmethod
    def validate_max_greater_than_min(cls, v, info):
        """Ensure max is greater than min"""
        if hasattr(info, 'data') and 'min' in info.data and v <= info.data['min']:
            raise ValueError("Max value must be greater than min value")
        return v
    
    @field_validator('population')
    @classmethod
    def validate_population(cls, v):
        """Validate population is from allowed list"""
        allowed_populations = [
            "general_adult", "pediatric", "elderly", "pregnant", 
            "diabetic", "hypertensive", "athletic", "male_adult", 
            "female_adult", "fasting_adult", "other"
        ]
        if v not in allowed_populations:
            raise ValueError(f"Population must be one of: {', '.join(allowed_populations)}")
        return v


class UnitDefinition(BaseModel):
    """Schema for individual unit definitions in units.yaml"""
    
    name: str = Field(..., min_length=1, description="Display name of the unit")
    description: str = Field(..., min_length=1, description="Human-readable description")
    category: str = Field(..., min_length=1, description="Unit category")
    si_equivalent: str = Field(..., min_length=1, description="SI equivalent unit")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        """Validate unit name format"""
        if not v or not v.strip():
            raise ValueError("Unit name cannot be empty")
        return v.strip()
    
    @field_validator('category')
    @classmethod
    def validate_category(cls, v):
        """Validate unit category is from allowed list"""
        allowed_categories = [
            "concentration", "ratio", "enzyme_activity", "count", 
            "volume", "mass", "length", "time", "temperature", "other"
        ]
        if v not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return v


class BiomarkersSchema(BaseModel):
    """Schema for the entire biomarkers.yaml file"""
    
    biomarkers: Dict[str, BiomarkerDefinition] = Field(..., description="Biomarker definitions")
    
    @field_validator('biomarkers')
    @classmethod
    def validate_biomarkers(cls, v):
        """Validate biomarker definitions"""
        if not v:
            raise ValueError("At least one biomarker definition is required")
        
        # Check for duplicate aliases across biomarkers
        all_aliases = []
        for biomarker_id, definition in v.items():
            for alias in definition.aliases:
                if alias in all_aliases:
                    raise ValueError(f"Duplicate alias '{alias}' found across biomarkers")
                all_aliases.append(alias)
        
        return v


class ReferenceRangesSchema(BaseModel):
    """Schema for the entire ranges.yaml file"""
    
    reference_ranges: Dict[str, Dict[str, ReferenceRange]] = Field(..., description="Reference ranges by biomarker")
    
    @field_validator('reference_ranges')
    @classmethod
    def validate_reference_ranges(cls, v):
        """Validate reference range definitions"""
        if not v:
            raise ValueError("At least one reference range definition is required")
        
        for biomarker_id, ranges in v.items():
            if not ranges:
                raise ValueError(f"No reference ranges defined for biomarker '{biomarker_id}'")
            
            # Check for overlapping ranges (only warn, don't fail validation)
            range_list = list(ranges.values())
            for i, range1 in enumerate(range_list):
                for j, range2 in enumerate(range_list[i+1:], i+1):
                    if (range1.min < range2.max and range1.max > range2.min):
                        # Only warn about overlapping ranges, don't fail validation
                        # This allows for gender-specific ranges that may overlap
                        logger.warning(f"Overlapping ranges found for biomarker '{biomarker_id}': "
                                     f"{range1.min}-{range1.max} and {range2.min}-{range2.max}")
        
        return v


class ConversionFactor(BaseModel):
    """Schema for unit conversion factors"""
    from_unit: str = Field(..., description="Source unit")
    to_unit: str = Field(..., description="Target unit")
    factor: float = Field(..., description="Conversion factor")
    description: str = Field(..., description="Conversion description")


class UnitCategory(BaseModel):
    """Schema for unit categories"""
    description: str = Field(..., description="Category description")
    units: List[str] = Field(..., description="Units in this category")


class UnitsSchema(BaseModel):
    """Schema for the entire units.yaml file"""
    
    units: Dict[str, UnitDefinition] = Field(..., description="Unit definitions")
    conversions: Optional[Dict[str, ConversionFactor]] = Field(default=None, description="Unit conversion factors")
    categories: Optional[Dict[str, UnitCategory]] = Field(default=None, description="Unit categories")
    
    @field_validator('units')
    @classmethod
    def validate_units(cls, v):
        """Validate unit definitions"""
        if not v:
            raise ValueError("At least one unit definition is required")
        
        # Check for duplicate unit names
        unit_names = []
        for unit_id, definition in v.items():
            if definition.name in unit_names:
                raise ValueError(f"Duplicate unit name '{definition.name}' found")
            unit_names.append(definition.name)
        
        return v
