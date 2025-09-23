# Complete API Reference

Comprehensive REST API and MCP integration reference for CultivAR.

## Overview

CultivAR provides two main API interfaces:

1. **REST API** - Traditional HTTP endpoints for web and mobile applications
2. **MCP (Model Context Protocol)** - AI/LLM integration for intelligent assistance

## Authentication

### API Key Authentication

All API requests require authentication via API key:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:5000/api/v1/plants
```

### Session Authentication

Web interface uses session-based authentication:

```python
# Login endpoint
POST /auth/login
{
    "username": "admin",
    "password": "isley"
}
```

## REST API Reference

### Base URL
```
http://localhost:5000/api/v1
```

### Plants API

#### GET /plants
Retrieve all plants

**Parameters:**
- `active_only` (boolean): Filter active plants only
- `strain_id` (integer): Filter by strain ID
- `page` (integer): Page number for pagination
- `per_page` (integer): Items per page (max 100)

**Response:**
```json
{
  "plants": [
    {
      "id": 1,
      "name": "Blue Dream #1",
      "strain_id": 1,
      "strain_name": "Blue Dream",
      "status": "flowering",
      "days_in_stage": 42,
      "planted_date": "2023-12-01T00:00:00Z",
      "last_activity": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "pages": 1
  }
}
```

#### GET /plants/{id}
Get plant details

**Response:**
```json
{
  "id": 1,
  "name": "Blue Dream #1",
  "description": "Premium Blue Dream genetics",
  "strain": {
    "id": 1,
    "name": "Blue Dream",
    "genetics": "hybrid",
    "indica_percentage": 40,
    "sativa_percentage": 60
  },
  "status": "flowering",
  "planted_date": "2023-12-01T00:00:00Z",
  "measurements": [
    {
      "metric": "height",
      "value": 85.5,
      "unit": "cm",
      "date": "2024-01-15T00:00:00Z"
    }
  ],
  "activities": [
    {
      "id": 123,
      "type": "watering",
      "amount": 500,
      "notes": "Regular watering",
      "date": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST /plants
Create new plant

**Request:**
```json
{
  "name": "Purple Haze #1",
  "strain_id": 2,
  "description": "Classic sativa strain",
  "planted_date": "2024-01-01T00:00:00Z"
}
```

#### PUT /plants/{id}
Update plant

#### DELETE /plants/{id}
Delete plant

### Plant Activities API

#### POST /plants/{id}/activities
Add plant activity

**Request:**
```json
{
  "activity_type": "watering",
  "amount": 500,
  "notes": "Morning watering session",
  "date": "2024-01-15T08:00:00Z"
}
```

#### GET /plants/{id}/activities
Get plant activities

### Plant Measurements API

#### POST /plants/{id}/measurements
Add measurement

**Request:**
```json
{
  "metric": "height",
  "value": 87.2,
  "unit": "cm",
  "date": "2024-01-15T00:00:00Z"
}
```

#### GET /plants/{id}/measurements
Get plant measurements

### Strains API

#### GET /strains
List all strains

**Parameters:**
- `search` (string): Search strain names
- `genetics` (string): Filter by genetics (indica, sativa, hybrid)
- `breeder` (string): Filter by breeder

**Response:**
```json
{
  "strains": [
    {
      "id": 1,
      "name": "Blue Dream",
      "genetics": "hybrid",
      "indica_percentage": 40,
      "sativa_percentage": 60,
      "breeder": "DJ Short",
      "flowering_time": "9-10 weeks",
      "description": "Popular hybrid with balanced effects",
      "thc_content": "17-24%",
      "cbd_content": "0.1-0.2%"
    }
  ]
}
```

#### POST /strains
Create new strain

#### GET /strains/{id}
Get strain details

### Environmental Data API

#### GET /environmental
Get environmental sensor data

**Parameters:**
- `start_date` (ISO date): Start date for data range
- `end_date` (ISO date): End date for data range
- `sensor_type` (string): Filter by sensor type
- `metric` (string): Specific metric (temperature, humidity, etc.)

**Response:**
```json
{
  "data": [
    {
      "timestamp": "2024-01-15T12:00:00Z",
      "temperature": 24.5,
      "humidity": 55.2,
      "light_level": 850,
      "co2_level": 1200,
      "vpd": 1.1,
      "sensor_id": "ac_infinity_1"
    }
  ],
  "summary": {
    "avg_temperature": 24.2,
    "avg_humidity": 56.8,
    "readings_count": 144
  }
}
```

#### POST /environmental
Add environmental data point

### Images API

#### POST /plants/{id}/images
Upload plant image

**Request:** Multipart form data
- `image` (file): Image file
- `description` (string): Image description
- `date` (string): Date taken

#### GET /plants/{id}/images
Get plant images

#### DELETE /images/{id}
Delete image

### Analytics API

#### GET /analytics/growth-trends
Get growth trend analysis

**Parameters:**
- `plant_id` (integer): Specific plant
- `metric` (string): Metric to analyze
- `period` (string): Analysis period (7d, 30d, 90d)

#### GET /analytics/harvest-prediction
Get harvest date predictions

#### GET /analytics/environmental-summary
Get environmental condition summary

## MCP (Model Context Protocol) Reference

### Available Tools

#### get_plants
**Description:** Retrieve all plants in the grow journal

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "active_only": {"type": "boolean"},
    "strain_id": {"type": "integer"}
  }
}
```

**Example Usage:**
```
AI: "Show me all my active plants"
```

#### get_plant_details
**Description:** Get detailed information about a specific plant

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "plant_id": {"type": "integer", "required": true}
  },
  "required": ["plant_id"]
}
```

#### get_strains
**Description:** Retrieve strain database information

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "search": {"type": "string"},
    "genetics": {
      "type": "string",
      "enum": ["indica", "sativa", "hybrid"]
    }
  }
}
```

#### get_environmental_data
**Description:** Retrieve sensor data and environmental conditions

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "start_date": {"type": "string"},
    "end_date": {"type": "string"},
    "sensor_type": {"type": "string"}
  }
}
```

#### add_plant_activity
**Description:** Record a new activity for a plant

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "plant_id": {"type": "integer", "required": true},
    "activity_type": {"type": "string", "required": true},
    "notes": {"type": "string"},
    "amount": {"type": "number"}
  },
  "required": ["plant_id", "activity_type"]
}
```

#### get_grow_room_status
**Description:** Get current environmental conditions

**Input Schema:**
```json
{
  "type": "object",
  "properties": {}
}
```

### MCP Resources

#### cultivar://plants
Complete list of all plants in JSON format

#### cultivar://strains
Complete strain database in JSON format

#### cultivar://environmental
Current and historical environmental data

## Error Handling

### HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Rate Limited
- `500` - Server Error

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "plant_id",
      "issue": "Required field missing"
    }
  }
}
```

### MCP Error Handling

MCP errors are returned as TextContent with error details:

```json
{
  "type": "text",
  "text": "Error: Plant with ID 999 not found"
}
```

## Rate Limiting

### REST API Limits
- 100 requests per minute per IP
- 1000 requests per hour per user
- Burst limit: 10 requests per second

### MCP Limits
- 60 tool calls per minute
- 10 concurrent requests

## Data Validation

### Input Validation Rules

**Plant Names:**
- 1-100 characters
- Alphanumeric, spaces, hyphens allowed

**Measurements:**
- Numeric values only
- Range validation per metric type
- Required units for each metric

**Dates:**
- ISO 8601 format required
- Cannot be in the future for historical data

### Response Validation

All API responses include:
- Timestamp of request processing
- Data validation checksums
- Version information

## Pagination

### REST API Pagination

```json
{
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 100,
    "pages": 5,
    "has_next": true,
    "has_prev": false,
    "next_url": "/api/v1/plants?page=2",
    "prev_url": null
  }
}
```

### MCP Pagination

MCP tools automatically handle pagination internally and return summarized results.

## Filtering and Searching

### Query Parameters

**Common Filters:**
- `search` - Text search across relevant fields
- `date_from` / `date_to` - Date range filtering
- `status` - Status-based filtering
- `sort` - Sort order (asc/desc)
- `sort_by` - Sort field

**Example:**
```
GET /api/v1/plants?search=blue&status=active&sort_by=name&sort=asc
```

## Webhooks (Future)

### Event Types
- `plant.created`
- `plant.updated`
- `activity.added`
- `measurement.recorded`
- `environmental.alert`

## SDK Examples

### Python SDK

```python
from cultivar_sdk import CultivARClient

client = CultivARClient(api_key="your-key", base_url="http://localhost:5000")

# Get plants
plants = client.plants.list(active_only=True)

# Add activity
client.plants.add_activity(
    plant_id=1,
    activity_type="watering",
    amount=500,
    notes="Morning watering"
)
```

### JavaScript SDK

```javascript
const CultivAR = require('cultivar-js-sdk');

const client = new CultivAR({
  apiKey: 'your-key',
  baseURL: 'http://localhost:5000'
});

// Get plants
const plants = await client.plants.list({ activeOnly: true });

// Add measurement
await client.plants.addMeasurement(1, {
  metric: 'height',
  value: 85.5,
  unit: 'cm'
});
```

## Testing

### API Testing

```bash
# Test authentication
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"isley"}'

# Test plant listing
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/v1/plants
```

### MCP Testing

```python
import asyncio
from mcp_server import handle_call_tool

async def test_mcp():
    result = await handle_call_tool(
        "get_plants", 
        {"active_only": True}
    )
    print(result[0].text)

asyncio.run(test_mcp())
```

## 🔗 See Also

- [MCP Integration](mcp-integration.md) - Complete MCP setup guide
- [Authentication](security.md) - Security and authentication details
- [Database Schema](database-schema.md) - Database structure reference
- [Quick Start](quick-start.md) - Getting started guide

---

*API documentation is automatically generated and always up-to-date. For the latest changes, see the [changelog](changelog.md).*