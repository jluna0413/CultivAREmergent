# CultivAR API Endpoints Documentation

## Authentication Endpoints

### POST /login
Handle user login.

**Request Body:**
```json
{
    "username": "john_doe",
    "password": "secure_password123"
}
```

**Response:**
- Success: Redirect to dashboard
- Error: Flash message with error details

**Example:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=secure_password123"
```

### POST /signup
Handle user registration.

**Request Body:**
```json
{
    "phone": "+1234567890",
    "email": "john@example.com",
    "password": "secure_password123"
}
```

**Response:**
- Success: Account created with generated username
- Error: Flash message with validation errors

**Example:**
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "phone=+1234567890&email=john@example.com&password=secure_password123"
```

### GET /logout
Handle user logout.

**Response:**
- Success: Redirect to login page with success message

**Example:**
```bash
curl -X GET http://localhost:5000/logout
```

## Plant Management Endpoints

### GET /plants
Get all plants for the current user.

**Response:**
```json
{
    "plants": [
        {
            "id": 1,
            "name": "Blue Dream #1",
            "status": "Vegetative",
            "strain_name": "Blue Dream",
            "current_day": 45,
            "current_week": 6,
            "last_water_date": "2024-01-15T10:30:00Z"
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/plants \
  -H "Cookie: session=your_session_cookie"
```

### GET /plants/<int:plant_id>
Get detailed information about a specific plant.

**Parameters:**
- `plant_id` (int): The ID of the plant

**Response:**
```json
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
    "measurements": [
        {
            "id": 1,
            "name": "Height Measurement",
            "value": 45.5,
            "date": "2024-01-15T10:30:00Z"
        }
    ],
    "activities": [
        {
            "id": 1,
            "name": "Watering",
            "note": "Regular watering",
            "date": "2024-01-14T08:00:00Z"
        }
    ],
    "images": [
        {
            "id": 1,
            "image_path": "/uploads/plants/1/image1.jpg",
            "image_description": "Week 6 growth",
            "image_date": "2024-01-15T10:30:00Z"
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/plants/1 \
  -H "Cookie: session=your_session_cookie"
```

### POST /plants
Create a new plant.

**Request Body:**
```json
{
    "name": "New Plant",
    "description": "Plant description",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2,
    "is_clone": false,
    "autoflower": false
}
```

**Response:**
```json
{
    "success": true,
    "message": "Plant created successfully",
    "plant_id": 123
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/plants \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "name": "New Plant",
    "description": "Plant description",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2,
    "is_clone": false,
    "autoflower": false
  }'
```

### PUT /plants/<int:plant_id>
Update an existing plant.

**Parameters:**
- `plant_id` (int): The ID of the plant to update

**Request Body:**
```json
{
    "name": "Updated Plant Name",
    "description": "Updated description",
    "current_height": "50cm"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Plant updated successfully"
}
```

**Example:**
```bash
curl -X PUT http://localhost:5000/plants/1 \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "name": "Updated Plant Name",
    "description": "Updated description",
    "current_height": "50cm"
  }'
```

### DELETE /plants/<int:plant_id>
Delete a plant.

**Parameters:**
- `plant_id` (int): The ID of the plant to delete

**Response:**
```json
{
    "success": true,
    "message": "Plant deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/plants/1 \
  -H "Cookie: session=your_session_cookie"
```

## Sensor Management Endpoints

### GET /sensors
Get all sensors.

**Response:**
```json
{
    "sensors": [
        {
            "id": 1,
            "name": "Temperature Sensor",
            "type": "temperature",
            "unit": "°C",
            "zone_name": "Tent 1",
            "zone_id": 1,
            "source": "AC Infinity",
            "device": "Controller 69",
            "show": true
        }
    ]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/sensors \
  -H "Cookie: session=your_session_cookie"
```

### POST /sensors
Create a new sensor.

**Request Body:**
```json
{
    "name": "New Sensor",
    "type": "humidity",
    "unit": "%",
    "zone_id": 1,
    "source": "AC Infinity",
    "device": "Controller 69"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Sensor created successfully",
    "sensor_id": 123
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/sensors \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "name": "New Sensor",
    "type": "humidity",
    "unit": "%",
    "zone_id": 1
  }'
```

### DELETE /sensors/<int:sensor_id>
Delete a sensor.

**Parameters:**
- `sensor_id` (int): The ID of the sensor to delete

**Response:**
```json
{
    "success": true,
    "message": "Sensor deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/sensors/1 \
  -H "Cookie: session=your_session_cookie"
```

## Admin Endpoints

### GET /admin/users
Get all users (admin only).

**Response:**
```json
{
    "users": [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "phone": "+1234567890",
            "is_admin": true,
            "created_at": "2024-01-01T00:00:00Z",
            "force_password_change": false
        }
    ],
    "statistics": {
        "total_users": 10,
        "active_users": 8,
        "admin_users": 2
    }
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/admin/users \
  -H "Cookie: session=your_session_cookie"
```

### POST /admin/users/create
Create a new user (admin only).

**Request Body:**
```json
{
    "username": "new_user",
    "password": "password123",
    "email": "user@example.com",
    "phone": "+1234567890",
    "is_admin": false,
    "force_password_change": true
}
```

**Response:**
```json
{
    "success": true,
    "message": "User created successfully",
    "user_id": 123
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/admin/users/create \
  -H "Content-Type: application/json" \
  -H "Cookie: session=your_session_cookie" \
  -d '{
    "username": "new_user",
    "password": "password123",
    "email": "user@example.com",
    "is_admin": false
  }'
```

## Export Endpoints

### GET /admin/export/plants/csv
Export plants data as CSV (admin only).

**Response:**
- CSV file download

**Example:**
```bash
curl -X GET http://localhost:5000/admin/export/plants/csv \
  -H "Cookie: session=your_session_cookie" \
  --output plants_export.csv
```

### GET /admin/export/plants/json
Export plants data as JSON (admin only).

**Response:**
- JSON file download

**Example:**
```bash
curl -X GET http://localhost:5000/admin/export/plants/json \
  -H "Cookie: session=your_session_cookie" \
  --output plants_export.json
```

### GET /admin/export/activities/csv
Export activities data as CSV (admin only).

**Response:**
- CSV file download

**Example:**
```bash
curl -X GET http://localhost:5000/admin/export/activities/csv \
  -H "Cookie: session=your_session_cookie" \
  --output activities_export.csv
```

### GET /admin/export/complete-backup
Export complete database backup (admin only).

**Response:**
- Backup file download

**Example:**
```bash
curl -X GET http://localhost:5000/admin/export/complete-backup \
  -H "Cookie: session=your_session_cookie" \
  --output backup.zip
```

## Utility Endpoints

### GET /health
Health check endpoint.

**Response:**
```json
{
    "status": "ok"
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/health
```

### POST /api/newsletter/subscribe
Handle newsletter subscription.

**Request Body:**
```json
{
    "phone": "1234567890"
}
```

**Response:**
```json
{
    "success": true,
    "message": "Successfully subscribed to newsletter"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"phone": "1234567890"}'
```

## Error Responses

### Validation Error (400)
```json
{
    "success": false,
    "error": "Validation failed: name is required"
}
```

### Unauthorized (401)
```json
{
    "success": false,
    "error": "Authentication required"
}
```

### Forbidden (403)
```json
{
    "success": false,
    "error": "Admin privileges required"
}
```

### Not Found (404)
```json
{
    "success": false,
    "error": "Plant not found"
}
```

### Server Error (500)
```json
{
    "success": false,
    "error": "Internal server error"
}
```

## Authentication

Most endpoints require authentication via session cookies. Include the session cookie in your requests:

```bash
curl -H "Cookie: session=your_session_cookie" http://localhost:5000/protected-endpoint
```

## Rate Limiting

The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP address
- 1000 requests per hour per user

## CORS

CORS is enabled for the following origins:
- http://localhost:3000 (development)
- https://yourdomain.com (production)

## Pagination

For endpoints that return lists, pagination is supported:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 20, max: 100)

**Example:**
```bash
curl -X GET "http://localhost:5000/plants?page=2&per_page=10"
```
