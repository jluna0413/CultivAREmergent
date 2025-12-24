"""
Async clone management handlers for the CultivAR application.
"""

from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload

from app.logger import logger
from app.models_async.grow import Plant, Cultivar, Status, Zone
from app.models_async.activities import ActivityLog, ActivityType, PlantActivity
from app.handlers_async import activity_handlers

async def get_available_parent_plants_async(session: AsyncSession, user_id: int) -> Dict[str, Any]:
    """
    Get all plants for a user that can be used as parents for cloning.
    Only living plants (not harvested or dead) can be parent plants.
    """
    try:
        stmt = (
            select(Plant)
            .where(Plant.user_id == user_id, Plant.status_id.in_([1, 2, 3]))  # Filter by user_id and living plants
            .options(
                selectinload(Plant.cultivar).selectinload(Cultivar.breeder),
                selectinload(Plant.status),
                selectinload(Plant.zone),
                selectinload(Plant.parent),
            )
        )
        result = await session.execute(stmt)
        available_parents = result.scalars().all()

        parent_list = []
        for plant in available_parents:
            clone_count_res = await session.execute(
                select(func.count(Plant.id)).where(Plant.parent_id == plant.id)
            )
            clone_count = clone_count_res.scalar_one()

            parent_data = {
                "id": plant.id,
                "name": plant.name,
                "strain_name": plant.cultivar.name if plant.cultivar else "N/A",
                "breeder_name": plant.cultivar.breeder.name if plant.cultivar and plant.cultivar.breeder else "N/A",
                "status": plant.status.name if plant.status else "N/A",
                "current_week": (datetime.now(timezone.utc) - plant.start_dt).days // 7 if plant.start_dt else 0,
                "current_day": (datetime.now(timezone.utc) - plant.start_dt).days % 7 if plant.start_dt else 0,
                "description": plant.description,
                "start_date": plant.start_dt.strftime("%Y-%m-%d") if plant.start_dt else None,
                "clone_count": clone_count,
                "zone_name": plant.zone.name if plant.zone else "N/A",
                "is_clone": plant.is_clone,
                "parent_name": plant.parent.name if plant.parent else None,
            }
            parent_list.append(parent_data)

        return {"parents": parent_list}
    except Exception as e:
        logger.error(f"Error getting available parent plants: {e}")
        return {"parents": []}


async def create_clones_async(session: AsyncSession, parent_id: int, clone_data_list: List[Dict[str, Any]], user_id: int) -> Dict[str, Any]:
    """
    Create multiple clones from a parent plant.
    """
    try:
        parent_plant_res = await session.execute(select(Plant).where(Plant.id == parent_id, Plant.user_id == user_id))
        parent_plant = parent_plant_res.scalar_one_or_none()
        if not parent_plant:
            return {"success": False, "error": "Parent plant not found or access denied"}

        if parent_plant.status_id in [4, 5]:  # Harvested or Dead
            return {"success": False, "error": "Cannot clone from harvested or dead plants"}

        created_clones = []
        errors = []

        for i, clone_data in enumerate(clone_data_list):
            try:
                clone_name = clone_data.get("name", f"{parent_plant.name} - Clone {i+1}")
                description = clone_data.get("description", f"Clone from {parent_plant.name}")
                zone_id = clone_data.get("zone_id", parent_plant.zone_id)
                start_date_str = clone_data.get("start_date")

                start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else datetime.now(timezone.utc)

                clone = Plant(
                    name=clone_name,
                    description=description,
                    cultivar_id=parent_plant.cultivar_id,
                    zone_id=zone_id,
                    status_id=1,
                    is_clone=True,
                    parent_id=parent_id,
                    start_dt=start_date,
                    user_id=user_id
                )

                session.add(clone)
                await session.flush()

                await activity_handlers.record_plant_activity(
                    session,
                    plant_id=clone.id,
                    activity_name="Clone Created",
                    note=f"Clone created from parent plant: {parent_plant.name}",
                    user_id=user_id
                )

                created_clones.append({"id": clone.id, "name": clone.name})

            except Exception as e:
                errors.append(f"Clone {i+1}: {str(e)}")
                continue

        if created_clones:
            await session.commit()
            await activity_handlers.record_activity_log(
                session,
                user_id=user_id,
                activity_type_name="clones_created",
                activity_category="system",
                title="Clones Created",
                description=f"{len(created_clones)} clones created from {parent_plant.name}",
                entity_type="plant",
                entity_id=parent_plant.id,
                entity_name=parent_plant.name,
                details={"parent_plant_id": parent_plant.id, "clones_count": len(created_clones)}
            )

            result = {
                "success": True,
                "created_clones": created_clones,
                "message": f"Successfully created {len(created_clones)} clones from {parent_plant.name}",
            }
            if errors:
                result["errors"] = errors
            return result
        else:
            await session.rollback()
            return {"success": False, "error": "Failed to create any clones", "errors": errors}

    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating clones: {e}")
        return {"success": False, "error": str(e)}


async def get_clone_lineage_async(session: AsyncSession, plant_id: int, user_id: int) -> Dict[str, Any]:
    """
    Get the complete clone lineage for a plant (parents and children) for a specific user.
    """
    try:
        plant_res = await session.execute(select(Plant).where(Plant.id == plant_id, Plant.user_id == user_id))
        plant = plant_res.scalar_one_or_none()

        if not plant:
            return {"success": False, "error": "Plant not found or access denied"}

        lineage = {"plant": {"id": plant.id, "name": plant.name}, "parent": None, "children": [], "siblings": []}

        # Recursively find ancestors
        current = plant
        while current and current.parent_id:
            parent_res = await session.execute(select(Plant).where(Plant.id == current.parent_id, Plant.user_id == user_id))
            parent = parent_res.scalar_one_or_none()
            if not parent: break
            
            parent_node = lineage["parent"]
            if not parent_node:
                lineage["parent"] = {"id": parent.id, "name": parent.name, "parent": None}
                parent_node = lineage["parent"]
            else:
                # This logic is a bit complex for deep trees, simplifying for now
                pass
            current = parent

        # Find direct children
        children_res = await session.execute(select(Plant).where(Plant.parent_id == plant.id, Plant.user_id == user_id))
        children = children_res.scalars().all()
        lineage["children"] = [{"id": child.id, "name": child.name} for child in children]

        # Find siblings
        if plant.parent_id:
            siblings_res = await session.execute(select(Plant).where(Plant.parent_id == plant.parent_id, Plant.id != plant.id, Plant.user_id == user_id))
            siblings = siblings_res.scalars().all()
            lineage["siblings"] = [{"id": sibling.id, "name": sibling.name} for sibling in siblings]

        return {"success": True, "lineage": lineage}

    except Exception as e:
        logger.error(f"Error getting clone lineage: {e}")
        return {"success": False, "error": str(e)}


async def get_clone_statistics_async(session: AsyncSession, user_id: int) -> Dict[str, Any]:
    """
    Get clone statistics and success rates for a specific user.
    """
    try:
        total_clones_res = await session.execute(select(func.count(Plant.id)).where(Plant.is_clone == True, Plant.user_id == user_id))
        total_clones = total_clones_res.scalar_one()

        successful_clones_res = await session.execute(select(func.count(Plant.id)).where(Plant.is_clone == True, Plant.status_id != 5, Plant.user_id == user_id))
        successful_clones = successful_clones_res.scalar_one()

        failed_clones = total_clones - successful_clones

        success_rate = round((successful_clones / total_clones) * 100, 1) if total_clones > 0 else 0

        stats = {
            "total_clones": total_clones,
            "successful_clones": successful_clones,
            "failed_clones": failed_clones,
            "success_rate": success_rate,
        }
        return {"stats": stats}

    except Exception as e:
        logger.error(f"Error getting clone statistics: {e}")
        return {"stats": {"total_clones": 0, "successful_clones": 0, "failed_clones": 0, "success_rate": 0}}


async def get_all_clones_async(session: AsyncSession, user_id: int) -> Dict[str, Any]:
    """
    Get all clone plants with their parent information for a specific user.
    """
    try:
        stmt = (
            select(Plant)
            .where(Plant.is_clone == True, Plant.user_id == user_id)
            .options(selectinload(Plant.cultivar), selectinload(Plant.parent), selectinload(Plant.status), selectinload(Plant.zone))
        )
        result = await session.execute(stmt)
        clones = result.scalars().all()

        clone_list = []
        for clone in clones:
            clone_data = {
                "id": clone.id,
                "name": clone.name,
                "description": clone.description,
                "strain_name": clone.cultivar.name if clone.cultivar else "N/A",
                "parent_name": clone.parent.name if clone.parent else "N/A",
                "parent_id": clone.parent_id,
                "status": clone.status.name if clone.status else "N/A",
                "start_date": clone.start_dt.strftime("%Y-%m-%d") if clone.start_dt else None,
                "zone_name": clone.zone.name if clone.zone else "N/A",
                "days_alive": (datetime.now(timezone.utc) - clone.start_dt).days if clone.start_dt else 0,
            }
            clone_list.append(clone_data)

        return {"clones": clone_list}

    except Exception as e:
        logger.error(f"Error getting all clones: {e}")
        return {"clones": []}


async def delete_clone_async(session: AsyncSession, clone_id: int, user_id: int) -> Dict[str, Any]:
    """
    Delete a clone plant for a specific user.
    """
    try:
        clone_res = await session.execute(select(Plant).where(Plant.id == clone_id, Plant.user_id == user_id))
        clone = clone_res.scalar_one_or_none()
        if not clone:
            return {"success": False, "error": "Clone not found or access denied"}

        if not clone.is_clone:
            return {"success": False, "error": "Plant is not a clone"}

        clone_name = clone.name
        await session.delete(clone)
        
        await activity_handlers.record_activity_log(
            session,
            user_id=user_id,
            activity_type_name="clone_deleted",
            activity_category="plant",
            title="Clone Deleted",
            description=f"Clone deleted: {clone_name}",
            entity_type="plant",
            entity_id=clone_id,
            entity_name=clone_name,
            details={"clone_id": clone_id, "deleted_by": user_id}
        )
        await session.commit()

        return {"success": True, "message": f"Clone {clone_name} deleted successfully"}

    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting clone: {e}")
        return {"success": False, "error": str(e)}
