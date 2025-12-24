# CultivAR Project Documentation

## 1. Project Overview

CultivAR is a cloud-hosted application designed for tracking the cultivation of cannabis. It enables users to monitor plants, manage strains, and log environmental data from various sensors. While it can be run locally for development and testing, the production environment is a cloud-based service that users interact with via a Progressive Web App (PWA) or a native mobile/desktop application. The system is architected with a distinct frontend and backend.

The backend has recently migrated from Flask to FastAPI, which now serves as the primary framework. The system supports a dual-stack mode, allowing both frameworks to run simultaneously for migration and legacy purposes.

The frontend is a modern, cross-platform application built with Flutter, ensuring a consistent user experience on web, mobile, and desktop platforms.

## 2. Technology Stack

- **Backend:**
    - **Framework:** FastAPI (primary), Flask (legacy support)
    - **Language:** Python
    - **Database:** PostgreSQL or SQLite
    - **ORM:** SQLAlchemy
    - **Real-time Communication:** WebSockets
    - **Containerization:** Docker
- **Frontend:**
    - **Framework:** Flutter
    - **Language:** Dart

## 3. Backend Architecture

The CultivAR backend is designed to be modular and has undergone a significant migration from Flask to FastAPI.

### 3.1. FastAPI (Primary)

The primary backend is built using the FastAPI framework, located in the `app/fastapi_main` directory.

- **Entry Point:** The application is launched via `run_fastapi.py`, which uses `uvicorn` to serve the main app instance created in `app/fastapi_main/main.py`.

- **Middleware:** The FastAPI application leverages a robust middleware stack for handling requests and implementing cross-cutting concerns:
    - `CORSMiddleware`: Manages Cross-Origin Resource Sharing.
    - `SessionMiddleware`: Handles user sessions.
    - `CSRFMiddleware`: Protects against Cross-Site Request Forgery.
    - `FlashMiddleware`: Enables flash messages.
    - `RateLimitMiddleware`: Provides protection against brute-force and DoS attacks.
    - `SecurityHeadersMiddleware`: Sets important security-related HTTP headers.
    - Custom Middleware for logging, performance, and security monitoring.

- **Routing:** The application's endpoints are organized into modular routers, which are analogous to Flask's Blueprints. This includes routers for both web UI (HTML) and a versioned JSON API (`/api/v1`). Key routers include `auth`, `dashboard`, `plants`, `strains`, `sensors`, `admin`, and `websocket`.

- **Exception Handling:** Global exception handlers are in place to provide consistent error responses, returning JSON for API endpoints and user-friendly HTML pages for web routes.

### 3.2. Flask (Legacy)

The legacy backend is built using the Flask framework and is primarily located in the `app` directory, with `cultivar_app.py` serving as the application factory.

- **Application Factory:** The `create_app` function in `cultivar_app.py` configures and instantiates the Flask application.

- **Blueprints:** The application is organized using Flask Blueprints to maintain modularity. It includes blueprints for `auth`, `dashboard`, `strains`, `admin`, and more.

- **Security:** Security is handled by a combination of Flask extensions:
    - `Flask-Talisman`: Manages security headers like CSP.
    - `Flask-Limiter`: Implements rate limiting.
    - `Flask-WTF`: Provides CSRF protection.
    - `Flask-Login`: Manages user authentication and sessions.

- **Database:** It uses `Flask-SQLAlchemy` to integrate with the SQLAlchemy ORM for database operations.

## 4. Frontend Architecture



The CultivAR frontend is a modern, cross-platform application built with Flutter. It is located in the `flutter_app` directory.



- **State Management:** The application uses the **Riverpod** framework for state management. The root of the application is wrapped in a `ProviderScope`, making providers available throughout the widget tree. This allows for a reactive and scalable architecture for managing application state.



- **Routing:** Navigation is handled by the **GoRouter** package. The routes are defined declaratively in `lib/core/router/app_router.dart` and are organized by feature. The router includes authentication guards to protect routes that require a logged-in user, redirecting unauthenticated users to the login screen.



- **Key Dependencies:**

    - **UI & Forms:** `flutter_form_builder` for creating forms and `fl_chart` for data visualization.

    - **HTTP & API:** `dio` and `http` for communicating with the backend REST API.

    - **Real-time:** `web_socket_channel` for WebSocket communication.

    - **Local Storage:** `drift` (a reactive SQLite wrapper) for local database, `shared_preferences` for key-value storage, and `flutter_secure_storage` for sensitive data.

    - **Data Modeling:** `freezed` for immutable data classes and `json_serializable` for JSON conversion.

    - **Authentication:** `flutter_appauth` for OAuth flows and `jwt_decoder` for handling JSON Web Tokens.



## 5. Key Features



- **Plant & Strain Management:** Track growth stages, activities, measurements, and strain-specific information.

- **Sensor Integration:** Connect with AC Infinity and Ecowitt devices to monitor environmental conditions.

- **Data Visualization:** View environmental data through charts and graphs.

- **Image Uploads:** Attach images to journal entries.

- **User Authentication:** Secure user accounts.

- **Cross-Platform:** Single codebase for web (including PWA), mobile (Android/iOS), and desktop (macOS).



## 6. Installation and Setup



The application can be set up in several ways:



- **Local Python Environment:** Run the FastAPI or Flask server directly.

- **Docker:** Use Docker Compose to run the backend with either SQLite or PostgreSQL. A dual-stack configuration is also available to run both Flask and FastAPI servers.

- **Flutter:** The frontend application is run using standard Flutter commands (`flutter run`).



## 7. Configuration



Application settings are managed via a `.env` file, derived from the `.env.example` template. Key configuration options include:



- `SECRET_KEY`

- Database connection details (`CULTIVAR_DB_*`)

- Application ports (`CULTIVAR_PORT`, `FASTAPI_PORT`)

- Application mode (`APP_MODE`)

- Debug mode (`DEBUG`)

- Frontend API and WebSocket URLs



## 8. Default Credentials



For initial setup, the application uses the following default credentials:



- **Username:** `admin`

- **Password:** `isley`



## 9. Migration Status

The CultivAR application has undergone a significant architectural migration from a monolithic Flask application to a modern, decoupled architecture with a FastAPI backend and a Flutter frontend.

A detailed analysis was performed to ensure that all functionality from the legacy Flask blueprints was successfully migrated to the new architecture. The conclusion of this analysis is that the migration is **complete**.

- **Diagnostics Blueprint:** The functionality of the legacy `diagnostics` blueprint has been fully migrated to the new `health` router in the FastAPI application. The new implementation is significantly more comprehensive, providing detailed health checks, system metrics, and Kubernetes-style liveness and readiness probes.

- **Market Blueprint:** The legacy `market` blueprint, which was responsible for rendering the cart, seed bank, extensions, and gear pages, has been fully migrated to the Flutter frontend. The Flutter application now contains dedicated screens for each of these features, and the backend API provides the necessary data.

All other Flask blueprints have also been successfully migrated to their corresponding routers and API endpoints in the FastAPI application, ensuring functional parity and a clear path for future development on the new architecture.
