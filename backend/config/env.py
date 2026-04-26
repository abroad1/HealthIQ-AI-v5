# backend/config/env.py

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv, find_dotenv

# 1) Legacy: first .env found walking upward from os.getcwd() (monorepo root, etc.)
load_dotenv(find_dotenv(), override=True)

# 2) Authoritative for API vars: always merge backend/.env (next to this package's parent),
#    with override so local edits win over a parent directory .env. Without this, only
#    HEALTHIQ_FREE_COMPLETED_ANALYSES in a discovered root .env applied; supabase_anon
#    loads the same file with override=False and could not fix a bad parent value.
_backend_root = Path(__file__).resolve().parent.parent
load_dotenv(_backend_root / ".env", override=True)


class Settings:
    # LLM Configuration (policy-driven)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    # Test mode: when HEALTHIQ_MODE=test or LLM_ENABLED=false, skip LLM init/calls
    HEALTHIQ_MODE: str = os.getenv("HEALTHIQ_MODE", "")
    # BE-S1B: with default orchestrator path, live insight narrative also requires
    # HEALTHIQ_NARRATIVE_LLM=1 (read in narrative_runtime_policy; not duplicated here).
    LLM_ENABLED: bool = os.getenv("LLM_ENABLED", "true").lower() in ("true", "1", "yes")
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
