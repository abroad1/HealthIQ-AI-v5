import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend/ to sys.path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

# Load .env file into environment
load_dotenv()

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Get the URL from config first
url = config.get_main_option("sqlalchemy.url")

# Allow dynamic override via CLI: `-x url=...`
cmd_opts = context.get_x_argument(as_dictionary=True)
if "url" in cmd_opts:
    url = cmd_opts["url"]
else:
    # Fallback to environment variables if no CLI override
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    # If DATABASE_URL is not set, try to construct it from Supabase configuration
    if not DATABASE_URL:
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")  # User needs to set this
        if SUPABASE_URL and SUPABASE_PASSWORD:
            # Convert Supabase URL to PostgreSQL connection string
            # Format: postgresql://postgres:[password]@[host]:5432/postgres
            host = SUPABASE_URL.replace("https://", "").replace("http://", "")
            DATABASE_URL = f"postgresql://postgres:{SUPABASE_PASSWORD}@{host}:5432/postgres"
        elif SUPABASE_URL:
            # Fallback: construct URL without password (user will need to set SUPABASE_PASSWORD)
            host = SUPABASE_URL.replace("https://", "").replace("http://", "")
            DATABASE_URL = f"postgresql://postgres:YOUR_PASSWORD@{host}:5432/postgres"
            print(f"Warning: SUPABASE_PASSWORD not set. Using placeholder. Set SUPABASE_PASSWORD in .env file.")
            print(f"Constructed DATABASE_URL: {DATABASE_URL}")
    
    if DATABASE_URL:
        url = DATABASE_URL

# Set the final URL in config
config.set_main_option("sqlalchemy.url", url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from config.database import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
