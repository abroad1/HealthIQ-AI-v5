"""
Unit tests for questionnaire mapper.

Tests the mapping of questionnaire responses to lifestyle factors and medical history.
"""

import pytest
from typing import Dict, Any

from core.pipeline.questionnaire_mapper import (
    QuestionnaireMapper,
    MappedLifestyleFactors,
    MappedMedicalHistory,
    LifestyleLevel
)
from core.models.questionnaire import QuestionnaireSubmission


class TestQuestionnaireMapper:
    """Test questionnaire mapping functionality."""
    
    def setup_method(self):
        """Set up test data."""
        self.mapper = QuestionnaireMapper()
    
    def test_map_diet_level_excellent(self):
        """Test mapping excellent diet level."""
        responses = {
            "dietary_pattern": "Mediterranean",  # Dietary pattern
            "fruit_vegetable_servings": "6+ servings",    # Fruit and vegetables
            "sugar_beverages_weekly": "None"            # Sugar-sweetened beverages
        }
        
        lifestyle_factors, _ = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        assert lifestyle_factors.diet_level == LifestyleLevel.EXCELLENT
    
    def test_map_diet_level_poor(self):
        """Test mapping poor diet level."""
        responses = {
            "dietary_pattern": "None",           # No specific pattern
            "fruit_vegetable_servings": "0-1 servings",   # Low fruit and vegetables
            "sugar_beverages_weekly": "15+ drinks"      # High sugar beverages
        }
        
        lifestyle_factors, _ = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        assert lifestyle_factors.diet_level == LifestyleLevel.VERY_POOR
    
    def test_map_sleep_hours(self):
        """Test mapping sleep hours from questionnaire responses."""
        test_cases = [
            ("Less than 5 hours", 4.5),
            ("5-6 hours", 5.5),
            ("7-8 hours", 7.5),
            ("9+ hours", 9.0)
        ]
        
        for sleep_range, expected_hours in test_cases:
            responses = {"sleep_hours_nightly": sleep_range}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.sleep_hours == expected_hours
    
    def test_map_exercise_minutes(self):
        """Test mapping exercise minutes per week."""
        responses = {
            "vigorous_exercise_days": "4+ days",  # Vigorous exercise
            "resistance_training_days": "3+ days"   # Resistance training
        }
        
        lifestyle_factors, _ = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        # 4 days * 30 min + 3 days * 30 min = 210 minutes
        assert lifestyle_factors.exercise_minutes_per_week == 210
    
    def test_map_alcohol_consumption(self):
        """Test mapping alcohol consumption to units per week."""
        test_cases = [
            ("None", 0),
            ("1-3 drinks", 2),
            ("4-7 drinks", 5),
            ("8-14 drinks", 11),
            ("15+ drinks", 20)
        ]
        
        for consumption, expected_units in test_cases:
            responses = {"alcohol_drinks_weekly": consumption}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.alcohol_units_per_week == expected_units
    
    def test_map_smoking_status(self):
        """Test mapping smoking status."""
        test_cases = [
            ("Never used", "never"),
            ("Former user quit >1 year", "former"),
            ("Former user quit <1 year", "former"),
            ("Occasional use", "current"),
            ("Daily use", "current")
        ]
        
        for status, expected in test_cases:
            responses = {"tobacco_use": status}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.smoking_status == expected
    
    def test_map_stress_level_excellent(self):
        """Test mapping excellent stress level."""
        responses = {
            "stress_level_rating": 2,                    # Low stress level
            "stress_control_frequency": "Never",              # Good control
            "major_life_stressors": "No major stressors"  # No major stressors
        }
        
        lifestyle_factors, _ = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        assert lifestyle_factors.stress_level == LifestyleLevel.EXCELLENT
    
    def test_map_stress_level_very_poor(self):
        """Test mapping very poor stress level."""
        responses = {
            "stress_level_rating": 10,                   # High stress level
            "stress_control_frequency": "Very often",         # Poor control
            "major_life_stressors": "4+ major stressors"  # Many stressors
        }
        
        lifestyle_factors, _ = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        assert lifestyle_factors.stress_level == LifestyleLevel.VERY_POOR
    
    def test_map_sedentary_hours(self):
        """Test mapping sedentary hours per day."""
        test_cases = [
            ("Less than 4 hours", 3.0),
            ("4-6 hours", 5.0),
            ("7-9 hours", 8.0),
            ("10-12 hours", 11.0),
            ("13+ hours", 14.0)
        ]
        
        for sitting_time, expected_hours in test_cases:
            responses = {"sitting_hours_daily": sitting_time}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.sedentary_hours_per_day == expected_hours
    
    def test_map_caffeine_consumption(self):
        """Test mapping caffeine consumption."""
        test_cases = [
            ("None", 0),
            ("1-2", 1),
            ("3-4", 3),
            ("5-6", 5),
            ("7+", 8)
        ]
        
        for consumption, expected in test_cases:
            responses = {"caffeine_beverages_daily": consumption}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.caffeine_consumption == expected
    
    def test_map_fluid_intake(self):
        """Test mapping fluid intake."""
        test_cases = [
            ("Less than 1 litre", 0.5),
            ("1-2 litres", 1.5),
            ("2-3 litres", 2.5),
            ("More than 3 litres", 3.5)
        ]
        
        for intake, expected in test_cases:
            responses = {"daily_fluid_intake": intake}
            lifestyle_factors, _ = self.mapper.map_submission(
                QuestionnaireSubmission(responses=responses, submission_id="test")
            )
            
            assert lifestyle_factors.fluid_intake_liters == expected
    
    def test_map_medical_history(self):
        """Test mapping medical history from questionnaire responses."""
        responses = {
            "chronic_conditions": ["Diabetes", "Hypertension"],  # Medical conditions
            "current_medications": "3-5 medications",  # SSOT dropdown: coarse band
            "family_cardiovascular_disease": ["Heart Disease"],   # Family history
            "family_cancer_history": ["Cancer"],   # Family history
            "supplements": ["Vitamin D", "Omega-3"],      # Supplements
            "sleep_disorders": ["Sleep apnea"],               # Sleep disorders
            "food_sensitivities": ["Peanuts", "Shellfish"]       # Allergies
        }
        
        _, medical_history = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="test")
        )
        
        assert medical_history.conditions == ["Diabetes", "Hypertension"]
        assert medical_history.medications == ["3-5 medications"]
        assert "Heart Disease" in medical_history.family_history
        assert "Cancer" in medical_history.family_history
        assert medical_history.supplements == ["Vitamin D", "Omega-3"]
        assert medical_history.sleep_disorders == ["Sleep apnea"]
        assert medical_history.allergies == ["Peanuts", "Shellfish"]
    
    def test_map_demographic_data(self):
        """Test mapping demographic data from questionnaire responses."""
        responses = {
            "date_of_birth": "1990-01-01",  # Date of birth
            "biological_sex": "Male",        # Sex
            "height": {"Feet": 5, "Inches": 10},  # Height
            "weight": {"Weight (lbs)": 180},      # Weight
            "ethnicity": "Caucasian"   # Ethnicity
        }
        
        demographics = self.mapper.get_demographic_data(responses)
        
        assert demographics["gender"] == "male"
        assert demographics["height"] == pytest.approx(177.8, rel=1e-2)  # 5'10" in cm
        assert demographics["weight"] == pytest.approx(81.6, rel=1e-2)   # 180 lbs in kg
        assert demographics["ethnicity"] == "Caucasian"
    
    def test_map_complete_submission(self):
        """Test mapping a complete questionnaire submission."""
        responses = {
            # Demographics
            "date_of_birth": "1990-01-01",
            "biological_sex": "Male",
            "height": {"Feet": 5, "Inches": 10},
            "weight": {"Weight (lbs)": 180},
            "ethnicity": "Caucasian",
            
            # Lifestyle
            "dietary_pattern": "Mediterranean",
            "fruit_vegetable_servings": "6+ servings",
            "sugar_beverages_weekly": "None",
            "sleep_hours_nightly": "7-8 hours",
            "sleep_quality_rating": 8,
            "alcohol_drinks_weekly": "1-3 drinks",
            "tobacco_use": "Never used",
            "stress_level_rating": 3,
            "stress_control_frequency": "Never",
            "major_life_stressors": "No major stressors",
            "vigorous_exercise_days": "4+ days",
            "resistance_training_days": "3+ days",
            "sitting_hours_daily": "7-9 hours",
            "caffeine_beverages_daily": "1-2",
            "daily_fluid_intake": "2-3 litres",
            
            # Medical
            "chronic_conditions": ["Diabetes"],
            "current_medications": "1-2 medications",
            "family_cardiovascular_disease": ["Heart Disease"],
            "supplements": ["Vitamin D"],
            "sleep_disorders": ["Sleep apnea"],
            "food_sensitivities": ["Peanuts"]
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="complete_test"
        )
        
        lifestyle_factors, medical_history = self.mapper.map_submission(submission)
        
        # Verify lifestyle factors
        assert lifestyle_factors.diet_level == LifestyleLevel.EXCELLENT
        assert lifestyle_factors.sleep_hours == 7.5
        assert lifestyle_factors.exercise_minutes_per_week == 210
        assert lifestyle_factors.alcohol_units_per_week == 2
        assert lifestyle_factors.smoking_status == "never"
        assert lifestyle_factors.stress_level == LifestyleLevel.EXCELLENT
        assert lifestyle_factors.sedentary_hours_per_day == 8.0
        assert lifestyle_factors.caffeine_consumption == 1
        assert lifestyle_factors.fluid_intake_liters == 2.5
        
        # Verify medical history
        assert medical_history.conditions == ["Diabetes"]
        assert medical_history.medications == ["1-2 medications"]
        assert medical_history.family_history == ["Heart Disease"]
        assert medical_history.supplements == ["Vitamin D"]
        assert medical_history.sleep_disorders == ["Sleep apnea"]
        assert medical_history.allergies == ["Peanuts"]
    
    def test_long_term_medication_classes_and_qrisk_flags(self):
        """SSOT long_term_medications classes and QRISK booleans map deterministically."""
        responses = {
            "chronic_conditions": ["None"],
            "current_medications": "None",
            "long_term_medications": ["Corticosteroids", "HIV/AIDS treatments"],
            "medical_conditions": ["Atrial fibrillation", "Rheumatoid arthritis"],
            "regular_migraines": "Yes",
            "supplements": ["Vitamin D"],
        }
        _, mh = self.mapper.map_submission(
            QuestionnaireSubmission(responses=responses, submission_id="qrisk_test")
        )
        assert mh.long_term_medication_classes == ["Corticosteroids", "HIV/AIDS treatments"]
        assert mh.corticosteroids is True
        assert mh.hiv_treatments is True
        assert mh.atrial_fibrillation is True
        assert mh.rheumatoid_arthritis is True
        assert mh.migraines is True
        assert mh.systemic_lupus is False
        assert mh.atypical_antipsychotics is False
    
    def test_parse_checkbox_response(self):
        """Test parsing checkbox responses."""
        # Test list response
        result = self.mapper._parse_checkbox_response(["Option1", "Option2"])
        assert result == ["Option1", "Option2"]
        
        # Test string response
        result = self.mapper._parse_checkbox_response("Single Option")
        assert result == ["Single Option"]
        
        # Test invalid response
        result = self.mapper._parse_checkbox_response(None)
        assert result == []
        
        # Test number response
        result = self.mapper._parse_checkbox_response(123)
        assert result == []


class TestQuestionnaireMapperEdgeCases:
    """Test edge cases and error handling in questionnaire mapper."""
    
    def setup_method(self):
        """Set up test data."""
        self.mapper = QuestionnaireMapper()
    
    def test_map_with_missing_responses(self):
        """Test mapping with missing questionnaire responses."""
        responses = {
            "sleep_hours_nightly": "7-8 hours",  # Only sleep data
            "alcohol_drinks_weekly": "None"        # Only alcohol data
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="partial_test"
        )
        
        lifestyle_factors, medical_history = self.mapper.map_submission(submission)
        
        # Should use default values for missing data
        assert lifestyle_factors.sleep_hours == 7.5
        assert lifestyle_factors.alcohol_units_per_week == 0
        assert lifestyle_factors.diet_level == LifestyleLevel.AVERAGE  # Default
        assert lifestyle_factors.exercise_minutes_per_week == 0  # Default
        assert lifestyle_factors.smoking_status == "never"  # Default
        assert lifestyle_factors.stress_level == LifestyleLevel.AVERAGE  # Default
    
    def test_map_with_empty_responses(self):
        """Test mapping with empty questionnaire responses."""
        responses = {}
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="empty_test"
        )
        
        lifestyle_factors, medical_history = self.mapper.map_submission(submission)
        
        # Should use all default values
        assert lifestyle_factors.diet_level == LifestyleLevel.AVERAGE
        assert lifestyle_factors.sleep_hours == 7.0
        assert lifestyle_factors.exercise_minutes_per_week == 0
        assert lifestyle_factors.alcohol_units_per_week == 5
        assert lifestyle_factors.smoking_status == "never"
        assert lifestyle_factors.stress_level == LifestyleLevel.AVERAGE
        
        # Medical history should be empty
        assert medical_history.conditions == []
        assert medical_history.medications == []
        assert medical_history.family_history == []
        assert medical_history.supplements == []
        assert medical_history.long_term_medication_classes == []
        assert medical_history.sleep_disorders == []
        assert medical_history.allergies == []
    
    def test_map_with_invalid_responses(self):
        """Test mapping with invalid questionnaire responses."""
        responses = {
            "sleep_hours_nightly": "Invalid sleep range",  # Invalid option
            "alcohol_drinks_weekly": "Invalid alcohol option",  # Invalid option
            "stress_level_rating": "not a number"  # Invalid type
        }
        
        submission = QuestionnaireSubmission(
            responses=responses,
            submission_id="invalid_test"
        )
        
        # Should not crash and use default values
        lifestyle_factors, medical_history = self.mapper.map_submission(submission)
        
        assert lifestyle_factors.sleep_hours == 7.0  # Default
        assert lifestyle_factors.alcohol_units_per_week == 5  # Default
        assert lifestyle_factors.stress_level == LifestyleLevel.AVERAGE  # Default


class TestObjectiveLifestyleExtraction:
    """CONTEXT-HARDENING-B — objective questionnaire → LifestyleModifierEngine keys."""

    def setup_method(self):
        self.mapper = QuestionnaireMapper()

    def test_waist_numeric_is_inches_converted_to_cm(self):
        out = self.mapper.extract_objective_lifestyle_inputs({"waist_circumference": 35.0})
        assert abs(out["waist_circumference_cm"] - 35.0 * 2.54) < 1e-6

    def test_waist_dict_cm_key_direct(self):
        out = self.mapper.extract_objective_lifestyle_inputs(
            {"waist_circumference": {"Waist circumference (cm)": 92.0}}
        )
        assert out["waist_circumference_cm"] == 92.0

    def test_bp_group_extracted(self):
        out = self.mapper.extract_objective_lifestyle_inputs({
            "blood_pressure_reading": {
                "Systolic (mmHg)": 128,
                "Diastolic (mmHg)": 82,
            }
        })
        assert out["systolic_bp"] == 128.0
        assert out["diastolic_bp"] == 82.0

    def test_bp_absent_empty(self):
        out = self.mapper.extract_objective_lifestyle_inputs({})
        assert "systolic_bp" not in out
        assert "diastolic_bp" not in out

    def test_bp_partial_sys_only(self):
        out = self.mapper.extract_objective_lifestyle_inputs({
            "blood_pressure_reading": {"Systolic (mmHg)": 118}
        })
        assert out["systolic_bp"] == 118.0
        assert "diastolic_bp" not in out

    def test_bp_zero_omitted(self):
        out = self.mapper.extract_objective_lifestyle_inputs({
            "blood_pressure_reading": {"Systolic (mmHg)": 0, "Diastolic (mmHg)": 70}
        })
        assert "systolic_bp" not in out
        assert out["diastolic_bp"] == 70.0


class TestBehaviouralLifestyleExtraction:
    """CONTEXT-HARDENING-C — behavioural questionnaire → LifestyleModifierEngine keys."""

    def setup_method(self):
        self.mapper = QuestionnaireMapper()

    def test_extract_behavioural_empty_without_fields(self):
        assert self.mapper.extract_behavioural_lifestyle_inputs({}) == {}

    def test_smoking_daily_use_is_current(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs({"tobacco_use": "Daily use"})
        assert out == {"smoking_status": "current"}

    def test_smoking_former_long_quit(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs(
            {"tobacco_use": "Former user quit >1 year"}
        )
        assert out == {"smoking_status": "former"}

    def test_smoking_never_used(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs({"tobacco_use": "Never used"})
        assert out == {"smoking_status": "never"}

    def test_alcohol_mid_bucket(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs(
            {"alcohol_drinks_weekly": "8-14 drinks"}
        )
        assert out == {"alcohol_units_per_week": 11.0}

    def test_sleep_short_bucket(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs(
            {"sleep_hours_nightly": "Less than 5 hours"}
        )
        assert out == {"sleep_hours": 4.5}

    def test_unknown_sleep_option_omitted(self):
        out = self.mapper.extract_behavioural_lifestyle_inputs(
            {"sleep_hours_nightly": "Invalid sleep range"}
        )
        assert "sleep_hours" not in out


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
