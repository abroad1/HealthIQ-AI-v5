# TODO: Implement database configuration
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .settings import settings

# Database engine
if settings.database_url:
    engine = create_engine(
        settings.database_url,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        echo=settings.debug
    )
else:
    # Fallback to SQLite for development
    engine = create_engine(
        "sqlite:///./healthiq.db",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=settings.debug
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Metadata
metadata = MetaData()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables."""
    # TODO: Import all models here
    # from ..core.models import user, biomarker, analysis
    Base.metadata.create_all(bind=engine)
