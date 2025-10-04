"""
Unit tests for AnalysisContext enhancement with questionnaire fields.
"""

import pytest
from datetime import datetime, UTC
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.pipeline.context_factory import AnalysisContextFactory


class TestAnalysisContextEnhancement:
    """Test enhanced AnalysisContext with questionnaire fields."""
    
    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            user_id="test_user_123",
            email="test@example.com",
            age=35,
            gender="male",
            height=175.0,
            weight=70.0,
            ethnicity="white",
            medical_history={},
            medications=[],
            lifestyle_factors={},
            questionnaire={},
            created_at=datetime.now(UTC).isoformat(),
            updated_at=datetime.now(UTC).isoformat()
        )
    
    @pytest.fixture
    def sample_biomarker_panel(self):
        """Create a sample biomarker panel for testing."""
        biomarkers = {
            "total_cholesterol": BiomarkerValue(
                name="total_cholesterol",
                value=180.0,
                unit="mg/dL"
            ),
            "hdl_cholesterol": BiomarkerValue(
                name="hdl_cholesterol", 
                value=45.0,
                unit="mg/dL"
            )
        }
        return BiomarkerPanel(biomarkers=biomarkers)
    
    @pytest.fixture
    def sample_questionnaire_responses(self):
        """Create sample questionnaire responses."""
        return {
            "diet_quality_rating": 8,
            "exercise_frequency": "4+ days per week",
            "sleep_hours_nightly": "7-8 hours",
            "stress_level_rating": 4,
            "tobacco_use": "Never used",
            "alcohol_drinks_weekly": "1-3 drinks",
            "chronic_conditions": ["None"],
            "current_medications": "None"
        }
    
    @pytest.fixture
    def sample_lifestyle_factors(self):
        """Create sample lifestyle factors."""
        return {
            "diet_level": "good",
            "sleep_hours": 7.5,
            "exercise_minutes_per_week": 180,
            "alcohol_units_per_week": 2,
            "smoking_status": "never",
            "stress_level": "good",
            "sedentary_hours_per_day": 8.0,
            "caffeine_consumption": 3,
            "fluid_intake_liters": 2.5
        }
    
    @pytest.fixture
    def sample_medical_history(self):
        """Create sample medical history."""
        return {
            "conditions": ["None"],
            "medications": ["None"],
            "family_history": [],
            "supplements": ["Vitamin D", "Omega-3"],
            "sleep_disorders": [],
            "allergies": [],
            "atrial_fibrillation": False,
            "rheumatoid_arthritis": False,
            "systemic_lupus": False,
            "corticosteroids": False,
            "atypical_antipsychotics": False,
            "hiv_treatments": False,
            "migraines": False
        }
    
    def test_analysis_context_with_questionnaire_fields(
        self, 
        sample_user, 
        sample_biomarker_panel,
        sample_questionnaire_responses,
        sample_lifestyle_factors,
        sample_medical_history
    ):
        """Test AnalysisContext creation with questionnaire fields."""
        context = AnalysisContext(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            questionnaire_responses=sample_questionnaire_responses,
            lifestyle_factors=sample_lifestyle_factors,
            medical_history=sample_medical_history,
            analysis_parameters={"test_param": "test_value"},
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
        
        # Verify all fields are present
        assert context.analysis_id == "test_analysis_123"
        assert context.user == sample_user
        assert context.biomarker_panel == sample_biomarker_panel
        assert context.questionnaire_responses == sample_questionnaire_responses
        assert context.lifestyle_factors == sample_lifestyle_factors
        assert context.medical_history == sample_medical_history
        assert context.analysis_parameters == {"test_param": "test_value"}
        assert context.version == "1.0"
    
    def test_analysis_context_without_questionnaire_fields(
        self, 
        sample_user, 
        sample_biomarker_panel
    ):
        """Test AnalysisContext creation without questionnaire fields (backward compatibility)."""
        context = AnalysisContext(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            analysis_parameters={"test_param": "test_value"},
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
        
        # Verify questionnaire fields are None by default
        assert context.questionnaire_responses is None
        assert context.lifestyle_factors is None
        assert context.medical_history is None
        
        # Verify other fields are present
        assert context.analysis_id == "test_analysis_123"
        assert context.user == sample_user
        assert context.biomarker_panel == sample_biomarker_panel
    
    def test_context_factory_with_questionnaire_fields(
        self,
        sample_user,
        sample_biomarker_panel,
        sample_questionnaire_responses,
        sample_lifestyle_factors,
        sample_medical_history
    ):
        """Test AnalysisContextFactory with questionnaire fields."""
        context = AnalysisContextFactory.create_context(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            questionnaire_responses=sample_questionnaire_responses,
            lifestyle_factors=sample_lifestyle_factors,
            medical_history=sample_medical_history,
            analysis_parameters={"test_param": "test_value"}
        )
        
        # Verify all fields are correctly set
        assert context.analysis_id == "test_analysis_123"
        assert context.questionnaire_responses == sample_questionnaire_responses
        assert context.lifestyle_factors == sample_lifestyle_factors
        assert context.medical_history == sample_medical_history
        assert context.analysis_parameters == {"test_param": "test_value"}
        assert context.version == "1.0"
        assert context.created_at is not None
    
    def test_context_factory_backward_compatibility(
        self,
        sample_user,
        sample_biomarker_panel
    ):
        """Test AnalysisContextFactory backward compatibility."""
        context = AnalysisContextFactory.create_context(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            analysis_parameters={"test_param": "test_value"}
        )
        
        # Verify questionnaire fields are None by default
        assert context.questionnaire_responses is None
        assert context.lifestyle_factors is None
        assert context.medical_history is None
        
        # Verify other fields are present
        assert context.analysis_id == "test_analysis_123"
        assert context.user == sample_user
        assert context.biomarker_panel == sample_biomarker_panel
    
    def test_analysis_context_immutability(
        self,
        sample_user,
        sample_biomarker_panel,
        sample_questionnaire_responses
    ):
        """Test that AnalysisContext remains immutable."""
        from pydantic import ValidationError
        
        context = AnalysisContext(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            questionnaire_responses=sample_questionnaire_responses,
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
        
        # Attempting to modify should raise an error
        with pytest.raises(ValidationError):
            context.analysis_id = "modified_id"
        
        # Verify the context is properly constructed
        assert context.analysis_id == "test_analysis_123"
        assert context.questionnaire_responses is not None
        assert len(context.questionnaire_responses) > 0
    
    def test_analysis_context_with_partial_questionnaire_data(
        self,
        sample_user,
        sample_biomarker_panel,
        sample_questionnaire_responses
    ):
        """Test AnalysisContext with only questionnaire responses (no lifestyle/medical mapping)."""
        context = AnalysisContext(
            analysis_id="test_analysis_123",
            user=sample_user,
            biomarker_panel=sample_biomarker_panel,
            questionnaire_responses=sample_questionnaire_responses,
            created_at=datetime.now(UTC).isoformat(),
            version="1.0"
        )
        
        # Verify questionnaire responses are present
        assert context.questionnaire_responses == sample_questionnaire_responses
        
        # Verify lifestyle and medical history are None
        assert context.lifestyle_factors is None
        assert context.medical_history is None
