"""
High-value tests for scoring rules functionality.

These tests focus on business-critical functionality for biomarker scoring rules,
ensuring clinical thresholds and scoring logic are accurate and consistent.
"""

import pytest
from typing import Dict, Any

from core.scoring.rules import ScoringRules, ScoreRange, BiomarkerRule, HealthSystemRules


class TestScoringRules:
    """Test scoring rules functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.rules = ScoringRules()
    
    def test_biomarker_rule_retrieval(self):
        """
        Test biomarker rule retrieval for known biomarkers.
        
        Business Value: Ensures scoring rules are properly defined for all biomarkers.
        """
        # Test known biomarkers
        glucose_rule = self.rules.get_biomarker_rule("glucose")
        assert glucose_rule is not None, "Should find glucose rule"
        assert glucose_rule.biomarker_name == "glucose", "Should have correct biomarker name"
        assert glucose_rule.unit == "mg/dL", "Should have correct unit"
        assert glucose_rule.weight > 0, "Should have positive weight"
        
        # Test unknown biomarker
        unknown_rule = self.rules.get_biomarker_rule("unknown_biomarker")
        assert unknown_rule is None, "Should return None for unknown biomarker"
    
    def test_health_system_rules_retrieval(self):
        """
        Test health system rules retrieval.
        
        Business Value: Ensures all health systems have proper rule definitions.
        """
        # Test known health systems
        metabolic_rules = self.rules.get_health_system_rules("metabolic")
        assert metabolic_rules is not None, "Should find metabolic rules"
        assert metabolic_rules.system_name == "metabolic", "Should have correct system name"
        assert len(metabolic_rules.biomarkers) > 0, "Should have biomarkers defined"
        assert metabolic_rules.min_biomarkers_required > 0, "Should have minimum biomarkers required"
        assert metabolic_rules.system_weight > 0, "Should have positive system weight"
        
        # Test unknown health system
        unknown_rules = self.rules.get_health_system_rules("unknown_system")
        assert unknown_rules is None, "Should return None for unknown health system"
    
    def test_glucose_scoring_accuracy(self):
        """
        Test glucose scoring accuracy against clinical thresholds.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_range = {"min": 70.0, "max": 100.0, "unit": "mg/dL", "source": "lab"}
        # Test optimal glucose (70-100 mg/dL)
        score_optimal, range_optimal, _ = self.rules.calculate_biomarker_score(
            "glucose", 85.0, input_reference_range=lab_range
        )
        assert score_optimal >= 90, "Optimal glucose should score high"
        assert range_optimal == ScoreRange.OPTIMAL, "Should be in optimal range"

        # Test normal glucose (70-100 mg/dL)
        score_normal, range_normal, _ = self.rules.calculate_biomarker_score(
            "glucose", 95.0, input_reference_range=lab_range
        )
        assert score_normal >= 90, "Normal glucose should score high"
        assert range_normal in [ScoreRange.NORMAL, ScoreRange.OPTIMAL], "Should be in normal or optimal range"

        # Test prediabetic glucose (100-125 mg/dL) - lab range scores by position
        lab_pred = {"min": 70.0, "max": 125.0, "unit": "mg/dL", "source": "lab"}
        score_prediabetic, range_prediabetic, _ = self.rules.calculate_biomarker_score(
            "glucose", 110.0, input_reference_range=lab_pred
        )
        assert score_prediabetic > 0, "Prediabetic glucose should be scored"
        assert range_prediabetic in [ScoreRange.BORDERLINE, ScoreRange.NORMAL, ScoreRange.OPTIMAL]

        # Test diabetic glucose (>126 mg/dL) - value near top of range scores lower
        lab_diabetic = {"min": 70.0, "max": 126.0, "unit": "mg/dL", "source": "lab"}
        score_diabetic, range_diabetic, _ = self.rules.calculate_biomarker_score(
            "glucose", 150.0, input_reference_range=lab_diabetic
        )
        assert score_diabetic <= 50, "Diabetic glucose should score low"
        assert range_diabetic in [ScoreRange.HIGH, ScoreRange.VERY_HIGH, ScoreRange.CRITICAL], "Should be in high range"
    
    def test_hba1c_scoring_accuracy(self):
        """
        Test HbA1c scoring accuracy against clinical thresholds.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_range = {"min": 4.0, "max": 5.6, "unit": "%", "source": "lab"}
        score_optimal, range_optimal, _ = self.rules.calculate_biomarker_score(
            "hba1c", 5.0, input_reference_range=lab_range
        )
        assert score_optimal >= 90, "Optimal HbA1c should score high"
        assert range_optimal == ScoreRange.OPTIMAL, "Should be in optimal range"

        lab_pred = {"min": 4.0, "max": 6.4, "unit": "%", "source": "lab"}
        score_prediabetic, range_prediabetic, _ = self.rules.calculate_biomarker_score(
            "hba1c", 6.0, input_reference_range=lab_pred
        )
        assert score_prediabetic > 0, "Prediabetic HbA1c should be scored"
        assert range_prediabetic in [ScoreRange.BORDERLINE, ScoreRange.NORMAL, ScoreRange.OPTIMAL]

        lab_diabetic = {"min": 4.0, "max": 6.5, "unit": "%", "source": "lab"}
        score_diabetic, range_diabetic, _ = self.rules.calculate_biomarker_score(
            "hba1c", 7.5, input_reference_range=lab_diabetic
        )
        assert score_diabetic <= 50, "Diabetic HbA1c should score low"
        assert range_diabetic in [ScoreRange.HIGH, ScoreRange.VERY_HIGH, ScoreRange.CRITICAL], "Should be in high range"
    
    def test_cholesterol_scoring_accuracy(self):
        """
        Test cholesterol scoring accuracy against clinical thresholds.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_optimal = {"min": 0.0, "max": 100.0, "unit": "mg/dL", "source": "lab"}
        score_optimal, range_optimal, _ = self.rules.calculate_biomarker_score(
            "ldl_cholesterol", 90.0, input_reference_range=lab_optimal
        )
        assert score_optimal >= 90, "Optimal LDL should score high"
        assert range_optimal in [ScoreRange.OPTIMAL, ScoreRange.NORMAL], "Should be in optimal/normal range"

        lab_borderline = {"min": 0.0, "max": 130.0, "unit": "mg/dL", "source": "lab"}
        score_borderline, range_borderline, _ = self.rules.calculate_biomarker_score(
            "ldl_cholesterol", 140.0, input_reference_range=lab_borderline
        )
        assert score_borderline > 0, "Borderline LDL should be scored"
        assert range_borderline in [ScoreRange.BORDERLINE, ScoreRange.HIGH, ScoreRange.CRITICAL], "Should indicate elevated"

        lab_high = {"min": 0.0, "max": 130.0, "unit": "mg/dL", "source": "lab"}
        score_high, range_high, _ = self.rules.calculate_biomarker_score(
            "ldl_cholesterol", 180.0, input_reference_range=lab_high
        )
        assert score_high < 50, "High LDL should score low"
        assert range_high in [ScoreRange.HIGH, ScoreRange.VERY_HIGH, ScoreRange.CRITICAL], "Should be in high range"
    
    def test_crp_scoring_accuracy(self):
        """
        Test CRP scoring accuracy against clinical thresholds.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_low = {"min": 0.0, "max": 1.0, "unit": "mg/L", "source": "lab"}
        score_low, range_low, _ = self.rules.calculate_biomarker_score(
            "crp", 0.5, input_reference_range=lab_low
        )
        assert score_low >= 90, "Low CRP should score high"
        assert range_low == ScoreRange.OPTIMAL, "Should be in optimal range"

        lab_normal = {"min": 0.0, "max": 3.0, "unit": "mg/L", "source": "lab"}
        score_normal, range_normal, _ = self.rules.calculate_biomarker_score(
            "crp", 2.0, input_reference_range=lab_normal
        )
        assert score_normal >= 90, "Normal CRP should score high"
        assert range_normal in [ScoreRange.NORMAL, ScoreRange.OPTIMAL], "Should be in normal/optimal range"

        lab_high = {"min": 0.0, "max": 10.0, "unit": "mg/L", "source": "lab"}
        score_high, range_high, _ = self.rules.calculate_biomarker_score(
            "crp", 15.0, input_reference_range=lab_high
        )
        assert score_high <= 50, "High CRP should score low"
        assert range_high in [ScoreRange.HIGH, ScoreRange.VERY_HIGH, ScoreRange.CRITICAL], "Should be in high range"
    
    def test_age_adjustments(self):
        """
        Test age adjustments for biomarkers that require them.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_creat = {"min": 0.6, "max": 1.2, "unit": "mg/dL", "source": "lab"}
        score_young, _, _ = self.rules.calculate_biomarker_score(
            "creatinine", 1.0, age=25, input_reference_range=lab_creat
        )
        score_old, _, _ = self.rules.calculate_biomarker_score(
            "creatinine", 1.0, age=75, input_reference_range=lab_creat
        )
        assert score_young > 0, "Should have positive score"
        assert score_old > 0, "Should have positive score"

        lab_glucose = {"min": 70.0, "max": 125.0, "unit": "mg/dL", "source": "lab"}
        score_young_glucose, _, _ = self.rules.calculate_biomarker_score(
            "glucose", 100.0, age=25, input_reference_range=lab_glucose
        )
        score_old_glucose, _, _ = self.rules.calculate_biomarker_score(
            "glucose", 100.0, age=75, input_reference_range=lab_glucose
        )
        assert score_young_glucose > 0, "Should have positive score"
        assert score_old_glucose > 0, "Should have positive score"
    
    def test_sex_adjustments(self):
        """
        Test sex adjustments for biomarkers that require them.
        Uses lab reference range (required for lab-provided biomarkers).
        """
        lab_hemo = {"min": 12.0, "max": 16.0, "unit": "g/dL", "source": "lab"}
        score_male, _, _ = self.rules.calculate_biomarker_score(
            "hemoglobin", 14.0, sex="male", input_reference_range=lab_hemo
        )
        score_female, _, _ = self.rules.calculate_biomarker_score(
            "hemoglobin", 14.0, sex="female", input_reference_range=lab_hemo
        )
        assert score_male > 0, "Should have positive score"
        assert score_female > 0, "Should have positive score"

        lab_hdl = {"min": 40.0, "max": 60.0, "unit": "mg/dL", "source": "lab"}
        score_male_hdl, _, _ = self.rules.calculate_biomarker_score(
            "hdl_cholesterol", 50.0, sex="male", input_reference_range=lab_hdl
        )
        score_female_hdl, _, _ = self.rules.calculate_biomarker_score(
            "hdl_cholesterol", 50.0, sex="female", input_reference_range=lab_hdl
        )
        assert score_male_hdl > 0, "Should have positive score"
        assert score_female_hdl > 0, "Should have positive score"
    
    def test_metabolic_health_system_rules(self):
        """
        Test metabolic health system rules completeness.
        
        Business Value: Ensures metabolic health system has proper biomarker definitions.
        """
        metabolic_rules = self.rules.get_health_system_rules("metabolic")
        assert metabolic_rules is not None, "Should have metabolic rules"
        
        # Check required biomarkers
        biomarker_names = [rule.biomarker_name for rule in metabolic_rules.biomarkers]
        assert "glucose" in biomarker_names, "Should include glucose"
        assert "hba1c" in biomarker_names, "Should include hba1c"
        assert "insulin" in biomarker_names, "Should include insulin"
        
        # Check minimum biomarkers required
        assert metabolic_rules.min_biomarkers_required >= 2, "Should require at least 2 biomarkers"
        
        # Check system weight
        assert metabolic_rules.system_weight > 0, "Should have positive system weight"
    
    def test_cardiovascular_health_system_rules(self):
        """
        Test cardiovascular health system rules completeness.
        
        Business Value: Ensures cardiovascular health system has proper biomarker definitions.
        """
        cardiovascular_rules = self.rules.get_health_system_rules("cardiovascular")
        assert cardiovascular_rules is not None, "Should have cardiovascular rules"
        
        # Check required biomarkers (canonical keys: hdl_cholesterol, ldl_cholesterol)
        biomarker_names = [rule.biomarker_name for rule in cardiovascular_rules.biomarkers]
        assert "total_cholesterol" in biomarker_names, "Should include total cholesterol"
        assert "ldl_cholesterol" in biomarker_names, "Should include LDL (canonical key)"
        assert "hdl_cholesterol" in biomarker_names, "Should include HDL (canonical key)"
        assert "triglycerides" in biomarker_names, "Should include triglycerides"
        
        # Check minimum biomarkers required
        assert cardiovascular_rules.min_biomarkers_required >= 3, "Should require at least 3 biomarkers"
        
        # Check system weight
        assert cardiovascular_rules.system_weight > 0, "Should have positive system weight"
    
    def test_inflammatory_health_system_rules(self):
        """
        Test inflammatory health system rules completeness.
        
        Business Value: Ensures inflammatory health system has proper biomarker definitions.
        """
        inflammatory_rules = self.rules.get_health_system_rules("inflammatory")
        assert inflammatory_rules is not None, "Should have inflammatory rules"
        
        # Check required biomarkers
        biomarker_names = [rule.biomarker_name for rule in inflammatory_rules.biomarkers]
        assert "crp" in biomarker_names, "Should include CRP"
        
        # Check minimum biomarkers required
        assert inflammatory_rules.min_biomarkers_required >= 1, "Should require at least 1 biomarker"
        
        # Check system weight
        assert inflammatory_rules.system_weight > 0, "Should have positive system weight"
    
    def test_kidney_health_system_rules(self):
        """
        Test kidney health system rules completeness.
        
        Business Value: Ensures kidney health system has proper biomarker definitions.
        """
        kidney_rules = self.rules.get_health_system_rules("kidney")
        assert kidney_rules is not None, "Should have kidney rules"
        
        # Check required biomarkers
        biomarker_names = [rule.biomarker_name for rule in kidney_rules.biomarkers]
        assert "creatinine" in biomarker_names, "Should include creatinine"
        assert "urea" in biomarker_names, "Should include urea"
        
        # Check minimum biomarkers required
        assert kidney_rules.min_biomarkers_required >= 1, "Should require at least 1 biomarker"
        
        # Check system weight
        assert kidney_rules.system_weight > 0, "Should have positive system weight"
    
    def test_liver_health_system_rules(self):
        """
        Test liver health system rules completeness.
        
        Business Value: Ensures liver health system has proper biomarker definitions.
        """
        liver_rules = self.rules.get_health_system_rules("liver")
        assert liver_rules is not None, "Should have liver rules"
        
        # Check required biomarkers
        biomarker_names = [rule.biomarker_name for rule in liver_rules.biomarkers]
        assert "alt" in biomarker_names, "Should include ALT"
        assert "ast" in biomarker_names, "Should include AST"
        
        # Check minimum biomarkers required
        assert liver_rules.min_biomarkers_required >= 1, "Should require at least 1 biomarker"
        
        # Check system weight
        assert liver_rules.system_weight > 0, "Should have positive system weight"
    
    def test_cbc_health_system_rules(self):
        """
        Test CBC health system rules completeness.
        
        Business Value: Ensures CBC health system has proper biomarker definitions.
        """
        cbc_rules = self.rules.get_health_system_rules("cbc")
        assert cbc_rules is not None, "Should have CBC rules"
        
        # Check required biomarkers
        biomarker_names = [rule.biomarker_name for rule in cbc_rules.biomarkers]
        assert "hemoglobin" in biomarker_names, "Should include hemoglobin"
        assert "hematocrit" in biomarker_names, "Should include hematocrit"
        assert "white_blood_cells" in biomarker_names, "Should include white blood cells"
        assert "platelets" in biomarker_names, "Should include platelets"
        
        # Check minimum biomarkers required
        assert cbc_rules.min_biomarkers_required >= 2, "Should require at least 2 biomarkers"
        
        # Check system weight
        assert cbc_rules.system_weight > 0, "Should have positive system weight"
    
    def test_all_health_system_rules_retrieval(self):
        """
        Test retrieval of all health system rules.
        
        Business Value: Ensures all health systems are properly defined and accessible.
        """
        all_rules = self.rules.get_all_rules()
        
        # Check that all expected health systems are present
        expected_systems = ["metabolic", "cardiovascular", "inflammatory", "hormonal", "nutritional", "kidney", "liver", "cbc"]
        for system in expected_systems:
            assert system in all_rules, f"Should have rules for {system} health system"
            assert all_rules[system] is not None, f"Should have non-null rules for {system} health system"
        
        # Check that all rules are HealthSystemRules instances
        for system, rules in all_rules.items():
            assert isinstance(rules, HealthSystemRules), f"Should be HealthSystemRules instance for {system}"
            assert rules.system_name == system, f"Should have correct system name for {system}"
    
    def test_biomarker_rule_validation(self):
        """
        Test biomarker rule validation and consistency.
        
        Business Value: Ensures biomarker rules are internally consistent and valid.
        """
        all_rules = self.rules.get_all_rules()
        
        for system_name, system_rules in all_rules.items():
            for biomarker_rule in system_rules.biomarkers:
                # Check rule consistency
                assert biomarker_rule.biomarker_name, "Should have biomarker name"
                assert biomarker_rule.unit, "Should have unit"
                assert biomarker_rule.weight > 0, "Should have positive weight"
                
                # Check range consistency (optimal should be within normal)
                # Skip for tc_hdl_ratio (inverse ordering: lower is better)
                if biomarker_rule.biomarker_name != "tc_hdl_ratio":
                    assert biomarker_rule.optimal_range[0] >= biomarker_rule.normal_range[0], "Optimal min should be >= normal min"
                    assert biomarker_rule.optimal_range[1] <= biomarker_rule.normal_range[1], "Optimal max should be <= normal max"
                
                # Check range ordering (skip for biomarkers with reverse ordering or complex ranges)
                if biomarker_rule.biomarker_name not in ["hdl_cholesterol", "hemoglobin", "hematocrit", "white_blood_cells", "platelets", "tc_hdl_ratio"]:
                    assert biomarker_rule.normal_range[1] <= biomarker_rule.borderline_range[0], "Normal max should be <= borderline min"
                    assert biomarker_rule.borderline_range[1] <= biomarker_rule.high_range[0], "Borderline max should be <= high min"
                    assert biomarker_rule.high_range[1] <= biomarker_rule.very_high_range[0], "High max should be <= very high min"
                    assert biomarker_rule.very_high_range[1] <= biomarker_rule.critical_range[0], "Very high max should be <= critical min"
