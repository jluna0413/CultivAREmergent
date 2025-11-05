"""
Cultivar management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import Cultivar, Breeder, Plant, SystemActivity


async def get_all_cultivars(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all cultivars with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of cultivar data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).order_by(Cultivar.name)
        )
        cultivars = result.scalars().all()

        cultivar_list = []
        for cultivar in cultivars:
            # Get plant count for this cultivar
            plant_count_result = await session.execute(
                select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar.id)
            )
            plant_count = plant_count_result.scalar() or 0

            cultivar_data = {
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder.name if cultivar.breeder else "",
                "breeder_id": cultivar.breeder_id,
                "indica": cultivar.indica,
                "sativa": cultivar.sativa,
                "autoflower": cultivar.autoflower,
                "description": cultivar.description or "",
                "short_description": cultivar.short_description or "",
                "seed_count": cultivar.seed_count,
                "cycle_time": cultivar.cycle_time,
                "url": cultivar.url or "",
                "plant_count": plant_count,
            }
            cultivar_list.append(cultivar_data)

        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting all cultivars: {e}")
        return []


async def get_cultivar_by_id(cultivar_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific cultivar by ID - ASYNC VERSION.

    Args:
        cultivar_id (int): The ID of the cultivar.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: Cultivar data or None if not found.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == cultivar_id))
        cultivar = result.scalars().first()
        
        if not cultivar:
            return None

        # Get plant count for this cultivar
        plant_count_result = await session.execute(
            select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar.id)
        )
        plant_count = plant_count_result.scalar() or 0

        cultivar_data = {
            "id": cultivar.id,
            "name": cultivar.name,
            "breeder": cultivar.breeder.name if cultivar.breeder else "",
            "breeder_id": cultivar.breeder_id,
            "indica": cultivar.indica,
            "sativa": cultivar.sativa,
            "autoflower": cultivar.autoflower,
            "description": cultivar.description or "",
            "short_description": cultivar.short_description or "",
            "seed_count": cultivar.seed_count,
            "cycle_time": cultivar.cycle_time,
            "url": cultivar.url or "",
            "plant_count": plant_count,
        }

        return cultivar_data
    except Exception as e:
        logger.error(f"Error getting cultivar by ID: {e}")
        return None


async def create_cultivar(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new cultivar - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Cultivar data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Check if cultivar name already exists
        existing_result = await session.execute(select(Cultivar).where(Cultivar.name == data.get("name")))
        existing = existing_result.scalars().first()
        if existing:
            return {"success": False, "error": "Cultivar name already exists"}

        # Create new cultivar
        new_cultivar = Cultivar(
            name=data.get("name"),
            breeder_id=data.get("breeder_id"),
            indica=data.get("indica", 0),
            sativa=data.get("sativa", 0),
            autoflower=data.get("autoflower", False),
            description=data.get("description"),
            short_description=data.get("short_description"),
            seed_count=data.get("seed_count", 0),
            cycle_time=data.get("cycle_time"),
            url=data.get("url"),
        )

        session.add(new_cultivar)
        await session.commit()
        await session.refresh(new_cultivar)

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="cultivar_created",
            details=f"Cultivar created: {new_cultivar.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "cultivar_id": new_cultivar.id,
            "message": f"Cultivar '{new_cultivar.name}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating cultivar: {e}")
        return {"success": False, "error": str(e)}


async def update_cultivar(cultivar_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing cultivar - ASYNC VERSION.

    Args:
        cultivar_id (int): The ID of the cultivar to update.
        data (Dict[str, Any]): Updated cultivar data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == cultivar_id))
        cultivar = result.scalars().first()
        
        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        # Update fields
        cultivar.name = data.get("name", cultivar.name)
        cultivar.breeder_id = data.get("breeder_id", cultivar.breeder_id)
        cultivar.indica = data.get("indica", cultivar.indica)
        cultivar.sativa = data.get("sativa", cultivar.sativa)
        cultivar.autoflower = data.get("autoflower", cultivar.autoflower)
        cultivar.description = data.get("description", cultivar.description)
        cultivar.short_description = data.get("short_description", cultivar.short_description)
        cultivar.seed_count = data.get("seed_count", cultivar.seed_count)
        cultivar.cycle_time = data.get("cycle_time", cultivar.cycle_time)
        cultivar.url = data.get("url", cultivar.url)

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="cultivar_updated",
            details=f"Cultivar updated: {cultivar.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Cultivar '{cultivar.name}' updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating cultivar: {e}")
        return {"success": False, "error": str(e)}


async def delete_cultivar(cultivar_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a cultivar - ASYNC VERSION.

    Args:
        cultivar_id (int): The ID of the cultivar to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == cultivar_id))
        cultivar = result.scalars().first()
        
        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        # Check if cultivar has plants
        plant_count_result = await session.execute(
            select(func.count(Plant.id)).where(Plant.cultivar_id == cultivar_id)
        )
        plant_count = plant_count_result.scalar() or 0

        if plant_count > 0:
            return {
                "success": False, 
                "error": f"Cannot delete cultivar with {plant_count} associated plants"
            }

        cultivar_name = cultivar.name
        await session.delete(cultivar)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="cultivar_deleted",
            details=f"Cultivar deleted: {cultivar_name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": f"Cultivar '{cultivar_name}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting cultivar: {e}")
        return {"success": False, "error": str(e)}


async def get_in_stock_cultivars(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get cultivars that are in stock (seed_count > 0) - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of in-stock cultivar data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).where(Cultivar.seed_count > 0).order_by(Cultivar.name)
        )
        cultivars = result.scalars().all()

        cultivar_list = []
        for cultivar in cultivars:
            cultivar_data = {
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder.name if cultivar.breeder else "",
                "seed_count": cultivar.seed_count,
                "autoflower": cultivar.autoflower,
                "description": cultivar.short_description or cultivar.description or "",
            }
            cultivar_list.append(cultivar_data)

        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting in-stock cultivars: {e}")
        return []


async def get_out_of_stock_cultivars(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get cultivars that are out of stock (seed_count == 0) - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of out-of-stock cultivar data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).where(Cultivar.seed_count == 0).order_by(Cultivar.name)
        )
        cultivars = result.scalars().all()

        cultivar_list = []
        for cultivar in cultivars:
            cultivar_data = {
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder.name if cultivar.breeder else "",
                "autoflower": cultivar.autoflower,
                "description": cultivar.short_description or cultivar.description or "",
            }
            cultivar_list.append(cultivar_data)

        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting out-of-stock cultivars: {e}")
        return []


async def search_cultivars(query: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Search cultivars by name or breeder - ASYNC VERSION.

    Args:
        query (str): Search query.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of matching cultivar data dictionaries.
    """
    try:
        # Simple search by name and breeder (in a real app, you'd want full-text search)
        result = await session.execute(select(Cultivar))
        all_cultivars = result.scalars().all()

        matching_cultivars = []
        query_lower = query.lower()

        for cultivar in all_cultivars:
            cultivar_breeder = cultivar.breeder.name if cultivar.breeder else ""
            if (query_lower in cultivar.name.lower() or 
                query_lower in cultivar_breeder.lower() or
                (cultivar.description and query_lower in cultivar.description.lower())):
                
                cultivar_data = {
                    "id": cultivar.id,
                    "name": cultivar.name,
                    "breeder": cultivar_breeder,
                    "indica": cultivar.indica,
                    "sativa": cultivar.sativa,
                    "autoflower": cultivar.autoflower,
                    "description": cultivar.short_description or cultivar.description or "",
                }
                matching_cultivars.append(cultivar_data)

        return matching_cultivars
    except Exception as e:
        logger.error(f"Error searching cultivars: {e}")
        return []


# Backward compatibility aliases
async def get_all_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """Legacy alias for get_all_cultivars"""
    return await get_all_cultivars(session)


async def get_strain_by_id(strain_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """Legacy alias for get_cultivar_by_id"""
    return await get_cultivar_by_id(strain_id, session)


async def create_strain(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """Legacy alias for create_cultivar"""
    return await create_cultivar(data, session)


async def update_strain(strain_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """Legacy alias for update_cultivar"""
    return await update_cultivar(strain_id, data, session)


async def delete_strain(strain_id: int, session: AsyncSession) -> Dict[str, Any]:
    """Legacy alias for delete_cultivar"""
    return await delete_cultivar(strain_id, session)


async def get_in_stock_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """Legacy alias for get_in_stock_cultivars"""
    return await get_in_stock_cultivars(session)


async def get_out_of_stock_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """Legacy alias for get_out_of_stock_cultivars"""
    return await get_out_of_stock_cultivars(session)


async def search_strains(query: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """Legacy alias for search_cultivars"""
    return await search_cultivars(query, session)