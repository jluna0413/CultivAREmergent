"""
Sensors Router - CRUD operations for sensor device management
Migrated from legacy Flask application
Dual-router pattern: HTML template routes + Clean JSON API contracts
"""

from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from sqlalchemy import select, func, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Optional, List
import math
from pydantic import BaseModel

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.models.sensors import (
    SensorCreate, SensorUpdate, SensorResponse, SensorListResponse,
    SensorFilters, SensorStats, SensorCreateResponse, SensorUpdateResponse, 
    SensorDeleteResponse, SensorListApiResponse, SensorReading, SensorReadingCreate,
    SensorReadingResponse, SensorReadingsListResponse, SensorStatsResponse, 
    SensorTypesResponse, SensorType, SensorSource
)
from app.fastapi_app.models.common import ApiResponse
from app.models_async.auth import User
from app.models_async.sensors import Sensor as SensorModel, SensorData
from app.models_async.grow import Zone

# HTML routes for backward compatibility - Legacy template support
router = APIRouter(tags=["sensors"])

# Clean JSON API routes under /api/v1/sensors/*
api_router = APIRouter(tags=["sensors-api"])


# ============================================================================
# Helper Functions
# ============================================================================

def create_paginated_response(items: List, total: int, page: int, page_size: int) -> dict:
    """Create standardized paginated response."""
    pages = math.ceil(total / page_size) if total > 0 else 0
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }


# ============================================================================
# HTML Pages (Legacy Support)
# ============================================================================

@router.get("/", name="sensors_list_page")
async def sensors_list_page(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display list of sensors with legacy template support."""
    try:
        # Get sensors with eager loading of zone
        result = await db.execute(
            select(SensorModel).options(selectinload(SensorModel.zone)).order_by(SensorModel.name)
        )
        sensors = result.scalars().all()
        
        # Get zones for filter dropdown
        result = await db.execute(select(Zone).order_by(Zone.name))
        zones = result.scalars().all()
        
        # Transform to match legacy template format
        sensor_data = []
        for sensor in sensors:
            sensor_data.append({
                'id': sensor.id,
                'name': sensor.name,
                'zone_id': sensor.zone_id,
                'zone_name': sensor.zone.name if sensor.zone else 'Unknown',
                'source': sensor.source,
                'device': sensor.device,
                'sensor_type': sensor.sensor_type,
                'show': sensor.show,
                'unit': sensor.unit,
                'ac_infinity_device_id': sensor.ac_infinity_device_id,
                'ecowitt_device_id': sensor.ecowitt_device_id,
                'readings_count': len(sensor.readings) if sensor.readings else 0,
                'created_at': sensor.created_at.isoformat() if sensor.created_at else None,
            })
        
        context.update({
            "sensors": sensor_data,
            "zones": [{'id': z.id, 'name': z.name} for z in zones],
            "sensor_types": [t.value for t in SensorType],
            "sensor_sources": [s.value for s in SensorSource],
            "sensor_count": len(sensor_data),
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/sensors.html",
            context
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sensors: {str(e)}")


@router.get("/{sensor_id}", name="sensor_detail_page")
async def sensor_detail_page(
    request: Request,
    sensor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display sensor detail page."""
    try:
        result = await db.execute(
            select(SensorModel).options(selectinload(SensorModel.zone)).where(SensorModel.id == sensor_id)
        )
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get zones for edit modal
        result = await db.execute(select(Zone).order_by(Zone.name))
        zones = result.scalars().all()
        
        # Get recent readings
        result = await db.execute(
            select(SensorData)
            .where(SensorData.sensor_id == sensor_id)
            .order_by(SensorData.created_at.desc())
            .limit(50)
        )
        readings = result.scalars().all()
        
        sensor_data = {
            'id': sensor.id,
            'name': sensor.name,
            'zone_id': sensor.zone_id,
            'zone_name': sensor.zone.name if sensor.zone else 'Unknown',
            'source': sensor.source,
            'device': sensor.device,
            'sensor_type': sensor.sensor_type,
            'show': sensor.show,
            'unit': sensor.unit,
            'ac_infinity_device_id': sensor.ac_infinity_device_id,
            'ecowitt_device_id': sensor.ecowitt_device_id,
            'created_at': sensor.created_at.isoformat() if sensor.created_at else None,
            'updated_at': sensor.updated_at.isoformat() if sensor.updated_at else None,
            'readings': [r.to_dict() for r in readings] if readings else []
        }
        
        context.update({
            "sensor": sensor_data,
            "zones": zones,
            "sensor_types": [t.value for t in SensorType],
            "sensor_sources": [s.value for s in SensorSource],
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/sensor.html",
            context
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sensor: {str(e)}")


@router.get("/{sensor_id}/readings", name="sensor_readings_page")
async def sensor_readings_page(
    request: Request,
    sensor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Display sensor readings page."""
    try:
        # Get sensor
        result = await db.execute(
            select(SensorModel).where(SensorModel.id == sensor_id)
        )
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get readings with pagination
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 50))
        offset = (page - 1) * page_size
        
        # Get total count
        count_result = await db.execute(
            select(func.count(SensorData.id)).where(SensorData.sensor_id == sensor_id)
        )
        total = count_result.scalar() or 0
        
        # Get readings
        result = await db.execute(
            select(SensorData)
            .where(SensorData.sensor_id == sensor_id)
            .order_by(SensorData.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        readings = result.scalars().all()
        
        context.update({
            "sensor": {
                'id': sensor.id,
                'name': sensor.name,
                'sensor_type': sensor.sensor_type,
                'unit': sensor.unit,
            },
            "readings": [r.to_dict() for r in readings] if readings else [],
            "pagination": {
                'total': total,
                'page': page,
                'page_size': page_size,
                'pages': math.ceil(total / page_size) if total > 0 else 0,
                'has_next': page < math.ceil(total / page_size),
                'has_prev': page > 1
            }
        })
        
        return request.app.state.templates.TemplateResponse(
            "views/sensor_readings.html",
            context
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading sensor readings: {str(e)}")


# ============================================================================
# Clean JSON API Contracts
# ============================================================================

@api_router.get("/list", response_model=SensorListApiResponse, name="api_sensors_list")
async def api_sensors_list(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search term"),
    zone_id: Optional[int] = Query(None, description="Filter by zone"),
    sensor_type: Optional[SensorType] = Query(None, description="Filter by sensor type"),
    source: Optional[SensorSource] = Query(None, description="Filter by source"),
    show: Optional[bool] = Query(None, description="Filter by show status"),
):
    """Get paginated list of sensors with filters - Clean JSON API."""
    try:
        # Build base query with eager loading
        query = select(SensorModel).options(selectinload(SensorModel.zone))
        
        # Apply filters
        if search:
            query = query.where(
                or_(
                    SensorModel.name.contains(search),
                    SensorModel.device.contains(search)
                )
            )
        
        if zone_id:
            query = query.where(SensorModel.zone_id == zone_id)
        
        if sensor_type:
            query = query.where(SensorModel.sensor_type == sensor_type)
        
        if source:
            query = query.where(SensorModel.source == source)
        
        if show is not None:
            query = query.where(SensorModel.show == show)
        
        # Get total count
        count_query = select(func.count(SensorModel.id))
        # Apply same filters for count
        if search:
            count_query = count_query.where(
                or_(
                    SensorModel.name.contains(search),
                    SensorModel.device.contains(search)
                )
            )
        if zone_id:
            count_query = count_query.where(SensorModel.zone_id == zone_id)
        if sensor_type:
            count_query = count_query.where(SensorModel.sensor_type == sensor_type)
        if source:
            count_query = count_query.where(SensorModel.source == source)
        if show is not None:
            count_query = count_query.where(SensorModel.show == show)
        
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # Apply pagination and ordering
        query = query.order_by(SensorModel.name).offset((page - 1) * page_size).limit(page_size)
        
        # Execute main query
        result = await db.execute(query)
        sensors = result.scalars().all()
        
        # Transform to response format
        items = []
        for sensor in sensors:
            # Get latest reading
            latest_reading_result = await db.execute(
                select(SensorData)
                .where(SensorData.sensor_id == sensor.id)
                .order_by(SensorData.created_at.desc())
                .limit(1)
            )
            latest_reading = latest_reading_result.scalar_one_or_none()
            
            items.append(SensorResponse(
                id=sensor.id,
                name=sensor.name,
                zone_id=sensor.zone_id,
                source=sensor.source,
                device=sensor.device,
                sensor_type=sensor.sensor_type,
                show=sensor.show,
                unit=sensor.unit,
                ac_infinity_device_id=sensor.ac_infinity_device_id,
                ecowitt_device_id=sensor.ecowitt_device_id,
                zone_name=sensor.zone.name if sensor.zone else None,
                readings_count=len(sensor.readings) if sensor.readings else 0,
                latest_reading=SensorReading(
                    id=latest_reading.id,
                    sensor_id=latest_reading.sensor_id,
                    sensor_name=sensor.name,
                    value=latest_reading.value,
                    unit=latest_reading.unit,
                    created_at=latest_reading.created_at
                ) if latest_reading else None,
                created_at=sensor.created_at,
                updated_at=sensor.updated_at
            ))
        
        return SensorListApiResponse(**create_paginated_response(items, total, page, page_size))
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensors: {str(e)}")


@api_router.get("/{sensor_id}", response_model=SensorResponse, name="api_sensor_get")
async def api_sensor_get(
    sensor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get sensor details - Clean JSON API."""
    try:
        result = await db.execute(
            select(SensorModel).options(selectinload(SensorModel.zone)).where(SensorModel.id == sensor_id)
        )
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get latest reading
        latest_reading_result = await db.execute(
            select(SensorData)
            .where(SensorData.sensor_id == sensor.id)
            .order_by(SensorData.created_at.desc())
            .limit(1)
        )
        latest_reading = latest_reading_result.scalar_one_or_none()
        
        return SensorResponse(
            id=sensor.id,
            name=sensor.name,
            zone_id=sensor.zone_id,
            source=sensor.source,
            device=sensor.device,
            sensor_type=sensor.sensor_type,
            show=sensor.show,
            unit=sensor.unit,
            ac_infinity_device_id=sensor.ac_infinity_device_id,
            ecowitt_device_id=sensor.ecowitt_device_id,
            zone_name=sensor.zone.name if sensor.zone else None,
            readings_count=len(sensor.readings) if sensor.readings else 0,
            latest_reading=SensorReading(
                id=latest_reading.id,
                sensor_id=latest_reading.sensor_id,
                sensor_name=sensor.name,
                value=latest_reading.value,
                unit=latest_reading.unit,
                created_at=latest_reading.created_at
            ) if latest_reading else None,
            created_at=sensor.created_at,
            updated_at=sensor.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor: {str(e)}")


@api_router.post("/", response_model=SensorCreateResponse, name="api_sensor_create")
async def api_sensor_create(
    sensor_data: SensorCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Create a new sensor - Clean JSON API."""
    try:
        # Validate zone exists if provided
        if sensor_data.zone_id:
            result = await db.execute(select(Zone).where(Zone.id == sensor_data.zone_id))
            zone = result.scalar_one_or_none()
            if not zone:
                raise HTTPException(status_code=400, detail="Invalid zone ID")
        
        # Create sensor
        sensor = SensorModel(
            name=sensor_data.name,
            zone_id=sensor_data.zone_id,
            source=sensor_data.source,
            device=sensor_data.device,
            sensor_type=sensor_data.sensor_type,
            show=sensor_data.show,
            unit=sensor_data.unit,
            ac_infinity_device_id=sensor_data.ac_infinity_device_id,
            ecowitt_device_id=sensor_data.ecowitt_device_id,
        )
        
        db.add(sensor)
        await db.commit()
        await db.refresh(sensor)
        
        return SensorCreateResponse(
            sensor_id=sensor.id,
            message="Sensor created successfully",
            status="created"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating sensor: {str(e)}")


@api_router.patch("/{sensor_id}", response_model=SensorUpdateResponse, name="api_sensor_update")
async def api_sensor_update(
    sensor_id: int,
    sensor_data: SensorUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Update an existing sensor - Clean JSON API."""
    try:
        result = await db.execute(select(SensorModel).where(SensorModel.id == sensor_id))
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Validate zone if being updated
        if sensor_data.zone_id is not None:
            if sensor_data.zone_id:
                result = await db.execute(select(Zone).where(Zone.id == sensor_data.zone_id))
                zone = result.scalar_one_or_none()
                if not zone:
                    raise HTTPException(status_code=400, detail="Invalid zone ID")
            sensor.zone_id = sensor_data.zone_id
        
        # Update other fields
        update_data = sensor_data.dict(exclude_unset=True, exclude={'zone_id'})
        for key, value in update_data.items():
            setattr(sensor, key, value)
        
        await db.commit()
        
        return SensorUpdateResponse(
            message="Sensor updated successfully",
            status="updated"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating sensor: {str(e)}")


@api_router.delete("/{sensor_id}", response_model=SensorDeleteResponse, name="api_sensor_delete")
async def api_sensor_delete(
    sensor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Delete a sensor - Clean JSON API."""
    try:
        result = await db.execute(select(SensorModel).where(SensorModel.id == sensor_id))
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        await db.delete(sensor)
        await db.commit()
        
        return SensorDeleteResponse(
            message="Sensor deleted successfully",
            status="deleted"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting sensor: {str(e)}")


@api_router.get("/{sensor_id}/readings", response_model=SensorReadingsListResponse, name="api_sensor_readings")
async def api_sensor_readings(
    sensor_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(50, ge=1, le=200, description="Items per page"),
):
    """Get sensor readings - Clean JSON API."""
    try:
        # Verify sensor exists
        result = await db.execute(select(SensorModel).where(SensorModel.id == sensor_id))
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Get total count
        count_result = await db.execute(
            select(func.count(SensorData.id)).where(SensorData.sensor_id == sensor_id)
        )
        total = count_result.scalar() or 0
        
        # Get readings
        result = await db.execute(
            select(SensorData)
            .where(SensorData.sensor_id == sensor_id)
            .order_by(SensorData.created_at.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        readings = result.scalars().all()
        
        # Transform to response format
        items = [
            SensorReading(
                id=reading.id,
                sensor_id=reading.sensor_id,
                sensor_name=sensor.name,
                value=reading.value,
                unit=reading.unit,
                created_at=reading.created_at
            )
            for reading in readings
        ]
        
        return SensorReadingsListResponse(**create_paginated_response(items, total, page, page_size))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor readings: {str(e)}")


@api_router.post("/{sensor_id}/readings", response_model=SensorReadingResponse, name="api_sensor_reading_create")
async def api_sensor_reading_create(
    sensor_id: int,
    reading_data: SensorReadingCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Create a new sensor reading - Clean JSON API."""
    try:
        # Verify sensor exists
        result = await db.execute(select(SensorModel).where(SensorModel.id == sensor_id))
        sensor = result.scalar_one_or_none()
        
        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor not found")
        
        # Create reading
        reading = SensorData(
            sensor_id=sensor_id,
            value=reading_data.value,
            unit=reading_data.unit
        )
        
        db.add(reading)
        await db.commit()
        await db.refresh(reading)
        
        return SensorReadingResponse(
            reading=SensorReading(
                id=reading.id,
                sensor_id=reading.sensor_id,
                sensor_name=sensor.name,
                value=reading.value,
                unit=reading.unit,
                created_at=reading.created_at
            ),
            message="Sensor reading recorded successfully",
            status="created"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating sensor reading: {str(e)}")


@api_router.get("/stats", response_model=SensorStatsResponse, name="api_sensor_stats")
async def api_sensor_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get sensor statistics - Clean JSON API."""
    try:
        # Total sensors
        total_result = await db.execute(select(func.count(SensorModel.id)))
        total_sensors = total_result.scalar() or 0
        
        # Active sensors (show=true)
        active_result = await db.execute(
            select(func.count(SensorModel.id)).where(SensorModel.show == True)
        )
        active_sensors = active_result.scalar() or 0
        
        # Sensors by type
        type_result = await db.execute(
            select(SensorModel.sensor_type, func.count(SensorModel.id))
            .group_by(SensorModel.sensor_type)
        )
        sensors_by_type = dict(type_result.all())
        
        # Sensors by zone
        zone_result = await db.execute(
            select(Zone.name, func.count(SensorModel.id))
            .join(SensorModel, SensorModel.zone_id == Zone.id)
            .group_by(Zone.name)
        )
        sensors_by_zone = dict(zone_result.all())
        
        # Sensors by source
        source_result = await db.execute(
            select(SensorModel.source, func.count(SensorModel.id))
            .group_by(SensorModel.source)
        )
        sensors_by_source = dict(source_result.all())
        
        # Recent readings (last 24 hours)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_result = await db.execute(
            select(func.count(SensorData.id))
            .where(SensorData.created_at >= yesterday)
        )
        recent_readings_count = recent_result.scalar() or 0
        
        return SensorStatsResponse(
            stats=SensorStats(
                total_sensors=total_sensors,
                active_sensors=active_sensors,
                sensors_by_type=sensors_by_type,
                sensors_by_zone=sensors_by_zone,
                sensors_by_source=sensors_by_source,
                recent_readings_count=recent_readings_count
            ),
            message="Sensor statistics retrieved successfully",
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor stats: {str(e)}")


@api_router.get("/types", response_model=SensorTypesResponse, name="api_sensor_types")
async def api_sensor_types(
    current_user: User = Depends(require_login),
):
    """Get available sensor types - Clean JSON API."""
    try:
        return SensorTypesResponse(
            sensor_types=list(SensorType),
            message="Sensor types retrieved successfully",
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sensor types: {str(e)}")


# Note: This router needs to be included in the main FastAPI app with both routers
# In __init__.py: app.include_router(sensors.router, tags=["Sensors Legacy"])
#                app.include_router(sensors.api_router, prefix="/api/v1", tags=["Sensors API"])