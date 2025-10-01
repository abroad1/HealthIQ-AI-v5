"""
Unit tests for Gemini configuration and environment loading.
"""

import pytest
import os
from unittest.mock import patch
from config.ai import LLMConfig


class TestGeminiConfig:
    """Test Gemini configuration loading and validation."""
    
    def test_gemini_api_key_loaded(self):
        """Test that GEMINI_API_KEY is loaded from environment."""
        # This test only checks that the key is loaded, not its value
        gemini_key = LLMConfig.API_KEYS["gemini"]
        assert gemini_key is not None
        assert isinstance(gemini_key, str)
        assert len(gemini_key) > 0
    
    def test_llm_provider_configuration(self):
        """Test that LLM_PROVIDER is correctly configured."""
        assert "gemini" in LLMConfig.PROVIDERS
        assert LLMConfig.get_primary_provider() == "gemini"
    
    def test_gemini_provider_configured(self):
        """Test that Gemini provider is properly configured."""
        assert LLMConfig.is_provider_configured("gemini")
        assert LLMConfig.get_api_key("gemini") is not None
    
    def test_config_validation_passes(self):
        """Test that configuration validation passes with valid setup."""
        # This should not raise an exception
        LLMConfig.validate()
    
    def test_missing_gemini_key_fails(self):
        """Test that missing GEMINI_API_KEY causes validation to fail."""
        # Test the validation logic directly by mocking the API_KEYS
        original_api_keys = LLMConfig.API_KEYS.copy()
        original_providers = LLMConfig.PROVIDERS.copy()
        
        try:
            # Mock the configuration to simulate missing API key
            LLMConfig.API_KEYS["gemini"] = None
            LLMConfig.PROVIDERS = ["gemini"]
            
            with pytest.raises(ValueError, match="API key for provider 'gemini' is missing"):
                LLMConfig.validate()
        finally:
            # Restore original values
            LLMConfig.API_KEYS.update(original_api_keys)
            LLMConfig.PROVIDERS = original_providers
    
    def test_config_summary_structure(self):
        """Test that config summary has expected structure."""
        summary = LLMConfig.get_config_summary()
        
        assert "configured_providers" in summary
        assert "policy_allowed_providers" in summary
        assert "has_api_keys" in summary
        assert "primary_provider" in summary
        
        assert isinstance(summary["configured_providers"], list)
        assert isinstance(summary["has_api_keys"], dict)
        assert summary["primary_provider"] == "gemini"
