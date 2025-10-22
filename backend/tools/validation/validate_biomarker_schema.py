"""
Biomarker Schema Validation Tool

This module validates that all biomarker definitions have required fields
and are consistent with the expected schema.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import Counter


# Expected biomarker categories (should match frontend constants)
EXPECTED_CATEGORIES = {
    "metabolic",
    "cardiovascular", 
    "inflammatory",
    "kidney",
    "liver",
    "cbc",
    "other"
}


def validate_biomarker_schema(biomarkers_yaml: str) -> Dict[str, Any]:
    """
    Validate that all biomarker definitions have required fields
    and are consistent with the expected schema.
    
    Args:
        biomarkers_yaml: Path to biomarkers.yaml
        
    Returns:
        Dict with summary and errors
    """
    print("🔍 Validating biomarker schema...")
    
    result = {
        "summary": {
            "total_biomarkers": 0,
            "valid_biomarkers": 0,
            "invalid_biomarkers": 0,
            "duplicate_names": 0,
            "invalid_categories": 0
        },
        "errors": [],
        "warnings": []
    }
    
    required_fields = {
        "unit",
        "description", 
        "category",
        "data_type"
    }
    
    try:
        # Load biomarkers
        with open(biomarkers_yaml, 'r', encoding='utf-8') as f:
            biomarkers_data = yaml.safe_load(f)
        
        if 'biomarkers' not in biomarkers_data:
            result["errors"].append("No 'biomarkers' section found in YAML file")
            return result
        
        biomarkers = biomarkers_data['biomarkers']
        result["summary"]["total_biomarkers"] = len(biomarkers)
        
        # Track canonical names for duplicate detection
        canonical_names = []
        categories_found = set()
        
        for biomarker_name, biomarker_info in biomarkers.items():
            biomarker_errors = []
            biomarker_warnings = []
            
            # Check required fields
            missing_fields = required_fields - set(biomarker_info.keys())
            if missing_fields:
                biomarker_errors.append(f"Missing required fields: {', '.join(missing_fields)}")
            
            # Check biomarker name (canonical name)
            if not biomarker_name or not isinstance(biomarker_name, str):
                biomarker_errors.append("biomarker name must be a non-empty string")
            else:
                canonical_names.append(biomarker_name)
            
            # Check unit
            if 'unit' in biomarker_info:
                unit = biomarker_info['unit']
                if not unit or not isinstance(unit, str):
                    biomarker_errors.append("unit must be a non-empty string")
            
            # Check description
            if 'description' in biomarker_info:
                description = biomarker_info['description']
                if not description or not isinstance(description, str):
                    biomarker_errors.append("description must be a non-empty string")
            
            # Check data_type
            if 'data_type' in biomarker_info:
                data_type = biomarker_info['data_type']
                if not data_type or not isinstance(data_type, str):
                    biomarker_errors.append("data_type must be a non-empty string")
                elif data_type not in ['numeric', 'categorical', 'boolean']:
                    biomarker_warnings.append(f"Unknown data_type '{data_type}' (expected: numeric, categorical, boolean)")
            
            # Check category
            if 'category' in biomarker_info:
                category = biomarker_info['category']
                if not category or not isinstance(category, str):
                    biomarker_errors.append("category must be a non-empty string")
                else:
                    categories_found.add(category)
                    if category not in EXPECTED_CATEGORIES:
                        biomarker_warnings.append(f"Unknown category '{category}' (expected: {', '.join(sorted(EXPECTED_CATEGORIES))})")
            
            # Check for empty or None values
            for field in required_fields:
                if field in biomarker_info and biomarker_info[field] is None:
                    biomarker_errors.append(f"{field} cannot be None")
                elif field in biomarker_info and biomarker_info[field] == "":
                    biomarker_errors.append(f"{field} cannot be empty string")
            
            # Add errors and warnings
            if biomarker_errors:
                result["summary"]["invalid_biomarkers"] += 1
                for error in biomarker_errors:
                    result["errors"].append(f"Biomarker '{biomarker_name}': {error}")
            else:
                result["summary"]["valid_biomarkers"] += 1
            
            for warning in biomarker_warnings:
                result["warnings"].append(f"Biomarker '{biomarker_name}': {warning}")
        
        # Check for duplicate canonical names
        name_counts = Counter(canonical_names)
        duplicates = {name: count for name, count in name_counts.items() if count > 1}
        if duplicates:
            result["summary"]["duplicate_names"] = len(duplicates)
            for name, count in duplicates.items():
                result["errors"].append(f"Duplicate canonical_name '{name}' found {count} times")
        
        # Check for unused categories
        unused_categories = EXPECTED_CATEGORIES - categories_found
        if unused_categories:
            result["warnings"].append(f"Unused expected categories: {', '.join(sorted(unused_categories))}")
        
        # Check for unexpected categories
        unexpected_categories = categories_found - EXPECTED_CATEGORIES
        if unexpected_categories:
            result["summary"]["invalid_categories"] = len(unexpected_categories)
            result["warnings"].append(f"Unexpected categories found: {', '.join(sorted(unexpected_categories))}")
        
        # Print summary
        print(f"✅ Valid biomarkers: {result['summary']['valid_biomarkers']}/{result['summary']['total_biomarkers']}")
        print(f"✅ Duplicate names: {result['summary']['duplicate_names']}")
        print(f"✅ Invalid categories: {result['summary']['invalid_categories']}")
        
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


def validate_biomarker_schema_cli():
    """
    CLI entry point for biomarker schema validation.
    """
    import sys
    
    # Default path
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    
    # Allow override via command line arg
    if len(sys.argv) > 1:
        biomarkers_yaml = sys.argv[1]
    
    result = validate_biomarker_schema(biomarkers_yaml)
    
    # Exit with error code if validation failed
    if result["errors"]:
        sys.exit(1)
    
    print("✅ Biomarker schema validation passed!")


if __name__ == "__main__":
    validate_biomarker_schema_cli()
