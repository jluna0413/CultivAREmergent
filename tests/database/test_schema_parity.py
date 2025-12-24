
import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import inspect
import os
import asyncio

# Use the same logic as validation, relying on env vars or defaulting to test db
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://cultivar:cultivar@localhost:5432/cultivardb")

@pytest.mark.asyncio
async def test_phase_1_1_schema_parity():
    """
    Verifies that the database schema contains all tables and columns 
    required by Phase 1.1 of the Genetics Marketplace, including 
    Merch tables and User Genetics metadata.
    """
    engine = create_async_engine(DATABASE_URL)
    
    expected_tables = {
        "exclusive_drop_nfts",
        "marketplace_breeders",
        "user_genetics",
        "gnft_packs",
        "gnft_listings",
        "sales_transactions",
        "user_wallets",
        "wallet_transactions",
        "user_xp",
        "user_achievements",
        "user_streaks",
        "checkin_logs",
        "marketplace_listings",
        "auctions",
        "auction_bids",
        "auction_watches",
        "merch_products",
        "merch_orders",
        "hypergraph_strain_mapping",
        "hypergraph_breeder_mapping"
    }

    async with engine.connect() as conn:
        def get_tables(connection):
            inspector = inspect(connection)
            return set(inspector.get_table_names())

        tables = await conn.run_sync(get_tables)
        
        # Check for missing tables
        missing_tables = expected_tables - tables
        assert not missing_tables, f"Missing Critical Phase 1.1 Tables: {missing_tables}"
        
        # Check user_genetics columns
        if "user_genetics" in tables:
            def get_columns(connection):
                inspector = inspect(connection)
                return {c['name'] for c in inspector.get_columns("user_genetics")}
            
            columns = await conn.run_sync(get_columns)
            required_cols = {"lineage_string", "dominant_terpenes", "thc_percentage", "cbd_percentage"}
            missing_cols = required_cols - columns
            assert not missing_cols, f"user_genetics table missing required columns: {missing_cols}"
            
    await engine.dispose()
