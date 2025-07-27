"""
Handlers module for the CultivAR application.
"""

from app.handlers.plant_handlers import get_plant, get_living_plants, get_harvested_plants, get_dead_plants
from app.handlers.strain_handlers import get_strain, get_in_stock_strains, get_out_of_stock_strains
from app.handlers.sensor_handlers import get_sensors, get_grouped_sensors_with_latest_reading
from app.handlers.settings_handlers import get_settings, update_user_password
from app.handlers.breeder_handlers import get_breeders, add_breeder, update_breeder, delete_breeder

# User management handlers
from app.handlers.user_handlers import get_all_users, get_user_by_id, create_user, update_user, delete_user
from app.handlers.user_handlers import toggle_user_admin_status, force_password_reset, get_user_statistics
