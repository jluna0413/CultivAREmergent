"""
Load configuration data from the database into the Config class.
"""

from app.models.base_models import Activity, Metric, Status, Zone, Strain, Breeder
from app.config import Config
from app.logger import logger

def load_config_from_db():
    """
    Load configuration data from the database into the Config class.
    This function should be called after the database is initialized.
    """
    try:
        # Load activities
        activities = Activity.query.all()
        Config.Activities = [{'id': a.id, 'name': a.name} for a in activities]
        
        # Load metrics
        metrics = Metric.query.all()
        Config.Metrics = [{'id': m.id, 'name': m.name, 'unit': m.unit} for m in metrics]
        
        # Load statuses
        statuses = Status.query.all()
        Config.Statuses = [{'id': s.id, 'status': s.status} for s in statuses]
        
        # Load zones
        zones = Zone.query.all()
        Config.Zones = [{'id': z.id, 'name': z.name} for z in zones]
        
        # Load strains
        strains = Strain.query.all()
        Config.Strains = [{
            'id': s.id,
            'name': s.name,
            'breeder_id': s.breeder_id,
            'breeder_name': s.breeder_name,
            'indica': s.indica,
            'sativa': s.sativa,
            'autoflower': s.autoflower,
            'description': s.description,
            'seed_count': s.seed_count,
            'cycle_time': s.cycle_time,
            'url': s.url,
            'short_description': s.short_description
        } for s in strains]
        
        # Load breeders
        breeders = Breeder.query.all()
        Config.Breeders = [{'id': b.id, 'name': b.name} for b in breeders]
        
        logger.info("Configuration loaded from database")
    except Exception as e:
        logger.error(f"Error loading configuration from database: {e}")
