"""
Async strain handlers for the CultivAR application.
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.grow import Cultivar, Plant
from app.handlers_async import activity_handlers

async def get_cultivar_async(session: AsyncSession, cultivar_id: int):
    """
    Get a cultivar by ID.
    """
    try:
        stmt = select(Cultivar).where(Cultivar.id == cultivar_id).options(selectinload(Cultivar.breeder))
        result = await session.execute(stmt)
        cultivar = result.scalar_one_or_none()

        if not cultivar:
            return None

        plant_count_res = await session.execute(select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar_id))
        plant_count = plant_count_res.scalar_one()

        return {
            "id": cultivar.id,
            "name": cultivar.name,
            "breeder": cultivar.breeder.name if cultivar.breeder else None,
            "breeder_id": cultivar.breeder_id,
            "indica": cultivar.indica,
            "sativa": cultivar.sativa,
            "autoflower": cultivar.autoflower,
            "description": cultivar.description,
            "seed_count": cultivar.seed_count,
            "cycle_time": cultivar.cycle_time,
            "url": cultivar.url,
            "parent_1": cultivar.parent_1,
            "parent_2": cultivar.parent_2,
            "lineage_json": cultivar.lineage_json,
            "seedfinder_id": cultivar.seedfinder_id,
            "thc_content": cultivar.thc_content,
            "cbd_content": cultivar.cbd_content,
            "flowering_type": cultivar.flowering_type,
            "categories": cultivar.categories,
            "plant_count": plant_count,
        }
    except Exception as e:
        logger.error(f"Error getting cultivar: {e}")
        return None

async def get_cultivars_async(session: AsyncSession, in_stock: bool = True):
    """
    Get all cultivars based on stock status.
    """
    try:
        if in_stock:
            stmt = select(Cultivar).where(Cultivar.seed_count > 0).options(selectinload(Cultivar.breeder))
        else:
            stmt = select(Cultivar).where(Cultivar.seed_count == 0).options(selectinload(Cultivar.breeder))
        
        result = await session.execute(stmt)
        cultivars = result.scalars().all()

        cultivar_list = []
        for cultivar in cultivars:
            plant_count_res = await session.execute(select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar.id))
            plant_count = plant_count_res.scalar_one()
            cultivar_list.append({
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder.name if cultivar.breeder else None,
                "seed_count": cultivar.seed_count,
                "plant_count": plant_count,
                "indica": cultivar.indica,
                "sativa": cultivar.sativa,
                "autoflower": cultivar.autoflower,
                "description": cultivar.description,
                "cycle_time": cultivar.cycle_time,
                "url": cultivar.url,
                "parent_1": cultivar.parent_1,
                "parent_2": cultivar.parent_2,
                "lineage_json": cultivar.lineage_json,
                "seedfinder_id": cultivar.seedfinder_id,
                "thc_content": cultivar.thc_content,
                "cbd_content": cultivar.cbd_content,
                "flowering_type": cultivar.flowering_type,
                "categories": cultivar.categories,
            })
        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting cultivars: {e}")
        return []

async def add_cultivar_async(session: AsyncSession, data: dict, admin_user_id: Optional[int] = None):
    """
    Add a new cultivar.
    """
    try:
        new_cultivar = Cultivar(
            name=data.get("name"),
            breeder_id=data.get("breeder_id"),
            indica=data.get("indica", 0),
            sativa=data.get("sativa", 0),
            autoflower=data.get("autoflower", False),
            description=data.get("description"),
            seed_count=data.get("seed_count", 0),
            cycle_time=data.get("cycle_time"),
            url=data.get("url"),
            parent_1=data.get("parent_1"),
            parent_2=data.get("parent_2"),
            lineage_json=data.get("lineage_json"),
            seedfinder_id=data.get("seedfinder_id"),
            thc_content=data.get("thc_content"),
            cbd_content=data.get("cbd_content"),
            flowering_type=data.get("flowering_type"),
            categories=data.get("categories"),
        )
        session.add(new_cultivar)
        await session.commit()
        await session.refresh(new_cultivar)

        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="cultivar_added",
            activity_category="system",
            title="Cultivar Added",
            description=f"Cultivar added: {new_cultivar.name}",
            entity_type="cultivar",
            entity_id=new_cultivar.id,
            entity_name=new_cultivar.name,
            details={"added_by": admin_user_id}
        )

        return {"success": True, "cultivar_id": new_cultivar.id, "message": f"Cultivar {new_cultivar.name} added successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error adding cultivar: {e}")
        return {"success": False, "error": str(e)}

async def update_cultivar_async(session: AsyncSession, cultivar_id: int, data: dict, admin_user_id: Optional[int] = None):
    """
    Update a cultivar.
    """
    try:
        cultivar = await session.get(Cultivar, cultivar_id)
        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        for key, value in data.items():
            if hasattr(cultivar, key):
                setattr(cultivar, key, value)
        
        await session.commit()

        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="cultivar_updated",
            activity_category="system",
            title="Cultivar Updated",
            description=f"Cultivar updated: {cultivar.name}",
            entity_type="cultivar",
            entity_id=cultivar.id,
            entity_name=cultivar.name,
            details={"updated_by": admin_user_id}
        )

        return {"success": True, "cultivar_id": cultivar.id, "message": f"Cultivar {cultivar.name} updated successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating cultivar: {e}")
        return {"success": False, "error": str(e)}

async def delete_cultivar_async(session: AsyncSession, cultivar_id: int, admin_user_id: Optional[int] = None):
    """
    Delete a cultivar.
    """
    try:
        cultivar = await session.get(Cultivar, cultivar_id)
        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        plant_count_res = await session.execute(select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar_id))
        if plant_count_res.scalar_one() > 0:
            return {"success": False, "error": "Cannot delete cultivar: it is in use by plants"}

        cultivar_name = cultivar.name
        await session.delete(cultivar)
        await session.commit()

        await activity_handlers.record_activity_log(
            session,
            user_id=admin_user_id,
            activity_type_name="cultivar_deleted",
            activity_category="system",
            title="Cultivar Deleted",
            description=f"Cultivar deleted: {cultivar_name}",
            entity_type="cultivar",
            entity_id=cultivar_id,
            entity_name=cultivar_name,
            details={"deleted_by": admin_user_id}
        )

        return {"success": True, "message": f"Cultivar {cultivar_name} deleted successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting cultivar: {e}")
        return {"success": False, "error": str(e)}
