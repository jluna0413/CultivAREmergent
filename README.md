# CultivAR

CultivAR is a self-hosted cannabis grow journal application. It allows you to track your plants, cultivars, and environmental data.

## Features

- Plant tracking (growth stages, activities, measurements)
- Cultivar management
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

4. Access the application at http://localhost:5000

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

3. Access the application at http://localhost:5000

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

3. Access the application at http://localhost:5000

## Default Credentials

- Username: admin
- Password: isley

**Important:** Change the default password after first login.

## Configuration

CultivAR can be configured using environment variables:

### Core Application Settings
- `SECRET_KEY`: Secret key for JWT authentication (CHANGE IN PRODUCTION)
- `CULTIVAR_DB_DRIVER`: Database driver (`sqlite` or `postgres`)
- `CULTIVAR_DB_HOST`: PostgreSQL host (default: `localhost`)
- `CULTIVAR_DB_PORT`: PostgreSQL port (default: `5432`)
- `CULTIVAR_DB_USER`: PostgreSQL username (default: `cultivar`)
- `CULTIVAR_DB_PASSWORD`: PostgreSQL password (default: `cultivar`)
- `CULTIVAR_DB_NAME`: PostgreSQL database name (default: `cultivardb`)
- `CULTIVAR_PORT`: Application port (default: `5000`)
- `DEBUG`: Debug mode (`true` or `false`)

### Security Configuration

**CORS Origins:**
- `FRONTEND_ORIGINS`: Comma-separated list of allowed frontend origins for CORS
  - Example: `http://localhost:3000,https://myapp.com`
  - Filters empty entries automatically for security
  - Default: `http://localhost:3000,http://localhost:8000`

**Trusted Hosts:**
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts for TrustedHostMiddleware
  - Example: `localhost,127.0.0.1,myapp.com,*.myapp.com`
  - Filters empty hosts and prevents header injection attacks
  - Default: `localhost,127.0.0.1,*.localhost`

**JWT Security:**
- Implements JWT with JTI (JSON Token Identifier) for token tracking
- Supports refresh token rotation to prevent reuse attacks
- Includes token revocation store for immediate invalidation
- Access tokens expire in 30 minutes, refresh tokens in 7 days
- Admin role validation through JWT claims

**Rate Limiting:**
- Built-in rate limiting by IP address
- Configurable limits and time windows
- Prevents abuse and DDoS attacks

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

This project is a Python port of the [Isley](https://github.com/dwot/isley) project by dwot.
