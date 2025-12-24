"""
Async breeder handlers for the CultivAR application.
"""

from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.grow import Breeder, Cultivar
from app.handlers_async import activity_handlers


async def get_breeders_async(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all breeders sorted alphabetically by name.
    """
    try:
        stmt = select(Breeder).order_by(Breeder.name)
        result = await session.execute(stmt)
        breeders = result.scalars().all()

        breeder_list = []
        for breeder in breeders:
            breeder_data = {
                "id": breeder.id,
                "name": breeder.name,
                "country": breeder.country,
                "website": breeder.website,
                "seedfinder_id": breeder.seedfinder_id,
                "description": breeder.description,
            }
            breeder_list.append(breeder_data)
        return breeder_list
    except Exception as e:
        logger.error(f"Error getting breeders: {e}")
        return []


async def add_breeder_async(session: AsyncSession, data: Dict[str, Any], user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Add a new breeder.
    """
    try:
        name = data.get("name")
        if not name:
            return {"success": False, "error": "Breeder name is required"}

        existing_breeder_res = await session.execute(select(Breeder).where(Breeder.name == name))
        if existing_breeder_res.scalar_one_or_none():
            return {"success": False, "error": "Breeder with this name already exists"}

        new_breeder = Breeder(
            name=name,
            country=data.get("country"),
            website=data.get("website"),
            seedfinder_id=data.get("seedfinder_id"),
            description=data.get("description"),
        )
        session.add(new_breeder)
        await session.commit()
        await session.refresh(new_breeder)

        await activity_handlers.record_activity_log(
            session,
            user_id=user_id,
            activity_type_name="breeder_added",
            activity_category="system",
            title="Breeder Added",
            description=f"Breeder added: {new_breeder.name}",
            entity_type="breeder",
            entity_id=new_breeder.id,
            entity_name=new_breeder.name,
            details={"added_by": user_id}
        )

        return {"success": True, "breeder_id": new_breeder.id, "name": new_breeder.name, "message": f"Breeder {new_breeder.name} added successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error adding breeder: {e}")
        return {"success": False, "error": str(e)}


async def update_breeder_async(session: AsyncSession, breeder_id: int, data: Dict[str, Any], user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Update a breeder.
    """
    try:
        breeder = await session.get(Breeder, breeder_id)
        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        new_name = data.get("name")
        if new_name and new_name != breeder.name:
            existing_breeder_res = await session.execute(select(Breeder).where(Breeder.name == new_name))
            if existing_breeder_res.scalar_one_or_none():
                return {"success": False, "error": "Breeder with this name already exists"}
            breeder.name = new_name
        
        breeder.country = data.get("country", breeder.country)
        breeder.website = data.get("website", breeder.website)
        breeder.seedfinder_id = data.get("seedfinder_id", breeder.seedfinder_id)
        breeder.description = data.get("description", breeder.description)

        await session.commit()

        await activity_handlers.record_activity_log(
            session,
            user_id=user_id,
            activity_type_name="breeder_updated",
            activity_category="system",
            title="Breeder Updated",
            description=f"Breeder updated: {breeder.name}",
            entity_type="breeder",
            entity_id=breeder.id,
            entity_name=breeder.name,
            details={"updated_by": user_id}
        )

        return {"success": True, "breeder_id": breeder.id, "message": f"Breeder {breeder.name} updated successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating breeder: {e}")
        return {"success": False, "error": str(e)}


async def delete_breeder_async(session: AsyncSession, breeder_id: int, user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Delete a breeder.
    """
    try:
        breeder = await session.get(Breeder, breeder_id, options=[selectinload(Breeder.cultivars)])
        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        if breeder.cultivars:
            return {"success": False, "error": f"Cannot delete breeder: {len(breeder.cultivars)} strains are using this breeder"}

        breeder_name = breeder.name
        await session.delete(breeder)
        await session.commit()

        await activity_handlers.record_activity_log(
            session,
            user_id=user_id,
            activity_type_name="breeder_deleted",
            activity_category="system",
            title="Breeder Deleted",
            description=f"Breeder deleted: {breeder_name}",
            entity_type="breeder",
            entity_id=breeder_id,
            entity_name=breeder_name,
            details={"deleted_by": user_id}
        )

        return {"success": True, "message": f"Breeder {breeder_name} deleted successfully."}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting breeder: {e}")
        return {"success": False, "error": str(e)}
