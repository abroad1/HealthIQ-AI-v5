"""
Test ContextFactory Phase 1 Restorations

This module tests the Phase 1 restorations that bring critical v4 ContextFactory
functionality into the v5 implementation, including:

- ScoringMetrics support
- BiomarkerPanel creation
- Reference range validation
- Decimal parsing
- Enhanced logging
"""

import pytest
from decimal import Decimal
from datetime import datetime

from core.context import ContextFactory, AnalysisContext, BiomarkerPanel, ScoringMetrics, Sex


class TestContextFactoryPhase1:
    """Test Phase 1 restorations for ContextFactory."""

    def test_create_scoring_metrics(self):
        """
        Test ScoringMetrics creation with proper decimal conversion.
        
        Business Value: Ensures scoring data is properly validated and converted.
        Failure Impact: Invalid scoring data would cause analysis failures.
        """
        factory = ContextFactory()
        
        # Test valid scoring data
        raw_scoring_data = {
            'raw_scores': {
                'glucose': 95.5,
                'cholesterol': 180.0,
                'hdl': 45.2
            },
            'weighted_scores': {
                'glucose': 0.85,
                'cholesterol': 0.72,
                'hdl': 0.91
            },
            'cluster_scores': {
                'metabolic': 0.78,
                'cardiovascular': 0.82
            },
            'confidence_scores': {
                'overall': 0.88,
                'metabolic': 0.85
            },
            'risk_factors': ['high_cholesterol', 'sedentary_lifestyle'],
            'metadata': {
                'algorithm_version': '2.1',
                'computation_time': 1.23
            }
        }
        
        scoring_metrics = factory._create_scoring_metrics(raw_scoring_data)
        
        assert isinstance(scoring_metrics, ScoringMetrics)
        assert len(scoring_metrics.raw_scores) == 3
        assert scoring_metrics.raw_scores['glucose'] == 95.5
        assert scoring_metrics.raw_scores['cholesterol'] == 180.0
        assert scoring_metrics.raw_scores['hdl'] == 45.2
        
        assert len(scoring_metrics.weighted_scores) == 3
        assert scoring_metrics.weighted_scores['glucose'] == 0.85
        
        assert len(scoring_metrics.cluster_scores) == 2
        assert scoring_metrics.cluster_scores['metabolic'] == 0.78
        
        assert len(scoring_metrics.confidence_scores) == 2
        assert scoring_metrics.confidence_scores['overall'] == 0.88
        
        assert scoring_metrics.risk_factors == ['high_cholesterol', 'sedentary_lifestyle']
        assert scoring_metrics.metadata['algorithm_version'] == '2.1'
        assert isinstance(scoring_metrics.computed_at, datetime)

    def test_create_biomarker_panel(self):
        """
        Test BiomarkerPanel creation with metadata.
        
        Business Value: Ensures panel data is properly structured with metadata.
        Failure Impact: Missing panel metadata would cause analysis issues.
        """
        factory = ContextFactory()
        
        # Test valid panel data
        raw_panel_data = {
            'name': 'Comprehensive Metabolic Panel',
            'panel_type': 'metabolic',
            'collected_at': '2024-01-15T10:30:00Z',
            'laboratory': 'LabCorp',
            'notes': 'Fasting blood draw',
            'biomarkers': {
                'glucose': {
                    'value': 95.5,
                    'unit': 'mg/dL',
                    'reference_range': {
                        'min': 70,
                        'max': 100,
                        'interpretation': 'normal'
                    }
                },
                'cholesterol': {
                    'value': 180.0,
                    'unit': 'mg/dL',
                    'reference_range': {
                        'min': 0,
                        'max': 200,
                        'interpretation': 'normal'
                    }
                }
            }
        }
        
        panel = factory._create_biomarker_panel(raw_panel_data)
        
        assert isinstance(panel, BiomarkerPanel)
        assert panel.name == 'Comprehensive Metabolic Panel'
        assert panel.panel_type == 'metabolic'
        assert panel.laboratory == 'LabCorp'
        assert panel.notes == 'Fasting blood draw'
        assert isinstance(panel.collected_at, datetime)
        
        assert len(panel.biomarkers) == 2
        assert 'glucose' in panel.biomarkers
        assert 'cholesterol' in panel.biomarkers
        
        # Check biomarker values
        glucose = panel.biomarkers['glucose']
        assert glucose.value == 95.5
        assert glucose.unit == 'mg/dL'
        assert glucose.reference_range['min'] == 70.0
        assert glucose.reference_range['max'] == 100.0

    def test_validate_reference_range(self):
        """
        Test reference range validation.
        
        Business Value: Ensures reference ranges are properly validated.
        Failure Impact: Invalid reference ranges would cause incorrect analysis.
        """
        factory = ContextFactory()
        
        # Test valid reference range
        valid_range = {
            'min': 70,
            'max': 100,
            'interpretation': 'normal'
        }
        
        validated_range = factory._validate_reference_range(valid_range)
        
        assert validated_range['min'] == 70.0
        assert validated_range['max'] == 100.0
        assert validated_range['interpretation'] == 'normal'
        
        # Test invalid reference range (min >= max)
        invalid_range = {
            'min': 100,
            'max': 70,
            'interpretation': 'normal'
        }
        
        with pytest.raises(Exception) as exc_info:
            factory._validate_reference_range(invalid_range)
        
        assert "Reference range min must be less than max" in str(exc_info.value)
        
        # Test missing required keys
        incomplete_range = {
            'min': 70,
            'max': 100
        }
        
        with pytest.raises(Exception) as exc_info:
            factory._validate_reference_range(incomplete_range)
        
        assert "Reference range must contain 'min', 'max', and 'interpretation' keys" in str(exc_info.value)

    def test_parse_decimal(self):
        """
        Test decimal parsing with various input types.
        
        Business Value: Ensures numeric values are properly converted to Decimal.
        Failure Impact: Incorrect numeric conversion would cause calculation errors.
        """
        factory = ContextFactory()
        
        # Test various input types
        assert factory._parse_decimal(95.5) == 95.5
        assert factory._parse_decimal(100) == 100.0
        assert factory._parse_decimal('95.5') == 95.5
        assert factory._parse_decimal('1000.50') == 1000.50
        assert factory._parse_decimal(Decimal('95.5')) == 95.5
        
        # Test invalid inputs
        with pytest.raises(Exception) as exc_info:
            factory._parse_decimal('invalid')
        
        assert "Invalid numeric value for biomarker" in str(exc_info.value)
        
        with pytest.raises(Exception) as exc_info:
            factory._parse_decimal('1,000.50')  # Commas not supported
        
        assert "Invalid numeric value for biomarker" in str(exc_info.value)
        
        with pytest.raises(Exception) as exc_info:
            factory._parse_decimal(None)
        
        assert "Invalid numeric value for biomarker" in str(exc_info.value)

    def test_create_context_with_panel(self):
        """
        Test creating context with panel-based payload.
        
        Business Value: Ensures panel-based payloads are properly handled.
        Failure Impact: Panel-based analysis would fail without proper support.
        """
        factory = ContextFactory()
        
        # Test panel-based payload
        panel_payload = {
            'panel_name': 'Metabolic Panel',
            'panel_type': 'metabolic',
            'collected_at': '2024-01-15T10:30:00Z',
            'laboratory': 'LabCorp',
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
        
        context = factory.create_context(panel_payload)
        
        assert isinstance(context, AnalysisContext)
        assert context.biomarker_panel is not None
        assert context.biomarkers is None  # Should be None for panel-based
        assert context.user.user_id == 'test_user'
        
        panel = context.biomarker_panel
        assert panel.name == 'Metabolic Panel'
        assert panel.panel_type == 'metabolic'
        assert panel.laboratory == 'LabCorp'
        assert len(panel.biomarkers) == 2

    def test_create_context_with_scoring_metrics(self):
        """
        Test creating context with scoring metrics.
        
        Business Value: Ensures scoring metrics are properly integrated.
        Failure Impact: Analysis results would lack scoring data.
        """
        factory = ContextFactory()
        
        # Test payload with scoring metrics
        payload = {
            'biomarkers': {
                'glucose': {
                    'value': 95.5,
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
        
        scoring_metrics = {
            'raw_scores': {
                'glucose': 95.5,
                'overall': 0.85
            },
            'weighted_scores': {
                'glucose': 0.88,
                'overall': 0.82
            },
            'risk_factors': ['high_glucose'],
            'metadata': {
                'algorithm_version': '2.1'
            }
        }
        
        context = factory.create_context(payload, scoring_metrics=scoring_metrics)
        
        assert isinstance(context, AnalysisContext)
        assert context.scoring_metrics is not None
        
        metrics = context.scoring_metrics
        assert metrics.raw_scores['glucose'] == 95.5
        assert metrics.weighted_scores['glucose'] == 0.88
        assert metrics.risk_factors == ['high_glucose']
        assert metrics.metadata['algorithm_version'] == '2.1'

    def test_create_context_with_requirements_validation(self):
        """
        Test creating context with requirements validation.
        
        Business Value: Ensures analysis requirements are properly validated.
        Failure Impact: Invalid analysis requirements would cause failures.
        """
        factory = ContextFactory()
        
        # Test payload
        payload = {
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
        
        # Test valid requirements
        valid_requirements = {
            'min_biomarkers': 2,
            'required_biomarkers': ['glucose', 'cholesterol'],
            'min_age': 18,
            'max_age': 65
        }
        
        context = factory.create_context(payload, validate_requirements=valid_requirements)
        assert isinstance(context, AnalysisContext)
        
        # Test invalid requirements (missing required biomarker)
        invalid_requirements = {
            'min_biomarkers': 2,
            'required_biomarkers': ['glucose', 'cholesterol', 'hdl'],
            'min_age': 18,
            'max_age': 65
        }
        
        with pytest.raises(Exception) as exc_info:
            factory.create_context(payload, validate_requirements=invalid_requirements)
        
        assert "Missing required biomarkers" in str(exc_info.value)

    def test_backward_compatibility(self):
        """
        Test that legacy payload format still works.
        
        Business Value: Ensures existing integrations continue to work.
        Failure Impact: Breaking changes would cause system failures.
        """
        factory = ContextFactory()
        
        # Test legacy payload format
        legacy_payload = {
            'biomarkers': {
                'glucose': {
                    'value': 95.5,
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
        
        context = factory.create_context(legacy_payload)
        
        assert isinstance(context, AnalysisContext)
        assert context.biomarkers is not None  # Should use legacy structure
        assert context.biomarker_panel is None  # Should be None for legacy
        assert len(context.biomarkers) == 1
        assert 'glucose' in context.biomarkers
