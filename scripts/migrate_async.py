import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models_async.base import Base
from app.logger import logger

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./instance/cultivar.db")

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)

async def run_migrations():
    logger.info("Running async database migrations...")
    async with async_engine.begin() as conn:
        # This will create tables based on Base.metadata if they don't exist
        # For more complex migrations (e.g., schema changes, data migrations),
        # Alembic should be used. This script is for initial table creation.
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Async database migrations complete (tables created/updated).")

    # Optionally, run initial data seeding if the database is empty
    from scripts.init_db_async import init_db
    await init_db()

if __name__ == "__main__":
    asyncio.run(run_migrations())
