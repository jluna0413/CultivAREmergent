"""
Create nutrient management tables in the database.
Run this before seeding data.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.models_async.base import async_engine, Base
import app.models_async.nutrients  # Import to register models
import logging

logger = logging.getLogger(__name__)


async def create_tables():
    """Create all nutrient-related tables."""
    logger.info("Creating nutrient management tables...")
    
    async with async_engine.begin() as conn:
        # Import all models to ensure they're registered
        from app.models_async.nutrients import (
            NutrientBrand,
            NutrientComponent,
            NutrientFormula,
            WaterSource,
            NutrientInventory,
            InventoryTransaction,
            FeedingSchedule,
            FeedingLog,
        )
        
        # Create tables for nutrient models
        await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())
