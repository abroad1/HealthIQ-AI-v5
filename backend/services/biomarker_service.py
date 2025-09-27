"""
Biomarker service - handles biomarker-specific operations.
"""

from typing import Dict, Any, Optional, List
from core.models.biomarker import BiomarkerDefinition, BiomarkerPanel, ReferenceRange
from core.canonical.resolver import CanonicalResolver
from core.canonical.normalize import BiomarkerNormalizer


class BiomarkerService:
    """Service for handling biomarker-specific operations."""
    
    def __init__(self):
        """Initialize the biomarker service."""
        self.resolver = CanonicalResolver()
        self.normalizer = BiomarkerNormalizer()
    
    async def get_all_biomarkers(self) -> Dict[str, BiomarkerDefinition]:
        """
        Get all available biomarkers with their definitions.
        
        Returns:
            Dictionary mapping canonical biomarker names to definitions
        """
        return self.resolver.load_biomarkers()
    
    async def get_biomarker_definition(self, name: str) -> Optional[BiomarkerDefinition]:
        """
        Get definition for a specific biomarker.
        
        Args:
            name: Canonical biomarker name
            
        Returns:
            BiomarkerDefinition or None if not found
        """
        return self.resolver.get_biomarker_definition(name)
    
    async def search_biomarkers(self, query: str) -> List[BiomarkerDefinition]:
        """
        Search biomarkers by name, alias, or description.
        
        Args:
            query: Search query string
            
        Returns:
            List of matching BiomarkerDefinition objects
        """
        all_biomarkers = self.resolver.load_biomarkers()
        query_lower = query.lower()
        
        matches = []
        for biomarker in all_biomarkers.values():
            # Check name
            if query_lower in biomarker.name.lower():
                matches.append(biomarker)
                continue
            
            # Check aliases
            if any(query_lower in alias.lower() for alias in biomarker.aliases):
                matches.append(biomarker)
                continue
            
            # Check description
            if query_lower in biomarker.description.lower():
                matches.append(biomarker)
                continue
            
            # Check category
            if query_lower in biomarker.category.lower():
                matches.append(biomarker)
                continue
        
        return matches
    
    async def get_biomarkers_by_category(self, category: str) -> List[BiomarkerDefinition]:
        """
        Get all biomarkers in a specific category.
        
        Args:
            category: Biomarker category (e.g., "cardiovascular", "metabolic")
            
        Returns:
            List of BiomarkerDefinition objects in the category
        """
        all_biomarkers = self.resolver.load_biomarkers()
        category_lower = category.lower()
        
        return [
            biomarker for biomarker in all_biomarkers.values()
            if biomarker.category.lower() == category_lower
        ]
    
    async def get_biomarker_categories(self) -> List[str]:
        """
        Get all available biomarker categories.
        
        Returns:
            List of unique category names
        """
        all_biomarkers = self.resolver.load_biomarkers()
        categories = set()
        
        for biomarker in all_biomarkers.values():
            if biomarker.category:
                categories.add(biomarker.category)
        
        return sorted(list(categories))
    
    async def normalize_biomarker_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize raw biomarker data to canonical form.
        
        Args:
            raw_data: Raw biomarker data with potential aliases
            
        Returns:
            Dictionary with normalized biomarker data
        """
        biomarker_panel, unmapped_keys = self.normalizer.normalize_biomarkers(raw_data)
        
        # Convert to simple dictionary format
        normalized_data = {}
        for name, biomarker_value in biomarker_panel.biomarkers.items():
            normalized_data[name] = {
                "value": biomarker_value.value,
                "unit": biomarker_value.unit,
                "timestamp": biomarker_value.timestamp
            }
        
        return {
            "normalized_biomarkers": normalized_data,
            "unmapped_keys": unmapped_keys,
            "total_biomarkers": len(normalized_data),
            "unmapped_count": len(unmapped_keys)
        }
    
    async def validate_biomarker_value(
        self, 
        biomarker_name: str, 
        value: float, 
        unit: str,
        age: Optional[int] = None,
        gender: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validate a single biomarker value against reference ranges.
        
        Args:
            biomarker_name: Canonical biomarker name
            value: Measured value
            unit: Unit of measurement
            age: Patient age
            gender: Patient gender
            
        Returns:
            Validation results dictionary
        """
        return self.resolver.validate_biomarker_value(
            biomarker_name=biomarker_name,
            value=value,
            unit=unit,
            age=age,
            gender=gender
        )
    
    async def get_reference_ranges(
        self, 
        biomarker_name: str, 
        age: Optional[int] = None, 
        gender: Optional[str] = None,
        population: str = "general_adult"
    ) -> Optional[ReferenceRange]:
        """
        Get reference range for a biomarker.
        
        Args:
            biomarker_name: Canonical biomarker name
            age: Patient age
            gender: Patient gender
            population: Population group
            
        Returns:
            ReferenceRange object or None if not found
        """
        return self.resolver.get_reference_range(
            biomarker_name=biomarker_name,
            age=age,
            gender=gender,
            population=population
        )
    
    async def get_all_reference_ranges(self, biomarker_name: str) -> List[ReferenceRange]:
        """
        Get all available reference ranges for a biomarker.
        
        Args:
            biomarker_name: Canonical biomarker name
            
        Returns:
            List of ReferenceRange objects
        """
        return self.resolver.get_all_reference_ranges(biomarker_name)
    
    async def convert_unit(self, value: float, from_unit: str, to_unit: str) -> float:
        """
        Convert a value from one unit to another.
        
        Args:
            value: Value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Converted value with 4 decimal place precision
            
        Raises:
            ValueError: If conversion is not supported
        """
        return self.resolver.convert_unit(value, from_unit, to_unit)
    
    async def get_available_units(self) -> Dict[str, Any]:
        """
        Get all available units and conversion factors.
        
        Returns:
            Dictionary with unit definitions and conversion factors
        """
        return self.resolver.load_units()
    
    async def get_biomarker_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about available biomarkers.
        
        Returns:
            Dictionary with biomarker statistics
        """
        all_biomarkers = self.resolver.load_biomarkers()
        
        # Count by category
        category_counts = {}
        for biomarker in all_biomarkers.values():
            category = biomarker.category or "uncategorized"
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Count by data type
        data_type_counts = {}
        for biomarker in all_biomarkers.values():
            data_type = biomarker.data_type or "unknown"
            data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1
        
        # Count units
        unit_counts = {}
        for biomarker in all_biomarkers.values():
            unit = biomarker.unit or "no_unit"
            unit_counts[unit] = unit_counts.get(unit, 0) + 1
        
        return {
            "total_biomarkers": len(all_biomarkers),
            "categories": category_counts,
            "data_types": data_type_counts,
            "units": unit_counts,
            "categories_list": sorted(category_counts.keys()),
            "units_list": sorted(unit_counts.keys())
        }
    
    async def validate_biomarker_panel(self, biomarkers: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an entire biomarker panel.
        
        Args:
            biomarkers: Raw biomarker data
            
        Returns:
            Comprehensive validation results
        """
        try:
            # Normalize the data first
            normalized_result = await self.normalize_biomarker_data(biomarkers)
            normalized_biomarkers = normalized_result["normalized_biomarkers"]
            
            # Validate each biomarker
            validation_results = {}
            total_biomarkers = len(normalized_biomarkers)
            valid_count = 0
            abnormal_count = 0
            error_count = 0
            
            for biomarker_name, biomarker_data in normalized_biomarkers.items():
                value = biomarker_data["value"]
                unit = biomarker_data["unit"]
                
                # Skip non-numeric values
                if not isinstance(value, (int, float)):
                    validation_results[biomarker_name] = {
                        "status": "invalid_type",
                        "message": "Non-numeric value",
                        "value": value,
                        "unit": unit
                    }
                    error_count += 1
                    continue
                
                # Validate against reference ranges
                validation_result = self.resolver.validate_biomarker_value(
                    biomarker_name=biomarker_name,
                    value=float(value),
                    unit=unit
                )
                
                validation_results[biomarker_name] = validation_result
                
                # Count validation results
                if validation_result["status"] == "normal":
                    valid_count += 1
                elif validation_result["status"] in ["low", "high"]:
                    abnormal_count += 1
                elif validation_result["status"] in ["conversion_error", "unknown"]:
                    error_count += 1
            
            # Calculate overall score
            overall_score = valid_count / total_biomarkers if total_biomarkers > 0 else 0.0
            
            return {
                "valid": overall_score >= 0.8,  # 80% threshold for validity
                "overall_score": overall_score,
                "total_biomarkers": total_biomarkers,
                "valid_biomarkers": valid_count,
                "abnormal_biomarkers": abnormal_count,
                "error_biomarkers": error_count,
                "unmapped_biomarkers": normalized_result["unmapped_keys"],
                "validation_results": validation_results,
                "summary": {
                    "normal_percentage": (valid_count / total_biomarkers * 100) if total_biomarkers > 0 else 0,
                    "abnormal_percentage": (abnormal_count / total_biomarkers * 100) if total_biomarkers > 0 else 0,
                    "error_percentage": (error_count / total_biomarkers * 100) if total_biomarkers > 0 else 0
                }
            }
            
        except Exception as e:
            return {
                "valid": False,
                "overall_score": 0.0,
                "error": str(e),
                "total_biomarkers": 0,
                "valid_biomarkers": 0,
                "abnormal_biomarkers": 0,
                "error_biomarkers": 0,
                "unmapped_biomarkers": [],
                "validation_results": {},
                "summary": {
                    "normal_percentage": 0,
                    "abnormal_percentage": 0,
                    "error_percentage": 100
                }
            }
    
    async def get_biomarker_recommendations(
        self, 
        biomarkers: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Generate recommendations based on biomarker values.
        
        Args:
            biomarkers: Raw biomarker data
            user_context: Optional user context (age, gender, etc.)
            
        Returns:
            List of actionable recommendations
        """
        recommendations = []
        
        # Validate the panel first
        validation_result = await self.validate_biomarker_panel(biomarkers)
        
        if not validation_result["valid"]:
            recommendations.append("Consider reviewing biomarker data quality before analysis")
        
        # Check for critical abnormalities
        for biomarker_name, result in validation_result["validation_results"].items():
            if result["status"] == "high":
                if "cholesterol" in biomarker_name:
                    recommendations.append("High cholesterol detected - consider lifestyle modifications and medical consultation")
                elif "glucose" in biomarker_name or "hba1c" in biomarker_name:
                    recommendations.append("Elevated glucose levels detected - consider diabetes screening and dietary modifications")
                elif "pressure" in biomarker_name:
                    recommendations.append("High blood pressure detected - consider monitoring and medical consultation")
            
            elif result["status"] == "low":
                if "hemoglobin" in biomarker_name:
                    recommendations.append("Low hemoglobin detected - consider iron deficiency screening")
                elif "vitamin" in biomarker_name.lower():
                    recommendations.append("Low vitamin levels detected - consider supplementation consultation")
        
        # Add general recommendations based on overall panel quality
        if validation_result["summary"]["abnormal_percentage"] > 30:
            recommendations.append("Multiple abnormal values detected - consider comprehensive health assessment")
        
        if validation_result["summary"]["error_percentage"] > 20:
            recommendations.append("High error rate in biomarker data - consider data verification")
        
        # Add user-specific recommendations if context provided
        if user_context:
            age = user_context.get("age")
            gender = user_context.get("gender")
            
            if age and age > 50:
                recommendations.append("Consider age-appropriate health screenings and monitoring")
            
            if gender == "female" and age and age > 40:
                recommendations.append("Consider hormone level monitoring and bone density assessment")
        
        return recommendations[:10]  # Limit to top 10 recommendations