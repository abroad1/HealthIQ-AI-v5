"""
Application Configuration

This module contains configuration settings for the HealthIQ-AI-v5 application.
"""

import os
from typing import Optional


class Settings:
    """Application settings."""

    # Supabase Auth (backend): align with frontend NEXT_PUBLIC_SUPABASE_* / .env.local
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_ANON_KEY: Optional[str] = os.getenv("SUPABASE_ANON_KEY")
    
    # Validation settings
    STRICT_VALIDATION: bool = os.getenv("STRICT_VALIDATION", "false").lower() == "true"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "HealthIQ-AI-v5"
    
    # Database settings (if needed in future)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File paths
    BIOMARKER_ALIAS_REGISTRY_PATH: str = "backend/ssot/biomarker_alias_registry.yaml"
    BIOMARKERS_PATH: str = "backend/ssot/biomarkers.yaml"
    
    # Validation report settings
    VALIDATION_REPORT_DIR: str = "tests/reports"


# Global settings instance
settings = Settings()
