"""
Integration tests for questionnaire mapper integration in orchestrator pipeline.
"""

import pytest
from datetime import datetime, UTC
from core.pipeline.orchestrator import AnalysisOrchestrator
from core.pipeline.context_factory import AnalysisContextFactory
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


class TestQuestionnairePipelineIntegration:
    """Test questionnaire mapper integration in the orchestrator pipeline."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create an analysis orchestrator instance."""
        return AnalysisOrchestrator()
    
    @pytest.fixture
    def sample_questionnaire_responses(self):
        """Create sample questionnaire responses."""
        return {
            "biological_sex": "Male",
            "date_of_birth": "1988-05-15",
            "height": {"Feet": 5, "Inches": 10},
            "weight": {"Weight (lbs)": 175},
            "ethnicity": "White/Caucasian",
            "diet_quality_rating": 8,
            "sleep_hours_nightly": "7-8 hours",
            "alcohol_drinks_weekly": "1-3 drinks",
            "tobacco_use": "Never used",
            "chronic_conditions": ["None"],
            "current_medications": "None"
        }
    
    @pytest.fixture
    def sample_biomarkers(self):
        """Create sample biomarker data."""
        return {
            "total_cholesterol": {"value": 180, "unit": "mg/dL"},
            "hdl_cholesterol": {"value": 45, "unit": "mg/dL"}
        }
    
    def test_orchestrator_with_questionnaire_data(
        self,
        orchestrator,
        sample_questionnaire_responses,
        sample_biomarkers
    ):
        """Test orchestrator processing with questionnaire data."""
        context = orchestrator.create_analysis_context(
            analysis_id="test_integration_123",
            raw_biomarkers=sample_biomarkers,
            user_data={},
            questionnaire_data=sample_questionnaire_responses
        )
        
        # Verify questionnaire data is properly integrated
        assert context.questionnaire_responses is not None
        assert context.lifestyle_factors is not None
        assert context.medical_history is not None
        
        # Verify questionnaire responses are preserved
        assert context.questionnaire_responses["biological_sex"] == "Male"
        assert context.questionnaire_responses["diet_quality_rating"] == 8
    
    def test_orchestrator_without_questionnaire_data(
        self,
        orchestrator,
        sample_biomarkers
    ):
        """Test orchestrator processing without questionnaire data."""
        context = orchestrator.create_analysis_context(
            analysis_id="test_no_questionnaire_123",
            raw_biomarkers=sample_biomarkers,
            user_data={}
        )
        
        # Verify questionnaire fields are None
        assert context.questionnaire_responses is None
        assert context.lifestyle_factors is None
        assert context.medical_history is None
    
    def test_questionnaire_mapping_accuracy(
        self,
        orchestrator,
        sample_questionnaire_responses,
        sample_biomarkers
    ):
        """Test accuracy of questionnaire mapping."""
        context = orchestrator.create_analysis_context(
            analysis_id="test_mapping_123",
            raw_biomarkers=sample_biomarkers,
            user_data={},
            questionnaire_data=sample_questionnaire_responses
        )
        
        lifestyle = context.lifestyle_factors
        
        # Test sleep hours mapping
        assert lifestyle["sleep_hours"] == 7.5
        
        # Test alcohol mapping
        assert lifestyle["alcohol_units_per_week"] == 2
        
        # Test smoking status
        assert lifestyle["smoking_status"] == "never"