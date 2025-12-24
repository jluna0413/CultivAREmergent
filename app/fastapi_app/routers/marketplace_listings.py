from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.fastapi_app.database import get_async_session
from app.fastapi_app.dependencies import get_current_user
from app.models_async import User
from app.schemas.marketplace import GNFTListingCreate, GNFTListingUpdate, GNFTListingResponse
from app.services.marketplace_service import MarketplaceService

router = APIRouter(prefix="/marketplace/listings", tags=["marketplace"])

@router.post("/", response_model=GNFTListingResponse, status_code=status.HTTP_201_CREATED)
async def create_listing(
    listing_data: GNFTListingCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new G-NFT Listing.
    User must be a verified breeder and own the genetics.
    """
    try:
        new_listing = await MarketplaceService.create_listing(session, user.id, listing_data)
        return new_listing
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Log error in production
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Could not create listing.")

@router.get("/", response_model=List[GNFTListingResponse])
async def get_listings(
    skip: int = 0,
    limit: int = 20,
    breeder_id: Optional[int] = Query(None, description="Filter by breeder ID"),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get active listings.
    """
    listings = await MarketplaceService.get_listings(session, skip, limit, breeder_id)
    return listings

@router.get("/{listing_id}", response_model=GNFTListingResponse)
async def get_listing(
    listing_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific listing by ID.
    """
    listing = await MarketplaceService.get_listing(session, listing_id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    return listing
