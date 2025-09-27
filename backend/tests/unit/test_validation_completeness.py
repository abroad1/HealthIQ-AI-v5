"""
High-value tests for data completeness validation.

These tests focus on business-critical functionality for biomarker completeness assessment,
ensuring the system correctly identifies missing data and provides accurate scoring.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from core.validation.completeness import (
    DataCompletenessValidator, 
    CompletenessResult, 
    HealthSystem
)


class TestDataCompletenessValidator:
    """Test data completeness validation functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.validator = DataCompletenessValidator()
    
    def test_complete_biomarker_panel_assessment(self):
        """
        Test completeness assessment with a complete biomarker panel.
        
        Business Value: Ensures users with complete data get accurate analysis readiness.
        """
        # Complete biomarker panel
        complete_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "insulin": 8.5,
            "total_cholesterol": 180.0,
            "ldl_cholesterol": 110.0,
            "hdl_cholesterol": 55.0,
            "triglycerides": 120.0,
            "crp": 1.2,
            "creatinine": 0.9,
            "bun": 15.0,
            "alt": 25.0,
            "ast": 30.0,
            "hemoglobin": 14.5,
            "hematocrit": 42.0,
            "white_blood_cells": 7.2,
            "platelets": 280.0
        }
        
        result = self.validator.assess_completeness(complete_biomarkers)
        
        # Assertions for complete panel
        assert result.overall_score >= 80.0, "Complete panel should have high score"
        assert result.analysis_ready is True, "Complete panel should be ready for analysis"
        assert result.confidence_level in ["high", "medium"], "Complete panel should have good confidence"
        assert len(result.missing_critical) == 0, "Complete panel should have no critical gaps"
        assert len(result.recommendations) > 0, "Should provide recommendations even for complete data"
    
    def test_incomplete_biomarker_panel_assessment(self):
        """
        Test completeness assessment with incomplete biomarker panel.
        
        Business Value: Ensures users with incomplete data get accurate gap identification.
        """
        # Incomplete biomarker panel - missing critical biomarkers
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        result = self.validator.assess_completeness(incomplete_biomarkers)
        
        # Assertions for incomplete panel
        assert result.overall_score < 80.0, "Incomplete panel should have lower score"
        assert result.analysis_ready is False, "Incomplete panel should not be ready for analysis"
        assert result.confidence_level == "low", "Incomplete panel should have low confidence"
        assert len(result.missing_critical) > 0, "Incomplete panel should have critical gaps"
        assert "hba1c" in result.missing_critical, "Should identify missing hba1c as critical"
        assert "ldl_cholesterol" in result.missing_critical, "Should identify missing LDL as critical"
    
    def test_health_system_scoring_accuracy(self):
        """
        Test health system scoring accuracy.
        
        Business Value: Ensures accurate health system coverage assessment for clinical decisions.
        """
        # Biomarkers for specific health systems
        metabolic_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "insulin": 8.5
        }
        
        result = self.validator.assess_completeness(metabolic_biomarkers)
        
        # Check metabolic system scoring
        metabolic_score = result.health_system_scores.get(HealthSystem.METABOLIC, 0.0)
        assert metabolic_score >= 90.0, "Complete metabolic panel should have high score"
        
        # Check other systems have lower scores
        cardiovascular_score = result.health_system_scores.get(HealthSystem.CARDIOVASCULAR, 0.0)
        assert cardiovascular_score < 50.0, "Missing cardiovascular biomarkers should have low score"
    
    def test_critical_vs_optional_biomarker_classification(self):
        """
        Test correct classification of critical vs optional biomarkers.
        
        Business Value: Ensures proper prioritization of biomarker importance for clinical decisions.
        """
        # Panel with only critical biomarkers
        critical_only_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 180.0,
            "ldl_cholesterol": 110.0,
            "crp": 1.2,
            "creatinine": 0.9,
            "alt": 25.0,
            "hemoglobin": 14.5
        }
        
        result = self.validator.assess_completeness(critical_only_biomarkers)
        
        # Should have no critical gaps but some optional gaps
        assert len(result.missing_critical) == 0, "Critical-only panel should have no critical gaps"
        assert len(result.missing_optional) > 0, "Critical-only panel should have optional gaps"
        assert "insulin" in result.missing_optional, "Insulin should be classified as optional"
        assert "hdl_cholesterol" in result.missing_optional, "HDL should be classified as optional"
    
    def test_confidence_level_calculation(self):
        """
        Test confidence level calculation based on completeness.
        
        Business Value: Ensures accurate confidence assessment for analysis reliability.
        """
        # High completeness panel
        high_completeness = {
            "glucose": 95.0, "hba1c": 5.2, "insulin": 8.5,
            "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0,
            "crp": 1.2, "creatinine": 0.9, "alt": 25.0, "hemoglobin": 14.5
        }
        
        result = self.validator.assess_completeness(high_completeness)
        assert result.confidence_level in ["high", "medium"], "High completeness should have good confidence"
        
        # Low completeness panel
        low_completeness = {"glucose": 95.0}
        result = self.validator.assess_completeness(low_completeness)
        assert result.confidence_level == "low", "Low completeness should have low confidence"
    
    def test_recommendation_generation(self):
        """
        Test recommendation generation for incomplete data.
        
        Business Value: Ensures users get actionable guidance for improving their data.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.validator.assess_completeness(incomplete_biomarkers)
        
        # Should generate recommendations
        assert len(result.recommendations) > 0, "Should generate recommendations for incomplete data"
        
        # Check recommendation content
        recommendation_text = " ".join(result.recommendations)
        assert "critical" in recommendation_text.lower() or "add" in recommendation_text.lower(), \
            "Recommendations should suggest adding biomarkers"
    
    def test_empty_biomarker_panel_handling(self):
        """
        Test handling of empty biomarker panel.
        
        Business Value: Ensures system gracefully handles edge cases without crashing.
        """
        empty_biomarkers = {}
        
        result = self.validator.assess_completeness(empty_biomarkers)
        
        # Should handle empty panel gracefully
        assert result.overall_score == 0.0, "Empty panel should have zero score"
        assert result.analysis_ready is False, "Empty panel should not be ready for analysis"
        assert result.confidence_level == "low", "Empty panel should have low confidence"
        assert len(result.missing_critical) > 0, "Empty panel should have many critical gaps"
    
    def test_health_system_requirements_retrieval(self):
        """
        Test retrieval of health system requirements.
        
        Business Value: Ensures system provides accurate requirements for clinical planning.
        """
        requirements = self.validator.get_health_system_requirements()
        
        # Should have requirements for all health systems
        assert len(requirements) == len(HealthSystem), "Should have requirements for all health systems"
        
        # Check specific system requirements
        metabolic_req = requirements[HealthSystem.METABOLIC]
        assert "critical_biomarkers" in metabolic_req, "Should have critical biomarkers defined"
        assert "optional_biomarkers" in metabolic_req, "Should have optional biomarkers defined"
        assert "glucose" in metabolic_req["critical_biomarkers"], "Glucose should be critical for metabolic"
        assert "insulin" in metabolic_req["optional_biomarkers"], "Insulin should be optional for metabolic"
    
    def test_biomarker_normalization_integration(self):
        """
        Test integration with biomarker normalization.
        
        Business Value: Ensures system works with canonical biomarker names and aliases.
        """
        # Test with aliases (should be normalized)
        biomarkers_with_aliases = {
            "blood_sugar": 95.0,  # alias for glucose
            "cholesterol": 180.0,  # alias for total_cholesterol
            "hgb": 14.5  # alias for hemoglobin
        }
        
        # Mock the normalizer to return canonical names
        with patch.object(self.validator.normalizer, 'normalize_biomarkers') as mock_normalize:
            mock_normalize.return_value = (
                Mock(biomarkers={"glucose": 95.0, "total_cholesterol": 180.0, "hemoglobin": 14.5}),
                []
            )
            
            result = self.validator.assess_completeness(biomarkers_with_aliases)
            
            # Should process normalized biomarkers
            assert result.overall_score > 0, "Should process normalized biomarkers"
            mock_normalize.assert_called_once_with(biomarkers_with_aliases)
    
    def test_edge_case_biomarker_values(self):
        """
        Test handling of edge case biomarker values.
        
        Business Value: Ensures system handles unusual but valid biomarker values.
        """
        # Edge case values
        edge_case_biomarkers = {
            "glucose": 0.0,  # Zero value
            "hba1c": 15.0,   # Very high value
            "total_cholesterol": -1.0,  # Negative value (should still be processed)
            "crp": 0.001     # Very small value
        }
        
        result = self.validator.assess_completeness(edge_case_biomarkers)
        
        # Should handle edge cases without crashing
        assert isinstance(result.overall_score, float), "Should return numeric score"
        assert 0.0 <= result.overall_score <= 100.0, "Score should be in valid range"
        assert isinstance(result.analysis_ready, bool), "Should return boolean for analysis readiness"


class TestCompletenessResult:
    """Test CompletenessResult data structure."""
    
    def test_completeness_result_creation(self):
        """
        Test CompletenessResult creation and validation.
        
        Business Value: Ensures result structure is correct for frontend consumption.
        """
        result = CompletenessResult(
            overall_score=75.5,
            health_system_scores={HealthSystem.METABOLIC: 80.0, HealthSystem.CARDIOVASCULAR: 70.0},
            missing_critical=["hba1c"],
            missing_optional=["insulin", "hdl_cholesterol"],
            confidence_level="medium",
            analysis_ready=False,
            recommendations=["Add hba1c for metabolic assessment"]
        )
        
        # Validate result structure
        assert result.overall_score == 75.5
        assert result.confidence_level == "medium"
        assert result.analysis_ready is False
        assert "hba1c" in result.missing_critical
        assert len(result.recommendations) == 1
        assert HealthSystem.METABOLIC in result.health_system_scores
