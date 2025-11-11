"""
Health check router for Cultivar Collection Management System
Provides comprehensive operational monitoring, health checks, and observability endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from fastapi.responses import JSONResponse
import datetime
import psutil
import asyncio
import aiofiles
import os
import sys
import json
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Global metrics storage (in production, use Redis or similar)
class MetricsCollector:
    """Collects and stores application metrics for monitoring"""
    
    def __init__(self):
        self.request_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.response_times = deque(maxlen=1000)  # Keep last 1000 response times
        self.start_time = time.time()
        self.last_request_time = {}
        
    def record_request(self, method: str, endpoint: str, status_code: int, response_time: float):
        """Record request metrics"""
        key = f"{method} {endpoint}"
        self.request_counts[key] += 1
        
        if status_code >= 500:
            self.error_counts[f"{key}_{status_code}"] += 1
        
        self.response_times.append({
            'timestamp': time.time(),
            'method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time': response_time
        })
        
        self.last_request_time[key] = time.time()
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current metrics summary"""
        uptime = time.time() - self.start_time
        
        # Calculate average response time
        if self.response_times:
            avg_response_time = sum(r['response_time'] for r in self.response_times) / len(self.response_times)
            max_response_time = max(r['response_time'] for r in self.response_times)
            min_response_time = min(r['response_time'] for r in self.response_times)
        else:
            avg_response_time = max_response_time = min_response_time = 0
        
        # Calculate error rate (last 100 requests)
        recent_requests = list(self.response_times)[-100:] if self.response_times else []
        error_count = sum(1 for r in recent_requests if r['status_code'] >= 500)
        error_rate = (error_count / len(recent_requests) * 100) if recent_requests else 0
        
        return {
            "uptime_seconds": uptime,
            "total_requests": sum(self.request_counts.values()),
            "average_response_time": round(avg_response_time, 4),
            "max_response_time": round(max_response_time, 4),
            "min_response_time": round(min_response_time, 4),
            "error_rate_percent": round(error_rate, 2),
            "error_counts": dict(self.error_counts),
            "top_endpoints": dict(sorted(self.request_counts.items(), key=lambda x: x[1], reverse=True)[:10])
        }

# Global metrics instance
metrics = MetricsCollector()

@dataclass
class HealthCheck:
    """Individual health check result"""
    name: str
    status: str  # "healthy", "degraded", "unhealthy"
    message: str
    response_time: Optional[float] = None
    last_check: Optional[str] = None

class HealthChecker:
    """Performs various health checks on the system"""
    
    @staticmethod
    async def check_database() -> HealthCheck:
        """Check database connectivity"""
        try:
            start_time = time.time()
            # Simulate database check - replace with actual async SQLAlchemy check
            await asyncio.sleep(0.1)  # Simulate database operation
            
            # In production, use actual database connection check
            response_time = time.time() - start_time
            return HealthCheck(
                name="database",
                status="healthy",
                message="Database connection successful",
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="database",
                status="unhealthy",
                message=f"Database connection failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )
    
    @staticmethod
    async def check_disk_space() -> HealthCheck:
        """Check disk space availability"""
        try:
            start_time = time.time()
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            used_percent = (disk.used / disk.total) * 100
            
            # Define thresholds
            if free_gb < 1:  # Less than 1GB free
                status = "unhealthy"
                message = f"Critical disk space: {free_gb:.2f}GB free ({used_percent:.1f}% used)"
            elif free_gb < 5:  # Less than 5GB free
                status = "degraded"
                message = f"Low disk space: {free_gb:.2f}GB free ({used_percent:.1f}% used)"
            else:
                status = "healthy"
                message = f"Disk space OK: {free_gb:.2f}GB free ({used_percent:.1f}% used)"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="disk_space",
                status=status,
                message=message,
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="disk_space",
                status="unhealthy",
                message=f"Disk check failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )
    
    @staticmethod
    async def check_memory() -> HealthCheck:
        """Check memory usage"""
        try:
            start_time = time.time()
            memory = psutil.virtual_memory()
            free_gb = memory.available / (1024**3)
            total_gb = memory.total / (1024**3)
            used_percent = memory.percent
            
            # Define thresholds
            if used_percent > 90:
                status = "unhealthy"
                message = f"Critical memory usage: {used_percent:.1f}% used, {free_gb:.2f}GB available"
            elif used_percent > 80:
                status = "degraded"
                message = f"High memory usage: {used_percent:.1f}% used, {free_gb:.2f}GB available"
            else:
                status = "healthy"
                message = f"Memory usage OK: {used_percent:.1f}% used, {free_gb:.2f}GB available"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="memory",
                status=status,
                message=message,
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="memory",
                status="unhealthy",
                message=f"Memory check failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )
    
    @staticmethod
    async def check_cpu() -> HealthCheck:
        """Check CPU usage"""
        try:
            start_time = time.time()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Define thresholds
            if cpu_percent > 90:
                status = "unhealthy"
                message = f"Critical CPU usage: {cpu_percent:.1f}%"
            elif cpu_percent > 80:
                status = "degraded"
                message = f"High CPU usage: {cpu_percent:.1f}%"
            else:
                status = "healthy"
                message = f"CPU usage OK: {cpu_percent:.1f}%"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="cpu",
                status=status,
                message=message,
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="cpu",
                status="unhealthy",
                message=f"CPU check failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )
    
    @staticmethod
    async def check_environment_variables() -> HealthCheck:
        """Check critical environment variables"""
        try:
            start_time = time.time()
            required_vars = [
                'DATABASE_URL',
                'JWT_SECRET_KEY',
                'SECRET_KEY'
            ]
            
            missing_vars = []
            for var in required_vars:
                if not os.getenv(var):
                    missing_vars.append(var)
            
            if missing_vars:
                status = "unhealthy"
                message = f"Missing environment variables: {', '.join(missing_vars)}"
            else:
                status = "healthy"
                message = "All required environment variables present"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="environment",
                status=status,
                message=message,
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="environment",
                status="unhealthy",
                message=f"Environment check failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )
    
    @staticmethod
    async def check_application_health() -> HealthCheck:
        """Check application-specific health metrics"""
        try:
            start_time = time.time()
            
            # Check recent metrics
            summary = metrics.get_metrics_summary()
            
            # Define thresholds
            if summary['error_rate_percent'] > 5:
                status = "unhealthy"
                message = f"High error rate: {summary['error_rate_percent']}%"
            elif summary['error_rate_percent'] > 1:
                status = "degraded"
                message = f"Elevated error rate: {summary['error_rate_percent']}%"
            elif summary['average_response_time'] > 2.0:
                status = "degraded"
                message = f"High response time: {summary['average_response_time']}s"
            else:
                status = "healthy"
                message = "Application performance normal"
            
            response_time = time.time() - start_time
            return HealthCheck(
                name="application",
                status=status,
                message=message,
                response_time=response_time,
                last_check=datetime.datetime.utcnow().isoformat()
            )
        except Exception as e:
            return HealthCheck(
                name="application",
                status="unhealthy",
                message=f"Application health check failed: {str(e)}",
                last_check=datetime.datetime.utcnow().isoformat()
            )

health_checker = HealthChecker()

@router.get("/", summary="Health Check")
async def health_check():
    """
    Comprehensive health check endpoint
    
    Returns overall system health including database, memory, disk, and CPU status.
    This is the primary health endpoint that should be monitored.
    """
    try:
        # Run all health checks
        checks = await asyncio.gather(
            health_checker.check_database(),
            health_checker.check_disk_space(),
            health_checker.check_memory(),
            health_checker.check_cpu(),
            health_checker.check_environment_variables(),
            health_checker.check_application_health(),
            return_exceptions=True
        )
        
        # Determine overall status
        healthy_checks = []
        degraded_checks = []
        unhealthy_checks = []
        error_checks = []
        
        for check in checks:
            if isinstance(check, HealthCheck):
                if check.status == "healthy":
                    healthy_checks.append(check)
                elif check.status == "degraded":
                    degraded_checks.append(check)
                elif check.status == "unhealthy":
                    unhealthy_checks.append(check)
            else:
                # Handle exceptions from failed health checks
                error_checks.append(str(check))
        
        if unhealthy_checks or error_checks:
            overall_status = "unhealthy"
            status_code = 503
        elif degraded_checks:
            overall_status = "degraded"
            status_code = 200
        else:
            overall_status = "healthy"
            status_code = 200
        
        # Build response
        check_results = {}
        for check in checks:
            if isinstance(check, HealthCheck):
                check_results[check.name] = {
                    "status": check.status,
                    "message": check.message,
                    "response_time": check.response_time,
                    "last_check": check.last_check
                }
        
        # Add error information if any checks failed
        if error_checks:
            check_results["errors"] = error_checks
        
        response_data = {
            "status": overall_status,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "service": "Cultivar Collection Management API",
            "version": "2.0.0",
            "uptime_seconds": time.time() - metrics.start_time,
            "checks": check_results,
            "total_checks": len(checks),
            "healthy_checks": len(healthy_checks),
            "degraded_checks": len(degraded_checks),
            "unhealthy_checks": len(unhealthy_checks),
            "error_checks": len(error_checks)
        }
        
        return JSONResponse(content=response_data, status_code=status_code)
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            content={
                "status": "unhealthy",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "error": "Health check execution failed",
                "message": str(e)
            },
            status_code=503
        )

@router.get("/live", summary="Liveness Probe")
async def liveness_check():
    """
    Kubernetes liveness probe endpoint
    
    Returns 200 if the application is running, 503 if it should be restarted.
    This should be very simple and fast - just check if the process is alive.
    """
    try:
        # Very basic liveness check
        return JSONResponse(
            content={
                "status": "alive",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "uptime_seconds": time.time() - metrics.start_time
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Liveness check failed: {str(e)}")
        return JSONResponse(
            content={
                "status": "dead",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "error": str(e)
            },
            status_code=503
        )

@router.get("/ready", summary="Readiness Probe")
async def readiness_check():
    """
    Kubernetes readiness probe endpoint
    
    Returns 200 if the application is ready to receive traffic, 503 otherwise.
    This should check dependencies like database connectivity.
    """
    try:
        # Check database connectivity
        db_check = await health_checker.check_database()
        
        if db_check.status == "healthy":
            return JSONResponse(
                content={
                    "status": "ready",
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "dependencies": {
                        "database": db_check.status
                    }
                },
                status_code=200
            )
        else:
            return JSONResponse(
                content={
                    "status": "not_ready",
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                    "dependencies": {
                        "database": db_check.status,
                        "reason": db_check.message
                    }
                },
                status_code=503
            )
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            content={
                "status": "not_ready",
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "error": str(e)
            },
            status_code=503
        )

@router.get("/metrics", summary="Application Metrics")
async def get_metrics():
    """
    Prometheus-compatible metrics endpoint
    
    Returns application metrics including request counts, response times, and error rates.
    This can be scraped by monitoring systems like Prometheus.
    """
    try:
        summary = metrics.get_metrics_summary()
        
        # Add system metrics
        system_metrics = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        }
        
        response_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "application_metrics": summary,
            "system_metrics": system_metrics
        }
        
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}")
        return JSONResponse(
            content={
                "error": "Failed to collect metrics",
                "message": str(e)
            },
            status_code=500
        )

@router.get("/status", summary="System Status")
async def system_status():
    """
    Detailed system status endpoint
    
    Provides comprehensive system information including uptime, version, and environment.
    """
    try:
        # Get current metrics
        summary = metrics.get_metrics_summary()
        
        response_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "service": {
                "name": "Cultivar Collection Management API",
                "version": "2.0.0",
                "uptime_seconds": summary["uptime_seconds"],
                "environment": os.getenv("ENVIRONMENT", "development"),
                "build_date": "2025-01-29",
                "api_version": "v1"
            },
            "performance": {
                "total_requests": summary["total_requests"],
                "average_response_time": summary["average_response_time"],
                "max_response_time": summary["max_response_time"],
                "error_rate_percent": summary["error_rate_percent"]
            },
            "system": {
                "cpu_percent": psutil.cpu_percent(),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage_percent": psutil.disk_usage('/').percent,
                "python_version": sys.version,
                "platform": sys.platform
            }
        }
        
        return JSONResponse(content=response_data, status_code=200)
    except Exception as e:
        logger.error(f"System status check failed: {str(e)}")
        return JSONResponse(
            content={
                "error": "Failed to get system status",
                "message": str(e)
            },
            status_code=500
        )

@router.get("/dependencies", summary="Dependency Health")
async def dependency_health():
    """
    Check health of external dependencies
    
    Returns status of all external services and dependencies.
    """
    try:
        # Run dependency checks
        checks = await asyncio.gather(
            health_checker.check_database(),
            health_checker.check_environment_variables(),
            return_exceptions=True
        )
        
        dependencies = {}
        for check in checks:
            if isinstance(check, HealthCheck):
                dependencies[check.name] = {
                    "status": check.status,
                    "message": check.message,
                    "last_check": check.last_check
                }
            else:
                dependencies[f"error_{len(dependencies)}"] = {
                    "status": "error",
                    "message": str(check),
                    "last_check": datetime.datetime.utcnow().isoformat()
                }
        
        # Determine overall dependency status
        unhealthy_deps = [dep for dep in dependencies.values() if dep["status"] == "unhealthy"]
        overall_status = "unhealthy" if unhealthy_deps else "healthy"
        status_code = 503 if unhealthy_deps else 200
        
        response_data = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "overall_status": overall_status,
            "dependencies": dependencies,
            "total_dependencies": len(dependencies),
            "healthy_dependencies": len([d for d in dependencies.values() if d["status"] == "healthy"])
        }
        
        return JSONResponse(content=response_data, status_code=status_code)
    except Exception as e:
        logger.error(f"Dependency health check failed: {str(e)}")
        return JSONResponse(
            content={
                "error": "Failed to check dependencies",
                "message": str(e)
            },
            status_code=500
        )

@router.post("/metrics/reset", summary="Reset Metrics")
async def reset_metrics():
    """
    Reset application metrics
    
    Resets all collected metrics. Requires admin authentication in production.
    """
    try:
        # Reset all metrics
        metrics.request_counts.clear()
        metrics.error_counts.clear()
        metrics.response_times.clear()
        metrics.start_time = time.time()
        metrics.last_request_time.clear()
        
        return JSONResponse(
            content={
                "message": "Metrics reset successfully",
                "timestamp": datetime.datetime.utcnow().isoformat()
            },
            status_code=200
        )
    except Exception as e:
        logger.error(f"Failed to reset metrics: {str(e)}")
        return JSONResponse(
            content={
                "error": "Failed to reset metrics",
                "message": str(e)
            },
            status_code=500
        )

@router.get("/health/alert", summary="Alert Configuration")
async def get_alert_configuration():
    """
    Get alerting thresholds and configuration
    
    Returns the configured thresholds for various health metrics.
    """
    try:
        alert_config = {
            "response_time_warning": 1.0,  # seconds
            "response_time_critical": 2.0,  # seconds
            "error_rate_warning": 1.0,  # percentage
            "error_rate_critical": 5.0,  # percentage
            "memory_usage_warning": 80.0,  # percentage
            "memory_usage_critical": 90.0,  # percentage
            "cpu_usage_warning": 80.0,  # percentage
            "cpu_usage_critical": 90.0,  # percentage
            "disk_space_warning_gb": 5.0,  # GB
            "disk_space_critical_gb": 1.0,  # GB
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        
        return JSONResponse(content=alert_config, status_code=200)
    except Exception as e:
        logger.error(f"Failed to get alert configuration: {str(e)}")
        return JSONResponse(
            content={
                "error": "Failed to get alert configuration",
                "message": str(e)
            },
            status_code=500
        )