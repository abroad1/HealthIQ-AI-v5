# TODO: Implement settings configuration
from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # API Settings
    api_title: str = "HealthIQ AI v5"
    api_version: str = "1.0.0"
    api_description: str = "Precision Biomarker Intelligence Platform"
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Database Settings
    database_url: Optional[str] = None
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Redis Settings
    redis_url: Optional[str] = None
    
    # AI/ML Settings
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    model_provider: str = "openai"
    model_name: str = "gpt-4"
    
    # Security Settings
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30
    algorithm: str = "HS256"
    
    # CORS Settings
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
