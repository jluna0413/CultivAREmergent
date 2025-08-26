# API Reference

This document provides a reference for the CultivAR API.

## Authentication

Most API endpoints require authentication. To authenticate, you will need to log in to the application and obtain a session cookie. The session cookie will be automatically included in subsequent requests.

## Endpoints

### Health Check

*   **Endpoint:** `/health`
*   **Method:** `GET`
*   **Description:** Checks the health of the application.
*   **Authentication:** None
*   **Response:**
    ```json
    {
      "status": "ok"
    }
    ```

### Admin API

All admin API endpoints are prefixed with `/admin/api`.

#### Users

*   **Endpoint:** `/admin/api/users`
*   **Method:** `GET`
*   **Description:** Gets a list of all users.
*   **Authentication:** Admin
*   **Response:**
    ```json
    {
      "success": true,
      "users": [
        {
          "id": 1,
          "username": "admin",
          "email": "admin@example.com",
          "is_admin": true,
          ...
        }
      ]
    }
    ```

*   **Endpoint:** `/admin/api/users`
*   **Method:** `POST`
*   **Description:** Creates a new user.
*   **Authentication:** Admin
*   **Request Body:**
    ```json
    {
      "username": "newuser",
      "password": "newpassword",
      "email": "newuser@example.com"
    }
    ```
*   **Response:**
    ```json
    {
      "success": true,
      "user_id": 2,
      "message": "User newuser created successfully"
    }
    ```

#### System

*   **Endpoint:** `/admin/api/system/logs`
*   **Method:** `GET`
*   **Description:** Gets the system logs.
*   **Authentication:** Admin
*   **Response:**
    ```json
    {
      "success": true,
      "logs": [
        {
          "timestamp": "...",
          "level": "INFO",
          "message": "..."
        }
      ]
    }
    ```

*   **Endpoint:** `/admin/api/system/info`
*   **Method:** `GET`
*   **Description:** Gets system information.
*   **Authentication:** Admin
*   **Response:**
    ```json
    {
      "success": true,
      "info": {
        "python_version": "...",
        "os_name": "...",
        ...
      }
    }
    ```
