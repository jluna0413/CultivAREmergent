from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.fastapi_app.dependencies import get_db, require_login
from app.models_async.auth import User
from app.schemas.checkout import CheckoutRequest, CheckoutResponse
from app.services.checkout_service import CheckoutService

router = APIRouter(prefix="/checkout", tags=["checkout"])

@router.post("/", response_model=CheckoutResponse)
async def process_checkout(
    request: CheckoutRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_login)
):
    """
    Process a checkout request for the logged-in user.
    """
    try:
        response = await CheckoutService.process_checkout(db, current_user.id, request)
        return response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during checkout: {str(e)}"
        )
