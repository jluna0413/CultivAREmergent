# Installation Guide

This guide will walk you through the process of setting up CultivAR on your own server. You can choose between a local installation or a Docker-based installation.

## Prerequisites

Before you begin, make sure you have the following software installed on your system:

*   **Python:** Version 3.9 or higher.
*   **pip:** The Python package manager.
*   **Git:** The version control system.
*   **Docker and Docker Compose (for Docker installation):** The containerization platform.

## Local Installation

This method is recommended for development and testing purposes.

### 1. Clone the Repository

First, clone the CultivAR repository to your local machine:

```bash
git clone https://github.com/jluna0413/CultivAREmergent.git
cd CultivAREmergent
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Configure the Application

CultivAR is configured using environment variables. You can create a `.env` file in the root of the project to store your configuration.

Here is an example `.env` file:

```
SECRET_KEY=your_super_secret_key
CULTIVAR_DB_DRIVER=sqlite
CULTIVAR_PORT=5000
DEBUG=true
```

For a full list of configuration options, see the [Configuration](Developer-Guide.md#configuration) section of the Developer Guide.

### 4. Run the Application

Start the application using the following command:

```bash
python cultivar_app.py
```

You should see output indicating that the application is running on `http://localhost:5000`.

## Docker Installation

This is the recommended method for production deployments using FastAPI.

### Docker with FastAPI

This method runs the FastAPI version of CultivAR, which is the primary framework.

1.  **Build and run the Docker container:**
    ```bash
    docker compose -f docker-compose.fastapi.yml up -d --build
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://localhost:8000`.

    API documentation is available at `http://localhost:8000/docs`.

**Note:** By default, this setup uses PostgreSQL. If you prefer SQLite, set `CULTIVAR_DB_DRIVER=sqlite` in your `.env` file and modify the compose file to comment out the `db` service and add a volume mount for `./data:/app/data`.

**Troubleshooting:** If you need to run Flask for any reason (e.g., legacy testing), use `docker-compose.dual.yml` to run both frameworks simultaneously. Flask will be available on port 5000, and FastAPI on port 8000.

## Default Credentials

After a fresh installation, you will need to create an admin user. The application does not create one automatically for security reasons.

You can create an admin user by running the following command from the root of the project:

```bash
# This is a placeholder for a future admin creation script.
# For now, you will need to create a user through the signup page
# and then manually set the `is_admin` flag in the database.
```