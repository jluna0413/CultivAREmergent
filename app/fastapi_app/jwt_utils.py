"""
JWT utility functions for FastAPI application
Centralized JWT token creation, validation, and management
"""

import os
import uuid
import datetime
from typing import Optional, Dict, Any
from jose import jwt, JWTError

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable must be set. This is required for JWT token security.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Enhanced token revocation store with JTI support for rotation
revoked_tokens: Dict[str, datetime.datetime] = {}  # token_jti -> expiry
rotated_refresh_tokens: Dict[str, datetime.datetime] = {}  # old_jti -> expiry

def generate_jti() -> str:
    """Generate unique JWT ID for tracking"""
    return str(uuid.uuid4())

def add_token_to_revocation(token_jti: str, expiry: datetime.datetime) -> None:
    """Add token JTI to revocation store with expiry"""
    revoked_tokens[token_jti] = expiry

def is_token_revoked_by_jti(token_jti: str) -> bool:
    """Check if token JTI is revoked"""
    if token_jti not in revoked_tokens:
        return False
    
    # Clean up expired revocations
    if datetime.datetime.utcnow() > revoked_tokens[token_jti]:
        del revoked_tokens[token_jti]
        return False
    
    return True

def add_rotated_refresh_token(old_jti: str, expiry: datetime.datetime) -> None:
    """Track rotated refresh tokens to prevent reuse"""
    rotated_refresh_tokens[old_jti] = expiry

def is_refresh_token_rotated(old_jti: str) -> bool:
    """Check if refresh token was already rotated"""
    if old_jti not in rotated_refresh_tokens:
        return False
    
    # Clean up expired entries
    if datetime.datetime.utcnow() > rotated_refresh_tokens[old_jti]:
        del rotated_refresh_tokens[old_jti]
        return False
    
    return True

def verify_jwt_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Enhanced JWT verification with JTI checking and type validation
    Returns payload with JTI validation and revocation checking
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Validate token type
        if payload.get("type") != token_type:
            return None
        
        # Validate JTI for security
        jti = payload.get("jti")
        if not jti:
            return None
        
        # Check if token is revoked
        if is_token_revoked_by_jti(jti):
            return None
        
        # For refresh tokens, check if already rotated
        if token_type == "refresh" and is_refresh_token_rotated(jti):
            return None
        
        return payload
    except JWTError:
        return None

def create_access_token_with_jti(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Create JWT access token with JTI for tracking"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add JTI for token tracking
    jti = generate_jti()
    to_encode.update({
        "exp": expire, 
        "type": "access",
        "jti": jti
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token_with_jti(data: dict) -> str:
    """Create JWT refresh token with JTI for rotation tracking"""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    # Add JTI for rotation tracking
    jti = generate_jti()
    to_encode.update({
        "exp": expire, 
        "type": "refresh",
        "jti": jti
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def rotate_refresh_token(old_refresh_token: str, user_data: dict) -> tuple[str, str]:
    """
    Rotate refresh token - invalidate old one and create new one
    Returns (new_access_token, new_refresh_token)
    """
    # Verify the old refresh token
    old_payload = verify_jwt_token(old_refresh_token, "refresh")
    if old_payload is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Mark old token as rotated
    old_jti = old_payload.get("jti")
    exp_timestamp = old_payload.get("exp")
    if old_jti is None or exp_timestamp is None:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token claims"
        )
    
    old_expiry = datetime.datetime.utcfromtimestamp(exp_timestamp)
    add_rotated_refresh_token(old_jti, old_expiry)
    
    # Create new tokens
    new_access_token = create_access_token_with_jti(user_data)
    new_refresh_token = create_refresh_token_with_jti(user_data)
    
    return new_access_token, new_refresh_token

async def revoke_token_jti(jti: str, expiry: datetime.datetime) -> None:
    """
    Add token JTI to revocation blacklist
    """
    add_token_to_revocation(jti, expiry)

# Backward compatibility functions
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """Create JWT access token (backward compatibility)"""
    return create_access_token_with_jti(data, expires_delta)

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token (backward compatibility)"""
    return create_refresh_token_with_jti(data)

def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    """Verify and decode JWT token (backward compatibility)"""
    return verify_jwt_token(token, token_type)

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)