"""
Seed data for nutrient brands, components, and formulas.
Run this script to populate the database with common nutrient lines.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from app.models_async.base import get_async_session
from app.models_async.nutrients import NutrientBrand, NutrientComponent, NutrientFormula
import logging

logger = logging.getLogger(__name__)


async def seed_general_hydroponics(db: AsyncSession):
    """Seed General Hydroponics FloraSeries."""
    brand = NutrientBrand(
        name="General Hydroponics FloraSeries",
        manufacturer="General Hydroponics",
        brand_type="3-part",
        component_count=3,
        description="Classic 3-part nutrient system used worldwide",
    )
    db.add(brand)
    await db.flush()

    # Components
    flora_gro = NutrientComponent(
        brand_id=brand.id,
        name="FloraGro",
        npk_ratio="2-1-6",
        description="Vegetative growth formula",
        order_index=1,
    )
    flora_micro = NutrientComponent(
        brand_id=brand.id,
        name="FloraMicro",
        npk_ratio="5-0-1",
        description="Micronutrients and foundation",
        order_index=2,
    )
    flora_bloom = NutrientComponent(
        brand_id=brand.id,
        name="FloraBloom",
        npk_ratio="0-5-4",
        description="Flowering formula",
        order_index=3,
    )
    db.add_all([flora_gro, flora_micro, flora_bloom])
    await db.flush()

    # Formulas for different stages (Hydro medium)
    formulas = [
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="seedling",
            medium="hydro",
            ratios={flora_gro.id: 0.5, flora_micro.id: 0.5, flora_bloom.id: 0.25},
            ppm_target_min=250,
            ppm_target_max=350,
            ec_target_min=0.5,
            ec_target_max=0.7,
            ph_target_min=5.5,
            ph_target_max=6.2,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_veg",
            medium="hydro",
            ratios={flora_gro.id: 1.0, flora_micro.id: 1.0, flora_bloom.id: 0.5},
            ppm_target_min=400,
            ppm_target_max=600,
            ec_target_min=0.8,
            ec_target_max=1.2,
            ph_target_min=5.5,
            ph_target_max=6.0,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="late_veg",
            medium="hydro",
            ratios={flora_gro.id: 2.0, flora_micro.id: 2.0, flora_bloom.id: 1.0},
            ppm_target_min=700,
            ppm_target_max=900,
            ec_target_min=1.4,
            ec_target_max=1.8,
            ph_target_min=5.5,
            ph_target_max=6.0,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_flower",
            medium="hydro",
            ratios={flora_gro.id: 1.0, flora_micro.id: 2.0, flora_bloom.id: 2.5},
            ppm_target_min=900,
            ppm_target_max=1200,
            ec_target_min=1.8,
            ec_target_max=2.4,
            ph_target_min=5.8,
            ph_target_max=6.3,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="mid_flower",
            medium="hydro",
            ratios={flora_gro.id: 0.5, flora_micro.id: 2.0, flora_bloom.id: 3.0},
            ppm_target_min=1000,
            ppm_target_max=1400,
            ec_target_min=2.0,
            ec_target_max=2.8,
            ph_target_min=5.8,
            ph_target_max=6.3,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="late_flower",
            medium="hydro",
            ratios={flora_gro.id: 0.25, flora_micro.id: 1.5, flora_bloom.id: 2.5},
            ppm_target_min=800,
            ppm_target_max=1200,
            ec_target_min=1.6,
            ec_target_max=2.4,
            ph_target_min=5.8,
            ph_target_max=6.5,
        ),
    ]
    db.add_all(formulas)
    logger.info(f"✓ Seeded General Hydroponics FloraSeries with {len(formulas)} formulas")


async def seed_fox_farm(db: AsyncSession):
    """Seed Fox Farm Trio."""
    brand = NutrientBrand(
        name="Fox Farm Trio",
        manufacturer="Fox Farm",
        brand_type="3-part",
        component_count=3,
        description="Popular organic-based nutrient trio",
    )
    db.add(brand)
    await db.flush()

    # Components
    grow_big = NutrientComponent(
        brand_id=brand.id,
        name="Grow Big",
        npk_ratio="6-4-4",
        description="Vegetative growth booster",
        order_index=1,
    )
    big_bloom = NutrientComponent(
        brand_id=brand.id,
        name="Big Bloom",
        npk_ratio="0.01-0.3-0.7",
        description="Micro-nutrients and beneficial organisms",
        order_index=2,
    )
    tiger_bloom = NutrientComponent(
        brand_id=brand.id,
        name="Tiger Bloom",
        npk_ratio="2-8-4",
        description="Flowering formula",
        order_index=3,
    )
    db.add_all([grow_big, big_bloom, tiger_bloom])
    await db.flush()

    # Formulas for soil medium
    formulas = [
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_veg",
            medium="soil",
            ratios={grow_big.id: 1.0, big_bloom.id: 2.0, tiger_bloom.id: 0},
            ppm_target_min=400,
            ppm_target_max=600,
            ec_target_min=0.8,
            ec_target_max=1.2,
            ph_target_min=6.0,
            ph_target_max=6.8,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="late_veg",
            medium="soil",
            ratios={grow_big.id: 2.0, big_bloom.id: 3.0, tiger_bloom.id: 0},
            ppm_target_min=600,
            ppm_target_max=800,
            ec_target_min=1.2,
            ec_target_max=1.6,
            ph_target_min=6.0,
            ph_target_max=6.8,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_flower",
            medium="soil",
            ratios={grow_big.id: 0, big_bloom.id: 3.0, tiger_bloom.id: 2.0},
            ppm_target_min=800,
            ppm_target_max=1000,
            ec_target_min=1.6,
            ec_target_max=2.0,
            ph_target_min=6.0,
            ph_target_max=7.0,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="mid_flower",
            medium="soil",
            ratios={grow_big.id: 0, big_bloom.id: 3.0, tiger_bloom.id: 4.0},
            ppm_target_min=1000,
            ppm_target_max=1200,
            ec_target_min=2.0,
            ec_target_max=2.4,
            ph_target_min=6.0,
            ph_target_max=7.0,
        ),
    ]
    db.add_all(formulas)
    logger.info(f"✓ Seeded Fox Farm Trio with {len(formulas)} formulas")


async def seed_canna_coco(db: AsyncSession):
    """Seed Canna Coco A&B."""
    brand = NutrientBrand(
        name="Canna Coco A&B",
        manufacturer="Canna",
        brand_type="2-part",
        component_count=2,
        description="Premium 2-part system optimized for coco coir",
    )
    db.add(brand)
    await db.flush()

    # Components
    canna_a = NutrientComponent(
        brand_id=brand.id,
        name="Canna Coco A",
        npk_ratio="5-0-1",
        description="Part A - Calcium and trace elements",
        order_index=1,
    )
    canna_b = NutrientComponent(
        brand_id=brand.id,
        name="Canna Coco B",
        npk_ratio="1-4-2",
        description="Part B - Phosphorus and potassium",
        order_index=2,
    )
    db.add_all([canna_a, canna_b])
    await db.flush()

    # Formulas for coco medium
    formulas = [
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_veg",
            medium="coco",
            ratios={canna_a.id: 1.0, canna_b.id: 1.0},
            ppm_target_min=500,
            ppm_target_max=700,
            ec_target_min=1.0,
            ec_target_max=1.4,
            ph_target_min=5.8,
            ph_target_max=6.2,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="late_veg",
            medium="coco",
            ratios={canna_a.id: 2.0, canna_b.id: 2.0},
            ppm_target_min=700,
            ppm_target_max=1000,
            ec_target_min=1.4,
            ec_target_max=2.0,
            ph_target_min=5.8,
            ph_target_max=6.2,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="early_flower",
            medium="coco",
            ratios={canna_a.id: 2.5, canna_b.id: 2.5},
            ppm_target_min=1000,
            ppm_target_max=1300,
            ec_target_min=2.0,
            ec_target_max=2.6,
            ph_target_min=5.8,
            ph_target_max=6.5,
        ),
        NutrientFormula(
            brand_id=brand.id,
            growth_stage="mid_flower",
            medium="coco",
            ratios={canna_a.id: 3.0, canna_b.id: 3.0},
            ppm_target_min=1200,
            ppm_target_max=1600,
            ec_target_min=2.4,
            ec_target_max=3.2,
            ph_target_min=6.0,
            ph_target_max=6.5,
        ),
    ]
    db.add_all(formulas)
    logger.info(f"✓ Seeded Canna Coco A&B with {len(formulas)} formulas")


async def main():
    """Main seed function."""
    logger.info("Starting nutrient database seeding...")
    
    async for db in get_async_session():
        try:
            await seed_general_hydroponics(db)
            await seed_fox_farm(db)
            await seed_canna_coco(db)
            
            await db.commit()
            logger.info("✅ Nutrient database seeding completed successfully!")
            
        except Exception as e:
            await db.rollback()
            logger.error(f"❌ Error seeding database: {e}")
            raise
        finally:
            await db.close()
            break  # Only run once


if __name__ == "__main__":
    asyncio.run(main())
