# Flutter API Integration

This document outlines the integration between the CultivAR Flutter application and the backend API.

## Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/auth/login` | POST | Authenticates a user and returns JWT tokens. |
| `/api/v1/auth/register` | POST | Registers a new user. |
| `/api/v1/auth/refresh` | POST | Refreshes the access token. |
| `/api/v1/auth/me` | GET | Retrieves the current user's information. |
| `/ws` | WebSocket | Real-time communication for sensor data and notifications. |

## Authentication Flow

1.  The user enters their credentials on the login screen.
2.  The app sends a POST request to `/api/v1/auth/login`.
3.  The server validates the credentials and returns an access token and a refresh token.
4.  The app stores the tokens securely.
5.  The access token is sent in the `Authorization` header for all subsequent API requests.
6.  When the access token expires, the app uses the refresh token to obtain a new access token.

## WebSocket Flow

1.  After a successful login, the app establishes a WebSocket connection to `/ws` with the access token as a query parameter.
2.  The server authenticates the WebSocket connection.
3.  The server pushes real-time data (e.g., sensor readings) to the client.
4.  The client can send messages to the server to subscribe to specific topics.
