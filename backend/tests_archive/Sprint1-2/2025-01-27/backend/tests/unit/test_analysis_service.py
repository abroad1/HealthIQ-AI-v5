"""
Unit tests for analysis service.
"""

import pytest
from unittest.mock import Mock, patch
from services.analysis_service import AnalysisService
from core.models.biomarker import BiomarkerPanel, BiomarkerValue
from core.models.user import User
from core.models.results import AnalysisResult


class TestAnalysisService:
    """Test cases for AnalysisService class."""
    
    @pytest.fixture
    def service(self):
        """Create an analysis service instance for testing."""
        return AnalysisService()
    
    @pytest.fixture
    def sample_biomarkers(self):
        """Sample biomarker data for testing."""
        return {
            "total_cholesterol": 200.0,
            "glucose": 95.0,
            "hdl_cholesterol": 45.0,
            "ldl_cholesterol": 120.0
        }
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "user_id": "test_user_123",
            "email": "test@example.com",
            "age": 35,
            "gender": "male",
            "height": 175.0,
            "weight": 70.0,
            "ethnicity": "caucasian",
            "medical_history": {"diabetes": False},
            "medications": ["vitamin_d"],
            "lifestyle_factors": {"exercise": "moderate", "smoking": False}
        }
    
    @pytest.mark.asyncio
    async def test_start_analysis_success(self, service, sample_biomarkers, sample_user_data):
        """Test successful analysis start."""
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize, \
             patch.object(service.orchestrator, 'create_analysis_context') as mock_context, \
             patch.object(service, '_process_analysis') as mock_process:
            
            # Mock the normalization
            mock_panel = Mock()
            mock_panel.biomarkers = {
                "total_cholesterol": Mock(value=200.0, unit="mg/dL"),
                "glucose": Mock(value=95.0, unit="mg/dL")
            }
            mock_normalize.return_value = (mock_panel, [])
            
            # Mock the context creation
            mock_context_obj = Mock()
            mock_context_obj.user.user_id = "test_user_123"
            mock_context.return_value = mock_context_obj
            
            # Start analysis
            analysis_id = await service.start_analysis(sample_biomarkers, sample_user_data)
            
            # Verify analysis ID was generated
            assert analysis_id is not None
            assert len(analysis_id) > 0
            
            # Verify status was initialized
            status = await service.get_analysis_status(analysis_id)
            assert status["status"] == "processing"
            assert status["user_id"] == "test_user_123"
            assert status["biomarker_count"] == 2
    
    @pytest.mark.asyncio
    async def test_start_analysis_with_unmapped_biomarkers(self, service, sample_user_data):
        """Test analysis start with unmapped biomarkers."""
        biomarkers_with_unknown = {
            "total_cholesterol": 200.0,
            "unknown_biomarker": 50.0,
            "glucose": 95.0
        }
        
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize, \
             patch.object(service.orchestrator, 'create_analysis_context') as mock_context, \
             patch.object(service, '_process_analysis') as mock_process:
            
            # Mock the normalization with unmapped keys
            mock_panel = Mock()
            mock_panel.biomarkers = {
                "total_cholesterol": Mock(value=200.0, unit="mg/dL"),
                "glucose": Mock(value=95.0, unit="mg/dL")
            }
            mock_normalize.return_value = (mock_panel, ["unknown_biomarker"])
            
            # Mock the context creation
            mock_context_obj = Mock()
            mock_context_obj.user.user_id = "test_user_123"
            mock_context.return_value = mock_context_obj
            
            # Start analysis
            analysis_id = await service.start_analysis(biomarkers_with_unknown, sample_user_data)
            
            # Verify unmapped biomarkers are tracked
            status = await service.get_analysis_status(analysis_id)
            assert "unknown_biomarker" in status["unmapped_biomarkers"]
    
    @pytest.mark.asyncio
    async def test_start_analysis_error_handling(self, service, sample_biomarkers, sample_user_data):
        """Test error handling in analysis start."""
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize:
            # Mock an error during normalization
            mock_normalize.side_effect = ValueError("Normalization failed")
            
            # Start analysis should raise the error
            with pytest.raises(ValueError, match="Normalization failed"):
                await service.start_analysis(sample_biomarkers, sample_user_data)
    
    @pytest.mark.asyncio
    async def test_get_analysis_result_not_found(self, service):
        """Test getting analysis result for non-existent analysis."""
        result = await service.get_analysis_result("nonexistent_id")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_analysis_status_not_found(self, service):
        """Test getting analysis status for non-existent analysis."""
        status = await service.get_analysis_status("nonexistent_id")
        assert status["status"] == "not_found"
    
    @pytest.mark.asyncio
    async def test_get_user_analysis_history_empty(self, service):
        """Test getting analysis history for user with no analyses."""
        history = await service.get_user_analysis_history("user_with_no_analyses")
        assert history == []
    
    @pytest.mark.asyncio
    async def test_get_user_analysis_history_with_results(self, service):
        """Test getting analysis history for user with analyses."""
        # Create a mock analysis result
        mock_result = Mock(spec=AnalysisResult)
        mock_result.user_id = "test_user"
        mock_result.created_at = "2024-01-01T00:00:00Z"
        
        # Add to service's internal storage
        service._analysis_results["analysis_1"] = mock_result
        
        # Get history
        history = await service.get_user_analysis_history("test_user")
        
        assert len(history) == 1
        assert history[0].user_id == "test_user"
    
    def test_calculate_confidence_score_complete_panel(self, service):
        """Test confidence score calculation with complete panel."""
        # Create a mock biomarker panel
        mock_panel = Mock()
        mock_panel.biomarkers = {
            "total_cholesterol": Mock(value=200.0, unit="mg/dL"),
            "glucose": Mock(value=95.0, unit="mg/dL"),
            "hdl_cholesterol": Mock(value=45.0, unit="mg/dL")
        }
        
        with patch.object(service.resolver, 'load_biomarkers') as mock_load, \
             patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            
            # Mock available biomarkers (small set for testing)
            mock_load.return_value = {
                "total_cholesterol": Mock(),
                "glucose": Mock(),
                "hdl_cholesterol": Mock(),
                "ldl_cholesterol": Mock(),
                "triglycerides": Mock()
            }
            
            # Mock validation results (all normal)
            mock_validate.return_value = {"status": "normal"}
            
            score = service._calculate_confidence_score(mock_panel)
            
            # Should have high confidence (3 out of 5 biomarkers = 60% completeness)
            assert 0.0 <= score <= 1.0
            assert score > 0.5  # Should be reasonable confidence
    
    def test_calculate_confidence_score_with_errors(self, service):
        """Test confidence score calculation with validation errors."""
        # Create a mock biomarker panel
        mock_panel = Mock()
        mock_panel.biomarkers = {
            "total_cholesterol": Mock(value=200.0, unit="mg/dL"),
            "glucose": Mock(value=95.0, unit="mg/dL")
        }
        
        with patch.object(service.resolver, 'load_biomarkers') as mock_load, \
             patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            
            # Mock available biomarkers
            mock_load.return_value = {
                "total_cholesterol": Mock(),
                "glucose": Mock(),
                "hdl_cholesterol": Mock()
            }
            
            # Mock validation results with errors
            def mock_validate_side_effect(biomarker_name, value, unit):
                if biomarker_name == "total_cholesterol":
                    return {"status": "conversion_error"}
                else:
                    return {"status": "normal"}
            
            mock_validate.side_effect = mock_validate_side_effect
            
            score = service._calculate_confidence_score(mock_panel)
            
            # Should have lower confidence due to errors
            assert 0.0 <= score <= 1.0
            assert score < 0.8  # Should be lower due to errors
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_success(self, service, sample_biomarkers):
        """Test successful biomarker panel validation."""
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize, \
             patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            
            # Mock normalization
            mock_panel = Mock()
            mock_panel.biomarkers = {
                "total_cholesterol": Mock(value=200.0, unit="mg/dL"),
                "glucose": Mock(value=95.0, unit="mg/dL")
            }
            mock_normalize.return_value = (mock_panel, [])
            
            # Mock validation results
            mock_validate.return_value = {"status": "normal"}
            
            result = await service.validate_biomarker_panel(sample_biomarkers)
            
            assert result["valid"] is True
            assert result["score"] == 1.0
            assert result["total_biomarkers"] == 2
            assert result["valid_biomarkers"] == 2
            assert result["error_biomarkers"] == 0
            assert len(result["recommendations"]) == 0
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_with_errors(self, service):
        """Test biomarker panel validation with errors."""
        biomarkers_with_errors = {
            "total_cholesterol": "invalid_value",  # Non-numeric
            "glucose": 95.0
        }
        
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize:
            # Mock normalization
            mock_panel = Mock()
            mock_panel.biomarkers = {
                "total_cholesterol": Mock(value="invalid_value", unit="mg/dL"),
                "glucose": Mock(value=95.0, unit="mg/dL")
            }
            mock_normalize.return_value = (mock_panel, [])
            
            result = await service.validate_biomarker_panel(biomarkers_with_errors)
            
            assert result["valid"] is False
            assert result["error_biomarkers"] > 0
            assert len(result["recommendations"]) > 0
    
    def test_generate_validation_recommendations_unmapped(self, service):
        """Test generating recommendations for unmapped biomarkers."""
        validation_results = {
            "total_cholesterol": {"status": "normal"},
            "glucose": {"status": "high"}
        }
        unmapped_keys = ["unknown_biomarker", "another_unknown"]
        
        recommendations = service._generate_validation_recommendations(
            validation_results, unmapped_keys
        )
        
        assert len(recommendations) > 0
        assert any("unknown_biomarker" in rec for rec in recommendations)
        assert any("glucose" in rec for rec in recommendations)
    
    def test_generate_validation_recommendations_conversion_errors(self, service):
        """Test generating recommendations for conversion errors."""
        validation_results = {
            "total_cholesterol": {"status": "conversion_error"},
            "glucose": {"status": "normal"}
        }
        unmapped_keys = []
        
        recommendations = service._generate_validation_recommendations(
            validation_results, unmapped_keys
        )
        
        assert len(recommendations) > 0
        assert any("total_cholesterol" in rec for rec in recommendations)
        assert any("units" in rec.lower() for rec in recommendations)
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_exception_handling(self, service):
        """Test exception handling in biomarker panel validation."""
        with patch.object(service.orchestrator, 'normalize_biomarkers') as mock_normalize:
            # Mock an exception during normalization
            mock_normalize.side_effect = Exception("Validation failed")
            
            result = await service.validate_biomarker_panel({"test": 100})
            
            assert result["valid"] is False
            assert result["score"] == 0.0
            assert "error" in result
            assert result["error"] == "Validation failed"