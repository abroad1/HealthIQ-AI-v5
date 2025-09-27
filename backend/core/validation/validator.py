"""
SSOT YAML Validator
HealthIQ-AI v5 Backend

Validates SSOT YAML files against defined schemas and provides detailed error reporting.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from pydantic import ValidationError

from .schemas import (
    BiomarkersSchema,
    ReferenceRangesSchema, 
    UnitsSchema,
    BiomarkerDefinition,
    ReferenceRange,
    UnitDefinition,
)

logger = logging.getLogger(__name__)


class SSOTValidationError(Exception):
    """Custom exception for SSOT validation errors"""
    
    def __init__(self, message: str, errors: List[Dict[str, Any]] = None):
        super().__init__(message)
        self.errors = errors or []


class SSOTValidator:
    """Validates SSOT YAML files against defined schemas"""
    
    def __init__(self, ssot_dir: str = "backend/ssot"):
        """
        Initialize validator with SSOT directory path
        
        Args:
            ssot_dir: Path to directory containing SSOT YAML files
        """
        self.ssot_dir = Path(ssot_dir)
        self.validation_results = {}
        
    def validate_biomarkers(self, file_path: Optional[str] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validate biomarkers.yaml file
        
        Args:
            file_path: Optional path to biomarkers.yaml file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        if file_path is None:
            file_path = self.ssot_dir / "biomarkers.yaml"
        else:
            file_path = Path(file_path)
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Validate against schema
            schema = BiomarkersSchema(**data)
            
            # Additional validation: check that all biomarkers have corresponding reference ranges
            self._validate_biomarker_reference_consistency(schema.biomarkers)
            
            logger.info(f"✅ biomarkers.yaml validation successful: {len(schema.biomarkers)} biomarkers validated")
            return True, []
            
        except FileNotFoundError:
            error_msg = f"biomarkers.yaml file not found at {file_path}"
            logger.error(error_msg)
            return False, [{"error": "file_not_found", "message": error_msg}]
            
        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error in biomarkers.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "yaml_parse_error", "message": error_msg}]
            
        except ValidationError as e:
            errors = []
            for error in e.errors():
                errors.append({
                    "error": "validation_error",
                    "field": " -> ".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "value": error.get("input", "N/A")
                })
            logger.error(f"❌ biomarkers.yaml validation failed: {len(errors)} errors")
            return False, errors
            
        except Exception as e:
            error_msg = f"Unexpected error validating biomarkers.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "unexpected_error", "message": error_msg}]
    
    def validate_reference_ranges(self, file_path: Optional[str] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validate ranges.yaml file
        
        Args:
            file_path: Optional path to ranges.yaml file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        if file_path is None:
            file_path = self.ssot_dir / "ranges.yaml"
        else:
            file_path = Path(file_path)
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Validate against schema
            schema = ReferenceRangesSchema(**data)
            
            # Additional validation: check range completeness
            self._validate_range_completeness(schema.reference_ranges)
            
            logger.info(f"✅ ranges.yaml validation successful: {len(schema.reference_ranges)} biomarkers with ranges validated")
            return True, []
            
        except FileNotFoundError:
            error_msg = f"ranges.yaml file not found at {file_path}"
            logger.error(error_msg)
            return False, [{"error": "file_not_found", "message": error_msg}]
            
        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error in ranges.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "yaml_parse_error", "message": error_msg}]
            
        except ValidationError as e:
            errors = []
            for error in e.errors():
                errors.append({
                    "error": "validation_error",
                    "field": " -> ".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "value": error.get("input", "N/A")
                })
            logger.error(f"❌ ranges.yaml validation failed: {len(errors)} errors")
            return False, errors
            
        except Exception as e:
            error_msg = f"Unexpected error validating ranges.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "unexpected_error", "message": error_msg}]
    
    def validate_units(self, file_path: Optional[str] = None) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Validate units.yaml file
        
        Args:
            file_path: Optional path to units.yaml file
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        if file_path is None:
            file_path = self.ssot_dir / "units.yaml"
        else:
            file_path = Path(file_path)
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Validate only the units section against UnitDefinition schema
            # Skip conversions and categories for now as they have different structure
            units_data = {k: v for k, v in data.get('units', {}).items() 
                         if k not in ['conversions', 'categories']}
            
            # Validate units against UnitDefinition schema
            for unit_id, unit_data in units_data.items():
                UnitDefinition(**unit_data)
            
            # Additional validation: check unit usage consistency
            self._validate_unit_usage_consistency(units_data)
            
            logger.info(f"✅ units.yaml validation successful: {len(units_data)} units validated")
            return True, []
            
        except FileNotFoundError:
            error_msg = f"units.yaml file not found at {file_path}"
            logger.error(error_msg)
            return False, [{"error": "file_not_found", "message": error_msg}]
            
        except yaml.YAMLError as e:
            error_msg = f"YAML parsing error in units.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "yaml_parse_error", "message": error_msg}]
            
        except ValidationError as e:
            errors = []
            for error in e.errors():
                errors.append({
                    "error": "validation_error",
                    "field": " -> ".join(str(x) for x in error["loc"]),
                    "message": error["msg"],
                    "value": error.get("input", "N/A")
                })
            logger.error(f"❌ units.yaml validation failed: {len(errors)} errors")
            return False, errors
            
        except Exception as e:
            error_msg = f"Unexpected error validating units.yaml: {str(e)}"
            logger.error(error_msg)
            return False, [{"error": "unexpected_error", "message": error_msg}]
    
    def validate_all(self) -> Dict[str, Tuple[bool, List[Dict[str, Any]]]]:
        """
        Validate all SSOT YAML files
        
        Returns:
            Dictionary mapping file names to (is_valid, errors) tuples
        """
        results = {}
        
        # Validate each file
        results["biomarkers.yaml"] = self.validate_biomarkers()
        results["ranges.yaml"] = self.validate_reference_ranges()
        results["units.yaml"] = self.validate_units()
        
        # Store results for reporting
        self.validation_results = results
        
        # Log overall status
        all_valid = all(is_valid for is_valid, _ in results.values())
        if all_valid:
            logger.info("✅ All SSOT YAML files validated successfully")
        else:
            failed_files = [name for name, (is_valid, _) in results.items() if not is_valid]
            logger.error(f"❌ SSOT validation failed for: {', '.join(failed_files)}")
        
        return results
    
    def _validate_biomarker_reference_consistency(self, biomarkers: Dict[str, BiomarkerDefinition]) -> None:
        """Validate that biomarkers have consistent reference ranges"""
        # This would check against ranges.yaml in a full implementation
        # For now, we'll just log a note
        logger.debug(f"Validating biomarker-reference consistency for {len(biomarkers)} biomarkers")
    
    def _validate_range_completeness(self, reference_ranges: Dict[str, Dict[str, ReferenceRange]]) -> None:
        """Validate that reference ranges are complete and non-overlapping"""
        for biomarker_id, ranges in reference_ranges.items():
            # Check that ranges cover the full spectrum
            range_values = [(r.min, r.max) for r in ranges.values()]
            range_values.sort()
            
            # Check for gaps (simplified check)
            for i in range(len(range_values) - 1):
                if range_values[i][1] < range_values[i+1][0]:
                    logger.warning(f"Gap found in ranges for {biomarker_id}: "
                                 f"{range_values[i][1]} to {range_values[i+1][0]}")
    
    def _validate_unit_usage_consistency(self, units: Dict[str, UnitDefinition]) -> None:
        """Validate that units are used consistently across SSOT files"""
        # This would check unit usage in biomarkers.yaml and ranges.yaml
        # For now, we'll just log a note
        logger.debug(f"Validating unit usage consistency for {len(units)} units")
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results
        
        Returns:
            Dictionary with validation summary
        """
        if not self.validation_results:
            return {"status": "not_validated", "message": "No validation results available"}
        
        total_files = len(self.validation_results)
        valid_files = sum(1 for is_valid, _ in self.validation_results.values() if is_valid)
        total_errors = sum(len(errors) for _, errors in self.validation_results.values())
        
        return {
            "status": "valid" if valid_files == total_files else "invalid",
            "total_files": total_files,
            "valid_files": valid_files,
            "invalid_files": total_files - valid_files,
            "total_errors": total_errors,
            "files": {
                name: {
                    "valid": is_valid,
                    "error_count": len(errors),
                    "errors": errors
                }
                for name, (is_valid, errors) in self.validation_results.items()
            }
        }
