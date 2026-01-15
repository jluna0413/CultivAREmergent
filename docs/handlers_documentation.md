# CultivAR Handlers Documentation

## Handler Functions

### Plant Handlers

#### get_plant(plant_id)
Get detailed information about a specific plant.

**Parameters:**
- `plant_id` (int): The ID of the plant to retrieve

**Returns:**
- `dict`: Complete plant data including measurements, activities, and images, or None if not found

**Data Structure:**
```python
{
    "id": 1,
    "name": "Blue Dream #1",
    "description": "First Blue Dream plant",
    "status": "Vegetative",
    "status_id": 2,
    "strain_name": "Blue Dream",
    "strain_id": 1,
    "breeder_name": "Humboldt Seeds",
    "zone_name": "Tent 1",
    "zone_id": 1,
    "current_day": 45,
    "current_week": 6,
    "current_height": "45cm",
    "height_date": "2024-01-15T10:30:00Z",
    "last_water_date": "2024-01-14T08:00:00Z",
    "last_feed_date": "2024-01-12T08:00:00Z",
    "days_since_watering": 1,
    "days_since_feeding": 3,
    "measurements": [...],
    "activities": [...],
    "images": [...],
    "status_history": [...]
}
```

#### create_plant(plant_data)
Create a new plant.

**Parameters:**
- `plant_data` (dict): Plant data dictionary

**Required Fields:**
- `name` (str): Plant name
- `status_id` (int): Growth status ID

**Optional Fields:**
- `description` (str): Plant description
- `strain_id` (int): Associated strain ID
- `zone_id` (int): Growing zone ID
- `is_clone` (bool): Clone indicator
- `autoflower` (bool): Autoflowering type

**Returns:**
- `dict`: Result with success status and plant ID or error message

**Example:**
```python
plant_data = {
    "name": "Blue Dream #1",
    "description": "First Blue Dream plant",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2,
    "is_clone": False,
    "autoflower": False
}

result = create_plant(plant_data)
if result["success"]:
    print(f"Plant created with ID: {result['plant_id']}")
else:
    print(f"Error: {result['error']}")
```

#### update_plant(plant_id, plant_data)
Update an existing plant.

**Parameters:**
- `plant_id` (int): The ID of the plant to update
- `plant_data` (dict): Updated plant data

**Returns:**
- `dict`: Result with success status and message

**Example:**
```python
update_data = {
    "name": "Updated Plant Name",
    "description": "Updated description",
    "current_height": "50cm"
}

result = update_plant(1, update_data)
if result["success"]:
    print("Plant updated successfully")
else:
    print(f"Error: {result['error']}")
```

#### delete_plant(plant_id)
Delete a plant and all associated data.

**Parameters:**
- `plant_id` (int): The ID of the plant to delete

**Returns:**
- `dict`: Result with success status and message

**Note:**
- Deletes plant, measurements, activities, and images
- Cannot be undone

### Sensor Handlers

#### get_sensors()
Get all sensors in the system.

**Returns:**
- `list`: List of sensor objects with zone information

**Data Structure:**
```python
[
    {
        "id": 1,
        "name": "Temperature Sensor",
        "type": "temperature",
        "unit": "°C",
        "zone_name": "Tent 1",
        "zone_id": 1,
        "source": "AC Infinity",
        "device": "Controller 69",
        "show": True
    }
]
```

#### create_sensor(sensor_data)
Create a new sensor.

**Parameters:**
- `sensor_data` (dict): Sensor data dictionary

**Required Fields:**
- `name` (str): Sensor name
- `type` (str): Sensor type

**Optional Fields:**
- `unit` (str): Measurement unit
- `zone_id` (int): Associated zone ID
- `source` (str): Data source
- `device` (str): Device type
- `show` (bool): Display flag

**Returns:**
- `dict`: Result with success status and sensor ID or error message

#### delete_sensor(sensor_id)
Delete a sensor and its data.

**Parameters:**
- `sensor_id` (int): The ID of the sensor to delete

**Returns:**
- `dict`: Result with success status and message

### User Handlers

#### get_all_users()
Get all users in the system (admin only).

**Returns:**
- `list`: List of user objects

**Data Structure:**
```python
[
    {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "phone": "+1234567890",
        "is_admin": True,
        "created_at": "2024-01-01T00:00:00Z",
        "force_password_change": False
    }
]
```

#### create_user(user_data)
Create a new user.

**Parameters:**
- `user_data` (dict): User data dictionary

**Required Fields:**
- `username` (str): Username
- `password` (str): Password

**Optional Fields:**
- `email` (str): Email address
- `phone` (str): Phone number
- `is_admin` (bool): Admin privileges
- `force_password_change` (bool): Force password change

**Returns:**
- `dict`: Result with success status and user ID or error message

#### update_user(user_id, user_data)
Update an existing user.

**Parameters:**
- `user_id` (int): The ID of the user to update
- `user_data` (dict): Updated user data

**Returns:**
- `dict`: Result with success status and message

#### delete_user(user_id)
Delete a user.

**Parameters:**
- `user_id` (int): The ID of the user to delete

**Returns:**
- `dict`: Result with success status and message

### Export Handlers

#### export_plants_csv()
Export all plants data as CSV format.

**Returns:**
- `BytesIO`: CSV file data

**CSV Columns:**
- Plant ID, Name, Description, Status, Strain, Zone, Current Day, Current Week, Height, Last Water Date, Last Feed Date, Clone, Autoflower, Start Date, Harvest Weight, Harvest Date

#### export_plants_json()
Export all plants data as JSON format.

**Returns:**
- `BytesIO`: JSON file data

#### export_activities_csv()
Export all plant activities as CSV format.

**Returns:**
- `BytesIO`: CSV file data

#### export_complete_backup()
Export complete database backup.

**Returns:**
- `BytesIO`: Backup file data

**Note:**
- Includes all tables and data
- Admin only function

### Activity Handlers

#### add_activity(activity_data)
Add a new activity to a plant.

**Parameters:**
- `activity_data` (dict): Activity data dictionary

**Required Fields:**
- `plant_id` (int): Plant ID
- `activity_id` (int): Activity type ID
- `name` (str): Activity name

**Optional Fields:**
- `note` (str): Activity notes
- `date` (datetime): Activity date

**Returns:**
- `dict`: Result with success status and activity ID or error message

#### get_plant_activities(plant_id)
Get all activities for a specific plant.

**Parameters:**
- `plant_id` (int): Plant ID

**Returns:**
- `list`: List of activity objects

### Measurement Handlers

#### add_measurement(measurement_data)
Add a new measurement to a plant.

**Parameters:**
- `measurement_data` (dict): Measurement data dictionary

**Required Fields:**
- `plant_id` (int): Plant ID
- `metric_id` (int): Metric type ID
- `name` (str): Measurement name
- `value` (float): Measurement value

**Optional Fields:**
- `date` (datetime): Measurement date

**Returns:**
- `dict`: Result with success status and measurement ID or error message

#### get_plant_measurements(plant_id)
Get all measurements for a specific plant.

**Parameters:**
- `plant_id` (int): Plant ID

**Returns:**
- `list`: List of measurement objects

## Error Handling

All handlers return consistent response formats:

### Success Response
```python
{
    "success": True,
    "message": "Operation completed successfully",
    "data": {...},  # Optional data
    "id": 123  # Optional ID for created/updated items
}
```

### Error Response
```python
{
    "success": False,
    "error": "Error message describing what went wrong"
}
```

## Common Error Types

- **Validation Errors**: Missing required fields, invalid data types
- **Not Found**: Requested resource doesn't exist
- **Permission Errors**: Insufficient privileges
- **Database Errors**: Connection or constraint violations
- **File Errors**: Upload or processing failures

## Usage Examples

### Complete Plant Workflow
```python
from app.handlers.plant_handlers import (
    create_plant,
    get_plant,
    update_plant,
    delete_plant
)

# Create a new plant
plant_data = {
    "name": "Blue Dream #1",
    "description": "First Blue Dream plant",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2,
    "is_clone": False,
    "autoflower": False
}

result = create_plant(plant_data)
if result["success"]:
    plant_id = result["plant_id"]
    
    # Get plant details
    plant = get_plant(plant_id)
    print(f"Created plant: {plant['name']}")
    
    # Update plant
    update_data = {"current_height": "50cm"}
    update_result = update_plant(plant_id, update_data)
    
    # Delete plant (if needed)
    # delete_result = delete_plant(plant_id)
```

### Sensor Management
```python
from app.handlers.sensor_handlers import (
    get_sensors,
    create_sensor,
    delete_sensor
)

# Get all sensors
sensors = get_sensors()
for sensor in sensors:
    print(f"Sensor: {sensor['name']} ({sensor['type']})")

# Create new sensor
sensor_data = {
    "name": "Humidity Sensor",
    "type": "humidity",
    "unit": "%",
    "zone_id": 1
}

result = create_sensor(sensor_data)
if result["success"]:
    print(f"Created sensor with ID: {result['sensor_id']}")
```

### User Management
```python
from app.handlers.user_handlers import (
    get_all_users,
    create_user,
    update_user
)

# Get all users (admin only)
users = get_all_users()
for user in users:
    print(f"User: {user['username']} ({'Admin' if user['is_admin'] else 'User'})")

# Create new user
user_data = {
    "username": "new_grower",
    "password": "secure_password123",
    "email": "grower@example.com",
    "is_admin": False
}

result = create_user(user_data)
if result["success"]:
    print(f"Created user with ID: {result['user_id']}")
```
