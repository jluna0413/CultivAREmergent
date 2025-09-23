# CultivAR Function Reference

## Database Functions

### migrate_db()
Initialize and migrate the database schema.

**Location:** `app/models/__init__.py`

**Description:** Creates all database tables and handles schema migrations.

**Usage:**
```python
from app.models import migrate_db
migrate_db()
```

### init_db()
Initialize the database with default data.

**Location:** `app/models/__init__.py`

**Description:** Adds default activities, metrics, and statuses to the database.

**Usage:**
```python
from app.models import init_db
init_db()
```

## User Model Methods

### set_password(password)
Hash and set the user's password.

**Location:** `app/models/base_models.py`

**Parameters:**
- `password` (str): Plain text password

**Usage:**
```python
user = User(username="john_doe")
user.set_password("secure_password123")
```

### check_password(password)
Verify if the provided password matches the stored hash.

**Location:** `app/models/base_models.py`

**Parameters:**
- `password` (str): Plain text password to verify

**Returns:** `bool`

**Usage:**
```python
if user.check_password("secure_password123"):
    print("Password is correct")
```

## Plant Model Properties

### status_name
Get the current status name.

**Returns:** `str` or `None`

### strain_name
Get the associated strain name.

**Returns:** `str` or `None`

### breeder_name
Get the strain breeder name.

**Returns:** `str` or `None`

### zone_name
Get the growing zone name.

**Returns:** `str` or `None`

### parent_name
Get the parent plant name (for clones).

**Returns:** `str` or `None`

### latest_image
Get the most recent plant image.

**Returns:** `PlantImage` object or `None`

## Plant Handlers

### get_plant(plant_id)
Get detailed information about a specific plant.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `plant_id` (int): The ID of the plant to retrieve

**Returns:** `dict` or `None`

**Usage:**
```python
from app.handlers.plant_handlers import get_plant

plant_data = get_plant(1)
if plant_data:
    print(f"Plant: {plant_data['name']}")
```

### create_plant(plant_data)
Create a new plant.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `plant_data` (dict): Plant data dictionary

**Returns:** `dict` with success status and plant ID or error message

**Usage:**
```python
from app.handlers.plant_handlers import create_plant

plant_data = {
    "name": "Blue Dream #1",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2
}

result = create_plant(plant_data)
if result["success"]:
    print(f"Plant created with ID: {result['plant_id']}")
```

### update_plant(plant_id, plant_data)
Update an existing plant.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `plant_id` (int): The ID of the plant to update
- `plant_data` (dict): Updated plant data

**Returns:** `dict` with success status and message

**Usage:**
```python
from app.handlers.plant_handlers import update_plant

update_data = {
    "name": "Updated Plant Name",
    "current_height": "50cm"
}

result = update_plant(1, update_data)
```

### delete_plant(plant_id)
Delete a plant and all associated data.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `plant_id` (int): The ID of the plant to delete

**Returns:** `dict` with success status and message

**Usage:**
```python
from app.handlers.plant_handlers import delete_plant

result = delete_plant(1)
```

### add_measurement(measurement_data)
Add a new measurement to a plant.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `measurement_data` (dict): Measurement data dictionary

**Returns:** `dict` with success status and measurement ID or error message

**Usage:**
```python
from app.handlers.plant_handlers import add_measurement

measurement_data = {
    "plant_id": 1,
    "metric_id": 1,
    "name": "Height Measurement",
    "value": 45.5
}

result = add_measurement(measurement_data)
```

### add_activity(activity_data)
Add a new activity to a plant.

**Location:** `app/handlers/plant_handlers.py`

**Parameters:**
- `activity_data` (dict): Activity data dictionary

**Returns:** `dict` with success status and activity ID or error message

**Usage:**
```python
from app.handlers.plant_handlers import add_activity

activity_data = {
    "plant_id": 1,
    "activity_id": 1,
    "name": "Watering",
    "note": "Regular watering"
}

result = add_activity(activity_data)
```

## Sensor Handlers

### get_sensors()
Get all sensors in the system.

**Location:** `app/handlers/sensor_handlers.py`

**Returns:** `list` of sensor objects

**Usage:**
```python
from app.handlers.sensor_handlers import get_sensors

sensors = get_sensors()
for sensor in sensors:
    print(f"Sensor: {sensor['name']}")
```

### create_sensor(sensor_data)
Create a new sensor.

**Location:** `app/handlers/sensor_handlers.py`

**Parameters:**
- `sensor_data` (dict): Sensor data dictionary

**Returns:** `dict` with success status and sensor ID or error message

**Usage:**
```python
from app.handlers.sensor_handlers import create_sensor

sensor_data = {
    "name": "Temperature Sensor",
    "type": "temperature",
    "unit": "°C",
    "zone_id": 1
}

result = create_sensor(sensor_data)
```

### delete_sensor(sensor_id)
Delete a sensor and its data.

**Location:** `app/handlers/sensor_handlers.py`

**Parameters:**
- `sensor_id` (int): The ID of the sensor to delete

**Returns:** `dict` with success status and message

**Usage:**
```python
from app.handlers.sensor_handlers import delete_sensor

result = delete_sensor(1)
```

## User Handlers

### get_all_users()
Get all users in the system (admin only).

**Location:** `app/handlers/user_handlers.py`

**Returns:** `list` of user objects

**Usage:**
```python
from app.handlers.user_handlers import get_all_users

users = get_all_users()
for user in users:
    print(f"User: {user['username']}")
```

### create_user(user_data)
Create a new user.

**Location:** `app/handlers/user_handlers.py`

**Parameters:**
- `user_data` (dict): User data dictionary

**Returns:** `dict` with success status and user ID or error message

**Usage:**
```python
from app.handlers.user_handlers import create_user

user_data = {
    "username": "new_user",
    "password": "password123",
    "email": "user@example.com",
    "is_admin": False
}

result = create_user(user_data)
```

### update_user(user_id, user_data)
Update an existing user.

**Location:** `app/handlers/user_handlers.py`

**Parameters:**
- `user_id` (int): The ID of the user to update
- `user_data` (dict): Updated user data

**Returns:** `dict` with success status and message

**Usage:**
```python
from app.handlers.user_handlers import update_user

update_data = {
    "email": "newemail@example.com",
    "is_admin": True
}

result = update_user(1, update_data)
```

### delete_user(user_id)
Delete a user.

**Location:** `app/handlers/user_handlers.py`

**Parameters:**
- `user_id` (int): The ID of the user to delete

**Returns:** `dict` with success status and message

**Usage:**
```python
from app.handlers.user_handlers import delete_user

result = delete_user(1)
```

## Export Handlers

### export_plants_csv()
Export all plants data as CSV format.

**Location:** `app/handlers/export_handlers.py`

**Returns:** `BytesIO` object containing CSV data

**Usage:**
```python
from app.handlers.export_handlers import export_plants_csv

csv_data = export_plants_csv()
with open("plants_export.csv", "wb") as f:
    f.write(csv_data.getvalue())
```

### export_plants_json()
Export all plants data as JSON format.

**Location:** `app/handlers/export_handlers.py`

**Returns:** `BytesIO` object containing JSON data

**Usage:**
```python
from app.handlers.export_handlers import export_plants_json

json_data = export_plants_json()
with open("plants_export.json", "wb") as f:
    f.write(json_data.getvalue())
```

### export_activities_csv()
Export all plant activities as CSV format.

**Location:** `app/handlers/export_handlers.py`

**Returns:** `BytesIO` object containing CSV data

**Usage:**
```python
from app.handlers.export_handlers import export_activities_csv

csv_data = export_activities_csv()
with open("activities_export.csv", "wb") as f:
    f.write(csv_data.getvalue())
```

### export_complete_backup()
Export complete database backup.

**Location:** `app/handlers/export_handlers.py`

**Returns:** `BytesIO` object containing backup data

**Usage:**
```python
from app.handlers.export_handlers import export_complete_backup

backup_data = export_complete_backup()
with open("backup.zip", "wb") as f:
    f.write(backup_data.getvalue())
```

## Utility Functions

### Date and Time Functions

#### format_date(date)
Format a date as a string in MM/DD/YYYY format.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `date` (datetime): The date to format

**Returns:** `str`

**Usage:**
```python
from app.utils.helpers import format_date
from datetime import datetime

date = datetime(2024, 1, 15)
formatted = format_date(date)  # Returns "01/15/2024"
```

#### format_datetime(date)
Format a datetime as a string in MM/DD/YYYY HH:MM AM/PM format.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `date` (datetime): The datetime to format

**Returns:** `str`

**Usage:**
```python
from app.utils.helpers import format_datetime
from datetime import datetime

dt = datetime(2024, 1, 15, 14, 30)
formatted = format_datetime(dt)  # Returns "01/15/2024 02:30 PM"
```

#### parse_date(date_str)
Parse a date string into a datetime object.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `date_str` (str): The date string to parse

**Returns:** `datetime` or `None`

**Usage:**
```python
from app.utils.helpers import parse_date

date = parse_date("2024-01-15")  # Returns datetime object
```

#### calculate_days_since(date)
Calculate the number of days since a given date.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `date` (datetime): The reference date

**Returns:** `int` or `None`

**Usage:**
```python
from app.utils.helpers import calculate_days_since
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(days=30)
days = calculate_days_since(start_date)  # Returns 30
```

#### calculate_weeks_since(date)
Calculate the number of weeks since a given date.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `date` (datetime): The reference date

**Returns:** `int` or `None`

**Usage:**
```python
from app.utils.helpers import calculate_weeks_since
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(weeks=4)
weeks = calculate_weeks_since(start_date)  # Returns 4
```

### File and Image Functions

#### is_valid_image(filename)
Check if a file is a valid image based on its extension.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `filename` (str): The filename to check

**Returns:** `bool`

**Usage:**
```python
from app.utils.helpers import is_valid_image

is_valid_image("photo.jpg")  # Returns True
is_valid_image("document.pdf")  # Returns False
```

#### get_file_extension(filename)
Get the file extension from a filename.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `filename` (str): The filename to get the extension from

**Returns:** `str`

**Usage:**
```python
from app.utils.helpers import get_file_extension

ext = get_file_extension("photo.JPG")  # Returns ".jpg"
```

### Text Functions

#### slugify(text)
Convert a string to a URL-friendly slug.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `text` (str): The text to convert

**Returns:** `str`

**Usage:**
```python
from app.utils.helpers import slugify

slug = slugify("Blue Dream Strain")  # Returns "blue-dream-strain"
```

### Network Functions

#### get_client_ip()
Get the client's IP address from the request.

**Location:** `app/utils/helpers.py`

**Returns:** `str`

**Usage:**
```python
from app.utils.helpers import get_client_ip

ip = get_client_ip()  # Returns "192.168.1.100"
```

### Plant-Specific Functions

#### estimate_harvest_date(start_date, cycle_time, autoflower=False)
Estimate the harvest date based on start date and cycle time.

**Location:** `app/utils/helpers.py`

**Parameters:**
- `start_date` (datetime): The plant start date
- `cycle_time` (int): The cycle time in days
- `autoflower` (bool): Whether the plant is an autoflower

**Returns:** `datetime` or `None`

**Usage:**
```python
from app.utils.helpers import estimate_harvest_date
from datetime import datetime

start_date = datetime(2024, 1, 1)
harvest_date = estimate_harvest_date(start_date, 70, autoflower=True)
```

## Route Registration Functions

### register_routes(app)
Register all routes for the application.

**Location:** `app/routes/routes.py`

**Parameters:**
- `app`: The Flask application instance

**Usage:**
```python
from app.routes.routes import register_routes

register_routes(app)
```

### register_basic_routes(app)
Register basic routes that don't require authentication.

**Location:** `app/routes/routes.py`

**Parameters:**
- `app`: The Flask application instance

**Usage:**
```python
from app.routes.routes import register_basic_routes

register_basic_routes(app)
```

## Configuration Functions

### Config
Application configuration class.

**Location:** `app/config/config.py`

**Usage:**
```python
from app.config.config import Config

app.config.from_object(Config)
```

## Logging Functions

### logger
Application logger instance.

**Location:** `app/logger/__init__.py`

**Usage:**
```python
from app.logger import logger

logger.info("Information message")
logger.error("Error message")
logger.warning("Warning message")
```
