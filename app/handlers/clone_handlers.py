"""
Clone management handlers for the CultivAR application.
"""

from datetime import datetime, timedelta
from app.models import db
from app.models.base_models import Plant, Strain, Status, Zone, User, PlantActivity, Activity
from app.models.system_models import SystemActivity
from app.logger import logger

def get_available_parent_plants():
    """
    Get all plants that can be used as parents for cloning.
    Only living plants (not harvested or dead) can be parent plants.
    
    Returns:
        list: List of available parent plants.
    """
    try:
        # Get living plants that are not clones themselves (optional restriction)
        # Status IDs: 1=Seedling, 2=Vegetative, 3=Flowering (living), 4=Harvested, 5=Dead
        available_parents = Plant.query.filter(
            Plant.status_id.in_([1, 2, 3])  # Only living plants
        ).all()
        
        parent_list = []
        for plant in available_parents:
            # Get clone count for this parent
            clone_count = Plant.query.filter_by(parent_id=plant.id).count()
            
            parent_data = {
                'id': plant.id,
                'name': plant.name,
                'strain_name': plant.strain.name if plant.strain else 'Unknown',
                'breeder_name': plant.strain.breeder.name if plant.strain and plant.strain.breeder else 'Unknown',
                'status': plant.status.name if plant.status else 'Unknown',
                'current_week': plant.current_week,
                'current_day': plant.current_day,
                'description': plant.description,
                'start_date': plant.start_dt.strftime('%Y-%m-%d') if plant.start_dt else None,
                'clone_count': clone_count,
                'zone_name': plant.zone.name if plant.zone else 'No Zone',
                'is_clone': plant.get('is_clone', False),
                'parent_name': plant.parent.name if plant.parent else None
            }
            parent_list.append(parent_data)
        
        return parent_list
    except Exception as e:
        logger.error(f"Error getting available parent plants: {e}")
        return []

def create_clones(parent_id, clone_data_list):
    """
    Create multiple clones from a parent plant.
    
    Args:
        parent_id (int): ID of the parent plant.
        clone_data_list (list): List of clone data dictionaries.
        
    Returns:
        dict: Result of the operation with success status and clone IDs.
    """
    try:
        parent_plant = Plant.query.get(parent_id)
        if not parent_plant:
            return {'success': False, 'error': 'Parent plant not found'}
        
        # Validate parent plant is alive
        if parent_plant.status_id in [4, 5]:  # Harvested or Dead
            return {'success': False, 'error': 'Cannot clone from harvested or dead plants'}
        
        created_clones = []
        errors = []
        
        for i, clone_data in enumerate(clone_data_list):
            try:
                clone_name = clone_data.get('name', f"{parent_plant.name} - Clone {i+1}")
                description = clone_data.get('description', f"Clone from {parent_plant.name}")
                zone_id = clone_data.get('zone_id', parent_plant.zone_id)
                start_date = clone_data.get('start_date')
                
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d')
                else:
                    start_date = datetime.now()
                
                # Create clone plant
                clone = Plant(
                    name=clone_name,
                    description=description,
                    strain_id=parent_plant.strain_id,
                    zone_id=zone_id,
                    status_id=1,  # Start as Seedling
                    is_clone=True,
                    parent_id=parent_id,
                    start_dt=start_date,
                    current_week=1,
                    current_day=1
                )
                
                db.session.add(clone)
                db.session.flush()  # Get the ID
                
                # Create initial clone activity
                clone_activity = PlantActivity(
                    plant_id=clone.id,
                    activity_id=1,  # Assuming ID 1 is a general activity
                    name="Clone Created",
                    note=f"Clone created from parent plant: {parent_plant.name}",
                    date=start_date
                )
                db.session.add(clone_activity)
                
                created_clones.append({
                    'id': clone.id,
                    'name': clone.name,
                    'description': clone.description
                })
                
            except Exception as e:
                errors.append(f"Clone {i+1}: {str(e)}")
                continue
        
        if created_clones:
            db.session.commit()
            
            # Log system activity
            activity = SystemActivity(
                user_id=1,  # This should be current_user.id in the route
                type='clones_created',
                description=f'{len(created_clones)} clones created from {parent_plant.name}',
                timestamp=datetime.now()
            )
            db.session.add(activity)
            db.session.commit()
            
            result = {
                'success': True,
                'created_clones': created_clones,
                'clone_count': len(created_clones),
                'message': f'Successfully created {len(created_clones)} clones from {parent_plant.name}'
            }
            
            if errors:
                result['errors'] = errors
                
            return result
        else:
            db.session.rollback()
            return {
                'success': False,
                'error': 'Failed to create any clones',
                'errors': errors
            }
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating clones: {e}")
        return {'success': False, 'error': str(e)}

def get_clone_lineage(plant_id):
    """
    Get the complete clone lineage for a plant (parents and children).
    
    Args:
        plant_id (int): ID of the plant.
        
    Returns:
        dict: Clone lineage information.
    """
    try:
        plant = Plant.query.get(plant_id)
        if not plant:
            return {'success': False, 'error': 'Plant not found'}
        
        lineage = {
            'plant': {
                'id': plant.id,
                'name': plant.name,
                'is_clone': plant.get('is_clone', False),
                'strain_name': plant.strain.name if plant.strain else 'Unknown'
            },
            'parent': None,
            'children': [],
            'siblings': [],
            'grandparent': None
        }
        
        # Get parent information
        if plant.parent:
            lineage['parent'] = {
                'id': plant.parent.id,
                'name': plant.parent.name,
                'strain_name': plant.parent.strain.name if plant.parent.strain else 'Unknown',
                'status': plant.parent.status.name if plant.parent.status else 'Unknown',
                'start_date': plant.parent.start_dt.strftime('%Y-%m-%d') if plant.parent.start_dt else None
            }
            
            # Get grandparent if parent is also a clone
            if plant.parent.parent:
                lineage['grandparent'] = {
                    'id': plant.parent.parent.id,
                    'name': plant.parent.parent.name,
                    'strain_name': plant.parent.parent.strain.name if plant.parent.parent.strain else 'Unknown'
                }
            
            # Get siblings (other clones from the same parent)
            siblings = Plant.query.filter(
                Plant.parent_id == plant.parent_id,
                Plant.id != plant.id
            ).all()
            
            for sibling in siblings:
                lineage['siblings'].append({
                    'id': sibling.id,
                    'name': sibling.name,
                    'status': sibling.status.name if sibling.status else 'Unknown',
                    'start_date': sibling.start_dt.strftime('%Y-%m-%d') if sibling.start_dt else None
                })
        
        # Get children (clones of this plant)
        children = Plant.query.filter_by(parent_id=plant.id).all()
        for child in children:
            lineage['children'].append({
                'id': child.id,
                'name': child.name,
                'status': child.status.name if child.status else 'Unknown',
                'start_date': child.start_dt.strftime('%Y-%m-%d') if child.start_dt else None,
                'current_week': child.current_week,
                'current_day': child.current_day
            })
        
        return {'success': True, 'lineage': lineage}
        
    except Exception as e:
        logger.error(f"Error getting clone lineage: {e}")
        return {'success': False, 'error': str(e)}

def get_clone_statistics():
    """
    Get clone statistics and success rates.
    
    Returns:
        dict: Clone statistics.
    """
    try:
        # Total clones created
        total_clones = Plant.query.filter_by(is_clone=True).count()
        
        # Successful clones (living - not dead)
        successful_clones = Plant.query.filter(
            Plant.is_clone == True,
            Plant.status_id != 5  # Not dead
        ).count()
        
        # Failed clones (dead)
        failed_clones = Plant.query.filter(
            Plant.is_clone == True,
            Plant.status_id == 5  # Dead
        ).count()
        
        # Harvested clones
        harvested_clones = Plant.query.filter(
            Plant.is_clone == True,
            Plant.status_id == 4  # Harvested
        ).count()
        
        # Success rate calculation
        success_rate = 0
        if total_clones > 0:
            success_rate = round((successful_clones / total_clones) * 100, 1)
        
        # Get top parent plants (plants with most clones)
        top_parents = db.session.query(
            Plant.id,
            Plant.name,
            db.func.count(Plant.id).label('clone_count')
        ).join(
            Plant, Plant.parent_id == Plant.id, isouter=True
        ).group_by(Plant.id, Plant.name).order_by(
            db.func.count(Plant.id).desc()
        ).limit(5).all()
        
        top_parents_list = []
        for parent in top_parents:
            if parent.clone_count > 0:  # Only include plants that actually have clones
                parent_plant = Plant.query.get(parent.id)
                top_parents_list.append({
                    'id': parent.id,
                    'name': parent.name,
                    'clone_count': parent.clone_count,
                    'strain_name': parent_plant.strain.name if parent_plant.strain else 'Unknown'
                })
        
        # Recent clone activity (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_clones = Plant.query.filter(
            Plant.clone == True,
            Plant.start_dt >= thirty_days_ago
        ).count()
        
        stats = {
            'total_clones': total_clones,
            'successful_clones': successful_clones,
            'failed_clones': failed_clones,
            'harvested_clones': harvested_clones,
            'success_rate': success_rate,
            'recent_clones': recent_clones,
            'top_parents': top_parents_list[:5]  # Limit to top 5
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting clone statistics: {e}")
        return {
            'total_clones': 0,
            'successful_clones': 0,
            'failed_clones': 0,
            'harvested_clones': 0,
            'success_rate': 0,
            'recent_clones': 0,
            'top_parents': []
        }

def get_all_clones():
    """
    Get all clone plants with their parent information.
    
    Returns:
        list: List of all clone plants.
    """
    try:
        clones = Plant.query.filter_by(clone=True).all()
        
        clone_list = []
        for clone in clones:
            clone_data = {
                'id': clone.id,
                'name': clone.name,
                'description': clone.description,
                'strain_name': clone.strain.name if clone.strain else 'Unknown',
                'parent_name': clone.parent.name if clone.parent else 'Unknown',
                'parent_id': clone.parent_id,
                'status': clone.status.name if clone.status else 'Unknown',
                'status_id': clone.status_id,
                'start_date': clone.start_dt.strftime('%Y-%m-%d') if clone.start_dt else None,
                'current_week': clone.current_week,
                'current_day': clone.current_day,
                'zone_name': clone.zone.name if clone.zone else 'No Zone',
                'days_alive': (datetime.now() - clone.start_dt).days if clone.start_dt else 0
            }
            clone_list.append(clone_data)
        
        return clone_list
        
    except Exception as e:
        logger.error(f"Error getting all clones: {e}")
        return []

def delete_clone(clone_id):
    """
    Delete a clone plant.
    
    Args:
        clone_id (int): ID of the clone to delete.
        
    Returns:
        dict: Result of the operation.
    """
    try:
        clone = Plant.query.get(clone_id)
        if not clone:
            return {'success': False, 'error': 'Clone not found'}
        
        if not clone.clone:
            return {'success': False, 'error': 'Plant is not a clone'}
        
        clone_name = clone.name
        
        # Delete associated activities first
        PlantActivity.query.filter_by(plant_id=clone_id).delete()
        
        # Delete the clone
        db.session.delete(clone)
        db.session.commit()
        
        # Log system activity
        activity = SystemActivity(
            user_id=1,  # This should be current_user.id in the route
            type='clone_deleted',
            description=f'Clone deleted: {clone_name}',
            timestamp=datetime.now()
        )
        db.session.add(activity)
        db.session.commit()
        
        return {'success': True, 'message': f'Clone {clone_name} deleted successfully'}
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting clone: {e}")
        return {'success': False, 'error': str(e)}