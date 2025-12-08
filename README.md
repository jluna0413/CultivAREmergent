# CultivAR

CultivAR is a cannabis grow platform. It allows you to track your plants, strains, and environmental data.

## Features

- Plant tracking (growth stages, activities, measurements)
- Strain management
- Sensor integration (AC Infinity, Ecowitt)
- Image uploads
- Environmental data visualization
- User authentication
- Cross-platform support (Web, Mobile, Desktop) via Flutter
- Progressive Web App (PWA) with offline capabilities
- Real-time sensor data via WebSockets
- Asynchronous database operations for improved performance
- Automatic OpenAPI documentation generation

## Migration Status

The CultivAR project has migrated to FastAPI as the primary framework, with Flask available for legacy support. Here's the current status:

- **FastAPI app**: Primary framework running on port **4200**
- **Flask app**: Legacy support available on port 5000 via dual-stack setup
- **Flutter Frontend**: Cross-platform app running on port **4242**
- **Database**: Both apps share the same database for consistency
- **Strategy**: FastAPI-first with optional Flask fallback for migration scenarios

**⚠️ IMPORTANT PORT ASSIGNMENTS:**

- Backend API: **Port 4200** (FastAPI)
- Flutter Frontend: **Port 4242**
- Reserved Ports: 3000, 8000, 8080 (different project)

![FastAPI Tests](https://github.com/your-username/your-repo-name/workflows/FastAPI%20Tests/badge.svg)

For detailed migration information, see the [Migration Guide](MIGRATION.md).

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- SQLite or PostgreSQL

### FastAPI vs Flask Startup Commands

Use the appropriate command based on your deployment needs during migration.

| Mode | Command | Port | Documentation |
|------|---------|------|---------------|
| Flask | `python run_flask.py` | 5000 | N/A |
| FastAPI | `python run_fastapi.py` | **4200** | <http://localhost:4200/docs> |
| Flutter | `cd flutter_app && flutter run --web-port 4242` | **4242** | N/A |
| Dual-stack | `docker compose -f docker-compose.dual.yml up` | 5000 & 4200 | /docs (FastAPI) |

### Option 1: Local Installation (Flask)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the Flask application:

   ```
   python run_flask.py
   ```

   This uses the dedicated Flask runner for consistency with the FastAPI version and Makefile targets.

4. Access the application at <http://localhost:5000>

### Option 2: Local Installation (FastAPI)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the FastAPI application:

   ```
   python run_fastapi.py
   ```

4. Access the application at <http://localhost:4200>

### Option 3: Docker Installation (FastAPI with SQLite)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run the Docker container:

   ```
   docker compose -f docker-compose.fastapi.yml up -d
   ```

   Note: To use SQLite instead of the default PostgreSQL, set `CULTIVAR_DB_DRIVER=sqlite` in your `.env` file and ensure the `./data` volume is mounted (see comments in `docker-compose.fastapi.yml`).

3. Access the application at <http://localhost:4200>
    - API documentation available at <http://localhost:4200/docs>

### Option 4: Docker Installation (FastAPI with PostgreSQL)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run the Docker containers:

   ```
   docker compose -f docker-compose.fastapi.yml up -d
   ```

3. Access the application at <http://localhost:4200>
    - API documentation available at <http://localhost:4200/docs>

### Option 5: Docker Installation (FastAPI)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run the Docker container:

   ```
   docker compose -f docker-compose.fastapi.yml up -d
   ```

3. Access the application at <http://localhost:4200>

### Option 6: Docker Installation (Dual-stack)

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run both Flask and FastAPI applications in Docker:

   ```
   docker compose -f docker-compose.dual.yml up -d
   ```

3. Access Flask at <http://localhost:5000> and FastAPI at <http://localhost:4200>

## Default Credentials

- Username: admin
- Password: isley

**Important:** Change the default password after first login.

## Configuration

CultivAR can be configured using environment variables. A template for these variables is provided in `.env.example`. Copy this file to `.env` and customize it for your environment:

```bash
cp .env.example .env
```

- `SECRET_KEY`: Secret key for session management
- `CULTIVAR_DB_DRIVER`: Database driver (`sqlite` or `postgres`)
- `CULTIVAR_DB_HOST`: PostgreSQL host (default: `localhost`)
- `CULTIVAR_DB_PORT`: PostgreSQL port (default: `5432`)
- `CULTIVAR_DB_USER`: PostgreSQL username (default: `cultivar`)
- `CULTIVAR_DB_PASSWORD`: PostgreSQL password (default: `cultivar`)
- `CULTIVAR_DB_NAME`: PostgreSQL database name (default: `cultivardb`)
- `CULTIVAR_PORT`: Flask application port (default: `5000`)
- `FASTAPI_PORT`: FastAPI application port (default: `4200`)
- `APP_MODE`: Application mode (`flask` or `fastapi`, default: `fastapi`)
- `DEBUG`: Debug mode (`true` or `false`)
- FastAPI-specific secrets (e.g., `JWT_SECRET_KEY`, `SESSION_SECRET_KEY`, `CSRF_SECRET_KEY`, `FLASH_SECRET_KEY`, `FRONTEND_ORIGINS`) are required only when `APP_MODE=fastapi` or in dual-stack mode.

For detailed production deployment instructions, refer to [DEPLOYMENT.md](DEPLOYMENT.md). For dual-stack deployment, traffic splitting via Nginx, and production considerations, see `DEPLOYMENT.md` and `nginx.conf.example`.
To verify the migration status, run `python scripts/verify_migration.py` to check migration status and generate `MIGRATION_STATUS.md`.

## Flutter App

The new CultivAR frontend is being built with Flutter to provide a modern, cross-platform experience.

### Prerequisites

- Flutter SDK (version 3.19.0 or higher)
- An IDE like Android Studio or Visual Studio Code with the Flutter plugin.
- For mobile development: Android SDK / Xcode.

### Setup

1. Navigate to the Flutter project directory:

   ```
   cd flutter_app
   ```

2. Get the dependencies:

   ```
   flutter pub get
   ```

3. Set up environment variables. Copy the example file and edit it:

   ```
   cp .env.example .env
   ```

   Then, set the `API_BASE_URL` in the `.env` file:

   ```
   API_BASE_URL=http://localhost:4200
   WS_BASE_URL=ws://localhost:4200/ws
   ```

### Running the App

You can run the app on any supported platform.

```bash
# Run on Chrome (web) - Backend must be running on port 4200
flutter run --web-port 4242 -d chrome

# Run on a connected Android device
flutter run -d android

# Run on the iOS simulator (macOS only)
flutter run -d ios

# Run on the macOS desktop app
flutter run -d macos
```

### Building the App

```bash
# Build the web app (output in build/web)
flutter build web

# Build an Android APK
flutter build apk

# Build for iOS
flutter build ios
```

### Testing

```bash
# Run all unit and widget tests
flutter test

# Run integration tests
flutter test integration_test
```

For more details on the migration, see the [Flutter Migration Plan](FLUTTER_MIGRATION.md).

## Development Notes

The `legacy/` directory contains archived Flask-era code and is intentionally excluded from CI quality checks (linting and testing).

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project is a Python port of the [Isley](https://github.com/dwot/isley) project by dwot.
