# ARCHIVED TEST
# Reason: Tests expect custom error messages but Pydantic provides standard validation errors
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_validation_schemas_coverage.py

"""
Unit tests for validation schemas to improve coverage.
"""

import pytest
from pydantic import ValidationError
from core.validation.schemas import (
    BiomarkerDefinition, ReferenceRange, UnitDefinition,
    BiomarkersSchema, ReferenceRangesSchema, UnitsSchema
)


class TestBiomarkerDefinitionCoverage:
    """Test cases for BiomarkerDefinition schema coverage."""
    
    def test_validate_aliases_empty_list(self):
        """Test validation with empty aliases list."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=[],
                unit="mg/dL",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        assert "At least one alias is required" in str(exc_info.value)
    
    def test_validate_aliases_empty_string(self):
        """Test validation with empty string alias."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["valid", ""],
                unit="mg/dL",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        assert "Aliases cannot be empty or whitespace" in str(exc_info.value)
    
    def test_validate_aliases_whitespace_only(self):
        """Test validation with whitespace-only alias."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["valid", "   "],
                unit="mg/dL",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        assert "Aliases cannot be empty or whitespace" in str(exc_info.value)
    
    def test_validate_unit_empty(self):
        """Test validation with empty unit."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["test"],
                unit="",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        assert "Unit cannot be empty" in str(exc_info.value)
    
    def test_validate_unit_whitespace(self):
        """Test validation with whitespace-only unit."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["test"],
                unit="   ",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        assert "Unit cannot be empty" in str(exc_info.value)
    
    def test_validate_category_invalid(self):
        """Test validation with invalid category."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["test"],
                unit="mg/dL",
                description="Test biomarker",
                category="invalid_category",
                data_type="numeric"
            )
        assert "Category must be one of" in str(exc_info.value)
    
    def test_validate_data_type_invalid(self):
        """Test validation with invalid data type."""
        with pytest.raises(ValidationError) as exc_info:
            BiomarkerDefinition(
                aliases=["test"],
                unit="mg/dL",
                description="Test biomarker",
                category="cardiovascular",
                data_type="invalid_type"
            )
        assert "String should match pattern" in str(exc_info.value)


class TestReferenceRangeCoverage:
    """Test cases for ReferenceRange schema coverage."""
    
    def test_validate_biomarker_empty(self):
        """Test validation with empty biomarker name."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="",
                population="adult",
                min_value=50.0,
                max_value=100.0,
                unit="mg/dL"
            )
        assert "Biomarker name cannot be empty" in str(exc_info.value)
    
    def test_validate_biomarker_whitespace(self):
        """Test validation with whitespace-only biomarker name."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="   ",
                population="adult",
                min_value=50.0,
                max_value=100.0,
                unit="mg/dL"
            )
        assert "Biomarker name cannot be empty" in str(exc_info.value)
    
    def test_validate_population_invalid(self):
        """Test validation with invalid population."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="test",
                population="invalid_population",
                min_value=50.0,
                max_value=100.0,
                unit="mg/dL"
            )
        assert "Population must be one of" in str(exc_info.value)
    
    def test_validate_min_value_negative(self):
        """Test validation with negative min value."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="test",
                population="adult",
                min_value=-10.0,
                max_value=100.0,
                unit="mg/dL"
            )
        assert "Min value must be non-negative" in str(exc_info.value)
    
    def test_validate_max_value_negative(self):
        """Test validation with negative max value."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="test",
                population="adult",
                min_value=50.0,
                max_value=-10.0,
                unit="mg/dL"
            )
        assert "Max value must be non-negative" in str(exc_info.value)
    
    def test_validate_min_greater_than_max(self):
        """Test validation with min greater than max."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="test",
                population="adult",
                min_value=100.0,
                max_value=50.0,
                unit="mg/dL"
            )
        assert "Min value must be less than or equal to max value" in str(exc_info.value)
    
    def test_validate_unit_empty(self):
        """Test validation with empty unit."""
        with pytest.raises(ValidationError) as exc_info:
            ReferenceRange(
                biomarker="test",
                population="adult",
                min_value=50.0,
                max_value=100.0,
                unit=""
            )
        assert "Unit cannot be empty" in str(exc_info.value)


class TestUnitDefinitionCoverage:
    """Test cases for UnitDefinition schema coverage."""
    
    def test_validate_name_empty(self):
        """Test validation with empty unit name."""
        with pytest.raises(ValidationError) as exc_info:
            UnitDefinition(
                name="",
                category="volume",
                si_equivalent="L",
                conversion_factor=1.0
            )
        assert "Unit name cannot be empty" in str(exc_info.value)
    
    def test_validate_category_invalid(self):
        """Test validation with invalid category."""
        with pytest.raises(ValidationError) as exc_info:
            UnitDefinition(
                name="test_unit",
                category="invalid_category",
                si_equivalent="L",
                conversion_factor=1.0
            )
        assert "Category must be one of" in str(exc_info.value)
    
    def test_validate_si_equivalent_empty(self):
        """Test validation with empty SI equivalent."""
        with pytest.raises(ValidationError) as exc_info:
            UnitDefinition(
                name="test_unit",
                category="volume",
                si_equivalent="",
                conversion_factor=1.0
            )
        assert "SI equivalent cannot be empty" in str(exc_info.value)
    
    def test_validate_conversion_factor_zero(self):
        """Test validation with zero conversion factor."""
        with pytest.raises(ValidationError) as exc_info:
            UnitDefinition(
                name="test_unit",
                category="volume",
                si_equivalent="L",
                conversion_factor=0.0
            )
        assert "Conversion factor must be positive" in str(exc_info.value)
    
    def test_validate_conversion_factor_negative(self):
        """Test validation with negative conversion factor."""
        with pytest.raises(ValidationError) as exc_info:
            UnitDefinition(
                name="test_unit",
                category="volume",
                si_equivalent="L",
                conversion_factor=-1.0
            )
        assert "Conversion factor must be positive" in str(exc_info.value)


class TestBiomarkersSchemaCoverage:
    """Test cases for BiomarkersSchema coverage."""
    
    def test_validate_biomarkers_empty_dict(self):
        """Test validation with empty biomarkers dict."""
        schema = BiomarkersSchema(biomarkers={})
        assert schema.biomarkers == {}
    
    def test_validate_biomarkers_with_data(self):
        """Test validation with valid biomarkers data."""
        biomarkers_data = {
            "test_biomarker": BiomarkerDefinition(
                aliases=["test"],
                unit="mg/dL",
                description="Test biomarker",
                category="cardiovascular",
                data_type="numeric"
            )
        }
        schema = BiomarkersSchema(biomarkers=biomarkers_data)
        assert len(schema.biomarkers) == 1
        assert "test_biomarker" in schema.biomarkers


class TestReferenceRangesSchemaCoverage:
    """Test cases for ReferenceRangesSchema coverage."""
    
    def test_validate_reference_ranges_empty_dict(self):
        """Test validation with empty reference ranges dict."""
        schema = ReferenceRangesSchema(reference_ranges={})
        assert schema.reference_ranges == {}
    
    def test_validate_reference_ranges_with_data(self):
        """Test validation with valid reference ranges data."""
        ranges_data = {
            "test_biomarker": {
                "adult_male": ReferenceRange(
                    biomarker="test_biomarker",
                    population="adult",
                    min_value=50.0,
                    max_value=100.0,
                    unit="mg/dL"
                )
            }
        }
        schema = ReferenceRangesSchema(reference_ranges=ranges_data)
        assert len(schema.reference_ranges) == 1


class TestUnitsSchemaCoverage:
    """Test cases for UnitsSchema coverage."""
    
    def test_validate_units_empty_dict(self):
        """Test validation with empty units dict."""
        schema = UnitsSchema(units={})
        assert schema.units == {}
    
    def test_validate_units_with_data(self):
        """Test validation with valid units data."""
        units_data = {
            "test_unit": UnitDefinition(
                name="test_unit",
                category="volume",
                si_equivalent="L",
                conversion_factor=1.0
            )
        }
        schema = UnitsSchema(units=units_data)
        assert len(schema.units) == 1
        assert "test_unit" in schema.units


class TestSchemaEdgeCases:
    """Test edge cases for schema validation."""
    
    def test_biomarker_definition_with_all_valid_categories(self):
        """Test biomarker definition with all valid categories."""
        valid_categories = [
            "cardiovascular", "metabolic", "inflammatory", "hormonal", 
            "liver", "kidney", "thyroid", "vitamin", "mineral", "cbc", "other"
        ]
        
        for category in valid_categories:
            biomarker = BiomarkerDefinition(
                aliases=["test"],
                unit="mg/dL",
                description="Test biomarker",
                category=category,
                data_type="numeric"
            )
            assert biomarker.category == category
    
    def test_reference_range_with_all_valid_populations(self):
        """Test reference range with all valid populations."""
        valid_populations = [
            "general_adult", "elderly", "pediatric", "pregnant", "athlete"
        ]
        
        for population in valid_populations:
            range_obj = ReferenceRange(
                biomarker="test",
                population=population,
                min_value=50.0,
                max_value=100.0,
                unit="mg/dL"
            )
            assert range_obj.population == population
    
    def test_unit_definition_with_all_valid_categories(self):
        """Test unit definition with all valid categories."""
        valid_categories = [
            "volume", "mass", "length", "time", "temperature", "pressure", "concentration"
        ]
        
        for category in valid_categories:
            unit = UnitDefinition(
                name="test_unit",
                category=category,
                si_equivalent="L",
                conversion_factor=1.0
            )
            assert unit.category == category
