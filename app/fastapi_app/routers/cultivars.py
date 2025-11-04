"""
Cultivars API Router for FastAPI
Provides CRUD operations for cultivar management using real database models
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, not_
import logging

from app.fastapi_app.database import get_database as get_db
from app.fastapi_app.models.strains import (
    CultivarCreate, 
    CultivarUpdate, 
    CultivarResponse, 
    CultivarListResponse,
    CultivarFilters,
    CultivarStats
)
from app.models.base_models import Cultivar
from app.models_async.grow import Cultivar as AsyncCultivar

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=List[CultivarResponse])
async def list_cultivars(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    db: Session = Depends(get_db)
):
    """Get all cultivars with pagination"""
    try:
        cultivars = db.query(Cultivar).offset(skip).limit(limit).all()
        return [CultivarResponse.from_orm(cultivar) for cultivar in cultivars]
    except Exception as e:
        logger.error(f"Error fetching cultivars: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/list", response_model=List[CultivarResponse])
async def api_list_cultivars(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """API endpoint for backward compatibility"""
    return await list_cultivars(skip=skip, limit=limit, db=db)


@router.get("/{cultivar_id}", response_model=CultivarResponse)
async def get_cultivar(cultivar_id: int, db: Session = Depends(get_db)):
    """Get a specific cultivar by ID"""
    try:
        cultivar = db.query(Cultivar).filter(Cultivar.id == cultivar_id).first()
        if not cultivar:
            raise HTTPException(status_code=404, detail="Cultivar not found")
        return CultivarResponse.from_orm(cultivar)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching cultivar {cultivar_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/api/{cultivar_id}", response_model=CultivarResponse)
async def api_get_cultivar(cultivar_id: int, db: Session = Depends(get_db)):
    """API endpoint for backward compatibility"""
    return await get_cultivar(cultivar_id, db=db)


@router.post("/", response_model=CultivarResponse)
async def create_cultivar(cultivar_data: CultivarCreate, db: Session = Depends(get_db)):
    """Create a new cultivar"""
    try:
        # Check if cultivar name already exists
        existing = db.query(Cultivar).filter(Cultivar.name == cultivar_data.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Cultivar with this name already exists")
        
        # Create new cultivar
        db_cultivar = Cultivar(
            name=cultivar_data.name,
            breeder_id=cultivar_data.breeder_id,
            indica=cultivar_data.indica,
            sativa=cultivar_data.sativa,
            autoflower=cultivar_data.autoflower,
            cycle_time=cultivar_data.cycle_time,
            seed_count=cultivar_data.seed_count,
            url=cultivar_data.url,
            description=cultivar_data.description
        )
        
        db.add(db_cultivar)
        db.commit()
        db.refresh(db_cultivar)
        
        return CultivarResponse.from_orm(db_cultivar)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating cultivar: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{cultivar_id}", response_model=CultivarResponse)
async def update_cultivar(cultivar_id: int, update_data: CultivarUpdate, db: Session = Depends(get_db)):
    """Update an existing cultivar"""
    try:
        cultivar = db.query(Cultivar).filter(Cultivar.id == cultivar_id).first()
        if not cultivar:
            raise HTTPException(status_code=404, detail="Cultivar not found")
        
        # Update fields if provided
        update_dict = update_data.dict(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(cultivar, field, value)
        
        db.commit()
        db.refresh(cultivar)
        
        return CultivarResponse.from_orm(cultivar)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating cultivar {cultivar_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{cultivar_id}")
async def delete_cultivar(cultivar_id: int, db: Session = Depends(get_db)):
    """Delete a cultivar"""
    try:
        cultivar = db.query(Cultivar).filter(Cultivar.id == cultivar_id).first()
        if not cultivar:
            raise HTTPException(status_code=404, detail="Cultivar not found")
        
        db.delete(cultivar)
        db.commit()
        
        return {"message": "Cultivar deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting cultivar {cultivar_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/stats/summary", response_model=CultivarStats)
async def get_cultivar_stats(db: Session = Depends(get_db)):
    """Get cultivar statistics"""
    try:
        total_cultivars = db.query(Cultivar).count()
        
        # Count by type
        indica_count = db.query(Cultivar).filter(Cultivar.indica > 0.5).count()
        sativa_count = db.query(Cultivar).filter(Cultivar.sativa > 0.5).count()
        hybrid_count = total_cultivars - indica_count - sativa_count
        
        # Count autoflower
        autoflower_count = db.query(Cultivar).filter(Cultivar.autoflower == True).count()
        
        # Average cycle time
        cycle_times = db.query(Cultivar.cycle_time).filter(Cultivar.cycle_time.isnot(None)).all()
        average_cycle_time = None
        if cycle_times:
            average_cycle_time = sum(ct[0] for ct in cycle_times) / len(cycle_times)
        
        return CultivarStats(
            total_cultivars=total_cultivars,
            indica_count=indica_count,
            sativa_count=sativa_count,
            hybrid_count=hybrid_count,
            autoflower_count=autoflower_count,
            average_cycle_time=average_cycle_time
        )
    except Exception as e:
        logger.error(f"Error fetching cultivar stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search/{query}", response_model=List[CultivarResponse])
async def search_cultivars(query: str, db: Session = Depends(get_db)):
    """Search cultivars by name or description"""
    try:
        cultivars = db.query(Cultivar).filter(
            or_(
                Cultivar.name.ilike(f"%{query}%"),
                Cultivar.description.ilike(f"%{query}%")
            )
        ).all()
        
        return [CultivarResponse.from_orm(cultivar) for cultivar in cultivars]
    except Exception as e:
        logger.error(f"Error searching cultivars: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/filters/", response_model=List[CultivarResponse])
async def filter_cultivars(
    breeder_id: Optional[int] = None,
    cultivar_type: Optional[str] = None,
    autoflower: Optional[bool] = None,
    min_cycle_time: Optional[int] = None,
    max_cycle_time: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Filter cultivars by various criteria"""
    try:
        query = db.query(Cultivar)
        
        if breeder_id:
            query = query.filter(Cultivar.breeder_id == breeder_id)
        
        if cultivar_type:
            if cultivar_type.lower() == "indica":
                query = query.filter(Cultivar.indica > 0.5)
            elif cultivar_type.lower() == "sativa":
                query = query.filter(Cultivar.sativa > 0.5)
            elif cultivar_type.lower() == "hybrid":
                query = query.filter(Cultivar.indica <= 0.5, Cultivar.sativa <= 0.5)
        
        if autoflower is not None:
            query = query.filter(Cultivar.autoflower == autoflower)
        
        if min_cycle_time:
            query = query.filter(Cultivar.cycle_time >= min_cycle_time)
        
        if max_cycle_time:
            query = query.filter(Cultivar.cycle_time <= max_cycle_time)
        
        if search:
            query = query.filter(
                or_(
                    Cultivar.name.ilike(f"%{search}%"),
                    Cultivar.description.ilike(f"%{search}%")
                )
            )
        
        cultivars = query.all()
        return [CultivarResponse.from_orm(cultivar) for cultivar in cultivars]
    except Exception as e:
        logger.error(f"Error filtering cultivars: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")