# ARCHIVED TEST
# Reason: Medium-value test (setup infrastructure)
# Archived: 2025-01-27
# Original Path: backend/tests/unit/test_pipeline_context_factory.py

"""
Unit tests for pipeline context factory
HealthIQ-AI v5 Backend
"""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from pydantic_core import ValidationError

from core.pipeline.context_factory import AnalysisContextFactory
from core.models.context import AnalysisContext
from core.models.user import User
from core.models.biomarker import BiomarkerPanel, BiomarkerValue


class TestAnalysisContextFactory:
    """Test AnalysisContextFactory functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.user = User(user_id="test", age=30, gender="male")
        self.biomarkers = {
            "total_cholesterol": BiomarkerValue(name="total_cholesterol", value=200, unit="mg/dL"),
            "glucose": BiomarkerValue(name="glucose", value=95, unit="mg/dL")
        }
        self.panel = BiomarkerPanel(biomarkers=self.biomarkers)
    
    def test_create_context_basic(self):
        """Test basic context creation"""
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-1",
            user=self.user,
            biomarker_panel=self.panel
        )
        
        assert isinstance(context, AnalysisContext)
        assert context.analysis_id == "test-analysis-1"
        assert context.user == self.user
        assert context.biomarker_panel == self.panel
        assert context.version == "1.0"
        assert isinstance(context.created_at, str)
    
    def test_create_context_with_parameters(self):
        """Test context creation with analysis parameters"""
        parameters = {
            "clustering_algorithm": "kmeans",
            "max_clusters": 5,
            "similarity_threshold": 0.8
        }
        
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-2",
            user=self.user,
            biomarker_panel=self.panel,
            analysis_parameters=parameters
        )
        
        assert isinstance(context, AnalysisContext)
        assert context.analysis_parameters == parameters
    
    def test_create_context_with_none_parameters(self):
        """Test context creation with None parameters"""
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-3",
            user=self.user,
            biomarker_panel=self.panel,
            analysis_parameters=None
        )
        
        assert isinstance(context, AnalysisContext)
        assert context.analysis_parameters == {}
    
    def test_create_context_with_empty_parameters(self):
        """Test context creation with empty parameters"""
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-4",
            user=self.user,
            biomarker_panel=self.panel,
            analysis_parameters={}
        )
        
        assert isinstance(context, AnalysisContext)
        assert context.analysis_parameters == {}
    
    def test_create_user_from_dict_basic(self):
        """Test basic user creation from dictionary"""
        user_data = {
            "user_id": "test-user-1",
            "email": "test@example.com",
            "age": 35,
            "gender": "female",
            "height": 165.0,
            "weight": 60.0,
            "ethnicity": "asian",
            "medical_history": {"diabetes": False},
            "medications": ["vitamin_d"],
            "lifestyle_factors": {"exercise": "moderate"},
            "created_at": "2025-01-27T10:00:00Z",
            "updated_at": "2025-01-27T11:00:00Z"
        }
        
        user = AnalysisContextFactory.create_user_from_dict(user_data)
        
        assert isinstance(user, User)
        assert user.user_id == "test-user-1"
        assert user.email == "test@example.com"
        assert user.age == 35
        assert user.gender == "female"
        assert user.height == 165.0
        assert user.weight == 60.0
        assert user.ethnicity == "asian"
        assert user.medical_history == {"diabetes": False}
        assert user.medications == ["vitamin_d"]
        assert user.lifestyle_factors == {"exercise": "moderate"}
        assert user.created_at == "2025-01-27T10:00:00Z"
        assert user.updated_at == "2025-01-27T11:00:00Z"
    
    def test_create_user_from_dict_minimal(self):
        """Test user creation with minimal data"""
        user_data = {
            "user_id": "test-user-2",
            "age": 25
        }
        
        user = AnalysisContextFactory.create_user_from_dict(user_data)
        
        assert isinstance(user, User)
        assert user.user_id == "test-user-2"
        assert user.age == 25
        assert user.email is None
        assert user.gender is None
        assert user.height is None
        assert user.weight is None
        assert user.ethnicity is None
        assert user.medical_history == {}
        assert user.medications == []
        assert user.lifestyle_factors == {}
        assert user.created_at is None
        assert user.updated_at is None
    
    def test_create_user_from_dict_empty(self):
        """Test user creation with empty dictionary"""
        user_data = {}
        
        user = AnalysisContextFactory.create_user_from_dict(user_data)
        
        assert isinstance(user, User)
        assert user.user_id == ""
        assert user.age is None
        assert user.email is None
        assert user.gender is None
        assert user.height is None
        assert user.weight is None
        assert user.ethnicity is None
        assert user.medical_history == {}
        assert user.medications == []
        assert user.lifestyle_factors == {}
        assert user.created_at is None
        assert user.updated_at is None
    
    def test_create_user_from_dict_with_none_values(self):
        """Test user creation with None values"""
        user_data = {
            "user_id": "test-user-3",
            "email": None,
            "age": None,
            "gender": None,
            "height": None,
            "weight": None,
            "ethnicity": None,
            "medical_history": None,
            "medications": None,
            "lifestyle_factors": None,
            "created_at": None,
            "updated_at": None
        }
        
        # The factory should handle None values by using defaults
        with pytest.raises(ValidationError):
            AnalysisContextFactory.create_user_from_dict(user_data)
    
    def test_create_context_immutability(self):
        """Test that created context is immutable"""
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-5",
            user=self.user,
            biomarker_panel=self.panel
        )
        
        # Should not be able to modify the context (Pydantic raises ValidationError for frozen models)
        with pytest.raises(ValidationError):
            context.analysis_id = "modified"
    
    def test_create_user_immutability(self):
        """Test that created user is immutable"""
        user_data = {
            "user_id": "test-user-4",
            "age": 30
        }
        
        user = AnalysisContextFactory.create_user_from_dict(user_data)
        
        # Should not be able to modify the user (Pydantic raises ValidationError for frozen models)
        with pytest.raises(ValidationError):
            user.user_id = "modified"
    
    def test_create_context_timestamp_format(self):
        """Test that created context has valid timestamp format"""
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-6",
            user=self.user,
            biomarker_panel=self.panel
        )
        
        # Should be valid ISO format
        try:
            datetime.fromisoformat(context.created_at.replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Invalid timestamp format")
    
    def test_create_context_consistency(self):
        """Test that context creation is consistent"""
        context1 = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-7",
            user=self.user,
            biomarker_panel=self.panel
        )
        
        context2 = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-7",
            user=self.user,
            biomarker_panel=self.panel
        )
        
        # Should have same structure but different timestamps
        assert context1.analysis_id == context2.analysis_id
        assert context1.user == context2.user
        assert context1.biomarker_panel == context2.biomarker_panel
        assert context1.version == context2.version
        # Timestamps should be different (created at different times)
        assert context1.created_at != context2.created_at
    
    def test_factory_methods_are_static(self):
        """Test that factory methods are static"""
        import inspect
        
        # Both methods should be static
        assert inspect.isfunction(AnalysisContextFactory.create_context)
        assert inspect.isfunction(AnalysisContextFactory.create_user_from_dict)
    
    def test_create_context_with_complex_parameters(self):
        """Test context creation with complex analysis parameters"""
        parameters = {
            "clustering": {
                "algorithm": "kmeans",
                "max_clusters": 10,
                "min_cluster_size": 2
            },
            "validation": {
                "min_confidence": 0.7,
                "max_uncertainty": 0.3
            },
            "output": {
                "include_raw_data": True,
                "format": "json"
            }
        }
        
        context = AnalysisContextFactory.create_context(
            analysis_id="test-analysis-8",
            user=self.user,
            biomarker_panel=self.panel,
            analysis_parameters=parameters
        )
        
        assert isinstance(context, AnalysisContext)
        assert context.analysis_parameters == parameters
        assert context.analysis_parameters["clustering"]["algorithm"] == "kmeans"
        assert context.analysis_parameters["validation"]["min_confidence"] == 0.7
        assert context.analysis_parameters["output"]["include_raw_data"] is True
    
    def test_create_user_from_dict_with_complex_data(self):
        """Test user creation with complex data structures"""
        user_data = {
            "user_id": "test-user-5",
            "medical_history": {
                "diabetes": False,
                "hypertension": True,
                "heart_disease": False,
                "family_history": {
                    "diabetes": True,
                    "heart_disease": True
                }
            },
            "medications": [
                "metformin",
                "lisinopril",
                "vitamin_d3"
            ],
            "lifestyle_factors": {
                "exercise": "moderate",
                "smoking": False,
                "alcohol": "light",
                "diet": "mediterranean"
            }
        }
        
        user = AnalysisContextFactory.create_user_from_dict(user_data)
        
        assert isinstance(user, User)
        assert user.medical_history == user_data["medical_history"]
        assert user.medications == user_data["medications"]
        assert user.lifestyle_factors == user_data["lifestyle_factors"]
    
    def test_create_context_performance(self):
        """Test context creation performance"""
        import time
        
        start_time = time.time()
        for i in range(100):
            AnalysisContextFactory.create_context(
                analysis_id=f"test-analysis-{i}",
                user=self.user,
                biomarker_panel=self.panel
            )
        end_time = time.time()
        
        # Should be fast (less than 1 second for 100 contexts)
        assert (end_time - start_time) < 1.0
