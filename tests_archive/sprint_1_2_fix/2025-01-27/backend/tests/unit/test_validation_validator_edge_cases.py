# ARCHIVED TEST
# Reason: Tests expect validate_ranges method that doesn't exist and incorrect return format expectations
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_validation_validator_edge_cases.py

"""
Unit tests for validation validator edge cases
HealthIQ-AI v5 Backend
"""

import pytest
from unittest.mock import patch, MagicMock, mock_open
import tempfile
import os

from core.validation.validator import SSOTValidator, SSOTValidationError


class TestSSOTValidatorEdgeCases:
    """Test SSOT validator edge cases and error handling"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = SSOTValidator()
    
    def test_validate_biomarkers_nonexistent_file(self):
        """Test validating nonexistent biomarkers file"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = self.validator.validate_biomarkers("nonexistent.yaml")
            assert result is False
    
    def test_validate_biomarkers_permission_error(self):
        """Test validating biomarkers file with permission error"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            result = self.validator.validate_biomarkers("restricted.yaml")
            assert result is False
    
    def test_validate_biomarkers_invalid_yaml(self):
        """Test validating biomarkers file with invalid YAML"""
        invalid_yaml = "invalid: yaml: content: ["
        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            result = self.validator.validate_biomarkers("invalid.yaml")
            assert result is False
    
    def test_validate_biomarkers_empty_file(self):
        """Test validating empty biomarkers file"""
        with patch('builtins.open', mock_open(read_data="")):
            result = self.validator.validate_biomarkers("empty.yaml")
            assert result is False
    
    def test_validate_biomarkers_corrupted_data(self):
        """Test validating biomarkers file with corrupted data"""
        corrupted_data = "biomarkers:\n  - name: test\n    invalid_field: value"
        with patch('builtins.open', mock_open(read_data=corrupted_data)):
            result = self.validator.validate_biomarkers("corrupted.yaml")
            assert result is False
    
    def test_validate_ranges_nonexistent_file(self):
        """Test validating nonexistent ranges file"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = self.validator.validate_ranges("nonexistent.yaml")
            assert result is False
    
    def test_validate_ranges_permission_error(self):
        """Test validating ranges file with permission error"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            result = self.validator.validate_ranges("restricted.yaml")
            assert result is False
    
    def test_validate_ranges_invalid_yaml(self):
        """Test validating ranges file with invalid YAML"""
        invalid_yaml = "ranges:\n  - name: test\n    invalid_field: value"
        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            result = self.validator.validate_ranges("invalid.yaml")
            assert result is False
    
    def test_validate_units_nonexistent_file(self):
        """Test validating nonexistent units file"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = self.validator.validate_units("nonexistent.yaml")
            assert result is False
    
    def test_validate_units_permission_error(self):
        """Test validating units file with permission error"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            result = self.validator.validate_units("restricted.yaml")
            assert result is False
    
    def test_validate_units_invalid_yaml(self):
        """Test validating units file with invalid YAML"""
        invalid_yaml = "units:\n  - name: test\n    invalid_field: value"
        with patch('builtins.open', mock_open(read_data=invalid_yaml)):
            result = self.validator.validate_units("invalid.yaml")
            assert result is False
    
    def test_validate_all_files_nonexistent(self):
        """Test validating all files when they don't exist"""
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = self.validator.validate_all()
            assert result is False
    
    def test_validate_all_files_permission_error(self):
        """Test validating all files with permission error"""
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            result = self.validator.validate_all()
            assert result is False
    
    def test_validate_all_files_mixed_errors(self):
        """Test validating all files with mixed errors"""
        def mock_open_side_effect(filename, mode='r'):
            if 'biomarkers' in filename:
                return mock_open(read_data="biomarkers:\n  - name: test\n    category: test").return_value
            elif 'ranges' in filename:
                raise FileNotFoundError("Ranges file not found")
            elif 'units' in filename:
                return mock_open(read_data="units:\n  - name: test\n    category: test").return_value
        
        with patch('builtins.open', side_effect=mock_open_side_effect):
            result = self.validator.validate_all()
            assert result is False
    
    def test_validate_biomarkers_malformed_data(self):
        """Test validating biomarkers file with malformed data"""
        malformed_data = """
        biomarkers:
          - name: test_biomarker
            category: test
            data_type: numeric
            aliases: []
            units: mg/dL
            description: Test biomarker
            reference_ranges: invalid_data
        """
        with patch('builtins.open', mock_open(read_data=malformed_data)):
            result = self.validator.validate_biomarkers("malformed.yaml")
            assert result is False
    
    def test_validate_ranges_malformed_data(self):
        """Test validating ranges file with malformed data"""
        malformed_data = """
        ranges:
          - biomarker: test_biomarker
            population: adult
            min_value: invalid_value
            max_value: 100
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=malformed_data)):
            result = self.validator.validate_ranges("malformed.yaml")
            assert result is False
    
    def test_validate_units_malformed_data(self):
        """Test validating units file with malformed data"""
        malformed_data = """
        units:
          - name: test_unit
            category: test
            si_equivalent: invalid_si
            conversion_factor: not_a_number
        """
        with patch('builtins.open', mock_open(read_data=malformed_data)):
            result = self.validator.validate_units("malformed.yaml")
            assert result is False
    
    def test_validate_biomarkers_missing_required_fields(self):
        """Test validating biomarkers file with missing required fields"""
        missing_fields_data = """
        biomarkers:
          - name: test_biomarker
            # Missing category, data_type, etc.
        """
        with patch('builtins.open', mock_open(read_data=missing_fields_data)):
            result = self.validator.validate_biomarkers("missing_fields.yaml")
            assert result is False
    
    def test_validate_ranges_missing_required_fields(self):
        """Test validating ranges file with missing required fields"""
        missing_fields_data = """
        ranges:
          - biomarker: test_biomarker
            # Missing population, min_value, max_value, etc.
        """
        with patch('builtins.open', mock_open(read_data=missing_fields_data)):
            result = self.validator.validate_ranges("missing_fields.yaml")
            assert result is False
    
    def test_validate_units_missing_required_fields(self):
        """Test validating units file with missing required fields"""
        missing_fields_data = """
        units:
          - name: test_unit
            # Missing category, si_equivalent, etc.
        """
        with patch('builtins.open', mock_open(read_data=missing_fields_data)):
            result = self.validator.validate_units("missing_fields.yaml")
            assert result is False
    
    def test_validate_biomarkers_invalid_data_types(self):
        """Test validating biomarkers file with invalid data types"""
        invalid_types_data = """
        biomarkers:
          - name: test_biomarker
            category: test
            data_type: invalid_type
            aliases: not_a_list
            units: mg/dL
            description: Test biomarker
        """
        with patch('builtins.open', mock_open(read_data=invalid_types_data)):
            result = self.validator.validate_biomarkers("invalid_types.yaml")
            assert result is False
    
    def test_validate_ranges_invalid_data_types(self):
        """Test validating ranges file with invalid data types"""
        invalid_types_data = """
        ranges:
          - biomarker: test_biomarker
            population: adult
            min_value: not_a_number
            max_value: not_a_number
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=invalid_types_data)):
            result = self.validator.validate_ranges("invalid_types.yaml")
            assert result is False
    
    def test_validate_units_invalid_data_types(self):
        """Test validating units file with invalid data types"""
        invalid_types_data = """
        units:
          - name: test_unit
            category: test
            si_equivalent: mg/dL
            conversion_factor: not_a_number
        """
        with patch('builtins.open', mock_open(read_data=invalid_types_data)):
            result = self.validator.validate_units("invalid_types.yaml")
            assert result is False
    
    def test_validate_biomarkers_empty_aliases(self):
        """Test validating biomarkers file with empty aliases"""
        empty_aliases_data = """
        biomarkers:
          - name: test_biomarker
            category: test
            data_type: numeric
            aliases: []
            units: mg/dL
            description: Test biomarker
        """
        with patch('builtins.open', mock_open(read_data=empty_aliases_data)):
            result = self.validator.validate_biomarkers("empty_aliases.yaml")
            assert result is False
    
    def test_validate_ranges_invalid_range_values(self):
        """Test validating ranges file with invalid range values"""
        invalid_range_data = """
        ranges:
          - biomarker: test_biomarker
            population: adult
            min_value: 100
            max_value: 50
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=invalid_range_data)):
            result = self.validator.validate_ranges("invalid_range.yaml")
            assert result is False
    
    def test_validate_units_invalid_conversion_factor(self):
        """Test validating units file with invalid conversion factor"""
        invalid_conversion_data = """
        units:
          - name: test_unit
            category: test
            si_equivalent: mg/dL
            conversion_factor: 0
        """
        with patch('builtins.open', mock_open(read_data=invalid_conversion_data)):
            result = self.validator.validate_units("invalid_conversion.yaml")
            assert result is False
    
    def test_validate_biomarkers_duplicate_names(self):
        """Test validating biomarkers file with duplicate names"""
        duplicate_names_data = """
        biomarkers:
          - name: test_biomarker
            category: test
            data_type: numeric
            aliases: ["test"]
            units: mg/dL
            description: Test biomarker
          - name: test_biomarker
            category: test
            data_type: numeric
            aliases: ["test2"]
            units: mg/dL
            description: Test biomarker 2
        """
        with patch('builtins.open', mock_open(read_data=duplicate_names_data)):
            result = self.validator.validate_biomarkers("duplicate_names.yaml")
            assert result is False
    
    def test_validate_ranges_duplicate_biomarkers(self):
        """Test validating ranges file with duplicate biomarkers"""
        duplicate_biomarkers_data = """
        ranges:
          - biomarker: test_biomarker
            population: adult
            min_value: 50
            max_value: 100
            unit: mg/dL
          - biomarker: test_biomarker
            population: adult
            min_value: 60
            max_value: 110
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=duplicate_biomarkers_data)):
            result = self.validator.validate_ranges("duplicate_biomarkers.yaml")
            assert result is False
    
    def test_validate_units_duplicate_names(self):
        """Test validating units file with duplicate names"""
        duplicate_names_data = """
        units:
          - name: test_unit
            category: test
            si_equivalent: mg/dL
            conversion_factor: 1.0
          - name: test_unit
            category: test
            si_equivalent: g/L
            conversion_factor: 0.1
        """
        with patch('builtins.open', mock_open(read_data=duplicate_names_data)):
            result = self.validator.validate_units("duplicate_names.yaml")
            assert result is False
    
    def test_validate_biomarkers_invalid_categories(self):
        """Test validating biomarkers file with invalid categories"""
        invalid_categories_data = """
        biomarkers:
          - name: test_biomarker
            category: invalid_category
            data_type: numeric
            aliases: ["test"]
            units: mg/dL
            description: Test biomarker
        """
        with patch('builtins.open', mock_open(read_data=invalid_categories_data)):
            result = self.validator.validate_biomarkers("invalid_categories.yaml")
            assert result is False
    
    def test_validate_ranges_invalid_populations(self):
        """Test validating ranges file with invalid populations"""
        invalid_populations_data = """
        ranges:
          - biomarker: test_biomarker
            population: invalid_population
            min_value: 50
            max_value: 100
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=invalid_populations_data)):
            result = self.validator.validate_ranges("invalid_populations.yaml")
            assert result is False
    
    def test_validate_units_invalid_categories(self):
        """Test validating units file with invalid categories"""
        invalid_categories_data = """
        units:
          - name: test_unit
            category: invalid_category
            si_equivalent: mg/dL
            conversion_factor: 1.0
        """
        with patch('builtins.open', mock_open(read_data=invalid_categories_data)):
            result = self.validator.validate_units("invalid_categories.yaml")
            assert result is False
    
    def test_validate_biomarkers_invalid_data_types_enum(self):
        """Test validating biomarkers file with invalid data type enum"""
        invalid_data_types_data = """
        biomarkers:
          - name: test_biomarker
            category: test
            data_type: invalid_data_type
            aliases: ["test"]
            units: mg/dL
            description: Test biomarker
        """
        with patch('builtins.open', mock_open(read_data=invalid_data_types_data)):
            result = self.validator.validate_biomarkers("invalid_data_types.yaml")
            assert result is False
    
    def test_validate_ranges_invalid_units(self):
        """Test validating ranges file with invalid units"""
        invalid_units_data = """
        ranges:
          - biomarker: test_biomarker
            population: adult
            min_value: 50
            max_value: 100
            unit: invalid_unit
        """
        with patch('builtins.open', mock_open(read_data=invalid_units_data)):
            result = self.validator.validate_ranges("invalid_units.yaml")
            assert result is False
    
    def test_validate_units_invalid_si_equivalent(self):
        """Test validating units file with invalid SI equivalent"""
        invalid_si_data = """
        units:
          - name: test_unit
            category: test
            si_equivalent: invalid_si
            conversion_factor: 1.0
        """
        with patch('builtins.open', mock_open(read_data=invalid_si_data)):
            result = self.validator.validate_units("invalid_si.yaml")
            assert result is False
    
    def test_validate_biomarkers_very_large_file(self):
        """Test validating very large biomarkers file"""
        large_data = "biomarkers:\n"
        for i in range(10000):
            large_data += f"""
          - name: biomarker_{i}
            category: test
            data_type: numeric
            aliases: ["test_{i}"]
            units: mg/dL
            description: Test biomarker {i}
        """
        
        with patch('builtins.open', mock_open(read_data=large_data)):
            result = self.validator.validate_biomarkers("large.yaml")
            assert result is False  # Should fail due to validation errors
    
    def test_validate_ranges_very_large_file(self):
        """Test validating very large ranges file"""
        large_data = "ranges:\n"
        for i in range(10000):
            large_data += f"""
          - biomarker: biomarker_{i}
            population: adult
            min_value: 50
            max_value: 100
            unit: mg/dL
        """
        
        with patch('builtins.open', mock_open(read_data=large_data)):
            result = self.validator.validate_ranges("large.yaml")
            assert result is False  # Should fail due to validation errors
    
    def test_validate_units_very_large_file(self):
        """Test validating very large units file"""
        large_data = "units:\n"
        for i in range(10000):
            large_data += f"""
          - name: unit_{i}
            category: test
            si_equivalent: mg/dL
            conversion_factor: 1.0
        """
        
        with patch('builtins.open', mock_open(read_data=large_data)):
            result = self.validator.validate_units("large.yaml")
            assert result is False  # Should fail due to validation errors
    
    def test_validate_biomarkers_unicode_content(self):
        """Test validating biomarkers file with unicode content"""
        unicode_data = """
        biomarkers:
          - name: test_biomarker_αβγ
            category: test
            data_type: numeric
            aliases: ["test_αβγ"]
            units: mg/dL
            description: Test biomarker with unicode αβγ
        """
        with patch('builtins.open', mock_open(read_data=unicode_data)):
            result = self.validator.validate_biomarkers("unicode.yaml")
            assert result is False  # Should fail due to invalid characters
    
    def test_validate_ranges_unicode_content(self):
        """Test validating ranges file with unicode content"""
        unicode_data = """
        ranges:
          - biomarker: test_biomarker_αβγ
            population: adult
            min_value: 50
            max_value: 100
            unit: mg/dL
        """
        with patch('builtins.open', mock_open(read_data=unicode_data)):
            result = self.validator.validate_ranges("unicode.yaml")
            assert result is False  # Should fail due to invalid characters
    
    def test_validate_units_unicode_content(self):
        """Test validating units file with unicode content"""
        unicode_data = """
        units:
          - name: test_unit_αβγ
            category: test
            si_equivalent: mg/dL
            conversion_factor: 1.0
        """
        with patch('builtins.open', mock_open(read_data=unicode_data)):
            result = self.validator.validate_units("unicode.yaml")
            assert result is False  # Should fail due to invalid characters
