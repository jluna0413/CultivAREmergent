"""
Cultivar handlers for the CultivAR application.
Backward compatibility aliases maintain 'strain' terminology for existing code.
"""

from app.logger import logger
from app.models import db
from app.models.base_models import Plant, Cultivar as Strain


def get_cultivar(cultivar_id):
    """
    Get a cultivar by ID.

    Args:
        cultivar_id (int): The ID of the cultivar.

    Returns:
        dict: The cultivar data.
    """
    try:
        cultivar = Strain.query.get(cultivar_id)
        if not cultivar:
            return None

        # Count plants using this cultivar
        plant_count = Plant.query.filter_by(cultivar_id=cultivar.id).count()

        # Build cultivar data
        cultivar_data = {
            "id": cultivar.id,
            "name": cultivar.name,
            "breeder": cultivar.breeder_name,
            "breeder_id": cultivar.breeder_id,
            "indica": cultivar.indica,
            "sativa": cultivar.sativa,
            "autoflower": cultivar.autoflower,
            "description": cultivar.description,
            "seed_count": cultivar.seed_count,
            "cycle_time": cultivar.cycle_time,
            "url": cultivar.url,
            "short_description": cultivar.short_description,
            "plant_count": plant_count,
        }

        return cultivar_data
    except Exception as e:
        logger.error(f"Error getting cultivar: {e}")
        return None


def get_in_stock_cultivars():
    """
    Get all in-stock cultivars.

    Returns:
        list: The in-stock cultivars.
    """
    try:
        # Get cultivars with seed_count > 0
        cultivars = Strain.query.filter(Strain.seed_count > 0).all()

        cultivar_list = []
        for cultivar in cultivars:
            # Count plants using this cultivar
            plant_count = Plant.query.filter_by(cultivar_id=cultivar.id).count()

            cultivar_data = {
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder_name,
                "breeder_id": cultivar.breeder_id,
                "indica": cultivar.indica,
                "sativa": cultivar.sativa,
                "autoflower": cultivar.autoflower,
                "description": cultivar.description,
                "seed_count": cultivar.seed_count,
                "cycle_time": cultivar.cycle_time,
                "url": cultivar.url,
                "short_description": cultivar.short_description,
                "plant_count": plant_count,
            }

            cultivar_list.append(cultivar_data)

        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting in-stock cultivars: {e}")
        return []


def get_out_of_stock_cultivars():
    """
    Get all out-of-stock cultivars.

    Returns:
        list: The out-of-stock cultivars.
    """
    try:
        # Get cultivars with seed_count = 0
        cultivars = Strain.query.filter(Strain.seed_count == 0).all()

        cultivar_list = []
        for cultivar in cultivars:
            # Count plants using this cultivar
            plant_count = Plant.query.filter_by(cultivar_id=cultivar.id).count()

            cultivar_data = {
                "id": cultivar.id,
                "name": cultivar.name,
                "breeder": cultivar.breeder_name,
                "breeder_id": cultivar.breeder_id,
                "indica": cultivar.indica,
                "sativa": cultivar.sativa,
                "autoflower": cultivar.autoflower,
                "description": cultivar.description,
                "seed_count": cultivar.seed_count,
                "cycle_time": cultivar.cycle_time,
                "url": cultivar.url,
                "short_description": cultivar.short_description,
                "plant_count": plant_count,
            }

            cultivar_list.append(cultivar_data)

        return cultivar_list
    except Exception as e:
        logger.error(f"Error getting out-of-stock cultivars: {e}")
        return []


def add_cultivar(data):
    """
    Add a new cultivar.

    Args:
        data (dict): The cultivar data.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Create a new cultivar
        cultivar = Strain(
            name=data.get("name"),
            breeder_id=data.get("breeder_id"),
            indica=data.get("indica", 0),
            sativa=data.get("sativa", 0),
            autoflower=data.get("autoflower", False),
            description=data.get("description", ""),
            seed_count=data.get("seed_count", 0),
            cycle_time=data.get("cycle_time"),
            url=data.get("url", ""),
            short_description=data.get("short_description", ""),
        )

        # Add the cultivar to the database
        db.session.add(cultivar)
        db.session.commit()

        return {"success": True, "cultivar_id": cultivar.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding cultivar: {e}")
        return {"success": False, "error": str(e)}


def update_cultivar(cultivar_id, data):
    """
    Update a cultivar.

    Args:
        cultivar_id (int): The ID of the cultivar.
        data (dict): The cultivar data.

    Returns:
        dict: The result of the operation.
    """
    try:
        cultivar = Strain.query.get(cultivar_id)

        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        # Update cultivar fields
        cultivar.name = data.get("name", cultivar.name)
        cultivar.breeder_id = data.get("breeder_id", cultivar.breeder_id)
        cultivar.indica = data.get("indica", cultivar.indica)
        cultivar.sativa = data.get("sativa", cultivar.sativa)
        cultivar.autoflower = data.get("autoflower", cultivar.autoflower)
        cultivar.description = data.get("description", cultivar.description)
        cultivar.seed_count = data.get("seed_count", cultivar.seed_count)
        cultivar.cycle_time = data.get("cycle_time", cultivar.cycle_time)
        cultivar.url = data.get("url", cultivar.url)
        cultivar.short_description = data.get(
            "short_description", cultivar.short_description
        )

        db.session.commit()

        return {"success": True, "cultivar_id": cultivar.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating cultivar: {e}")
        return {"success": False, "error": str(e)}


def delete_cultivar(cultivar_id):
    """
    Delete a cultivar.

    Args:
        cultivar_id (int): The ID of the cultivar.

    Returns:
        dict: The result of the operation.
    """
    try:
        cultivar = Strain.query.get(cultivar_id)

        if not cultivar:
            return {"success": False, "error": "Cultivar not found"}

        # Check if there are plants using this cultivar
        plants = Plant.query.filter_by(cultivar_id=cultivar_id).count()
        if plants > 0:
            return {
                "success": False,
                "error": f"Cannot delete cultivar: {plants} plants are using this cultivar",
            }

        # Delete the cultivar
        db.session.delete(cultivar)
        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting cultivar: {e}")
        return {"success": False, "error": str(e)}


# Backward compatibility aliases
def get_strain(strain_id):
    """
    Get a strain by ID.

    Args:
        strain_id (int): The ID of the strain.

    Returns:
        dict: The strain data.
    """
    try:
        strain = Strain.query.get(strain_id)
        if not strain:
            return None

        # Count plants using this strain
        plant_count = Plant.query.filter_by(strain_id=strain.id).count()

        # Build strain data
        strain_data = {
            "id": strain.id,
            "name": strain.name,
            "breeder": strain.breeder_name,
            "breeder_id": strain.breeder_id,
            "indica": strain.indica,
            "sativa": strain.sativa,
            "autoflower": strain.autoflower,
            "description": strain.description,
            "seed_count": strain.seed_count,
            "cycle_time": strain.cycle_time,
            "url": strain.url,
            "short_description": strain.short_description,
            "plant_count": plant_count,
        }

        return strain_data
    except Exception as e:
        logger.error(f"Error getting strain: {e}")
        return None


def get_in_stock_strains():
    """
    Get all in-stock strains.

    Returns:
        list: The in-stock strains.
    """
    try:
        # Get strains with seed_count > 0
        strains = Strain.query.filter(Strain.seed_count > 0).all()

        strain_list = []
        for strain in strains:
            # Count plants using this strain
            plant_count = Plant.query.filter_by(strain_id=strain.id).count()

            strain_data = {
                "id": strain.id,
                "name": strain.name,
                "breeder": strain.breeder_name,
                "breeder_id": strain.breeder_id,
                "indica": strain.indica,
                "sativa": strain.sativa,
                "autoflower": strain.autoflower,
                "description": strain.description,
                "seed_count": strain.seed_count,
                "cycle_time": strain.cycle_time,
                "url": strain.url,
                "short_description": strain.short_description,
                "plant_count": plant_count,
            }

            strain_list.append(strain_data)

        return strain_list
    except Exception as e:
        logger.error(f"Error getting in-stock strains: {e}")
        return []


def get_out_of_stock_strains():
    """
    Get all out-of-stock strains.

    Returns:
        list: The out-of-stock strains.
    """
    try:
        # Get strains with seed_count = 0
        strains = Strain.query.filter(Strain.seed_count == 0).all()

        strain_list = []
        for strain in strains:
            # Count plants using this strain
            plant_count = Plant.query.filter_by(strain_id=strain.id).count()

            strain_data = {
                "id": strain.id,
                "name": strain.name,
                "breeder": strain.breeder_name,
                "breeder_id": strain.breeder_id,
                "indica": strain.indica,
                "sativa": strain.sativa,
                "autoflower": strain.autoflower,
                "description": strain.description,
                "seed_count": strain.seed_count,
                "cycle_time": strain.cycle_time,
                "url": strain.url,
                "short_description": strain.short_description,
                "plant_count": plant_count,
            }

            strain_list.append(strain_data)

        return strain_list
    except Exception as e:
        logger.error(f"Error getting out-of-stock strains: {e}")
        return []


def add_strain(data):
    """
    Add a new strain.

    Args:
        data (dict): The strain data.

    Returns:
        dict: The result of the operation.
    """
    try:
        # Create a new strain
        strain = Strain(
            name=data.get("name"),
            breeder_id=data.get("breeder_id"),
            indica=data.get("indica", 0),
            sativa=data.get("sativa", 0),
            autoflower=data.get("autoflower", False),
            description=data.get("description", ""),
            seed_count=data.get("seed_count", 0),
            cycle_time=data.get("cycle_time"),
            url=data.get("url", ""),
            short_description=data.get("short_description", ""),
        )

        # Add the strain to the database
        db.session.add(strain)
        db.session.commit()

        return {"success": True, "strain_id": strain.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding strain: {e}")
        return {"success": False, "error": str(e)}


def update_strain(strain_id, data):
    """
    Update a strain.

    Args:
        strain_id (int): The ID of the strain.
        data (dict): The strain data.

    Returns:
        dict: The result of the operation.
    """
    try:
        strain = Strain.query.get(strain_id)

        if not strain:
            return {"success": False, "error": "Strain not found"}

        # Update strain fields
        strain.name = data.get("name", strain.name)
        strain.breeder_id = data.get("breeder_id", strain.breeder_id)
        strain.indica = data.get("indica", strain.indica)
        strain.sativa = data.get("sativa", strain.sativa)
        strain.autoflower = data.get("autoflower", strain.autoflower)
        strain.description = data.get("description", strain.description)
        strain.seed_count = data.get("seed_count", strain.seed_count)
        strain.cycle_time = data.get("cycle_time", strain.cycle_time)
        strain.url = data.get("url", strain.url)
        strain.short_description = data.get(
            "short_description", strain.short_description
        )

        db.session.commit()

        return {"success": True, "strain_id": strain.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating strain: {e}")
        return {"success": False, "error": str(e)}


def delete_strain(strain_id):
    """
    Delete a strain.

    Args:
        strain_id (int): The ID of the strain.

    Returns:
        dict: The result of the operation.
    """
    try:
        strain = Strain.query.get(strain_id)

        if not strain:
            return {"success": False, "error": "Strain not found"}

        # Check if there are plants using this strain
        plants = Plant.query.filter_by(strain_id=strain_id).count()
        if plants > 0:
            return {
                "success": False,
                "error": f"Cannot delete strain: {plants} plants are using this strain",
            }

        # Delete the strain
        db.session.delete(strain)
        db.session.commit()

        return {"success": True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting strain: {e}")
        return {"success": False, "error": str(e)}
