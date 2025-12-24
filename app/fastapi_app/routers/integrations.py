"""
Integrations API Router
Provides endpoints for third-party integrations like Emerald Plant Tracker.
"""

from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from app.services.emerald_client import get_emerald_client, EmeraldAPIClient
from app.logger import logger


router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


class IntegrationStatus(BaseModel):
    """Integration service status."""
    service: str
    status: str
    healthy: bool
    base_url: Optional[str] = None


class EmeraldPlantResponse(BaseModel):
    """Emerald plant data response."""
    id: int
    name: str
    strain: Optional[str] = None
    status: Optional[str] = None
    data: Dict = Field(default_factory=dict)


class EmeraldEnvironmentResponse(BaseModel):
    """Emerald environment log response."""
    id: Optional[int] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    timestamp: Optional[str] = None
    data: Dict = Field(default_factory=dict)


@router.get("/emerald/status", response_model=IntegrationStatus)
async def get_emerald_status(
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> IntegrationStatus:
    """
    Check Emerald Plant Tracker integration status.
    
    Returns:
        Integration status with health check
    """
    healthy = await client.health_check()
    return IntegrationStatus(
        service="emerald-plant-tracker",
        status="online" if healthy else "offline",
        healthy=healthy,
        base_url=client.base_url
    )


@router.get("/emerald/plants", response_model=List[Dict])
async def get_emerald_plants(
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> List[Dict]:
    """
    Get all plants from Emerald Plant Tracker.
    
    Returns:
        List of plants from Emerald
        
    Raises:
        HTTPException: If Emerald API is unreachable
    """
    plants = await client.get_plants()
    if plants is None:
        raise HTTPException(
            status_code=503,
            detail="Emerald Plant Tracker API is unavailable"
        )
    return plants


@router.get("/emerald/plants/{plant_id}", response_model=Dict)
async def get_emerald_plant(
    plant_id: int,
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> Dict:
    """
    Get specific plant details from Emerald.
    
    Args:
        plant_id: Emerald plant ID
        
    Returns:
        Plant details
        
    Raises:
        HTTPException: If plant not found or API unavailable
    """
    plant = await client.get_plant(plant_id)
    if plant is None:
        raise HTTPException(
            status_code=404,
            detail=f"Plant {plant_id} not found in Emerald"
        )
    return plant


@router.get("/emerald/environment", response_model=List[Dict])
async def get_emerald_environment(
    tent_id: Optional[int] = Query(None, description="Filter by tent ID"),
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> List[Dict]:
    """
    Get environment logs from Emerald.
    
    Args:
        tent_id: Optional tent/zone filter
        
    Returns:
        List of environment readings
        
    Raises:
        HTTPException: If API unavailable
    """
    params = {}
    if tent_id is not None:
        params["tent_id"] = tent_id
        
    logs = await client.get_environment_logs(params=params)
    if logs is None:
        raise HTTPException(
            status_code=503,
            detail="Emerald Plant Tracker API is unavailable"
        )
    return logs


@router.get("/emerald/environment/weekly", response_model=Dict)
async def get_emerald_weekly_averages(
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> Dict:
    """
    Get weekly environment averages from Emerald.
    
    Returns:
        Weekly average environmental data
        
    Raises:
        HTTPException: If API unavailable
    """
    averages = await client.get_weekly_environment_averages()
    if averages is None:
        raise HTTPException(
            status_code=503,
            detail="Emerald Plant Tracker API is unavailable"
        )
    return averages


@router.get("/emerald/logs", response_model=List[Dict])
async def get_emerald_activity_logs(
    plant_id: Optional[int] = Query(None, description="Filter by plant ID"),
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> List[Dict]:
    """
    Get activity logs (feeding, watering) from Emerald.
    
    Args:
        plant_id: Optional plant filter
        
    Returns:
        List of activity logs
        
    Raises:
        HTTPException: If API unavailable
    """
    params = {}
    if plant_id is not None:
        params["plant_id"] = plant_id
        
    logs = await client.get_activity_logs(params=params)
    if logs is None:
        raise HTTPException(
            status_code=503,
            detail="Emerald Plant Tracker API is unavailable"
        )
    return logs


@router.get("/emerald/plants/{plant_id}/stats", response_model=Dict)
async def get_emerald_plant_stats(
    plant_id: int,
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> Dict:
    """
    Get statistics for a specific plant from Emerald.
    
    Args:
        plant_id: Emerald plant ID
        
    Returns:
        Plant statistics
        
    Raises:
        HTTPException: If not found or API unavailable
    """
    stats = await client.get_plant_statistics(plant_id)
    if stats is None:
        raise HTTPException(
            status_code=404,
            detail=f"Statistics for plant {plant_id} not found"
        )
    return stats


@router.get("/emerald/tents", response_model=List[Dict])
async def get_emerald_tents(
    client: EmeraldAPIClient = Depends(get_emerald_client)
) -> List[Dict]:
    """
    Get all grow tents/spaces from Emerald.
    
    Returns:
        List of tents
        
    Raises:
        HTTPException: If API unavailable
    """
    tents = await client.get_tents()
    if tents is None:
        raise HTTPException(
            status_code=503,
            detail="Emerald Plant Tracker API is unavailable"
        )
    return tents
