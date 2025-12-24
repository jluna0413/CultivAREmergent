#!/usr/bin/env python3
"""
SeedFinder Full Database Ingestion Script

Systematically crawls SeedFinder.eu to ingest all breeders and their strains
into the CultivAR database with HyperGraph sync.

Features:
- Checkpointing: Resumes from last position if interrupted
- Rate limiting: Configurable delay between LLM extractions
- Progress tracking: Detailed logging and progress file
- Dry run mode: Preview without database writes

Usage:
    python ingest_seedfinder_full.py                    # Full ingestion
    python ingest_seedfinder_full.py --dry-run          # Preview mode
    python ingest_seedfinder_full.py --breeders-only    # Just fetch breeder list
    python ingest_seedfinder_full.py --limit 10         # Limit to first 10 breeders
"""

import asyncio
import json
import logging
import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Force UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.fastapi_app.database import async_session_factory
from app.models_async import Cultivar, Breeder, HypergraphCultivarMapping, HypergraphBreederMapping
from app.services.agents.seedfinder_scraper import SeedFinderScraper

# Optional: HyperGraph service
try:
    from app.services.hypergraph_service import HypergraphService
    HYPERGRAPH_AVAILABLE = True
except ImportError:
    HYPERGRAPH_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CHECKPOINT_FILE = Path(__file__).parent / "seedfinder_checkpoint.json"
LLM_COOLDOWN_SECONDS = 30  # Delay between LLM extractions to avoid overload
BREEDER_COOLDOWN_SECONDS = 2  # Delay between breeder page fetches


class SeedFinderFullIngestor:
    """Orchestrates full SeedFinder database ingestion."""
    
    def __init__(self, dry_run: bool = False):
        self.scraper = SeedFinderScraper()
        self.dry_run = dry_run
        self.hypergraph = HypergraphService() if HYPERGRAPH_AVAILABLE else None
        self.session_factory = async_session_factory
        
        # Stats
        self.stats = {
            'breeders_processed': 0,
            'breeders_created': 0,
            'strains_processed': 0,
            'strains_created': 0,
            'errors': 0,
            'start_time': datetime.now().isoformat()
        }
    
    def load_checkpoint(self) -> Dict[str, Any]:
        """Load checkpoint from file."""
        if CHECKPOINT_FILE.exists():
            with open(CHECKPOINT_FILE, 'r') as f:
                return json.load(f)
        return {'last_breeder_index': 0, 'processed_breeders': []}
    
    def save_checkpoint(self, data: Dict[str, Any]):
        """Save checkpoint to file."""
        with open(CHECKPOINT_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    async def ingest_breeder(self, db: AsyncSession, breeder_data: Dict[str, str]) -> Optional[Breeder]:
        """
        Ingest a single breeder into the database.
        
        Args:
            db: Database session
            breeder_data: Dict with 'slug', 'name', 'url'
        
        Returns:
            Breeder model instance or None
        """
        slug = breeder_data['slug']
        name = breeder_data['name']
        
        # Check if exists
        query = await db.execute(select(Breeder).where(Breeder.seedfinder_id == slug))
        breeder = query.scalar_one_or_none()
        
        if breeder:
            logger.info(f"Breeder already exists: {name}")
            return breeder
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create breeder: {name}")
            return None
        
        # Optionally fetch more details via LLM
        # For now, use basic info from URL
        breeder = Breeder(
            name=name,
            seedfinder_id=slug,
            website=breeder_data.get('url')
        )
        db.add(breeder)
        await db.commit()
        await db.refresh(breeder)
        
        self.stats['breeders_created'] += 1
        logger.info(f"Created breeder: {name} (ID: {breeder.id})")
        
        # Sync to HyperGraph
        if self.hypergraph and not self.dry_run:
            try:
                await self._sync_breeder_to_hypergraph(db, breeder)
            except Exception as e:
                logger.warning(f"HyperGraph sync failed for breeder {name}: {e}")
        
        return breeder
    
    async def _sync_breeder_to_hypergraph(self, db: AsyncSession, breeder: Breeder):
        """Sync breeder to HyperGraph knowledge graph."""
        mapping_query = await db.execute(
            select(HypergraphBreederMapping).where(HypergraphBreederMapping.breeder_id == breeder.id)
        )
        if mapping_query.scalar_one_or_none():
            return  # Already synced
        
        node_id = await self.hypergraph.create_breeder_node(
            name=breeder.name,
            website=breeder.website,
            country=breeder.country
        )
        if node_id:
            mapping = HypergraphBreederMapping(breeder_id=breeder.id, node_id=node_id)
            db.add(mapping)
            await db.commit()
            logger.debug(f"Synced breeder to HyperGraph: {breeder.name}")
    
    async def ingest_strain(self, db: AsyncSession, strain_data: Dict[str, Any], breeder_id: int) -> Optional[Cultivar]:
        """
        Ingest a single strain into the database.
        
        Args:
            db: Database session
            strain_data: Extracted strain data dict
            breeder_id: ID of the parent breeder
        
        Returns:
            Cultivar model instance or None
        """
        name = strain_data.get('name', 'Unknown')
        sf_id = strain_data.get('seedfinder_id') or strain_data.get('slug')
        
        # Check if exists
        query = await db.execute(select(Cultivar).where(Cultivar.seedfinder_id == sf_id))
        cultivar = query.scalar_one_or_none()
        
        if cultivar:
            logger.info(f"Strain already exists: {name}")
            return cultivar
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would create strain: {name}")
            return None
        
        # Create cultivar
        cultivar = Cultivar(
            name=name,
            breeder_id=breeder_id,
            seedfinder_id=sf_id,
            indica=strain_data.get('indica_pct', 0) or 0,
            sativa=strain_data.get('sativa_pct', 0) or 0,
            autoflower='auto' in name.lower() or strain_data.get('flowering_type', '').lower() == 'autoflower',
            description=strain_data.get('description', ''),
            thc_content=strain_data.get('thc_pct'),
            cbd_content=strain_data.get('cbd_pct'),
            flowering_type=strain_data.get('flowering_type'),
            lineage_json=strain_data.get('lineage'),
            image_urls=strain_data.get('images', [])
        )
        db.add(cultivar)
        await db.commit()
        await db.refresh(cultivar)
        
        self.stats['strains_created'] += 1
        logger.info(f"Created strain: {name} (ID: {cultivar.id})")
        
        # Sync to HyperGraph
        if self.hypergraph and not self.dry_run:
            try:
                await self._sync_strain_to_hypergraph(db, cultivar, strain_data)
            except Exception as e:
                logger.warning(f"HyperGraph sync failed for strain {name}: {e}")
        
        return cultivar
    
    async def _sync_strain_to_hypergraph(self, db: AsyncSession, cultivar: Cultivar, strain_data: Dict):
        """Sync strain to HyperGraph knowledge graph."""
        mapping_query = await db.execute(
            select(HypergraphCultivarMapping).where(HypergraphCultivarMapping.cultivar_id == cultivar.id)
        )
        if mapping_query.scalar_one_or_none():
            return  # Already synced
        
        node_id = await self.hypergraph.create_strain_node(
            name=cultivar.name,
            breeder_name=strain_data.get('breeder_name', 'Unknown'),
            genetics_id=cultivar.id
        )
        if node_id:
            mapping = HypergraphCultivarMapping(cultivar_id=cultivar.id, node_id=node_id)
            db.add(mapping)
            await db.commit()
            logger.debug(f"Synced strain to HyperGraph: {cultivar.name}")
    
    async def run_breeders_only(self) -> List[Dict[str, str]]:
        """Fetch and display all breeders without ingesting strains."""
        logger.info("Fetching all breeders from SeedFinder...")
        breeders = await self.scraper.get_all_breeders()
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Found {len(breeders)} breeders")
        logger.info(f"{'='*60}")
        
        for i, b in enumerate(breeders[:20]):  # Show first 20
            logger.info(f"  {i+1}. {b['name']} ({b['slug']})")
        
        if len(breeders) > 20:
            logger.info(f"  ... and {len(breeders) - 20} more")
        
        return breeders
    
    async def run_full_ingestion(self, limit: Optional[int] = None, use_llm: bool = True):
        """
        Run full database ingestion.
        
        Args:
            limit: Optional limit on number of breeders to process
            use_llm: Whether to use LLM for detailed strain extraction
        """
        checkpoint = self.load_checkpoint()
        start_index = checkpoint.get('last_breeder_index', 0)
        processed = set(checkpoint.get('processed_breeders', []))
        
        logger.info("="*60)
        logger.info("SeedFinder Full Database Ingestion")
        logger.info(f"Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        logger.info(f"LLM Extraction: {'ENABLED' if use_llm else 'DISABLED'}")
        logger.info(f"Resuming from index: {start_index}")
        logger.info("="*60)
        
        # Step 1: Get all breeders
        logger.info("\n[Phase 1] Fetching breeder list...")
        breeders = await self.scraper.get_all_breeders()
        
        if limit:
            breeders = breeders[:limit]
            logger.info(f"Limited to first {limit} breeders")
        
        # Step 2: Process each breeder
        for i, breeder_data in enumerate(breeders[start_index:], start=start_index):
            slug = breeder_data['slug']
            
            if slug in processed:
                logger.info(f"[{i+1}/{len(breeders)}] Skipping {breeder_data['name']} (already processed)")
                continue
            
            logger.info(f"\n[{i+1}/{len(breeders)}] Processing breeder: {breeder_data['name']}")
            
            try:
                # Use a fresh session for each breeder to avoid transaction contamination
                async with self.session_factory() as db:
                    try:
                        # Ingest breeder
                        breeder = await self.ingest_breeder(db, breeder_data)
                        self.stats['breeders_processed'] += 1
                        
                        if breeder:
                            # Get strain list for this breeder
                            await asyncio.sleep(BREEDER_COOLDOWN_SECONDS)
                            strains = await self.scraper.get_breeder_strains(slug)
                            
                            logger.info(f"  Found {len(strains)} strains for {breeder_data['name']}")
                            
                            # Process each strain
                            for j, strain_info in enumerate(strains):
                                self.stats['strains_processed'] += 1
                                
                                if use_llm:
                                    # Full LLM extraction
                                    logger.info(f"    [{j+1}/{len(strains)}] Extracting {strain_info['name']}...")
                                    strain_data = await self.scraper.extract_strain_from_url(strain_info['url'])
                                    await asyncio.sleep(LLM_COOLDOWN_SECONDS)
                                else:
                                    # Basic extraction from URL only
                                    strain_data = {
                                        'name': strain_info['name'],
                                        'slug': strain_info['slug'],
                                        'seedfinder_id': strain_info['slug'],
                                        'source_url': strain_info['url'],
                                        'breeder_name': breeder_data['name']
                                    }
                                
                                if strain_data:
                                    strain_data['breeder_name'] = breeder_data['name']
                                    try:
                                        await self.ingest_strain(db, strain_data, breeder.id)
                                    except Exception as strain_err:
                                        logger.warning(f"    Failed to ingest strain {strain_info['name']}: {strain_err}")
                                        await db.rollback()
                        
                        # Update checkpoint after successful processing
                        processed.add(slug)
                        self.save_checkpoint({
                            'last_breeder_index': i + 1,
                            'processed_breeders': list(processed),
                            'stats': self.stats
                        })
                        
                    except Exception as inner_e:
                        await db.rollback()
                        raise inner_e
                    
            except Exception as e:
                self.stats['errors'] += 1
                logger.error(f"Error processing breeder {breeder_data['name']}: {e}")
        
        # Summary
        logger.info("\n" + "="*60)
        logger.info("INGESTION COMPLETE")
        logger.info("="*60)
        logger.info(f"Breeders processed: {self.stats['breeders_processed']}")
        logger.info(f"Breeders created: {self.stats['breeders_created']}")
        logger.info(f"Strains processed: {self.stats['strains_processed']}")
        logger.info(f"Strains created: {self.stats['strains_created']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        await self.scraper.close()


async def main():
    parser = argparse.ArgumentParser(description="SeedFinder Database Ingestion")
    parser.add_argument('--dry-run', action='store_true', help='Preview mode without database writes')
    parser.add_argument('--breeders-only', action='store_true', help='Just fetch and display breeder list')
    parser.add_argument('--limit', type=int, help='Limit number of breeders to process')
    parser.add_argument('--no-llm', action='store_true', help='Skip LLM extraction (basic info only)')
    parser.add_argument('--reset', action='store_true', help='Reset checkpoint and start fresh')
    
    args = parser.parse_args()
    
    if args.reset and CHECKPOINT_FILE.exists():
        CHECKPOINT_FILE.unlink()
        logger.info("Checkpoint reset")
    
    ingestor = SeedFinderFullIngestor(dry_run=args.dry_run)
    
    if args.breeders_only:
        await ingestor.run_breeders_only()
    else:
        await ingestor.run_full_ingestion(
            limit=args.limit,
            use_llm=not args.no_llm
        )


if __name__ == "__main__":
    asyncio.run(main())
