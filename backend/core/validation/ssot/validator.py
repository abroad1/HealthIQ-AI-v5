"""
SSOT YAML validation utilities.

This module provides validation functionality for SSOT YAML files
including syntax validation, schema validation, and consistency checks.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from .schemas import BiomarkersSchema, RangesSchema, UnitsSchema


class SSOTValidator:
    """Validator for SSOT YAML files."""
    
    def __init__(self):
        """Initialize the SSOT validator."""
        self.supported_files = ['biomarkers.yaml', 'ranges.yaml', 'units.yaml']
    
    def validate_biomarkers_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """
        Validate biomarkers YAML content.
        
        Args:
            yaml_content: YAML content as string
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse YAML
            data = yaml.safe_load(yaml_content)
            if data is None:
                return {
                    "valid": False,
                    "errors": ["YAML file is empty"],
                    "data": None
                }
            
            # Validate schema
            schema = BiomarkersSchema(**data)
            
            return {
                "valid": True,
                "errors": [],
                "data": schema.model_dump(),
                "biomarker_count": len(schema.biomarkers)
            }
            
        except yaml.YAMLError as e:
            return {
                "valid": False,
                "errors": [f"YAML syntax error: {str(e)}"],
                "data": None
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Schema validation error: {str(e)}"],
                "data": None
            }
    
    def validate_ranges_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """
        Validate reference ranges YAML content.
        
        Args:
            yaml_content: YAML content as string
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse YAML
            data = yaml.safe_load(yaml_content)
            if data is None:
                return {
                    "valid": False,
                    "errors": ["YAML file is empty"],
                    "data": None
                }
            
            # Validate schema
            schema = RangesSchema(**data)
            
            # Count total ranges
            total_ranges = sum(len(ranges) for ranges in schema.reference_ranges.values())
            
            return {
                "valid": True,
                "errors": [],
                "data": schema.model_dump(),
                "biomarker_count": len(schema.reference_ranges),
                "range_count": total_ranges
            }
            
        except yaml.YAMLError as e:
            return {
                "valid": False,
                "errors": [f"YAML syntax error: {str(e)}"],
                "data": None
            }
        except Exception as e:
            return {
                "valid": False,
                "data": None,
                "errors": [f"Schema validation error: {str(e)}"]
            }
    
    def validate_units_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """
        Validate units YAML content.
        
        Args:
            yaml_content: YAML content as string
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse YAML
            data = yaml.safe_load(yaml_content)
            if data is None:
                return {
                    "valid": False,
                    "errors": ["YAML file is empty"],
                    "data": None
                }
            
            # Validate schema
            schema = UnitsSchema(**data)
            
            return {
                "valid": True,
                "errors": [],
                "data": schema.model_dump(),
                "unit_count": len(schema.units),
                "conversion_count": 0  # Conversions are not validated separately
            }
            
        except yaml.YAMLError as e:
            return {
                "valid": False,
                "errors": [f"YAML syntax error: {str(e)}"],
                "data": None
            }
        except Exception as e:
            return {
                "valid": False,
                "errors": [f"Schema validation error: {str(e)}"],
                "data": None
            }
    
    def validate_all_ssot_files(self, ssot_directory: Union[str, Path]) -> Dict[str, Any]:
        """
        Validate all SSOT files in a directory.
        
        Args:
            ssot_directory: Path to directory containing SSOT files
            
        Returns:
            Dictionary with validation results for all files
        """
        ssot_path = Path(ssot_directory)
        if not ssot_path.exists():
            return {
                "valid": False,
                "errors": [f"SSOT directory not found: {ssot_path}"],
                "files_validated": 0,
                "file_results": {}
            }
        
        results = {
            "valid": True,
            "errors": [],
            "files_validated": 0,
            "file_results": {}
        }
        
        for filename in self.supported_files:
            file_path = ssot_path / filename
            if not file_path.exists():
                results["errors"].append(f"Required file not found: {filename}")
                results["valid"] = False
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if filename == 'biomarkers.yaml':
                    file_result = self.validate_biomarkers_yaml(content)
                elif filename == 'ranges.yaml':
                    file_result = self.validate_ranges_yaml(content)
                elif filename == 'units.yaml':
                    file_result = self.validate_units_yaml(content)
                else:
                    file_result = {
                        "valid": False,
                        "errors": [f"Unsupported file type: {filename}"],
                        "data": None
                    }
                
                results["file_results"][filename] = file_result
                results["files_validated"] += 1
                
                if not file_result["valid"]:
                    results["valid"] = False
                    results["errors"].extend([f"{filename}: {error}" for error in file_result["errors"]])
                    
            except Exception as e:
                results["valid"] = False
                results["errors"].append(f"Error reading {filename}: {str(e)}")
                results["file_results"][filename] = {
                    "valid": False,
                    "errors": [f"File read error: {str(e)}"],
                    "data": None
                }
        
        return results
    
    def validate_biomarker_consistency(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate consistency between biomarkers and reference ranges.
        
        Args:
            validation_results: Results from validate_all_ssot_files
            
        Returns:
            Dictionary with consistency validation results
        """
        if not validation_results["valid"]:
            return {
                "valid": False,
                "errors": ["Cannot validate consistency with invalid SSOT files"],
                "inconsistent_biomarkers": []
            }
        
        errors = []
        inconsistent_biomarkers = []
        
        # Get biomarkers from biomarkers.yaml
        biomarkers_data = validation_results["file_results"].get("biomarkers.yaml", {})
        if not biomarkers_data.get("valid"):
            return {
                "valid": False,
                "errors": ["Biomarkers file is invalid"],
                "inconsistent_biomarkers": []
            }
        
        biomarkers = set(biomarkers_data["data"]["biomarkers"].keys())
        
        # Get reference ranges from ranges.yaml
        ranges_data = validation_results["file_results"].get("ranges.yaml", {})
        if ranges_data.get("valid"):
            ranges_biomarkers = set(ranges_data["data"]["reference_ranges"].keys())
            
            # Check for biomarkers in ranges but not in biomarkers
            missing_in_biomarkers = ranges_biomarkers - biomarkers
            if missing_in_biomarkers:
                inconsistent_biomarkers.extend(missing_in_biomarkers)
                errors.append(f"Biomarkers in ranges but not in biomarkers: {missing_in_biomarkers}")
            
            # Check for biomarkers in biomarkers but not in ranges
            missing_in_ranges = biomarkers - ranges_biomarkers
            if missing_in_ranges:
                errors.append(f"Biomarkers in biomarkers but not in ranges: {missing_in_ranges}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "inconsistent_biomarkers": inconsistent_biomarkers
        }
    
    def validate_unit_consistency(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate consistency between biomarkers and units.
        
        Args:
            validation_results: Results from validate_all_ssot_files
            
        Returns:
            Dictionary with unit consistency validation results
        """
        if not validation_results["valid"]:
            return {
                "valid": False,
                "errors": ["Cannot validate consistency with invalid SSOT files"],
                "inconsistent_units": []
            }
        
        errors = []
        inconsistent_units = []
        
        # Get units from units.yaml
        units_data = validation_results["file_results"].get("units.yaml", {})
        if not units_data.get("valid"):
            return {
                "valid": False,
                "errors": ["Units file is invalid"],
                "inconsistent_units": []
            }
        
        units = set(units_data["data"]["units"].keys())
        unit_names = {unit_def["name"] for unit_def in units_data["data"]["units"].values()}
        
        # Get biomarkers from biomarkers.yaml
        biomarkers_data = validation_results["file_results"].get("biomarkers.yaml", {})
        if biomarkers_data.get("valid"):
            biomarkers = biomarkers_data["data"]["biomarkers"]
            
            # Check for units used in biomarkers but not defined
            for biomarker_name, biomarker_def in biomarkers.items():
                unit = biomarker_def["unit"]
                if unit not in unit_names:
                    inconsistent_units.append(unit)
                    errors.append(f"Unit '{unit}' used in biomarker '{biomarker_name}' but not defined in units")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "inconsistent_units": inconsistent_units
        }
    
    def get_validation_summary(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get a summary of validation results.
        
        Args:
            validation_results: Results from validate_all_ssot_files
            
        Returns:
            Dictionary with validation summary
        """
        summary = {
            "total_files": validation_results["files_validated"],
            "valid_files": 0,
            "invalid_files": 0,
            "total_biomarkers": 0,
            "total_ranges": 0,
            "total_units": 0,
            "total_conversions": 0
        }
        
        for filename, file_result in validation_results["file_results"].items():
            if file_result["valid"]:
                summary["valid_files"] += 1
                
                if filename == "biomarkers.yaml":
                    summary["total_biomarkers"] = file_result.get("biomarker_count", 0)
                elif filename == "ranges.yaml":
                    summary["total_ranges"] = file_result.get("range_count", 0)
                elif filename == "units.yaml":
                    summary["total_units"] = file_result.get("unit_count", 0)
                    summary["total_conversions"] = file_result.get("conversion_count", 0)
            else:
                summary["invalid_files"] += 1
        
        return summary
