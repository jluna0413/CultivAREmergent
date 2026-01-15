# CultivAR API Documentation

## Overview
CultivAR is a Flask-based cannabis cultivation management application.

## Core Models

### User Model
- id: Primary key
- username: Unique username
- password_hash: Hashed password
- phone: Phone number
- email: Email address
- is_admin: Admin privileges
- created_at: Creation timestamp

### Plant Model
- id: Primary key
- name: Plant name
- description: Plant description
- status_id: Growth status
- strain_id: Associated strain
- zone_id: Growing zone
- current_day/week: Growth tracking
- current_height: Current height
- last_water/feed_date: Maintenance tracking
- is_clone: Clone indicator
- autoflower: Autoflowering type

### Strain Model
- id: Primary key
- name: Strain name
- breeder_id: Associated breeder
- indica/sativa: Genetics percentages
- autoflower: Autoflowering type
- cycle_time: Growth cycle duration

### Sensor Model
- id: Primary key
- name: Sensor name
- type: Sensor type
- unit: Measurement unit
- zone_id: Associated zone
- source: Data source

## API Endpoints

### Authentication
- POST /login - User login
- POST /signup - User registration
- GET /logout - User logout

### Plants
- GET /plants - List all plants
- GET /plants/<id> - Get plant details
- POST /plants - Create plant
- PUT /plants/<id> - Update plant
- DELETE /plants/<id> - Delete plant

### Sensors
- GET /sensors - List all sensors
- POST /sensors - Create sensor
- DELETE /sensors/<id> - Delete sensor

### Admin
- GET /admin/users - List all users
- POST /admin/users/create - Create user
- GET /admin/export/* - Export data

## Utility Functions

### Date/Time
- format_date(date) - Format as MM/DD/YYYY
- format_datetime(date) - Format as MM/DD/YYYY HH:MM AM/PM
- parse_date(date_str) - Parse date string
- calculate_days_since(date) - Days since date
- calculate_weeks_since(date) - Weeks since date

### File/Image
- is_valid_image(filename) - Validate image file
- get_file_extension(filename) - Get file extension

### Text
- slugify(text) - Create URL-friendly slug

### Plant
- estimate_harvest_date(start_date, cycle_time, autoflower) - Estimate harvest

## Handler Functions

### Plant Handlers
- get_plant(plant_id) - Get plant details
- create_plant(plant_data) - Create plant
- update_plant(plant_id, plant_data) - Update plant
- delete_plant(plant_id) - Delete plant

### Sensor Handlers
- get_sensors() - List sensors
- create_sensor(sensor_data) - Create sensor
- delete_sensor(sensor_id) - Delete sensor

### User Handlers
- get_all_users() - List users
- create_user(user_data) - Create user
- update_user(user_id, user_data) - Update user
- delete_user(user_id) - Delete user

### Export Handlers
- export_plants_csv() - Export plants as CSV
- export_plants_json() - Export plants as JSON
- export_complete_backup() - Full backup

## Response Format
{
    "success": true/false,
    "message": "Status message",
    "data": {...} // Optional data
}

## Error Codes
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error
