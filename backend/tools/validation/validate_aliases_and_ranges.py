"""
Alias and Range Validation Tool

This module validates that all aliases map to existing canonical biomarkers
and that reference ranges are numerically consistent.
"""

import yaml
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Tuple
from decimal import Decimal


def validate_alias_registry(alias_yaml: str, biomarkers_yaml: str) -> Dict[str, Any]:
    """
    Validate that all aliases map to existing canonical biomarkers
    and that reference ranges are numerically consistent.
    
    Args:
        alias_yaml: Path to biomarker_alias_registry.yaml
        biomarkers_yaml: Path to biomarkers.yaml
        
    Returns:
        Dict with summary and errors
    """
    print("🔍 Validating alias registry and reference ranges...")
    
    result = {
        "summary": {
            "total_aliases": 0,
            "valid_aliases": 0,
            "invalid_aliases": 0,
            "total_biomarkers": 0,
            "valid_ranges": 0,
            "invalid_ranges": 0
        },
        "errors": [],
        "warnings": []
    }
    
    try:
        # Load alias registry
        with open(alias_yaml, 'r', encoding='utf-8') as f:
            alias_data = yaml.safe_load(f)
        
        # Load biomarkers
        with open(biomarkers_yaml, 'r', encoding='utf-8') as f:
            biomarkers_data = yaml.safe_load(f)
        
        # Extract canonical biomarker names
        canonical_names = set()
        if 'biomarkers' in biomarkers_data:
            for biomarker_name, biomarker_info in biomarkers_data['biomarkers'].items():
                canonical_names.add(biomarker_name)
        
        result["summary"]["total_biomarkers"] = len(canonical_names)
        
        # Validate aliases
        if 'aliases' in alias_data:
            for alias_name, alias_info in alias_data['aliases'].items():
                result["summary"]["total_aliases"] += 1
                
                if 'canonical_name' not in alias_info:
                    result["errors"].append(f"Alias '{alias_name}' missing canonical_name")
                    result["summary"]["invalid_aliases"] += 1
                    continue
                
                canonical_name = alias_info['canonical_name']
                if canonical_name not in canonical_names:
                    result["errors"].append(f"Alias '{alias_name}' maps to non-existent canonical '{canonical_name}'")
                    result["summary"]["invalid_aliases"] += 1
                    continue
                
                result["summary"]["valid_aliases"] += 1
        
        # Validate reference ranges from separate ranges file
        ranges_yaml = biomarkers_yaml.replace('biomarkers.yaml', 'ranges.yaml')
        if os.path.exists(ranges_yaml):
            with open(ranges_yaml, 'r', encoding='utf-8') as f:
                ranges_data = yaml.safe_load(f)
            
            if 'reference_ranges' in ranges_data:
                for biomarker_name, ranges in ranges_data['reference_ranges'].items():
                    if biomarker_name not in canonical_names:
                        result["warnings"].append(f"Range defined for non-canonical biomarker '{biomarker_name}'")
                        continue
                    
                    # Check normal range
                    if 'normal' in ranges:
                        normal_range = ranges['normal']
                        try:
                            min_val = float(normal_range.get('min', 0))
                            max_val = float(normal_range.get('max', 0))
                            
                            if min_val >= max_val:
                                result["errors"].append(f"Biomarker '{biomarker_name}' has invalid normal range: min={min_val} >= max={max_val}")
                                result["summary"]["invalid_ranges"] += 1
                            else:
                                result["summary"]["valid_ranges"] += 1
                                
                        except (ValueError, TypeError) as e:
                            result["errors"].append(f"Biomarker '{biomarker_name}' has non-numeric normal range values: {e}")
                            result["summary"]["invalid_ranges"] += 1
                    else:
                        result["warnings"].append(f"Biomarker '{biomarker_name}' missing normal range")
        else:
            result["warnings"].append(f"Ranges file not found: {ranges_yaml}")
        
        # Print summary
        print(f"✅ Aliases: {result['summary']['valid_aliases']}/{result['summary']['total_aliases']} valid")
        print(f"✅ Ranges: {result['summary']['valid_ranges']}/{result['summary']['total_biomarkers']} valid")
        
        if result["errors"]:
            print(f"❌ Found {len(result['errors'])} errors:")
            for error in result["errors"][:5]:  # Show first 5 errors
                print(f"   - {error}")
            if len(result["errors"]) > 5:
                print(f"   ... and {len(result['errors']) - 5} more errors")
        
        if result["warnings"]:
            print(f"⚠️  Found {len(result['warnings'])} warnings:")
            for warning in result["warnings"][:3]:  # Show first 3 warnings
                print(f"   - {warning}")
            if len(result["warnings"]) > 3:
                print(f"   ... and {len(result['warnings']) - 3} more warnings")
        
    except FileNotFoundError as e:
        result["errors"].append(f"File not found: {e}")
    except yaml.YAMLError as e:
        result["errors"].append(f"YAML parsing error: {e}")
    except Exception as e:
        result["errors"].append(f"Unexpected error: {e}")
    
    return result


def validate_alias_registry_cli():
    """
    CLI entry point for alias and range validation.
    """
    import sys
    
    # Default paths
    alias_yaml = "backend/ssot/biomarker_alias_registry.yaml"
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    
    # Allow override via command line args
    if len(sys.argv) > 1:
        alias_yaml = sys.argv[1]
    if len(sys.argv) > 2:
        biomarkers_yaml = sys.argv[2]
    
    result = validate_alias_registry(alias_yaml, biomarkers_yaml)
    
    # Exit with error code if validation failed
    if result["errors"]:
        sys.exit(1)
    
    print("✅ Alias and range validation passed!")


if __name__ == "__main__":
    validate_alias_registry_cli()
