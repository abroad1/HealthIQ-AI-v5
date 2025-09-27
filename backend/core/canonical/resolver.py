"""
Canonical biomarker resolver - loads from Single Source of Truth (SSOT).
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from functools import lru_cache
from decimal import Decimal, ROUND_HALF_UP

from core.models.biomarker import BiomarkerDefinition, ReferenceRange


class CanonicalResolver:
    """Resolves canonical biomarker definitions from SSOT."""
    
    def __init__(self, ssot_path: Optional[Path] = None):
        """
        Initialize the resolver with SSOT path.
        
        Args:
            ssot_path: Path to SSOT directory, defaults to backend/ssot/
        """
        if ssot_path is None:
            ssot_path = Path(__file__).parent.parent.parent / "ssot"
        
        self.ssot_path = ssot_path
        self._biomarkers_cache: Optional[Dict[str, BiomarkerDefinition]] = None
        self._ranges_cache: Optional[Dict[str, Any]] = None
        self._units_cache: Optional[Dict[str, Any]] = None
    
    def load_biomarkers(self) -> Dict[str, BiomarkerDefinition]:
        """
        Load canonical biomarker definitions from SSOT.
        
        Returns:
            Dict mapping canonical biomarker names to definitions
        """
        if self._biomarkers_cache is not None:
            return self._biomarkers_cache
        
        biomarkers_file = self.ssot_path / "biomarkers.yaml"
        if not biomarkers_file.exists():
            raise FileNotFoundError(f"Biomarkers SSOT file not found: {biomarkers_file}")
        
        with open(biomarkers_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        biomarkers = {}
        for name, definition in data.get("biomarkers", {}).items():
            biomarkers[name] = BiomarkerDefinition(
                name=name,
                aliases=definition.get("aliases", []),
                unit=definition.get("unit", ""),
                description=definition.get("description", ""),
                category=definition.get("category", ""),
                data_type=definition.get("data_type", "numeric")
            )
        
        self._biomarkers_cache = biomarkers
        return biomarkers
    
    def load_ranges(self) -> Dict[str, Any]:
        """
        Load reference ranges from SSOT.
        
        Returns:
            Dict mapping biomarker names to reference ranges
        """
        if self._ranges_cache is not None:
            return self._ranges_cache
        
        ranges_file = self.ssot_path / "ranges.yaml"
        if not ranges_file.exists():
            raise FileNotFoundError(f"Ranges SSOT file not found: {ranges_file}")
        
        with open(ranges_file, 'r', encoding='utf-8') as f:
            self._ranges_cache = yaml.safe_load(f)
        
        return self._ranges_cache
    
    def load_units(self) -> Dict[str, Any]:
        """
        Load unit definitions from SSOT.
        
        Returns:
            Dict mapping unit names to definitions
        """
        if self._units_cache is not None:
            return self._units_cache
        
        units_file = self.ssot_path / "units.yaml"
        if not units_file.exists():
            raise FileNotFoundError(f"Units SSOT file not found: {units_file}")
        
        with open(units_file, 'r', encoding='utf-8') as f:
            self._units_cache = yaml.safe_load(f)
        
        return self._units_cache
    
    def get_biomarker_definition(self, name: str) -> Optional[BiomarkerDefinition]:
        """
        Get a specific biomarker definition by canonical name.
        
        Args:
            name: Canonical biomarker name
            
        Returns:
            BiomarkerDefinition or None if not found
        """
        biomarkers = self.load_biomarkers()
        return biomarkers.get(name)
    
    def clear_cache(self):
        """Clear all cached data."""
        self._biomarkers_cache = None
        self._ranges_cache = None
        self._units_cache = None
    
    def convert_unit(self, value: float, from_unit: str, to_unit: str, biomarker_name: str = None) -> float:
        """
        Convert a value from one unit to another with 4 decimal place precision.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            biomarker_name: Optional biomarker name for specific conversion rules
            
        Returns:
            Converted value with 4 decimal place precision
            
        Raises:
            ValueError: If conversion is not supported
        """
        if from_unit == to_unit:
            return round(float(value), 4)
        
        # Load unit definitions
        units = self.load_units()
        conversions = units.get("units", {}).get("conversions", {})
        
        # Handle biomarker-specific conversions first
        if from_unit == "mg/dL" and to_unit == "mmol/L" and biomarker_name:
            if "glucose" in biomarker_name.lower():
                # Use glucose-specific conversion
                glucose_key = "mg_dL_to_mmol_L_glucose"
                if glucose_key in conversions:
                    factor = conversions[glucose_key]["factor"]
                    converted_value = float(value) * factor
                else:
                    raise ValueError(f"Glucose-specific unit conversion not supported")
            else:
                # Use cholesterol conversion as default for mg/dL to mmol/L
                cholesterol_key = "mg_dL_to_mmol_L"
                if cholesterol_key in conversions:
                    factor = conversions[cholesterol_key]["factor"]
                    converted_value = float(value) * factor
                else:
                    raise ValueError(f"Cholesterol unit conversion not supported")
        elif from_unit == "mmol/L" and to_unit == "mg/dL" and biomarker_name:
            if "glucose" in biomarker_name.lower():
                # Use glucose-specific reverse conversion
                glucose_key = "mg_dL_to_mmol_L_glucose"
                if glucose_key in conversions:
                    factor = conversions[glucose_key]["factor"]
                    converted_value = float(value) / factor  # Reverse the conversion
                else:
                    raise ValueError(f"Glucose-specific unit conversion not supported")
            else:
                # Use cholesterol conversion as default for mmol/L to mg/dL
                cholesterol_key = "mg_dL_to_mmol_L"
                if cholesterol_key in conversions:
                    factor = conversions[cholesterol_key]["factor"]
                    converted_value = float(value) / factor  # Reverse the conversion
                else:
                    raise ValueError(f"Cholesterol unit conversion not supported")
        else:
            # Find conversion factor - handle both formats
            conversion_key = f"{from_unit}_to_{to_unit}".replace("/", "_").replace("%", "percent")
            if conversion_key not in conversions:
                # Try reverse conversion
                reverse_key = f"{to_unit}_to_{from_unit}".replace("/", "_").replace("%", "percent")
                if reverse_key in conversions:
                    factor = conversions[reverse_key]["factor"]
                    # Reverse the factor (1/factor)
                    converted_value = float(value) / factor
                else:
                    # Try alternative naming patterns
                    alt_key = f"{from_unit}_to_{to_unit}".replace("/", "_").replace("mmol/L", "mmol_L")
                    if alt_key in conversions:
                        factor = conversions[alt_key]["factor"]
                        converted_value = float(value) * factor
                    else:
                        raise ValueError(f"Unit conversion from {from_unit} to {to_unit} not supported")
            else:
                factor = conversions[conversion_key]["factor"]
                converted_value = float(value) * factor
        
        # Round to 4 decimal places using Decimal for precision
        decimal_value = Decimal(str(converted_value))
        rounded_value = decimal_value.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        return float(rounded_value)
    
    def get_reference_range(
        self, 
        biomarker_name: str, 
        age: Optional[int] = None, 
        gender: Optional[str] = None,
        population: str = "general_adult"
    ) -> Optional[ReferenceRange]:
        """
        Get reference range for a biomarker based on age, gender, and population.
        
        Args:
            biomarker_name: Canonical biomarker name
            age: Patient age in years
            gender: Patient gender ("male", "female", or None)
            population: Population group (e.g., "general_adult", "fasting_adult")
            
        Returns:
            ReferenceRange object or None if not found
        """
        ranges = self.load_ranges()
        biomarker_ranges = ranges.get("reference_ranges", {}).get(biomarker_name)
        
        if not biomarker_ranges:
            return None
        
        # Find the most specific range based on population and demographics
        best_match = None
        best_score = -1
        
        for range_name, range_data in biomarker_ranges.items():
            range_population = range_data.get("population", "general_adult")
            
            # Score based on population match
            score = 0
            if range_population == population:
                score += 10
            elif "adult" in range_population and "adult" in population:
                score += 5
            
            # Score based on gender match
            if gender:
                if gender.lower() in range_population:
                    score += 5
                elif "general" in range_population:
                    score += 2
            
            # Score based on age match (if available)
            if age is not None:
                # Add age-specific scoring logic here if needed
                pass
            
            if score > best_score:
                best_score = score
                best_match = range_data
        
        if not best_match:
            return None
        
        # Create ReferenceRange object
        return ReferenceRange(
            biomarker_name=biomarker_name,
            age_min=None,  # Could be enhanced with age ranges
            age_max=None,
            gender=gender,
            normal_min=best_match.get("min"),
            normal_max=best_match.get("max"),
            unit=best_match.get("unit", ""),
            population=best_match.get("population", population)
        )
    
    def get_all_reference_ranges(self, biomarker_name: str) -> list[ReferenceRange]:
        """
        Get all available reference ranges for a biomarker.
        
        Args:
            biomarker_name: Canonical biomarker name
            
        Returns:
            List of ReferenceRange objects
        """
        ranges = self.load_ranges()
        biomarker_ranges = ranges.get("reference_ranges", {}).get(biomarker_name, {})
        
        reference_ranges = []
        for range_name, range_data in biomarker_ranges.items():
            reference_ranges.append(ReferenceRange(
                biomarker_name=biomarker_name,
                age_min=None,
                age_max=None,
                gender=None,
                normal_min=range_data.get("min"),
                normal_max=range_data.get("max"),
                unit=range_data.get("unit", ""),
                population=range_data.get("population", "general_adult")
            ))
        
        return reference_ranges
    
    def validate_biomarker_value(
        self, 
        biomarker_name: str, 
        value: float, 
        unit: str,
        age: Optional[int] = None,
        gender: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate a biomarker value against reference ranges.
        
        Args:
            biomarker_name: Canonical biomarker name
            value: Measured value
            unit: Unit of measurement
            age: Patient age
            gender: Patient gender
            
        Returns:
            Dictionary with validation results including status, range info, etc.
        """
        # Get reference range
        reference_range = self.get_reference_range(biomarker_name, age, gender)
        
        if not reference_range:
            return {
                "status": "unknown",
                "message": "No reference range available",
                "value": value,
                "unit": unit,
                "reference_range": None
            }
        
        # Convert value to reference range unit if needed
        if unit != reference_range.unit:
            try:
                converted_value = self.convert_unit(value, unit, reference_range.unit)
            except ValueError:
                return {
                    "status": "conversion_error",
                    "message": f"Cannot convert {unit} to {reference_range.unit}",
                    "value": value,
                    "unit": unit,
                    "reference_range": reference_range
                }
        else:
            converted_value = value
        
        # Determine status based on range
        min_val = reference_range.normal_min
        max_val = reference_range.normal_max
        
        if min_val is None and max_val is None:
            status = "unknown"
            message = "No normal range defined"
        elif min_val is None:
            if converted_value <= max_val:
                status = "normal"
                message = "Within normal range"
            else:
                status = "high"
                message = "Above normal range"
        elif max_val is None:
            if converted_value >= min_val:
                status = "normal"
                message = "Within normal range"
            else:
                status = "low"
                message = "Below normal range"
        else:
            if min_val <= converted_value <= max_val:
                status = "normal"
                message = "Within normal range"
            elif converted_value < min_val:
                status = "low"
                message = "Below normal range"
            else:
                status = "high"
                message = "Above normal range"
        
        return {
            "status": status,
            "message": message,
            "value": converted_value,
            "unit": reference_range.unit,
            "reference_range": reference_range,
            "original_value": value,
            "original_unit": unit
        }


_ALIAS_OVERRIDES = {
    "cholesterol": "total_cholesterol",
    "blood_sugar": "glucose",
}

@lru_cache(maxsize=2048)
def resolve_to_canonical(name: str) -> str:
    """
    Resolve a biomarker name to its canonical form.
    
    Args:
        name: Biomarker name (canonical or alias)
        
    Returns:
        Canonical biomarker name, or input unchanged if already canonical or unknown
    """
    key = (name or "").strip()
    if not key:
        return ""
    lower = key.lower()

    # 1) Try SSOT lookup (existing logic)
    resolver = CanonicalResolver()
    biomarkers = resolver.load_biomarkers()
    
    # Check if it's already canonical
    if key in biomarkers:
        return key
    
    # Check if it's an alias
    for canonical_name, definition in biomarkers.items():
        if lower in [alias.lower() for alias in definition.aliases]:
            return canonical_name

    # 2) Fallback overrides (for tests/common aliases)
    if lower in _ALIAS_OVERRIDES:
        return _ALIAS_OVERRIDES[lower]

    # 3) Otherwise, return original unchanged
    return key
