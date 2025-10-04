"""
Unit tests for manifest service functionality.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

from services.insights.manifest_service import ManifestService, InsightManifest, InsightConfig
from core.insights.registry import insight_registry


class TestManifestService:
    """Test manifest service functionality."""
    
    def test_manifest_service_initialization(self):
        """Test manifest service initializes correctly."""
        service = ManifestService()
        assert service.manifest_dir == Path("backend/data/insight_manifests")
        assert service._active_manifest is None
    
    def test_validate_manifest_valid(self):
        """Test validating a valid manifest."""
        service = ManifestService()
        
        valid_manifest = {
            "schema_version": "1.0",
            "manifest_id": "test_v1",
            "name": "Test Manifest",
            "description": "Test description",
            "created_by": "Test User",
            "updated_by": "Test User",
            "insights": [
                {
                    "insight_id": "test_insight",
                    "version": "v1.0.0",
                    "enabled": True,
                    "weight": 1.0
                }
            ]
        }
        
        assert service.validate_manifest(valid_manifest) is True
    
    def test_validate_manifest_invalid_missing_fields(self):
        """Test validating manifest with missing required fields."""
        service = ManifestService()
        
        invalid_manifest = {
            "schema_version": "1.0",
            "manifest_id": "test_v1",
            # Missing name, description, etc.
            "insights": []
        }
        
        assert service.validate_manifest(invalid_manifest) is False
    
    def test_validate_manifest_invalid_insights_format(self):
        """Test validating manifest with invalid insights format."""
        service = ManifestService()
        
        invalid_manifest = {
            "schema_version": "1.0",
            "manifest_id": "test_v1",
            "name": "Test Manifest",
            "description": "Test description",
            "created_by": "Test User",
            "updated_by": "Test User",
            "insights": "not_a_list"  # Should be a list
        }
        
        assert service.validate_manifest(invalid_manifest) is False
    
    def test_validate_manifest_invalid_insight_missing_fields(self):
        """Test validating manifest with invalid insight format."""
        service = ManifestService()
        
        invalid_manifest = {
            "schema_version": "1.0",
            "manifest_id": "test_v1",
            "name": "Test Manifest",
            "description": "Test description",
            "created_by": "Test User",
            "updated_by": "Test User",
            "insights": [
                {
                    "insight_id": "test_insight",
                    # Missing version and enabled
                    "weight": 1.0
                }
            ]
        }
        
        assert service.validate_manifest(invalid_manifest) is False
    
    def test_load_manifest(self):
        """Test loading a manifest from file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_dir = Path(temp_dir)
            service = ManifestService(str(manifest_dir))
            
            # Create test manifest file
            manifest_data = {
                "schema_version": "1.0",
                "manifest_id": "test_v1",
                "name": "Test Manifest",
                "description": "Test description",
                "created_by": "Test User",
                "updated_by": "Test User",
                "insights": [
                    {
                        "insight_id": "test_insight",
                        "version": "v1.0.0",
                        "enabled": True,
                        "weight": 1.0
                    }
                ]
            }
            
            manifest_file = manifest_dir / "test_v1.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest_data, f)
            
            manifest = service.load_manifest("test_v1")
            
            assert isinstance(manifest, InsightManifest)
            assert manifest.manifest_id == "test_v1"
            assert manifest.name == "Test Manifest"
            assert len(manifest.insights) == 1
            assert manifest.insights[0].insight_id == "test_insight"
    
    def test_load_manifest_file_not_found(self):
        """Test loading nonexistent manifest raises FileNotFoundError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            service = ManifestService(temp_dir)
            
            with pytest.raises(FileNotFoundError, match="not found"):
                service.load_manifest("nonexistent")
    
    def test_load_manifest_invalid_format(self):
        """Test loading invalid manifest raises ValueError."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_dir = Path(temp_dir)
            service = ManifestService(str(manifest_dir))
            
            # Create invalid manifest file
            manifest_file = manifest_dir / "invalid.json"
            with open(manifest_file, 'w') as f:
                json.dump({"invalid": "data"}, f)
            
            with pytest.raises(ValueError, match="Invalid manifest format"):
                service.load_manifest("invalid")
    
    def test_get_enabled_insights(self):
        """Test getting enabled insights from manifest."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_dir = Path(temp_dir)
            service = ManifestService(str(manifest_dir))
            
            # Create test manifest with mixed enabled/disabled insights
            manifest_data = {
                "schema_version": "1.0",
                "manifest_id": "test_v1",
                "name": "Test Manifest",
                "description": "Test description",
                "created_by": "Test User",
                "updated_by": "Test User",
                "insights": [
                    {
                        "insight_id": "enabled_insight",
                        "version": "v1.0.0",
                        "enabled": True,
                        "weight": 1.0
                    },
                    {
                        "insight_id": "disabled_insight",
                        "version": "v1.0.0",
                        "enabled": False,
                        "weight": 1.0
                    }
                ]
            }
            
            manifest_file = manifest_dir / "default.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest_data, f)
            
            enabled_insights = service.get_enabled_insights()
            
            assert len(enabled_insights) == 1
            assert enabled_insights[0].insight_id == "enabled_insight"
            assert enabled_insights[0].enabled is True
    
    @patch('services.insights.manifest_service.insight_registry')
    def test_validate_insight_registry_success(self, mock_registry):
        """Test validating insight registry succeeds when all insights registered."""
        service = ManifestService()
        
        # Mock manifest with insights
        service._active_manifest = InsightManifest(
            schema_version="1.0",
            manifest_id="test_v1",
            name="Test Manifest",
            description="Test description",
            created_by="Test User",
            updated_by="Test User",
            insights=[
                InsightConfig("test_insight_1", "v1.0.0", True),
                InsightConfig("test_insight_2", "v1.0.0", True)
            ]
        )
        
        # Mock registry to not raise for any assertions
        mock_registry.assert_registered = Mock(return_value=None)
        
        # Should not raise
        service.validate_insight_registry()
        
        # Verify assert_registered was called for each insight
        assert mock_registry.assert_registered.call_count == 2
    
    @patch('services.insights.manifest_service.insight_registry')
    def test_validate_insight_registry_failure(self, mock_registry):
        """Test validating insight registry fails when insight not registered."""
        service = ManifestService()
        
        # Mock manifest with insights
        service._active_manifest = InsightManifest(
            schema_version="1.0",
            manifest_id="test_v1",
            name="Test Manifest",
            description="Test description",
            created_by="Test User",
            updated_by="Test User",
            insights=[
                InsightConfig("test_insight_1", "v1.0.0", True),
                InsightConfig("missing_insight", "v1.0.0", True)
            ]
        )
        
        # Mock registry to raise KeyError for missing insight
        def side_effect(insight_id, version):
            if insight_id == "missing_insight":
                raise KeyError(f"Insight {insight_id} version {version} not registered")
        
        mock_registry.assert_registered = side_effect
        
        # Should raise KeyError
        with pytest.raises(KeyError, match="not registered"):
            service.validate_insight_registry()
    
    def test_save_manifest(self):
        """Test saving a manifest to file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest_dir = Path(temp_dir)
            service = ManifestService(str(manifest_dir))
            
            manifest = InsightManifest(
                schema_version="1.0",
                manifest_id="test_v1",
                name="Test Manifest",
                description="Test description",
                created_by="Test User",
                updated_by="Test User",
                insights=[
                    InsightConfig("test_insight", "v1.0.0", True, 1.0)
                ]
            )
            
            service.save_manifest(manifest)
            
            # Verify file was created
            manifest_file = manifest_dir / "test_v1.json"
            assert manifest_file.exists()
            
            # Verify content
            with open(manifest_file, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["manifest_id"] == "test_v1"
            assert saved_data["name"] == "Test Manifest"
            assert len(saved_data["insights"]) == 1
            assert saved_data["insights"][0]["insight_id"] == "test_insight"


class TestInsightConfig:
    """Test InsightConfig dataclass."""
    
    def test_insight_config_creation(self):
        """Test creating InsightConfig."""
        config = InsightConfig(
            insight_id="test_insight",
            version="v1.0.0",
            enabled=True,
            weight=1.5
        )
        
        assert config.insight_id == "test_insight"
        assert config.version == "v1.0.0"
        assert config.enabled is True
        assert config.weight == 1.5
    
    def test_insight_config_defaults(self):
        """Test InsightConfig with default values."""
        config = InsightConfig(
            insight_id="test_insight",
            version="v1.0.0",
            enabled=True
        )
        
        assert config.weight == 1.0  # Default value


class TestInsightManifest:
    """Test InsightManifest dataclass."""
    
    def test_insight_manifest_creation(self):
        """Test creating InsightManifest."""
        manifest = InsightManifest(
            schema_version="1.0",
            manifest_id="test_v1",
            name="Test Manifest",
            description="Test description",
            created_by="Test User",
            updated_by="Test User",
            insights=[
                InsightConfig("test_insight", "v1.0.0", True)
            ]
        )
        
        assert manifest.schema_version == "1.0"
        assert manifest.manifest_id == "test_v1"
        assert manifest.name == "Test Manifest"
        assert len(manifest.insights) == 1
        assert manifest.overrides is None  # Default value
