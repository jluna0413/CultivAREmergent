# Unused Variables and Imports

This document lists unused variables and imports that were identified during the codebase audit. These were not removed from the code to preserve them for potential future development and integration.

## Unused Imports

### `app.handlers.__init__.py`
- `app.handlers.breeder_handlers.add_breeder`
- `app.handlers.breeder_handlers.delete_breeder`
- `app.handlers.breeder_handlers.get_breeders`
- `app.handlers.breeder_handlers.update_breeder`
- `app.handlers.clone_handlers.create_clones`
- `app.handlers.clone_handlers.delete_clone`
- `app.handlers.clone_handlers.get_all_clones`
- `app.handlers.clone_handlers.get_available_parent_plants`
- `app.handlers.clone_handlers.get_clone_lineage`
- `app.handlers.clone_handlers.get_clone_statistics`
- `app.handlers.export_handlers.export_activities_csv`
- `app.handlers.export_handlers.export_complete_backup`
- `app.handlers.export_handlers.export_plants_csv`
- `app.handlers.export_handlers.export_plants_json`
- `app.handlers.export_handlers.export_sensors_csv`
- `app.handlers.export_handlers.export_strains_csv`
- `app.handlers.export_handlers.export_strains_json`
- `app.handlers.export_handlers.export_users_csv`
- `app.handlers.export_handlers.get_export_statistics`
- `app.handlers.plant_handlers.get_dead_plants`
- `app.handlers.plant_handlers.get_harvested_plants`
- `app.handlers.plant_handlers.get_living_plants`
- `app.handlers.plant_handlers.get_plant`
- `app.handlers.sensor_handlers.get_grouped_sensors_with_latest_reading`
- `app.handlers.sensor_handlers.get_sensors`
- `app.handlers.settings_handlers.get_settings`
- `app.handlers.settings_handlers.update_user_password`
- `app.handlers.strain_handlers.get_in_stock_strains`
- `app.handlers.strain_handlers.get_out_of_stock_strains`
- `app.handlers.strain_handlers.get_strain`
- `app.handlers.user_handlers.create_user`
- `app.handlers.user_handlers.delete_user`
- `app.handlers.user_handlers.force_password_reset`
- `app.handlers.user_handlers.get_all_users`
- `app.handlers.user_handlers.get_user_by_id`
- `app.handlers.user_handlers.get_user_statistics`
- `app.handlers.user_handlers.toggle_user_admin_status`
- `app.handlers.user_handlers.update_user`

### `app.handlers.sensor_handlers.py`
- `requests`

## Unused Variables

### `app.handlers.sensor_handlers.py`
- `sensor_id` in `add_sensor` function. This variable is assigned but not used. It is intended to be the ID of the new sensor, but it is not returned or used in any other way.

### `app.blueprints.auth.py`
- `contact_method` in `signup` function. This variable is assigned either the phone number or the email address, but it is not used. It was likely intended for a confirmation message or logging.
