"""
Cultivars Legacy API Router for FastAPI (Deprecated - Use /cultivars instead)
Provides backward compatibility for cultivar endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.fastapi_app.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.fastapi_app.models.cultivars import (
    CultivarCreate, 
    CultivarUpdate, 
    CultivarResponse, 
    CultivarListResponse,
    CultivarFilters,
    CultivarStats
)
from app.models.base_models import Cultivar
from app.fastapi_app.routers import cultivars

logger = logging.getLogger(__name__)
router = APIRouter(tags=["cultivars-legacy"])


# Import router functions directly
from app.fastapi_app.routers.cultivars import (
    list_cultivars,
    get_cultivar,
    create_cultivar,
    update_cultivar,
    delete_cultivar,
    get_cultivar_stats,
    search_cultivars
)

# Backward compatibility aliases - delegate to cultivars router
@router.get("/", response_model=List[CultivarResponse])
async def list_cultivars_legacy(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get all cultivars (deprecated - use /cultivars instead)"""
    return await list_cultivars(skip=skip, limit=limit, db=db)


@router.get("/api/list", response_model=List[CultivarResponse])
async def api_list_cultivars_legacy(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """API endpoint for backward compatibility"""
    return await list_cultivars_legacy(skip=skip, limit=limit, db=db)


@router.get("/{cultivar_id}", response_model=CultivarResponse)
async def get_cultivar_legacy(cultivar_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific cultivar by ID (deprecated - use /cultivars instead)"""
    return await get_cultivar(cultivar_id=cultivar_id, db=db)


@router.get("/api/{cultivar_id}", response_model=CultivarResponse)
async def api_get_cultivar_legacy(cultivar_id: int, db: AsyncSession = Depends(get_db)):
    """API endpoint for backward compatibility"""
    return await get_cultivar_legacy(cultivar_id=cultivar_id, db=db)


@router.post("/", response_model=CultivarResponse)
async def create_cultivar_legacy(cultivar_data: CultivarCreate, db: AsyncSession = Depends(get_db)):
    """Create a new cultivar (deprecated - use /cultivars instead)"""
    return await create_cultivar(cultivar_data=cultivar_data, db=db)


@router.put("/{cultivar_id}", response_model=CultivarResponse)
async def update_cultivar_legacy(cultivar_id: int, update_data: CultivarUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing cultivar (deprecated - use /cultivars instead)"""
    return await update_cultivar(cultivar_id=cultivar_id, update_data=update_data, db=db)


@router.delete("/{cultivar_id}")
async def delete_cultivar_legacy(cultivar_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a cultivar (deprecated - use /cultivars instead)"""
    return await delete_cultivar(cultivar_id=cultivar_id, db=db)


@router.get("/stats/summary", response_model=CultivarStats)
async def get_cultivar_stats_legacy(db: AsyncSession = Depends(get_db)):
    """Get cultivar statistics (deprecated - use /cultivars/stats instead)"""
    stats = await get_cultivar_stats(db=db)
    return CultivarStats(
        total_cultivars=stats.total_cultivars,
        indica_count=stats.indica_count,
        sativa_count=stats.sativa_count,
        hybrid_count=stats.hybrid_count,
        autoflower_count=stats.autoflower_count,
        average_cycle_time=stats.average_cycle_time
    )


@router.get("/search/{query}", response_model=List[CultivarResponse])
async def search_cultivars_legacy(query: str, db: AsyncSession = Depends(get_db)):
    """Search cultivars by name or description (deprecated - use /cultivars/search instead)"""
    return await search_cultivars(query=query, db=db)

