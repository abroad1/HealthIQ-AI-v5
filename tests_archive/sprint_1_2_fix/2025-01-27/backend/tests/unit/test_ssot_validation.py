# ARCHIVED TEST
# Reason: Medium-value test (infrastructure/framework)
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_ssot_validation.py

"""
Unit tests for SSOT YAML schema validation.
"""

import pytest
import yaml
from pathlib import Path
from unittest.mock import Mock, patch
from core.validation.ssot.schemas import (
    BiomarkerDefinition,
    ReferenceRange,
    UnitDefinition,
    BiomarkersSchema,
    RangesSchema,
    UnitsSchema,
)
from core.validation.ssot.validator import SSOTValidator


class TestBiomarkerDefinition:
    """Test cases for BiomarkerDefinition schema."""
    
    def test_valid_biomarker_definition(self):
        """Test valid biomarker definition creation."""
        biomarker_data = {
            "aliases": ["cholesterol", "total_chol"],
            "unit": "mg/dL",
            "description": "Total cholesterol level",
            "category": "cardiovascular",
            "data_type": "numeric",
        }
        
        biomarker = BiomarkerDefinition(**biomarker_data)
        
        assert biomarker.aliases == ["cholesterol", "total_chol"]
        assert biomarker.unit == "mg/dL"
        assert biomarker.description == "Total cholesterol level"
        assert biomarker.category == "cardiovascular"
        assert biomarker.data_type == "numeric"
    
    def test_biomarker_definition_missing_required_fields(self):
        """Test biomarker definition with missing required fields."""
        with pytest.raises(ValueError):
            BiomarkerDefinition(unit="mg/dL")  # Missing required fields

    def test_biomarker_definition_invalid_data_type(self):
        """Test biomarker definition with invalid data type."""
        biomarker_data = {
            "aliases": ["cholesterol"],
            "unit": "mg/dL",
            "description": "Total cholesterol level",
            "category": "cardiovascular",
            "data_type": "invalid_type",  # Invalid data type
        }
        
        with pytest.raises(ValueError):
            BiomarkerDefinition(**biomarker_data)

    def test_biomarker_definition_invalid_category(self):
        """Test biomarker definition with invalid category."""
        biomarker_data = {
            "aliases": ["cholesterol"],
            "unit": "mg/dL",
            "description": "Total cholesterol level",
            "category": "invalid_category",  # Invalid category
            "data_type": "numeric",
        }
        
        with pytest.raises(ValueError):
            BiomarkerDefinition(**biomarker_data)


class TestReferenceRange:
    """Test cases for ReferenceRange schema."""
    
    def test_valid_reference_range(self):
        """Test valid reference range creation."""
        range_data = {
            "min": 0,
            "max": 200,
            "unit": "mg/dL",
            "population": "general_adult",
        }
        
        ref_range = ReferenceRange(**range_data)
        
        assert ref_range.min == 0
        assert ref_range.max == 200
        assert ref_range.unit == "mg/dL"
        assert ref_range.population == "general_adult"

    def test_reference_range_invalid_min_max(self):
        """Test reference range with invalid min/max values."""
        range_data = {
            "min": 200,  # min > max
            "max": 100,
            "unit": "mg/dL",
            "population": "general_adult",
        }
        
        with pytest.raises(ValueError):
            ReferenceRange(**range_data)

    def test_reference_range_missing_required_fields(self):
        """Test reference range with missing required fields."""
        with pytest.raises(ValueError):
            ReferenceRange(min=0, max=200)  # Missing unit and population


class TestUnitDefinition:
    """Test cases for UnitDefinition schema."""
    
    def test_valid_unit_definition(self):
        """Test valid unit definition creation."""
        unit_data = {
            "name": "mg/dL",
            "description": "Milligrams per deciliter",
            "category": "concentration",
            "si_equivalent": "mg/dL",
        }
        
        unit = UnitDefinition(**unit_data)
        
        assert unit.name == "mg/dL"
        assert unit.description == "Milligrams per deciliter"
        assert unit.category == "concentration"
        assert unit.si_equivalent == "mg/dL"
    
    def test_unit_definition_invalid_category(self):
        """Test unit definition with invalid category."""
        unit_data = {
            "name": "mg/dL",
            "description": "Milligrams per deciliter",
            "category": "invalid_category",  # Invalid category
            "si_equivalent": "mg/dL",
        }
        
        with pytest.raises(ValueError):
            UnitDefinition(**unit_data)


class TestBiomarkersSchema:
    """Test cases for BiomarkersSchema validation."""
    
    def test_valid_biomarkers_schema(self):
        """Test valid biomarkers schema."""
        biomarkers_data = {
            "biomarkers": {
                "total_cholesterol": {
                    "aliases": ["cholesterol"],
                    "unit": "mg/dL",
                    "description": "Total cholesterol level",
                    "category": "cardiovascular",
                    "data_type": "numeric",
                }
            }
        }
        
        schema = BiomarkersSchema(**biomarkers_data)
        assert len(schema.biomarkers) == 1
        assert "total_cholesterol" in schema.biomarkers

    def test_biomarkers_schema_missing_biomarkers_key(self):
        """Test biomarkers schema with missing biomarkers key."""
        with pytest.raises(ValueError):
            BiomarkersSchema(biomarkers={})  # Missing biomarkers key

    def test_biomarkers_schema_empty_biomarkers(self):
        """Test biomarkers schema with empty biomarkers."""
        with pytest.raises(ValueError):
            BiomarkersSchema(biomarkers={})  # Empty biomarkers


class TestRangesSchema:
    """Test cases for RangesSchema validation."""

    def test_valid_ranges_schema(self):
        """Test valid ranges schema."""
        ranges_data = {
            "reference_ranges": {
                "total_cholesterol": {
                    "normal": {
                        "min": 0,
                        "max": 200,
                        "unit": "mg/dL",
                        "population": "general_adult",
                    }
                }
            }
        }
        
        schema = RangesSchema(**ranges_data)
        assert len(schema.reference_ranges) == 1
        assert "total_cholesterol" in schema.reference_ranges

    def test_ranges_schema_missing_reference_ranges_key(self):
        """Test ranges schema with missing reference_ranges key."""
        with pytest.raises(ValueError):
            RangesSchema(reference_ranges={})  # Missing reference_ranges key


class TestUnitsSchema:
    """Test cases for UnitsSchema validation."""
    
    def test_valid_units_schema(self):
        """Test valid units schema."""
        units_data = {
            "units": {
                "mg_dL": {
                    "name": "mg/dL",
                    "description": "Milligrams per deciliter",
                    "category": "concentration",
                    "si_equivalent": "mg/dL",
                }
            }
        }
        
        schema = UnitsSchema(**units_data)
        assert len(schema.units) == 1
        assert "mg_dL" in schema.units

    def test_units_schema_missing_units_key(self):
        """Test units schema with missing units key."""
        with pytest.raises(ValueError):
            UnitsSchema(units={})  # Missing units key


class TestSSOTValidator:
    """Test cases for SSOTValidator class."""

    @pytest.fixture
    def validator(self):
        """Create SSOT validator instance for testing."""
        return SSOTValidator()

    @pytest.fixture
    def sample_biomarkers_yaml(self):
        """Sample biomarkers YAML content."""
        return """
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol", "total_chol"]
    unit: "mg/dL"
    description: "Total cholesterol level"
    category: "cardiovascular"
    data_type: "numeric"
"""

    @pytest.fixture
    def sample_ranges_yaml(self):
        """Sample ranges YAML content."""
        return """
reference_ranges:
  total_cholesterol:
    normal:
      min: 0
      max: 200
      unit: "mg/dL"
      population: "general_adult"
"""

    @pytest.fixture
    def sample_units_yaml(self):
        """Sample units YAML content."""
        return """
units:
  mg_dL:
    name: "mg/dL"
    description: "Milligrams per deciliter"
    category: "concentration"
    si_equivalent: "mg/dL"
"""

    def test_validate_biomarkers_yaml_success(self, validator, sample_biomarkers_yaml):
        """Test successful biomarkers YAML validation."""
        result = validator.validate_biomarkers_yaml(sample_biomarkers_yaml)
        
        assert result["valid"] is True
        assert result["errors"] == []
        assert "total_cholesterol" in result["data"]["biomarkers"]

    def test_validate_biomarkers_yaml_invalid_syntax(self, validator):
        """Test biomarkers YAML validation with invalid YAML syntax."""
        invalid_yaml = """
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol"  # Missing closing bracket
    unit: "mg/dL"
"""
        
        result = validator.validate_biomarkers_yaml(invalid_yaml)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "YAML syntax error" in result["errors"][0]

    def test_validate_biomarkers_yaml_invalid_schema(self, validator):
        """Test biomarkers YAML validation with invalid schema."""
        invalid_yaml = """
biomarkers:
  total_cholesterol:
    unit: "mg/dL"
    # Missing required fields
"""
        
        result = validator.validate_biomarkers_yaml(invalid_yaml)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "validation error" in result["errors"][0]

    def test_validate_ranges_yaml_success(self, validator, sample_ranges_yaml):
        """Test successful ranges YAML validation."""
        result = validator.validate_ranges_yaml(sample_ranges_yaml)
        
        assert result["valid"] is True
        assert result["errors"] == []
        assert "total_cholesterol" in result["data"]["reference_ranges"]

    def test_validate_units_yaml_success(self, validator, sample_units_yaml):
        """Test successful units YAML validation."""
        result = validator.validate_units_yaml(sample_units_yaml)
        
        assert result["valid"] is True
        assert result["errors"] == []
        assert "mg_dL" in result["data"]["units"]

    def test_validate_all_ssot_files_success(self, validator, tmp_path):
        """Test validation of all SSOT files."""
        # Create temporary SSOT files
        biomarkers_file = tmp_path / "biomarkers.yaml"
        ranges_file = tmp_path / "ranges.yaml"
        units_file = tmp_path / "units.yaml"
        
        biomarkers_file.write_text("""
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol"]
    unit: "mg/dL"
    description: "Total cholesterol level"
    category: "cardiovascular"
    data_type: "numeric"
""")
        
        ranges_file.write_text("""
reference_ranges:
  total_cholesterol:
    normal:
      min: 0
      max: 200
      unit: "mg/dL"
      population: "general_adult"
""")
        
        units_file.write_text("""
units:
  mg_dL:
    name: "mg/dL"
    description: "Milligrams per deciliter"
    category: "concentration"
    si_equivalent: "mg/dL"
""")
        
        result = validator.validate_all_ssot_files(tmp_path)
        
        assert result["valid"] is True
        assert result["errors"] == []
        assert result["files_validated"] == 3

    def test_validate_all_ssot_files_missing_files(self, validator, tmp_path):
        """Test validation with missing SSOT files."""
        result = validator.validate_all_ssot_files(tmp_path)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert "not found" in result["errors"][0]

    def test_validate_all_ssot_files_invalid_content(self, validator, tmp_path):
        """Test validation with invalid SSOT file content."""
        biomarkers_file = tmp_path / "biomarkers.yaml"
        biomarkers_file.write_text("invalid: yaml: content: [")
        
        result = validator.validate_all_ssot_files(tmp_path)
        
        assert result["valid"] is False
        assert len(result["errors"]) > 0

    def test_get_validation_summary(self, validator, tmp_path):
        """Test getting validation summary."""
        # Create valid SSOT files
        biomarkers_file = tmp_path / "biomarkers.yaml"
        biomarkers_file.write_text("""
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol"]
    unit: "mg/dL"
    description: "Total cholesterol level"
    category: "cardiovascular"
    data_type: "numeric"
""")
        
        result = validator.validate_all_ssot_files(tmp_path)
        summary = validator.get_validation_summary(result)
        
        assert "total_biomarkers" in summary
        assert "total_ranges" in summary
        assert "total_units" in summary
        assert summary["total_biomarkers"] == 1

    def test_validate_biomarker_consistency(self, validator, tmp_path):
        """Test biomarker consistency validation."""
        # Create SSOT files with inconsistent biomarker references
        biomarkers_file = tmp_path / "biomarkers.yaml"
        ranges_file = tmp_path / "ranges.yaml"
        units_file = tmp_path / "units.yaml"
        
        biomarkers_file.write_text("""
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol"]
    unit: "mg/dL"
    description: "Total cholesterol level"
    category: "cardiovascular"
    data_type: "numeric"
""")
        
        ranges_file.write_text("""
reference_ranges:
  unknown_biomarker:  # Biomarker not defined in biomarkers.yaml
    normal:
      min: 0
      max: 200
      unit: "mg/dL"
      population: "general_adult"
""")
        
        units_file.write_text("""
units:
  mg_dL:
    name: "mg/dL"
    description: "Milligrams per deciliter"
    category: "concentration"
    si_equivalent: "mg/dL"
""")
        
        result = validator.validate_all_ssot_files(tmp_path)
        consistency_result = validator.validate_biomarker_consistency(result)
        
        assert consistency_result["valid"] is False
        assert len(consistency_result["errors"]) > 0
        assert "unknown_biomarker" in consistency_result["errors"][0]

    def test_validate_unit_consistency(self, validator, tmp_path):
        """Test unit consistency validation."""
        # Create SSOT files with inconsistent unit references
        biomarkers_file = tmp_path / "biomarkers.yaml"
        units_file = tmp_path / "units.yaml"
        ranges_file = tmp_path / "ranges.yaml"
        
        biomarkers_file.write_text("""
biomarkers:
  total_cholesterol:
    aliases: ["cholesterol"]
    unit: "unknown_unit"  # Unit not defined in units.yaml
    description: "Total cholesterol level"
    category: "cardiovascular"
    data_type: "numeric"
""")
        
        units_file.write_text("""
units:
  mg_dL:
    name: "mg/dL"
    description: "Milligrams per deciliter"
    category: "concentration"
    si_equivalent: "mg/dL"
""")
        
        ranges_file.write_text("""
reference_ranges:
  total_cholesterol:
    normal:
      min: 0
      max: 200
      unit: "mg/dL"
      population: "general_adult"
""")
        
        result = validator.validate_all_ssot_files(tmp_path)
        consistency_result = validator.validate_unit_consistency(result)
        
        assert consistency_result["valid"] is False
        assert len(consistency_result["errors"]) > 0
        assert "unknown_unit" in consistency_result["errors"][0]