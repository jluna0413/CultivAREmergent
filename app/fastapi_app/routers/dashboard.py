"""
Dashboard Router
Main dashboard and plant management routes.
"""

from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import func, select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.models.dashboard import (
    DashboardStats, DashboardStatsRequest, CountStats, CultivarStats,
    EnvironmentalStats, SensorStats, DataSlice, EnvironmentalSlice,
    GrowthPhaseSlice, RecentReading, RecentActivity
)
from app.models_async.auth import User
from app.models_async.grow import Plant, Cultivar
from app.models_async.activities import PlantActivity
from app.models_async.sensors import SensorData

router = APIRouter(tags=["dashboard"])


@router.get("/", name="dashboard_home")
async def dashboard_home(
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Main dashboard page with real data."""
    try:
        # Get user's plants statistics
        result = await db.execute(
            select(func.count(Plant.id)).where(Plant.user_id == current_user.id)
        )
        total_plants = result.scalar() or 0
        
        # Active plants (status_id in [1,2,3] - seedling, veg, flowering)
        active_status_ids = [1, 2, 3]
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.status_id.in_(active_status_ids)
            )
        )
        active_plants = result.scalar() or 0
        
        # Get unique cultivars for this user
        result = await db.execute(
            select(func.count(func.distinct(Plant.cultivar_id))).where(
                Plant.user_id == current_user.id,
                Plant.cultivar_id.isnot(None)
            )
        )
        user_cultivars = result.scalar() or 0
        
        # Harvested plants
        result = await db.execute(
            select(func.count(Plant.id)).where(
                Plant.user_id == current_user.id,
                Plant.harvest_date.isnot(None)
            )
        )
        harvested_plants = result.scalar() or 0
        
        # Get recent activities for this user
        result = await db.execute(
            select(PlantActivity).join(Plant).where(
                Plant.user_id == current_user.id
            ).order_by(PlantActivity.activity_date.desc()).limit(10)
        )
        recent_activities = result.scalars().all()
        
        # Get user's recent plants
        result = await db.execute(
            select(Plant).where(
                Plant.user_id == current_user.id
            ).order_by(Plant.start_dt.desc()).limit(5)
        )
        recent_plants = result.scalars().all()
        
        # Update context with real data
        context.update({
            "total_plants": total_plants,
            "active_plants": active_plants,
            "user_cultivars": user_cultivars,
            "harvested_plants": harvested_plants,
            "recent_activities": recent_activities,
            "recent_plants": recent_plants,
        })
    except Exception as e:
        # If query fails, use defaults
        print(f"Dashboard query error: {e}")
        context.update({
            "total_plants": 0,
            "active_plants": 0,
            "user_cultivars": 0,
            "harvested_plants": 0,
            "recent_activities": [],
            "recent_plants": [],
        })
    
    return request.app.state.templates.TemplateResponse(
        "views/dashboard.html",
        context
    )


@router.get("/stats", response_model=DashboardStats, name="dashboard_stats")
async def get_dashboard_stats(
    request: DashboardStatsRequest = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login)
):
    """
    Get comprehensive dashboard statistics for the current user.
    
    This endpoint provides all the data needed to populate the Flutter dashboard
    with real-time information including counts, environmental data, and charts.
    """
    try:
        # Set default request if None
        if request is None:
            request = DashboardStatsRequest()
        
        # Calculate date range for historical data
        time_cutoff = datetime.utcnow() - timedelta(hours=request.time_range_hours)
        
        # === PLANT COUNT STATISTICS ===
        
        # Total plants count
        total_plants_result = await db.execute(
            select(func.count(Plant.id)).where(Plant.user_id == current_user.id)
        )
        total_plants = total_plants_result.scalar() or 0
        
        # Count plants by different statuses
        # Assuming status_id mapping: 1=seedling, 2=vegetative, 3=flowering, 4=harvested
        seedling_count = await _get_plant_count_by_status(db, current_user.id, 1)
        vegetative_count = await _get_plant_count_by_status(db, current_user.id, 2)
        flowering_count = await _get_plant_count_by_status(db, current_user.id, 3)
        
        # Active plants (seedling + vegetative + flowering)
        active_plants = seedling_count + vegetative_count + flowering_count
        
        # Harvested plants
        harvested_plants = await _get_plant_count_by_status(db, current_user.id, 4)
        
        counts = CountStats(
            total=total_plants,
            active=active_plants,
            harvested=harvested_plants,
            seedlings=seedling_count,
            vegetative=vegetative_count,
            flowering=flowering_count
        )
        
        # === CULTIVAR STATISTICS ===
        
        # Total unique cultivars in system
        total_cultivars_result = await db.execute(
            select(func.count(func.distinct(Cultivar.id)))
        )
        total_cultivars = total_cultivars_result.scalar() or 0
        
        # User's unique cultivars
        user_cultivars_result = await db.execute(
            select(func.count(func.distinct(Plant.cultivar_id))).where(
                Plant.user_id == current_user.id,
                Plant.cultivar_id.isnot(None)
            )
        )
        user_cultivars = user_cultivars_result.scalar() or 0
        
        cultivars = CultivarStats(
            total_cultivars=total_cultivars,
            user_cultivars=user_cultivars
        )
        
        # === ENVIRONMENTAL STATISTICS ===
        
        # Get average sensor readings
        temp_readings = await _get_average_sensor_reading(db, "temperature")
        humidity_readings = await _get_average_sensor_reading(db, "humidity")
        ph_readings = await _get_average_sensor_reading(db, "ph")
        ec_readings = await _get_average_sensor_reading(db, "ec")
        
        environment = EnvironmentalStats(
            avg_temperature=temp_readings,
            avg_humidity=humidity_readings,
            avg_ph=ph_readings,
            avg_ec=ec_readings
        )
        
        # === SENSOR STATISTICS ===
        
        # Get sensor counts and last reading time
        sensor_stats = await _get_sensor_statistics(db, time_cutoff)
        
        sensors = sensor_stats
        
        # === CHART DATA SLICES ===
        
        data_slices = EnvironmentalSlice()
        
        if request.include_history:
            # Temperature trend data
            temp_trend = await _get_sensor_trend_data(db, "temperature", time_cutoff)
            data_slices.temperature_data = temp_trend
            
            # Humidity trend data
            humidity_trend = await _get_sensor_trend_data(db, "humidity", time_cutoff)
            data_slices.humidity_data = humidity_trend
            
            # pH trend data (if available)
            if ph_readings is not None:
                ph_trend = await _get_sensor_trend_data(db, "ph", time_cutoff)
                data_slices.ph_data = ph_trend
            
            # EC trend data (if available)
            if ec_readings is not None:
                ec_trend = await _get_sensor_trend_data(db, "ec", time_cutoff)
                data_slices.ec_data = ec_trend
        
        # === GROWTH PHASE DISTRIBUTION ===
        
        growth_phases = [
            GrowthPhaseSlice(phase="Seedling", count=seedling_count, percentage=(seedling_count / total_plants * 100) if total_plants > 0 else 0),
            GrowthPhaseSlice(phase="Vegetative", count=vegetative_count, percentage=(vegetative_count / total_plants * 100) if total_plants > 0 else 0),
            GrowthPhaseSlice(phase="Flowering", count=flowering_count, percentage=(flowering_count / total_plants * 100) if total_plants > 0 else 0),
            GrowthPhaseSlice(phase="Harvested", count=harvested_plants, percentage=(harvested_plants / total_plants * 100) if total_plants > 0 else 0),
        ]
        
        # === RECENT READINGS ===
        
        recent_readings = await _get_recent_sensor_readings(db, request.limit_recent_readings, time_cutoff)
        
        # === RECENT ACTIVITIES ===
        
        recent_activities = await _get_recent_activities(db, current_user.id, request.limit_recent_activities)
        
        # === CONSTRUCT FINAL RESPONSE ===
        
        dashboard_stats = DashboardStats(
            counts=counts,
            cultivars=cultivars,
            environment=environment,
            sensors=sensors,
            data_slices=data_slices,
            growth_phases=growth_phases,
            recent_readings=recent_readings,
            recent_activities=recent_activities,
            user_id=current_user.id
        )
        
        return dashboard_stats
        
    except Exception as e:
        print(f"Dashboard stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve dashboard statistics: {str(e)}")


@router.get("/plants", name="dashboard_plants")
async def plants_page(
    request: Request,
    current_user: User = Depends(require_login),
    context: dict = Depends(inject_template_context)
):
    """Plants page."""
    # TODO: Migrate from app/blueprints/dashboard.py
    return request.app.state.templates.TemplateResponse(
        "views/plants.html",
        context
    )


# === HELPER FUNCTIONS ===

async def _get_plant_count_by_status(db: AsyncSession, user_id: int, status_id: int) -> int:
    """Get count of plants with a specific status for a user."""
    result = await db.execute(
        select(func.count(Plant.id)).where(
            Plant.user_id == user_id,
            Plant.status_id == status_id
        )
    )
    return result.scalar() or 0


async def _get_average_sensor_reading(db: AsyncSession, sensor_type: str) -> Optional[float]:
    """Get average reading for a specific sensor type."""
    try:
        result = await db.execute(
            select(func.avg(SensorData.value)).where(
                SensorData.sensor_type == sensor_type,
                SensorData.timestamp >= datetime.utcnow() - timedelta(hours=24)
            )
        )
        return result.scalar()
    except Exception:
        return None


async def _get_sensor_statistics(db: AsyncSession, time_cutoff: datetime) -> SensorStats:
    """Get sensor statistics including counts and last reading time."""
    try:
        # Total sensors (unique sensor_ids)
        total_result = await db.execute(
            select(func.count(func.distinct(SensorData.sensor_id)))
        )
        total_sensors = total_result.scalar() or 0
        
        # Active sensors (with recent readings)
        active_result = await db.execute(
            select(func.count(func.distinct(SensorData.sensor_id))).where(
                SensorData.timestamp >= time_cutoff
            )
        )
        active_sensors = active_result.scalar() or 0
        
        # Last reading time
        last_result = await db.execute(
            select(func.max(SensorData.timestamp))
        )
        last_reading_time = last_result.scalar()
        
        return SensorStats(
            total_sensors=total_sensors,
            active_sensors=active_sensors,
            last_reading_time=last_reading_time
        )
    except Exception:
        return SensorStats(
            total_sensors=0,
            active_sensors=0,
            last_reading_time=None
        )


async def _get_sensor_trend_data(db: AsyncSession, sensor_type: str, time_cutoff: datetime) -> List[DataSlice]:
    """Get trend data for a specific sensor type for chart visualization."""
    try:
        result = await db.execute(
            select(
                func.date_trunc('hour', SensorData.timestamp),
                func.avg(SensorData.value)
            ).where(
                SensorData.sensor_type == sensor_type,
                SensorData.timestamp >= time_cutoff
            ).group_by(
                func.date_trunc('hour', SensorData.timestamp)
            ).order_by(
                func.date_trunc('hour', SensorData.timestamp)
            )
        )
        
        data_slices = []
        for timestamp, value in result.all():
            if timestamp and value is not None:
                data_slices.append(DataSlice(
                    timestamp=timestamp,
                    value=float(value),
                    label=None
                ))
        
        return data_slices
    except Exception:
        return []


async def _get_recent_sensor_readings(db: AsyncSession, limit: int, time_cutoff: datetime) -> List[RecentReading]:
    """Get recent sensor readings."""
    try:
        result = await db.execute(
            select(SensorData).where(
                SensorData.timestamp >= time_cutoff
            ).order_by(
                SensorData.timestamp.desc()
            ).limit(limit)
        )
        
        readings = []
        for reading in result.scalars().all():
            readings.append(RecentReading(
                timestamp=reading.timestamp,
                sensor_type=reading.sensor_type,
                value=reading.value,
                unit=_get_sensor_unit(reading.sensor_type),
                location=reading.location
            ))
        
        return readings
    except Exception:
        return []


async def _get_recent_activities(db: AsyncSession, user_id: int, limit: int) -> List[RecentActivity]:
    """Get recent activities for dashboard."""
    try:
        result = await db.execute(
            select(PlantActivity).join(Plant).where(
                Plant.user_id == user_id
            ).order_by(
                PlantActivity.activity_date.desc()
            ).limit(limit)
        )
        
        activities = []
        for activity in result.scalars().all():
            activities.append(RecentActivity(
                timestamp=activity.activity_date,
                activity_type=activity.activity_type or 'general',
                description=activity.description or '',
                plant_id=activity.plant_id,
                severity=_determine_activity_severity(activity.activity_type)
            ))
        
        return activities
    except Exception:
        return []


def _get_sensor_unit(sensor_type: str) -> str:
    """Get the unit for a sensor type."""
    unit_map = {
        'temperature': '°C',
        'humidity': '%',
        'ph': 'pH',
        'ec': 'mS/cm',
        'co2': 'ppm'
    }
    return unit_map.get(sensor_type, '')


def _determine_activity_severity(activity_type: Optional[str]) -> str:
    """Determine activity severity based on activity type."""
    if not activity_type:
        return 'info'
    
    activity_type_lower = activity_type.lower()
    
    if any(keyword in activity_type_lower for keyword in ['alert', 'warning', 'critical', 'error']):
        return 'critical'
    elif any(keyword in activity_type_lower for keyword in ['update', 'change', 'notification']):
        return 'warning'
    else:
        return 'info'
