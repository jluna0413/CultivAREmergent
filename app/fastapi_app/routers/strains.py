"""
Strains API Router for FastAPI (Deprecated - Use /cultivars instead)
Provides backward compatibility for strain endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
import logging

from app.fastapi_app.dependencies import get_db
from app.fastapi_app.models.strains import (
    StrainCreate, 
    StrainUpdate, 
    StrainResponse, 
    StrainListResponse,
    StrainFilters,
    StrainStats
)
from app.models.base_models import Cultivar
from app.fastapi_app.routers import cultivars

logger = logging.getLogger(__name__)
router = APIRouter()


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
@router.get("/", response_model=List[StrainResponse])
async def list_strains(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all strains (deprecated - use /cultivars instead)"""
    return await list_cultivars(skip=skip, limit=limit, db=db)


@router.get("/api/list", response_model=List[StrainResponse])
async def api_list_strains(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """API endpoint for backward compatibility"""
    return await list_strains(skip=skip, limit=limit, db=db)


@router.get("/{strain_id}", response_model=StrainResponse)
async def get_strain(strain_id: int, db: Session = Depends(get_db)):
    """Get a specific strain by ID (deprecated - use /cultivars instead)"""
    return await get_cultivar(cultivar_id=strain_id, db=db)


@router.get("/api/{strain_id}", response_model=StrainResponse)
async def api_get_strain(strain_id: int, db: Session = Depends(get_db)):
    """API endpoint for backward compatibility"""
    return await get_strain(strain_id=strain_id, db=db)


@router.post("/", response_model=StrainResponse)
async def create_strain(strain_data: StrainCreate, db: Session = Depends(get_db)):
    """Create a new strain (deprecated - use /cultivars instead)"""
    return await create_cultivar(cultivar_data=strain_data, db=db)


@router.put("/{strain_id}", response_model=StrainResponse)
async def update_strain(strain_id: int, update_data: StrainUpdate, db: Session = Depends(get_db)):
    """Update an existing strain (deprecated - use /cultivars instead)"""
    return await update_cultivar(cultivar_id=strain_id, update_data=update_data, db=db)


@router.delete("/{strain_id}")
async def delete_strain(strain_id: int, db: Session = Depends(get_db)):
    """Delete a strain (deprecated - use /cultivars instead)"""
    return await delete_cultivar(cultivar_id=strain_id, db=db)


@router.get("/stats/summary", response_model=StrainStats)
async def get_strain_stats(db: Session = Depends(get_db)):
    """Get strain statistics (deprecated - use /cultivars/stats instead)"""
    stats = await get_cultivar_stats(db=db)
    return StrainStats(
        total_cultivars=stats.total_cultivars,
        indica_count=stats.indica_count,
        sativa_count=stats.sativa_count,
        hybrid_count=stats.hybrid_count,
        autoflower_count=stats.autoflower_count,
        average_cycle_time=stats.average_cycle_time
    )


@router.get("/search/{query}", response_model=List[StrainResponse])
async def search_strains(query: str, db: Session = Depends(get_db)):
    """Search strains by name or description (deprecated - use /cultivars/search instead)"""
    return await search_cultivars(query=query, db=db)
