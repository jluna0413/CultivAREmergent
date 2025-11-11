"""Pydantic models for Admin domain."""
from pydantic import BaseModel, Field
from typing import List, Optional
from .users import UserResponse

class AdminStats(BaseModel):
    """Model for admin dashboard statistics."""
    total_users: int
    total_plants: int
    total_cultivars: int
    total_breeders: int
    total_clones: int
    total_activities: int
    total_sensors: int

class AdminUserBulkDeleteRequest(BaseModel):
    user_ids: List[int]

class AdminUserToggleAdminRequest(BaseModel):
    user_id: int

class AdminUserForcePasswordResetRequest(BaseModel):
    user_id: int

class SystemInfo(BaseModel):
    python_version: str
    os_name: str
    os_version: str
    cpu_count: str
    memory_total: str
    memory_available: str
    disk_total: str
    disk_free: str
    boot_time: str

class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
