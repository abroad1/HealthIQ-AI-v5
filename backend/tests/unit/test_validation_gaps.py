"""
High-value tests for biomarker gap analysis.

These tests focus on business-critical functionality for identifying missing biomarkers
and providing detailed gap analysis for clinical decision-making.
"""

import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

from core.validation.gaps import (
    BiomarkerGapAnalyzer,
    GapAnalysisResult,
    BiomarkerGap,
    HealthSystemGap,
    GapSeverity
)
from core.validation.completeness import HealthSystem


class TestBiomarkerGapAnalyzer:
    """Test biomarker gap analysis functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = BiomarkerGapAnalyzer()
    
    def test_comprehensive_gap_analysis_complete_panel(self):
        """
        Test gap analysis with complete biomarker panel.
        
        Business Value: Ensures users with complete data get accurate gap assessment.
        """
        # Complete biomarker panel
        complete_biomarkers = {
            "glucose": 95.0, "hba1c": 5.2, "insulin": 8.5,
            "total_cholesterol": 180.0, "ldl_cholesterol": 110.0, "hdl_cholesterol": 55.0,
            "triglycerides": 120.0, "crp": 1.2, "creatinine": 0.9, "bun": 15.0,
            "alt": 25.0, "ast": 30.0, "hemoglobin": 14.5, "hematocrit": 42.0,
            "white_blood_cells": 7.2, "platelets": 280.0
        }
        
        result = self.analyzer.analyze_gaps(complete_biomarkers)
        
        # Assertions for complete panel
        assert result.total_missing == 0, "Complete panel should have no missing biomarkers"
        assert result.critical_missing == 0, "Complete panel should have no critical gaps"
        assert len(result.analysis_blockers) == 0, "Complete panel should have no analysis blockers"
        assert result.analysis_ready, "Complete panel should be ready for analysis"
        assert len(result.recommendations) > 0, "Should provide recommendations even for complete data"
    
    def test_gap_analysis_incomplete_panel(self):
        """
        Test gap analysis with incomplete biomarker panel.
        
        Business Value: Ensures users with incomplete data get accurate gap identification.
        """
        # Incomplete panel - missing critical biomarkers
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0,
            "crp": 1.2,
            "hemoglobin": 14.5
        }
        
        result = self.analyzer.analyze_gaps(incomplete_biomarkers)
        
        # Assertions for incomplete panel
        assert result.total_missing > 0, "Incomplete panel should have missing biomarkers"
        assert result.critical_missing > 0, "Incomplete panel should have critical gaps"
        assert len(result.analysis_blockers) > 0, "Incomplete panel should have analysis blockers"
        assert not result.analysis_ready, "Incomplete panel should not be ready for analysis"
        
        # Check specific critical gaps
        critical_biomarkers = [gap.biomarker_name for gap in result.critical_gaps]
        assert "hba1c" in critical_biomarkers, "Should identify hba1c as critical gap"
        assert "ldl_cholesterol" in critical_biomarkers, "Should identify LDL as critical gap"
    
    def test_health_system_gap_analysis(self):
        """
        Test health system-specific gap analysis.
        
        Business Value: Ensures accurate health system coverage assessment for clinical planning.
        """
        # Panel with only metabolic biomarkers
        metabolic_only_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "insulin": 8.5
        }
        
        result = self.analyzer.analyze_gaps(metabolic_only_biomarkers)
        
        # Check metabolic system gaps
        metabolic_gap = result.health_system_gaps.get(HealthSystem.METABOLIC)
        assert metabolic_gap is not None, "Should have metabolic system gap analysis"
        assert metabolic_gap.analysis_ready is True, "Complete metabolic system should be ready"
        assert metabolic_gap.coverage_percentage >= 90.0, "Complete metabolic system should have high coverage"
        
        # Check cardiovascular system gaps
        cardiovascular_gap = result.health_system_gaps.get(HealthSystem.CARDIOVASCULAR)
        assert cardiovascular_gap is not None, "Should have cardiovascular system gap analysis"
        assert cardiovascular_gap.analysis_ready is False, "Missing cardiovascular system should not be ready"
        assert len(cardiovascular_gap.critical_gaps) > 0, "Should identify cardiovascular critical gaps"
    
    def test_gap_severity_classification(self):
        """
        Test correct classification of gap severity levels.
        
        Business Value: Ensures proper prioritization of biomarker importance for clinical decisions.
        """
        # Panel with mixed critical and optional gaps
        mixed_biomarkers = {
            "glucose": 95.0,  # Critical metabolic
            "total_cholesterol": 180.0,  # Critical cardiovascular
            "crp": 1.2,  # Critical inflammatory
            "hemoglobin": 14.5  # Critical CBC
            # Missing: hba1c (critical), ldl_cholesterol (critical), insulin (optional)
        }
        
        result = self.analyzer.analyze_gaps(mixed_biomarkers)
        
        # Check severity classification
        critical_gaps = result.critical_gaps
        high_priority_gaps = result.high_priority_gaps
        medium_priority_gaps = result.medium_priority_gaps
        
        assert len(critical_gaps) > 0, "Should identify critical gaps"
        assert all(gap.severity == GapSeverity.CRITICAL for gap in critical_gaps), \
            "Critical gaps should have CRITICAL severity"
        assert all(gap.is_critical for gap in critical_gaps), \
            "Critical gaps should be marked as critical"
        
        # Check specific critical biomarkers
        critical_biomarkers = [gap.biomarker_name for gap in critical_gaps]
        assert "hba1c" in critical_biomarkers, "hba1c should be classified as critical"
        assert "ldl_cholesterol" in critical_biomarkers, "LDL should be classified as critical"
    
    def test_analysis_blocker_identification(self):
        """
        Test identification of analysis blockers.
        
        Business Value: Ensures users understand what prevents analysis from proceeding.
        """
        # Panel with critical gaps
        blocked_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
            # Missing critical biomarkers
        }
        
        result = self.analyzer.analyze_gaps(blocked_biomarkers)
        
        # Should identify analysis blockers
        assert len(result.analysis_blockers) > 0, "Should identify analysis blockers"
        
        # Check blocker content
        blocker_text = " ".join(result.analysis_blockers)
        assert "critical" in blocker_text.lower() or "missing" in blocker_text.lower(), \
            "Blockers should mention critical or missing biomarkers"
    
    def test_recommendation_generation_quality(self):
        """
        Test quality of recommendation generation.
        
        Business Value: Ensures users get actionable guidance for improving their data.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.analyzer.analyze_gaps(incomplete_biomarkers)
        
        # Should generate recommendations
        assert len(result.recommendations) > 0, "Should generate recommendations for incomplete data"
        
        # Check recommendation content
        recommendation_text = " ".join(result.recommendations)
        assert "add" in recommendation_text.lower() or "priority" in recommendation_text.lower(), \
            "Recommendations should suggest adding biomarkers or prioritize actions"
    
    def test_gap_summary_generation(self):
        """
        Test gap summary generation.
        
        Business Value: Ensures system provides concise summary for quick assessment.
        """
        # Incomplete panel
        incomplete_biomarkers = {
            "glucose": 95.0,
            "total_cholesterol": 180.0
        }
        
        result = self.analyzer.analyze_gaps(incomplete_biomarkers)
        summary = self.analyzer.get_gap_summary(result)
        
        # Check summary structure
        assert "total_gaps" in summary, "Summary should include total gaps"
        assert "critical_gaps" in summary, "Summary should include critical gaps"
        assert "analysis_ready" in summary, "Summary should include analysis readiness"
        assert "top_priorities" in summary, "Summary should include top priorities"
        
        # Check summary values
        assert summary["total_gaps"] > 0, "Should have gaps for incomplete data"
        assert summary["critical_gaps"] > 0, "Should have critical gaps for incomplete data"
        assert summary["analysis_ready"] is False, "Incomplete data should not be analysis ready"
        assert len(summary["top_priorities"]) > 0, "Should have top priorities"
    
    def test_empty_biomarker_panel_gap_analysis(self):
        """
        Test gap analysis with empty biomarker panel.
        
        Business Value: Ensures system gracefully handles edge cases without crashing.
        """
        empty_biomarkers = {}
        
        result = self.analyzer.analyze_gaps(empty_biomarkers)
        
        # Should handle empty panel gracefully
        assert result.total_missing > 0, "Empty panel should have many missing biomarkers"
        assert result.critical_missing > 0, "Empty panel should have many critical gaps"
        assert not result.analysis_ready, "Empty panel should not be ready for analysis"
        assert len(result.analysis_blockers) > 0, "Empty panel should have analysis blockers"
    
    def test_biomarker_description_generation(self):
        """
        Test biomarker description generation.
        
        Business Value: Ensures users understand what each biomarker represents.
        """
        # Test with known biomarkers
        test_biomarkers = {
            "glucose": 95.0,
            "hba1c": 5.2,
            "total_cholesterol": 180.0
        }
        
        result = self.analyzer.analyze_gaps(test_biomarkers)
        
        # Check that gaps have descriptions
        for gap in result.overall_gaps:
            assert gap.description, "Each gap should have a description"
            assert len(gap.description) > 10, "Description should be meaningful"
            # Check that description contains biomarker name or related terms
            biomarker_lower = gap.biomarker_name.lower()
            description_lower = gap.description.lower()
            
            # Special cases for biomarker name variations
            name_variations = {
                'crp': ['crp', 'c-reactive protein', 'c reactive protein'],
                'hba1c': ['hba1c', 'hemoglobin a1c', 'a1c'],
                'ldl_cholesterol': ['ldl cholesterol', 'ldl', 'bad cholesterol'],
                'hdl_cholesterol': ['hdl cholesterol', 'hdl', 'good cholesterol'],
                'white_blood_cells': ['white blood cells', 'wbc', 'leukocytes', 'white blood cell'],
                'total_cholesterol': ['total cholesterol', 'cholesterol'],
                'bun': ['bun', 'blood urea nitrogen', 'urea nitrogen'],
                'alt': ['alt', 'alanine aminotransferase'],
                'ast': ['ast', 'aspartate aminotransferase'],
                'creatinine': ['creatinine', 'serum creatinine'],
                'hemoglobin': ['hemoglobin', 'hgb', 'hb'],
                'hematocrit': ['hematocrit', 'hct', 'pcv'],
                'platelets': ['platelets', 'plt', 'platelet count'],
                'insulin': ['insulin', 'insulin level', 'serum insulin'],
                'triglycerides': ['triglycerides', 'trig', 'triglyceride']
            }
            
            variations = name_variations.get(biomarker_lower, [biomarker_lower])
            assert any(variation in description_lower for variation in variations), \
                f"Description should mention biomarker name '{gap.biomarker_name}' or related terms"
    
    def test_impact_assessment_generation(self):
        """
        Test impact assessment generation for gaps.
        
        Business Value: Ensures users understand the clinical impact of missing biomarkers.
        """
        # Test with critical gaps
        test_biomarkers = {
            "glucose": 95.0
            # Missing critical biomarkers
        }
        
        result = self.analyzer.analyze_gaps(test_biomarkers)
        
        # Check that gaps have impact assessments
        for gap in result.critical_gaps:
            assert gap.impact, "Each gap should have an impact assessment"
            assert len(gap.impact) > 10, "Impact should be meaningful"
            assert "cannot" in gap.impact.lower() or "limited" in gap.impact.lower(), \
                "Impact should describe limitations"
    
    def test_health_system_coverage_calculation(self):
        """
        Test health system coverage calculation accuracy.
        
        Business Value: Ensures accurate coverage percentages for clinical planning.
        """
        # Test with partial coverage
        partial_biomarkers = {
            "glucose": 95.0,  # 1 of 3 metabolic
            "total_cholesterol": 180.0,  # 1 of 4 cardiovascular
            "crp": 1.2,  # 1 of 1 inflammatory
            "hemoglobin": 14.5  # 1 of 4 CBC
        }
        
        result = self.analyzer.analyze_gaps(partial_biomarkers)
        
        # Check coverage calculations
        metabolic_gap = result.health_system_gaps.get(HealthSystem.METABOLIC)
        assert metabolic_gap.coverage_percentage > 0, "Should have some coverage"
        assert metabolic_gap.coverage_percentage < 100, "Should not have complete coverage"
        
        inflammatory_gap = result.health_system_gaps.get(HealthSystem.INFLAMMATORY)
        assert inflammatory_gap.coverage_percentage == 100.0, "Complete inflammatory system should have 100% coverage"


class TestGapAnalysisResult:
    """Test GapAnalysisResult data structure."""
    
    def test_gap_analysis_result_creation(self):
        """
        Test GapAnalysisResult creation and validation.
        
        Business Value: Ensures result structure is correct for frontend consumption.
        """
        # Create mock gaps
        critical_gap = BiomarkerGap(
            biomarker_name="hba1c",
            health_system=HealthSystem.METABOLIC,
            severity=GapSeverity.CRITICAL,
            is_critical=True,
            is_optional=False,
            description="Hemoglobin A1c - long-term blood sugar control indicator",
            impact="Cannot assess long-term blood sugar control"
        )
        
        result = GapAnalysisResult(
            overall_gaps=[critical_gap],
            health_system_gaps={},
            critical_gaps=[critical_gap],
            high_priority_gaps=[],
            medium_priority_gaps=[],
            low_priority_gaps=[],
            total_missing=1,
            critical_missing=1,
            analysis_blockers=["Missing critical biomarkers: hba1c"],
            recommendations=["Add hba1c for metabolic assessment"],
            analysis_ready=False
        )
        
        # Validate result structure
        assert result.total_missing == 1
        assert result.critical_missing == 1
        assert len(result.critical_gaps) == 1
        assert result.critical_gaps[0].biomarker_name == "hba1c"
        assert len(result.analysis_blockers) == 1
        assert len(result.recommendations) == 1
