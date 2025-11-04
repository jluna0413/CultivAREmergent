"""
Diagnostics blueprint for the CultivAR application - ASYNC VERSION.
Comprehensive diagnostic and health monitoring functionality.
"""

import os
import platform
import sys
import traceback
from datetime import datetime
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.logger import logger
from app.utils.async_flask_helpers import FlaskAsyncSessionManager

# Import comprehensive async diagnostic handlers
from app.handlers.diagnostic_handlers_async import (
    get_system_health_diagnostics,
    get_database_health_check,
    get_user_activity_summary,
    get_plant_health_diagnostics,
    get_sensor_diagnostics,
    get_application_performance_metrics,
    get_error_logs_analysis,
    get_comprehensive_system_diagnostics
)

diagnostics_bp = Blueprint("diagnostics", __name__, url_prefix="/diagnostics", template_folder="../web/templates")


# Basic diagnostics route (existing functionality maintained)
@diagnostics_bp.route("/")
async def diagnostics():
    """Basic system diagnostics - API endpoint."""
    # App info
    info = {
        "app_name": "CultivAR",
        "version": getattr(current_app, "version", "unknown"),
        "environment": os.getenv("FLASK_ENV", "production"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "timestamp": datetime.now().isoformat()
    }

    # Database check using async handler
    try:
        async with FlaskAsyncSessionManager() as session:
            db_status = await get_database_health_check(session)
    except Exception as e:
        db_status = {"status": "error", "error": str(e)}

    # Recent log lines
    log_path = os.path.join(os.getcwd(), "logs", "cultivar.log")
    try:
        with open(log_path, "r") as f:
            log_lines = f.readlines()[-20:]
    except Exception as e:
        log_lines = [f"Could not read log: {e}"]

    return jsonify({
        "info": info, 
        "database": db_status, 
        "recent_logs": log_lines,
        "status": "success"
    })


# Web interface for diagnostics
@diagnostics_bp.route("/dashboard")
@login_required
async def diagnostics_dashboard():
    """Render comprehensive diagnostics dashboard."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get comprehensive system diagnostics
            system_data = await get_comprehensive_system_diagnostics(session)
            
            # Get specific metrics for display
            db_health = await get_database_health_check(session)
            user_activity = await get_user_activity_summary(session)
            plant_health = await get_plant_health_diagnostics(session)
            sensor_data = await get_sensor_diagnostics(session)
            performance_metrics = await get_application_performance_metrics(session)
            error_analysis = await get_error_logs_analysis(session)

        return render_template(
            "admin/diagnostics_dashboard.html",
            title="System Diagnostics",
            system_data=system_data,
            db_health=db_health,
            user_activity=user_activity,
            plant_health=plant_health,
            sensor_data=sensor_data,
            performance_metrics=performance_metrics,
            error_analysis=error_analysis,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.exception(f"Error loading diagnostics dashboard: {e}")
        flash(f"Error loading diagnostics dashboard: {str(e)}", "danger")
        return redirect(url_for("admin.admin_dashboard"))


# API endpoint for system health
@diagnostics_bp.route("/api/health")
async def system_health_api():
    """API endpoint for system health monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            health_data = await get_system_health_diagnostics(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": health_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting system health: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for database health
@diagnostics_bp.route("/api/database")
async def database_health_api():
    """API endpoint for database health monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            db_health = await get_database_health_check(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": db_health
        })
        
    except Exception as e:
        logger.exception(f"Error getting database health: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for user activity
@diagnostics_bp.route("/api/users")
@login_required
async def user_activity_api():
    """API endpoint for user activity monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            user_data = await get_user_activity_summary(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": user_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting user activity: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for plant health
@diagnostics_bp.route("/api/plants")
@login_required
async def plant_health_api():
    """API endpoint for plant health monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            plant_data = await get_plant_health_diagnostics(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": plant_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting plant health: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for sensor data
@diagnostics_bp.route("/api/sensors")
@login_required
async def sensor_data_api():
    """API endpoint for sensor data monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            sensor_data = await get_sensor_diagnostics(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": sensor_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting sensor data: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for performance metrics
@diagnostics_bp.route("/api/performance")
@login_required
async def performance_metrics_api():
    """API endpoint for application performance monitoring."""
    try:
        async with FlaskAsyncSessionManager() as session:
            performance_data = await get_application_performance_metrics(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": performance_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting performance metrics: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# API endpoint for error analysis
@diagnostics_bp.route("/api/errors")
@login_required
async def error_analysis_api():
    """API endpoint for error log analysis."""
    try:
        async with FlaskAsyncSessionManager() as session:
            error_data = await get_error_logs_analysis(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": error_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting error analysis: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# Comprehensive system overview API
@diagnostics_bp.route("/api/comprehensive")
@login_required
async def comprehensive_system_api():
    """API endpoint for comprehensive system diagnostics."""
    try:
        async with FlaskAsyncSessionManager() as session:
            comprehensive_data = await get_comprehensive_system_diagnostics(session)
            
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "data": comprehensive_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting comprehensive system data: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# System status page (simplified view)
@diagnostics_bp.route("/status")
async def system_status():
    """Simple system status page for monitoring tools."""
    try:
        async with FlaskAsyncSessionManager() as session:
            db_health = await get_database_health_check(session)
            system_health = await get_system_health_diagnostics(session)
            
        # Simple status for monitoring tools
        overall_status = "healthy"
        if db_health.get("status") != "connected":
            overall_status = "unhealthy"
        elif system_health.get("status") == "error":
            overall_status = "degraded"
            
        status_data = {
            "service": "CultivAR",
            "status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "version": getattr(current_app, "version", "unknown"),
            "database": db_health.get("status", "unknown"),
            "system": system_health.get("status", "unknown")
        }
        
        return jsonify(status_data)
        
    except Exception as e:
        logger.exception(f"Error getting system status: {e}")
        return jsonify({
            "service": "CultivAR",
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# Real-time monitoring data (for admin dashboard updates)
@diagnostics_bp.route("/api/realtime")
@login_required
async def realtime_monitoring_api():
    """API endpoint for real-time monitoring data."""
    try:
        async with FlaskAsyncSessionManager() as session:
            # Get fresh data for real-time updates
            user_activity = await get_user_activity_summary(session)
            sensor_data = await get_sensor_diagnostics(session)
            performance_data = await get_application_performance_metrics(session)
            
        realtime_data = {
            "timestamp": datetime.now().isoformat(),
            "user_activity": {
                "recent_activities_24_hours": user_activity.get("recent_activities_24_hours", 0),
                "active_users_30_days": user_activity.get("active_users_30_days", 0)
            },
            "sensors": {
                "active_streams_24_hours": sensor_data.get("active_streams_24_hours", 0),
                "recent_readings_24_hours": sensor_data.get("recent_readings_24_hours", 0)
            },
            "performance": {
                "unique_users_7_days": performance_data.get("unique_users_7_days", 0),
                "peak_activity_hour": performance_data.get("peak_activity_hour", 0)
            }
        }
        
        return jsonify({
            "status": "success",
            "data": realtime_data
        })
        
    except Exception as e:
        logger.exception(f"Error getting realtime monitoring data: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# Error handlers
@diagnostics_bp.errorhandler(404)
async def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Diagnostic endpoint not found",
        "status": 404,
        "timestamp": datetime.now().isoformat()
    }), 404


@diagnostics_bp.errorhandler(500)
async def internal_error(error):
    """Handle 500 errors."""
    try:
        logger.error(f"Diagnostics blueprint error: {error}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    except Exception:
        pass
    
    return jsonify({
        "error": "Internal server error in diagnostics",
        "status": 500,
        "timestamp": datetime.now().isoformat()
    }), 500


# Health check for load balancers
@diagnostics_bp.route("/health")
async def health_check():
    """Basic health check endpoint for load balancers."""
    try:
        # Test database connectivity
        async with FlaskAsyncSessionManager() as session:
            await session.execute(select(1))
        
        return jsonify({
            "status": "healthy",
            "service": "CultivAR",
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "service": "CultivAR",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 503


# Utility function for monitoring integration
@diagnostics_bp.route("/api/system-info")
async def system_info_api():
    """API endpoint for basic system information."""
    try:
        system_info = {
            "application": {
                "name": "CultivAR",
                "version": getattr(current_app, "version", "unknown"),
                "environment": os.getenv("FLASK_ENV", "production"),
                "timestamp": datetime.now().isoformat()
            },
            "runtime": {
                "python_version": sys.version,
                "platform": platform.platform(),
                "architecture": platform.architecture()[0],
                "processor": platform.processor(),
                "machine": platform.machine(),
                "node": platform.node()
            },
            "filesystem": {
                "current_directory": os.getcwd(),
                "directory_exists": os.path.exists(os.getcwd()),
                "writable": os.access(os.getcwd(), os.W_OK)
            }
        }
        
        return jsonify({
            "status": "success",
            "data": system_info
        })
        
    except Exception as e:
        logger.exception(f"Error getting system info: {e}")
        return jsonify({
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500
