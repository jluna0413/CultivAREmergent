"""
AC Infinity Devices API Router
Provides endpoints for managing AC Infinity hardware devices.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.models.acinfinity_models import ACInfinityDevice
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.logger import logger


router = APIRouter(prefix="/api/v1/devices/acinfinity", tags=["ac-infinity"])


class ACInfinityDeviceResponse(BaseModel):
    """AC Infinity device response model."""
    id: int
    device_id: str
    name: str
    type: str
    status: str
    device_uuid: str
    connection_security_level: str
    requires_encryption: bool
    last_heartbeat: Optional[datetime] = None
    is_blocked: bool
    security_violations: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class ACInfinityDeviceListResponse(BaseModel):
    """AC Infinity devices list response."""
    devices: List[ACInfinityDeviceResponse]
    total: int
    message: str = "Devices retrieved successfully"


class ACInfinityDeviceCreate(BaseModel):
    """AC Infinity device creation model."""
    device_id: str = Field(..., description="Unique device identifier")
    name: str = Field(..., description="Device name")
    type: str = Field(..., description="Device type (e.g., 'controller', 'fan')")
    connection_security_level: str = Field(default="basic", description="Security level")


class ACInfinityDeivceCreateResponse(BaseModel):
    """AC Infinity device creation response."""
    device_id: int
    message: str = "Device created successfully"
    status: str = "success"


@router.get("/list", response_model=ACInfinityDeviceListResponse)
async def list_ac_infinity_devices(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    status: Optional[str] = Query(None, description="Filter by status"),
    is_blocked: Optional[bool] = Query(None, description="Filter by blocked status"),
):
    """
    Get list of all AC Infinity devices.
    
    Args:
        status: Optional status filter
        is_blocked: Optional blocked status filter
        
    Returns:
        List of AC Infinity devices
    """
    try:
        query = select(ACInfinityDevice)
        
        if status:
            query = query.where(ACInfinityDevice.status == status)
        if is_blocked is not None:
            query = query.where(ACInfinityDevice.is_blocked == is_blocked)
            
        query = query.order_by(ACInfinityDevice.created_at.desc())
        
        result = await db.execute(query)
        devices = result.scalars().all()
        
        devices_response = [
            ACInfinityDeviceResponse(
                id=device.id,
                device_id=device.device_id,
                name=device.name,
                type=device.type,
                status=device.status,
                device_uuid=str(device.device_uuid),
                connection_security_level=device.connection_security_level,
                requires_encryption=device.requires_encryption,
                last_heartbeat=device.last_heartbeat,
                is_blocked=device.is_blocked,
                security_violations=device.security_violations,
                created_at=device.created_at,
                updated_at=device.updated_at
            )
            for device in devices
        ]
        
        return ACInfinityDeviceListResponse(
            devices=devices_response,
            total=len(devices_response)
        )
        
    except Exception as e:
        logger.error(f"Error fetching AC Infinity devices: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching devices: {str(e)}"
        )


@router.get("/{device_id}", response_model=ACInfinityDeviceResponse)
async def get_ac_infinity_device(
    device_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """
    Get specific AC Infinity device by ID.
    
    Args:
        device_id: Device ID
        
    Returns:
        AC Infinity device details
        
    Raises:
        HTTPException: If device not found
    """
    try:
        result = await db.execute(
            select(ACInfinityDevice).where(ACInfinityDevice.id == device_id)
        )
        device = result.scalar_one_or_none()
        
        if not device:
            raise HTTPException(
                status_code=404,
                detail=f"AC Infinity device {device_id} not found"
            )
        
        return ACInfinityDeviceResponse(
            id=device.id,
            device_id=device.device_id,
            name=device.name,
            type=device.type,
            status=device.status,
            device_uuid=str(device.device_uuid),
            connection_security_level=device.connection_security_level,
            requires_encryption=device.requires_encryption,
            last_heartbeat=device.last_heartbeat,
            is_blocked=device.is_blocked,
            security_violations=device.security_violations,
            created_at=device.created_at,
            updated_at=device.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching AC Infinity device {device_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching device: {str(e)}"
        )


@router.post("/", response_model=ACInfinityDeivceCreateResponse)
async def create_ac_infinity_device(
    device_data: ACInfinityDeviceCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """
    Register a new AC Infinity device.
    
    Args:
        device_data: Device creation data
        
    Returns:
        Created device info
        
    Raises:
        HTTPException: If device_id already exists
    """
    try:
        # Check if device_id already exists
        result = await db.execute(
            select(ACInfinityDevice).where(ACInfinityDevice.device_id == device_data.device_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Device with ID {device_data.device_id} already exists"
            )
        
        # Create new device
        device = ACInfinityDevice(
            device_id=device_data.device_id,
            name=device_data.name,
            type=device_data.type,
            connection_security_level=device_data.connection_security_level,
            status="inactive"
        )
        
        db.add(device)
        await db.commit()
        await db.refresh(device)
        
        return ACInfinityDeivceCreateResponse(
            device_id=device.id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating AC Infinity device: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error creating device: {str(e)}"
        )


@router.post("/{device_id}/heartbeat")
async def update_device_heartbeat(
    device_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """
    Update device heartbeat timestamp.
    
    Args:
        device_id: Device ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If device not found
    """
    try:
        result = await db.execute(
            select(ACInfinityDevice).where(ACInfinityDevice.id == device_id)
        )
        device = result.scalar_one_or_none()
        
        if not device:
            raise HTTPException(
                status_code=404,
                detail=f"Device {device_id} not found"
            )
        
        device.update_heartbeat()
        device.status = "active"
        await db.commit()
        
        return {
            "message": "Heartbeat updated successfully",
            "last_heartbeat": device.last_heartbeat,
            "status": "success"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating heartbeat for device {device_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error updating heartbeat: {str(e)}"
        )
