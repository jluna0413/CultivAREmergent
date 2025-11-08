"""
Integration tests for plants endpoints
Tests CRUD operations for plant management
"""

import pytest
import httpx
import asyncio
from typing import AsyncGenerator


class TestPlantsIntegration:
    """Integration tests for plants API endpoints"""
    
    @pytest.fixture
    def base_url(self) -> str:
        """Base URL for the FastAPI test server"""
        return "http://localhost:8000"
    
    @pytest.fixture
    async def auth_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """HTTP client for making requests"""
        async with httpx.AsyncClient() as client:
            yield client
    
    @pytest.fixture
    async def authenticated_client(self, auth_client: httpx.AsyncClient, base_url: str) -> AsyncGenerator[httpx.AsyncClient, None]:
        """Authenticated HTTP client with valid token"""
        # Login to get token
        login_response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data={
                "username": "test_user_integration",
                "password": "testpassword123"
            }
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            
            # Create authenticated client
            async with httpx.AsyncClient() as client:
                client.headers.update({"Authorization": f"Bearer {token}"})
                yield client
        else:
            # If login fails, yield unathenticated client
            yield auth_client
    
    @pytest.fixture
    async def test_plant_data(self) -> dict:
        """Sample plant data for testing"""
        return {
            "name": "Test Plant Integration",
            "cultivar_id": "test-cultivar-123",
            "breeder_id": "test-breeder-456",
            "growth_stage": "vegetative",
            "pot_size": 5.0,
            "medium": "soil",
            "location": "grow_tent_1",
            "purchase_date": "2025-01-15",
            "notes": "Integration test plant"
        }
    
    @pytest.mark.asyncio
    async def test_create_plant(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test creating a new plant"""
        response = await authenticated_client.post(
            f"{base_url}/plants/",
            json=test_plant_data
        )
        
        assert response.status_code in [200, 201]
        created_plant = response.json()
        assert "id" in created_plant
        assert created_plant["name"] == test_plant_data["name"]
        assert created_plant["cultivar_id"] == test_plant_data["cultivar_id"]
        return created_plant["id"]
    
    @pytest.mark.asyncio
    async def test_get_plants_list(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test retrieving list of plants"""
        response = await authenticated_client.get(f"{base_url}/plants/")
        
        assert response.status_code == 200
        plants_data = response.json()
        assert isinstance(plants_data, list)
        
        # Check if plants have expected structure
        if plants_data:
            plant = plants_data[0]
            assert "id" in plant
            assert "name" in plant
            assert "growth_stage" in plant
    
    @pytest.mark.asyncio
    async def test_get_plant_by_id(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test retrieving a specific plant by ID"""
        # First create a plant
        plant_id = await self.test_create_plant(authenticated_client, base_url, test_plant_data)
        
        # Then retrieve it
        response = await authenticated_client.get(f"{base_url}/plants/{plant_id}")
        
        assert response.status_code == 200
        plant = response.json()
        assert plant["id"] == plant_id
        assert plant["name"] == test_plant_data["name"]
    
    @pytest.mark.asyncio
    async def test_update_plant(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test updating an existing plant"""
        # Create a plant
        plant_id = await self.test_create_plant(authenticated_client, base_url, test_plant_data)
        
        # Update the plant
        update_data = {
            "name": "Updated Test Plant",
            "growth_stage": "flowering",
            "notes": "Updated integration test plant"
        }
        
        response = await authenticated_client.put(
            f"{base_url}/plants/{plant_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        updated_plant = response.json()
        assert updated_plant["id"] == plant_id
        assert updated_plant["name"] == update_data["name"]
        assert updated_plant["growth_stage"] == update_data["growth_stage"]
    
    @pytest.mark.asyncio
    async def test_delete_plant(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test deleting a plant"""
        # Create a plant
        plant_id = await self.test_create_plant(authenticated_client, base_url, test_plant_data)
        
        # Delete the plant
        response = await authenticated_client.delete(f"{base_url}/plants/{plant_id}")
        
        assert response.status_code == 200
        
        # Verify plant is deleted
        get_response = await authenticated_client.get(f"{base_url}/plants/{plant_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_plants_by_cultivar(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test filtering plants by cultivar (backward compatible with strain_id)"""
        # Create a plant with specific cultivar
        test_plant_data["strain_id"] = "specific_cultivar_789"  # Keep backward compatibility
        plant_id = await self.test_create_plant(authenticated_client, base_url, test_plant_data)
        
        # Filter by cultivar (backward compatible parameter name)
        response = await authenticated_client.get(
            f"{base_url}/plants/?strain_id=specific_cultivar_789"
        )
        
        assert response.status_code == 200
        plants = response.json()
        
        # Verify all returned plants have the specified cultivar
        for plant in plants:
            assert plant["strain_id"] == "specific_cultivar_789"  # Keep backward compatibility
    
    @pytest.mark.asyncio
    async def test_get_plants_by_stage(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test filtering plants by growth stage"""
        # Create a plant with specific stage
        test_plant_data["growth_stage"] = "flowering"
        await self.test_create_plant(authenticated_client, base_url, test_plant_data)
        
        # Filter by growth stage
        response = await authenticated_client.get(
            f"{base_url}/plants/?growth_stage=flowering"
        )
        
        assert response.status_code == 200
        plants = response.json()
        
        # Verify all returned plants have the specified stage
        for plant in plants:
            assert plant["growth_stage"] == "flowering"
    
    @pytest.mark.asyncio
    async def test_unauthorized_access(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test that unauthorized requests are rejected"""
        # Try to access protected endpoint without authentication
        response = await auth_client.get(f"{base_url}/plants/")
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_plant_invalid_data(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test creating plant with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should be invalid
            "strain_id": "test-cultivar",  # Keep backward compatibility
            # Missing required fields
        }
        
        response = await authenticated_client.post(
            f"{base_url}/plants/",
            json=invalid_data
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_plant(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test updating a plant that doesn't exist"""
        update_data = {
            "name": "Nonexistent Plant",
            "growth_stage": "vegetative"
        }
        
        response = await authenticated_client.put(
            f"{base_url}/plants/nonexistent-id-12345",
            json=update_data
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_pagination(self, authenticated_client: httpx.AsyncClient, base_url: str, test_plant_data: dict):
        """Test pagination of plants list"""
        # Create multiple plants (if possible)
        for i in range(3):
            plant_data = test_plant_data.copy()
            plant_data["name"] = f"Test Plant {i+1}"
            await self.test_create_plant(authenticated_client, base_url, plant_data)
        
        # Test pagination
        response = await authenticated_client.get(
            f"{base_url}/plants/?limit=2&offset=0"
        )
        
        assert response.status_code == 200
        plants = response.json()
        assert len(plants) <= 2
        
        # Test offset pagination
        response_offset = await authenticated_client.get(
            f"{base_url}/plants/?limit=2&offset=2"
        )
        
        assert response_offset.status_code == 200
        plants_offset = response_offset.json()
        assert len(plants_offset) <= 2
