"""
Integration tests for Clones endpoints
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

class TestClonesAPIIntegration:
    """Integration tests for Clones API endpoints"""
    
    @pytest.mark.asyncio
    async def test_clones_api_root_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test clones API root endpoint"""
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = await client.get("/api/v1/clones", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "items" in data
    
    @pytest.mark.asyncio
    async def test_clones_api_post_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test POST to clones API (create clone)"""
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {auth_token}"}
        
        # First, create a parent plant
        plant_data = {
            "name": "Parent Plant for Clone Test",
            "status_id": 1,
            "cultivar_id": 1
        }
        response = await client.post("/api/v1/plants", json=plant_data, headers=headers)
        
        if response.status_code != 201:
             # Create cultivar and status if they don't exist
            await client.post("/api/v1/cultivars", json={"name": "Test Cultivar"}, headers=headers)
            # Assuming status is seeded or created elsewhere. If not, this will fail.
            response = await client.post("/api/v1/plants", json=plant_data, headers=headers)

        assert response.status_code == 201
        parent_plant = response.json()

        # Test creating a clone with minimal data
        clone_data = {
            "name": "Test Clone",
            "parent_plant_id": parent_plant["id"],
        }
        
        response = await client.post("/api/v1/clones", json=clone_data, headers=headers)
        
        assert response.status_code == 201
        clone = response.json()
        assert clone["name"] == "Test Clone"
        assert clone["parent_plant_id"] == parent_plant["id"]
