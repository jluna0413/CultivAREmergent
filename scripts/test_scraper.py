import asyncio
import sys
import os
import logging
from pathlib import Path

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.agents.seedfinder_scraper import SeedFinderScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_scraper():
    logger.info("Initializing SeedFinderScraper...")
    scraper = SeedFinderScraper()
    
    try:
        # Test 1: Search Strain
        strain_name = "OG Kush"
        logger.info(f"\n--- Testing Strain Search: {strain_name} ---")
        strain_data = await scraper.search_strain(strain_name)
        
        if strain_data:
            logger.info("✅ Strain Found!")
            logger.info(f"Name: {strain_data.get('name')}")
            logger.info(f"Breeder: {strain_data.get('breeder_name')}")
            logger.info(f"Genetics: {strain_data.get('indica_pct')}% Indica / {strain_data.get('sativa_pct')}% Sativa")
            logger.info(f"Terpenes: {strain_data.get('terpene_profile')}")
            logger.info(f"URL: {strain_data.get('source_url')}")
        else:
            logger.error("❌ Strain Search Failed (or not found)")

        # Test 2: Search Breeder
        breeder_name = "Barneys Farm"
        logger.info(f"\n--- Testing Breeder Search: {breeder_name} ---")
        breeder_data = await scraper.search_breeder(breeder_name)
        
        if breeder_data:
            logger.info("✅ Breeder Found!")
            logger.info(f"Name: {breeder_data.get('name')}")
            logger.info(f"Country: {breeder_data.get('country')}")
            logger.info(f"Website: {breeder_data.get('website')}")
            logger.info(f"URL: {breeder_data.get('source_url')}")
            logger.info(f"ID: {breeder_data.get('source_id')}")
        else:
            logger.error("❌ Breeder Search Failed")
            
    except Exception as e:
        logger.error(f"Test failed with exception: {e}")
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(test_scraper())
