"""
Test Strict Validation Mode

This module tests the strict validation mode functionality.
"""

import pytest
import os
from core.context import ContextFactory


class TestStrictValidation:
    """Test strict validation mode functionality."""

    def test_strict_validation_mode_enabled(self):
        """
        Test that strict validation mode fails on first invalid biomarker.
        
        Business Value: Ensures strict mode provides immediate feedback on data quality issues.
        Failure Impact: Without strict mode, data quality issues could be silently ignored.
        """
        # Create factory with strict validation enabled
        factory = ContextFactory(strict_validation=True)
        
        # Test payload with invalid biomarker
        invalid_payload = {
            'biomarkers': {
                'glucose': {
                    'value': 'high',  # Invalid value
                    'unit': 'mg/dL'
                },
                'cholesterol': {
                    'value': 180.0,  # Valid value
                    'unit': 'mg/dL'
                }
            },
            'user': {
                'user_id': 'test_user',
                'sex': 'male',
                'chronological_age': 35,
                'height_cm': 175.0,
                'weight_kg': 75.0
            }
        }
        
        # Should fail on first invalid biomarker
        with pytest.raises(Exception) as exc_info:
            factory.create_context(invalid_payload)
        
        # Check that error message indicates strict validation failure
        assert "Strict validation failed" in str(exc_info.value)
        assert "glucose" in str(exc_info.value)

    def test_normal_validation_mode_skips_invalid(self):
        """
        Test that normal validation mode skips invalid biomarkers.
        
        Business Value: Ensures normal mode provides resilient processing.
        Failure Impact: Without normal mode, any invalid data would break the entire process.
        """
        # Create factory with normal validation (default)
        factory = ContextFactory(strict_validation=False)
        
        # Test payload with invalid biomarker
        invalid_payload = {
            'biomarkers': {
                'glucose': {
                    'value': 'high',  # Invalid value
                    'unit': 'mg/dL'
                },
                'cholesterol': {
                    'value': 180.0,  # Valid value
                    'unit': 'mg/dL'
                }
            },
            'user': {
                'user_id': 'test_user',
                'sex': 'male',
                'chronological_age': 35,
                'height_cm': 175.0,
                'weight_kg': 75.0
            }
        }
        
        # Should succeed with only valid biomarkers
        context = factory.create_context(invalid_payload)
        
        # Should only have the valid biomarker
        assert len(context.biomarkers) == 1
        assert 'cholesterol' in context.biomarkers
        assert 'glucose' not in context.biomarkers

    def test_strict_validation_environment_variable(self):
        """
        Test that strict validation can be controlled via environment variable.
        
        Business Value: Ensures configuration can be controlled without code changes.
        Failure Impact: Without environment control, configuration would be hardcoded.
        """
        # Set environment variable
        os.environ['STRICT_VALIDATION'] = 'true'
        
        try:
            # Create factory without explicit strict_validation parameter
            factory = ContextFactory()
            
            # Should be in strict mode
            assert factory.strict_validation is True
            
            # Test with invalid payload
            invalid_payload = {
                'biomarkers': {
                    'glucose': {
                        'value': 'high',
                        'unit': 'mg/dL'
                    }
                },
                'user': {
                    'user_id': 'test_user',
                    'sex': 'male',
                    'chronological_age': 35,
                    'height_cm': 175.0,
                    'weight_kg': 75.0
                }
            }
            
            # Should fail in strict mode
            with pytest.raises(Exception) as exc_info:
                factory.create_context(invalid_payload)
            
            assert "Strict validation failed" in str(exc_info.value)
            
        finally:
            # Clean up environment variable
            if 'STRICT_VALIDATION' in os.environ:
                del os.environ['STRICT_VALIDATION']

    def test_strict_validation_explicit_override(self):
        """
        Test that explicit strict_validation parameter overrides environment variable.
        
        Business Value: Ensures explicit configuration takes precedence.
        Failure Impact: Without precedence rules, configuration could be unpredictable.
        """
        # Set environment variable to false
        os.environ['STRICT_VALIDATION'] = 'false'
        
        try:
            # Create factory with explicit strict_validation=True
            factory = ContextFactory(strict_validation=True)
            
            # Should be in strict mode despite environment variable
            assert factory.strict_validation is True
            
        finally:
            # Clean up environment variable
            if 'STRICT_VALIDATION' in os.environ:
                del os.environ['STRICT_VALIDATION']

    def test_strict_validation_panel_mode(self):
        """
        Test strict validation mode with panel-based payloads.
        
        Business Value: Ensures strict mode works with both legacy and panel formats.
        Failure Impact: Inconsistent behavior between formats would be confusing.
        """
        # Create factory with strict validation enabled
        factory = ContextFactory(strict_validation=True)
        
        # Test panel payload with invalid biomarker
        panel_payload = {
            'panel_name': 'Test Panel',
            'panel_type': 'metabolic',
            'biomarkers': {
                'glucose': {
                    'value': 'high',  # Invalid value
                    'unit': 'mg/dL'
                },
                'cholesterol': {
                    'value': 180.0,  # Valid value
                    'unit': 'mg/dL'
                }
            },
            'user': {
                'user_id': 'test_user',
                'sex': 'male',
                'chronological_age': 35,
                'height_cm': 175.0,
                'weight_kg': 75.0
            }
        }
        
        # Should fail on first invalid biomarker
        with pytest.raises(Exception) as exc_info:
            factory.create_context(panel_payload)
        
        # Check that error message indicates strict validation failure
        assert "Strict validation failed" in str(exc_info.value)
        assert "glucose" in str(exc_info.value)

    def test_strict_validation_all_valid_biomarkers(self):
        """
        Test that strict validation mode works correctly with all valid biomarkers.
        
        Business Value: Ensures strict mode doesn't break valid data processing.
        Failure Impact: Strict mode would be unusable if it broke valid data.
        """
        # Create factory with strict validation enabled
        factory = ContextFactory(strict_validation=True)
        
        # Test payload with all valid biomarkers
        valid_payload = {
            'biomarkers': {
                'glucose': {
                    'value': 95.5,
                    'unit': 'mg/dL'
                },
                'cholesterol': {
                    'value': 180.0,
                    'unit': 'mg/dL'
                }
            },
            'user': {
                'user_id': 'test_user',
                'sex': 'male',
                'chronological_age': 35,
                'height_cm': 175.0,
                'weight_kg': 75.0
            }
        }
        
        # Should succeed with all valid biomarkers
        context = factory.create_context(valid_payload)
        
        # Should have both biomarkers
        assert len(context.biomarkers) == 2
        assert 'glucose' in context.biomarkers
        assert 'cholesterol' in context.biomarkers
