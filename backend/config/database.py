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

# Sprint 15 - Environment guards for local/prod separation
ENV = os.getenv("ENVIRONMENT", "local")
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST", "postgresql://postgres:test@localhost:5433/healthiq_test")

# Override with test database if running locally
if (ENV == "test" or 
    ENV == "local" or
    "supabase.com" in DATABASE_URL or 
    "localhost" in os.getenv("HOSTNAME", "")):
    DATABASE_URL = DATABASE_URL_TEST
    print(f"[ENV-GUARD] Overriding DATABASE_URL to local test database: {DATABASE_URL}")

# Sprint 15 - Assertion to prevent production writes during local testing
if ENV == "local" and "supabase.com" in DATABASE_URL:
    raise ValueError("Cannot use Supabase production database in local environment. Use DATABASE_URL_TEST instead.")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in environment")

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

# Create engine with optimized connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    **POOL_CONFIG
)

# Add connection event listeners for monitoring
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set connection-level optimizations."""
    if "postgresql" in DATABASE_URL:
        # PostgreSQL-specific optimizations
        with dbapi_connection.cursor() as cursor:
            cursor.execute("SET statement_timeout = 30000")  # 30 second timeout
            cursor.execute("SET idle_in_transaction_session_timeout = 300000")  # 5 minutes
            cursor.execute("SET lock_timeout = 10000")  # 10 second lock timeout

@event.listens_for(engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log connection checkout for monitoring."""
    logger.debug("Connection checked out from pool")

@event.listens_for(engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Log connection checkin for monitoring."""
    logger.debug("Connection checked in to pool")

# Initialize performance monitoring
try:
    from services.monitoring.performance_monitor import start_performance_monitoring
    start_performance_monitoring(engine)
    logger.info("Performance monitoring enabled")
except ImportError:
    logger.warning("Performance monitoring not available - services.monitoring not found")

# Session factory with optimized settings
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # Prevent lazy loading issues
)

# Dependency for FastAPI routes
def get_db():
    """Get database session with proper cleanup."""
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
    return engine

def get_pool_status() -> dict:
    """Return safe metrics from SQLAlchemy QueuePool."""
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_in": pool.checkedin(),
        "checked_out": pool.checkedout(),
        "overflow": max(pool.overflow(), 0),  # guard negative values
    }

def test_connection() -> bool:
    """Test database connectivity."""
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
    engine.dispose()
    logger.info("All database connections closed")
