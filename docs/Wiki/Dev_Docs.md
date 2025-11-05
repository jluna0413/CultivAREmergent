# CultivAR Developer Documentation

## Architecture

CultivAR is built using the following technologies:

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with support for SQLite and PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Flask-Login
- **Template Engine**: Jinja2

### Directory Structure

```
CultivAR/
├── app/
│   ├── config/         # Configuration settings
│   ├── handlers/       # Business logic handlers
│   ├── logger/         # Logging configuration
│   ├── models/         # Database models
│   ├── routes/         # Route definitions
│   ├── utils/          # Utility functions
│   ├── watcher/        # Background tasks
│   └── web/            # Frontend files
│       ├── static/     # Static assets (CSS, JS, images)
│       └── templates/  # HTML templates
├── data/               # SQLite database (if used)
├── docs/               # Documentation
├── logs/               # Application logs
├── uploads/            # Uploaded files
├── main.py             # Application entry point
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.*.yml # Docker Compose configurations
└── VERSION             # Application version
```

## Core Components

### Models

The application uses SQLAlchemy models to represent database entities:

- **User**: Authentication user
- **Plant**: Cannabis plant
- **Cultivar**: Cannabis cultivar
- **Breeder**: Seed breeder/bank
- **Zone**: Growing zone
- **Sensor**: Environmental sensor
- **SensorData**: Sensor readings
- **PlantActivity**: Plant activities (watering, feeding, etc.)
- **Measurement**: Plant measurements (height, pH, etc.)
- **PlantImage**: Plant images
- **Settings**: Application settings

### Handlers

Handlers contain the business logic of the application:

- **plant_handlers.py**: Plant management
- **cultivar_handlers.py**: Cultivar management
- **sensor_handlers.py**: Sensor management
- **settings_handlers.py**: Settings management

### Routes

Routes define the application endpoints:

- **Basic Routes**: Health check, favicon
- **Authentication Routes**: Login, logout, password change
- **Protected Routes**: Dashboard, plants, cultivars, sensors, settings
- **API Routes**: JSON endpoints for AJAX requests

### Watcher

The watcher module runs background tasks:

- **Sensor Data Collection**: Periodically polls sensors for data
- **Stream Image Capture**: Captures images from video streams
- **Data Pruning**: Removes old sensor data to prevent database bloat

## Development Setup

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application in debug mode:
   ```
   python main.py
   ```

### Database Migrations

The application handles database migrations automatically:

1. When the application starts, it checks if the database exists.
2. If not, it creates the necessary tables.
3. If migrating from SQLite to PostgreSQL, it can import data from the SQLite database.

## Adding Features

### Adding a New Model

1. Define the model in `app/models/base_models.py` or create a new file in the `models` directory.
2. Import the model in `app/models/__init__.py`.
3. Add any necessary migration code to the `migrate_db` function.

### Adding a New Handler

1. Create a new file in the `handlers` directory (e.g., `new_feature_handlers.py`).
2. Implement the necessary functions.
3. Import the functions in `app/handlers/__init__.py`.

### Adding a New Route

1. Add the route function to `app/routes/routes.py`.
2. Register the route in the appropriate section (basic, auth, protected, or API).

### Adding a New Template

1. Create a new template file in `app/web/templates/views/`.
2. Extend the base template: `{% extends 'common/base.html' %}`.
3. Implement the necessary blocks (title, header, content, scripts).

## Testing

The application can be tested using pytest:

1. Install pytest:
   ```
   pip install pytest
   ```

2. Run the tests:
   ```
   pytest
   ```

## Deployment

### Docker Deployment

1. Build the Docker image:
   ```
   docker build -t cultivar .
   ```

2. Run with SQLite:
   ```
   docker-compose -f docker-compose.sqlite.yml up -d
   ```

3. Run with PostgreSQL:
   ```
   docker-compose -f docker-compose.postgres.yml up -d
   ```

### Manual Deployment

1. Set up a production web server (e.g., Nginx, Apache).
2. Configure the web server to proxy requests to the Flask application.
3. Set up a process manager (e.g., Supervisor, systemd) to run the application.
4. Configure environment variables for production settings.

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Write tests for your changes.
5. Submit a pull request.
