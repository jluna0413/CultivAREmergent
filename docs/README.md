# CultivAR Documentation

Welcome to the comprehensive documentation for the CultivAR cannabis cultivation management application.

## Documentation Index

### Core Documentation
- **[API Overview](api_documentation.md)** - Main API reference and overview
- **[API Endpoints](api_endpoints.md)** - Detailed endpoint documentation with examples
- **[Models Documentation](models_documentation.md)** - Database models and data structures
- **[Handlers Documentation](handlers_documentation.md)** - Business logic handlers
- **[Utilities Documentation](utilities_documentation.md)** - Helper functions and utilities
- **[Examples](examples.md)** - Code examples and usage patterns

### Additional Documentation
- **[Tech Stack Summary](TechStackSummary.md)** - Technology overview
- **[Deployment Checklist](deployment_checklist.md)** - Deployment instructions
- **[Beta Testing Guide](beta_testing_guide.md)** - Testing procedures
- **[Version Log](VersionLog.md)** - Version history

## Quick Start

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Initialize database: `python -c "from app.models import migrate_db, init_db; migrate_db(); init_db()"`
5. Run the application: `python main.py`

### Basic Usage
```python
# Login
import requests
response = requests.post("http://localhost:5000/login", 
                        data={"username": "admin", "password": "password"})

# Get plants
plants = requests.get("http://localhost:5000/plants", 
                     cookies=response.cookies).json()

# Create plant
plant_data = {
    "name": "Blue Dream #1",
    "strain_id": 1,
    "zone_id": 1,
    "status_id": 2
}
result = requests.post("http://localhost:5000/plants", 
                      json=plant_data, cookies=response.cookies).json()
```

## API Overview

CultivAR provides RESTful APIs for:

- **Plant Management**: Create, read, update, delete plants
- **Sensor Management**: Monitor environmental conditions
- **User Management**: Authentication and user administration
- **Data Export**: Export data in various formats
- **Activity Tracking**: Log plant care activities
- **Measurement Recording**: Track plant growth metrics

## Authentication

The application uses session-based authentication with Flask-Login. Most endpoints require authentication via session cookies.

## Data Models

Core entities include:
- **Users**: Authentication and user management
- **Plants**: Individual cannabis plants
- **Strains**: Cannabis strain information
- **Sensors**: Environmental monitoring devices
- **Activities**: Plant care activities
- **Measurements**: Growth and environmental data

## Error Handling

All API endpoints return consistent error responses:
```json
{
    "success": false,
    "error": "Error message"
}
```

## Support

For questions or issues, please refer to the examples documentation or create an issue in the project repository.
