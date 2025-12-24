import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.fastapi_app.database import async_session_factory
from app.models_async import Cultivar, Breeder, HypergraphCultivarMapping, HypergraphBreederMapping
from app.services.hypergraph_service import HypergraphService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SeedFinderIngestor:
    def __init__(self):
        self.hypergraph = HypergraphService()
        self.session_factory = async_session_factory

    async def ingest_breeder(self, db: AsyncSession, data: Dict[str, Any]) -> Breeder:
        """Ingests a breeder from SeedFinder data."""
        name = data.get("name")
        sf_id = data.get("id")
        
        query = await db.execute(select(Breeder).where(Breeder.seedfinder_id == sf_id))
        breeder = query.scalar_one_or_none()
        
        if not breeder:
            breeder = Breeder(
                name=name,
                seedfinder_id=sf_id,
                country=data.get("country"),
                website=data.get("website"),
                description=data.get("description")
            )
            db.add(breeder)
            await db.commit()
            await db.refresh(breeder)
            logger.info(f"Created breeder: {name}")
        
        # Sync to HyperGraph if not already synced
        mapping_query = await db.execute(
            select(HypergraphBreederMapping).where(HypergraphBreederMapping.breeder_id == breeder.id)
        )
        if not mapping_query.scalar_one_or_none():
            node_id = await self.hypergraph.create_breeder_node(
                name=name,
                website=breeder.website,
                country=breeder.country
            )
            if node_id:
                mapping = HypergraphBreederMapping(breeder_id=breeder.id, node_id=node_id)
                db.add(mapping)
                await db.commit()
                logger.info(f"Synced breeder to HyperGraph: {name}")

        return breeder

    async def ingest_cultivar(self, db: AsyncSession, data: Dict[str, Any], breeder_id: int) -> Cultivar:
        """Ingests a cultivar (strain) from SeedFinder data."""
        name = data.get("name")
        sf_id = data.get("id")
        
        query = await db.execute(select(Cultivar).where(Cultivar.seedfinder_id == sf_id))
        cultivar = query.scalar_one_or_none()
        
        if not cultivar:
            cultivar = Cultivar(
                name=name,
                breeder_id=breeder_id,
                seedfinder_id=sf_id,
                indica=data.get("indica", 0),
                sativa=data.get("sativa", 0),
                autoflower=data.get("autoflower", False),
                description=data.get("description"),
                thc_content=data.get("thc"),
                cbd_content=data.get("cbd"),
                flowering_type=data.get("flowering_type"),
                lineage_json=data.get("lineage"),
                image_urls=data.get("images", [])
            )
            db.add(cultivar)
            await db.commit()
            await db.refresh(cultivar)
            logger.info(f"Created cultivar: {name}")

        # Sync to HyperGraph
        mapping_query = await db.execute(
            select(HypergraphCultivarMapping).where(HypergraphCultivarMapping.cultivar_id == cultivar.id)
        )
        if not mapping_query.scalar_one_or_none():
            node_id = await self.hypergraph.create_strain_node(
                name=name,
                breeder_name=data.get("breeder_name", "Unknown"),
                genetics_id=cultivar.id # Using SQL ID as external ID mapping
            )
            if node_id:
                mapping = HypergraphCultivarMapping(cultivar_id=cultivar.id, node_id=node_id)
                db.add(mapping)
                await db.commit()
                logger.info(f"Synced cultivar to HyperGraph: {name}")

        return cultivar

    async def run_ingestion(self, breeder_data: List[Dict[str, Any]], strain_data: List[Dict[str, Any]]):
        """Main ingestion loop."""
        async with self.session_factory() as db:
            # 1. Ingest Breeders
            breeder_map = {}
            for b_data in breeder_data:
                breeder = await self.ingest_breeder(db, b_data)
                breeder_map[b_data["id"]] = breeder.id
            
            # 2. Ingest Strains
            for s_data in strain_data:
                sf_breeder_id = s_data.get("breeder_sf_id")
                if sf_breeder_id in breeder_map:
                    await self.ingest_cultivar(db, s_data, breeder_map[sf_breeder_id])
                else:
                    logger.warning(f"Skipping strain {s_data.get('name')} - Breeder {sf_breeder_id} not found")

async def main():
    # Example mock data for demonstration
    # In a real scenario, this would load from a JSON file or API results
    mock_breeders = [
        {"id": "sf_b_001", "name": "Barney's Farm", "country": "NL", "website": "https://barneysfarm.com", "description": "Legendary breeder from Amsterdam"}
    ]
    mock_strains = [
        {
            "id": "sf_s_001", 
            "name": "Blueberry Zkittlez", 
            "breeder_sf_id": "sf_b_001", 
            "breeder_name": "Barney's Farm",
            "indica": 60, 
            "sativa": 40,
            "thc": 22.5,
            "lineage": {"parent1": "Blueberry", "parent2": "Zkittlez"},
            "images": ["https://images.seedfinder.eu/blueberry_zkittlez_1.jpg"]
        }
    ]
    
    ingestor = SeedFinderIngestor()
    await ingestor.run_ingestion(mock_breeders, mock_strains)

if __name__ == "__main__":
    asyncio.run(main())
