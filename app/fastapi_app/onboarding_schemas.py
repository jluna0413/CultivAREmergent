"""
Onboarding Schemas for FastAPI
Pydantic models for the user onboarding flow API endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import UUID


# --- Genetics ---
class GeneticItemCreate(BaseModel):
    """Schema for a genetic item collected during onboarding"""
    strain_name: str = Field(..., min_length=1, max_length=100, example="Blue Dream")
    breeder_name: str = Field(..., min_length=1, max_length=100, example="Humboldt Seed Co")
    type: Literal["seed", "clone"]
    packaging_image_url: Optional[str] = Field(None, max_length=500)


# --- Environment ---
class PotPosition(BaseModel):
    """Schema for a pot position in the tent layout"""
    id: str = Field(..., example="pot_1")
    pot_size_label: str = Field(..., example="5 Gal")
    pot_type: str = Field("fabric", example="air_pruning")
    x_position: float = Field(..., ge=0.0)
    y_position: float = Field(..., ge=0.0)


class EnvironmentConfigCreate(BaseModel):
    """Schema for environment configuration"""
    name: str = Field(..., min_length=1, max_length=100, example="My Main Tent")
    environment_type: Literal["tent", "greenhouse", "outdoors"]
    tent_width_inches: Optional[float] = Field(None, ge=0.0, example=48.0)
    tent_depth_inches: Optional[float] = Field(None, ge=0.0, example=48.0)
    pots: List[PotPosition] = []


# --- Hardware ---
class HardwareIntegrationCreate(BaseModel):
    """Schema for hardware integration"""
    manufacturer: Literal[
        "ac_infinity", "ecowitt", "vivosun", 
        "spider_farmer", "mars_hydro", "other"
    ]
    is_linked: bool = False
    linked_account_id: Optional[str] = Field(None, max_length=200)


# --- Master Payload ---
class OnboardingCompletionPayload(BaseModel):
    """
    Master schema for completing the onboarding flow.
    Contains all user setup data collected during onboarding.
    """
    user_id: UUID
    genetics: List[GeneticItemCreate] = Field(default_factory=list)
    environments: List[EnvironmentConfigCreate] = Field(default_factory=list)
    integrations: List[HardwareIntegrationCreate] = Field(default_factory=list)


class OnboardingStatusResponse(BaseModel):
    """Response schema for onboarding status"""
    is_completed: bool = False
    completed_at: Optional[str] = None
    genetics_count: int = 0
    environments_count: int = 0
    integrations_count: int = 0
