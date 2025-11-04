"""
Strain management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import Cultivar, Breeder, Plant, SystemActivity


async def get_all_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all strains/cultivars with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of strain data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).order_by(Cultivar.name)
        )
        strains = result.scalars().all()

        strain_list = []
        for strain in strains:
            # Get plant count for this strain
            plant_count_result = await session.execute(
                select(func.count(Plant.id)).where(Plant.cultivar_id == strain.id)
            )
            plant_count = plant_count_result.scalar() or 0

            strain_data = {
                "id": strain.id,
                "name": strain.name,
                "breeder": strain.breeder.name if strain.breeder else "",
                "breeder_id": strain.breeder_id,
                "indica": strain.indica,
                "sativa": strain.sativa,
                "autoflower": strain.autoflower,
                "description": strain.description or "",
                "short_description": strain.short_description or "",
                "seed_count": strain.seed_count,
                "cycle_time": strain.cycle_time,
                "url": strain.url or "",
                "plant_count": plant_count,
            }
            strain_list.append(strain_data)

        return strain_list
    except Exception as e:
        logger.error(f"Error getting all strains: {e}")
        return []


async def get_strain_by_id(strain_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific strain by ID - ASYNC VERSION.

    Args:
        strain_id (int): The ID of the strain.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: Strain data or None if not found.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == strain_id))
        strain = result.scalars().first()
        
        if not strain:
            return None

        # Get plant count for this strain
        plant_count_result = await session.execute(
            select(func.count(Plant.id)).where(Plant.cultivar_id == strain.id)
        )
        plant_count = plant_count_result.scalar() or 0

        strain_data = {
            "id": strain.id,
            "name": strain.name,
            "breeder": strain.breeder.name if strain.breeder else "",
            "breeder_id": strain.breeder_id,
            "indica": strain.indica,
            "sativa": strain.sativa,
            "autoflower": strain.autoflower,
            "description": strain.description or "",
            "short_description": strain.short_description or "",
            "seed_count": strain.seed_count,
            "cycle_time": strain.cycle_time,
            "url": strain.url or "",
            "plant_count": plant_count,
        }

        return strain_data
    except Exception as e:
        logger.error(f"Error getting strain by ID: {e}")
        return None


async def create_strain(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new strain - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Strain data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Check if strain name already exists
        existing_result = await session.execute(select(Cultivar).where(Cultivar.name == data.get("name")))
        existing = existing_result.scalars().first()
        if existing:
            return {"success": False, "error": "Strain name already exists"}

        # Create new strain
        new_strain = Cultivar(
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

        session.add(new_strain)
        await session.commit()
        await session.refresh(new_strain)

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="strain_created",
            details=f"Strain created: {new_strain.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "strain_id": new_strain.id,
            "message": f"Strain '{new_strain.name}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating strain: {e}")
        return {"success": False, "error": str(e)}


async def update_strain(strain_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing strain - ASYNC VERSION.

    Args:
        strain_id (int): The ID of the strain to update.
        data (Dict[str, Any]): Updated strain data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == strain_id))
        strain = result.scalars().first()
        
        if not strain:
            return {"success": False, "error": "Strain not found"}

        # Update fields
        strain.name = data.get("name", strain.name)
        strain.breeder_id = data.get("breeder_id", strain.breeder_id)
        strain.indica = data.get("indica", strain.indica)
        strain.sativa = data.get("sativa", strain.sativa)
        strain.autoflower = data.get("autoflower", strain.autoflower)
        strain.description = data.get("description", strain.description)
        strain.short_description = data.get("short_description", strain.short_description)
        strain.seed_count = data.get("seed_count", strain.seed_count)
        strain.cycle_time = data.get("cycle_time", strain.cycle_time)
        strain.url = data.get("url", strain.url)

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="strain_updated",
            details=f"Strain updated: {strain.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Strain '{strain.name}' updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating strain: {e}")
        return {"success": False, "error": str(e)}


async def delete_strain(strain_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a strain - ASYNC VERSION.

    Args:
        strain_id (int): The ID of the strain to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Cultivar).where(Cultivar.id == strain_id))
        strain = result.scalars().first()
        
        if not strain:
            return {"success": False, "error": "Strain not found"}

        # Check if strain has plants
        plant_count_result = await session.execute(
            select(func.count(Plant.id)).where(Plant.cultivar_id == strain_id)
        )
        plant_count = plant_count_result.scalar() or 0

        if plant_count > 0:
            return {
                "success": False, 
                "error": f"Cannot delete strain with {plant_count} associated plants"
            }

        strain_name = strain.name
        await session.delete(strain)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="strain_deleted",
            details=f"Strain deleted: {strain_name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": f"Strain '{strain_name}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting strain: {e}")
        return {"success": False, "error": str(e)}


async def get_in_stock_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get strains that are in stock (seed_count > 0) - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of in-stock strain data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).where(Cultivar.seed_count > 0).order_by(Cultivar.name)
        )
        strains = result.scalars().all()

        strain_list = []
        for strain in strains:
            strain_data = {
                "id": strain.id,
                "name": strain.name,
                "breeder": strain.breeder.name if strain.breeder else "",
                "seed_count": strain.seed_count,
                "autoflower": strain.autoflower,
                "description": strain.short_description or strain.description or "",
            }
            strain_list.append(strain_data)

        return strain_list
    except Exception as e:
        logger.error(f"Error getting in-stock strains: {e}")
        return []


async def get_out_of_stock_strains(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get strains that are out of stock (seed_count == 0) - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of out-of-stock strain data dictionaries.
    """
    try:
        result = await session.execute(
            select(Cultivar).where(Cultivar.seed_count == 0).order_by(Cultivar.name)
        )
        strains = result.scalars().all()

        strain_list = []
        for strain in strains:
            strain_data = {
                "id": strain.id,
                "name": strain.name,
                "breeder": strain.breeder.name if strain.breeder else "",
                "autoflower": strain.autoflower,
                "description": strain.short_description or strain.description or "",
            }
            strain_list.append(strain_data)

        return strain_list
    except Exception as e:
        logger.error(f"Error getting out-of-stock strains: {e}")
        return []


async def search_strains(query: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Search strains by name or breeder - ASYNC VERSION.

    Args:
        query (str): Search query.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of matching strain data dictionaries.
    """
    try:
        # Simple search by name and breeder (in a real app, you'd want full-text search)
        result = await session.execute(select(Cultivar))
        all_strains = result.scalars().all()

        matching_strains = []
        query_lower = query.lower()

        for strain in all_strains:
            strain_breeder = strain.breeder.name if strain.breeder else ""
            if (query_lower in strain.name.lower() or 
                query_lower in strain_breeder.lower() or
                (strain.description and query_lower in strain.description.lower())):
                
                strain_data = {
                    "id": strain.id,
                    "name": strain.name,
                    "breeder": strain_breeder,
                    "indica": strain.indica,
                    "sativa": strain.sativa,
                    "autoflower": strain.autoflower,
                    "description": strain.short_description or strain.description or "",
                }
                matching_strains.append(strain_data)

        return matching_strains
    except Exception as e:
        logger.error(f"Error searching strains: {e}")
        return []