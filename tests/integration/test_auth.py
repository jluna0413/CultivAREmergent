"""
Integration tests for authentication endpoints
Tests the complete auth flow including login, registration, and protected routes
"""

import pytest
import httpx
import asyncio
from typing import AsyncGenerator
import pytest_asyncio


class TestAuthIntegration:
    """Integration tests for authentication API endpoints"""
    
    @pytest.fixture
    def base_url(self) -> str:
        """Base URL for the FastAPI test server"""
        return "http://localhost:8000"
    
    @pytest_asyncio.fixture
    async def auth_client(self) -> AsyncGenerator[httpx.AsyncClient, None]:
        """HTTP client for making requests as an async fixture."""
        async with httpx.AsyncClient() as client:
            yield client
    
    @pytest.fixture
    async def test_user(self, auth_client: httpx.AsyncClient, base_url: str) -> dict:
        """Create a test user for integration testing"""
        user_data = {
            "username": "test_user_integration",
            "email": "test.integration@example.com",
            "password": "testpassword123",
            "full_name": "Test User Integration"
        }
        
        # Register user
        response = await auth_client.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data
        )
        
        assert response.status_code in [200, 201, 409]  # 409 if user already exists
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            # User exists, get existing user data
            login_response = await auth_client.post(
                f"{base_url}/api/v1/auth/login",
                data={
                    "username": "test_user_integration",
                    "password": "testpassword123"
                }
            )
            assert login_response.status_code == 200
            return login_response.json()
    
    @pytest.mark.asyncio
    async def test_user_registration_flow(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test complete user registration flow"""
        user_data = {
            "username": f"new_user_{pytest.__version__}",
            "email": f"newuser_{pytest.__version__}@example.com",
            "password": "newpassword123",
            "full_name": "New Test User"
        }
        
        # Register user
        response = await auth_client.post(
            f"{base_url}/api/v1/auth/register",
            json=user_data
        )
        
        assert response.status_code == 201
        response_data = response.json()
        assert "id" in response_data
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]
    
    @pytest.mark.asyncio
    async def test_user_login_flow(self, auth_client: httpx.AsyncClient, base_url: str, test_user: dict):
        """Test user login flow"""
        login_data = {
            "username": "test_user_integration",
            "password": "testpassword123"
        }
        
        response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data
        )
        
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert "token_type" in response_data
        assert response_data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_protected_route_access(self, auth_client: httpx.AsyncClient, base_url: str, test_user: dict):
        """Test access to protected routes with valid token"""
        # First login to get token
        login_response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data={
                "username": "test_user_integration",
                "password": "testpassword123"
            }
        )
        
        assert login_response.status_code == 200
        token_data = login_response.json()
        access_token = token_data["access_token"]
        
        # Access protected route
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # Test accessing user profile
        profile_response = await auth_client.get(
            f"{base_url}/api/v1/auth/profile",
            headers=headers
        )
        
        assert profile_response.status_code == 200
        profile_data = profile_response.json()
        assert "username" in profile_data
        assert profile_data["username"] == "test_user_integration"
    
    @pytest.mark.asyncio
    async def test_protected_route_without_token(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test that protected routes require authentication"""
        response = await auth_client.get(f"{base_url}/api/v1/auth/profile")
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_invalid_credentials(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent_user",
            "password": "wrongpassword"
        }
        
        response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_token_refresh(self, auth_client: httpx.AsyncClient, base_url: str, test_user: dict):
        """Test token refresh functionality"""
        # Login to get initial token
        login_response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data={
                "username": "test_user_integration",
                "password": "testpassword123"
            }
        )
        
        assert login_response.status_code == 200
        initial_token = login_response.json()["access_token"]
        
        # Refresh token
        headers = {"Authorization": f"Bearer {initial_token}"}
        refresh_response = await auth_client.post(
            f"{base_url}/api/v1/auth/refresh",
            headers=headers
        )
        
        assert refresh_response.status_code == 200
        refresh_data = refresh_response.json()
        assert "access_token" in refresh_data
        assert refresh_data["access_token"] != initial_token  # New token should be different
    
    @pytest.mark.asyncio
    async def test_logout(self, auth_client: httpx.AsyncClient, base_url: str, test_user: dict):
        """Test user logout"""
        # Login to get token
        login_response = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data={
                "username": "test_user_integration",
                "password": "testpassword123"
            }
        )
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {token}"}
        logout_response = await auth_client.post(
            f"{base_url}/api/v1/auth/logout",
            headers=headers
        )
        
        assert logout_response.status_code == 200
        
        # Verify token is invalidated by trying to access protected route
        profile_response = await auth_client.get(
            f"{base_url}/api/v1/auth/profile",
            headers=headers
        )
        
        assert profile_response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_concurrent_user_sessions(self, auth_client: httpx.AsyncClient, base_url: str):
        """Test that multiple sessions can exist for the same user"""
        # Login from two different "sessions"
        login_data = {
            "username": "test_user_integration",
            "password": "testpassword123"
        }
        
        response1 = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data
        )
        response2 = await auth_client.post(
            f"{base_url}/api/v1/auth/login",
            data=login_data
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        token1 = response1.json()["access_token"]
        token2 = response2.json()["access_token"]
        
        # Both tokens should work independently
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        profile1 = await auth_client.get(f"{base_url}/api/v1/auth/profile", headers=headers1)
        profile2 = await auth_client.get(f"{base_url}/api/v1/auth/profile", headers=headers2)
        
        assert profile1.status_code == 200
        assert profile2.status_code == 200
