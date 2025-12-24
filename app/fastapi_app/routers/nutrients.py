"""
Nutrients API Router
Endpoints for nutrient calculator, inventory, and feeding schedules.
"""

from typing import List, Optional, Dict
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.models_async.nutrients import (
    NutrientBrand,
    NutrientComponent,
    NutrientFormula,
    NutrientInventory,
    FeedingLog,
    WaterSource,
)
from app.models_async.base import get_async_session as get_async_db
from app.fastapi_app.dependencies import require_login
from app.models_async.auth import User
from app.services.nutrient_calculator import (
    NutrientCalculator,
    GrowthStage,
    GrowMedium,
    WaterType,
    FeedingStrength,
)
from app.logger import logger


router = APIRouter(prefix="/api/v2/nutrients", tags=["nutrients"])


# === Pydantic Models ===

class NutrientBrandResponse(BaseModel):
    id: int
    name: str
    manufacturer: Optional[str]
    brand_type: str
    component_count: int
    description: Optional[str]


class NutrientComponentResponse(BaseModel):
    id: int
    brand_id: int
    name: str
    npk_ratio: Optional[str]
    description: Optional[str]


class CalculatorRequest(BaseModel):
    brand_id: int
    growth_stage: str = Field(..., description="seedling, early_veg, late_veg, early_flower, etc.")
    medium: str = Field(..., description="hydro, coco, soil, inert")
    tank_size_liters: float = Field(..., gt=0, description="Reservoir size in liters")
    feeding_strength: str = Field(default="medium", description="light, medium, aggressive, custom")
    custom_strength: Optional[float] = Field(None, ge=0, le=2, description="Custom multiplier if feeding_strength=custom")
    water_type: str = Field(default="tap", description="tap, distilled, ro, re_mineralized")


class NutrientMixResponse(BaseModel):
    components: Dict[str, float]
    total_volume_liters: float
    ppm_target: tuple[float, float]
    ec_target: tuple[float, float]
    ph_target: tuple[float, float]
    mixing_instructions: List[str]
    requires_calmag: bool
    calmag_ml: Optional[float]
    inventory_sufficient: bool
    insufficient_items: List[str] = []
    estimated_cost: Optional[float] = None


class InventoryItemResponse(BaseModel):
    id: int
    component_id: int
    component_name: str
    quantity_ml: float
    original_quantity_ml: Optional[float]
    is_low_stock: bool
    percentage_remaining: Optional[float]
    purchase_date: Optional[str]
    expiry_date: Optional[str]


class AddInventoryRequest(BaseModel):
    component_id: int
    quantity_ml: float = Field(..., gt=0)
    original_quantity_ml: Optional[float] = None
    purchase_date: Optional[str] = None
    expiry_date: Optional[str] = None
    cost: Optional[float] = None
    low_stock_threshold: float = Field(default=100.0)


# === Endpoints ===

@router.get("/brands", response_model=List[NutrientBrandResponse])
async def list_nutrient_brands(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get all nutrient brands."""
    try:
        result = await db.execute(select(NutrientBrand).order_by(NutrientBrand.name))
        brands = result.scalars().all()
        
        return [
            NutrientBrandResponse(
                id=brand.id,
                name=brand.name,
                manufacturer=brand.manufacturer,
                brand_type=brand.brand_type,
                component_count=brand.component_count,
                description=brand.description,
            )
            for brand in brands
        ]
    except Exception as e:
        logger.error(f"Error fetching nutrient brands: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/brands/{brand_id}/components", response_model=List[NutrientComponentResponse])
async def get_brand_components(
    brand_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Get all components for a specific brand."""
    try:
        result = await db.execute(
            select(NutrientComponent)
            .where(NutrientComponent.brand_id == brand_id)
            .order_by(NutrientComponent.order_index)
        )
        components = result.scalars().all()
        
        return [
            NutrientComponentResponse(
                id=comp.id,
                brand_id=comp.brand_id,
                name=comp.name,
                npk_ratio=comp.npk_ratio,
                description=comp.description,
            )
            for comp in components
        ]
    except Exception as e:
        logger.error(f"Error fetching components for brand {brand_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calculate", response_model=NutrientMixResponse)
async def calculate_nutrient_mix(
    request: CalculatorRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Calculate nutrient mix based on parameters."""
    try:
        # Fetch formula for this brand/stage/medium
        result = await db.execute(
            select(NutrientFormula)
            .where(
                NutrientFormula.brand_id == request.brand_id,
                NutrientFormula.growth_stage == request.growth_stage,
                NutrientFormula.medium == request.medium,
            )
        )
        formula = result.scalar_one_or_none()
        
        if not formula:
            raise HTTPException(
                status_code=404,
                detail=f"No formula found for brand {request.brand_id}, stage {request.growth_stage}, medium {request.medium}",
            )

        # Get component names
        component_ids = list(formula.ratios.keys())
        component_result = await db.execute(
            select(NutrientComponent).where(NutrientComponent.id.in_(component_ids))
        )
        components = component_result.scalars().all()
        component_names = {comp.id: comp.name for comp in components}

        # Get user's inventory
        inventory_result = await db.execute(
            select(NutrientInventory)
            .where(
                NutrientInventory.user_id == current_user.id,
                NutrientInventory.component_id.in_(component_ids),
            )
        )
        inventory_items = inventory_result.scalars().all()
        inventory_dict = {inv.component.name: inv.quantity_ml for inv in inventory_items}
        inventory_full = {
            inv.component.name: {
                'quantity_ml': inv.quantity_ml,
                'cost': inv.cost,
                'original_quantity_ml': inv.original_quantity_ml,
            }
            for inv in inventory_items
        }

        # Calculate mix
        nutrient_mix = NutrientCalculator.calculate_mix(
            formula_ratios=formula.ratios,
            component_names=component_names,
            tank_size_liters=request.tank_size_liters,
            feeding_strength=FeedingStrength(request.feeding_strength),
            water_type=WaterType(request.water_type),
            ppm_range=(formula.ppm_target_min or 0, formula.ppm_target_max or 0),
            ec_range=(formula.ec_target_min or 0, formula.ec_target_max or 0),
            ph_range=(formula.ph_target_min or 5.5, formula.ph_target_max or 6.5),
            custom_strength=request.custom_strength,
        )

        # Check inventory sufficiency
        is_sufficient, insufficient = NutrientCalculator.check_inventory_sufficient(
            components=nutrient_mix.components,
            inventory=inventory_dict,
        )

        # Calculate cost
        estimated_cost = NutrientCalculator.calculate_ingredient_cost(
            components=nutrient_mix.components,
            inventory=inventory_full,
        )

        return NutrientMixResponse(
            components=nutrient_mix.components,
            total_volume_liters=nutrient_mix.total_volume_liters,
            ppm_target=nutrient_mix.ppm_target,
            ec_target=nutrient_mix.ec_target,
            ph_target=nutrient_mix.ph_target,
            mixing_instructions=nutrient_mix.mixing_instructions,
            requires_calmag=nutrient_mix.requires_calmag,
            calmag_ml=nutrient_mix.calmag_ml,
            inventory_sufficient=is_sufficient,
            insufficient_items=insufficient,
            estimated_cost=estimated_cost,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating nutrient mix: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/inventory", response_model=List[InventoryItemResponse])
async def get_nutrient_inventory(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
    low_stock_only: bool = Query(False, description="Show only low stock items"),
):
    """Get user's nutrient inventory."""
    try:
        query = select(NutrientInventory).where(NutrientInventory.user_id == current_user.id)
       
        if low_stock_only:
            query = query.where(NutrientInventory.quantity_ml <= NutrientInventory.low_stock_threshold)

        result = await db.execute(query.order_by(NutrientInventory.component_id))
        inventory_items = result.scalars().all()

        return [
            InventoryItemResponse(
                id=item.id,
                component_id=item.component_id,
                component_name=item.component.name,
                quantity_ml=item.quantity_ml,
                original_quantity_ml=item.original_quantity_ml,
                is_low_stock=item.is_low_stock,
                percentage_remaining=item.percentage_remaining,
                purchase_date=item.purchase_date.isoformat() if item.purchase_date else None,
                expiry_date=item.expiry_date.isoformat() if item.expiry_date else None,
            )
            for item in inventory_items
        ]

    except Exception as e:
        logger.error(f"Error fetching nutrient inventory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/inventory", response_model=Dict[str, str])
async def add_inventory_item(
    request: AddInventoryRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(require_login),
):
    """Add nutrient to inventory."""
    try:
        # Check if component exists
        comp_result = await db.execute(
            select(NutrientComponent).where(NutrientComponent.id == request.component_id)
        )
        component = comp_result.scalar_one_or_none()
        if not component:
            raise HTTPException(status_code=404, detail="Component not found")

        # Create inventory item
        inventory_item = NutrientInventory(
            user_id=current_user.id,
            component_id=request.component_id,
            quantity_ml=request.quantity_ml,
            original_quantity_ml=request.original_quantity_ml or request.quantity_ml,
            purchase_date=datetime.fromisoformat(request.purchase_date) if request.purchase_date else None,
            expiry_date=datetime.fromisoformat(request.expiry_date) if request.expiry_date else None,
            cost=request.cost,
            low_stock_threshold=request.low_stock_threshold,
        )

        db.add(inventory_item)
        await db.commit()

        return {"message": "Inventory item added successfully", "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error adding inventory item: {e}")
        raise HTTPException(status_code=500, detail=str(e))
