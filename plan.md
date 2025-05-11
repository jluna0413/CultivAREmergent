# CultivAR - Cannabis Grow Journal Application

## Overview
CultivAR is a Python-based clone of the Isley application, a self-hosted cannabis grow journal designed to help homegrowers track and monitor their plants. It provides a clean interface and integrations with popular grow equipment, making it simple to manage your grow effectively.

## Key Features to Implement
- **Grow Logs**: Track plant growth, watering, and feeding schedules
- **Environmental Monitoring**: View real-time data from grow equipment (AC Infinity, Ecowitt)
- **Image Uploads**: Attach photos to grow logs for visual tracking
- **Seed Inventory**: Manage seed collection and strain library
- **Harvest Tracking**: Record harvest details and yields
- **Graphs and Charts**: Visualize environmental data and plant progress
- **Customizable Settings**: Add custom activities and measurements
- **Mobile-Friendly**: Works on desktop and mobile devices

## Technology Stack
- **Backend**: Python with Flask
- **Database**: SQLite (with option for PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **Charts**: Chart.js
- **File Uploads**: Flask-Uploads

## Project Structure
```
CultivAR/
├── app/
│   ├── config/         # Configuration settings
│   ├── handlers/       # Request handlers
│   ├── logger/         # Logging utilities
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── utils/          # Utility functions
│   ├── watcher/        # Sensor data collection
│   └── web/            # Frontend files
│       ├── static/     # CSS, JS, images
│       └── templates/  # HTML templates
├── data/               # SQLite database
├── logs/               # Application logs
├── uploads/            # User uploads
│   ├── plants/         # Plant images
│   ├── streams/        # Stream data
│   └── logos/          # Logo images
├── tests/              # Test files
├── main.py             # Application entry point
├── Dockerfile          # Docker configuration
├── docker-compose.sqlite.yml
├── docker-compose.postgres.yml
└── README.md
```

## Database Models
1. **User**: Authentication and user management
2. **Plant**: Plant tracking and lifecycle
3. **Strain**: Cannabis strain information
4. **Activity**: Watering, feeding, training, etc.
5. **Sensor**: Environmental sensor data
6. **Harvest**: Harvest records and yields
7. **Setting**: Application settings
8. **Image**: Image uploads and metadata

## Implementation Plan
1. **Setup Project Structure**: Create directories and initial files
2. **Database Models**: Define SQLAlchemy models
3. **Authentication**: Implement user login/registration
4. **Core Features**: Implement plant tracking, activities, etc.
5. **Sensor Integration**: Add support for environmental sensors
6. **Frontend**: Create responsive UI with templates
7. **Image Uploads**: Implement file upload functionality
8. **Charts and Graphs**: Add data visualization
9. **Settings and Configuration**: Implement customizable settings
10. **Testing**: Write tests for core functionality
11. **Documentation**: Create user and developer documentation
12. **Docker Support**: Add Docker configuration files

## API Endpoints
- `/api/plants` - Plant management
- `/api/activities` - Activity tracking
- `/api/sensors` - Sensor data
- `/api/strains` - Strain information
- `/api/harvests` - Harvest records
- `/api/settings` - Application settings
- `/api/images` - Image uploads

## UI Pages
- Dashboard
- Plant Detail
- Sensor Monitoring
- Strain Library
- Harvest Records
- Settings
- User Profile

## Authentication
- Login/Logout
- Password Change
- User Management (Admin only)

## Deployment Options
- Docker with SQLite
- Docker with PostgreSQL
- Direct Python execution
