"""
Diagnostic handlers for the CultivAR application - ASYNC VERSION.
Comprehensive diagnostic and health monitoring functionality.
"""

import os
import platform
import sys
import psutil
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from sqlalchemy import desc, select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import (
    User, Plant, SensorData, SystemActivity, Activity, 
    PlantActivity, ActivitySummary, Waitlist, BlogPost,
    Stream, Metric, Zone
)


async def get_system_health_diagnostics(session: AsyncSession) -> Dict[str, Any]:
    """Get comprehensive system health diagnostics."""
    try:
        # Basic system information
        system_info = {
            "app_name": "CultivAR",
            "environment": os.getenv("FLASK_ENV", "production"),
            "python_version": sys.version,
            "platform": platform.platform(),
            "architecture": platform.architecture(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "node": platform.node(),
            "current_working_directory": os.getcwd(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Database health check
        db_health = await _check_database_health(session)
        
        # System performance metrics
        performance_metrics = _get_system_performance()
        
        # Application metrics
        app_metrics = await _get_application_metrics(session)
        
        return {
            "system_info": system_info,
            "database_health": db_health,
            "performance": performance_metrics,
            "application_metrics": app_metrics,
            "status": "healthy"
        }
        
    except Exception as e:
        logger.error(f"Error getting system health diagnostics: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


async def get_database_health_check(session: AsyncSession) -> Dict[str, Any]:
    """Perform comprehensive database health check."""
    try:
        # Test basic connectivity
        await session.execute(select(1))
        
        # Get table counts
        table_stats = {}
        
        # User table stats
        user_count_result = await session.execute(select(func.count(User.id)))
        table_stats["users"] = user_count_result.scalar() or 0
        
        # Plant table stats
        plant_count_result = await session.execute(select(func.count(Plant.id)))
        table_stats["plants"] = plant_count_result.scalar() or 0
        
        # System activity stats
        activity_count_result = await session.execute(select(func.count(SystemActivity.id)))
        table_stats["system_activities"] = activity_count_result.scalar() or 0
        
        # Recent activity (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        recent_activity_result = await session.execute(
            select(func.count(SystemActivity.id)).where(SystemActivity.timestamp >= yesterday)
        )
        table_stats["recent_activities"] = recent_activity_result.scalar() or 0
        
        # Sensor data stats
        sensor_count_result = await session.execute(select(func.count(SensorData.id)))
        table_stats["sensor_readings"] = sensor_count_result.scalar() or 0
        
        return {
            "status": "connected",
            "database_url": "Configured and accessible",
            "table_statistics": table_stats,
            "last_check": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "error": str(e),
            "last_check": datetime.now().isoformat()
        }


async def get_user_activity_summary(session: AsyncSession) -> Dict[str, Any]:
    """Get comprehensive user activity summary for diagnostics."""
    try:
        # Total users
        total_users_result = await session.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar() or 0
        
        # Active users (with activity in last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_users_result = await session.execute(
            select(func.count(func.distinct(SystemActivity.user_id)))
            .where(SystemActivity.timestamp >= thirty_days_ago)
        )
        active_users = active_users_result.scalar() or 0
        
        # Recent registrations (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_registrations_result = await session.execute(
            select(func.count(User.id)).where(User.created_at >= seven_days_ago)
        )
        recent_registrations = recent_registrations_result.scalar() or 0
        
        # Recent activities (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        recent_activities_result = await session.execute(
            select(func.count(SystemActivity.id)).where(SystemActivity.timestamp >= yesterday)
        )
        recent_activities = recent_activities_result.scalar() or 0
        
        # Most active users (top 10)
        most_active_users_result = await session.execute(
            select(SystemActivity.user_id, func.count(SystemActivity.id).label('activity_count'))
            .where(SystemActivity.timestamp >= thirty_days_ago)
            .group_by(SystemActivity.user_id)
            .order_by(desc('activity_count'))
            .limit(10)
        )
        most_active_users = [
            {"user_id": row[0], "activity_count": row[1]}
            for row in most_active_users_result.all()
        ]
        
        return {
            "total_users": total_users,
            "active_users_30_days": active_users,
            "recent_registrations_7_days": recent_registrations,
            "recent_activities_24_hours": recent_activities,
            "most_active_users": most_active_users,
            "activity_rate": round((active_users / max(total_users, 1)) * 100, 2)
        }
        
    except Exception as e:
        logger.error(f"Error getting user activity summary: {e}")
        return {
            "error": str(e),
            "total_users": 0,
            "active_users_30_days": 0,
            "recent_registrations_7_days": 0,
            "recent_activities_24_hours": 0,
            "most_active_users": [],
            "activity_rate": 0
        }


async def get_plant_health_diagnostics(session: AsyncSession) -> Dict[str, Any]:
    """Get comprehensive plant health diagnostics."""
    try:
        # Total plants
        total_plants_result = await session.execute(select(func.count(Plant.id)))
        total_plants = total_plants_result.scalar() or 0
        
        # Plants by status
        status_counts_result = await session.execute(
            select(Plant.status, func.count(Plant.id))
            .group_by(Plant.status)
        )
        plants_by_status = dict(status_counts_result.all())
        
        # Recent plant activities (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_plant_activities_result = await session.execute(
            select(func.count(PlantActivity.id)).where(PlantActivity.date >= seven_days_ago)
        )
        recent_plant_activities = recent_plant_activities_result.scalar() or 0
        
        # Plants with recent activity
        plants_with_activity_result = await session.execute(
            select(func.count(func.distinct(PlantActivity.plant_id)))
            .where(PlantActivity.date >= seven_days_ago)
        )
        plants_with_activity = plants_with_activity_result.scalar() or 0
        
        # Health distribution (plants with good care vs neglected)
        neglected_plants = max(0, total_plants - plants_with_activity)
        
        return {
            "total_plants": total_plants,
            "plants_by_status": plants_by_status,
            "recent_plant_activities_7_days": recent_plant_activities,
            "plants_with_recent_activity": plants_with_activity,
            "neglected_plants": neglected_plants,
            "care_percentage": round((plants_with_activity / max(total_plants, 1)) * 100, 2),
            "health_score": min(100, (plants_with_activity * 10) + (total_plants * 5))
        }
        
    except Exception as e:
        logger.error(f"Error getting plant health diagnostics: {e}")
        return {
            "error": str(e),
            "total_plants": 0,
            "plants_by_status": {},
            "recent_plant_activities_7_days": 0,
            "plants_with_recent_activity": 0,
            "neglected_plants": 0,
            "care_percentage": 0,
            "health_score": 0
        }


async def get_sensor_diagnostics(session: AsyncSession) -> Dict[str, Any]:
    """Get comprehensive sensor data diagnostics."""
    try:
        # Total sensors (from streams)
        total_streams_result = await session.execute(select(func.count(Stream.id)))
        total_streams = total_streams_result.scalar() or 0
        
        # Recent sensor data (last 24 hours)
        yesterday = datetime.now() - timedelta(days=1)
        recent_readings_result = await session.execute(
            select(func.count(SensorData.id)).where(SensorData.timestamp >= yesterday)
        )
        recent_readings = recent_readings_result.scalar() or 0
        
        # Active sensors (with data in last 24 hours)
        active_streams_result = await session.execute(
            select(func.count(func.distinct(SensorData.stream_id)))
            .where(SensorData.timestamp >= yesterday)
        )
        active_streams = active_streams_result.scalar() or 0
        
        # Average readings per stream
        avg_readings = round(recent_readings / max(active_streams, 1), 2)
        
        return {
            "total_streams": total_streams,
            "active_streams_24_hours": active_streams,
            "recent_readings_24_hours": recent_readings,
            "average_readings_per_stream": avg_readings,
            "inactive_streams": max(0, total_streams - active_streams),
            "sensor_health_percentage": round((active_streams / max(total_streams, 1)) * 100, 2)
        }
        
    except Exception as e:
        logger.error(f"Error getting sensor diagnostics: {e}")
        return {
            "error": str(e),
            "total_streams": 0,
            "active_streams_24_hours": 0,
            "recent_readings_24_hours": 0,
            "average_readings_per_stream": 0,
            "inactive_streams": 0,
            "sensor_health_percentage": 0
        }


async def get_application_performance_metrics(session: AsyncSession) -> Dict[str, Any]:
    """Get application performance and usage metrics."""
    try:
        # Activity patterns (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        # Daily activity counts
        daily_activity_result = await session.execute(
            select(
                func.date(SystemActivity.timestamp).label('date'),
                func.count(SystemActivity.id).label('count')
            )
            .where(SystemActivity.timestamp >= seven_days_ago)
            .group_by(func.date(SystemActivity.timestamp))
            .order_by('date')
        )
        
        daily_activity = [
            {"date": str(row[0]), "count": row[1]}
            for row in daily_activity_result.all()
        ]
        
        # User engagement metrics
        unique_users_result = await session.execute(
            select(func.count(func.distinct(SystemActivity.user_id)))
            .where(SystemActivity.timestamp >= seven_days_ago)
        )
        unique_users_7_days = unique_users_result.scalar() or 0
        
        # Peak activity hour (simplified)
        hourly_activity_result = await session.execute(
            select(
                func.extract('hour', SystemActivity.timestamp).label('hour'),
                func.count(SystemActivity.id).label('count')
            )
            .where(SystemActivity.timestamp >= seven_days_ago)
            .group_by(func.extract('hour', SystemActivity.timestamp))
            .order_by(desc('count'))
            .limit(1)
        )
        
        peak_hour_row = hourly_activity_result.first()
        peak_hour = peak_hour_row[0] if peak_hour_row else 0
        
        return {
            "daily_activity_7_days": daily_activity,
            "unique_users_7_days": unique_users_7_days,
            "peak_activity_hour": int(peak_hour),
            "average_daily_activity": round(len(daily_activity) * (unique_users_7_days / 7), 2) if daily_activity else 0
        }
        
    except Exception as e:
        logger.error(f"Error getting application performance metrics: {e}")
        return {
            "error": str(e),
            "daily_activity_7_days": [],
            "unique_users_7_days": 0,
            "peak_activity_hour": 0,
            "average_daily_activity": 0
        }


async def get_error_logs_analysis(session: AsyncSession) -> Dict[str, Any]:
    """Analyze recent error logs and system issues."""
    try:
        # Recent error activities (assuming error types are logged)
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
        
        # Get error activities (activities with 'error' in type or details)
        error_activities_result = await session.execute(
            select(SystemActivity)
            .where(
                SystemActivity.timestamp >= twenty_four_hours_ago,
                (SystemActivity.type.like('%error%')) | (SystemActivity.details.like('%error%'))
            )
            .order_by(desc(SystemActivity.timestamp))
            .limit(50)
        )
        
        error_activities = error_activities_result.scalars().all()
        
        # Count errors by type
        error_types = {}
        for activity in error_activities:
            error_type = activity.type or "unknown"
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Most recent errors
        recent_errors = [
            {
                "type": activity.type,
                "details": activity.details[:200] + "..." if len(activity.details or "") > 200 else activity.details,
                "timestamp": activity.timestamp.isoformat(),
                "user_id": activity.user_id
            }
            for activity in error_activities[:10]
        ]
        
        return {
            "total_errors_24_hours": len(error_activities),
            "error_types_distribution": error_types,
            "recent_errors": recent_errors,
            "error_rate": "low" if len(error_activities) < 10 else "medium" if len(error_activities) < 50 else "high"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing error logs: {e}")
        return {
            "error": str(e),
            "total_errors_24_hours": 0,
            "error_types_distribution": {},
            "recent_errors": [],
            "error_rate": "unknown"
        }


async def get_comprehensive_system_diagnostics(session: AsyncSession) -> Dict[str, Any]:
    """Get complete system diagnostics combining all diagnostic functions."""
    try:
        # Run all diagnostic functions concurrently
        system_health = await get_system_health_diagnostics(session)
        db_health = await get_database_health_check(session)
        user_activity = await get_user_activity_summary(session)
        plant_health = await get_plant_health_diagnostics(session)
        sensor_data = await get_sensor_diagnostics(session)
        performance_metrics = await get_application_performance_metrics(session)
        error_analysis = await get_error_logs_analysis(session)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_health": system_health,
            "database": db_health,
            "user_activity": user_activity,
            "plant_health": plant_health,
            "sensor_data": sensor_data,
            "performance": performance_metrics,
            "errors": error_analysis,
            "overall_status": _calculate_overall_status(system_health, db_health, plant_health, sensor_data)
        }
        
    except Exception as e:
        logger.error(f"Error getting comprehensive system diagnostics: {e}")
        return {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "overall_status": "error"
        }


# Helper functions

async def _check_database_health(session: AsyncSession) -> Dict[str, Any]:
    """Check database connectivity and basic operations."""
    try:
        start_time = datetime.now()
        await session.execute(select(1))
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return {
            "status": "healthy",
            "response_time_ms": round(response_time, 2),
            "connection": "active"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "connection": "failed"
        }


def _get_system_performance() -> Dict[str, Any]:
    """Get system performance metrics using psutil."""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory usage
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "cpu": {
                "usage_percent": cpu_percent,
                "count": cpu_count,
                "status": "high" if cpu_percent > 80 else "normal"
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "usage_percent": memory.percent,
                "status": "high" if memory.percent > 85 else "normal"
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": round((disk.used / disk.total) * 100, 2),
                "status": "high" if (disk.used / disk.total) > 0.9 else "normal"
            }
        }
    except Exception as e:
        logger.error(f"Error getting system performance metrics: {e}")
        return {
            "error": str(e),
            "cpu": {"usage_percent": 0, "count": 0, "status": "unknown"},
            "memory": {"total_gb": 0, "used_gb": 0, "usage_percent": 0, "status": "unknown"},
            "disk": {"total_gb": 0, "used_gb": 0, "usage_percent": 0, "status": "unknown"}
        }


async def _get_application_metrics(session: AsyncSession) -> Dict[str, Any]:
    """Get application-specific metrics."""
    try:
        # Basic counts
        total_users_result = await session.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar() or 0
        
        total_plants_result = await session.execute(select(func.count(Plant.id)))
        total_plants = total_plants_result.scalar() or 0
        
        # Uptime estimate (based on oldest activity)
        oldest_activity_result = await session.execute(
            select(func.min(SystemActivity.timestamp))
        )
        oldest_activity = oldest_activity_result.scalar()
        
        uptime_hours = 0
        if oldest_activity:
            uptime_hours = round((datetime.now() - oldest_activity).total_seconds() / 3600, 2)
        
        return {
            "total_users": total_users,
            "total_plants": total_plants,
            "estimated_uptime_hours": uptime_hours,
            "application_status": "running"
        }
        
    except Exception as e:
        logger.error(f"Error getting application metrics: {e}")
        return {
            "error": str(e),
            "total_users": 0,
            "total_plants": 0,
            "estimated_uptime_hours": 0,
            "application_status": "unknown"
        }


def _calculate_overall_status(system_health: Dict, db_health: Dict, plant_health: Dict, sensor_data: Dict) -> str:
    """Calculate overall system status based on individual components."""
    try:
        status_scores = []
        
        # System health score
        if system_health.get("status") == "healthy":
            status_scores.append(100)
        elif "error" in system_health:
            status_scores.append(0)
        else:
            status_scores.append(50)
        
        # Database health score
        if db_health.get("status") == "connected":
            status_scores.append(100)
        elif db_health.get("status") == "error":
            status_scores.append(0)
        else:
            status_scores.append(50)
        
        # Plant health score (care percentage as proxy)
        care_percentage = plant_health.get("care_percentage", 0)
        status_scores.append(care_percentage)
        
        # Sensor health percentage
        sensor_percentage = sensor_data.get("sensor_health_percentage", 0)
        status_scores.append(sensor_percentage)
        
        average_score = sum(status_scores) / len(status_scores)
        
        if average_score >= 80:
            return "excellent"
        elif average_score >= 60:
            return "good"
        elif average_score >= 40:
            return "fair"
        elif average_score >= 20:
            return "poor"
        else:
            return "critical"
            
    except Exception:
        return "unknown"