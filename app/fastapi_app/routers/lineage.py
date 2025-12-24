
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from app.fastapi_app.dependencies import get_db
from app.services.hypergraph_service import HypergraphService
from app.models_async import HypergraphStrainMapping, HypergraphBreederMapping, UserGenetics

router = APIRouter(
    prefix="/api/lineage",
    tags=["lineage", "hypergraph"]
)

hypergraph_service = HypergraphService() # Initialize service

@router.get("/{genetics_id}/ancestry", response_model=Dict[str, Any])
async def get_ancestry(
    genetics_id: int, 
    depth: int = 5,
    db: AsyncSession = Depends(get_db)
):
    """
    Get the ancestry tree for a specific genetics profile.
    Leverages the Hypergraph service for deep traversal.
    """
    # 1. Resolve Mapping
    mapping_query = await db.execute(
        select(HypergraphStrainMapping).where(HypergraphStrainMapping.genetics_id == genetics_id)
    )
    mapping = mapping_query.scalar_one_or_none()
    
    if not mapping:
        # Fallback logic or 404 if graph node not synced
        # Ideally, we trigger a sync here if missing, but for now 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Lineage data not initialized for this strain"
        )
    
    # 2. Query Hypergraph
    tree = await hypergraph_service.get_ancestry_tree(mapping.node_id, depth=depth)
    
    if not tree:
         raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail="Lineage service temporarily unavailable"
        )
        
    return tree

@router.get("/compliance/{breeder_id}/states", response_model=List[str])
async def get_breeder_shipping_states(
    breeder_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Returns list of US state codes where this breeder is authorized to ship.
    """
    mapping_query = await db.execute(
        select(HypergraphBreederMapping).where(HypergraphBreederMapping.breeder_id == breeder_id)
    )
    mapping = mapping_query.scalar_one_or_none()
    
    if not mapping:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Compliance profile not found for breeder"
        )
        
    states = await hypergraph_service.get_legal_states(mapping.node_id)
    return states
