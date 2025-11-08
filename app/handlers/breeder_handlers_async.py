from sqlalchemy import select, and_, or_, func, desc

"""
Breeder management handlers for the CultivAR application - ASYNC VERSION.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.models_async import Breeder, SystemActivity


async def get_all_breeders(session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Get all breeders with their details - ASYNC VERSION.

    Args:
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of breeder data dictionaries.
    """
    try:
        result = await session.execute(select(Breeder))
        breeders = result.scalars().all()

        breeder_list = []
        for breeder in breeders:
            breeder_data = {
                "id": breeder.id,
                "name": breeder.name,
            }
            breeder_list.append(breeder_data)

        return breeder_list
    except Exception as e:
        logger.error(f"Error getting all breeders: {e}")
        return []


async def get_breeder_by_id(breeder_id: int, session: AsyncSession) -> Optional[Dict[str, Any]]:
    """
    Get a specific breeder by ID - ASYNC VERSION.

    Args:
        breeder_id (int): The ID of the breeder.
        session: AsyncSession for database operations

    Returns:
        Optional[Dict[str, Any]]: Breeder data or None if not found.
    """
    try:
        result = await session.execute(select(Breeder).where(Breeder.id == breeder_id))
        breeder = result.scalars().first()
        
        if not breeder:
            return None

        breeder_data = {
            "id": breeder.id,
            "name": breeder.name,
        }

        return breeder_data
    except Exception as e:
        logger.error(f"Error getting breeder by ID: {e}")
        return None


async def create_breeder(data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Create a new breeder - ASYNC VERSION.

    Args:
        data (Dict[str, Any]): Breeder data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        # Check if breeder name already exists
        existing_result = await session.execute(select(Breeder).where(Breeder.name == data.get("name")))
        existing = existing_result.scalars().first()
        if existing:
            return {"success": False, "error": "Breeder name already exists"}

        # Create new breeder
        new_breeder = Breeder(
            name=data.get("name"),
            description=data.get("description", ""),
        )

        # Add optional fields if they exist
        if hasattr(Breeder, 'website') and data.get("website"):
            new_breeder.website = data.get("website")
        if hasattr(Breeder, 'contact_info') and data.get("contact_info"):
            new_breeder.contact_info = data.get("contact_info")

        session.add(new_breeder)
        await session.commit()
        await session.refresh(new_breeder)

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="breeder_created",
            details=f"Breeder created: {new_breeder.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "breeder_id": new_breeder.id,
            "message": f"Breeder '{new_breeder.name}' created successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error creating breeder: {e}")
        return {"success": False, "error": str(e)}


async def update_breeder(breeder_id: int, data: Dict[str, Any], session: AsyncSession) -> Dict[str, Any]:
    """
    Update an existing breeder - ASYNC VERSION.

    Args:
        breeder_id (int): The ID of the breeder to update.
        data (Dict[str, Any]): Updated breeder data.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Breeder).where(Breeder.id == breeder_id))
        breeder = result.scalars().first()
        
        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        # Update fields
        breeder.name = data.get("name", breeder.name)
        breeder.description = data.get("description", breeder.description)

        if hasattr(Breeder, 'website') and data.get("website") is not None:
            breeder.website = data.get("website")
        if hasattr(Breeder, 'contact_info') and data.get("contact_info") is not None:
            breeder.contact_info = data.get("contact_info")

        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=data.get("user_id"),
            type="breeder_updated",
            details=f"Breeder updated: {breeder.name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {
            "success": True,
            "message": f"Breeder '{breeder.name}' updated successfully",
        }
    except Exception as e:
        await session.rollback()
        logger.error(f"Error updating breeder: {e}")
        return {"success": False, "error": str(e)}


async def delete_breeder(breeder_id: int, session: AsyncSession) -> Dict[str, Any]:
    """
    Delete a breeder - ASYNC VERSION.

    Args:
        breeder_id (int): The ID of the breeder to delete.
        session: AsyncSession for database operations

    Returns:
        Dict[str, Any]: Result of the operation.
    """
    try:
        result = await session.execute(select(Breeder).where(Breeder.id == breeder_id))
        breeder = result.scalars().first()
        
        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        breeder_name = breeder.name
        await session.delete(breeder)
        await session.commit()

        # Log system activity
        activity = SystemActivity(
            user_id=1,  # System user
            type="breeder_deleted",
            details=f"Breeder deleted: {breeder_name}",
            timestamp=datetime.now(),
        )
        session.add(activity)
        await session.commit()

        return {"success": True, "message": f"Breeder '{breeder_name}' deleted successfully"}
    except Exception as e:
        await session.rollback()
        logger.error(f"Error deleting breeder: {e}")
        return {"success": False, "error": str(e)}


async def search_breeders(query: str, session: AsyncSession) -> List[Dict[str, Any]]:
    """
    Search breeders by name or description - ASYNC VERSION.

    Args:
        query (str): Search query.
        session: AsyncSession for database operations

    Returns:
        List[Dict[str, Any]]: List of matching breeder data dictionaries.
    """
    try:
        # Simple search by name (in a real app, you'd want full-text search)
        result = await session.execute(select(Breeder))
        all_breeders = result.scalars().all()

        matching_breeders = []
        query_lower = query.lower()

        for breeder in all_breeders:
            if (query_lower in breeder.name.lower() or 
                (breeder.description and query_lower in breeder.description.lower())):
                breeder_data = {
                    "id": breeder.id,
                    "name": breeder.name,
                    "description": breeder.description,
                    "website": breeder.website if hasattr(breeder, 'website') else "",
                }
                matching_breeders.append(breeder_data)

        return matching_breeders
    except Exception as e:
        logger.error(f"Error searching breeders: {e}")
        return []