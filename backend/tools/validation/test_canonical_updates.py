"""
Canonical Updates Test Suite

This module runs all validation scripts and ensures canonical data quality.
"""

import pytest
import json
import os
from pathlib import Path
from typing import Dict, Any

from .validate_aliases_and_ranges import validate_alias_registry
from .validate_biomarker_schema import validate_biomarker_schema
from .generate_validation_report import generate_validation_report


def test_alias_validation():
    """
    Test alias and range validation.
    
    Business Value: Ensures all aliases map to existing canonical biomarkers.
    Failure Impact: Invalid aliases would cause biomarker resolution failures.
    """
    alias_yaml = "backend/ssot/biomarker_alias_registry.yaml"
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    
    # Check if files exist
    if not os.path.exists(alias_yaml):
        pytest.skip(f"Alias registry file not found: {alias_yaml}")
    if not os.path.exists(biomarkers_yaml):
        pytest.skip(f"Biomarkers file not found: {biomarkers_yaml}")
    
    result = validate_alias_registry(alias_yaml, biomarkers_yaml)
    
    # Assertions
    assert "summary" in result, "Result should contain summary"
    assert "errors" in result, "Result should contain errors list"
    assert "warnings" in result, "Result should contain warnings list"
    
    # Check that validation completed
    assert result["summary"]["total_aliases"] >= 0, "Should have non-negative alias count"
    assert result["summary"]["total_biomarkers"] >= 0, "Should have non-negative biomarker count"
    
    # Check for critical errors
    critical_errors = [error for error in result["errors"] if "non-existent canonical" in error]
    assert len(critical_errors) == 0, f"Found aliases mapping to non-existent canonicals: {critical_errors}"
    
    # Check for range validation errors
    range_errors = [error for error in result["errors"] if "invalid range" in error]
    assert len(range_errors) == 0, f"Found invalid reference ranges: {range_errors}"


def test_schema_validation():
    """
    Test biomarker schema validation.
    
    Business Value: Ensures all biomarkers have required fields and valid data.
    Failure Impact: Invalid schema would cause data processing failures.
    """
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    
    # Check if file exists
    if not os.path.exists(biomarkers_yaml):
        pytest.skip(f"Biomarkers file not found: {biomarkers_yaml}")
    
    result = validate_biomarker_schema(biomarkers_yaml)
    
    # Assertions
    assert "summary" in result, "Result should contain summary"
    assert "errors" in result, "Result should contain errors list"
    assert "warnings" in result, "Result should contain warnings list"
    
    # Check that validation completed
    assert result["summary"]["total_biomarkers"] >= 0, "Should have non-negative biomarker count"
    
    # Check for critical errors
    missing_field_errors = [error for error in result["errors"] if "Missing required fields" in error]
    assert len(missing_field_errors) == 0, f"Found biomarkers with missing required fields: {missing_field_errors}"
    
    # Check for duplicate names
    duplicate_errors = [error for error in result["errors"] if "Duplicate canonical_name" in error]
    assert len(duplicate_errors) == 0, f"Found duplicate canonical names: {duplicate_errors}"
    
    # Check for invalid ranges
    range_errors = [error for error in result["errors"] if "range_min" in error and "range_max" in error]
    assert len(range_errors) == 0, f"Found invalid range values: {range_errors}"


def test_validation_report_generation():
    """
    Test validation report generation.
    
    Business Value: Ensures comprehensive validation reports can be generated.
    Failure Impact: Missing reports would make validation status unclear.
    """
    alias_yaml = "backend/ssot/biomarker_alias_registry.yaml"
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    output_dir = "tests/reports"
    
    # Check if input files exist
    if not os.path.exists(alias_yaml):
        pytest.skip(f"Alias registry file not found: {alias_yaml}")
    if not os.path.exists(biomarkers_yaml):
        pytest.skip(f"Biomarkers file not found: {biomarkers_yaml}")
    
    # Generate report
    result = generate_validation_report(alias_yaml, biomarkers_yaml, output_dir)
    
    # Assertions
    assert "timestamp" in result, "Result should contain timestamp"
    assert "alias_validation" in result, "Result should contain alias validation results"
    assert "schema_validation" in result, "Result should contain schema validation results"
    assert "status" in result, "Result should contain overall status"
    assert result["status"] in ["PASS", "FAIL"], "Status should be PASS or FAIL"
    
    # Check that reports were generated
    json_path = os.path.join(output_dir, "validation_report.json")
    html_path = os.path.join(output_dir, "validation_report.html")
    
    assert os.path.exists(json_path), f"JSON report should be generated at {json_path}"
    assert os.path.exists(html_path), f"HTML report should be generated at {html_path}"
    
    # Verify JSON report content
    with open(json_path, 'r', encoding='utf-8') as f:
        json_report = json.load(f)
    
    assert json_report["status"] == result["status"], "JSON report status should match result status"
    assert "timestamp" in json_report, "JSON report should contain timestamp"


def test_run_all_validations():
    """
    Test running all validations together.
    
    Business Value: Ensures all validation tools work together correctly.
    Failure Impact: Integration issues would prevent comprehensive validation.
    """
    result = run_all_validations()
    
    # Assertions
    assert "status" in result, "Result should contain status"
    assert result["status"] in ["PASS", "FAIL"], "Status should be PASS or FAIL"
    
    # If validation fails, provide helpful error message
    if result["status"] == "FAIL":
        error_count = 0
        if "alias_validation" in result:
            error_count += len(result["alias_validation"].get("errors", []))
        if "schema_validation" in result:
            error_count += len(result["schema_validation"].get("errors", []))
        
        pytest.fail(f"Validation failed with {error_count} errors. Check validation reports for details.")


def run_all_validations() -> Dict[str, Any]:
    """
    Run all validation tools and return combined results.
    
    Returns:
        Combined validation results
    """
    print("🚀 Running all validation tools...")
    
    alias_yaml = "backend/ssot/biomarker_alias_registry.yaml"
    biomarkers_yaml = "backend/ssot/biomarkers.yaml"
    
    # Check if files exist
    if not os.path.exists(alias_yaml):
        return {
            "status": "FAIL",
            "error": f"Alias registry file not found: {alias_yaml}"
        }
    
    if not os.path.exists(biomarkers_yaml):
        return {
            "status": "FAIL", 
            "error": f"Biomarkers file not found: {biomarkers_yaml}"
        }
    
    # Run validations
    alias_results = validate_alias_registry(alias_yaml, biomarkers_yaml)
    schema_results = validate_biomarker_schema(biomarkers_yaml)
    
    # Determine overall status
    has_errors = bool(alias_results["errors"] or schema_results["errors"])
    status = "PASS" if not has_errors else "FAIL"
    
    result = {
        "status": status,
        "alias_validation": alias_results,
        "schema_validation": schema_results
    }
    
    # Print summary
    if status == "PASS":
        print("✅ Validation passed (aliases + ranges + schema)")
    else:
        error_count = len(alias_results["errors"]) + len(schema_results["errors"])
        print(f"❌ Validation failed with {error_count} errors")
    
    return result


if __name__ == "__main__":
    # Run all validations when executed directly
    result = run_all_validations()
    
    if result["status"] == "PASS":
        print("🎉 All validations passed!")
        exit(0)
    else:
        print("💥 Some validations failed!")
        exit(1)
