"""
Genetics Data Agent - Expert Agent for Cannabis Genetics Data Operations

This agent handles:
1. On-demand strain lookups from external sources (SeedFinder.eu)
2. Breeder verification during onboarding
3. Trust Engine integration for G-NFT verification
4. JSON import from pre-scraped datasets

Architecture (Hybrid B+C):
- Scraper module fetches data from external sources
- Data is cached as JSON artifacts for audit/review
- Importer validates and persists to PostgreSQL
"""

import asyncio
import json
import logging
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import select, or_, String
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

# Crawl4AI Imports
# Crawl4AI Scraper
from app.services.agents.seedfinder_scraper import SeedFinderScraper

from app.models_async import Breeder, Cultivar
from app.config.config import Config

# Schema for LLM Extraction


logger = logging.getLogger(__name__)





class GeneticsDataAgent:
    """
    Expert Agent for Genetics Data Operations.
    
    Integrates with:
    - Trust Engine for G-NFT verification
    - Genetics Library for search miss handling
    - Breeder onboarding for auto-verification
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.scraper = SeedFinderScraper()
        self.data_dir = Path("data/genetics")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def lookup_strain(self, strain_name: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Look up a strain, first checking local DB, then external sources.
        
        This is the primary method called by the Trust Engine.
        """
        logger.info(f"GeneticsDataAgent: Looking up strain '{strain_name}'")
        
        # 1. Check local database
        if use_cache:
            local_result = await self._check_local_db_strain(strain_name)
            if local_result:
                logger.info(f"Found strain in local DB: {strain_name}")
                return {
                    "source": "local_db",
                    "verified": True,
                    "confidence": 1.0,
                    "data": local_result,
                }
        
        # 2. Check JSON cache files
        cached_result = self._check_json_cache("strains", strain_name)
        if cached_result:
            logger.info(f"Found strain in JSON cache: {strain_name}")
            # Optionally import to DB
            await self._import_cached_strain(cached_result)
            return {
                "source": "json_cache",
                "verified": True,
                "confidence": 0.9,
                "data": cached_result,
            }
        
        # 3. Scrape from SeedFinder
        logger.info(f"Scraping SeedFinder for: {strain_name}")
        scraped_result = await self.scraper.search_strain(strain_name)
        
        if scraped_result:
            # Cache the result
            self._cache_to_json("strains", strain_name, scraped_result)
            # Optionally import to DB
            await self._import_scraped_strain(scraped_result)
            
            return {
                "source": "seedfinder.eu",
                "verified": True,
                "confidence": 0.85,
                "data": scraped_result,
            }
        
        # 4. Not found anywhere
        logger.warning(f"Strain not found in any source: {strain_name}")
        return None
    
    async def lookup_breeder(self, breeder_name: str, use_cache: bool = True) -> Optional[Dict[str, Any]]:
        """
        Look up a breeder, first checking local DB, then external sources.
        """
        logger.info(f"GeneticsDataAgent: Looking up breeder '{breeder_name}'")
        
        # 1. Check local database
        if use_cache:
            local_result = await self._check_local_db_breeder(breeder_name)
            if local_result:
                return {
                    "source": "local_db",
                    "verified": True,
                    "confidence": 1.0,
                    "data": local_result,
                }
        
        # 2. Scrape from SeedFinder
        scraped_result = await self.scraper.search_breeder(breeder_name)
        
        if scraped_result:
            self._cache_to_json("breeders", breeder_name, scraped_result)
            await self._import_scraped_breeder(scraped_result)
            
            return {
                "source": "seedfinder.eu",
                "verified": True,
                "confidence": 0.85,
                "data": scraped_result,
            }
        
        return None
    
    async def verify_for_trust_engine(self, strain_name: str, breeder_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Called by AsyncAuditOrchestrator during G-NFT verification.
        
        Returns enriched verification data for the Trust Engine.
        """
        result = {
            "strain_verified": False,
            "breeder_verified": False,
            "data_source": None,
            "confidence": 0.0,
            "lineage": {},
            "thc_content": None,
            "cbd_content": None,
        }
        
        # Verify strain
        strain_data = await self.lookup_strain(strain_name)
        if strain_data:
            result["strain_verified"] = True
            result["data_source"] = strain_data["source"]
            result["confidence"] = strain_data["confidence"]
            
            if "data" in strain_data:
                data = strain_data["data"]
                result["lineage"] = data.get("lineage", data.get("lineage_json", {}))
                result["thc_content"] = data.get("thc_pct", data.get("thc_content"))
                result["cbd_content"] = data.get("cbd_pct", data.get("cbd_content"))
        
        # Verify breeder if provided
        if breeder_name:
            breeder_data = await self.lookup_breeder(breeder_name)
            if breeder_data:
                result["breeder_verified"] = True
                result["breeder_data"] = breeder_data.get("data", {})
        
        return result
    
    # ─── Enhanced Bulk Search Methods ───────────────────────────────────────
    
    async def search_strains(
        self,
        query: Optional[str] = None,
        breeder_id: Optional[int] = None,
        genetics_type: Optional[str] = None,
        min_indica: Optional[int] = None,
        max_indica: Optional[int] = None,
        autoflower: Optional[bool] = None,
        effects: Optional[List[str]] = None,
        terpenes: Optional[List[str]] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search strains with filters.
        
        Args:
            query: Text search on name/description
            breeder_id: Filter by breeder
            genetics_type: Filter by genetics type (Indica-Dominant, etc.)
            min_indica/max_indica: Filter by indica percentage
            autoflower: Filter by autoflower
            effects: Filter by effects (e.g., ["relaxed", "euphoric"])
            terpenes: Filter by dominant terpenes (e.g., ["myrcene"])
            limit: Max results
            offset: Pagination offset
        
        Returns:
            List of strain dicts
        """
        from sqlalchemy import or_, func
        
        stmt = select(Cultivar)
        
        # Text search
        if query:
            stmt = stmt.where(
                or_(
                    Cultivar.name.ilike(f"%{query}%"),
                    Cultivar.description.ilike(f"%{query}%")
                )
            )
        
        # Breeder filter
        if breeder_id:
            stmt = stmt.where(Cultivar.breeder_id == breeder_id)
        
        # Genetics type
        if genetics_type:
            stmt = stmt.where(Cultivar.genetics_type.ilike(f"%{genetics_type}%"))
        
        # Indica range
        if min_indica is not None:
            stmt = stmt.where(Cultivar.indica >= min_indica)
        if max_indica is not None:
            stmt = stmt.where(Cultivar.indica <= max_indica)
        
        # Autoflower
        if autoflower is not None:
            stmt = stmt.where(Cultivar.autoflower == autoflower)
        
        # Effects filter (JSON contains)
        if effects:
            for effect in effects:
                stmt = stmt.where(
                    func.cast(Cultivar.effects, String).ilike(f"%{effect}%")
                )
        
        # Terpene filter
        if terpenes:
            for terpene in terpenes:
                stmt = stmt.where(
                    func.cast(Cultivar.terpene_profile, String).ilike(f"%{terpene}%")
                )
        
        # Pagination
        stmt = stmt.offset(offset).limit(limit)
        
        result = await self.db.execute(stmt)
        cultivars = result.scalars().all()
        
        return [self._cultivar_to_dict(c) for c in cultivars]
    
    async def get_strains_by_breeder(self, breeder_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all strains for a specific breeder."""
        stmt = select(Cultivar).where(Cultivar.breeder_id == breeder_id).limit(limit)
        result = await self.db.execute(stmt)
        cultivars = result.scalars().all()
        return [self._cultivar_to_dict(c) for c in cultivars]
    
    async def get_strains_by_effect(self, effect: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get strains that have a specific effect."""
        from sqlalchemy import func, String
        stmt = select(Cultivar).where(
            func.cast(Cultivar.effects, String).ilike(f"%{effect}%")
        ).limit(limit)
        result = await self.db.execute(stmt)
        cultivars = result.scalars().all()
        return [self._cultivar_to_dict(c) for c in cultivars]
    
    async def get_strains_by_terpene(self, terpene: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get strains with a dominant terpene."""
        from sqlalchemy import func, String
        stmt = select(Cultivar).where(
            or_(
                Cultivar.dominant_terpene.ilike(f"%{terpene}%"),
                func.cast(Cultivar.terpene_profile, String).ilike(f"%{terpene}%")
            )
        ).limit(limit)
        result = await self.db.execute(stmt)
        cultivars = result.scalars().all()
        return [self._cultivar_to_dict(c) for c in cultivars]
    
    async def get_random_strains(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get random strains for discovery."""
        from sqlalchemy import func
        stmt = select(Cultivar).order_by(func.random()).limit(limit)
        result = await self.db.execute(stmt)
        cultivars = result.scalars().all()
        return [self._cultivar_to_dict(c) for c in cultivars]
    
    async def get_strain_detail(self, strain_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed info for a specific strain."""
        stmt = select(Cultivar).where(Cultivar.id == strain_id)
        result = await self.db.execute(stmt)
        cultivar = result.scalar_one_or_none()
        if cultivar:
            return self._cultivar_to_dict(cultivar, full=True)
        return None
    
    async def get_all_breeders(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """Get all breeders with pagination."""
        stmt = select(Breeder).offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        breeders = result.scalars().all()
        return [self._breeder_to_dict(b) for b in breeders]
    
    def _cultivar_to_dict(self, cultivar: Cultivar, full: bool = False) -> Dict[str, Any]:
        """Convert Cultivar model to dict."""
        data = {
            "id": cultivar.id,
            "name": cultivar.name,
            "breeder_id": cultivar.breeder_id,
            "indica": cultivar.indica,
            "sativa": cultivar.sativa,
            "autoflower": cultivar.autoflower,
            "genetics_type": cultivar.genetics_type,
            "seedfinder_id": cultivar.seedfinder_id,
        }
        
        if full:
            data.update({
                "description": cultivar.description,
                "thc_content": cultivar.thc_content,
                "cbd_content": cultivar.cbd_content,
                "lineage_json": cultivar.lineage_json,
                "effects": cultivar.effects,
                "flavors": cultivar.flavors,
                "aromas": cultivar.aromas,
                "terpene_profile": cultivar.terpene_profile,
                "dominant_terpene": cultivar.dominant_terpene,
                "flowering_type": cultivar.flowering_type,
                "flowering_time_min": cultivar.flowering_time_min,
                "flowering_time_max": cultivar.flowering_time_max,
                "yield_indoor": cultivar.yield_indoor,
                "url": cultivar.url,
                "image_urls": cultivar.image_urls,
            })
        
        return data
    
    def _breeder_to_dict(self, breeder: Breeder) -> Dict[str, Any]:
        """Convert Breeder model to dict."""
        return {
            "id": breeder.id,
            "name": breeder.name,
            "country": breeder.country,
            "website": breeder.website,
            "seedfinder_id": breeder.seedfinder_id,
        }
    
    async def import_from_json_file(self, filepath: str) -> Dict[str, int]:
        """
        Import breeders and strains from a JSON file.
        
        Expected format:
        {
            "breeders": [...],
            "strains": [...]
        }
        """
        logger.info(f"Importing from JSON file: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stats = {"breeders_imported": 0, "strains_imported": 0, "errors": 0}
        breeder_id_map = {}
        
        # Import breeders first
        for breeder_data in data.get("breeders", []):
            try:
                source_id = breeder_data.get("source_id", breeder_data.get("id"))
                breeder = await self._import_scraped_breeder(breeder_data)
                if breeder:
                    breeder_id_map[source_id] = breeder.id
                    stats["breeders_imported"] += 1
            except Exception as e:
                logger.error(f"Error importing breeder: {e}")
                stats["errors"] += 1
        
        # Import strains
        for strain_data in data.get("strains", []):
            try:
                breeder_source_id = strain_data.get("breeder_source_id")
                if breeder_source_id and breeder_source_id in breeder_id_map:
                    strain_data["breeder_id"] = breeder_id_map[breeder_source_id]
                
                await self._import_scraped_strain(strain_data)
                stats["strains_imported"] += 1
            except Exception as e:
                logger.error(f"Error importing strain: {e}")
                stats["errors"] += 1
        
        logger.info(f"Import complete: {stats}")
        return stats
    
    # ─── Private Helper Methods ───────────────────────────────────────────
    
    async def _check_local_db_strain(self, strain_name: str) -> Optional[Dict]:
        """Check if strain exists in local database."""
        query = select(Cultivar).where(Cultivar.name.ilike(f"%{strain_name}%"))
        result = await self.db.execute(query)
        cultivar = result.scalar_one_or_none()
        
        if cultivar:
            return {
                "id": cultivar.id,
                "name": cultivar.name,
                "thc_content": cultivar.thc_content,
                "cbd_content": cultivar.cbd_content,
                "lineage_json": cultivar.lineage_json,
                "seedfinder_id": cultivar.seedfinder_id,
            }
        return None
    
    async def _check_local_db_breeder(self, breeder_name: str) -> Optional[Dict]:
        """Check if breeder exists in local database."""
        query = select(Breeder).where(Breeder.name.ilike(f"%{breeder_name}%"))
        result = await self.db.execute(query)
        breeder = result.scalar_one_or_none()
        
        if breeder:
            return {
                "id": breeder.id,
                "name": breeder.name,
                "country": breeder.country,
                "website": breeder.website,
                "seedfinder_id": breeder.seedfinder_id,
            }
        return None
    
    def _check_json_cache(self, category: str, name: str) -> Optional[Dict]:
        """Check JSON cache files for pre-scraped data."""
        cache_dir = self.data_dir / category
        if not cache_dir.exists():
            return None
        
        # Check individual cache files
        safe_name = re.sub(r'[^\w\-]', '_', name.lower())
        cache_file = cache_dir / f"{safe_name}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        # Check bulk export files
        for export_file in cache_dir.glob("export_*.json"):
            with open(export_file, 'r') as f:
                data = json.load(f)
                items = data.get(category, data.get("items", []))
                for item in items:
                    if self.scraper._fuzzy_match(name, item.get("name", "")):
                        return item
        
        return None
    
    def _cache_to_json(self, category: str, name: str, data: Dict):
        """Cache scraped data to JSON file."""
        cache_dir = self.data_dir / category
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        safe_name = re.sub(r'[^\w\-]', '_', name.lower())
        cache_file = cache_dir / f"{safe_name}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.debug(f"Cached {category}/{safe_name} to JSON")
    
    async def _import_scraped_strain(self, data: Dict) -> Optional[Cultivar]:
        """Import a scraped strain to the database with comprehensive data."""
        name = data.get("name")
        if not name:
            return None
        
        # Resolve Breeder ID from Name if missing
        if not data.get("breeder_id") and data.get("breeder_name"):
            breeder = await self._check_local_db_breeder(data["breeder_name"])
            if breeder:
                data["breeder_id"] = breeder["id"]
        
        # Check if already exists
        existing = await self._check_local_db_strain(name)
        if existing:
            return None  # Already in DB
        
        # Build terpene fields
        terpene_profile = data.get("terpene_profile", {})
        
        cultivar = Cultivar(
            name=name,
            breeder_id=data.get("breeder_id"),
            description=data.get("description", f"Imported from {data.get('source', 'external')}"),
            short_description=data.get("short_description"),
            
            # Genetics
            indica=data.get("indica_pct") or 0,
            sativa=data.get("sativa_pct") or 0,
            ruderalis=data.get("ruderalis_pct") or 0,
            autoflower=data.get("flowering_type", "").lower() == "autoflower",
            genetics_type=data.get("genetics_type"),
            
            # Lineage
            parent_1=data.get("lineage", {}).get("parent1"),
            parent_2=data.get("lineage", {}).get("parent2"),
            lineage_json=data.get("lineage", {}),
            
            # External IDs
            seedfinder_id=data.get("source_id") or data.get("seedfinder_id"),
            
            # Cannabinoids - Primary
            thc_content=data.get("thc_pct"),
            thc_min=data.get("thc_min"),
            thc_max=data.get("thc_max"),
            cbd_content=data.get("cbd_pct"),
            cbd_min=data.get("cbd_min"),
            cbd_max=data.get("cbd_max"),
            
            # Cannabinoids - Secondary
            cbg_content=data.get("cbg_pct"),
            thcv_content=data.get("thcv_pct"),
            cbc_content=data.get("cbc_pct"),
            cbn_content=data.get("cbn_pct"),
            cannabinoid_profile=data.get("cannabinoid_profile"),
            
            # Terpenes - Individual
            myrcene=terpene_profile.get("myrcene"),
            limonene=terpene_profile.get("limonene"),
            caryophyllene=terpene_profile.get("caryophyllene"),
            linalool=terpene_profile.get("linalool"),
            pinene=terpene_profile.get("pinene"),
            humulene=terpene_profile.get("humulene"),
            terpinolene=terpene_profile.get("terpinolene"),
            ocimene=terpene_profile.get("ocimene"),
            bisabolol=terpene_profile.get("bisabolol"),
            terpene_profile=data.get("terpene_profile"),
            dominant_terpene=data.get("dominant_terpene"),
            
            # Sensory
            flavors=data.get("flavors"),
            aromas=data.get("aromas"),
            
            # Effects
            effects=data.get("effects"),
            medical_benefits=data.get("medical_benefits"),
            negative_effects=data.get("negative_effects"),
            
            # Growing Info
            flowering_type=data.get("flowering_type"),
            flowering_time_min=data.get("flowering_time_min"),
            flowering_time_max=data.get("flowering_time_max"),
            yield_indoor=data.get("yield_indoor"),
            yield_outdoor=data.get("yield_outdoor"),
            height_indoor=data.get("height_indoor"),
            grow_difficulty=data.get("grow_difficulty"),
            
            # Media
            url=data.get("source_url"),
            image_urls=data.get("image_urls", []),
            
            # Metadata
            data_source=data.get("source", "seedfinder"),
            verification_status="imported",
        )
        
        self.db.add(cultivar)
        await self.db.commit()
        await self.db.refresh(cultivar)
        
        logger.info(f"Imported strain to DB: {name} (source: {data.get('source')})")
        return cultivar
    
    async def _import_scraped_breeder(self, data: Dict) -> Optional[Breeder]:
        """Import a scraped breeder to the database."""
        name = data.get("name")
        if not name:
            return None
        
        # Check if already exists
        existing = await self._check_local_db_breeder(name)
        if existing:
            return None  # Already in DB
        
        breeder = Breeder(
            name=name,
            country=data.get("country"),
            website=data.get("website"),
            description=data.get("description"),
            seedfinder_id=data.get("source_id"),
        )
        
        self.db.add(breeder)
        await self.db.commit()
        await self.db.refresh(breeder)
        
        logger.info(f"Imported breeder to DB: {name}")
        return breeder
    
    async def _import_cached_strain(self, data: Dict) -> Optional[Cultivar]:
        """Import a cached strain to the database."""
        return await self._import_scraped_strain(data)
    
    async def close(self):
        """Clean up resources."""
        await self.scraper.close()
