"""
Integration test fixtures. Auto-applies Alembic migrations to test DB before any test.
"""

import os
from pathlib import Path

import pytest


def _is_test_db_allowed(db_url: str) -> bool:
    """Require explicit opt-in before migrating. Refuse non-test databases."""
    if os.getenv("ALLOW_TEST_DB_MIGRATIONS") == "1":
        return True
    if os.getenv("ENVIRONMENT", "").lower() == "test":
        return True
    if os.getenv("HEALTHIQ_MODE", "").lower() == "test":
        return True
    # Database name contains _test or test
    try:
        dbname = db_url.rsplit("/", 1)[-1].split("?")[0].lower()
        if "_test" in dbname or dbname == "test":
            return True
    except Exception:
        pass
    return False


@pytest.fixture(scope="session", autouse=True)
def _migrate_test_db_to_head():
    """
    Run Alembic upgrade head against the test database before any integration test.
    Uses DATABASE_URL (set to DATABASE_URL_TEST by parent conftest).
    Fail-fast if DB is configured but migration cannot run.
    """
    db_url = os.getenv("DATABASE_URL_TEST") or os.getenv("DATABASE_URL")
    if not db_url:
        yield
        return

    if not _is_test_db_allowed(db_url):
        raise RuntimeError(
            "Refusing to migrate non-test database. Set ALLOW_TEST_DB_MIGRATIONS=1, "
            "ENVIRONMENT=test, or use a DB name containing '_test' or 'test'."
        )

    try:
        from alembic.config import Config
        from alembic import command
    except ImportError as e:
        raise RuntimeError(
            f"alembic not installed; cannot auto-migrate test DB: {e}"
        ) from e

    backend_dir = Path(__file__).resolve().parents[2]
    alembic_ini = backend_dir / "alembic.ini"
    if not alembic_ini.exists():
        raise RuntimeError(f"alembic.ini not found at {alembic_ini}")

    cfg = Config(str(alembic_ini))
    cfg.set_main_option("sqlalchemy.url", db_url)

    try:
        command.upgrade(cfg, "head")
    except Exception as e:
        raise RuntimeError(f"Could not migrate test DB to head: {e}") from e

    yield
