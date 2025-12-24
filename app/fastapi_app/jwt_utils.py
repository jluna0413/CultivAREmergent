"""
JWT utility functions for FastAPI application
Validates tokens using Keycloak's JWKS endpoint.
"""

import jwt
from jwt import PyJWKClient, PyJWKClientError
from typing import Optional
from app.config.config import Config

# JWKS Client with caching
jwks_client = PyJWKClient(Config.KEYCLOAK_JWKS_URL, cache_keys=True)

async def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify JWT token using Keycloak JWKS.
    """
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        # Verify signature and expiration
        # We assume RS256 as per Keycloak default
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={
                "verify_aud": False, # Relax audience check for initial cleanup
                "verify_exp": True
            }
        )
        return payload
    except (jwt.PyJWTError, PyJWKClientError) as e:
        print(f"Token verification failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected token verification error: {e}")
        return None

# Backward compatibility wrapper
async def verify_token(token: str, token_type: str = "access") -> Optional[dict]:
    return await verify_jwt_token(token)

# Legacy password utils - kept only if strictly needed by other parts of the app during migration
# Keycloak handles auth, so these shouldn't be used for active logic
def get_password_hash(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)