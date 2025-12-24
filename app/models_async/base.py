import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import text
import logging

# Configure logging
logger = logging.getLogger(__name__)

from app.config.config import Config

# --- Database URL Configuration ---
# Default to SQLite if no other URL is set
if 'pytest' in sys.modules:
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
else:
    DATABASE_URL = Config.get_async_database_uri()

# --- Engine and Session Configuration ---
if 'pytest' in sys.modules:
    async_engine = create_async_engine(
        DATABASE_URL,
        echo=os.environ.get("SQLALCHEMY_ECHO", "False").lower() in ('true', '1', 't'),
    )
else:
    # Configure engine based on database type
    engine_kwargs = {
        'echo': os.environ.get("SQLALCHEMY_ECHO", "False").lower() in ('true', '1', 't'),
    }
    
    # Only apply pool configuration for PostgreSQL databases
    if DATABASE_URL.startswith(('postgresql', 'postgres')):
        engine_kwargs.update({
            'pool_size': 10,
            'max_overflow': 20,
            'pool_recycle': 3600,  # Recycle connections every hour
            'pool_pre_ping': True,  # Check connection before use
        })
    
    async_engine = create_async_engine(DATABASE_URL, **engine_kwargs)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

Base = declarative_base()

# --- Session Management ---
async def get_async_session() -> AsyncSession:
    """
    Dependency to get an async database session.
    Ensures the session is properly closed.
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()

# --- Connection Management ---
async def close_db_connections():
    """
    Properly close the database engine connections.
    """
    logger.info("Closing database connections...")
    await async_engine.dispose()
    logger.info("Database connections closed.")

async def check_db_connection():
    """
    Health check function for the database.
    Returns True if the connection is successful, False otherwise.
    """
    try:
        async with async_engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection health check failed: {e}")
        return False
