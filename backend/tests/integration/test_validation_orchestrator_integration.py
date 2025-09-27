"""
Integration tests for validation modules with orchestrator.

These tests verify that the validation modules integrate correctly with the orchestrator
and provide the expected functionality for biomarker data validation.
"""

import pytest
from typing import Dict, Any

from core.pipeline.orchestrator import AnalysisOrchestrator


class TestValidationOrchestratorIntegration:
    """Test integration between validation modules and orchestrator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.orchestrator = AnalysisOrchestrator()
    
    def test_completeness_assessment_integration(self):
        """
        Test completeness assessment integration with orchestrator.
        
        Business Value: Ensures orchestrator provides completeness assessment for users.
        """
        # Test with complete biomarker panel
        complete_biomarkers = {
            "glucose": 95.0, "hba1c": 5.2, "insulin": 8.5,
            "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0,
            "triglycerides": 120.0, "crp": 1.2, "creatinine": 0.9, "bun": 15.0,
            "alt": 25.0, "ast": 30.0, "hemoglobin": 14.5, "hematocrit": 42.0,
            "white_blood_cells": 7.2, "platelets": 280.0
        }
        
        result = self.orchestrator.assess_data_completeness(complete_biomarkers)
        
        # Validate result structure
        assert "overall_score" in result, "Should include overall score"
        assert "health_system_scores" in result, "Should include health system scores"
        assert "missing_critical" in result, "Should include missing critical biomarkers"
        assert "missing_optional" in result, "Should include missing optional biomarkers"
        assert "confidence_level" in result, "Should include confidence level"
        assert "analysis_ready" in result, "Should include analysis readiness"
        assert "recommendations" in result, "Should include recommendations"
        
        # Validate result values
        assert isinstance(result["overall_score"], float), "Overall score should be float"
        assert 0.0 <= result["overall_score"] <= 100.0, "Overall score should be in valid range"
        assert isinstance(result["analysis_ready"], bool), "Analysis ready should be boolean"
        assert isinstance(result["confidence_level"], str), "Confidence level should be string"
        assert result["confidence_level"] in ["high", "medium", "low"], "Confidence level should be valid"
        assert isinstance(result["recommendations"], list), "Recommendations should be list"
    
    def test_gap_analysis_integration(self):
        """
        Test gap analysis integration with orchestrator.
        
        Business Value: Ensures orchestrator provides detailed gap analysis for users.
        """
        # Test with incomplete biomarker panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        result = self.orchestrator.analyze_data_gaps(incomplete_biomarkers)
        
        # Validate result structure
        assert "total_missing" in result, "Should include total missing count"
        assert "critical_missing" in result, "Should include critical missing count"
        assert "analysis_ready" in result, "Should include analysis readiness"
        assert "analysis_blockers" in result, "Should include analysis blockers"
        assert "critical_gaps" in result, "Should include critical gaps"
        assert "health_system_gaps" in result, "Should include health system gaps"
        assert "recommendations" in result, "Should include recommendations"
        
        # Validate result values
        assert isinstance(result["total_missing"], int), "Total missing should be integer"
        assert isinstance(result["critical_missing"], int), "Critical missing should be integer"
        assert isinstance(result["analysis_ready"], bool), "Analysis ready should be boolean"
        assert isinstance(result["analysis_blockers"], list), "Analysis blockers should be list"
        assert isinstance(result["critical_gaps"], list), "Critical gaps should be list"
        assert isinstance(result["health_system_gaps"], dict), "Health system gaps should be dict"
        assert isinstance(result["recommendations"], list), "Recommendations should be list"
        
        # Validate critical gaps structure
        if result["critical_gaps"]:
            critical_gap = result["critical_gaps"][0]
            assert "biomarker_name" in critical_gap, "Critical gap should have biomarker name"
            assert "health_system" in critical_gap, "Critical gap should have health system"
            assert "severity" in critical_gap, "Critical gap should have severity"
            assert "description" in critical_gap, "Critical gap should have description"
            assert "impact" in critical_gap, "Critical gap should have impact"
    
    def test_recommendation_generation_integration(self):
        """
        Test recommendation generation integration with orchestrator.
        
        Business Value: Ensures orchestrator provides actionable recommendations for users.
        """
        # Test with incomplete biomarker panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        result = self.orchestrator.generate_recommendations(incomplete_biomarkers)
        
        # Validate result structure
        assert "summary" in result, "Should include summary"
        assert "analysis_readiness" in result, "Should include analysis readiness"
        assert "estimated_improvement" in result, "Should include estimated improvement"
        assert "next_steps" in result, "Should include next steps"
        assert "recommendations" in result, "Should include recommendations"
        assert "critical_recommendations" in result, "Should include critical recommendations"
        assert "high_priority_recommendations" in result, "Should include high priority recommendations"
        
        # Validate result values
        assert isinstance(result["summary"], str), "Summary should be string"
        assert isinstance(result["analysis_readiness"], bool), "Analysis readiness should be boolean"
        assert isinstance(result["estimated_improvement"], str), "Estimated improvement should be string"
        assert isinstance(result["next_steps"], list), "Next steps should be list"
        assert isinstance(result["recommendations"], list), "Recommendations should be list"
        assert isinstance(result["critical_recommendations"], list), "Critical recommendations should be list"
        assert isinstance(result["high_priority_recommendations"], list), "High priority recommendations should be list"
        
        # Validate recommendation structure
        if result["recommendations"]:
            recommendation = result["recommendations"][0]
            assert "title" in recommendation, "Recommendation should have title"
            assert "description" in recommendation, "Recommendation should have description"
            assert "priority" in recommendation, "Recommendation should have priority"
            assert "category" in recommendation, "Recommendation should have category"
            assert "action_items" in recommendation, "Recommendation should have action items"
            assert "expected_impact" in recommendation, "Recommendation should have expected impact"
            assert "effort_level" in recommendation, "Recommendation should have effort level"
            assert "biomarkers_involved" in recommendation, "Recommendation should have biomarkers involved"
            assert "health_systems_affected" in recommendation, "Recommendation should have health systems affected"
    
    def test_empty_biomarker_panel_integration(self):
        """
        Test integration with empty biomarker panel.
        
        Business Value: Ensures system gracefully handles edge cases without crashing.
        """
        empty_biomarkers = {}
        
        # Test all validation methods with empty panel
        completeness_result = self.orchestrator.assess_data_completeness(empty_biomarkers)
        gap_result = self.orchestrator.analyze_data_gaps(empty_biomarkers)
        recommendation_result = self.orchestrator.generate_recommendations(empty_biomarkers)
        
        # Validate completeness result
        assert completeness_result["overall_score"] == 0.0, "Empty panel should have zero score"
        assert completeness_result["analysis_ready"] is False, "Empty panel should not be analysis ready"
        assert completeness_result["confidence_level"] == "low", "Empty panel should have low confidence"
        assert len(completeness_result["missing_critical"]) > 0, "Empty panel should have critical gaps"
        
        # Validate gap result
        assert gap_result["total_missing"] > 0, "Empty panel should have many missing biomarkers"
        assert gap_result["critical_missing"] > 0, "Empty panel should have many critical gaps"
        assert gap_result["analysis_ready"] is False, "Empty panel should not be analysis ready"
        assert len(gap_result["analysis_blockers"]) > 0, "Empty panel should have analysis blockers"
        
        # Validate recommendation result
        assert recommendation_result["analysis_readiness"] is False, "Empty panel should not be analysis ready"
        assert len(recommendation_result["critical_recommendations"]) > 0, "Empty panel should have critical recommendations"
        assert len(recommendation_result["next_steps"]) > 0, "Empty panel should have next steps"
    
    def test_complete_biomarker_panel_integration(self):
        """
        Test integration with complete biomarker panel.
        
        Business Value: Ensures system provides appropriate feedback for complete data.
        """
        complete_biomarkers = {
            "glucose": 95.0, "hba1c": 5.2, "insulin": 8.5,
            "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0,
            "triglycerides": 120.0, "crp": 1.2, "creatinine": 0.9, "bun": 15.0,
            "alt": 25.0, "ast": 30.0, "hemoglobin": 14.5, "hematocrit": 42.0,
            "white_blood_cells": 7.2, "platelets": 280.0
        }
        
        # Test all validation methods with complete panel
        completeness_result = self.orchestrator.assess_data_completeness(complete_biomarkers)
        gap_result = self.orchestrator.analyze_data_gaps(complete_biomarkers)
        recommendation_result = self.orchestrator.generate_recommendations(complete_biomarkers)
        
        # Validate completeness result
        assert completeness_result["overall_score"] >= 80.0, "Complete panel should have high score"
        assert completeness_result["analysis_ready"] is True, "Complete panel should be analysis ready"
        assert completeness_result["confidence_level"] in ["high", "medium"], "Complete panel should have good confidence"
        assert len(completeness_result["missing_critical"]) == 0, "Complete panel should have no critical gaps"
        
        # Validate gap result
        assert gap_result["total_missing"] == 0, "Complete panel should have no missing biomarkers"
        assert gap_result["critical_missing"] == 0, "Complete panel should have no critical gaps"
        assert gap_result["analysis_ready"] is True, "Complete panel should be analysis ready"
        assert len(gap_result["analysis_blockers"]) == 0, "Complete panel should have no analysis blockers"
        
        # Validate recommendation result
        assert recommendation_result["analysis_readiness"] is True, "Complete panel should be analysis ready"
        assert len(recommendation_result["critical_recommendations"]) == 0, "Complete panel should have no critical recommendations"
        assert "good" in recommendation_result["summary"].lower() or "ready" in recommendation_result["summary"].lower(), \
            "Complete panel should have positive summary"
    
    def test_validation_methods_consistency(self):
        """
        Test consistency between different validation methods.
        
        Business Value: Ensures all validation methods provide consistent results.
        """
        test_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        # Get results from all validation methods
        completeness_result = self.orchestrator.assess_data_completeness(test_biomarkers)
        gap_result = self.orchestrator.analyze_data_gaps(test_biomarkers)
        recommendation_result = self.orchestrator.generate_recommendations(test_biomarkers)
        
        # Check consistency
        assert completeness_result["analysis_ready"] == gap_result["analysis_ready"], \
            "Completeness and gap analysis should agree on analysis readiness"
        assert completeness_result["analysis_ready"] == recommendation_result["analysis_readiness"], \
            "Completeness and recommendation should agree on analysis readiness"
        
        # Check that missing critical biomarkers are consistent
        completeness_critical = set(completeness_result["missing_critical"])
        gap_critical = set(gap["biomarker_name"] for gap in gap_result["critical_gaps"])
        assert completeness_critical == gap_critical, \
            "Completeness and gap analysis should identify the same critical gaps"
        
        # Check that recommendations are generated for incomplete data
        if not completeness_result["analysis_ready"]:
            assert len(recommendation_result["critical_recommendations"]) > 0, \
                "Should generate critical recommendations for incomplete data"
            assert len(recommendation_result["next_steps"]) > 0, \
                "Should generate next steps for incomplete data"
    
    def test_health_system_coverage_consistency(self):
        """
        Test consistency of health system coverage across validation methods.
        
        Business Value: Ensures health system assessment is consistent across all validation methods.
        """
        test_biomarkers = {
            "glucose": 95.0, "hba1c": 5.2,  # Complete metabolic system
            "total_cholesterol": 180.0,  # Partial cardiovascular system
            "crp": 1.2,  # Complete inflammatory system
            "hemoglobin": 14.5  # Partial CBC system
        }
        
        # Get results from validation methods
        completeness_result = self.orchestrator.assess_data_completeness(test_biomarkers)
        gap_result = self.orchestrator.analyze_data_gaps(test_biomarkers)
        
        # Check health system scores consistency
        completeness_scores = completeness_result["health_system_scores"]
        gap_scores = {
            system: gap["completeness_score"] 
            for system, gap in gap_result["health_system_gaps"].items()
        }
        
        # Compare scores for common systems
        for system in completeness_scores:
            if system in gap_scores:
                # Allow for small differences due to different calculation methods
                score_diff = abs(completeness_scores[system] - gap_scores[system])
                assert score_diff < 5.0, f"Health system scores should be consistent for {system}"
        
        # Check that complete systems are identified consistently
        complete_systems_completeness = [
            system for system, score in completeness_scores.items() 
            if score >= 90.0
        ]
        complete_systems_gap = [
            system for system, gap in gap_result["health_system_gaps"].items()
            if gap["coverage_percentage"] >= 90.0
        ]
        
        assert set(complete_systems_completeness) == set(complete_systems_gap), \
            "Complete systems should be identified consistently across validation methods"
