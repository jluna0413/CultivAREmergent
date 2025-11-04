"""
Async SQLAlchemy base module
Provides async database session management for FastAPI
Production-ready configuration with environment-driven settings
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import os
from typing import AsyncGenerator

# Database URL - get from environment or use default (async)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cultivar.db")

# Production performance configuration
ECHO = os.getenv("SQLALCHEMY_ECHO", "False").lower() == "true"
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))

# Create async engine with production settings
async_engine = create_async_engine(
    DATABASE_URL,
    echo=ECHO,  # Environment-driven: True for development, False for production
    future=True,
    # Connection pool settings for production
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    # Additional production optimizations
    pool_recycle=3600,  # Recycle connections every hour
    pool_pre_ping=True,  # Validate connections before use
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    """Base class for all async models"""
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session
    Used by FastAPI endpoints
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    """Create all database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """Drop all database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def close_connections():
    """Close all database connections"""
    await async_engine.dispose()
