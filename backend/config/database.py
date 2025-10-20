import os
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Import Base from core models so models and Alembic share metadata
from core.models.database import Base

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
try:
    # Override with test database if running locally
    if (os.getenv("ENVIRONMENT") == "test" or 
        (DATABASE_URL and "supabase.com" in DATABASE_URL) or 
        "localhost" in os.getenv("HOSTNAME", "")):
        DATABASE_URL = os.getenv("DATABASE_URL_TEST", "postgresql://postgres:test@localhost:5433/healthiq_test")
        print(f"Overriding DATABASE_URL to local test database: {DATABASE_URL}")
except Exception:
    # Fail silently in DB-optional runtime
    pass

# Connection pool configuration
POOL_CONFIG = {
    "pool_size": int(os.getenv("DB_POOL_SIZE", "10")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "20")),
    "pool_pre_ping": True,
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "3600")),  # 1 hour
    "pool_timeout": int(os.getenv("DB_POOL_TIMEOUT", "30")),  # 30 seconds
    "echo": os.getenv("DB_ECHO", "false").lower() == "true",
    "echo_pool": os.getenv("DB_ECHO_POOL", "false").lower() == "true"
}

# Create engine with optimized connection pooling (optional)
engine = None
try:
    if DATABASE_URL:
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            **POOL_CONFIG
        )
except Exception as e:
    logger.warning(f"Database engine not initialized: {e}")

# Add connection event listeners for monitoring
if engine is not None:
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """Set connection-level optimizations."""
        if DATABASE_URL and "postgresql" in DATABASE_URL:
            # PostgreSQL-specific optimizations
            with dbapi_connection.cursor() as cursor:
                cursor.execute("SET statement_timeout = 30000")  # 30 second timeout
                cursor.execute("SET idle_in_transaction_session_timeout = 300000")  # 5 minutes
                cursor.execute("SET lock_timeout = 10000")  # 10 second lock timeout

if engine is not None:
    @event.listens_for(engine, "checkout")
    def receive_checkout(dbapi_connection, connection_record, connection_proxy):
        """Log connection checkout for monitoring."""
        logger.debug("Connection checked out from pool")

if engine is not None:
    @event.listens_for(engine, "checkin")
    def receive_checkin(dbapi_connection, connection_record):
        """Log connection checkin for monitoring."""
        logger.debug("Connection checked in to pool")

# Initialize performance monitoring
try:
    if engine is not None:
        from services.monitoring.performance_monitor import start_performance_monitoring
        start_performance_monitoring(engine)
        logger.info("Performance monitoring enabled")
except ImportError:
    logger.warning("Performance monitoring not available - services.monitoring not found")

# Session factory with optimized settings
SessionLocal = None
if engine is not None:
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        expire_on_commit=False  # Prevent lazy loading issues
    )

# Dependency for FastAPI routes
def get_db():
    """Get database session with proper cleanup."""
    if SessionLocal is None:
        # DB optional runtime: yield a no-op placeholder
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def get_engine() -> Engine:
    """Get the database engine for direct access."""
    return engine  # may be None in DB-optional runtime

def get_pool_status() -> dict:
    """Return safe metrics from SQLAlchemy QueuePool."""
    if engine is None:
        return {"pool_size": 0, "checked_in": 0, "checked_out": 0, "overflow": 0}
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": max(pool.overflow(), 0),  # guard negative values
    }

def test_connection() -> bool:
    """Test database connectivity."""
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def close_all_connections():
    """Close all connections in the pool."""
    if engine is not None:
        engine.dispose()
        logger.info("All database connections closed")
