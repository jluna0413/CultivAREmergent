# CultivAR Codebase Documentation

## Table of Contents

1.  [Introduction](#introduction)
2.  [Application Structure](#application-structure)
3.  [Modules](#modules)
    *   [app/__init__.py](#app__init__py)
    *   [cultivar_app.py](#cultivar_apppy)
    *   [Blueprints](#blueprints)
        *   [app/blueprints/admin.py](#appblueprintsadminpy)
        *   [app/blueprints/auth.py](#appblueprintsauthpy)
        *   [app/blueprints/breeders.py](#appblueprintsbreederspy)
        *   [app/blueprints/clones.py](#appblueprintsclonespy)
        *   [app/blueprints/dashboard.py](#appblueprintsdashboardpy)
        *   [app/blueprints/diagnostics.py](#appblueprintsdiagnosticspy)
        *   [app/blueprints/market.py](#appblueprintsmarketpy)
        *   [app/blueprints/strains.py](#appblueprintsstrainspy)
    *   [Configuration](#configuration)
        *   [app/config/config.py](#appconfigconfigpy)
    *   [Handlers](#handlers)
        *   [app/handlers/activity_handlers.py](#apphandlersactivity_handlerspy)
        *   [app/handlers/breeder_handlers.py](#apphandlersbreeder_handlerspy)
        *   [app/handlers/clone_handlers.py](#apphandlersclone_handlerspy)
        *   [app/handlers/export_handlers.py](#apphandlersexport_handlerspy)
        *   [app/handlers/plant_handlers.py](#apphandlersplant_handlerspy)
        *   [app/handlers/sensor_handlers.py](#apphandlerssensor_handlerspy)
        *   [app/handlers/settings_handlers.py](#apphandlerssettings_handlerspy)
        *   [app/handlers/strain_handlers.py](#apphandlersstrain_handlerspy)
        *   [app/handlers/user_handlers.py](#apphandlersuser_handlerspy)
    *   [Logger](#logger)
        *   [app/logger/logger.py](#apploggerloggerpy)
    *   [Models](#models)
        *   [app/models/__init__.py](#appmodels__init__py)
        *   [app/models/acinfinity_models.py](#appmodelsacinfinity_modelspy)
        *   [app/models/base_models.py](#appmodelsbase_modelspy)
        *   [app/models/ecowitt_models.py](#appmodelsecowitt_modelspy)
        *   [app/models/system_models.py](#appmodelssystem_modelspy)
    *   [Routes](#routes)
        *   [app/routes/routes.py](#approutesroutespy)
    *   [Utilities](#utilities)
        *   [app/utils/auth.py](#apputilsauthpy)
        *   [app/utils/helpers.py](#apputilshelperspy)
        *   [app/utils/image.py](#apputilsimagepy)
        *   [app/utils/rate_limiter.py](#apputilsrate_limiterpy)
        *   [app/utils/validators.py](#apputilsvalidatorspy)
    *   [Watcher](#watcher)
        *   [app/watcher/watcher.py](#appwatcherwatcherpy)
4.  [How to Use This Documentation](#how-to-use-this-documentation)

## Introduction

This documentation provides a comprehensive overview of the CultivAR application codebase. CultivAR is a Flask-based web application designed for managing plant cultivation, including features for user authentication, plant tracking, strain management, clone management, sensor integration, and administrative functions.

The application is structured to be modular, utilizing Flask Blueprints for organizing different feature areas and SQLAlchemy for database interactions. Security is a key consideration, with Flask-Talisman implementing various security headers and Flask-Limiter providing DDoS protection.

## Application Structure

The project follows a typical Flask application structure, with a main application factory (`cultivar_app.py`) and various subdirectories for blueprints, configuration, handlers, models, routes, static assets, templates, and utilities.

-   `app/`: Contains the core application logic.
    -   `blueprints/`: Modular components for different feature areas (e.g., admin, auth, dashboard).
    -   `config/`: Application configuration settings.
    -   `handlers/`: Business logic and data processing functions.
    -   `logger/`: Logging configuration and utilities.
    -   `models/`: SQLAlchemy database models.
    -   `routes/`: Main application routes.
    -   `static/`: Static assets like CSS, JavaScript, and images.
    -   `utils/`: Helper functions and utilities.
    -   `watcher/`: Background tasks or monitoring.
    -   `web/`: Web-related assets, including static files and HTML templates.
-   `docs/`: Existing project documentation and where generated documentation will reside.
-   `data/`: Database files or other data storage.
-   `logs/`: Application log files.
-   `scripts/`: Utility scripts.
-   `uploads/`: User-uploaded files (e.g., plant images).

## Modules

### app/__init__.py

This file marks the `app` directory as a Python package and defines the application's version.

```python
"""
CultivAR application package.
"""

__version__ = "0.1.0"
```

### cultivar_app.py

This is the application factory, responsible for creating and configuring the Flask application instance. It initializes extensions like Flask-Login, Flask-Talisman, and Flask-Limiter, sets up database connections, registers blueprints, and handles initial data seeding.

**Functions:**

-   `create_app()`:
    -   Initializes the Flask app, loads configuration from `app.config.config.Config`.
    -   Sets up `SQLALCHEMY_DATABASE_URI`, `SECRET_KEY`, `UPLOAD_FOLDER`, etc.
    -   Initializes `Flask-SQLAlchemy` (`db`), `Flask-Login` (`login_manager`), `Flask-Talisman` (security headers), and `Flask-Limiter` (rate limiting).
    -   Registers user loader for Flask-Login.
    -   Configures session cookies for security.
    -   Handles database table creation and initial data seeding (e.g., a test plant if none exist).
    -   Registers main routes and blueprints.
    -   Initializes the application logger.
    -   Returns the configured Flask app.

**Example Usage:**

```python
# In main.py or run.py
from cultivar_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Blueprints

#### app/blueprints/admin.py

This blueprint handles administrative functions, including user management (create, edit, delete, toggle admin status, force password reset) and data export (plants, strains, activities, users, sensors, complete backup). It includes both HTML rendering routes and API endpoints for AJAX requests.

**Routes:**

-   `/admin/users` (GET): Renders the user management page.
-   `/admin/users/create` (GET, POST): Renders/handles new user creation.
-   `/admin/users/<int:user_id>/edit` (GET, POST): Renders/handles editing an existing user.
-   `/admin/users/<int:user_id>/delete` (POST): Deletes a user (API).
-   `/admin/users/<int:user_id>/toggle-admin` (POST): Toggles admin status (API).
-   `/admin/users/<int:user_id>/force-password-reset` (POST): Forces password reset (API).
-   `/admin/api/users` (GET): Returns all users (API).
-   `/admin/api/users/<int:user_id>` (GET): Returns a specific user (API).
-   `/admin/api/users/stats` (GET): Returns user statistics (API).
-   `/admin/export` (GET): Renders the data export page.
-   `/admin/export/plants/<format>` (GET): Exports plant data in CSV or JSON.
-   `/admin/export/strains/<format>` (GET): Exports strain data in CSV or JSON.
-   `/admin/export/activities` (GET): Exports activity data in CSV.
-   `/admin/export/users` (GET): Exports user data in CSV.
-   `/admin/export/sensors` (GET): Exports sensor data in CSV.
-   `/admin/export/complete` (GET): Creates and exports a complete system backup (ZIP).
-   `/admin/api/export/stats` (GET): Returns export statistics (API).
-   `/admin/api/users` (GET, POST): API for getting all users and adding a new user.
-   `/admin/api/users/<int:user_id>` (GET, PUT, DELETE): API for getting, updating, and deleting a specific user.
-   `/admin/api/users/<int:user_id>/reset-password` (POST): API for resetting a user's password.
-   `/admin/api/system/logs` (GET): API for getting system logs.
-   `/admin/api/system/info` (GET): API for getting system information (Python, OS, CPU, Memory, Disk, Boot time).
-   `/admin/api/diagnostics/test` (GET): Simple endpoint for testing diagnostics functionality.

**Functions:**

-   `admin_required(f)`: Decorator to ensure only authenticated admin users can access a route.

#### app/blueprints/auth.py

This blueprint manages user authentication, including login, signup, and logout functionalities. It integrates with Flask-Login for session management and `werkzeug.security` for password hashing. Rate limiting is applied to login and signup routes to prevent brute-force attacks.

**Routes:**

-   `/auth/login` (GET, POST): Handles user login.
-   `/auth/signup` (GET, POST): Handles new user registration.
-   `/auth/logout` (GET): Logs out the current user.
-   `/auth/forgot-password` (GET, POST): Placeholder for password reset functionality.

**Example Usage (Login):**

```html
<!-- In app/web/templates/views/new_login.html -->
<form method="POST" action="{{ url_for('auth.login') }}">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>
```

#### app/blueprints/breeders.py

This blueprint handles routes related to breeder management. Currently, it provides a route to render the page for adding new breeders.

**Routes:**

-   `/breeders/add` (GET): Renders the page to add a new breeder.

#### app/blueprints/clones.py

This blueprint manages clone-related functionalities, including a dashboard, creation of new clones from parent plants, viewing clone lineage, and deleting clones. It also provides API endpoints for these operations.

**Routes:**

-   `/clones/` (GET): Renders the clone management dashboard.
-   `/clones/create` (GET, POST): Renders/handles the creation of new clones.
-   `/clones/<int:clone_id>/lineage` (GET): Renders the clone lineage view.
-   `/clones/<int:clone_id>/delete` (POST): Deletes a clone (API).
-   `/clones/api/stats` (GET): Returns clone statistics (API).
-   `/clones/api/parents` (GET): Returns available parent plants (API).
-   `/clones/api` (GET): Returns all clones (API).
-   `/clones/api/<int:clone_id>/lineage` (GET): Returns clone lineage (API).

**Example Usage (Create Clones):**

```html
<!-- In app/web/templates/clones/create.html -->
<form method="POST" action="{{ url_for('clones.create') }}">
    <label for="parent_id">Parent Plant:</label>
    <select name="parent_id" id="parent_id">
        <!-- Options populated dynamically -->
    </select>
    <label for="clone_count">Number of Clones:</label>
    <input type="number" name="clone_count" value="1" min="1">
    <!-- Dynamic fields for each clone's name, description, zone, start date -->
    <button type="submit">Create Clones</button>
</form>
```

#### app/blueprints/dashboard.py

This blueprint defines routes for the main user dashboard and plant management pages. It allows users to view their plants and individual plant details.

**Routes:**

-   `/dashboard/` (GET): Renders the main user dashboard.
-   `/dashboard/plants` (GET): Renders the page displaying all plants for the current user.
-   `/dashboard/plant/<int:plant_id>` (GET): Renders the detail page for a specific plant.

**Example Usage (Plants Page):**

```html
<!-- In app/web/templates/views/plants.html -->
{% for plant in plants %}
    <div>
        <h3>{{ plant.name }}</h3>
        <p>Strain: {{ plant.strain_name }}</p>
        <a href="{{ url_for('dashboard.plant', plant_id=plant.id) }}">View Details</a>
    </div>
{% endfor %}
```

#### app/blueprints/diagnostics.py

This blueprint provides a diagnostics endpoint to retrieve application, database, and system information. It's useful for health checks and troubleshooting.

**Routes:**

-   `/diagnostics` (GET): Returns a JSON object containing application info, database status, and recent log lines.

**Example Response:**

```json
{
    "database": "ok",
    "info": {
        "app_name": "CultivAR",
        "cwd": "/app",
        "environment": "production",
        "platform": "Linux-5.10.104-linuxkit-x86_64-with-glibc2.31",
        "python_version": "3.9.7 (default, Sep 10 2021, 14:59:10) \n[GCC 9.3.0]",
        "version": "0.1.0"
    },
    "recent_logs": [
        "INFO:cultivar:CultivAR application created successfully\n"
    ]
}
```

#### app/blueprints/market.py

This blueprint handles routes related to the application's market features, including a shopping cart and various market categories like seed bank, extensions, and gear.

**Routes:**

-   `/cart` (GET): Renders the shopping cart page.
-   `/market/seed-bank` (GET): Renders the seed bank market page.
-   `/market/extensions` (GET): Renders the extensions market page.
-   `/market/gear` (GET): Renders the gear market page.

#### app/blueprints/strains.py

This blueprint manages routes for displaying and adding plant strains. It provides pages to view a collection of strains and their details, as well as a page to add new strains.

**Routes:**

-   `/` (GET): Renders the strains collection page.
-   `/strains` (GET): Alternative route for the strains collection page.
-   `/<int:strain_id>` (GET): Renders the detail page for a specific strain.
-   `/add` (GET): Renders the page to add a new strain.
-   `/strains/add` (GET): Legacy route for the add strain page.

**Example Usage (Strain Detail):**

```html
<!-- In app/web/templates/views/strain.html -->
<h1>{{ strain.name }}</h1>
<p>Breeder: {{ strain.breeder_name }}</p>
<p>Indica: {{ strain.indica }}%, Sativa: {{ strain.sativa }}%</p>
<p>Description: {{ strain.description }}</p>
```

### Configuration

#### app/config/config.py

This file defines the `Config` class, which centralizes all application configuration settings. It loads values from environment variables and provides methods for database URI construction and ensuring necessary directories exist.

**Class: `Config`**

-   **Attributes:**
    -   `SECRET_KEY`: Flask secret key.
    -   `DEBUG`: Debug mode flag.
    -   `PORT`: Application port.
    -   `DB_DRIVER`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: Database connection details.
    -   `SQLITE_DB_PATH`: Path for SQLite database.
    -   `UPLOAD_FOLDER`, `MAX_CONTENT_LENGTH`: File upload settings.
    -   `POLLING_INTERVAL`, `STREAM_GRAB_INTERVAL`: Sensor polling intervals.
    -   `GUEST_MODE`: Guest mode flag.
    -   `SSL_ENABLED`, `SSL_CERT_PATH`, `SSL_KEY_PATH`: SSL/TLS configuration.
    -   `Activities`, `Metrics`, `Statuses`, `Zones`, `Strains`, `Breeders`: Default lists (often populated from external sources or database).
    -   `DEFAULT_SETTINGS`: Default application settings.
-   **Methods:**
    -   `get_database_uri()`: Constructs the database URI based on `DB_DRIVER`.
    -   `ensure_upload_folder()`: Creates the `UPLOAD_FOLDER` and its subdirectories if they don't exist.
    -   `validate_production_settings()`: Validates critical settings for production environments.

**Example Usage:**

```python
# Accessing configuration in other modules
from app.config.config import Config

app.config['SECRET_KEY'] = Config.SECRET_KEY
db_uri = Config.get_database_uri()
```

### Handlers

#### app/handlers/activity_handlers.py

This module provides functions for recording and retrieving various types of activities within the CultivAR application, including system activities and specific plant activities. It helps in auditing and tracking user and system actions.

**Functions:**

-   `record_system_activity(activity_type, details=None, user_id=None)`:
    -   Records a general system activity.
    -   Automatically determines the `user_id` if not provided (current user, system user, or admin).
    -   `activity_type` (str): Type of activity (e.g., "login", "plant_add").
    -   `details` (dict, optional): Additional JSON-serializable details about the activity.
    -   `user_id` (int, optional): ID of the user performing the activity.
    -   Returns `{"success": True, "activity_id": int}` on success, `{"success": False, "error": str}` on failure.
-   `get_recent_activities(limit=10)`:
    -   Retrieves a list of recent system activities.
    -   `limit` (int, optional): Maximum number of activities to return (default: 10).
    -   Returns `list` of activity dictionaries.
-   `get_plant_activities(plant_id, limit=10)`:
    -   Retrieves recent activities for a specific plant.
    -   `plant_id` (int): The ID of the plant.
    -   `limit` (int, optional): Maximum number of activities to return (default: 10).
    -   Returns `list` of plant activity dictionaries.
-   `record_login_activity(username)`:
    -   Records a user login activity.
    -   `username` (str): The username of the user who logged in.
-   `record_plant_add_activity(plant_name, plant_id)`:
    -   Records an activity when a new plant is added.
    -   `plant_name` (str): Name of the added plant.
    -   `plant_id` (int): ID of the added plant.
-   `record_strain_edit_activity(strain_name, strain_id)`:
    -   Records an activity when a strain is edited.
    -   `strain_name` (str): Name of the edited strain.
    -   `strain_id` (int): ID of the edited strain.
-   `record_user_add_activity(new_username)`:
    -   Records an activity when a new user is added.
    -   `new_username` (str): Username of the new user.
-   `record_sensor_reading_activity(sensor_name, value, unit)`:
    -   Records an activity for a sensor reading.
    -   `sensor_name` (str): Name of the sensor.
    -   `value` (float/int): The sensor reading value.
    -   `unit` (str): Unit of the sensor reading (e.g., "°F", "%").
-   `record_plant_activity(plant_id, activity_name, note=None)`:
    -   Records a specific activity related to a plant.
    -   `plant_id` (int): The ID of the plant.
    -   `activity_name` (str): Name of the activity (e.g., "Watered", "Nutrients Applied").
    -   `note` (str, optional): Additional notes for the activity.

**Example Usage:**

```python
from app.handlers.activity_handlers import record_system_activity, get_recent_activities

# Record a system activity
record_system_activity("user_logout", {"user_id": 1, "reason": "manual"})

# Get recent activities
recent_activities = get_recent_activities(limit=5)
for activity in recent_activities:
    print(f"[{activity['timestamp']}] {activity['user']} - {activity['type']}")
```
#### app/handlers/breeder_handlers.py

This module provides functions for managing breeder information in the CultivAR application, including retrieving, adding, updating, and deleting breeder records.

**Functions:**

-   `get_breeders()`:
    -   Retrieves all breeders from the database, sorted alphabetically by name.
    -   Returns `list` of breeder dictionaries (each with `id` and `name`).
-   `add_breeder(data)`:
    -   Adds a new breeder to the database.
    -   `data` (dict): A dictionary containing the breeder's `name`.
    -   Returns `{"success": True, "breeder_id": int, "name": str}` on success, `{"success": False, "error": str}` on failure (e.g., if a breeder with the same name already exists).
-   `update_breeder(breeder_id, data)`:
    -   Updates an existing breeder's information.
    -   `breeder_id` (int): The ID of the breeder to update.
    -   `data` (dict): A dictionary containing the new breeder `name` (optional).
    -   Returns `{"success": True, "breeder_id": int}` on success, `{"success": False, "error": str}` on failure (e.g., breeder not found, or new name already exists).
-   `delete_breeder(breeder_id)`:
    -   Deletes a breeder from the database.
    -   `breeder_id` (int): The ID of the breeder to delete.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure (e.g., breeder not found, or if there are strains associated with this breeder).

**Example Usage:**

```python
from app.handlers.breeder_handlers import get_breeders, add_breeder, update_breeder, delete_breeder

# Get all breeders
all_breeders = get_breeders()
print(f"All Breeders: {all_breeders}")

# Add a new breeder
new_breeder_data = {"name": "New Seed Co."}
add_result = add_breeder(new_breeder_data)
print(f"Add Breeder Result: {add_result}")

# Update a breeder (assuming ID 1 exists)
update_result = update_breeder(1, {"name": "Updated Seed Co."})
print(f"Update Breeder Result: {update_result}")

# Delete a breeder (assuming ID 2 exists and has no associated strains)
delete_result = delete_breeder(2)
print(f"Delete Breeder Result: {delete_result}")
```
#### app/handlers/clone_handlers.py

This module provides functions for managing clone plants within the CultivAR application. It includes functionalities for retrieving available parent plants, creating new clones, managing clone lineage, and retrieving clone statistics.

**Functions:**

-   `get_available_parent_plants()`:
    -   Retrieves all plants that can be used as parent plants for cloning.
    -   Only living plants (status IDs 1, 2, 3) are considered valid parents.
    -   Returns a `list` of dictionaries, each containing information about a parent plant (ID, name, strain, status, etc.).
-   `create_clones(parent_id, clone_data_list, user_id)`:
    -   Creates multiple clone plants from a specified parent plant.
    -   `parent_id` (int): The ID of the parent plant.
    -   `clone_data_list` (list): A list of dictionaries, each containing data for a new clone (name, description, zone, start date).
    -   `user_id` (int): The ID of the user performing the action.
    -   Returns a `dict` with the success status, created clone information, and any errors encountered.
-   `get_clone_lineage(plant_id)`:
    -   Retrieves the complete clone lineage (parents and children) for a given plant.
    -   `plant_id` (int): The ID of the plant.
    -   Returns a `dict` containing lineage information, including the plant itself, its parent, grandparent (if applicable), siblings, and children.
-   `get_clone_statistics()`:
    -   Retrieves statistics related to clone plants, such as total clones created, successful clones, failed clones, success rate, and top parent plants.
    -   Returns a `dict` containing the clone statistics.
-   `get_all_clones()`:
    -   Retrieves all clone plants with their parent information.
    -   Returns a `list` of dictionaries, each containing information about a clone plant.
-   `delete_clone(clone_id, user_id)`:
    -   Deletes a clone plant from the database.
    -   `clone_id` (int): The ID of the clone to delete.
    -   `user_id` (int): The ID of the user performing the action.
    -   Returns a `dict` with the success status and a message.

**Example Usage:**

```python
from app.handlers.clone_handlers import get_available_parent_plants, create_clones, get_clone_lineage

# Get available parent plants
parent_plants = get_available_parent_plants()
print(f"Available Parent Plants: {parent_plants}")

# Create clones from a parent plant (assuming parent plant ID is 1)
clone_data_list = [
    {"name": "Clone 1", "description": "First clone"},
    {"name": "Clone 2", "description": "Second clone"},
]
create_result = create_clones(1, clone_data_list, user_id=1)
print(f"Create Clones Result: {create_result}")

# Get clone lineage (assuming clone ID is 2)
lineage_result = get_clone_lineage(2)
print(f"Clone Lineage: {lineage_result}")
```
#### app/handlers/export_handlers.py

This module provides functions for exporting data from the CultivAR application in various formats (CSV, JSON, ZIP). It includes functions for exporting data related to plants, strains, activities, users, and sensors, as well as creating complete system backups.

**Functions:**

-   `export_activities_csv()`:
    -   Exports activity data to CSV format.
    -   Returns a `str` containing the CSV data.
-   `export_complete_backup()`:
    -   Creates a complete system backup as a ZIP file.
    -   Returns a `BytesIO` object containing the ZIP data.
-   `export_plants_csv()`:
    -   Exports plant data to CSV format.
    -   Returns a `str` containing the CSV data.
-   `export_plants_json()`:
    -   Exports plant data to JSON format.
    -   Returns a `str` containing the JSON data.
-   `export_sensors_csv()`:
    -   Exports sensor data to CSV format.
    -   Returns a `str` containing the CSV data.
-   `export_strains_csv()`:
    -   Exports strain data to CSV format.
    -   Returns a `str` containing the CSV data.
-   `export_strains_json()`:
    -   Exports strain data to JSON format.
    -   Returns a `str` containing the JSON data.
-   `export_users_csv()`:
    -   Exports user data to CSV format.
    -   Returns a `str` containing the CSV data.
-   `get_export_statistics()`:
    -   Retrieves statistics related to data exports.
    -   Returns a `dict` containing the export statistics.

**Example Usage:**

```python
from app.handlers.export_handlers import export_plants_csv, export_users_csv

# Export plant data to CSV
plant_csv_data = export_plants_csv()
print(f"Plant CSV Data: {plant_csv_data[:100]}...")  # Print first 100 chars

# Export user data to CSV
user_csv_data = export_users_csv()
print(f"User CSV Data: {user_csv_data[:100]}...")  # Print first 100 chars
```

#### app/handlers/plant_handlers.py

This module provides functions for managing plant-related operations within the CultivAR application. It includes functionalities for retrieving plant data, managing plant status, linking sensors, uploading images, and recording plant activities.

**Functions:**

-   `get_plant(plant_id)`:
    -   Retrieves a specific plant by its ID.
    -   `plant_id` (int): The ID of the plant to retrieve.
    -   Returns a `dict` containing detailed plant information, including measurements, activities, status history, and images. Returns `None` if the plant is not found.
-   `get_living_plants()`:
    -   Retrieves all living plants (status IDs not in [4, 5]).
    -   Returns a `list` of dictionaries, each containing information about a living plant.
-   `get_harvested_plants()`:
    -   Retrieves all harvested plants (status ID 4).
    -   Returns a `list` of dictionaries, each containing information about a harvested plant.
-   `get_dead_plants()`:
    -   Retrieves all dead plants (status ID 5).
    -   Returns a `list` of dictionaries, each containing information about a dead plant.
-   `get_plants_by_strain(strain_id)`:
    -   Retrieves all plants associated with a specific strain.
    -   `strain_id` (int): The ID of the strain.
    -   Returns a `list` of dictionaries, each containing information about a plant of the specified strain.
-   `add_plant(data)`:
    -   Adds a new plant to the database.
    -   `data` (dict): A dictionary containing the plant's data (name, description, status, strain, zone, etc.).
    -   Returns `{"success": True, "id": int}` on success, `{"success": False, "error": str}` on failure.
-   `update_plant(data)`:
    -   Updates an existing plant's information.
    -   `data` (dict): A dictionary containing the plant's updated data (ID, name, description, status, strain, zone, etc.).
    -   Returns `{"success": True, "plant_id": int}` on success, `{"success": False, "error": str}` on failure.
-   `delete_plant(plant_id)`:
    -   Deletes a plant from the database, including associated images, activities, measurements, and status history.
    -   `plant_id` (int): The ID of the plant to delete.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `link_sensors_to_plant(data)`:
    -   Links sensors to a specific plant.
    -   `data` (dict): A dictionary containing the `plant_id` and a list of `sensor_ids`.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `upload_plant_images(plant_id, files, description)`:
    -   Uploads images for a plant.
    -   `plant_id` (int): The ID of the plant.
    -   `files` (list): A list of image files to upload.
    -   `description` (str): A description for the images.
    -   Returns `{"success": True, "images": list}` on success, `{"success": False, "error": str}` on failure.
-   `delete_plant_image(image_id)`:
    -   Deletes a plant image.
    -   `image_id` (int): The ID of the image to delete.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `record_activity(data)`:
    -   Records a plant activity.
    -   `data` (dict): A dictionary containing the activity data (plant_id, activity_id, note).
    -   Returns `{"success": True, "activity_id": int, "message": str}` on success, `{"success": False, "error": str}` on failure.

**Example Usage:**

```python
from app.handlers.plant_handlers import get_plant, add_plant, update_plant

# Get a plant by ID
plant_data = get_plant(1)
print(f"Plant Data: {plant_data}")

# Add a new plant
new_plant_data = {"name": "Test Plant", "strain_id": 1, "zone_id": 1}
add_result = add_plant(new_plant_data)
print(f"Add Plant Result: {add_result}")

# Update a plant (assuming plant ID is 1)
update_data = {"id": 1, "name": "Updated Plant Name", "status_id": 2}
update_result = update_plant(update_data)
print(f"Update Plant Result: {update_result}")
```

#### app/handlers/sensor_handlers.py

This module provides functions for managing sensors and sensor data within the CultivAR application. It includes functionalities for retrieving sensor information, scanning for new sensors from AC Infinity and Ecowitt devices, editing sensor properties, and deleting sensors.

**Functions:**

-   `get_sensors()`:
    -   Retrieves all sensors from the database.
    -   Returns a `list` of dictionaries, each containing information about a sensor (ID, name, zone, source, device, type, unit, creation/update dates, and the latest reading).
-   `get_grouped_sensors_with_latest_reading()`:
    -   Retrieves sensors grouped by zone, along with their latest readings.
    -   Returns a `dict` where keys are zone names and values are lists of sensor dictionaries.
-   `get_sensor_data(sensor_id, start_date=None, end_date=None)`:
    -   Retrieves sensor data for a specific sensor within a specified date range.
    -   `sensor_id` (int): The ID of the sensor.
    -   `start_date` (str, optional): The start date for the data (YYYY-MM-DD). Defaults to 7 days ago.
    -   `end_date` (str, optional): The end date for the data (YYYY-MM-DD). Defaults to now.
    -   Returns a `dict` containing sensor information and a list of data points (date and value).
-   `scan_ac_infinity_sensors()`:
    -   Scans for AC Infinity sensors using the AC Infinity API.
    -   Requires a valid AC Infinity token.
    -   Creates or updates AC Infinity devices and sensors in the database.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `scan_ecowitt_sensors()`:
    -   Scans for Ecowitt sensors by querying an Ecowitt server.
    -   Creates or updates Ecowitt devices and sensors in the database.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `edit_sensor(data)`:
    -   Edits an existing sensor's properties (name, zone, show).
    -   `data` (dict): A dictionary containing the sensor's updated data (ID, name, zone_id, show).
    -   Returns `{"success": True, "sensor_id": int}` on success, `{"success": False, "error": str}` on failure.
-   `delete_sensor(sensor_id)`:
    -   Deletes a sensor from the database, including associated sensor data.
    -   `sensor_id` (int): The ID of the sensor to delete.
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `get_sensor_unit(sensor_type)`:
    -   Retrieves the unit for a given sensor type.
    -   `sensor_type` (str): The sensor type (e.g., "temperature", "humidity").
    -   Returns a `str` representing the unit (e.g., "°F", "%").

**Example Usage:**

```python
from app.handlers.sensor_handlers import get_sensors, get_sensor_data

# Get all sensors
all_sensors = get_sensors()
print(f"All Sensors: {all_sensors}")

# Get sensor data for sensor ID 1
sensor_data = get_sensor_data(1)
print(f"Sensor Data: {sensor_data}")
```

#### app/handlers/settings_handlers.py

This module provides functions for managing application settings, including retrieving, updating, and saving settings, as well as handling user password updates and logo uploads.

**Functions:**

-   `get_settings()`:
    -   Retrieves all application settings from the database.
    -   Returns a `dict` containing formatted settings for AC Infinity, Ecowitt, polling intervals, guest mode, and stream grabbing.
-   `get_setting(key)`:
    -   Retrieves a specific setting by its key.
    -   `key` (str): The key of the setting to retrieve.
    -   Returns the setting `value` (str) if found, otherwise `None`.
-   `update_setting(key, value)`:
    -   Updates or creates a setting in the database.
    -   `key` (str): The key of the setting to update.
    -   `value` (str): The new value for the setting.
    -   Returns `True` on success, `False` on failure.
-   `exists_setting(key)`:
    -   Checks if a setting exists in the database.
    -   `key` (str): The key of the setting to check.
    -   Returns `True` if the setting exists, `False` otherwise.
-   `save_settings(data)`:
    -   Saves multiple settings to the database.
    -   `data` (dict): A dictionary containing the settings data (AC Infinity, Ecowitt, polling interval, guest mode, etc.).
    -   Returns `{"success": True}` on success, `{"success": False, "error": str}` on failure.
-   `update_user_password(user_id, password)`:
    -   Updates a user's password in the database.
    -   `user_id` (int): The ID of the user to update.
    -   `password` (str): The new password.
    -   Returns `True` on success, `False` on failure.
-   `upload_logo(file)`:
    -   Uploads a logo image file to the server and updates the logo setting in the database.
    -   `file`: The logo file to upload.
    -   Returns `{"success": True, "logo_path": str}` on success, `{"success": False, "error": str}` on failure.

**Example Usage:**

```python
from app.handlers.settings_handlers import get_settings, update_setting

# Get all settings
all_settings = get_settings()
print(f"All Settings: {all_settings}")

# Update a setting
update_result = update_setting("polling_interval", "600")
print(f"Update Setting Result: {update_result}")
```

#### app/handlers/strain_handlers.py

This module provides functions for managing plant strains within the CultivAR application. It includes functionalities for retrieving strain information, adding new strains, and handling strain-related data.

**Functions:**

-   `get_strains()`:
    -   Retrieves all plant strains from the database.
    -   Returns a `list` of dictionaries, each containing information about a strain (ID, name, breeder, indica/sativa percentages, etc.).
-   `add_strain(data)`:
    -   Adds a new plant strain to the database.
    -   `data` (dict): A dictionary containing the strain's data (name, breeder, indica/sativa percentages, etc.).
    -   Returns `{"success": True, "id": int}` on success, `{"success": False, "error": str}` on failure.

**Example Usage:**

```python
from app.handlers.strain_handlers import get_strains

# Get all strains
all_strains = get_strains()
print(f"All Strains: {all_strains}")
```

#### app/handlers/user_handlers.py

This module provides functions for managing users within the CultivAR application. It includes functionalities for retrieving user information, creating new users, updating existing users, deleting users, toggling admin status, forcing password resets, and retrieving user statistics.

**Functions:**

-   `get_all_users()`:
    -   Retrieves all users from the database with their details and activity summary.
    -   Returns a `list` of dictionaries, each containing information about a user (ID, username, phone, email, admin status, creation/update dates, activity count, last activity timestamp, and status).
-   `get_user_by_id(user_id)`:
    -   Retrieves a specific user by their ID with detailed information.
    -   `user_id` (int): The ID of the user to retrieve.
    -   Returns a `dict` containing detailed user information, including recent activities. Returns `None` if the user is not found.
-   `create_user(data)`:
    -   Creates a new user in the database.
    -   `data` (dict): A dictionary containing the user's data (username, password, phone/email, and role info).
    -   Returns `{"success": True, "user_id": int, "message": str}` on success, `{"success": False, "error": str}` on failure.
-   `update_user(user_id, data)`:
    -   Updates an existing user's information.
    -   `user_id` (int): The ID of the user to update.
    -   `data` (dict): A dictionary containing the updated user data.
    -   Returns `{"success": True, "message": str}` on success, `{"success": False, "error": str}` on failure.
-   `delete_user(user_id)`:
    -   Deletes a user from the database (soft delete by deactivating).
    -   `user_id` (int): The ID of the user to delete.
    -   Returns `{"success": True, "message": str}` on success, `{"success": False, "error": str}` on failure.
-   `toggle_user_admin_status(user_id)`:
    -   Toggles the admin status for a user.
    -   `user_id` (int): The ID of the user.
    -   Returns `{"success": True, "message": str}` on success, `{"success": False, "error": str}` on failure.
-   `force_password_reset(user_id)`:
    -   Forces a user to reset their password on the next login.
    -   `user_id` (int): The ID of the user.
    -   Returns `{"success": True, "message": str}` on success, `{"success": False, "error": str}` on failure.
-   `get_user_statistics()`:
    -   Retrieves user statistics for the admin dashboard.
    -   Returns a `dict` containing the user statistics (total users, admin users, regular users, users needing password reset, and recent registrations).

**Example Usage:**

```python
from app.handlers.user_handlers import get_all_users, create_user, update_user

# Get all users
all_users = get_all_users()
print(f"All Users: {all_users}")

# Create a new user
new_user_data = {"username": "testuser", "password": "password123", "email": "test@example.com"}
create_result = create_user(new_user_data)
print(f"Create User Result: {create_result}")

# Update a user (assuming user ID is 1)
update_data = {"user_id": 1, "username": "updateduser", "email": "updated@example.com"}
update_result = update_user(1, update_data)
print(f"Update User Result: {update_result}")
```

### Logger

#### app/logger/logger.py

This module configures and provides a logger instance for the CultivAR application. It sets up basic logging to a file and allows for customization of log levels and formatting.

**Functions:**

-   The module directly configures the logger; there are no exported functions for direct use.

**Example Usage:**

```python
from app.logger import logger

logger.info("This is an informational message.")
logger.error("This is an error message.")
```

### Models

#### app/models/__init__.py

This file initializes the database and imports the various model definitions for the CultivAR application. It also includes functions for database migration and initial data seeding.

**Functions:**

-   `init_db()`:
    -   Initializes the database with default data (activities, metrics, statuses, zones, strains, breeders).
    -   This function is called during application startup to ensure the database is properly seeded.
-   `migrate_db()`:
    -   Applies database migrations using Flask-Migrate.
    -   This function is used to update the database schema when changes are made to the models.

**Example Usage:**

```python
from app.models import db, init_db

# Initialize the database
with app.app_context():
    db.create_all()
    init_db()
```

#### app/models/acinfinity_models.py

This module defines the SQLAlchemy models for AC Infinity devices and tokens. These models are used to interact with the AC Infinity API and store device and authentication information in the database.

**Classes:**

-   `ACInfinityDevice`:
    -   Represents an AC Infinity device.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `device_id` (str): Unique device ID from AC Infinity API.
        -   `name` (str): Device name.
        -   `type` (str): Device type.
        -   `status` (str): Device status.
-   `ACInfinityToken`:
    -   Represents an AC Infinity API token.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `access_token` (str): The access token.
        -   `refresh_token` (str): The refresh token.
        -   `expires_at` (datetime): Expiration timestamp.
        -   `created_at` (datetime): Creation timestamp.

**Example Usage:**

```python
from app.models.acinfinity_models import ACInfinityDevice, ACInfinityToken

# Create a new AC Infinity device
new_device = ACInfinityDevice(device_id="12345", name="Test Fan", type="Fan", status="online")
db.session.add(new_device)
db.session.commit()

# Get the latest AC Infinity token
token = ACInfinityToken.query.order_by(ACInfinityToken.created_at.desc()).first()
```

#### app/models/base_models.py

This module defines the core SQLAlchemy models for the CultivAR application. These models represent the fundamental entities in the application's domain, such as users, plants, strains, zones, activities, and sensor data.

**Classes:**

-   `User`:
    -   Represents a user account.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `username` (str): User's username.
        -   `password_hash` (str): Hashed password.
        -   `phone` (str): User's phone number.
        -   `email` (str): User's email address.
        -   `is_admin` (bool): Flag indicating admin privileges.
        -   `force_password_change` (bool): Flag indicating if the user must reset their password.
        -   `created_at` (datetime): Timestamp of account creation.
        -   `updated_at` (datetime): Timestamp of last update.
    -   Methods:
        -   `set_password(password)`: Hashes and sets the user's password.
        -   `check_password(password)`: Checks if the provided password matches the stored hash.
-   `Plant`:
    -   Represents a plant.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `name` (str): Plant name.
        -   `description` (str): Plant description.
        -   `status_id` (int): Foreign key to `Status`.
        -   `strain_id` (int): Foreign key to `Strain`.
        -   `zone_id` (int): Foreign key to `Zone`.
        -   `is_clone` (bool): Flag indicating if the plant is a clone.
        -   `start_dt` (datetime): Start date.
        -   `current_week` (int): Current week in growth cycle.
        -   `current_day` (int): Current day in growth cycle.
        -   `last_water_date` (datetime): Last watering date.
        -   `last_feed_date` (datetime): Last feeding date.
        -   `harvest_weight` (float): Harvest weight.
        -   `harvest_date` (datetime): Harvest date.
        -   `cycle_time` (int): Total cycle time.
        -   `strain_url` (str): URL for strain information.
        -   `autoflower` (bool): Flag indicating if the plant is an autoflower.
        -   `parent_id` (int): Foreign key to parent plant (if clone).
-   `Strain`:
    -   Represents a plant strain.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `name` (str): Strain name.
        -   `breeder_id` (int): Foreign key to `Breeder`.
        -   `indica` (int): Indica percentage.
        -   `sativa` (int): Sativa percentage.
        -   `autoflower` (bool): Flag indicating if the strain is an autoflower.
        -   `cycle_time` (int): Typical cycle time in days.
        -   `seed_count` (int): Number of seeds.
        -   `url` (str): URL for strain information.
        -   `description` (str): Strain description.
-   `Zone`:
    -   Represents a growing zone.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `name` (str): Zone name.
-   `Activity`:
    -   Represents a type of plant activity.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `name` (str): Activity name.
-   `PlantActivity`:
    -   Represents a specific activity performed on a plant.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `plant_id` (int): Foreign key to `Plant`.
        -   `activity_id` (int): Foreign key to `Activity`.
        -   `name` (str): Activity name.
        -   `note` (str): Activity note.
        -   `date` (datetime): Activity date.
-   `Measurement`:
    -   Represents a measurement taken for a plant.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `plant_id` (int): Foreign key to `Plant`.
        -   `name` (str): Measurement name.
        -   `value` (float): Measurement value.
        -   `date` (datetime): Measurement date.
-   `PlantImage`:
    -   Represents an image associated with a plant.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `plant_id` (int): Foreign key to `Plant`.
        -   `image_path` (str): Path to the image file.
        -   `image_description` (str): Image description.
        -   `image_order` (int): Image order.
        -   `image_date` (datetime): Image date.
-   `Status`:
    -   Represents the status of a plant.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `plant_id` (int): Foreign key to `Plant`.
        -   `status` (str): Status name.
        -   `date` (datetime): Status date.
-   `Breeder`:
    -   Represents a plant breeder.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `name` (str): Breeder name.

**Example Usage:**

```python
from app.models.base_models import User, Plant, Strain

# Create a new user
new_user = User(username="testuser", password="password123", email="test@example.com")
db.session.add(new_user)
db.session.commit()

# Create a new plant
new_plant = Plant(name="Test Plant", strain_id=1, zone_id=1)
db.session.add(new_plant)
db.session.commit()
```

#### app/models/ecowitt_models.py

This module defines the SQLAlchemy models for Ecowitt devices. These models are used to interact with Ecowitt weather station data and store device information in the database.

**Classes:**

-   `EcowittDevice`:
    -   Represents an Ecowitt weather station device.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `device_id` (str): Unique device ID from Ecowitt.
        -   `name` (str): Device name.
        -   `ip_address` (str): IP address of the Ecowitt server.
        -   `mac_address` (str): MAC address of the Ecowitt device.

**Example Usage:**

```python
from app.models.ecowitt_models import EcowittDevice

# Create a new Ecowitt device
new_device = EcowittDevice(device_id="ABCDEF123456", name="My Weather Station", ip_address="192.168.1.100", mac_address="AA:BB:CC:DD:EE:FF")
db.session.add(new_device)
db.session.commit()
```

#### app/models/system_models.py

This module defines the SQLAlchemy models for system-related data in the CultivAR application, specifically for tracking system activities.

**Classes:**

-   `SystemActivity`:
    -   Represents a system activity log entry.
    -   Attributes:
        -   `id` (int): Primary key.
        -   `user_id` (int): Foreign key to `User`.
        -   `type` (str): Type of activity (e.g., "login", "plant_add").
        -   `description` (str): Description of the activity.
        -   `details` (str): JSON-serialized details about the activity.
        -   `timestamp` (datetime): Timestamp of the activity.

**Example Usage:**

```python
from app.models.system_models import SystemActivity

# Create a new system activity
new_activity = SystemActivity(user_id=1, type="user_login", description="User logged in", timestamp=datetime.now())
db.session.add(new_activity)
db.session.commit()
```

### Routes

#### app/routes/routes.py

This module defines the main routes for the CultivAR application. It registers the route handlers for various pages and functionalities.

**Functions:**

-   `register_routes(app)`:
    -   Registers the route handlers with the Flask application.
    -   `app` (Flask): The Flask application instance.
    -   This function defines routes for the index page, login page, and other core functionalities.

**Example Usage:**

```python
from app.routes import register_routes

# Register routes with the app
register_routes(app)
```

### Utilities

#### app/utils/auth.py

(Documentation to be generated)

#### app/utils/helpers.py

(Documentation to be generated)

#### app/utils/image.py

(Documentation to be generated)

#### app/utils/rate_limiter.py

(Documentation to be generated)

#### app/utils/validators.py

(Documentation to be generated)

### Watcher

#### app/watcher/watcher.py

(Documentation to be generated)

## How to Use This Documentation

This documentation is structured to provide a clear understanding of the CultivAR codebase.

-   **Table of Contents:** Use the table of contents to quickly navigate to specific modules or sections.
-   **Module Overviews:** Each module section provides a brief description of its purpose, key functions/classes, and relevant routes or API endpoints.
-   **Code Examples:** Where applicable, code snippets are provided to illustrate usage.
-   **"Documentation to be generated"**: For modules marked with this, detailed documentation will be added in subsequent steps.
