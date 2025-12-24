# Tech Stack: CultivAR

## Frontend
- **Framework**: Flutter (Web & Mobile)
- **State Management**: Riverpod
- **Routing**: GoRouter
- **Animations**: flutter_animate
- **Charts**: fl_chart
- **Icons**: Material Icons, flutter_svg

## Backend (Port 4200)
- **Framework**: FastAPI (Python) - *Async-First*
- **Database**: 
  - **Relational**: PostgreSQL (Production) / SQLite (Development) using SQLAlchemy 2.0 (Async).
  - **NoSQL/Cache**: Redis for real-time sensor caching and rate limiting.
- **Migrations**: Alembic for schema evolution.
- **Security**: 
  - JWT for session-based auth.
  - Moving to OAuth 2.0 / Keycloak for enterprise-grade identity.
  - Multi-layered Middleware (CORS, Rate Limiting, CSP).
- **Communication**: WebSockets for live sensor telemetry.

## Frontend (Port 4242)
- **Framework**: Flutter Web & Mobile
- **State Management**: Riverpod (Modern, provider-based).
- **Routing**: GoRouter (Declarative routing).
- **Networking**: Dio with integrated Interceptors for Auth.
- **UI Logic**: Feature-First architecture with modular components.
- **Analytics**: Live charting via fl_chart.
