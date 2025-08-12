"""
Breeder handlers for the CultivAR application.
"""

from app.logger import logger
from app.models import db
from app.models.base_models import Breeder


def get_breeders():
    """
    Get all breeders sorted alphabetically by name.

    Returns:
        list: The breeders sorted alphabetically.
    """
    try:
        # Query breeders and order them by name
        breeders = Breeder.query.order_by(Breeder.name).all()

        breeder_list = []
        for breeder in breeders:
            breeder_data = {"id": breeder.id, "name": breeder.name}

            breeder_list.append(breeder_data)

        return breeder_list
    except Exception as e:
        logger.error(f"Error getting breeders: {e}")
        return []


def add_breeder(data):
    """
    Add a new breeder.

    Args:
        data (dict): The breeder data.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Check if breeder already exists
        existing_breeder = Breeder.query.filter_by(name=data.get("name")).first()
        if existing_breeder:
            return {"success": False, "error": "Breeder with this name already exists"}

        # Create a new breeder
        breeder = Breeder(name=data.get("name"))

        # Add the breeder to the database
        db.session.add(breeder)
        db.session.commit()

        return {"success": True, "breeder_id": breeder.id, "name": breeder.name}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding breeder: {e}")
        return {"success": False, "error": str(e)}


def update_breeder(breeder_id, data):
    """
    Update a breeder.

    Args:
        breeder_id (int): The ID of the breeder.
        data (dict): The breeder data.

    Returns:
        dict: The result of the operation.
    """
    try:
        breeder = Breeder.query.get(breeder_id)

        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        # Check if name already exists
        if data.get("name") != breeder.name:
            existing_breeder = Breeder.query.filter_by(name=data.get("name")).first()
            if existing_breeder:
                return {
                    "success": False,
                    "error": "Breeder with this name already exists",
                }

        # Update breeder fields
        breeder.name = data.get("name", breeder.name)

        db.session.commit()

        return {"success": True, "breeder_id": breeder.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating breeder: {e}")
        return {"success": False, "error": str(e)}


def delete_breeder(breeder_id):
    """
    Delete a breeder.

    Args:
        breeder_id (int): The ID of the breeder.

    Returns:
        dict: The result of the operation.
    """
    try:
        breeder = Breeder.query.get(breeder_id)

        if not breeder:
            return {"success": False, "error": "Breeder not found"}

        # Check if there are strains using this breeder
        if breeder.strains and len(breeder.strains) > 0:
            return {
                "success": False,
                "error": f"Cannot delete breeder: {len(breeder.strains)} strains are using this breeder",
            }

        # Delete the breeder
        db.session.delete(breeder)
        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting breeder: {e}")
        return {"success": False, "error": str(e)}
