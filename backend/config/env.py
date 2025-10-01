# backend/config/env.py

import os
from typing import Optional
from dotenv import load_dotenv

from dotenv import load_dotenv, find_dotenv
import os

# Ensure .env is loaded from project root
load_dotenv(find_dotenv(), override=True)


class Settings:
    # LLM Configuration (policy-driven)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    CLAUDE_API_KEY: Optional[str] = os.getenv("CLAUDE_API_KEY")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")  # reserved, policy-restricted
    
    # Backend secure environment variables
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    EMAIL_SERVICE_KEY = os.getenv("EMAIL_SERVICE_KEY")
    
    # Frontend public environment variables (for server-side rendering)
    NEXT_PUBLIC_SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    NEXT_PUBLIC_SUPABASE_ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

settings = Settings()
