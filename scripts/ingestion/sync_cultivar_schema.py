#!/usr/bin/env python3
"""
Sync Cultivar table schema with model definition.
Adds all missing columns from the Cultivar model.
"""
import asyncio
import sys
import os
from pathlib import Path

# Force UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy import text
from app.fastapi_app.database import engine

# All columns needed based on Cultivar model (with their SQL types)
COLUMNS_TO_ADD = [
    ("ruderalis", "INTEGER DEFAULT 0"),
    ("short_description", "VARCHAR(500)"),
    ("parent_1", "VARCHAR(100)"),
    ("parent_2", "VARCHAR(100)"),
    ("parent_1_id", "INTEGER REFERENCES cultivars(id)"),
    ("parent_2_id", "INTEGER REFERENCES cultivars(id)"),
    ("lineage_json", "JSONB"),
    ("genetics_type", "VARCHAR(50)"),
    ("leafly_slug", "VARCHAR(100)"),
    ("weedmaps_id", "VARCHAR(100)"),
    ("thc_content", "FLOAT"),
    ("thc_min", "FLOAT"),
    ("thc_max", "FLOAT"),
    ("cbd_content", "FLOAT"),
    ("cbd_min", "FLOAT"),
    ("cbd_max", "FLOAT"),
    ("cbg_content", "FLOAT"),
    ("thcv_content", "FLOAT"),
    ("cbc_content", "FLOAT"),
    ("cbn_content", "FLOAT"),
    ("delta8_content", "FLOAT"),
    ("thca_content", "FLOAT"),
    ("cbda_content", "FLOAT"),
    ("cannabinoid_profile", "JSONB"),
    ("myrcene", "FLOAT"),
    ("limonene", "FLOAT"),
    ("caryophyllene", "FLOAT"),
    ("linalool", "FLOAT"),
    ("pinene", "FLOAT"),
    ("humulene", "FLOAT"),
    ("terpinolene", "FLOAT"),
    ("ocimene", "FLOAT"),
    ("bisabolol", "FLOAT"),
    ("terpene_profile", "JSONB"),
    ("dominant_terpene", "VARCHAR(50)"),
    ("flavors", "JSONB"),
    ("aromas", "JSONB"),
    ("taste_description", "TEXT"),
    ("aroma_description", "TEXT"),
    ("effects", "JSONB"),
    ("effects_description", "TEXT"),
    ("medical_benefits", "JSONB"),
    ("medical_description", "TEXT"),
    ("negative_effects", "JSONB"),
    ("potency_rating", "INTEGER"),
    ("body_high", "INTEGER"),
    ("head_high", "INTEGER"),
    ("flowering_type", "VARCHAR(50)"),
    ("flowering_time_min", "INTEGER"),
    ("flowering_time_max", "INTEGER"),
    ("cycle_time", "INTEGER"),
    ("yield_indoor", "VARCHAR(50)"),
    ("yield_outdoor", "VARCHAR(50)"),
    ("height_indoor", "VARCHAR(50)"),
    ("height_outdoor", "VARCHAR(50)"),
    ("grow_difficulty", "VARCHAR(50)"),
    ("climate", "JSONB"),
    ("optimal_temp_min", "INTEGER"),
    ("optimal_temp_max", "INTEGER"),
    ("humidity_preference", "VARCHAR(50)"),
    ("mold_resistance", "VARCHAR(50)"),
    ("pest_resistance", "VARCHAR(50)"),
    ("seed_count", "INTEGER DEFAULT 0"),
    ("url", "VARCHAR(255)"),
    ("image_urls", "JSONB DEFAULT '[]'::jsonb"),
    ("data_source", "VARCHAR(50)"),
    ("last_verified", "TIMESTAMP"),
    ("verification_status", "VARCHAR(50)"),
    ("awards", "JSONB"),
    ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
    ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
]

async def sync_schema():
    """Add all missing columns to cultivars table."""
    added = 0
    async with engine.begin() as conn:
        for col_name, col_type in COLUMNS_TO_ADD:
            # Remove references for simpler ADD COLUMN
            simple_type = col_type.split(" REFERENCES")[0]
            sql = f"ALTER TABLE cultivars ADD COLUMN IF NOT EXISTS {col_name} {simple_type}"
            try:
                await conn.execute(text(sql))
                print(f"[OK] Added/verified column: {col_name}")
                added += 1
            except Exception as e:
                print(f"[FAIL] Failed to add {col_name}: {e}")
    
    print(f"\nDone! Processed {added} columns.")

if __name__ == "__main__":
    asyncio.run(sync_schema())
