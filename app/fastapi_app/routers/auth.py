from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.fastapi_app.dependencies import get_current_user, get_db
from app.models_async.auth import User
from app.fastapi_app.jwt_utils import verify_token

# Create routers
router = APIRouter()
api_router = APIRouter()

security = HTTPBearer()

@api_router.get("/me", response_model=dict)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "is_admin": current_user.is_admin,
        "roles": ["user"] + (["admin"] if current_user.is_admin else [])
    }

@api_router.get("/verify")
async def verify_token_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify token validity
    """
    payload = await verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return {"valid": True, "payload": payload}

# Legacy endpoints - Removed or Deprecated
# /login, /register, /refresh are now handled by Keycloak
