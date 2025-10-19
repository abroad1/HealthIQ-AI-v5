"""
Pytest configuration and fixtures for backend tests.
"""

import sys
import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load test environment variables
load_dotenv(dotenv_path="backend/.env.test")

# Add the backend directory to Python path for imports
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_db():
    """Truncate key tables after tests finish to ensure clean state."""
    from sqlalchemy import create_engine, text
    
    db_url = os.getenv("DATABASE_URL_TEST")
    if not db_url:
        yield
        return
    
    engine = create_engine(db_url)
    yield
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE profiles, analyses, consents, audit_logs RESTART IDENTITY CASCADE;"))


@pytest.fixture(scope="session", autouse=True)
def _register_insights_once():
    """Ensure all insight modules are registered before any tests run."""
    from core.insights.registry import ensure_insights_registered
    ensure_insights_registered()


@pytest.fixture(scope="function")
def db_session():
    """Provide a temporary SQLAlchemy session for tests."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from config.settings import get_config
    
    config = get_config()
    
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
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()