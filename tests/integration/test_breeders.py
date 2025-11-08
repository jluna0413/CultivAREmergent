"""
Integration tests for Breeders endpoints
"""

import pytest
import httpx
from typing import AsyncGenerator
import os

@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create test client for FastAPI app"""
    base_url = os.getenv("TEST_BASE_URL", "http://127.0.0.1:8000")
    
    async with httpx.AsyncClient(base_url=base_url, timeout=30.0) as client:
        yield client

@pytest.fixture
async def auth_token(client: httpx.AsyncClient) -> str:
    """Get authentication token for testing"""
    try:
        response = await client.post("/api/v1/auth/token", json={
            "username": "testuser",
            "password": "testpassword"
        })
        
        if response.status_code == 200:
            return response.json().get("access_token", "")
        else:
            # Try to register the user first
            await client.post("/api/v1/auth/register", json={
                "username": "testuser",
                "password": "testpassword",
                "email": "testuser@example.com"
            })
            response = await client.post("/api/v1/auth/token", json={
                "username": "testuser",
                "password": "testpassword"
            })
            if response.status_code == 200:
                return response.json().get("access_token", "")
            return ""
    except Exception:
        return ""

class TestBreedersAPIIntegration:
    """Integration tests for Breeders API endpoints"""
    
    @pytest.mark.asyncio
    async def test_breeders_api_root_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test breeders API root endpoint"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/api/v1/breeders/list", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "items" in data
    
    @pytest.mark.asyncio
    async def test_breeders_api_post_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test POST to breeders API (create breeder)"""
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}
        
        breeder_data = {
            "name": "Test Breeder"
        }
        
        response = await client.post("/api/v1/breeders", json=breeder_data, headers=headers)
        
        assert response.status_code == 200
        breeder = response.json()
        assert breeder["message"] == "Breeder created successfully"
        assert "breeder_id" in breeder
