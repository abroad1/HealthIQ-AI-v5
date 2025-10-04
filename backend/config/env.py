# backend/config/env.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

class Settings:
    # Backend secure environment variables
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    EMAIL_SERVICE_KEY = os.getenv("EMAIL_SERVICE_KEY")
    
    # Frontend public environment variables (for server-side rendering)
    NEXT_PUBLIC_SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    NEXT_PUBLIC_SUPABASE_ANON_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")

settings = Settings()
