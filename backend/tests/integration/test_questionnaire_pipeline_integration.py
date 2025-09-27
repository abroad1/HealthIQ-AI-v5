"""
Integration tests for questionnaire pipeline.

Tests the complete flow from questionnaire responses through the analysis pipeline.
"""

import pytest
from typing import Dict, Any

from core.pipeline.orchestrator import AnalysisOrchestrator
from core.models.questionnaire import QuestionnaireSubmission, create_questionnaire_validator
from core.pipeline.questionnaire_mapper import QuestionnaireMapper


class TestQuestionnairePipelineIntegration:
    """Test questionnaire integration with the analysis pipeline."""
    
    def setup_method(self):
        """Set up test data."""
        self.orchestrator = AnalysisOrchestrator()
        self.questionnaire_mapper = QuestionnaireMapper()
        self.questionnaire_validator = create_questionnaire_validator()
    
    def test_questionnaire_to_analysis_context_flow(self):
        """Test complete flow from questionnaire to analysis context."""
        # Sample questionnaire responses
        questionnaire_responses = {
            # Demographics
            "full_name": "John Doe",
            "email_address": "john@example.com",
            "date_of_birth": "1990-01-01",
            "biological_sex": "Male",
            "height": {"Feet": 5, "Inches": 10},
            "weight": {"Weight (lbs)": 180},
            "ethnicity": "Caucasian",

            # Lifestyle factors
            "dietary_pattern": "Mediterranean",
            "fruit_vegetable_servings": "6+ servings",
            "sugar_beverages_weekly": "None",
            "sleep_hours_nightly": "7-8 hours",
            "sleep_quality_rating": 8,
            "alcohol_consumption": "1-3 drinks",
            "smoking_status": "Never used",
            "stress_level_rating": 3,
            "stress_control_frequency": "Never",
            "major_life_stressors": "No major stressors",
            "vigorous_exercise_days": "4+ days",
            "resistance_training_days": "3+ days",
            "sitting_hours_daily": "7-9 hours",
            "caffeine_beverages_daily": "1-2",
            "daily_fluid_intake": "2-3 litres",

            # Medical history
            "chronic_conditions": ["Diabetes"],
            "current_medications": ["Metformin"],
            "family_cardiovascular_disease": ["Heart Disease"],
            "supplements": ["Vitamin D"],
            "sleep_disorders": ["Sleep apnea"],
            "food_sensitivities": ["Peanuts"]
        }
        
        # Sample biomarker data
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"},
            "hba1c": {"value": 5.2, "unit": "%"},
            "total_cholesterol": {"value": 180, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 45, "unit": "mg/dL"},
            "ldl_cholesterol": {"value": 110, "unit": "mg/dL"},
            "triglycerides": {"value": 120, "unit": "mg/dL"},
            "crp": {"value": 1.2, "unit": "mg/L"}
        }
        
        # Sample user data
        user_data = {
            "user_id": "test_user_123",
            "email": "john@example.com"
        }
        
        # Create analysis context with questionnaire data
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data,
            questionnaire_data=questionnaire_responses
        )
        
        # Verify context was created successfully
        assert context is not None
        assert context.analysis_id == "test_analysis_123"
        assert context.user is not None
        assert context.biomarker_panel is not None
        
        # Verify questionnaire data was processed
        assert context.user.questionnaire == questionnaire_responses
        
        # Verify lifestyle factors were mapped
        lifestyle_factors = context.user.lifestyle_factors
        assert lifestyle_factors["diet_level"] == "excellent"
        assert lifestyle_factors["sleep_hours"] == 7.5
        assert lifestyle_factors["exercise_minutes_per_week"] == 210
        assert lifestyle_factors["alcohol_units_per_week"] == 2
        assert lifestyle_factors["smoking_status"] == "never"
        assert lifestyle_factors["stress_level"] == "excellent"
        
        # Verify medical history was mapped
        medical_history = context.user.medical_history
        assert "Diabetes" in medical_history["conditions"]
        assert "Metformin" in medical_history["medications"]
        assert "Heart Disease" in medical_history["family_history"]
        assert "Vitamin D" in medical_history["supplements"]
        assert "Sleep apnea" in medical_history["sleep_disorders"]
        assert "Peanuts" in medical_history["allergies"]
        
        # Verify demographic data was extracted
        assert context.user.gender == "male"
        assert context.user.height == pytest.approx(177.8, rel=1e-2)  # 5'10" in cm
        assert context.user.weight == pytest.approx(81.6, rel=1e-2)   # 180 lbs in kg
        assert context.user.ethnicity == "Caucasian"
    
    def test_questionnaire_validation_in_pipeline(self):
        """Test questionnaire validation within the pipeline."""
        # Invalid questionnaire responses (missing required fields)
        invalid_questionnaire = {
            "full_name": "John Doe",
            # Missing required email_address, date_of_birth, biological_sex
            "sleep_hours_nightly": "7-8 hours"
        }
        
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"}
        }
        
        user_data = {
            "user_id": "test_user_123"
        }
        
        # Should not crash, but should log validation warnings
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data,
            questionnaire_data=invalid_questionnaire
        )
        
        # Context should still be created
        assert context is not None
        assert context.user.questionnaire == invalid_questionnaire
        
        # Should use default values for missing lifestyle factors
        lifestyle_factors = context.user.lifestyle_factors
        assert lifestyle_factors["diet_level"] == "average"  # Default
        assert lifestyle_factors["sleep_hours"] == 7.5  # From sleep_hours_nightly
        assert lifestyle_factors["exercise_minutes_per_week"] == 0  # Default
    
    def test_questionnaire_without_data(self):
        """Test pipeline behavior when no questionnaire data is provided."""
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"},
            "hba1c": {"value": 5.2, "unit": "%"}
        }
        
        user_data = {
            "user_id": "test_user_123",
            "email": "john@example.com",
            "age": 35,
            "gender": "male"
        }
        
        # Create context without questionnaire data
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data
            # No questionnaire_data parameter
        )
        
        # Context should be created successfully
        assert context is not None
        assert context.user.user_id == "test_user_123"
        assert context.user.email == "john@example.com"
        assert context.user.age == 35
        assert context.user.gender == "male"
        
        # Questionnaire field should be empty
        assert context.user.questionnaire == {}
        
        # Lifestyle factors should be empty (from user_data)
        assert context.user.lifestyle_factors == {}
    
    def test_questionnaire_scoring_integration(self):
        """Test questionnaire data integration with scoring engine."""
        # Comprehensive questionnaire responses
        questionnaire_responses = {
            # Demographics
            "date_of_birth": "1990-01-01",
            "biological_sex": "Male",
            "height": {"Feet": 5, "Inches": 10},
            "weight": {"Weight (lbs)": 180},
            
            # Lifestyle factors for scoring
            "dietary_pattern": "Mediterranean",
            "fruit_vegetable_servings": "6+ servings",
            "sugar_beverages_weekly": "None",
            "sleep_hours_nightly": "7-8 hours",
            "alcohol_consumption": "1-3 drinks",
            "smoking_status": "Never used",
            "stress_level_rating": 3,
            "stress_control_frequency": "Never",
            "major_life_stressors": "No major stressors",
            "vigorous_exercise_days": "4+ days",
            "resistance_training_days": "3+ days"
        }
        
        # Biomarker data for scoring
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"},
            "hba1c": {"value": 5.2, "unit": "%"},
            "total_cholesterol": {"value": 180, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 45, "unit": "mg/dL"},
            "ldl_cholesterol": {"value": 110, "unit": "mg/dL"},
            "triglycerides": {"value": 120, "unit": "mg/dL"},
            "crp": {"value": 1.2, "unit": "mg/L"}
        }
        
        user_data = {
            "user_id": "test_user_123"
        }
        
        # Create analysis context
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data,
            questionnaire_data=questionnaire_responses
        )
        
        # Test scoring with lifestyle data
        lifestyle_data = {
            "diet_level": context.user.lifestyle_factors["diet_level"],
            "sleep_hours": context.user.lifestyle_factors["sleep_hours"],
            "exercise_minutes_per_week": context.user.lifestyle_factors["exercise_minutes_per_week"],
            "alcohol_units_per_week": context.user.lifestyle_factors["alcohol_units_per_week"],
            "smoking_status": context.user.lifestyle_factors["smoking_status"],
            "stress_level": context.user.lifestyle_factors["stress_level"]
        }
        
        # Score biomarkers with lifestyle adjustments
        scoring_result = self.orchestrator.score_biomarkers(
            biomarkers=biomarker_data,
            age=35,
            sex="male",
            lifestyle_data=lifestyle_data
        )
        
        # Verify scoring was successful
        assert scoring_result is not None
        assert "overall_score" in scoring_result
        assert "health_system_scores" in scoring_result
        assert "lifestyle_adjustments" in scoring_result
        
        # Verify lifestyle adjustments were applied
        assert scoring_result["lifestyle_adjustments"] is not None
        assert len(scoring_result["lifestyle_adjustments"]) > 0
    
    def test_questionnaire_mapper_integration(self):
        """Test questionnaire mapper integration with real data."""
        # Realistic questionnaire responses
        questionnaire_responses = {
            # Demographics
            "full_name": "Jane Smith",
            "email_address": "jane@example.com",
            "date_of_birth": "1985-06-15",
            "biological_sex": "Female",
            "height": {"Feet": 5, "Inches": 6},
            "weight": {"Weight (lbs)": 140},
            "ethnicity": "Asian",
            
            # Lifestyle
            "dietary_pattern": "Plant-based",
            "fruit_vegetable_servings": "4-5 servings",
            "sugar_beverages_weekly": "1-3 drinks",
            "sleep_hours_nightly": "5-6 hours",
            "sleep_quality_rating": 6,
            "alcohol_consumption": "4-7 drinks",
            "smoking_status": "Former user quit >1 year",
            "stress_level_rating": 7,
            "stress_control_frequency": "Sometimes",
            "major_life_stressors": "2-3 major stressors",
            "vigorous_exercise_days": "2 days",
            "resistance_training_days": "1 day",
            "sitting_hours_daily": "10-12 hours",
            "caffeine_beverages_daily": "3-4",
            "daily_fluid_intake": "1-2 litres",
            
            # Medical
            "chronic_conditions": ["Hypertension", "Anxiety"],
            "current_medications": ["Lisinopril", "Sertraline"],
            "family_cardiovascular_disease": ["Diabetes", "Heart Disease"],
            "supplements": ["Multivitamin", "Vitamin D"],
            "sleep_disorders": ["Mild snoring"],
            "food_sensitivities": ["Dairy", "Gluten"]
        }
        
        # Test mapper directly
        submission = QuestionnaireSubmission(
            responses=questionnaire_responses,
            submission_id="integration_test"
        )
        
        lifestyle_factors, medical_history = self.questionnaire_mapper.map_submission(submission)
        
        # Verify lifestyle factors
        assert lifestyle_factors.diet_level.value == "good"  # Plant-based + 4-5 servings
        assert lifestyle_factors.sleep_hours == 5.5  # 5-6 hours
        assert lifestyle_factors.exercise_minutes_per_week == 90  # 2 days vigorous + 1 day resistance
        assert lifestyle_factors.alcohol_units_per_week == 5  # 4-7 drinks
        assert lifestyle_factors.smoking_status == "former"  # Former user
        assert lifestyle_factors.stress_level.value == "poor"  # High stress + poor control + stressors
        assert lifestyle_factors.sedentary_hours_per_day == 11.0  # 10-12 hours
        assert lifestyle_factors.caffeine_consumption == 3  # 3-4
        assert lifestyle_factors.fluid_intake_liters == 1.5  # 1-2 litres
        
        # Verify medical history
        assert "Hypertension" in medical_history.conditions
        assert "Anxiety" in medical_history.conditions
        assert "Lisinopril" in medical_history.medications
        assert "Sertraline" in medical_history.medications
        assert "Diabetes" in medical_history.family_history
        assert "Heart Disease" in medical_history.family_history
        assert "Multivitamin" in medical_history.supplements
        assert "Vitamin D" in medical_history.supplements
        assert "Mild snoring" in medical_history.sleep_disorders
        assert "Dairy" in medical_history.allergies
        assert "Gluten" in medical_history.allergies
        
        # Test demographic extraction
        demographics = self.questionnaire_mapper.get_demographic_data(questionnaire_responses)
        assert demographics["gender"] == "female"
        assert demographics["height"] == pytest.approx(167.6, rel=1e-2)  # 5'6" in cm
        assert demographics["weight"] == pytest.approx(63.5, rel=1e-2)   # 140 lbs in kg
        assert demographics["ethnicity"] == "Asian"


class TestQuestionnaireErrorHandling:
    """Test error handling in questionnaire pipeline."""
    
    def setup_method(self):
        """Set up test data."""
        self.orchestrator = AnalysisOrchestrator()
    
    def test_questionnaire_with_malformed_data(self):
        """Test handling of malformed questionnaire data."""
        # Malformed questionnaire data
        malformed_questionnaire = {
            "full_name": 123,  # Should be string
            "sleep_hours_nightly": "Invalid option",  # Not in options
            "stress_level_rating": "not a number",  # Should be number
            "height": "not a dict"  # Should be group/dict
        }
        
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"}
        }
        
        user_data = {
            "user_id": "test_user_123"
        }
        
        # Should not crash
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data,
            questionnaire_data=malformed_questionnaire
        )
        
        # Context should still be created
        assert context is not None
        assert context.user.questionnaire == malformed_questionnaire
        
        # Should use default values for lifestyle factors
        lifestyle_factors = context.user.lifestyle_factors
        assert lifestyle_factors["diet_level"] == "average"  # Default
        assert lifestyle_factors["sleep_hours"] == 7.0  # Default
        assert lifestyle_factors["stress_level"] == "average"  # Default
    
    def test_questionnaire_with_empty_strings(self):
        """Test handling of empty string responses."""
        empty_questionnaire = {
            "full_name": "",
            "email_address": "",
            "sleep_hours_nightly": "",
            "alcohol_consumption": ""
        }
        
        biomarker_data = {
            "glucose": {"value": 95, "unit": "mg/dL"}
        }
        
        user_data = {
            "user_id": "test_user_123"
        }
        
        # Should not crash
        context = self.orchestrator.create_analysis_context(
            analysis_id="test_analysis_123",
            raw_biomarkers=biomarker_data,
            user_data=user_data,
            questionnaire_data=empty_questionnaire
        )
        
        # Context should still be created
        assert context is not None
        assert context.user.questionnaire == empty_questionnaire
        
        # Should use default values
        lifestyle_factors = context.user.lifestyle_factors
        assert lifestyle_factors["diet_level"] == "average"
        assert lifestyle_factors["sleep_hours"] == 7.0
        assert lifestyle_factors["alcohol_units_per_week"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
