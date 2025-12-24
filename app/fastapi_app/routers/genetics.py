
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.fastapi_app.dependencies import get_db
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.models_async.user_genetics import UserGenetics  
from app.models_async.hypergraph_mappings import HypergraphStrainMapping
from app.schemas.genetics import UserGeneticsCreate, UserGeneticsResponse
from app.services.hypergraph_service import HypergraphService
from app.logger import logger

router = APIRouter(
    prefix="/api/v2/genetics",
    tags=["Genetics Management"]
)

hypergraph_service = HypergraphService()

@router.post("/", response_model=UserGeneticsResponse, status_code=status.HTTP_201_CREATED)
async def create_user_genetics(
    genetics_data: UserGeneticsCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """
    Create a new UserGenetics record and sync to Hypergraph.
    """
    # 1. Create Local Record
    genetics = UserGenetics(
        user_id=current_user.id,
        **genetics_data.dict()
    )
    db.add(genetics)
    await db.commit()
    await db.refresh(genetics)
    
    # 2. Sync to Hypergraph (Task 5 Hook Implementation)
    try:
        # Determine breeder name (default to User if created by them, or fetch from cultivar)
        # For simplicity in this iteration, we use the user's name or generic
        breeder_name = current_user.email.split('@')[0] # Fallback
        
        node_id = await hypergraph_service.create_strain_node(
            name=genetics.name,
            breeder_name=breeder_name,
            genetics_id=genetics.id
        )
        
        if node_id:
            mapping = HypergraphStrainMapping(
                genetics_id=genetics.id,
                node_id=node_id
            )
            db.add(mapping)
            await db.commit()
            logger.info(f"Synced Genetics {genetics.id} to Hypergraph Node {node_id}")
            
    except Exception as e:
        logger.error(f"Failed to sync genetics to hypergraph: {e}")
        # We generally don't block the API response for this side effect, 
        # but could queue a retry task here.
        
    return genetics

@router.get("/", response_model=List[UserGeneticsResponse])
async def list_user_genetics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """List all genetics for the current user."""
    result = await db.execute(
        select(UserGenetics).where(UserGenetics.user_id == current_user.id)
    )
    return result.scalars().all()
