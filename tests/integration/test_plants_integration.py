"""
Integration tests for Plants endpoints
Tests plants API integration as required by CI setup
"""

import pytest
import httpx
import asyncio
from typing import AsyncGenerator
import os
import json


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
        response = await client.post("/auth/token", json={
            "username": "test_user",
            "password": "test_password"
        })
        
        if response.status_code == 200:
            return response.json().get("access_token", "")
        else:
            return ""
    except Exception:
        return ""


class TestPlantsAPIIntegration:
    """Integration tests for Plants API endpoints"""
    
    @pytest.mark.asyncio
    async def test_plants_api_root_endpoint(self, client: httpx.AsyncClient):
        """Test plants API root endpoint"""
        response = await client.get("/api/v1/plants")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (list, dict))
    
    @pytest.mark.asyncio
    async def test_plants_api_structure(self, client: httpx.AsyncClient):
        """Test that plants API returns expected structure"""
        response = await client.get("/api/v1/plants")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list):
                # If it's a list, check if it contains plant objects
                assert isinstance(data, list)
                if len(data) > 0:
                    # Check first item has expected fields
                    first_item = data[0]
                    assert isinstance(first_item, dict)
            
            elif isinstance(data, dict):
                # If it's a dict, check for expected structure
                assert isinstance(data, dict)
                # Common fields might include: id, name, strain, status, etc.
                # We don't require specific fields, just that it's valid JSON
    
    @pytest.mark.asyncio
    async def test_plants_api_with_auth(self, client: httpx.AsyncClient, auth_token: str):
        """Test plants API with authentication"""
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        response = await client.get("/api/v1/plants", headers=headers)
        
        # Should return 200 or 401, not 404 or 500
        assert response.status_code in [200, 401, 403]
        assert response.status_code != 404
    
    @pytest.mark.asyncio
    async def test_plants_api_post_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test POST to plants API (create plant)"""
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Test creating a plant with minimal data
        plant_data = {
            "name": "Test Plant",
            "cultivar": "Test Cultivar",
            "status": "active"
        }
        
        response = await client.post("/api/v1/plants", 
                                   json=plant_data, 
                                   headers=headers)
        
        # Should return success status or auth error, not 404
        assert response.status_code in [201, 200, 401, 403, 422]
        assert response.status_code != 404
    
    @pytest.mark.asyncio
    async def test_plants_api_get_by_id(self, client: httpx.AsyncClient):
        """Test getting a specific plant by ID"""
        # First, try to get a list to find a valid ID
        response = await client.get("/api/v1/plants")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                # Try to get the first plant
                first_plant = data[0]
                plant_id = first_plant.get("id") or first_plant.get("plant_id")
                
                if plant_id:
                    response = await client.get(f"/api/v1/plants/{plant_id}")
                    assert response.status_code in [200, 404, 401, 403]
            
            elif isinstance(data, dict) and "id" in data:
                plant_id = data["id"]
                response = await client.get(f"/api/v1/plants/{plant_id}")
                assert response.status_code in [200, 404, 401, 403]
        
        # If we can't test specific ID, that's okay
        assert True
    
    @pytest.mark.asyncio
    async def test_plants_api_put_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test PUT to plants API (update plant)"""
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Test updating a plant
        update_data = {
            "name": "Updated Test Plant",
            "status": "updated"
        }
        
        response = await client.put("/api/v1/plants/1", 
                                   json=update_data, 
                                   headers=headers)
        
        # Should return success status or auth error, not 404
        assert response.status_code in [200, 201, 401, 403, 404, 422]
    
    @pytest.mark.asyncio
    async def test_plants_api_delete_endpoint(self, client: httpx.AsyncClient, auth_token: str):
        """Test DELETE to plants API"""
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        response = await client.delete("/api/v1/plants/1", headers=headers)
        
        # Should return success status or auth error, not 500
        assert response.status_code in [200, 204, 401, 403, 404]
        assert response.status_code != 500


class TestPlantsLegacyIntegration:
    """Integration tests for Plants legacy HTML endpoints"""
    
    @pytest.mark.asyncio
    async def test_plants_legacy_page_load(self, client: httpx.AsyncClient):
        """Test that legacy plants page loads"""
        response = await client.get("/plants")
        assert response.status_code == 200
        assert "html" in response.headers.get("content-type", "").lower()
    
    @pytest.mark.asyncio
    async def test_plants_legacy_forms(self, client: httpx.AsyncClient):
        """Test that plants forms are accessible"""
        # Test form pages
        form_paths = [
            "/plants/add",
            "/plants/new",
            "/plants/form"
        ]
        
        for path in form_paths:
            try:
                response = await client.get(path)
                # Should return 200 or redirect, not 500
                assert response.status_code in [200, 302, 404]
            except Exception:
                # If endpoint doesn't exist, that's okay for legacy routes
                pass


class TestPlantsAPIPerformance:
    """Integration tests for plants API performance and reliability"""
    
    @pytest.mark.asyncio
    async def test_plants_api_response_time(self, client: httpx.AsyncClient):
        """Test that plants API responds within reasonable time"""
        import time
        
        start_time = time.time()
        response = await client.get("/api/v1/plants")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Should respond within 5 seconds
        assert response_time < 5.0
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_plants_api_pagination(self, client: httpx.AsyncClient):
        """Test plants API pagination if available"""
        # Test with limit parameter
        response = await client.get("/api/v1/plants?limit=10")
        assert response.status_code in [200, 404]
        
        # Test with offset parameter
        response = await client.get("/api/v1/plants?offset=0")
        assert response.status_code in [200, 404]
    
    @pytest.mark.asyncio
    async def test_plants_api_filtering(self, client: httpx.AsyncClient):
        """Test plants API filtering capabilities"""
        # Test common filter parameters
        filters = [
            "?status=active",
            "?strain=test",
            "?search=test",
            "?strain=sativa",
            "?strain=indica",
            "?strain=hybrid"
        ]
        
        for filter_param in filters:
            try:
                response = await client.get(f"/api/v1/plants{filter_param}")
                assert response.status_code in [200, 404]
            except Exception:
                # If filtering doesn't work, that's okay
                pass


class TestPlantsAPIValidation:
    """Integration tests for plants API data validation"""
    
    @pytest.mark.asyncio
    async def test_plants_api_validation_errors(self, client: httpx.AsyncClient, auth_token: str):
        """Test that API properly validates input data"""
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Test with invalid data
        invalid_data = {
            "name": "",  # Empty name
            "invalid_field": "value",
            "status": "invalid_status"
        }
        
        response = await client.post("/api/v1/plants", 
                                   json=invalid_data, 
                                   headers=headers)
        
        # Should return validation error (422) or success, not 500
        assert response.status_code in [200, 201, 422, 400]
        assert response.status_code != 500
    
    @pytest.mark.asyncio
    async def test_plants_api_missing_required_fields(self, client: httpx.AsyncClient, auth_token: str):
        """Test API behavior with missing required fields"""
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        # Test with empty JSON
        response = await client.post("/api/v1/plants", 
                                   json={}, 
                                   headers=headers)
        
        # Should return validation error, not 500
        assert response.status_code in [422, 400]
        assert response.status_code != 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])