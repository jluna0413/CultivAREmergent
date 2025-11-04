"""
Clone management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import Plant, SystemActivity, get_async_session


async def get_clones(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all clones (plants with parent_plant_id) - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of clone data dictionaries.
    """
    try:
        # Get all plants that are clones (have a parent plant)
        result = await session.execute(
            select(Plant).where(Plant.parent_plant_id.isnot(None))
        )
        clones = result.scalars().all()

        clone_list = []
        for clone in clones:
            clone_data = {
                "id": clone.id,
                "name": clone.name,
                "description": clone.description,
                "status": clone.status.name if clone.status else "",
                "parent_name": clone.parent_plant.name if clone.parent_plant else "",
                "zone_name": clone.zone.name if clone.zone else "",
                "start_date": clone.start_date.strftime("%Y-%m-%d") if clone.start_date else "",
                "clone_date": clone.created_at.strftime("%Y-%m-%d %H:%M:%S") if clone.created_at else "",
                "current_week": getattr(clone, 'current_week', ''),
                "current_day": getattr(clone, 'current_day', ''),
            }
            clone_list.append(clone_data)

        return clone_list
    except Exception as e:
        logger.error(f"Error getting clones: {e}")
        return []


async def create_clone(parent_plant_id: int, clone_data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new clone from a parent plant - ASYNC VERSION.

    Args:
        parent_plant_id (int): ID of the parent plant to clone
        clone_data (Dict[str, Any]): Data for the new clone
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Get parent plant
        parent_result = await session.execute(select(Plant).where(Plant.id == parent_plant_id))
        parent_plant = parent_result.scalars().first()
        
        if not parent_plant:
            return {"success": False, "error": "Parent plant not found"}

        # Create new clone
        new_clone = Plant(
            name=clone_data.get("name"),
            description=clone_data.get("description", f"Clone of {parent_plant.name}"),
            parent_plant_id=parent_plant_id,
            cultivar_id=parent_plant.cultivar_id,
            zone_id=clone_data.get("zone_id"),
            status_id=1,  # Default to "Seedling" status
            start_date=clone_data.get("start_date") or datetime.now(),
            autoflower=getattr(parent_plant, 'autoflower', False)
        )

        session.add(new_clone)
        await session.commit()
        await session.refresh(new_clone)

        # Log system activity
        activity = SystemActivity(
            user_id=clone_data.get("user_id"),
            type="clone_created",
            details=f"Clone created from plant {parent_plant.name}: {new_clone.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "clone_id": new_clone.id,
            "message": f"Clone '{new_clone.name}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating clone: {e}")
        return {"success": False, "error": str(e)}


async def get_clone_statistics(session: AsyncSession) -> Dict[str, int]:
    """
    Get clone-related statistics - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        Dict[str, int]: Clone statistics.
    """
    try:
        # Get total clones
        clones_result = await session.execute(
            select(Plant).where(Plant.parent_plant_id.isnot(None))
        )
        total_clones = len(clones_result.scalars().all())

        # Get clones by status
        all_plants_result = await session.execute(select(Plant))
        all_plants = all_plants_result.scalars().all()

        clone_stats = {
            "total_clones": total_clones,
            "active_clones": 0,
            "harvested_clones": 0,
        }

        for plant in all_plants:
            if plant.parent_plant_id:
                if plant.status and plant.status.name == "Harvested":
                    clone_stats["harvested_clones"] += 1
                else:
                    clone_stats["active_clones"] += 1

        return clone_stats
    except Exception as e:
        logger.error(f"Error getting clone statistics: {e}")
        return {
            "total_clones": 0,
            "active_clones": 0,
            "harvested_clones": 0,
        }


async def delete_clone(clone_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a clone - ASYNC VERSION.

    Args:
        clone_id (int): ID of the clone to delete
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Get clone
        clone_result = await session.execute(select(Plant).where(Plant.id == clone_id))
        clone = clone_result.scalars().first()
        
        if not clone:
            return {"success": False, "error": "Clone not found"}

        if not clone.parent_plant_id:
            return {"success": False, "error": "Plant is not a clone"}

        clone_name = clone.name
        await session.delete(clone)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="clone_deleted",
            details=f"Clone deleted: {clone_name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": f"Clone '{clone_name}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting clone: {e}")
        return {"success": False, "error": str(e)}


async def get_parent_plants(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all plants that can be used as parents for cloning - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of parent plant data dictionaries.
    """
    try:
        # Get plants that are not clones themselves
        result = await session.execute(
            select(Plant).where(Plant.parent_plant_id.is_(None))
        )
        parent_plants = result.scalars().all()

        parent_list = []
        for plant in parent_plants:
            parent_data = {
                "id": plant.id,
                "name": plant.name,
                "description": plant.description,
                "status": plant.status.name if plant.status else "",
                "strain": plant.cultivar.name if plant.cultivar else "",
                "zone": plant.zone.name if plant.zone else "",
                "clone_count": 0,  # Would need a separate query to count clones
            }
            parent_list.append(parent_data)

        return parent_list
    except Exception as e:
        logger.error(f"Error getting parent plants: {e}")
        return []