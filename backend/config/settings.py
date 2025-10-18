"""
Centralized application settings and configuration management.

This module provides a single source of truth for all application configuration,
including database settings, API keys, and feature flags.
"""

import os
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class Environment(Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    test_url: Optional[str] = None
    pool_size: int = 10
    max_overflow: int = 20
    pool_recycle: int = 3600
    pool_timeout: int = 30
    echo: bool = False
    echo_pool: bool = False
    
    @classmethod
    def from_env(cls) -> 'DatabaseConfig':
        """Create database config from environment variables."""
        return cls(
            url=os.getenv("DATABASE_URL", ""),
            test_url=os.getenv("DATABASE_URL_TEST"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            echo=os.getenv("DB_ECHO", "false").lower() == "true",
            echo_pool=os.getenv("DB_ECHO_POOL", "false").lower() == "true"
        )


@dataclass
class SupabaseConfig:
    """Supabase configuration settings."""
    url: str
    service_role_key: str
    anon_key: Optional[str] = None
    storage_bucket: str = "healthiq-exports"
    
    @classmethod
    def from_env(cls) -> 'SupabaseConfig':
        """Create Supabase config from environment variables."""
        return cls(
            url=os.getenv("SUPABASE_URL", ""),
            service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
            anon_key=os.getenv("SUPABASE_ANON_KEY"),
            storage_bucket=os.getenv("SUPABASE_STORAGE_BUCKET", "healthiq-exports")
        )


@dataclass
class GeminiConfig:
    """Gemini AI configuration settings."""
    api_key: str
    model: str = "gemini-1.5-pro"
    temperature: float = 0.7
    max_tokens: int = 8192
    timeout: int = 60
    
    @classmethod
    def from_env(cls) -> 'GeminiConfig':
        """Create Gemini config from environment variables."""
        return cls(
            api_key=os.getenv("GEMINI_API_KEY", ""),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "8192")),
            timeout=int(os.getenv("GEMINI_TIMEOUT", "60"))
        )


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    cors_origins: List[str] = field(default_factory=list)
    
    @classmethod
    def from_env(cls) -> 'SecurityConfig':
        """Create security config from environment variables."""
        cors_origins = os.getenv("CORS_ORIGINS", "").split(",")
        cors_origins = [origin.strip() for origin in cors_origins if origin.strip()]
        
        return cls(
            secret_key=os.getenv("SECRET_KEY", ""),
            algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            cors_origins=cors_origins
        )


@dataclass
class MonitoringConfig:
    """Monitoring and logging configuration."""
    log_level: str = "INFO"
    enable_performance_monitoring: bool = True
    slow_query_threshold: float = 1.0
    enable_metrics: bool = True
    metrics_port: int = 8001
    
    @classmethod
    def from_env(cls) -> 'MonitoringConfig':
        """Create monitoring config from environment variables."""
        return cls(
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            enable_performance_monitoring=os.getenv("ENABLE_PERFORMANCE_MONITORING", "true").lower() == "true",
            slow_query_threshold=float(os.getenv("SLOW_QUERY_THRESHOLD", "1.0")),
            enable_metrics=os.getenv("ENABLE_METRICS", "true").lower() == "true",
            metrics_port=int(os.getenv("METRICS_PORT", "8001"))
        )


@dataclass
class FeatureFlags:
    """Feature flags for enabling/disabling functionality."""
    enable_fallback_storage: bool = True
    enable_circuit_breaker: bool = True
    enable_retry_logic: bool = True
    enable_audit_logging: bool = True
    enable_performance_monitoring: bool = True
    enable_export_service: bool = True
    
    @classmethod
    def from_env(cls) -> 'FeatureFlags':
        """Create feature flags from environment variables."""
        return cls(
            enable_fallback_storage=os.getenv("ENABLE_FALLBACK_STORAGE", "true").lower() == "true",
            enable_circuit_breaker=os.getenv("ENABLE_CIRCUIT_BREAKER", "true").lower() == "true",
            enable_retry_logic=os.getenv("ENABLE_RETRY_LOGIC", "true").lower() == "true",
            enable_audit_logging=os.getenv("ENABLE_AUDIT_LOGGING", "true").lower() == "true",
            enable_performance_monitoring=os.getenv("ENABLE_PERFORMANCE_MONITORING", "true").lower() == "true",
            enable_export_service=os.getenv("ENABLE_EXPORT_SERVICE", "true").lower() == "true"
        )


@dataclass
class AppConfig:
    """Main application configuration."""
    environment: Environment
    debug: bool
    database: DatabaseConfig
    supabase: SupabaseConfig
    gemini: GeminiConfig
    security: SecurityConfig
    monitoring: MonitoringConfig
    features: FeatureFlags
    
    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create application config from environment variables."""
        environment = Environment(os.getenv("ENVIRONMENT", "development"))
        debug = os.getenv("DEBUG", "false").lower() == "true"
        
        return cls(
            environment=environment,
            debug=debug,
            database=DatabaseConfig.from_env(),
            supabase=SupabaseConfig.from_env(),
            gemini=GeminiConfig.from_env(),
            security=SecurityConfig.from_env(),
            monitoring=MonitoringConfig.from_env(),
            features=FeatureFlags.from_env()
        )
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate required settings
        if not self.database.url:
            errors.append("DATABASE_URL is required")
        
        if not self.supabase.url:
            errors.append("SUPABASE_URL is required")
        
        if not self.supabase.service_role_key:
            errors.append("SUPABASE_SERVICE_ROLE_KEY is required")
        
        if not self.gemini.api_key:
            errors.append("GEMINI_API_KEY is required")
        
        if not self.security.secret_key:
            errors.append("SECRET_KEY is required")
        
        # Validate numeric ranges
        if self.database.pool_size < 1:
            errors.append("DB_POOL_SIZE must be at least 1")
        
        if self.database.max_overflow < 0:
            errors.append("DB_MAX_OVERFLOW must be non-negative")
        
        if self.gemini.temperature < 0 or self.gemini.temperature > 2:
            errors.append("GEMINI_TEMPERATURE must be between 0 and 2")
        
        if self.monitoring.slow_query_threshold < 0:
            errors.append("SLOW_QUERY_THRESHOLD must be non-negative")
        
        return errors
    
    def get_database_url(self) -> str:
        """Get database URL with validation."""
        if not self.database.url:
            raise ValueError("DATABASE_URL is not configured")
        return self.database.url
    
    def get_supabase_config(self) -> Dict[str, str]:
        """Get Supabase configuration dictionary."""
        return {
            "url": self.supabase.url,
            "service_role_key": self.supabase.service_role_key,
            "anon_key": self.supabase.anon_key,
            "storage_bucket": self.supabase.storage_bucket
        }
    
    def get_gemini_config(self) -> Dict[str, Any]:
        """Get Gemini configuration dictionary."""
        return {
            "api_key": self.gemini.api_key,
            "model": self.gemini.model,
            "temperature": self.gemini.temperature,
            "max_tokens": self.gemini.max_tokens,
            "timeout": self.gemini.timeout
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING


# Global configuration instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get global application configuration."""
    global _config
    if _config is None:
        _config = AppConfig.from_env()
        
        # Validate configuration
        errors = _config.validate()
        if errors:
            error_msg = "Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors)
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Application configuration loaded for {_config.environment.value} environment")
    
    return _config


def reload_config():
    """Reload configuration from environment variables."""
    global _config
    _config = None
    return get_config()


def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return get_config().database


def get_supabase_config() -> SupabaseConfig:
    """Get Supabase configuration."""
    return get_config().supabase


def get_gemini_config() -> GeminiConfig:
    """Get Gemini configuration."""
    return get_config().gemini


def get_security_config() -> SecurityConfig:
    """Get security configuration."""
    return get_config().security


def get_monitoring_config() -> MonitoringConfig:
    """Get monitoring configuration."""
    return get_config().monitoring


def get_feature_flags() -> FeatureFlags:
    """Get feature flags."""
    return get_config().features


def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled."""
    features = get_feature_flags()
    return getattr(features, feature_name, False)


def get_environment() -> Environment:
    """Get current environment."""
    return get_config().environment


def is_production() -> bool:
    """Check if running in production."""
    return get_config().is_production()


def is_development() -> bool:
    """Check if running in development."""
    return get_config().is_development()


def is_testing() -> bool:
    """Check if running in testing."""
    return get_config().is_testing()
