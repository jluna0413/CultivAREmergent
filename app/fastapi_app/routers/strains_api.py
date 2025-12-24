"""
Strains API Router

Public-facing JSON API endpoints for searching and browsing the strain database.
Leverages the GeneticsDataAgent for enhanced search capabilities.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.fastapi_app.dependencies import get_db
from app.services.agents.genetics_data_agent import GeneticsDataAgent
from pydantic import BaseModel


router = APIRouter(
    prefix="/api/v2/strains",
    tags=["Strains Database API"]
)


# ─── Response Models ────────────────────────────────────────────────────────

class StrainSummary(BaseModel):
    id: int
    name: str
    breeder_id: Optional[int] = None
    indica: Optional[int] = None
    sativa: Optional[int] = None
    autoflower: Optional[bool] = None
    genetics_type: Optional[str] = None
    seedfinder_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class StrainDetail(StrainSummary):
    description: Optional[str] = None
    thc_content: Optional[float] = None
    cbd_content: Optional[float] = None
    lineage_json: Optional[dict] = None
    effects: Optional[list] = None
    flavors: Optional[list] = None
    aromas: Optional[list] = None
    terpene_profile: Optional[dict] = None
    dominant_terpene: Optional[str] = None
    flowering_type: Optional[str] = None
    flowering_time_min: Optional[int] = None
    flowering_time_max: Optional[int] = None
    yield_indoor: Optional[str] = None
    url: Optional[str] = None
    image_urls: Optional[list] = None


class BreederSummary(BaseModel):
    id: int
    name: str
    country: Optional[str] = None
    website: Optional[str] = None
    seedfinder_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    results: List[StrainSummary]
    total: int
    limit: int
    offset: int


# ─── Endpoints ──────────────────────────────────────────────────────────────

@router.get("/search", response_model=SearchResponse)
async def search_strains(
    q: Optional[str] = Query(None, description="Search query for strain name/description"),
    breeder_id: Optional[int] = Query(None, description="Filter by breeder ID"),
    genetics_type: Optional[str] = Query(None, description="Filter by genetics type (Indica-Dominant, Sativa-Dominant, etc.)"),
    min_indica: Optional[int] = Query(None, ge=0, le=100, description="Minimum indica percentage"),
    max_indica: Optional[int] = Query(None, ge=0, le=100, description="Maximum indica percentage"),
    autoflower: Optional[bool] = Query(None, description="Filter by autoflower"),
    effects: Optional[str] = Query(None, description="Comma-separated effects to filter by"),
    terpenes: Optional[str] = Query(None, description="Comma-separated terpenes to filter by"),
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    db: AsyncSession = Depends(get_db)
):
    """
    Search strains with filters.
    
    Examples:
    - `/api/v2/strains/search?q=blue` - Search for strains with "blue" in name
    - `/api/v2/strains/search?autoflower=true` - Get autoflower strains
    - `/api/v2/strains/search?min_indica=70` - Get indica-dominant strains
    - `/api/v2/strains/search?effects=relaxed,euphoric` - Filter by effects
    """
    agent = GeneticsDataAgent(db)
    
    # Parse comma-separated lists
    effects_list = [e.strip() for e in effects.split(",")] if effects else None
    terpenes_list = [t.strip() for t in terpenes.split(",")] if terpenes else None
    
    try:
        results = await agent.search_strains(
            query=q,
            breeder_id=breeder_id,
            genetics_type=genetics_type,
            min_indica=min_indica,
            max_indica=max_indica,
            autoflower=autoflower,
            effects=effects_list,
            terpenes=terpenes_list,
            limit=limit,
            offset=offset
        )
        
        return SearchResponse(
            results=results,
            total=len(results),  # Note: This is limited count, not true total
            limit=limit,
            offset=offset
        )
    finally:
        await agent.close()


@router.get("/random", response_model=List[StrainSummary])
async def get_random_strains(
    limit: int = Query(5, ge=1, le=20, description="Number of random strains"),
    db: AsyncSession = Depends(get_db)
):
    """Get random strains for discovery/exploration."""
    agent = GeneticsDataAgent(db)
    try:
        return await agent.get_random_strains(limit=limit)
    finally:
        await agent.close()


@router.get("/detail/{strain_id}", response_model=StrainDetail)
async def get_strain_detail(
    strain_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information for a specific strain."""
    agent = GeneticsDataAgent(db)
    try:
        result = await agent.get_strain_detail(strain_id)
        if not result:
            raise HTTPException(status_code=404, detail="Strain not found")
        return result
    finally:
        await agent.close()


@router.get("/by-breeder/{breeder_id}", response_model=List[StrainSummary])
async def get_strains_by_breeder(
    breeder_id: int,
    limit: int = Query(50, ge=1, le=200, description="Max strains to return"),
    db: AsyncSession = Depends(get_db)
):
    """Get all strains from a specific breeder."""
    agent = GeneticsDataAgent(db)
    try:
        return await agent.get_strains_by_breeder(breeder_id, limit=limit)
    finally:
        await agent.close()


@router.get("/by-effect/{effect}", response_model=List[StrainSummary])
async def get_strains_by_effect(
    effect: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get strains with a specific effect (e.g., relaxed, euphoric, creative)."""
    agent = GeneticsDataAgent(db)
    try:
        return await agent.get_strains_by_effect(effect, limit=limit)
    finally:
        await agent.close()


@router.get("/by-terpene/{terpene}", response_model=List[StrainSummary])
async def get_strains_by_terpene(
    terpene: str,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Get strains with a dominant terpene (e.g., myrcene, limonene, caryophyllene)."""
    agent = GeneticsDataAgent(db)
    try:
        return await agent.get_strains_by_terpene(terpene, limit=limit)
    finally:
        await agent.close()


# ─── Breeders Endpoints ─────────────────────────────────────────────────────

@router.get("/breeders", response_model=List[BreederSummary])
async def list_breeders(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get list of all breeders in the database."""
    agent = GeneticsDataAgent(db)
    try:
        return await agent.get_all_breeders(limit=limit, offset=offset)
    finally:
        await agent.close()
