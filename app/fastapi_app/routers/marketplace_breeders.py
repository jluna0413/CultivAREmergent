
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.fastapi_app.dependencies import get_db
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.models_async.breeders import MarketplaceBreeder
from app.models_async.hypergraph_mappings import HypergraphBreederMapping
from app.schemas.marketplace_breeder import MarketplaceBreederCreate, MarketplaceBreederResponse
from app.services.hypergraph_service import HypergraphService
from app.logger import logger

router = APIRouter(
    prefix="/api/v2/marketplace/breeders",
    tags=["Marketplace Breeders"]
)

hypergraph_service = HypergraphService()

@router.post("/", response_model=MarketplaceBreederResponse, status_code=status.HTTP_201_CREATED)
async def create_marketplace_breeder(
    breeder_data: MarketplaceBreederCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """
    Create a new Marketplace Breeder profile and sync to Hypergraph.
    """
    # Check if user already has a breeder profile
    existing = await db.execute(
        select(MarketplaceBreeder).where(MarketplaceBreeder.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User already has a breeder profile"
        )
        
    # 1. Create Local Record
    breeder = MarketplaceBreeder(
        user_id=current_user.id,
        **breeder_data.dict()
    )
    db.add(breeder)
    await db.commit()
    await db.refresh(breeder)
    
    # 2. Sync to Hypergraph (Task 5 Hook Implementation)
    try:
        node_id = await hypergraph_service.create_breeder_node(
            name=breeder.breeder_name,
            website=breeder.website_url,
            # Country not in model yet, default to None or extract from profile?
            # Assuming None for now as it's not in MarketplaceBreeder model
        )
        
        if node_id:
            mapping = HypergraphBreederMapping(
                breeder_id=breeder.id,
                node_id=node_id
            )
            db.add(mapping)
            await db.commit()
            logger.info(f"Synced MarketplaceBreeder {breeder.id} to Hypergraph Node {node_id}")
            
    except Exception as e:
        logger.error(f"Failed to sync breeder to hypergraph: {e}")
        
    return breeder

from app.services.commission_service import CommissionService

# ... imports ...

@router.get("/me", response_model=MarketplaceBreederResponse)
async def get_my_breeder_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """Get current user's breeder profile."""
    result = await db.execute(
        select(MarketplaceBreeder).where(MarketplaceBreeder.user_id == current_user.id)
    )
    breeder = result.scalar_one_or_none()
    
    if not breeder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breeder profile not found"
        )
        
    # Calculate Dynamic Commission Rate
    rate = CommissionService.calculate_commission_from_model(breeder)
    
    # Construct Response manually to include computed field
    response = MarketplaceBreederResponse.from_orm(breeder)
    response.active_commission_rate = rate
    
    return response
