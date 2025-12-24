"""
Emerald Plant Tracker Integration Client
Provides nutrient calculation and environment tracking integration.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
from app.logger import logger


class EmeraldAPIClient:
    """Client for integrating with Emerald Plant Tracker API."""

    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Emerald API client.
        
        Args:
            base_url: Base URL for Emerald API (defaults to env var EMERALD_API_URL)
        """
        self.base_url = base_url or os.getenv("EMERALD_API_URL", "http://localhost:420")
        self.timeout = httpx.Timeout(10.0, connect=5.0)
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Optional[Dict]:
        """
        Make HTTP request to Emerald API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data or None on error
        """
        url = f"{self.base_url}{endpoint}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params
                )
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPError as e:
            logger.error(f"Emerald API request failed: {method} {url} - {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling Emerald API: {e}")
            return None

    async def get_plants(self) -> Optional[List[Dict]]:
        """
        Get all plants from Emerald.
        
        Returns:
            List of plant objects or None on error
        """
        return await self._make_request("GET", "/api/plants")

    async def get_plant(self, plant_id: int) -> Optional[Dict]:
        """
        Get plant details by ID.
        
        Args:
            plant_id: Emerald plant ID
            
        Returns:
            Plant object or None
        """
        return await self._make_request("GET", f"/api/plants/{plant_id}")

    async def get_environment_logs(self, params: Optional[Dict] = None) -> Optional[List[Dict]]:
        """
        Get environment monitoring logs.
        
        Args:
            params: Query parameters (tent_id, date range, etc.)
            
        Returns:
            List of environment logs or None
        """
        return await self._make_request("GET", "/api/environment", params=params)

    async def get_weekly_environment_averages(self) -> Optional[Dict]:
        """
        Get weekly environment averages.
        
        Returns:
            Weekly averages data or None
        """
        return await self._make_request("GET", "/api/environment/weekly")

    async def get_activity_logs(self, params: Optional[Dict] = None) -> Optional[List[Dict]]:
        """
        Get activity logs (feeding, watering, etc.).
        
        Args:
            params: Query parameters
            
        Returns:
            List of activity logs or None
        """
        return await self._make_request("GET", "/api/logs", params=params)

    async def get_plant_statistics(self, plant_id: int) -> Optional[Dict]:
        """
        Get statistics for a specific plant.
        
        Args:
            plant_id: Emerald plant ID
            
        Returns:
            Plant statistics or None
        """
        return await self._make_request("GET", f"/api/logs/stats/{plant_id}")

    async def get_tents(self) -> Optional[List[Dict]]:
        """
        Get all grow tents/spaces.
        
        Returns:
            List of tents or None
        """
        return await self._make_request("GET", "/api/tents")

    async def health_check(self) -> bool:
        """
        Check if Emerald API is reachable.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/")
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"Emerald health check failed: {e}")
            return False


# Singleton instance
_emerald_client: Optional[EmeraldAPIClient] = None


def get_emerald_client() -> EmeraldAPIClient:
    """
    Get the singleton Emerald API client instance.
    
    Returns:
        EmeraldAPIClient instance
    """
    global _emerald_client
    if _emerald_client is None:
        _emerald_client = EmeraldAPIClient()
    return _emerald_client
