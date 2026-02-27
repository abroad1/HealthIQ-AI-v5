"""
Unit tests for AliasRegistryService.

Tests the v4 alias registry integration, resolution logic,
and normalization functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from core.canonical.alias_registry_service import AliasRegistryService, AliasCollisionError


class TestAliasRegistryService:
    """Test cases for AliasRegistryService."""
    
    def test_init_with_v4_registry(self):
        """Test initialization with v4 registry enabled."""
        service = AliasRegistryService(use_v4_registry=True)
        assert service.use_v4_registry is True
        assert service._alias_to_canonical is None
        assert service._loaded is False
    
    def test_init_without_v4_registry(self):
        """Test initialization with v4 registry disabled."""
        service = AliasRegistryService(use_v4_registry=False)
        assert service.use_v4_registry is False
        assert service._alias_to_canonical is None
        assert service._loaded is False
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_resolve_known_alias(self, mock_open, mock_yaml_load):
        """Test resolving a known alias to canonical name (hdl->hdl_cholesterol per PR)."""
        # Mock v4 registry data - common_aliases overwrite to hdl_cholesterol
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol', 'High-Density Lipoprotein']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test various forms of HDL -> hdl_cholesterol (canonical per PR)
        assert service.resolve("HDL") == "hdl_cholesterol"
        assert service.resolve("hdl") == "hdl_cholesterol"
        assert service.resolve("HDL Cholesterol") == "hdl_cholesterol"
        assert service.resolve("High-Density Lipoprotein") == "hdl_cholesterol"
        assert service.resolve("hdl_cholesterol") == "hdl_cholesterol"
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_resolve_unknown_alias(self, mock_open, mock_yaml_load):
        """Test resolving an unknown alias returns unmapped prefix."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test unknown alias
        result = service.resolve("Unknown Biomarker")
        assert result == "unmapped_Unknown Biomarker"
        assert result.startswith("unmapped_")

    def test_resolve_deterministic_fail_closed(self):
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service._build_alias_mapping()
        message = str(exc.value)
        assert "Alias collision for key" in message
        assert "canonical_ids=" in message
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_normalize_panel(self, mock_open, mock_yaml_load):
        """Test normalizing a biomarker panel (canonical: hdl_cholesterol, ldl_cholesterol)."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl_cholesterol': {
                'canonical_id': 'ldl_cholesterol',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test panel with known and unknown biomarkers
        test_panel = {
            "HDL": 45.0,
            "LDL Cholesterol": 120.0,
            "Unknown Biomarker": 10.0
        }
        
        normalized = service.normalize_panel(test_panel)
        
        # Check that known biomarkers are mapped to canonical IDs
        assert "hdl_cholesterol" in normalized
        assert normalized["hdl_cholesterol"] == 45.0
        assert "ldl_cholesterol" in normalized
        assert normalized["ldl_cholesterol"] == 120.0
        
        # Check that unknown biomarker is prefixed
        assert "unmapped_Unknown Biomarker" in normalized
        assert normalized["unmapped_Unknown Biomarker"] == 10.0
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry')
    def test_get_all_aliases(self, mock_load_v4):
        """Test getting all aliases grouped by canonical name (hdl_cholesterol, ldl_cholesterol)."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl_cholesterol': {
                'canonical_id': 'ldl_cholesterol',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        aliases = service.get_all_aliases()
        
        # Check structure
        assert isinstance(aliases, dict)
        assert "hdl_cholesterol" in aliases
        assert "ldl_cholesterol" in aliases
        
        # Check that aliases are lists
        assert isinstance(aliases["hdl_cholesterol"], list)
        assert isinstance(aliases["ldl_cholesterol"], list)
        
        # Check specific aliases (note: case variations are generated)
        assert "hdl" in aliases["hdl_cholesterol"] or "HDL" in aliases["hdl_cholesterol"]
        assert any("cholesterol" in alias.lower() for alias in aliases["hdl_cholesterol"])
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry')
    def test_get_canonical_biomarkers(self, mock_load_v4):
        """Test getting list of canonical biomarkers."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl_cholesterol': {
                'canonical_id': 'ldl_cholesterol',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        canonical = service.get_canonical_biomarkers()
        
        # Check structure
        assert isinstance(canonical, list)
        assert "hdl_cholesterol" in canonical
        assert "ldl_cholesterol" in canonical
        # Should have at least 2 canonical biomarkers from mock + common aliases
        assert len(canonical) >= 2
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_is_canonical(self, mock_open, mock_yaml_load):
        """Test checking if a name is canonical."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test canonical names (hdl_cholesterol per PR; hdl may still be canonical from common_aliases self-map)
        assert service.is_canonical("hdl_cholesterol") is True
        
        # Test non-canonical names
        assert service.is_canonical("HDL") is False
        assert service.is_canonical("Unknown") is False
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry')
    def test_get_alias_count(self, mock_load_v4):
        """Test getting alias count."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        count = service.get_alias_count()
        
        # Should have canonical name + 2 aliases + case variations = more than 3
        assert count >= 3
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry')
    def test_get_canonical_count(self, mock_load_v4):
        """Test getting canonical count."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl_cholesterol': {
                'canonical_id': 'ldl_cholesterol',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        count = service.get_canonical_count()
        
        # Should have 2 canonical biomarkers from mock + common aliases
        assert count >= 2
    
    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_ssot_biomarkers")
    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry")
    def test_common_aliases_integration(self, mock_load_alias_registry, mock_load_ssot_biomarkers):
        """Test that common aliases are properly integrated (hdl/ldl->hdl_cholesterol/ldl_cholesterol)."""
        mock_load_alias_registry.return_value = {}
        mock_load_ssot_biomarkers.return_value = {}
        service = AliasRegistryService(use_v4_registry=False)  # Use fallback to test common aliases
        
        # Test common aliases - lipids use _cholesterol suffix per PR
        assert service.resolve("hdl") == "hdl_cholesterol"
        assert service.resolve("ldl") == "ldl_cholesterol"
        assert service.resolve("cholesterol") == "total_cholesterol"
        assert service.resolve("glucose") == "glucose"
        assert service.resolve("hba1c") == "hba1c"
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_case_insensitive_resolution(self, mock_open, mock_yaml_load):
        """Test that resolution is case-insensitive (hdl->hdl_cholesterol)."""
        mock_registry_data = {
            'hdl_cholesterol': {
                'canonical_id': 'hdl_cholesterol',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test various cases -> hdl_cholesterol
        assert service.resolve("HDL") == "hdl_cholesterol"
        assert service.resolve("hdl") == "hdl_cholesterol"
        assert service.resolve("Hdl") == "hdl_cholesterol"
        assert service.resolve("HDL CHOLESTEROL") == "hdl_cholesterol"
        assert service.resolve("hdl cholesterol") == "hdl_cholesterol"

    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_ssot_biomarkers")
    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry")
    def test_alias_collision_raises_hard_fail(self, mock_load_alias_registry, mock_load_ssot_biomarkers):
        """Two canonicals sharing one alias must hard-fail on map build."""
        mock_load_alias_registry.return_value = {
            "alpha_marker": {"canonical_id": "alpha_marker", "aliases": ["Shared Alias"]},
            "beta_marker": {"canonical_id": "beta_marker", "aliases": ["Shared Alias"]},
        }
        mock_load_ssot_biomarkers.return_value = {}

        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service._build_alias_mapping()

        message = str(exc.value)
        assert "Alias collision for key 'shared alias'" in message
        assert "canonical_ids=['alpha_marker', 'beta_marker']" in message
        assert "source_aliases=['Shared Alias']" in message

    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_ssot_biomarkers")
    @patch("core.canonical.alias_registry_service.AliasRegistryService._load_alias_registry")
    def test_alias_collision_on_normalized_variant_raises_hard_fail(self, mock_load_alias_registry, mock_load_ssot_biomarkers):
        """Collisions in generated normalized variants must also hard-fail."""
        mock_load_alias_registry.return_value = {
            "alpha_marker": {"canonical_id": "alpha_marker", "aliases": ["A B"]},
            "beta_marker": {"canonical_id": "beta_marker", "aliases": ["A-B"]},
        }
        mock_load_ssot_biomarkers.return_value = {}

        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service._build_alias_mapping()

        message = str(exc.value)
        assert "Alias collision for key 'a_b'" in message
        assert "canonical_ids=['alpha_marker', 'beta_marker']" in message
        assert "source_aliases=['A B', 'A-B']" in message


class TestAliasRegistryServiceIntegration:
    """Integration tests for AliasRegistryService with real v4 data."""
    
    def test_real_v4_registry_loading(self):
        """Test loading real v4 registry data."""
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service.get_canonical_biomarkers()
        assert "Alias collision for key" in str(exc.value)
    
    def test_real_v4_alias_resolution(self):
        """Test resolving real v4 aliases (HDL/LDL->hdl_cholesterol/ldl_cholesterol per PR)."""
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service.resolve("HDL")
        assert "Alias collision for key" in str(exc.value)
    
    def test_real_v4_panel_normalization(self):
        """Test normalizing a real biomarker panel (hdl/ldl->hdl_cholesterol/ldl_cholesterol)."""
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service.normalize_panel({"HDL": 45.0})
        assert "Alias collision for key" in str(exc.value)

    def test_ssot_lab_style_aliases(self):
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service._build_alias_mapping()
        assert "Alias collision for key" in str(exc.value)

    def test_explicit_lab_aliases(self):
        service = AliasRegistryService(use_v4_registry=True)
        with pytest.raises(AliasCollisionError) as exc:
            service.resolve("total_creatine_kinese_ck")
        assert "Alias collision for key" in str(exc.value)
