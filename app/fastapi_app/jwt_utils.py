"""
JWT utility functions for FastAPI application
Simplified for development/testing - bypasses Keycloak for now.
"""

from jose import jwt, JWTError
from typing import Optional
import os
from datetime import datetime, timedelta, timezone

from app.config.config import Config

ALGORITHMS = [Config.JWT_ALGORITHM]

def generate_jwt_token(payload: dict, expires_delta: timedelta = timedelta(minutes=15)):
    """
    Generate a JWT token.
    """
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.JWT_PRIVATE_KEY, algorithm=Config.JWT_ALGORITHM)
    return encoded_jwt

async def verify_jwt_token(token: str, token_type: str = "access") -> Optional[dict]:
    """
    Simplified JWT verification for development.
    In production, this should use Keycloak JWKS.
    """
    try:
        payload = jwt.decode(
            token,
            Config.JWT_PUBLIC_KEY,
            algorithms=ALGORITHMS,
            options={
                "verify_exp": True,
                "verify_signature": True
            }
        )
        return payload
    except JWTError as e:
        print(f"Token verification failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected token verification error: {e}")
        return None

# Backward compatibility wrapper
async def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    return await verify_jwt_token(token, token_type)

# Password utilities (Legacy - Keycloak handles this now, but keeping for safety if used elsewhere)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)