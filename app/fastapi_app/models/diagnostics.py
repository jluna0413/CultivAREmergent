"""Pydantic models for Diagnostics domain."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class SystemHealth(BaseModel):
    status: str
    database: str
    cache: str
    disk_space: str

class DatabaseHealth(BaseModel):
    status: str
    connection_time: float
    active_connections: Optional[int] = None

class UserActivitySummary(BaseModel):
    active_users_24h: int
    new_users_24h: int
    logins_24h: int

class PlantHealthDiagnostics(BaseModel):
    total_plants: int
    plants_with_issues: int
    recent_activities: int

class SensorDiagnostics(BaseModel):
    total_sensors: int
    active_sensors: int
    readings_24h: int

class AppPerformanceMetrics(BaseModel):
    avg_response_time: float
    error_rate: float
    requests_per_minute: float

class ErrorLogAnalysis(BaseModel):
    total_errors_24h: int
    most_common_error: Optional[str] = None

class ComprehensiveDiagnostics(BaseModel):
    system_health: SystemHealth
    db_health: DatabaseHealth
    user_activity: UserActivitySummary
    plant_health: PlantHealthDiagnostics
    sensor_diagnostics: SensorDiagnostics
    app_performance: AppPerformanceMetrics
    error_analysis: ErrorLogAnalysis
    generated_at: datetime
