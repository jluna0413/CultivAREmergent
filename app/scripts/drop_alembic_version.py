
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os

# Use the docker internal connection string or localhost mapped port
DATABASE_URL = "postgresql+asyncpg://cultivar:cultivar@localhost:5432/cultivardb"

async def reset_alembic_version():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print("Dropping alembic_version table...")
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))
        print("Table dropped.")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(reset_alembic_version())
