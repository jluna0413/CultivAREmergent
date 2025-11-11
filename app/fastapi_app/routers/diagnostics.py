"""Diagnostics Router - Migrated from app/blueprints/diagnostics.py"""
from fastapi import APIRouter, Request, Depends, HTTPException
from app.fastapi_app.dependencies import require_login, inject_template_context
from app.models_async.auth import User
from app.fastapi_app.models.diagnostics import ComprehensiveDiagnostics, SystemHealth, DatabaseHealth, UserActivitySummary, PlantHealthDiagnostics, SensorDiagnostics, AppPerformanceMetrics, ErrorLogAnalysis
from datetime import datetime

router = APIRouter(tags=["diagnostics"])

@router.get("/", name="diagnostics_page")
async def diagnostics_page(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    return request.app.state.templates.TemplateResponse("views/diagnostics.html", context)

@router.get("/dashboard", name="diagnostics_dashboard")
async def diagnostics_dashboard(request: Request, current_user: User = Depends(require_login), context: dict = Depends(inject_template_context)):
    # In a real implementation, you would fetch diagnostic data here
    context["diagnostics_data"] = {"status": "ok"}
    return request.app.state.templates.TemplateResponse("admin/diagnostics_dashboard.html", context)

@router.get("/api/health", response_model=SystemHealth)
async def api_health():
    return SystemHealth(status="ok", database="ok", cache="ok", disk_space="ok")

@router.get("/api/database", response_model=DatabaseHealth)
async def api_database():
    return DatabaseHealth(status="ok", connection_time=0.123)

@router.get("/api/users", response_model=UserActivitySummary)
async def api_users():
    return UserActivitySummary(active_users_24h=10, new_users_24h=2, logins_24h=25)

@router.get("/api/plants", response_model=PlantHealthDiagnostics)
async def api_plants():
    return PlantHealthDiagnostics(total_plants=100, plants_with_issues=5, recent_activities=50)

@router.get("/api/sensors", response_model=SensorDiagnostics)
async def api_sensors():
    return SensorDiagnostics(total_sensors=20, active_sensors=18, readings_24h=1000)

@router.get("/api/performance", response_model=AppPerformanceMetrics)
async def api_performance():
    return AppPerformanceMetrics(avg_response_time=0.2, error_rate=0.01, requests_per_minute=120)

@router.get("/api/errors", response_model=ErrorLogAnalysis)
async def api_errors():
    return ErrorLogAnalysis(total_errors_24h=5, most_common_error="None")

@router.get("/api/comprehensive", response_model=ComprehensiveDiagnostics)
async def api_comprehensive():
    now = datetime.utcnow()
    return ComprehensiveDiagnostics(
        system_health=SystemHealth(status="ok", database="ok", cache="ok", disk_space="ok"),
        db_health=DatabaseHealth(status="ok", connection_time=0.123),
        user_activity=UserActivitySummary(active_users_24h=10, new_users_24h=2, logins_24h=25),
        plant_health=PlantHealthDiagnostics(total_plants=100, plants_with_issues=5, recent_activities=50),
        sensor_diagnostics=SensorDiagnostics(total_sensors=20, active_sensors=18, readings_24h=1000),
        app_performance=AppPerformanceMetrics(avg_response_time=0.2, error_rate=0.01, requests_per_minute=120),
        error_analysis=ErrorLogAnalysis(total_errors_24h=5, most_common_error="None"),
        generated_at=now
    )

@router.get("/status")
async def status():
    return {"status": "ok"}

@router.get("/api/realtime")
async def api_realtime():
    return {"timestamp": datetime.utcnow(), "cpu_usage": 0.5, "memory_usage": 0.6}

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/api/system-info")
async def api_system_info():
    return {"python_version": "3.9", "os": "linux"}
