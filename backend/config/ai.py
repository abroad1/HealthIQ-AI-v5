# backend/config/ai.py

"""
Central LLM configuration manager that validates against LLM_POLICY.md
and selects provider(s) based on environment configuration.
"""

import sys
from typing import Dict, List, Optional
from .env import settings


class LLMConfig:
    """
    Central LLM configuration manager that enforces policy compliance.
    
    Single source of truth: docs/context/LLM_POLICY.md
    """
    
    # Parse providers from comma-separated string
    PROVIDERS = [p.strip() for p in settings.LLM_PROVIDER.split(",")]
    
    # API keys mapping
    API_KEYS: Dict[str, Optional[str]] = {
        "gemini": settings.GEMINI_API_KEY,
        "claude": settings.CLAUDE_API_KEY,
        "openai": settings.OPENAI_API_KEY,
    }
    
    # Policy-defined allowed providers (from LLM_POLICY.md)
    POLICY_ALLOWED_PROVIDERS = {"gemini"}
    
    @classmethod
    def validate(cls) -> None:
        """
        Validate LLM configuration against policy.
        
        Raises:
            ValueError: If configuration violates LLM_POLICY.md
        """
        # Check each configured provider
        for provider in cls.PROVIDERS:
            # Enforce Gemini-only per docs/context/LLM_POLICY.md
            if provider not in cls.POLICY_ALLOWED_PROVIDERS:
                raise ValueError(
                    f"LLM provider '{provider}' not permitted by policy. "
                    f"Allowed providers: {cls.POLICY_ALLOWED_PROVIDERS}. "
                    f"See docs/context/LLM_POLICY.md for details."
                )
            
            # Check API key is provided
            api_key = cls.API_KEYS.get(provider)
            if not api_key:
                raise ValueError(
                    f"API key for provider '{provider}' is missing. "
                    f"Set {provider.upper()}_API_KEY in environment variables."
                )
        
        # Ensure at least one provider is configured
        if not cls.PROVIDERS:
            raise ValueError(
                "No LLM providers configured. Set LLM_PROVIDER environment variable."
            )
    
    @classmethod
    def get_primary_provider(cls) -> str:
        """
        Get the primary LLM provider.
        
        Returns:
            Primary provider name
            
        Raises:
            ValueError: If no providers are configured
        """
        if not cls.PROVIDERS:
            raise ValueError("No LLM providers configured")
        
        return cls.PROVIDERS[0]
    
    @classmethod
    def get_api_key(cls, provider: str) -> Optional[str]:
        """
        Get API key for a specific provider.
        
        Args:
            provider: Provider name
            
        Returns:
            API key or None if not found
        """
        return cls.API_KEYS.get(provider)
    
    @classmethod
    def get_configured_providers(cls) -> List[str]:
        """
        Get list of configured providers.
        
        Returns:
            List of provider names
        """
        return cls.PROVIDERS.copy()
    
    @classmethod
    def is_provider_configured(cls, provider: str) -> bool:
        """
        Check if a provider is configured and has an API key.
        
        Args:
            provider: Provider name to check
            
        Returns:
            True if provider is configured and has API key
        """
        return (
            provider in cls.PROVIDERS and 
            cls.API_KEYS.get(provider) is not None
        )
    
    @classmethod
    def get_config_summary(cls) -> Dict[str, any]:
        """
        Get configuration summary for debugging.
        
        Returns:
            Dictionary with configuration details
        """
        return {
            "configured_providers": cls.PROVIDERS,
            "policy_allowed_providers": list(cls.POLICY_ALLOWED_PROVIDERS),
            "has_api_keys": {
                provider: cls.API_KEYS.get(provider) is not None
                for provider in cls.API_KEYS.keys()
            },
            "primary_provider": cls.get_primary_provider() if cls.PROVIDERS else None
        }


# Validate configuration at import time (only in production)
def validate_configuration():
    """Validate LLM configuration. Call this explicitly when needed."""
    try:
        LLMConfig.validate()
        print(f"OK LLM configuration validated: {LLMConfig.get_configured_providers()}")
        return True
    except Exception as e:
        print(f"ERROR LLM configuration error: {e}")
        print(f"Configuration summary: {LLMConfig.get_config_summary()}")
        return False

# Only validate automatically if not in test environment
if not any('pytest' in arg or 'test' in arg for arg in sys.argv):
    if not validate_configuration():
        sys.exit(1)
