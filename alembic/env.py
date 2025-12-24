"""Alembic environment configuration for CultivAR."""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import url as sa_url

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import application config and models after adjusting sys.path
# Import application config and models after adjusting sys.path
from app.config.config import Config  # noqa: E402  pylint: disable=wrong-import-position
# from app.models import db  # noqa: E402  pylint: disable=wrong-import-position

# Ensure all models are imported so metadata includes every table
# import app.models.base_models  # noqa: E402,F401  pylint: disable=wrong-import-position
# import app.models.acinfinity_models  # noqa: E402,F401  pylint: disable=wrong-import-position
# import app.models.ecowitt_models  # noqa: E402,F401  pylint: disable=wrong-import-position
# import app.models.system_models  # noqa: E402,F401  pylint: disable=wrong-import-position

from app.models_async import Base
# Importing the package should load __init__.py which imports all models
import app.models_async

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

target_metadata = Base.metadata


def _get_database_url() -> str:
    """Return the database URL for migrations."""
    override = os.getenv("DATABASE_URL") or os.getenv("ALEMBIC_DATABASE_URL")
    if override:
        return override
    return Config.get_database_uri()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = _get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section, {})
    database_url = _get_database_url()

    # Convert async URL to sync for Alembic if detected
    parsed_url = sa_url.make_url(database_url)
    if parsed_url.drivername.startswith("sqlite+aiosqlite"):
        database_url = str(parsed_url.set(drivername="sqlite"))
    elif parsed_url.drivername.startswith("postgresql+asyncpg"):
        database_url = str(parsed_url.set(drivername="postgresql"))

    print(f"DEBUG: Alembic using database_url: {database_url}")
    configuration["sqlalchemy.url"] = database_url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
