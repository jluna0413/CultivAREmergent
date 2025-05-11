# CultivAR

CultivAR is a self-hosted cannabis grow journal application. It allows you to track your plants, strains, and environmental data.

## Features

- Plant tracking (growth stages, activities, measurements)
- Strain management
- Sensor integration (AC Infinity, Ecowitt)
- Image uploads
- Environmental data visualization
- User authentication

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- SQLite or PostgreSQL

### Option 1: Local Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```

4. Access the application at http://localhost:4200

### Option 2: Docker Installation (SQLite)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run the Docker container:
   ```
   docker-compose -f docker-compose.sqlite.yml up -d
   ```

3. Access the application at http://localhost:4200

### Option 3: Docker Installation (PostgreSQL)

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cultivar.git
   cd cultivar
   ```

2. Build and run the Docker containers:
   ```
   docker-compose -f docker-compose.postgres.yml up -d
   ```

3. Access the application at http://localhost:4200

## Default Credentials

- Username: admin
- Password: isley

**Important:** Change the default password after first login.

## Configuration

CultivAR can be configured using environment variables:

- `SECRET_KEY`: Secret key for session management
- `ISLEY_DB_DRIVER`: Database driver (`sqlite` or `postgres`)
- `ISLEY_DB_HOST`: PostgreSQL host (default: `localhost`)
- `ISLEY_DB_PORT`: PostgreSQL port (default: `5432`)
- `ISLEY_DB_USER`: PostgreSQL username (default: `cultivar`)
- `ISLEY_DB_PASSWORD`: PostgreSQL password (default: `cultivar`)
- `ISLEY_DB_NAME`: PostgreSQL database name (default: `cultivardb`)
- `ISLEY_PORT`: Application port (default: `4200`)
- `DEBUG`: Debug mode (`true` or `false`)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project is a Python port of the [Isley](https://github.com/dwot/isley) project by dwot.
