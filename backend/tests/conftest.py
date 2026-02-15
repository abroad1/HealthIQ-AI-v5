"""
Pytest configuration and fixtures for backend tests.
"""

import sys
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# (a) Set test mode and DB env vars BEFORE any app/config imports
os.environ["HEALTHIQ_MODE"] = "test"
os.environ["LLM_ENABLED"] = "false"
_TEST_DB_URL = "postgresql://postgres:test@localhost:5433/healthiq_test"
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("DATABASE_URL_TEST", _TEST_DB_URL)
os.environ.setdefault("DATABASE_URL", os.environ["DATABASE_URL_TEST"])

# Load test environment variables
load_dotenv(dotenv_path="backend/.env.test")

# (b) Re-assert minimal required vars after load_dotenv (no external service creds)
os.environ["HEALTHIQ_MODE"] = "test"
os.environ["LLM_ENABLED"] = "false"
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("DATABASE_URL_TEST", _TEST_DB_URL)
os.environ.setdefault("DATABASE_URL", os.environ["DATABASE_URL_TEST"])

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Truncate key tables after tests finish to ensure clean state."""
    from sqlalchemy import create_engine, text
    from sqlalchemy.exc import OperationalError
    
    db_url = os.getenv("DATABASE_URL_TEST")
    if not db_url:
        yield
        return
    
    engine = create_engine(db_url)
    yield
    try:
        with engine.begin() as conn:
            conn.execute(text("TRUNCATE profiles, analyses, consents, audit_logs RESTART IDENTITY CASCADE;"))
    except OperationalError:
        return


@pytest.fixture(scope="session", autouse=True)
def _register_insights_once():
    """Ensure all insight modules are registered before any tests run."""
    from core.insights.registry import ensure_insights_registered
    ensure_insights_registered()


@pytest.fixture
def lab_reference_ranges():
    """
    Lab-provided reference ranges for integration tests.
    Deterministic, local to tests. Format: {canonical_id: {"min": float, "max": float, "unit": str}}.
    """
    return {
        "glucose": {"min": 70.0, "max": 100.0, "unit": "mg/dL"},
        "hba1c": {"min": 4.0, "max": 5.6, "unit": "%"},
        "insulin": {"min": 2.0, "max": 25.0, "unit": "μU/mL"},
        "total_cholesterol": {"min": 100.0, "max": 250.0, "unit": "mg/dL"},
        "ldl_cholesterol": {"min": 0.0, "max": 130.0, "unit": "mg/dL"},
        "hdl_cholesterol": {"min": 40.0, "max": 80.0, "unit": "mg/dL"},
        "triglycerides": {"min": 0.0, "max": 150.0, "unit": "mg/dL"},
        "crp": {"min": 0.0, "max": 3.0, "unit": "mg/L"},
        "creatinine": {"min": 0.6, "max": 1.2, "unit": "mg/dL"},
        "bun": {"min": 7.0, "max": 20.0, "unit": "mg/dL"},
        "alt": {"min": 7.0, "max": 56.0, "unit": "U/L"},
        "ast": {"min": 10.0, "max": 40.0, "unit": "U/L"},
        "hemoglobin": {"min": 12.0, "max": 16.0, "unit": "g/dL"},
        "hematocrit": {"min": 36.0, "max": 46.0, "unit": "%"},
        "white_blood_cells": {"min": 4.5, "max": 11.0, "unit": "K/μL"},
        "platelets": {"min": 150.0, "max": 450.0, "unit": "K/μL"},
    }


@pytest.fixture(scope="function")
def db_session():
    """Provide a temporary SQLAlchemy session for tests. DB probe + skip run only when
    this fixture is used (db-dependent integration tests); not at import time."""
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.exc import OperationalError
    from config.settings import get_config

    try:
        config = get_config()
    except ValueError as e:
        pytest.skip(
            f"Config validation failed (missing SUPABASE/GEMINI in env): {e}. "
            "Set required vars in .env.test for persistence tests."
        )
    
    # Use test database if available, otherwise fall back to production
    database_url = config.database.test_url or config.database.url
    
    # Safety check: prevent accidental production database usage
    if '.supabase.co' in database_url:
        raise ValueError(
            "Tests cannot run against Supabase production database. "
            "Use DATABASE_URL_TEST for local testing. "
            "Set DATABASE_URL_TEST=postgresql://postgres:test@localhost:5433/healthiq_test"
        )
    
    engine = create_engine(database_url)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as e:
        pytest.skip(
            f"PostgreSQL not reachable at {database_url}. "
            "Start Docker or local Postgres for persistence tests."
        )
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()