"""
Plant handlers for the CultivAR application.
"""

import os
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename
from app.models import db
from app.models.base_models import Plant, PlantActivity, Measurement, PlantImage, Status, Sensor, Activity
from app.utils.helpers import calculate_days_since, calculate_weeks_since, estimate_harvest_date
#from app.utils.image import save_image #commented out
from app.logger import logger
from app.config import Config

def get_plant(plant_id):
    """
    Get a plant by ID.

    Args:
        plant_id (int): The ID of the plant.

    Returns:
        dict: The plant data.
    """
    try:
        plant = Plant.query.get(plant_id)
        if not plant:
            return None

        # Get plant measurements
        measurements = Measurement.query.filter_by(plant_id=plant.id).all()

        # Get plant activities
        activities = PlantActivity.query.filter_by(plant_id=plant.id).all()

        # Get plant status history
        status_history = Status.query.filter_by(plant_id=plant.id).all()

        # Get plant images
        images = PlantImage.query.filter_by(plant_id=plant.id).order_by(PlantImage.image_date.desc()).all()

        # Get latest image
        latest_image = images[0] if images else None

        # Calculate days since last watering and feeding
        days_since_watering = calculate_days_since(plant.last_water_date)
        days_since_feeding = calculate_days_since(plant.last_feed_date)

        # Calculate current day and week
        current_day = calculate_days_since(plant.start_dt)
        current_week = calculate_weeks_since(plant.start_dt)

        # Calculate estimated harvest date
        est_harvest_date = estimate_harvest_date(plant.start_dt, plant.cycle_time, plant.autoflower)

        # Build plant data
        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'description': plant.description,
            'status': plant.status_name,
            'status_id': plant.status_id,
            'strain_name': plant.strain_name,
            'strain_id': plant.strain_id,
            'breeder_name': plant.breeder_name,
            'zone_name': plant.zone_name,
            'zone_id': plant.zone_id,
            'current_day': current_day,
            'current_week': current_week,
            'current_height': plant.current_height,
            'height_date': plant.height_date,
            'last_water_date': plant.last_water_date,
            'last_feed_date': plant.last_feed_date,
            'days_since_watering': days_since_watering,
            'days_since_feeding': days_since_feeding,
            'measurements': [
                {
                    'id': m.id,
                    'name': m.name,
                    'value': m.value,
                    'date': m.date
                } for m in measurements
            ],
            'activities': [
                {
                    'id': a.id,
                    'name': a.name,
                    'note': a.note,
                    'date': a.date,
                    'activity_id': a.activity_id
                } for a in activities
            ],
            'status_history': [
                {
                    'id': s.id,
                    'status': s.status,
                    'date': s.date
                } for s in status_history
            ],
            'latest_image': {
                'id': latest_image.id,
                'image_path': latest_image.image_path,
                'image_description': latest_image.image_description,
                'image_date': latest_image.image_date
            } if latest_image else None,
            'images': [
                {
                    'id': img.id,
                    'image_path': img.image_path,
                    'image_description': img.image_description,
                    'image_date': img.image_date
                } for img in images
            ],
            'is_clone': plant.is_clone,
            'start_dt': plant.start_dt,
            'harvest_weight': plant.harvest_weight,
            'harvest_date': plant.harvest_date,
            'cycle_time': plant.cycle_time,
            'strain_url': plant.strain_url,
            'est_harvest_date': est_harvest_date,
            'autoflower': plant.autoflower,
            'parent_id': plant.parent_id,
            'parent_name': plant.parent_name
        }

        return plant_data
    except Exception as e:
        logger.error(f"Error getting plant: {e}")
        return None

def get_living_plants():
    """
    Get all living plants.

    Returns:
        list: The living plants.
    """
    try:
        # Get plants with status other than 'Harvested' or 'Dead'
        plants = Plant.query.filter(Plant.status_id.notin_([4, 5])).all()

        plant_list = []
        for plant in plants:
            # Calculate days since last watering and feeding
            days_since_watering = calculate_days_since(plant.last_water_date)
            days_since_feeding = calculate_days_since(plant.last_feed_date)

            # Calculate current day and week
            current_day = calculate_days_since(plant.start_dt)
            current_week = calculate_weeks_since(plant.start_dt)

            # Calculate flowering days if the plant is in flowering stage
            flowering_days = None
            if plant.status_id == 3:  # Flowering
                flowering_status = Status.query.filter_by(plant_id=plant.id, status='Flowering').first()
                if flowering_status:
                    flowering_days = calculate_days_since(flowering_status.date)

            # Calculate estimated harvest date
            est_harvest_date = estimate_harvest_date(plant.start_dt, plant.cycle_time, plant.autoflower)

            # Get the latest status date
            latest_status = Status.query.filter_by(plant_id=plant.id).order_by(Status.date.desc()).first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'description': plant.description,
                'clone': plant.is_clone,
                'strain_name': plant.strain_name,
                'breeder_name': plant.breeder_name,
                'zone_name': plant.zone_name,
                'start_dt': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else None,
                'current_week': current_week,
                'current_day': current_day,
                'days_since_last_watering': days_since_watering,
                'days_since_last_feeding': days_since_feeding,
                'flowering_days': flowering_days,
                'harvest_weight': plant.harvest_weight,
                'status': plant.status_name,
                'status_date': status_date,
                'cycle_time': plant.cycle_time,
                'strain_url': plant.strain_url,
                'est_harvest_date': est_harvest_date,
                'autoflower': plant.autoflower
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting living plants: {e}")
        return []

def get_harvested_plants():
    """
    Get all harvested plants.

    Returns:
        list: The harvested plants.
    """
    try:
        # Get plants with status 'Harvested'
        plants = Plant.query.filter_by(status_id=4).all()

        plant_list = []
        for plant in plants:
            # Calculate cycle time
            cycle_time = None
            if plant.start_dt and plant.harvest_date:
                delta = plant.harvest_date - plant.start_dt
                cycle_time = delta.days

            # Get the latest status date
            latest_status = Status.query.filter_by(plant_id=plant.id).order_by(Status.date.desc()).first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'description': plant.description,
                'clone': plant.is_clone,
                'strain_name': plant.strain_name,
                'breeder_name': plant.breeder_name,
                'zone_name': plant.zone_name,
                'start_dt': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else None,
                'harvest_weight': plant.harvest_weight,
                'status': plant.status_name,
                'status_date': status_date,
                'cycle_time': cycle_time,
                'strain_url': plant.strain_url,
                'harvest_date': plant.harvest_date,
                'autoflower': plant.autoflower
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting harvested plants: {e}")
        return []

def get_dead_plants():
    """
    Get all dead plants.

    Returns:
        list: The dead plants.
    """
    try:
        # Get plants with status 'Dead'
        plants = Plant.query.filter_by(status_id=5).all()

        plant_list = []
        for plant in plants:
            # Calculate cycle time
            cycle_time = None
            if plant.start_dt:
                latest_status = Status.query.filter_by(plant_id=plant.id).order_by(Status.date.desc()).first()
                if latest_status:
                    delta = latest_status.date - plant.start_dt
                    cycle_time = delta.days

            # Get the latest status date
            latest_status = Status.query.filter_by(plant_id=plant.id).order_by(Status.date.desc()).first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'description': plant.description,
                'clone': plant.is_clone,
                'strain_name': plant.strain_name,
                'breeder_name': plant.breeder_name,
                'zone_name': plant.zone_name,
                'start_dt': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else None,
                'status': plant.status_name,
                'status_date': status_date,
                'cycle_time': cycle_time,
                'strain_url': plant.strain_url,
                'autoflower': plant.autoflower
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting dead plants: {e}")
        return []

def get_plants_by_strain(strain_id):
    """
    Get all plants for a strain.

    Args:
        strain_id (int): The ID of the strain.

    Returns:
        list: The plants for the strain.
    """
    try:
        plants = Plant.query.filter_by(strain_id=strain_id).all()

        plant_list = []
        for plant in plants:
            # Calculate days since last watering and feeding
            days_since_watering = calculate_days_since(plant.last_water_date)
            days_since_feeding = calculate_days_since(plant.last_feed_date)

            # Calculate current day and week
            current_day = calculate_days_since(plant.start_dt)
            current_week = calculate_weeks_since(plant.start_dt)

            # Calculate flowering days if the plant is in flowering stage
            flowering_days = None
            if plant.status_id == 3:  # Flowering
                flowering_status = Status.query.filter_by(plant_id=plant.id, status='Flowering').first()
                if flowering_status:
                    flowering_days = calculate_days_since(flowering_status.date)

            # Calculate estimated harvest date
            est_harvest_date = estimate_harvest_date(plant.start_dt, plant.cycle_time, plant.autoflower)

            # Get the latest status date
            latest_status = Status.query.filter_by(plant_id=plant.id).order_by(Status.date.desc()).first()
            status_date = latest_status.date if latest_status else plant.start_dt

            plant_data = {
                'id': plant.id,
                'name': plant.name,
                'description': plant.description,
                'clone': plant.is_clone,
                'strain_name': plant.strain_name,
                'breeder_name': plant.breeder_name,
                'zone_name': plant.zone_name,
                'start_dt': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else None,
                'current_week': current_week,
                'current_day': current_day,
                'days_since_last_watering': days_since_watering,
                'days_since_feeding': days_since_feeding,
                'flowering_days': flowering_days,
                'harvest_weight': plant.harvest_weight,
                'status': plant.status_name,
                'status_date': status_date,
                'cycle_time': plant.cycle_time,
                'strain_url': plant.strain_url,
                'est_harvest_date': est_harvest_date,
                'autoflower': plant.autoflower,
                'harvest_date': plant.harvest_date
            }

            plant_list.append(plant_data)

        return plant_list
    except Exception as e:
        logger.error(f"Error getting plants by strain: {e}")
        return []

def add_plant(data):
    """
    Add a new plant.

    Args:
        data (dict): The plant data.

    Returns:
        dict: The result of the operation with success status and plant ID.
    """
    try:
        # Set default status to 'Seedling' (status_id=1) if not provided
        status_id = data.get('status_id', 1)

        # Create a new plant
        plant = Plant(
            name=data.get('name'),
            description=data.get('description', ''),
            status_id=status_id,
            strain_id=data.get('strain_id'),
            zone_id=data.get('zone_id'),
            is_clone=data.get('is_clone', False),
            start_dt=datetime.now(),
            autoflower=data.get('autoflower', False),
            parent_id=data.get('parent_id')
        )

        # Add the plant to the database
        db.session.add(plant)
        db.session.commit()

        # Get the status name from the database
        status_obj = Status.query.filter_by(id=status_id).first()
        status_name = "Seedling" if not status_obj else status_obj.status

        # Add the initial status history entry
        status_history = Status(
            plant_id=plant.id,
            status=status_name,
            date=datetime.now()
        )

        db.session.add(status_history)
        db.session.commit()

        # Return success with the plant ID
        return {'success': True, 'id': plant.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding plant: {e}")
        return {'success': False, 'error': str(e)}

def update_plant(data):
    """
    Update a plant.

    Args:
        data (dict): The plant data.

    Returns:
        dict: The result of the operation.
    """
    try:
        plant_id = data.get('id')
        plant = Plant.query.get(plant_id)

        if not plant:
            return {'success': False, 'error': 'Plant not found'}

        # Update plant fields
        plant.name = data.get('name', plant.name)
        plant.description = data.get('description', plant.description)

        # Check if status has changed
        new_status_id = data.get('status_id')
        if new_status_id and new_status_id != plant.status_id:
            plant.status_id = new_status_id

            # Add a new status history entry
            status = Status(
                plant_id=plant.id,
                status=plant.status.status,
                date=datetime.now()
            )

            db.session.add(status)

            # If the plant is harvested, set the harvest date
            if new_status_id == 4:  # Harvested
                plant.harvest_date = datetime.now()

                # Calculate cycle time
                if plant.start_dt:
                    delta = datetime.now() - plant.start_dt
                    plant.cycle_time = delta.days

        # Update other fields
        plant.strain_id = data.get('strain_id', plant.strain_id)
        plant.zone_id = data.get('zone_id', plant.zone_id)
        plant.current_height = data.get('current_height', plant.current_height)
        plant.height_date = datetime.now() if data.get('current_height') else plant.height_date
        plant.harvest_weight = data.get('harvest_weight', plant.harvest_weight)
        plant.strain_url = data.get('strain_url', plant.strain_url)
        plant.autoflower = data.get('autoflower', plant.autoflower)

        # Update watering and feeding dates
        if data.get('watered'):
            plant.last_water_date = datetime.now()

            # Add a watering activity
            activity = PlantActivity(
                plant_id=plant.id,
                name='Water',
                note=data.get('water_note', ''),
                date=datetime.now(),
                activity_id=1  # Water activity ID
            )

            db.session.add(activity)

        if data.get('fed'):
            plant.last_feed_date = datetime.now()

            # Add a feeding activity
            activity = PlantActivity(
                plant_id=plant.id,
                name='Feed',
                note=data.get('feed_note', ''),
                date=datetime.now(),
                activity_id=2  # Feed activity ID
            )

            db.session.add(activity)

        db.session.commit()

        return {'success': True, 'plant_id': plant.id}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating plant: {e}")
        return {'success': False, 'error': str(e)}

def delete_plant(plant_id):
    """
    Delete a plant.

    Args:
        plant_id (int): The ID of the plant.

    Returns:
        dict: The result of the operation.
    """
    try:
        plant = Plant.query.get(plant_id)

        if not plant:
            return {'success': False, 'error': 'Plant not found'}

        # Delete plant images
        images = PlantImage.query.filter_by(plant_id=plant.id).all()
        for image in images:
            # Delete the image file
            image_path = os.path.join(current_app.root_path, image.image_path)
            if os.path.exists(image_path):
                os.remove(image_path)

            db.session.delete(image)

        # Delete plant activities
        activities = PlantActivity.query.filter_by(plant_id=plant.id).all()
        for activity in activities:
            db.session.delete(activity)

        # Delete plant measurements
        measurements = Measurement.query.filter_by(plant_id=plant.id).all()
        for measurement in measurements:
            db.session.delete(measurement)

        # Delete plant status history
        statuses = Status.query.filter_by(plant_id=plant.id).all()
        for status in statuses:
            db.session.delete(status)

        # Delete the plant
        db.session.delete(plant)
        db.session.commit()

        return {'success': True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting plant: {e}")
        return {'success': False, 'error': str(e)}

def link_sensors_to_plant(data):
    """
    Link sensors to a plant.

    Args:
        data (dict): The data containing plant_id and sensor_ids.

    Returns:
        dict: The result of the operation.
    """
    try:
        plant_id = data.get('plant_id')
        sensor_ids = data.get('sensor_ids', [])

        plant = Plant.query.get(plant_id)

        if not plant:
            return {'success': False, 'error': 'Plant not found'}

        # Update sensors
        for sensor_id in sensor_ids:
            sensor = Sensor.query.get(sensor_id)
            if sensor:
                sensor.plant_id = plant_id

        db.session.commit()

        return {'success': True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error linking sensors to plant: {e}")
        return {'success': False, 'error': str(e)}

def upload_plant_images(plant_id, files, description):
    """
    Upload images for a plant.

    Args:
        plant_id (int): The ID of the plant.
        files (list): The image files.
        description (str): The image description.

    Returns:
        dict: The result of the operation.
    """
    try:
        plant = Plant.query.get(plant_id)

        if not plant:
            return {'success': False, 'error': 'Plant not found'}

        # Create the upload folder if it doesn't exist
        upload_folder = os.path.join(Config.UPLOAD_FOLDER, 'plants', str(plant_id))
        os.makedirs(upload_folder, exist_ok=True)

        uploaded_images = []

        for file in files:
            if file and file.filename:
                # Generate a secure filename
                filename = secure_filename(file.filename)

                # Add a timestamp to the filename to make it unique
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{timestamp}_{filename}"

                # Save the file
                #file_path = os.path.join(upload_folder, filename)
                #file.save(file_path)

                # Create a database record for the image
                image = PlantImage(
                    plant_id=plant_id,
                    image_path=os.path.join('uploads', 'plants', str(plant_id), filename),
                    image_description=description,
                    image_order=0,
                    image_date=datetime.now()
                )

                db.session.add(image)
                uploaded_images.append(image)

        db.session.commit()

        return {
            'success': True,
            'images': [
                {
                    'id': img.id,
                    'image_path': img.image_path,
                    'image_description': img.image_description,
                    'image_date': img.image_date
                } for img in uploaded_images
            ]
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error uploading plant images: {e}")
        return {'success': False, 'error': str(e)}

def delete_plant_image(image_id):
    """
    Delete a plant image.

    Args:
        image_id (int): The ID of the image.

    Returns:
        dict: The result of the operation.
    """
    try:
        image = PlantImage.query.get(image_id)

        if not image:
            return {'success': False, 'error': 'Image not found'}

        # Delete the image file
        image_path = os.path.join(current_app.root_path, image.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)

        # Delete the database record
        db.session.delete(image)
        db.session.commit()

        return {'success': True}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting plant image: {e}")
        return {'success': False, 'error': str(e)}


def record_activity(data):
    """
    Record a plant activity.

    Args:
        data (dict): The activity data containing plant_id, activity_id, and note.

    Returns:
        dict: The result of the operation.
    """
    try:
        plant_id = data.get('plant_id')
        activity_id = data.get('activity_id')
        note = data.get('note', '')

        # Validate input
        if not plant_id or not activity_id:
            return {'success': False, 'error': 'Plant ID and Activity ID are required'}

        # Check if plant exists
        plant = Plant.query.get(plant_id)
        if not plant:
            return {'success': False, 'error': 'Plant not found'}

        # Check if activity exists
        activity = Activity.query.get(activity_id)
        if not activity:
            return {'success': False, 'error': 'Activity not found'}

        # Create a new activity record
        plant_activity = PlantActivity(
            plant_id=plant_id,
            name=activity.name,
            note=note,
            date=datetime.now(),
            activity_id=activity_id
        )

        # Add the activity to the database
        db.session.add(plant_activity)

        # Update plant fields based on activity type
        if activity.name.lower() == 'watering' or activity.name.lower() == 'water':
            plant.last_water_date = datetime.now()
        elif activity.name.lower() == 'feeding' or activity.name.lower() == 'feed':
            plant.last_feed_date = datetime.now()
        elif activity.name.lower() == 'transplanting' or activity.name.lower() == 'transplant':
            # Update status to vegetative if it's a seedling
            if plant.status_id == 1:  # Seedling
                plant.status_id = 2  # Vegetative
                # Add a new status history entry
                status = Status(
                    plant_id=plant.id,
                    status='Vegetative',
                    date=datetime.now()
                )
                db.session.add(status)

        db.session.commit()

        return {
            'success': True,
            'activity_id': plant_activity.id,
            'message': f'{activity.name} recorded for {plant.name}'
        }
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error recording plant activity: {e}")
        return {'success': False, 'error': str(e)}
