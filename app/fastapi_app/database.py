"""
FastAPI Database Configuration - DEPRECATED
This module is deprecated. Use app.models_async.base instead for all database operations.
This file exists for backward compatibility only.
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

# DEPRECATED: Import the canonical implementation
from app.models_async.base import (
    async_engine as engine,
    AsyncSessionLocal as async_session_factory,
    get_async_session as get_database,
    Base
)

logger = logging.getLogger(__name__)

# Legacy aliases for backward compatibility
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cultivar.db")
async_session = None

@asynccontextmanager
async def get_async_db():
    """
    DEPRECATED: Use app.models_async.base.get_async_session instead
    NO AUTO-COMMIT: Manual commit/rollback required by caller
    """
    logger.warning("get_async_db is deprecated. Use app.models_async.base.get_async_session")
    async with get_database() as session:
        try:
            yield session
            # NO AUTO-COMMIT: Caller must explicitly commit
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

@asynccontextmanager
async def get_db_session():
    """
    DEPRECATED: Use app.models_async.base.get_async_session instead
    NO AUTO-COMMIT: Manual commit/rollback required by caller
    """
    logger.warning("get_db_session is deprecated. Use app.models_async.base.get_async_session")
    async with get_database() as session:
        try:
            yield session
            # NO AUTO-COMMIT: Caller must explicitly commit
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_database():
    """
    DEPRECATED: Database initialization is now handled automatically by app.models_async.base
    """
    logger.warning("init_database is deprecated. Database initialization is handled automatically.")
    pass

async def close_database():
    """
    DEPRECATED: Use app.models_async.base.close_connections instead
    """
    from app.models_async.base import close_connections
    await close_connections()

async def health_check_db() -> dict:
    """
    Database health check - delegating to base module
    """
    try:
        from sqlalchemy import text
        async with get_database() as session:
            result = await session.execute(text("SELECT 1"))
            return {
                "database": "healthy",
                "status": "connected"
            }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "database": "unhealthy",
            "error": str(e)
        }