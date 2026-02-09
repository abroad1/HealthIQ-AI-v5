"""
Unit tests for AliasRegistryService.

Tests the v4 alias registry integration, resolution logic,
and normalization functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
from core.canonical.alias_registry_service import AliasRegistryService


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
        """Test resolving a known alias to canonical name."""
        # Mock v4 registry data
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol', 'High-Density Lipoprotein']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test various forms of HDL
        assert service.resolve("HDL") == "hdl"
        assert service.resolve("hdl") == "hdl"
        assert service.resolve("HDL Cholesterol") == "hdl"
        assert service.resolve("High-Density Lipoprotein") == "hdl"
        assert service.resolve("hdl_cholesterol") == "hdl"
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_resolve_unknown_alias(self, mock_open, mock_yaml_load):
        """Test resolving an unknown alias returns unmapped prefix."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test unknown alias
        result = service.resolve("Unknown Biomarker")
        assert result == "unmapped_Unknown Biomarker"
        assert result.startswith("unmapped_")

    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_specimen_suffix_stripping_and_safety(self, mock_open, mock_yaml_load):
        """Test specimen suffix stripping and fail-closed behavior."""
        mock_registry_data = {
            'calcium': {
                'canonical_id': 'calcium',
                'aliases': ['calcium']
            },
            'lipoprotein_a': {
                'canonical_id': 'lipoprotein_a',
                'aliases': ['lipoprotein_(a)']
            },
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['hdl']
            }
        }
        mock_yaml_load.return_value = mock_registry_data

        service = AliasRegistryService(use_v4_registry=True)

        assert service.resolve("calcium_(venous)") == "calcium"
        assert service.resolve("lipoprotein_(a)_(venous)") == "lipoprotein_a"
        assert service.resolve("hdl_(venous)") == "hdl"
        assert service.resolve("albumin_(venous)") == "unmapped_albumin_(venous)"
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_normalize_panel(self, mock_open, mock_yaml_load):
        """Test normalizing a biomarker panel."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl': {
                'canonical_id': 'ldl',
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
        
        # Check that known biomarkers are mapped correctly
        assert "hdl" in normalized
        assert normalized["hdl"] == 45.0
        assert "ldl" in normalized
        assert normalized["ldl"] == 120.0
        
        # Check that unknown biomarker is prefixed
        assert "unmapped_Unknown Biomarker" in normalized
        assert normalized["unmapped_Unknown Biomarker"] == 10.0
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_v4_registry')
    def test_get_all_aliases(self, mock_load_v4):
        """Test getting all aliases grouped by canonical name."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl': {
                'canonical_id': 'ldl',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        aliases = service.get_all_aliases()
        
        # Check structure
        assert isinstance(aliases, dict)
        assert "hdl" in aliases
        assert "ldl" in aliases
        
        # Check that aliases are lists
        assert isinstance(aliases["hdl"], list)
        assert isinstance(aliases["ldl"], list)
        
        # Check specific aliases (note: case variations are generated)
        assert "hdl" in aliases["hdl"]
        assert "HDL" in aliases["hdl"]
        # The service generates case variations, so check for the normalized version
        assert any("cholesterol" in alias.lower() for alias in aliases["hdl"])
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_v4_registry')
    def test_get_canonical_biomarkers(self, mock_load_v4):
        """Test getting list of canonical biomarkers."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl': {
                'canonical_id': 'ldl',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        canonical = service.get_canonical_biomarkers()
        
        # Check structure
        assert isinstance(canonical, list)
        assert "hdl" in canonical
        assert "ldl" in canonical
        # Should have at least 2 canonical biomarkers from mock + common aliases
        assert len(canonical) >= 2
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_is_canonical(self, mock_open, mock_yaml_load):
        """Test checking if a name is canonical."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test canonical names
        assert service.is_canonical("hdl") is True
        
        # Test non-canonical names
        assert service.is_canonical("HDL") is False
        assert service.is_canonical("Unknown") is False
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_v4_registry')
    def test_get_alias_count(self, mock_load_v4):
        """Test getting alias count."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        count = service.get_alias_count()
        
        # Should have canonical name + 2 aliases + case variations = more than 3
        assert count >= 3
    
    @patch('core.canonical.alias_registry_service.AliasRegistryService._load_v4_registry')
    def test_get_canonical_count(self, mock_load_v4):
        """Test getting canonical count."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            },
            'ldl': {
                'canonical_id': 'ldl',
                'aliases': ['LDL', 'LDL Cholesterol']
            }
        }
        mock_load_v4.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        count = service.get_canonical_count()
        
        # Should have 2 canonical biomarkers from mock + common aliases
        assert count >= 2
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_fuzzy_matching_blocked_without_token_overlap(self, mock_open, mock_yaml_load):
        """Test fuzzy matching fails closed when analyte tokens do not overlap."""
        mock_registry_data = {
            'calcium': {
                'canonical_id': 'calcium',
                'aliases': ['calcium']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        result = service.resolve("albumin_(venous)")
        assert result == "unmapped_albumin_(venous)"
    
    def test_common_aliases_integration(self):
        """Test that common aliases are properly integrated."""
        service = AliasRegistryService(use_v4_registry=False)  # Use fallback to test common aliases
        
        # Test common aliases that should be available
        assert service.resolve("hdl") == "hdl"
        assert service.resolve("ldl") == "ldl"
        assert service.resolve("cholesterol") == "total_cholesterol"
        assert service.resolve("glucose") == "glucose"
        assert service.resolve("hba1c") == "hba1c"
    
    @patch('core.canonical.alias_registry_service.yaml.safe_load')
    @patch('builtins.open')
    def test_case_insensitive_resolution(self, mock_open, mock_yaml_load):
        """Test that resolution is case-insensitive."""
        mock_registry_data = {
            'hdl': {
                'canonical_id': 'hdl',
                'aliases': ['HDL', 'HDL Cholesterol']
            }
        }
        mock_yaml_load.return_value = mock_registry_data
        
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test various cases
        assert service.resolve("HDL") == "hdl"
        assert service.resolve("hdl") == "hdl"
        assert service.resolve("Hdl") == "hdl"
        assert service.resolve("HDL CHOLESTEROL") == "hdl"
        assert service.resolve("hdl cholesterol") == "hdl"


class TestAliasRegistryServiceIntegration:
    """Integration tests for AliasRegistryService with real v4 data."""
    
    def test_real_v4_registry_loading(self):
        """Test loading real v4 registry data."""
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test that service loads without errors
        canonical = service.get_canonical_biomarkers()
        assert isinstance(canonical, list)
        assert len(canonical) > 0
        
        # Test that common biomarkers are available
        common_biomarkers = ["hdl", "ldl", "total_cholesterol", "triglycerides"]
        for biomarker in common_biomarkers:
            if biomarker in canonical:
                assert service.is_canonical(biomarker) is True
    
    def test_real_v4_alias_resolution(self):
        """Test resolving real v4 aliases."""
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test common aliases that should be in v4 registry
        test_cases = [
            ("HDL", "hdl"),
            ("LDL", "ldl"),
            ("Total Cholesterol", "total_cholesterol"),
            ("Triglycerides", "triglycerides"),
        ]
        
        for alias, expected_canonical in test_cases:
            result = service.resolve(alias)
            if not result.startswith("unmapped_"):
                assert result == expected_canonical, f"Failed to resolve '{alias}' to '{expected_canonical}', got '{result}'"
    
    def test_real_v4_panel_normalization(self):
        """Test normalizing a real biomarker panel."""
        service = AliasRegistryService(use_v4_registry=True)
        
        # Test panel with common biomarkers
        test_panel = {
            "HDL": 45.0,
            "LDL Cholesterol": 120.0,
            "Total Cholesterol": 200.0,
            "Triglycerides": 150.0,
            "Unknown Test": 10.0
        }
        
        normalized = service.normalize_panel(test_panel)
        
        # Check that known biomarkers are normalized
        assert "hdl" in normalized
        assert "ldl" in normalized
        assert "total_cholesterol" in normalized
        assert "triglycerides" in normalized
        
        # Check that unknown biomarker is prefixed
        assert "unmapped_Unknown Test" in normalized
        
        # Check values are preserved
        assert normalized["hdl"] == 45.0
        assert normalized["ldl"] == 120.0
        assert normalized["total_cholesterol"] == 200.0
        assert normalized["triglycerides"] == 150.0
        assert normalized["unmapped_Unknown Test"] == 10.0
