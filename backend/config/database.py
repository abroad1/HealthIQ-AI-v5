"""
SQLAlchemy engine and session factory for the live FastAPI app.

Schema is managed by Alembic (`backend/migrations`). Operators should run:

    cd backend && alembic upgrade head

when DATABASE_URL points at a fresh database.
"""

from __future__ import annotations

import logging
import os
from typing import Callable, Generator, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

logger = logging.getLogger(__name__)

_engine: Optional[Engine] = None
_session_factory: Optional[Callable[[], Session]] = None


def get_database_url() -> Optional[str]:
    raw = (os.getenv("DATABASE_URL") or "").strip()
    return raw or None


def init_database() -> None:
    """Legacy hook; use log_database_config_on_startup / warmup_engine for live API."""
    if get_database_url():
        logger.info("DATABASE_URL is set — persistence is available.")
    else:
        print("[INIT] DATABASE_URL not set — analysis DB persistence disabled")


def warmup_engine() -> None:
    """Eagerly create engine and verify connectivity (one round-trip)."""
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        url = get_database_url()
        if not url:
            raise RuntimeError("DATABASE_URL is not set")
        _engine = create_engine(url, pool_pre_ping=True)
    return _engine


def get_session_factory() -> Callable[[], Session]:
    global _session_factory
    if _session_factory is None:
        _session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )
    return _session_factory


def log_database_config_on_startup() -> None:
    if get_database_url():
        logger.info("Database persistence enabled (DATABASE_URL is set).")
    else:
        logger.warning("DATABASE_URL not set — authenticated analysis saves will be skipped in test or return 503 in production.")


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: one session per request (raises if DATABASE_URL unset)."""
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_optional() -> Generator[Optional[Session], None, None]:
    """Like get_db, but yields None when DATABASE_URL is unset (unit tests / local without DB)."""
    url = get_database_url()
    if not url:
        yield None
        return

    # In test mode, avoid failing the whole request when Postgres from conftest is not running locally.
    if os.getenv("HEALTHIQ_MODE", "").lower() == "test":
        try:
            probe = create_engine(url, pool_pre_ping=True)
            with probe.connect() as conn:
                conn.execute(text("SELECT 1"))
            probe.dispose()
        except Exception:
            yield None
            return

    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
