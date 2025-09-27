"""
Unit tests for biomarker service.
"""

import pytest
from unittest.mock import Mock, patch
from services.biomarker_service import BiomarkerService
from core.models.biomarker import BiomarkerDefinition, ReferenceRange


class TestBiomarkerService:
    """Test cases for BiomarkerService class."""
    
    @pytest.fixture
    def service(self):
        """Create a biomarker service instance for testing."""
        return BiomarkerService()
    
    @pytest.fixture
    def sample_biomarker_data(self):
        """Sample biomarker data for testing."""
        return {
            "total_cholesterol": 200.0,
            "glucose": 95.0,
            "unknown_biomarker": 50.0
        }
    
    @pytest.mark.asyncio
    async def test_get_all_biomarkers(self, service):
        """Test getting all available biomarkers."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_biomarkers = {
                "total_cholesterol": Mock(spec=BiomarkerDefinition),
                "glucose": Mock(spec=BiomarkerDefinition)
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.get_all_biomarkers()
            
            assert result == mock_biomarkers
            mock_load.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_biomarker_definition_found(self, service):
        """Test getting specific biomarker definition that exists."""
        with patch.object(service.resolver, 'get_biomarker_definition') as mock_get:
            mock_definition = Mock(spec=BiomarkerDefinition)
            mock_get.return_value = mock_definition
            
            result = await service.get_biomarker_definition("total_cholesterol")
            
            assert result == mock_definition
            mock_get.assert_called_once_with("total_cholesterol")
    
    @pytest.mark.asyncio
    async def test_get_biomarker_definition_not_found(self, service):
        """Test getting biomarker definition that doesn't exist."""
        with patch.object(service.resolver, 'get_biomarker_definition') as mock_get:
            mock_get.return_value = None
            
            result = await service.get_biomarker_definition("nonexistent")
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_search_biomarkers_by_name(self, service):
        """Test searching biomarkers by name."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_cholesterol = Mock()
            mock_cholesterol.name = "total_cholesterol"
            mock_cholesterol.aliases = ["cholesterol"]
            mock_cholesterol.description = "Total cholesterol level"
            mock_cholesterol.category = "cardiovascular"
            
            mock_glucose = Mock()
            mock_glucose.name = "glucose"
            mock_glucose.aliases = ["blood_sugar"]
            mock_glucose.description = "Blood glucose level"
            mock_glucose.category = "metabolic"
            
            mock_biomarkers = {
                "total_cholesterol": mock_cholesterol,
                "glucose": mock_glucose
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.search_biomarkers("cholesterol")
            
            assert len(result) == 1
            assert result[0].name == "total_cholesterol"
    
    @pytest.mark.asyncio
    async def test_search_biomarkers_by_alias(self, service):
        """Test searching biomarkers by alias."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_glucose = Mock()
            mock_glucose.name = "glucose"
            mock_glucose.aliases = ["blood_sugar", "sugar"]
            mock_glucose.description = "Blood glucose level"
            mock_glucose.category = "metabolic"
            
            mock_biomarkers = {
                "glucose": mock_glucose
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.search_biomarkers("sugar")
            
            assert len(result) == 1
            assert result[0].name == "glucose"
    
    @pytest.mark.asyncio
    async def test_search_biomarkers_by_category(self, service):
        """Test searching biomarkers by category."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_cholesterol = Mock()
            mock_cholesterol.name = "total_cholesterol"
            mock_cholesterol.aliases = []
            mock_cholesterol.description = "Total cholesterol level"
            mock_cholesterol.category = "cardiovascular"
            
            mock_glucose = Mock()
            mock_glucose.name = "glucose"
            mock_glucose.aliases = []
            mock_glucose.description = "Blood glucose level"
            mock_glucose.category = "metabolic"
            
            mock_biomarkers = {
                "total_cholesterol": mock_cholesterol,
                "glucose": mock_glucose
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.search_biomarkers("cardiovascular")
            
            assert len(result) == 1
            assert result[0].name == "total_cholesterol"
    
    @pytest.mark.asyncio
    async def test_get_biomarkers_by_category(self, service):
        """Test getting biomarkers by specific category."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_biomarkers = {
                "total_cholesterol": Mock(category="cardiovascular"),
                "ldl_cholesterol": Mock(category="cardiovascular"),
                "glucose": Mock(category="metabolic")
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.get_biomarkers_by_category("cardiovascular")
            
            assert len(result) == 2
            assert all(b.category == "cardiovascular" for b in result)
    
    @pytest.mark.asyncio
    async def test_get_biomarker_categories(self, service):
        """Test getting all available biomarker categories."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_biomarkers = {
                "total_cholesterol": Mock(category="cardiovascular"),
                "glucose": Mock(category="metabolic"),
                "alt": Mock(category="liver"),
                "unknown": Mock(category="")  # Empty category
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.get_biomarker_categories()
            
            assert "cardiovascular" in result
            assert "metabolic" in result
            assert "liver" in result
            assert "" not in result  # Empty categories should be excluded
            assert len(result) == 3
    
    @pytest.mark.asyncio
    async def test_normalize_biomarker_data(self, service, sample_biomarker_data):
        """Test normalizing biomarker data."""
        with patch.object(service.normalizer, 'normalize_biomarkers') as mock_normalize:
            mock_panel = Mock()
            mock_panel.biomarkers = {
                "total_cholesterol": Mock(value=200.0, unit="mg/dL", timestamp=None),
                "glucose": Mock(value=95.0, unit="mg/dL", timestamp=None)
            }
            mock_normalize.return_value = (mock_panel, ["unknown_biomarker"])
            
            result = await service.normalize_biomarker_data(sample_biomarker_data)
            
            assert "normalized_biomarkers" in result
            assert "unmapped_keys" in result
            assert result["total_biomarkers"] == 2
            assert result["unmapped_count"] == 1
            assert "unknown_biomarker" in result["unmapped_keys"]
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_value(self, service):
        """Test validating a single biomarker value."""
        with patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            mock_result = {
                "status": "normal",
                "message": "Within normal range",
                "value": 200.0,
                "unit": "mg/dL"
            }
            mock_validate.return_value = mock_result
            
            result = await service.validate_biomarker_value(
                "total_cholesterol", 200.0, "mg/dL", age=35, gender="male"
            )
            
            assert result == mock_result
            mock_validate.assert_called_once_with(
                biomarker_name="total_cholesterol",
                value=200.0,
                unit="mg/dL",
                age=35,
                gender="male"
            )
    
    @pytest.mark.asyncio
    async def test_get_reference_ranges(self, service):
        """Test getting reference ranges for a biomarker."""
        with patch.object(service.resolver, 'get_reference_range') as mock_get:
            mock_range = Mock(spec=ReferenceRange)
            mock_get.return_value = mock_range
            
            result = await service.get_reference_ranges(
                "total_cholesterol", age=35, gender="male", population="general_adult"
            )
            
            assert result == mock_range
            mock_get.assert_called_once_with(
                biomarker_name="total_cholesterol",
                age=35,
                gender="male",
                population="general_adult"
            )
    
    @pytest.mark.asyncio
    async def test_get_all_reference_ranges(self, service):
        """Test getting all reference ranges for a biomarker."""
        with patch.object(service.resolver, 'get_all_reference_ranges') as mock_get:
            mock_ranges = [Mock(spec=ReferenceRange), Mock(spec=ReferenceRange)]
            mock_get.return_value = mock_ranges
            
            result = await service.get_all_reference_ranges("total_cholesterol")
            
            assert result == mock_ranges
            mock_get.assert_called_once_with("total_cholesterol")
    
    @pytest.mark.asyncio
    async def test_convert_unit(self, service):
        """Test unit conversion."""
        with patch.object(service.resolver, 'convert_unit') as mock_convert:
            mock_convert.return_value = 5.18
            
            result = await service.convert_unit(200.0, "mg/dL", "mmol/L")
            
            assert result == 5.18
            mock_convert.assert_called_once_with(200.0, "mg/dL", "mmol/L")
    
    @pytest.mark.asyncio
    async def test_get_available_units(self, service):
        """Test getting available units."""
        with patch.object(service.resolver, 'load_units') as mock_load:
            mock_units = {"units": {"mg_dL": {"name": "mg/dL"}}}
            mock_load.return_value = mock_units
            
            result = await service.get_available_units()
            
            assert result == mock_units
            mock_load.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_biomarker_statistics(self, service):
        """Test getting biomarker statistics."""
        with patch.object(service.resolver, 'load_biomarkers') as mock_load:
            mock_biomarkers = {
                "total_cholesterol": Mock(
                    category="cardiovascular",
                    data_type="numeric",
                    unit="mg/dL"
                ),
                "ldl_cholesterol": Mock(
                    category="cardiovascular",
                    data_type="numeric",
                    unit="mg/dL"
                ),
                "glucose": Mock(
                    category="metabolic",
                    data_type="numeric",
                    unit="mg/dL"
                ),
                "hba1c": Mock(
                    category="metabolic",
                    data_type="numeric",
                    unit="%"
                )
            }
            mock_load.return_value = mock_biomarkers
            
            result = await service.get_biomarker_statistics()
            
            assert result["total_biomarkers"] == 4
            assert result["categories"]["cardiovascular"] == 2
            assert result["categories"]["metabolic"] == 2
            assert result["units"]["mg/dL"] == 3
            assert result["units"]["%"] == 1
            assert "cardiovascular" in result["categories_list"]
            assert "mg/dL" in result["units_list"]
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_success(self, service, sample_biomarker_data):
        """Test successful biomarker panel validation."""
        with patch.object(service, 'normalize_biomarker_data') as mock_normalize, \
             patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            
            # Mock normalization
            mock_normalize.return_value = {
                "normalized_biomarkers": {
                    "total_cholesterol": {"value": 200.0, "unit": "mg/dL"},
                    "glucose": {"value": 95.0, "unit": "mg/dL"}
                },
                "unmapped_keys": ["unknown_biomarker"]
            }
            
            # Mock validation results
            mock_validate.return_value = {"status": "normal"}
            
            result = await service.validate_biomarker_panel(sample_biomarker_data)
            
            assert result["valid"] is True
            assert result["overall_score"] == 1.0
            assert result["total_biomarkers"] == 2
            assert result["valid_biomarkers"] == 2
            assert result["error_biomarkers"] == 0
            assert "unknown_biomarker" in result["unmapped_biomarkers"]
            assert result["summary"]["normal_percentage"] == 100.0
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_with_errors(self, service):
        """Test biomarker panel validation with various errors."""
        biomarkers_with_errors = {
            "total_cholesterol": "invalid",  # Non-numeric
            "glucose": 95.0,
            "unknown_biomarker": 50.0
        }
        
        with patch.object(service, 'normalize_biomarker_data') as mock_normalize, \
             patch.object(service.resolver, 'validate_biomarker_value') as mock_validate:
            
            # Mock normalization
            mock_normalize.return_value = {
                "normalized_biomarkers": {
                    "total_cholesterol": {"value": "invalid", "unit": "mg/dL"},
                    "glucose": {"value": 95.0, "unit": "mg/dL"}
                },
                "unmapped_keys": ["unknown_biomarker"]
            }
            
            # Mock validation results
            def mock_validate_side_effect(biomarker_name, value, unit):
                if biomarker_name == "total_cholesterol":
                    return {"status": "normal"}  # This won't be called due to type check
                else:
                    return {"status": "high"}  # Abnormal value
            
            mock_validate.side_effect = mock_validate_side_effect
            
            result = await service.validate_biomarker_panel(biomarkers_with_errors)
            
            assert result["valid"] is False
            assert result["error_biomarkers"] > 0  # Due to non-numeric value
            assert result["abnormal_biomarkers"] > 0  # Due to high glucose
            assert "unknown_biomarker" in result["unmapped_biomarkers"]
    
    @pytest.mark.asyncio
    async def test_validate_biomarker_panel_exception(self, service):
        """Test biomarker panel validation with exception."""
        with patch.object(service, 'normalize_biomarker_data') as mock_normalize:
            mock_normalize.side_effect = Exception("Normalization failed")
            
            result = await service.validate_biomarker_panel({"test": 100})
            
            assert result["valid"] is False
            assert result["overall_score"] == 0.0
            assert result["error"] == "Normalization failed"
            assert result["summary"]["error_percentage"] == 100
    
    @pytest.mark.asyncio
    async def test_get_biomarker_recommendations(self, service):
        """Test generating biomarker recommendations."""
        biomarkers = {
            "total_cholesterol": 250.0,  # High
            "glucose": 95.0,  # Normal
            "hdl_cholesterol": 35.0  # Low
        }
        
        with patch.object(service, 'validate_biomarker_panel') as mock_validate:
            mock_validate.return_value = {
                "valid": True,
                "overall_score": 0.8,
                "validation_results": {
                    "total_cholesterol": {"status": "high"},
                    "glucose": {"status": "normal"},
                    "hdl_cholesterol": {"status": "low"}
                },
                "summary": {
                    "abnormal_percentage": 40.0,
                    "error_percentage": 0.0
                }
            }
            
            result = await service.get_biomarker_recommendations(biomarkers)
            
            assert len(result) > 0
            assert any("cholesterol" in rec.lower() for rec in result)
            assert any("health" in rec.lower() for rec in result)
    
    @pytest.mark.asyncio
    async def test_get_biomarker_recommendations_with_context(self, service):
        """Test generating biomarker recommendations with user context."""
        biomarkers = {"glucose": 95.0}
        user_context = {"age": 55, "gender": "female"}
        
        with patch.object(service, 'validate_biomarker_panel') as mock_validate:
            mock_validate.return_value = {
                "valid": True,
                "overall_score": 1.0,
                "validation_results": {"glucose": {"status": "normal"}},
                "summary": {"abnormal_percentage": 0.0, "error_percentage": 0.0}
            }
            
            result = await service.get_biomarker_recommendations(biomarkers, user_context)
            
            assert len(result) > 0
            assert any("age" in rec.lower() or "screening" in rec.lower() for rec in result)
            assert any("hormone" in rec.lower() or "bone" in rec.lower() for rec in result)