"""
Authentication Router - FastAPI authentication endpoints
Implements login, refresh, logout, and token validation with JWT
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from pydantic import BaseModel, EmailStr, Field

# Import JWT utilities
from app.fastapi_app.jwt_utils import (
    create_access_token_with_jti,
    create_refresh_token_with_jti,
    verify_jwt_token,
    rotate_refresh_token,
    revoke_token_jti,
    is_token_revoked_by_jti,
    generate_jti
)

# Import database and models
from app.models_async.base import get_async_session
from app.models_async.auth import User

# Import dependencies
from app.fastapi_app.dependencies import get_current_user, get_current_admin_user

# Security schemes
security = HTTPBearer()
router = APIRouter()

# Pydantic schemas for request/response
class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=80, description="Username")
    password: str = Field(..., min_length=1, description="Password")

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., description="Valid refresh token")

class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = Field(None, description="Refresh token to revoke")

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    user_type: str
    created_at: datetime

    class Config:
        from_attributes = True

# Authentication endpoints
@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_async_session)
) -> TokenResponse:
    """
    Authenticate user and return access/refresh tokens
    """
    try:
        # Find user by username or email
        result = await db.execute(
            select(User).where(
                or_(
                    User.username == login_data.username,
                    User.email == login_data.username
                )
            )
        )
        user = result.scalar_one_or_none()
        
        if not user or not user.check_password(login_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check if user needs to change password
        if user.force_password_change:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password change required"
            )
        
        # Create user data for JWT
        user_data = {
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        }
        
        # Create access and refresh tokens
        access_token = create_access_token_with_jti(user_data)
        refresh_token = create_refresh_token_with_jti(user_data)
        
        # Log successful login
        print(f"User {user.username} logged in successfully")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800  # 30 minutes in seconds
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_async_session)
) -> TokenResponse:
    """
    Refresh access token using valid refresh token
    """
    try:
        # Verify the refresh token
        payload = verify_jwt_token(refresh_data.refresh_token, "refresh")
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user data from token
        user_id = payload.get("user_id")
        username = payload.get("username")
        
        if not user_id or not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token claims"
            )
        
        # Verify user still exists and is active
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Check if password change is required
        if user.force_password_change:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password change required"
            )
        
        # Create new user data
        user_data = {
            "user_id": user.id,
            "username": user.username,
            "is_admin": user.is_admin,
        }
        
        # Rotate refresh token and get new tokens
        new_access_token, new_refresh_token = await rotate_refresh_token(
            refresh_data.refresh_token, user_data
        )
        
        print(f"Tokens refreshed for user {user.username}")
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=1800  # 30 minutes in seconds
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )

@router.post("/logout")
async def logout(
    logout_data: Optional[LogoutRequest] = Body(default=None),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Logout user and optionally revoke refresh token
    """
    try:
        # Get current user if authenticated
        user = None
        if credentials:
            try:
                user = await get_current_user(credentials, db)
            except HTTPException:
                # If token is invalid, user is already effectively logged out
                return {"message": "Logout successful"}
        
        # Revoke refresh token if provided
        if logout_data and logout_data.refresh_token:
            try:
                payload = verify_jwt_token(logout_data.refresh_token, "refresh")
                if payload:
                    jti = payload.get("jti")
                    exp_timestamp = payload.get("exp")
                    if jti and exp_timestamp:
                        expiry = datetime.utcfromtimestamp(exp_timestamp)
                        await revoke_token_jti(jti, expiry)
            except Exception as e:
                print(f"Error revoking refresh token: {e}")
        
        # Log logout if user was authenticated
        if user:
            print(f"User {user.username} logged out successfully")
        
        return {"message": "Logout successful"}
        
    except Exception as e:
        print(f"Logout error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during logout"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user information
    """
    return UserResponse.from_orm(current_user)

@router.get("/verify")
async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify if current access token is valid
    """
    try:
        payload = verify_jwt_token(credentials.credentials, "access")
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return {
            "valid": True,
            "user_id": payload.get("user_id"),
            "username": payload.get("username"),
            "is_admin": payload.get("is_admin")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed"
        )

@router.post("/change-password")
async def change_password(
    password_data: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Change user password
    """
    try:
        current_password = password_data.get("current_password")
        new_password = password_data.get("new_password")
        
        if not current_password or not new_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password and new password are required"
            )
        
        # Verify current password
        if not current_user.check_password(current_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        current_user.set_password(new_password)
        current_user.force_password_change = False
        
        await db.commit()
        
        print(f"Password changed for user {current_user.username}")
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Password change error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password change"
        )
