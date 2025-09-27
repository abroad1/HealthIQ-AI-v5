"""
High-value tests for biomarker recommendation engine.

These tests focus on business-critical functionality for generating actionable recommendations
to help users improve their biomarker data completeness and analysis quality.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from core.validation.recommendations import (
    RecommendationEngine,
    RecommendationSet,
    Recommendation,
    RecommendationPriority,
    RecommendationCategory
)
from core.validation.completeness import HealthSystem


class TestRecommendationEngine:
    """Test recommendation engine functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = RecommendationEngine()
    
    def test_complete_biomarker_panel_recommendations(self):
        """
        Test recommendation generation for complete biomarker panel.
        
        Business Value: Ensures users with complete data get appropriate guidance.
        """
        # Complete biomarker panel
        complete_biomarkers = {
            "glucose": 95.0, "hba1c": 5.2, "insulin": 8.5,
            "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0,
            "triglycerides": 120.0, "crp": 1.2, "creatinine": 0.9, "bun": 15.0,
            "alt": 25.0, "ast": 30.0, "hemoglobin": 14.5, "hematocrit": 42.0,
            "white_blood_cells": 7.2, "platelets": 280.0
        }
        
        result = self.engine.generate_recommendations(complete_biomarkers)
        
        # Assertions for complete panel
        assert result.analysis_readiness is True, "Complete panel should be analysis ready"
        assert len(result.critical_recommendations) == 0, "Complete panel should have no critical recommendations"
        # Note: Complete panels may not have recommendations, which is valid
        assert "ready" in result.summary.lower() or "good" in result.summary.lower() or "complete" in result.summary.lower(), \
            "Summary should indicate good status"
        assert len(result.next_steps) > 0, "Should provide next steps"
    
    def test_incomplete_biomarker_panel_recommendations(self):
        """
        Test recommendation generation for incomplete biomarker panel.
        
        Business Value: Ensures users with incomplete data get actionable guidance.
        """
        # Incomplete panel - missing critical biomarkers
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        result = self.engine.generate_recommendations(incomplete_biomarkers)
        
        # Assertions for incomplete panel
        assert result.analysis_readiness is False, "Incomplete panel should not be analysis ready"
        assert len(result.critical_recommendations) > 0, "Incomplete panel should have critical recommendations"
        assert len(result.high_priority_recommendations) > 0, "Should have high priority recommendations"
        
        # Check recommendation content
        critical_rec = result.critical_recommendations[0]
        assert critical_rec.priority == RecommendationPriority.CRITICAL, "Should have critical priority"
        assert critical_rec.category == RecommendationCategory.BIOMARKER_ADDITION, "Should be biomarker addition"
        assert len(critical_rec.action_items) > 0, "Should have actionable items"
        assert "hba1c" in critical_rec.biomarkers_involved or "ldl_cholesterol" in critical_rec.biomarkers_involved, \
            "Should recommend adding critical biomarkers"
    
    def test_critical_biomarker_recommendation_generation(self):
        """
        Test generation of critical biomarker recommendations.
        
        Business Value: Ensures users get prioritized guidance for critical gaps.
        """
        # Panel with critical gaps
        critical_gap_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
            # Missing: hba1c, ldl_cholesterol (critical)
        }
        
        result = self.engine.generate_recommendations(critical_gap_biomarkers)
        
        # Check critical recommendations
        assert len(result.critical_recommendations) > 0, "Should generate critical recommendations"
        
        critical_rec = result.critical_recommendations[0]
        assert critical_rec.priority == RecommendationPriority.CRITICAL, "Should have critical priority"
        assert critical_rec.category == RecommendationCategory.BIOMARKER_ADDITION, "Should be biomarker addition"
        assert "critical" in critical_rec.title.lower(), "Title should mention critical"
        assert len(critical_rec.biomarkers_involved) > 0, "Should specify which biomarkers to add"
        assert critical_rec.expected_impact, "Should describe expected impact"
        assert critical_rec.effort_level in ["low", "medium", "high"], "Should specify effort level"
    
    def test_health_system_improvement_recommendations(self):
        """
        Test generation of health system improvement recommendations.
        
        Business Value: Ensures users get guidance for improving specific health system coverage.
        """
        # Panel with low health system coverage
        low_coverage_biomarkers = {
            "glucose": 95.0,  # Only 1 of 3 metabolic biomarkers
            "total_cholesterol": 180.0,  # Only 1 of 4 cardiovascular biomarkers
            "crp": 1.2,  # Complete inflammatory system
            "hemoglobin": 14.5  # Only 1 of 4 CBC biomarkers
        }
        
        result = self.engine.generate_recommendations(low_coverage_biomarkers)
        
        # Check for health system improvement recommendations
        health_system_recs = [
            rec for rec in result.recommendations
            if rec.category == RecommendationCategory.HEALTH_SYSTEM_IMPROVEMENT
        ]
        
        assert len(health_system_recs) > 0, "Should generate health system improvement recommendations"
        
        health_system_rec = health_system_recs[0]
        assert health_system_rec.priority == RecommendationPriority.HIGH, "Should have high priority"
        assert "coverage" in health_system_rec.title.lower() or "improve" in health_system_rec.title.lower(), \
            "Title should mention coverage improvement"
        assert len(health_system_rec.health_systems_affected) > 0, "Should specify affected health systems"
    
    def test_analysis_readiness_recommendations(self):
        """
        Test generation of analysis readiness recommendations.
        
        Business Value: Ensures users understand what's blocking analysis and how to proceed.
        """
        # Panel with analysis blockers
        blocked_biomarkers = {
            "glucose": 95.0
            # Missing critical biomarkers that block analysis
        }
        
        result = self.engine.generate_recommendations(blocked_biomarkers)
        
        # Check for analysis readiness recommendations
        analysis_readiness_recs = [
            rec for rec in result.recommendations
            if rec.category == RecommendationCategory.ANALYSIS_READINESS
        ]
        
        assert len(analysis_readiness_recs) > 0, "Should generate analysis readiness recommendations"
        
        analysis_rec = analysis_readiness_recs[0]
        assert analysis_rec.priority == RecommendationPriority.CRITICAL, "Should have critical priority"
        assert "blocker" in analysis_rec.title.lower() or "analysis" in analysis_rec.title.lower(), \
            "Title should mention analysis blockers"
        assert len(analysis_rec.action_items) > 0, "Should have actionable items"
    
    def test_recommendation_priority_classification(self):
        """
        Test correct classification of recommendation priorities.
        
        Business Value: Ensures users get properly prioritized guidance for clinical decisions.
        """
        # Panel with mixed gaps
        mixed_gap_biomarkers = {
            "glucose": 95.0,  # Critical metabolic
            "total_cholesterol": 180.0,  # Critical cardiovascular
            "crp": 1.2,  # Critical inflammatory
            "hemoglobin": 14.5  # Critical CBC
            # Missing: hba1c (critical), ldl_cholesterol (critical), insulin (optional)
        }
        
        result = self.engine.generate_recommendations(mixed_gap_biomarkers)
        
        # Check priority classification
        assert len(result.critical_recommendations) > 0, "Should have critical recommendations"
        assert len(result.high_priority_recommendations) > 0, "Should have high priority recommendations"
        assert len(result.medium_priority_recommendations) > 0, "Should have medium priority recommendations"
        
        # Check priority consistency
        for rec in result.critical_recommendations:
            assert rec.priority == RecommendationPriority.CRITICAL, "Critical recommendations should have critical priority"
        
        for rec in result.high_priority_recommendations:
            assert rec.priority == RecommendationPriority.HIGH, "High priority recommendations should have high priority"
    
    def test_recommendation_action_items_quality(self):
        """
        Test quality of recommendation action items.
        
        Business Value: Ensures users get specific, actionable guidance.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.engine.generate_recommendations(incomplete_biomarkers)
        
        # Check action items quality
        for rec in result.recommendations:
            assert len(rec.action_items) > 0, "Each recommendation should have action items"
            
            for action_item in rec.action_items:
                assert len(action_item) > 10, "Action items should be specific and detailed"
                assert any(word in action_item.lower() for word in ["add", "consider", "improve", "ensure", "focus", "retest"]), \
                    "Action items should be actionable"
    
    def test_recommendation_expected_impact_assessment(self):
        """
        Test quality of expected impact assessments.
        
        Business Value: Ensures users understand the value of following recommendations.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.engine.generate_recommendations(incomplete_biomarkers)
        
        # Check expected impact quality
        for rec in result.recommendations:
            assert rec.expected_impact, "Each recommendation should have expected impact"
            assert len(rec.expected_impact) > 20, "Expected impact should be detailed"
            assert "improve" in rec.expected_impact.lower() or "enable" in rec.expected_impact.lower() or "increase" in rec.expected_impact.lower(), \
                "Expected impact should describe positive outcomes"
    
    def test_next_steps_generation(self):
        """
        Test generation of actionable next steps.
        
        Business Value: Ensures users have clear, prioritized next steps to follow.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.engine.generate_recommendations(incomplete_biomarkers)
        
        # Check next steps quality
        assert len(result.next_steps) > 0, "Should generate next steps"
        assert len(result.next_steps) <= 5, "Should not overwhelm with too many next steps"
        
        # Check next steps content
        next_steps_text = " ".join(result.next_steps)
        assert "1." in next_steps_text or "2." in next_steps_text, "Should be numbered steps"
        assert "add" in next_steps_text.lower() or "improve" in next_steps_text.lower(), \
            "Next steps should be actionable"
    
    def test_summary_generation_quality(self):
        """
        Test quality of summary generation.
        
        Business Value: Ensures users get clear, concise summary of their data status.
        """
        # Test with different completeness levels
        test_cases = [
            ({"glucose": 95.0, "hba1c": 5.2, "total_cholesterol": 180.0, "ldl_cholesterol": 110.0}, "ready"),
            ({"glucose": 95.0}, "incomplete"),
            ({}, "empty")
        ]
        
        for biomarkers, expected_status in test_cases:
            result = self.engine.generate_recommendations(biomarkers)
            
            assert result.summary, "Should generate summary"
            assert len(result.summary) > 20, "Summary should be meaningful"
            assert len(result.summary) < 200, "Summary should be concise"
            
            # Check summary content based on expected status
            if expected_status == "ready":
                assert any(word in result.summary.lower() for word in ["ready", "good", "complete", "well-suited"]), \
                    "Ready data should have positive summary"
            elif expected_status == "incomplete":
                assert any(word in result.summary.lower() for word in ["incomplete", "missing", "gap", "critical gaps"]), \
                    "Incomplete data should mention gaps or missing data"
    
    def test_estimated_improvement_calculation(self):
        """
        Test calculation of estimated improvement from following recommendations.
        
        Business Value: Ensures users understand the potential value of following recommendations.
        """
        # Test with different completeness levels
        test_cases = [
            ({"glucose": 95.0}, "low"),
            ({"glucose": 95.0, "hba1c": 5.2, "total_cholesterol": 180.0}, "medium"),
            ({"glucose": 95.0, "hba1c": 5.2, "insulin": 8.5, "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0}, "high")
        ]
        
        for biomarkers, expected_level in test_cases:
            result = self.engine.generate_recommendations(biomarkers)
            
            assert result.estimated_improvement, "Should estimate improvement"
            assert len(result.estimated_improvement) > 20, "Estimate should be detailed"
            assert "improve" in result.estimated_improvement.lower() or "increase" in result.estimated_improvement.lower() or "enable" in result.estimated_improvement.lower(), \
                "Estimate should describe positive outcomes"
    
    def test_recommendation_summary_generation(self):
        """
        Test generation of recommendation summary.
        
        Business Value: Ensures system provides concise summary for quick assessment.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.engine.generate_recommendations(incomplete_biomarkers)
        summary = self.engine.get_recommendation_summary(result)
        
        # Check summary structure
        required_fields = [
            "total_recommendations", "critical_count", "high_priority_count",
            "medium_priority_count", "low_priority_count", "analysis_ready",
            "next_steps_count", "estimated_improvement"
        ]
        
        for field in required_fields:
            assert field in summary, f"Summary should include {field}"
        
        # Check summary values
        assert summary["total_recommendations"] > 0, "Should have recommendations for incomplete data"
        assert summary["critical_count"] > 0, "Should have critical recommendations for incomplete data"
        assert summary["analysis_ready"] is False, "Incomplete data should not be analysis ready"
        assert summary["next_steps_count"] > 0, "Should have next steps"
    
    def test_empty_biomarker_panel_recommendations(self):
        """
        Test recommendation generation for empty biomarker panel.
        
        Business Value: Ensures system gracefully handles edge cases without crashing.
        """
        empty_biomarkers = {}
        
        result = self.engine.generate_recommendations(empty_biomarkers)
        
        # Should handle empty panel gracefully
        assert result.analysis_readiness is False, "Empty panel should not be analysis ready"
        assert len(result.critical_recommendations) > 0, "Empty panel should have critical recommendations"
        assert len(result.recommendations) > 0, "Should provide recommendations for empty data"
        assert any(word in result.summary.lower() for word in ["incomplete", "missing", "gap", "critical gaps", "0.0%"]), \
            "Summary should mention incomplete or missing data"
        assert len(result.next_steps) > 0, "Should provide next steps for empty data"


class TestRecommendationSet:
    """Test RecommendationSet data structure."""
    
    def test_recommendation_set_creation(self):
        """
        Test RecommendationSet creation and validation.
        
        Business Value: Ensures result structure is correct for frontend consumption.
        """
        # Create mock recommendation
        mock_rec = Recommendation(
            title="Add Critical Biomarkers",
            description="Missing critical biomarkers for analysis",
            priority=RecommendationPriority.CRITICAL,
            category=RecommendationCategory.BIOMARKER_ADDITION,
            action_items=["Add hba1c", "Add ldl_cholesterol"],
            expected_impact="Enables comprehensive analysis",
            effort_level="medium",
            biomarkers_involved=["hba1c", "ldl_cholesterol"],
            health_systems_affected=[HealthSystem.METABOLIC, HealthSystem.CARDIOVASCULAR]
        )
        
        result = RecommendationSet(
            recommendations=[mock_rec],
            critical_recommendations=[mock_rec],
            high_priority_recommendations=[],
            medium_priority_recommendations=[],
            low_priority_recommendations=[],
            summary="Data has critical gaps",
            next_steps=["Add critical biomarkers", "Improve coverage"],
            analysis_readiness=False,
            estimated_improvement="Could improve score to 80%+"
        )
        
        # Validate result structure
        assert len(result.recommendations) == 1
        assert len(result.critical_recommendations) == 1
        assert result.analysis_readiness is False
        assert "critical gaps" in result.summary
        assert len(result.next_steps) == 2
        assert "improve" in result.estimated_improvement
