
import asyncio
import jwt
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from unittest.mock import MagicMock, patch
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from app.fastapi_app.jwt_utils import verify_jwt_token

# Generate keys
print("Generating test RSA keys...")
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Create a token
print("Creating test token...")
token = jwt.encode(
    {"sub": "123", "preferred_username": "testuser", "email": "test@example.com", "exp": 9999999999},
    pem_private,
    algorithm="RS256"
)

async def test_verification():
    print("Testing JWT verification with mocked JWKS...")
    
    # Mock PyJWKClient
    with patch("app.fastapi_app.jwt_utils.jwks_client") as mock_client:
        mock_key = MagicMock()
        mock_key.key = pem_public # PyJWT expects the key object or pem bytes
        mock_client.get_signing_key_from_jwt.return_value = mock_key
        
        payload = await verify_jwt_token(token)
        
        if payload and payload["preferred_username"] == "testuser":
            print("SUCCESS: Token verified and payload matches.")
        else:
            print(f"FAILURE: Payload mismatch or None. Payload: {payload}")

if __name__ == "__main__":
    asyncio.run(test_verification())
