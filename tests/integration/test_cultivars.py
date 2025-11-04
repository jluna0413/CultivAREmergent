"""
Integration tests for cultivars endpoints
Tests CRUD operations for cultivar management
"""

import pytest
import httpx
import asyncio
from typing import AsyncGenerator


class TestCultivarsIntegration:
    """Integration tests for cultivars API endpoints"""
    
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
    async def test_breeder_data(self) -> dict:
        """Sample breeder data for testing"""
        return {
            "name": "Test Breeder Integration",
            "description": "Integration test breeder",
            "location": "Test City, TC",
            "website": "https://testbreeder.com"
        }
    
    @pytest.fixture
    async def test_cultivar_data(self) -> dict:
        """Sample cultivar data for testing"""
        return {
            "name": "Test Cultivar Integration",
            "breeder_id": "test-breeder-123",
            "genetics": "Test Parent A x Test Parent B",
            "type": "indica",
            "thc_content": 22.5,
            "cbd_content": 1.2,
            "flowering_time": 60,
            "description": "Integration test cultivar",
            "effects": ["relaxed", "euphoric", "happy"],
            "flavors": ["sweet", "earthy", "citrus"],
            "growing_difficulty": "moderate",
            "yield": "high"
        }
    
    @pytest.mark.asyncio
    async def test_create_cultivar(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test creating a new cultivar"""
        response = await authenticated_client.post(
            f"{base_url}/cultivars/",
            json=test_cultivar_data
        )
        
        assert response.status_code in [200, 201]
        created_cultivar = response.json()
        assert "id" in created_cultivar
        assert created_cultivar["name"] == test_cultivar_data["name"]
        assert created_cultivar["type"] == test_cultivar_data["type"]
        return created_cultivar["id"]
    
    @pytest.mark.asyncio
    async def test_get_cultivars_list(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test retrieving list of cultivars"""
        response = await authenticated_client.get(f"{base_url}/cultivars/")
        
        assert response.status_code == 200
        cultivars_data = response.json()
        assert isinstance(cultivars_data, list)
        
        # Check if cultivars have expected structure
        if cultivars_data:
            cultivar = cultivars_data[0]
            assert "id" in cultivar
            assert "name" in cultivar
            assert "type" in cultivar
    
    @pytest.mark.asyncio
    async def test_get_cultivar_by_id(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test retrieving a specific cultivar by ID"""
        # First create a cultivar
        cultivar_id = await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Then retrieve it
        response = await authenticated_client.get(f"{base_url}/cultivars/{cultivar_id}")
        
        assert response.status_code == 200
        cultivar = response.json()
        assert cultivar["id"] == cultivar_id
        assert cultivar["name"] == test_cultivar_data["name"]
    
    @pytest.mark.asyncio
    async def test_update_cultivar(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test updating an existing cultivar"""
        # Create a cultivar
        cultivar_id = await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Update the cultivar
        update_data = {
            "name": "Updated Test Cultivar",
            "thc_content": 25.0,
            "description": "Updated integration test cultivar"
        }
        
        response = await authenticated_client.put(
            f"{base_url}/cultivars/{cultivar_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        updated_cultivar = response.json()
        assert updated_cultivar["id"] == cultivar_id
        assert updated_cultivar["name"] == update_data["name"]
        assert updated_cultivar["thc_content"] == update_data["thc_content"]
    
    @pytest.mark.asyncio
    async def test_delete_cultivar(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test deleting a cultivar"""
        # Create a cultivar
        cultivar_id = await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Delete the cultivar
        response = await authenticated_client.delete(f"{base_url}/cultivars/{cultivar_id}")
        
        assert response.status_code == 200
        
        # Verify cultivar is deleted
        get_response = await authenticated_client.get(f"{base_url}/cultivars/{cultivar_id}")
        assert get_response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_get_cultivars_by_type(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test filtering cultivars by type"""
        # Create a cultivar with specific type
        test_cultivar_data["type"] = "sativa"
        await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Filter by type
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?type=sativa"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify all returned cultivars have the specified type
        for cultivar in cultivars:
            assert cultivar["type"] == "sativa"
    
    @pytest.mark.asyncio
    async def test_search_cultivars_by_name(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test searching cultivars by name"""
        # Create a cultivar with searchable name
        test_cultivar_data["name"] = "Unique Searchable Cultivar Name"
        await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Search by name
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?search=Unique%20Searchable"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify the cultivar is found
        found_cultivar = next(
            (s for s in cultivars if "Unique Searchable" in s["name"]),
            None
        )
        assert found_cultivar is not None
    
    @pytest.mark.asyncio
    async def test_get_cultivars_by_genetics(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test filtering cultivars by genetics"""
        # Create a cultivar with specific genetics
        test_cultivar_data["genetics"] = "Unique Parent A x Unique Parent B"
        await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Filter by genetics
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?genetics=Unique%20Parent"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify cultivars contain the genetics filter
        for cultivar in cultivars:
            assert "Unique Parent" in cultivar["genetics"]
    
    @pytest.mark.asyncio
    async def test_get_cultivars_by_effects(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test filtering cultivars by effects"""
        # Create a cultivar with specific effects
        test_cultivar_data["effects"] = ["uplifting", "creative", "focused"]
        await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Filter by effect
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?effect=uplifting"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify cultivars contain the specified effect
        for cultivar in cultivars:
            assert "uplifting" in cultivar["effects"]
    
    @pytest.mark.asyncio
    async def test_get_cultivars_by_thc_range(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test filtering cultivars by THC content range"""
        # Create a cultivar with specific THC content
        test_cultivar_data["thc_content"] = 28.0
        await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
        
        # Filter by THC range
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?thc_min=25&thc_max=30"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify all cultivars are in the THC range
        for cultivar in cultivars:
            assert 25 <= cultivar["thc_content"] <= 30
    
    @pytest.mark.asyncio
    async def test_unauthorized_access(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test that unauthorized requests are rejected"""
        # Try to access protected endpoint without authentication
        response = await auth_client.get(f"{base_url}/cultivars/")
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_create_cultivar_invalid_data(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test creating cultivar with invalid data"""
        invalid_data = {
            "name": "",  # Empty name should be invalid
            "type": "invalid_type",  # Invalid type
            "thc_content": "not_a_number",  # Invalid number
        }
        
        response = await authenticated_client.post(
            f"{base_url}/cultivars/",
            json=invalid_data
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_update_nonexistent_cultivar(self, authenticated_client: httpx.AsyncClient, base_url: str):
        """Test updating a cultivar that doesn't exist"""
        update_data = {
            "name": "Nonexistent Cultivar",
            "type": "indica"
        }
        
        response = await authenticated_client.put(
            f"{base_url}/cultivars/nonexistent-cultivar-id-12345",
            json=update_data
        )
        
        assert response.status_code == 404
    
    @pytest.mark.asyncio
    async def test_cultivar_breeder_relationship(self, authenticated_client: httpx.AsyncClient, base_url: str, test_breeder_data: dict, test_cultivar_data: dict):
        """Test cultivar-breeder relationship"""
        # First create a breeder
        breeder_response = await authenticated_client.post(
            f"{base_url}/breeders/",
            json=test_breeder_data
        )
        
        if breeder_response.status_code in [200, 201]:
            breeder = breeder_response.json()
            test_cultivar_data["breeder_id"] = breeder["id"]
            
            # Create cultivar with the breeder
            cultivar_id = await self.test_create_cultivar(authenticated_client, base_url, test_cultivar_data)
            
            # Verify relationship
            cultivar_response = await authenticated_client.get(f"{base_url}/cultivars/{cultivar_id}")
            assert cultivar_response.status_code == 200
            cultivar = cultivar_response.json()
            assert cultivar["breeder_id"] == breeder["id"]
    
    @pytest.mark.asyncio
    async def test_pagination(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test pagination of cultivars list"""
        # Create multiple cultivars (if possible)
        for i in range(3):
            cultivar_data = test_cultivar_data.copy()
            cultivar_data["name"] = f"Test Cultivar {i+1}"
            await self.test_create_cultivar(authenticated_client, base_url, cultivar_data)
        
        # Test pagination
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?limit=2&offset=0"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        assert len(cultivars) <= 2
        
        # Test offset pagination
        response_offset = await authenticated_client.get(
            f"{base_url}/cultivars/?limit=2&offset=2"
        )
        
        assert response_offset.status_code == 200
        cultivars_offset = response_offset.json()
        assert len(cultivars_offset) <= 2
    
    @pytest.mark.asyncio
    async def test_cultivar_sorting(self, authenticated_client: httpx.AsyncClient, base_url: str, test_cultivar_data: dict):
        """Test sorting cultivars by different criteria"""
        # Create cultivars with different THC contents
        thc_values = [15.0, 25.0, 20.0]
        for thc in thc_values:
            cultivar_data = test_cultivar_data.copy()
            cultivar_data["name"] = f"THC{thc} Cultivar"
            cultivar_data["thc_content"] = thc
            await self.test_create_cultivar(authenticated_client, base_url, cultivar_data)
        
        # Sort by THC content ascending
        response = await authenticated_client.get(
            f"{base_url}/cultivars/?sort_by=thc_content&sort_order=asc"
        )
        
        assert response.status_code == 200
        cultivars = response.json()
        
        # Verify sorting
        thc_contents = [s["thc_content"] for s in cultivars if "thc_content" in s]
        if len(thc_contents) > 1:
            assert thc_contents == sorted(thc_contents)
