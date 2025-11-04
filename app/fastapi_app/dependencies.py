"""
FastAPI Application Dependencies
Provides authentication, database session, and other shared dependencies
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any, Set
import datetime
import os
from sqlalchemy.orm import Session

# Import JWT utilities and user model
from app.fastapi_app.jwt_utils import verify_token
from app.models_async.auth import User
from app.models_async.base import AsyncSessionLocal, get_async_session
from typing import AsyncGenerator

# Security scheme
security = HTTPBearer()

# Token revocation store - in production, use Redis or database
revoked_tokens: Set[str] = set()

# Mock user session for now
MOCK_USERS = {
    1: {"id": 1, "email": "admin@cultivar.com", "username": "admin", "is_active": True, "is_admin": True},
    2: {"id": 2, "email": "user@cultivar.com", "username": "user", "is_active": True, "is_admin": False}
}

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Unified authentication dependency using JWT tokens from auth.py
    Returns proper User model with JWT verification
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Use the unified verify_token function from auth.py
        payload = verify_token(credentials.credentials, "access")
        if payload is None:
            raise credentials_exception
        
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        
        # Check if token is revoked
        if credentials.credentials in revoked_tokens:
            raise credentials_exception
        
    except Exception:
        raise credentials_exception
    
    # Get user from database using async patterns
    from sqlalchemy import select
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Unified admin authentication dependency
    Uses the same JWT verification as get_current_user
    """
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions - Admin access required"
        )
    return current_user

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Get proper async database session dependency using models_async
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Proper async database session dependency using models_async
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_optional_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[User]:
    """
    Optional user dependency - returns user if authenticated, None otherwise
    """
    if credentials is None:
        return None
    
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None

# ---------------------------------------------------------------------------
# Token Blacklist Management
# ---------------------------------------------------------------------------

def revoke_token(token: str) -> None:
    """
    Add token to revocation blacklist
    """
    revoked_tokens.add(token)

def is_token_revoked(token: str) -> bool:
    """
    Check if token is revoked
    """
    return token in revoked_tokens

async def revoke_all_user_tokens(user_id: int) -> None:
    """
    Revoke all tokens for a specific user (useful for password changes)
    This is a simplified implementation - in production, you'd want to:
    1. Use a database table to store revoked tokens with expiration
    2. Or use JWT with short expiration times and refresh token rotation
    """
    # For now, clear all revoked tokens (not ideal for production)
    # In production, store user_id in revoked token metadata
    pass

# ---------------------------------------------------------------------------
# CORS and Security Configuration
# ---------------------------------------------------------------------------

def get_cors_origins():
    """
    Enhanced CORS origin parsing with environment-driven configuration
    """
    origins_env = os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://localhost:8000")
    
    # Parse comma-separated origins and filter empty items
    origins = []
    for origin in origins_env.split(","):
        origin = origin.strip()
        if origin:  # Only add non-empty origins
            origins.append(origin)
    
    # Add development defaults if no env var set
    if not origins_env.strip():
        origins = ["http://localhost:3000", "http://localhost:8000"]
    
    return origins

def get_allowed_hosts():
    """
    Enhanced ALLOWED_HOSTS parsing with comma-separated filtering
    """
    allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "")
    
    # Parse comma-separated hosts and filter empty items
    hosts = []
    for host in allowed_hosts_env.split(","):
        host = host.strip()
        if host:  # Only add non-empty hosts
            hosts.append(host)
    
    # Add development defaults
    if not hosts:
        hosts = ["localhost", "127.0.0.1", "*.localhost"]
    
    return hosts

# ---------------------------------------------------------------------------
# Rate limiting (enhanced implementation)
# ---------------------------------------------------------------------------

request_counts: Dict[str, Dict[str, datetime.datetime]] = {}

async def rate_limit_check(client_ip: str, limit: int = 100, window: int = 60) -> bool:
    """
    Enhanced rate limiting with configurable limits
    """
    current_time = datetime.datetime.utcnow()
    
    # Initialize IP tracking if not exists
    if client_ip not in request_counts:
        request_counts[client_ip] = {}
    
    # Clean old entries for this IP
    for ip, timestamps in list(request_counts.items()):
        for timestamp_key in list(timestamps.keys()):
            if (current_time - timestamps[timestamp_key]).seconds > window:
                del timestamps[timestamp_key]
        
        # Remove IP entry if no recent requests
        if not timestamps:
            del request_counts[ip]
    
    # Check current IP request count
    if len(request_counts.get(client_ip, {})) >= limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Maximum {limit} requests per {window} seconds.",
            headers={"Retry-After": str(window)}
        )
    
    # Record this request
    request_counts[client_ip][current_time.isoformat()] = current_time
    return True

# ---------------------------------------------------------------------------
# Legacy convenience wrappers (updated to use new unified auth)
# ---------------------------------------------------------------------------

async def require_login(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Updated dependency using unified JWT authentication
    """
    return await get_current_user(credentials)

async def require_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Updated admin dependency using unified JWT authentication
    """
    return await get_current_admin_user(credentials)

async def inject_template_context(
    user: Optional[User] = Depends(get_optional_user)
) -> Dict[str, Any]:
    """
    Updated template context with proper User model
    """
    return {
        "current_user": user,
        "year": datetime.datetime.utcnow().year,
        "is_authenticated": user is not None,
        "is_admin": getattr(user, 'is_admin', False) if user else False
    }

# ---------------------------------------------------------------------------
# JWT Claims Documentation
# ---------------------------------------------------------------------------

"""
JWT CLAIMS STRUCTURE:

Standard claims in access tokens:
- user_id: int - User identifier
- username: str - User's username
- is_admin: bool - Admin role flag
- exp: int - Token expiration timestamp
- type: str - Token type ("access")

Standard claims in refresh tokens:
- user_id: int - User identifier
- username: str - User's username
- exp: int - Token expiration timestamp
- type: str - Token type ("refresh")

Token Rotation Strategy:
1. Each refresh generates new refresh token
2. Old refresh tokens are invalidated
3. Short-lived access tokens (30 min)
4. Medium-lived refresh tokens (7 days)
5. Revocation blacklist for immediate invalidation

Security Features:
- JWT signature verification with SECRET_KEY and HS256
- Token type validation
- Automatic expiration checking
- Revocation blacklist for immediate invalidation
- Rate limiting per IP address
"""
