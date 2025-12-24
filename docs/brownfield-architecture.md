# CultivAR Brownfield Architecture Document

## Introduction

This document captures the CURRENT STATE of the CultivAR Flutter application and FastAPI backend codebase, including technical debt, workarounds, and real-world patterns. It serves as a reference for AI agents working on the Flutter verification and Phase 2 feature implementation enhancements.

### Document Scope

Focused on areas relevant to: Flutter verification PRD - Tests and Documentation Implementation, Phase 2 Feature Module Implementation (dashboard, plants). Includes dashboard, plants CRUD, API client implementations, provider patterns, and integration testing.

### Change Log

| Date   | Version | Description                 | Author    |
| ------ | ------- | --------------------------- | --------- |
| 2025-12-07 | 1.0     | Initial brownfield analysis | Architect |

## Quick Reference - Key Files and Entry Points

### Critical Files for Understanding the System

- **Flutter Main Entry**: `flutter_app/lib/main.dart`
- **FastAPI Main Entry**: `app/fastapi_app/main.py`
- **Dashboard Screen**: `flutter_app/lib/features/dashboard/ui/dashboard_screen.dart` (Partially implemented, needs API integration)
- **Plants API**: `app/fastapi_app/routers/plants_api.py` (Backend plants endpoints)
- **Dashboard API**: `app/fastapi_app/routers/dashboard.py` (Backend dashboard stats)
- **API Client**: `flutter_app/lib/core/api/api_client.dart` (Dio-based HTTP client)

### Enhancement Impact Areas

Based on the Flutter verification PRD, these files will be affected:

- `flutter_app/lib/features/dashboard/ui/dashboard_screen.dart` - Wire to real API data
- `flutter_app/lib/features/plants/ui/plants_list_screen.dart` - Complete plants CRUD implementation
- `flutter_app/lib/core/providers/dashboard_provider.dart` - Implement real data fetching
- `flutter_app/lib/core/providers/plants_provider.dart` - Implement plants CRUD operations
- `flutter_app/lib/core/services/dashboard_api_client.dart` - Complete API client implementation
- `flutter_app/lib/core/services/plants_api_service.dart` - Complete plants API service

## High Level Architecture

### Technical Summary

**Frontend**: Flutter mobile/web app with Riverpod state management
**Backend**: FastAPI with async SQLAlchemy, PostgreSQL database
**Architecture Pattern**: Clean Architecture with providers, services, and API layers
**State Management**: Riverpod 3.x with AsyncValue pattern
**Networking**: Dio HTTP client with error handling
**Database**: PostgreSQL with async SQLAlchemy ORM

### Actual Tech Stack (from pubspec.yaml/requirements.txt)

| Category  | Technology | Version | Notes                      |
| --------- | ---------- | ------- | -------------------------- |
| Frontend Runtime   | Flutter SDK | 3.8.0+ | Dart 3.8+ required |
| State Management | Riverpod | 3.0.3 | AsyncValue pattern used |
| Routing | Go Router | 17.0.0 | Declarative routing with guards |
| HTTP Client | Dio | 5.9.0 | REST API communication |
| Forms | flutter_form_builder | 10.2.0 | Complex form handling |
| Charts | fl_chart | 1.1.1 | Dashboard visualization |
| Local Storage | Drift | 2.14.1 | SQLite for offline data |
| Secure Storage | flutter_secure_storage | 9.2.4 | JWT token storage |
| Backend Runtime | FastAPI | 0.104.1 | Async Python web framework |
| Database | PostgreSQL | asyncpg | Async database driver |
| ORM | SQLAlchemy | 2.0.23 | Async ORM with relationships |
| Auth | JWT | python-jose | Token-based authentication |

### Repository Structure Reality Check

- **Type**: Monorepo with Flutter app and Python backend
- **Frontend Location**: `flutter_app/` directory
- **Backend Location**: `app/` directory with FastAPI routers
- **Build System**: Flutter CLI for mobile/web, Python venv for backend
- **Package Manager**: Flutter pub, Python pip
- **Notable**: Mixed architecture - some Flask blueprints still exist alongside FastAPI

## Source Tree and Module Organization

### Flutter App Structure (Actual)

```
flutter_app/
├── lib/
│   ├── main.dart                          # App entry point with router setup
│   ├── core/                              # Shared utilities and services
│   │   ├── api/                           # HTTP client and error handling
│   │   │   ├── api_client.dart            # Dio client with interceptors
│   │   │   └── api_exceptions.dart        # Custom exception types
│   │   ├── providers/                     # Riverpod providers (MIXED STATE)
│   │   │   ├── dashboard_provider.dart    # TODO: Needs real API integration
│   │   │   ├── plants_provider.dart       # TODO: CRUD operations incomplete
│   │   │   └── [other providers]          # Some implemented, some stubs
│   │   ├── services/                      # API service layer
│   │   │   ├── dashboard_api_client.dart  # TODO: Mock implementation only
│   │   │   └── plants_api_service.dart    # TODO: Partial implementation
│   │   └── models/                        # Data models with Freezed
│   │       ├── dashboard_stats.dart       # Dashboard statistics model
│   │       └── plant_models.dart          # Plant-related data structures
│   └── features/                          # Feature-based organization
│       ├── dashboard/                     # Dashboard feature (PARTIALLY COMPLETE)
│       │   └── ui/
│       │       └── dashboard_screen.dart  # UI exists, needs API wiring
│       └── plants/                        # Plants feature (MOSTLY STUBS)
│           └── ui/
│               └── plants_list_screen.dart # TODO: Complete CRUD implementation
```

### Backend Structure (Actual)

```
app/
├── fastapi_app/                          # FastAPI application
│   ├── main.py                           # FastAPI app factory and routes
│   ├── routers/                          # API route handlers
│   │   ├── dashboard.py                  # Dashboard stats endpoints
│   │   ├── plants_api.py                 # Plants CRUD operations
│   │   └── [other routers]               # Auth, users, sensors, etc.
│   ├── models_async/                     # SQLAlchemy async models
│   │   └── [model files]                 # Database table definitions
│   └── dependencies.py                   # Auth and DB dependencies
├── blueprints/                           # LEGACY: Flask blueprints (still used)
│   └── [legacy routes]                   # TODO: Migrate to FastAPI
└── models_async/                         # Shared async models
    └── [database models]                 # Plant, User, Sensor models
```

### Key Modules and Their Purpose

- **Dashboard Feature**: `flutter_app/lib/features/dashboard/` - Statistics display and quick actions (UI exists, API integration missing)
- **Plants Feature**: `flutter_app/lib/features/plants/` - Plant CRUD operations (Heavy TODO state)
- **API Client Layer**: `flutter_app/lib/core/api/` - HTTP communication with backend (Implemented but needs error handling polish)
- **Provider Layer**: `flutter_app/lib/core/providers/` - State management (Mixed - some real, some mock implementations)
- **Dashboard API**: `app/fastapi_app/routers/dashboard.py` - Backend stats endpoints (Implemented)
- **Plants API**: `app/fastapi_app/routers/plants_api.py` - Backend CRUD operations (Implemented)
- **Auth System**: JWT-based with refresh tokens (Mostly implemented across both frontend/backend)

## Data Models and APIs

### Flutter Data Models

Reference actual model files rather than duplicating:

- **DashboardStats**: See `flutter_app/lib/core/models/dashboard_stats.dart` (Freezed-generated model)
- **Plant Models**: See `flutter_app/lib/core/models/plant_models.dart` (Create, Update, List models)
- **User Models**: See `flutter_app/lib/core/models/user_models.dart` (Auth-related models)
- **API Response Models**: See `flutter_app/lib/core/models/` directory

### Backend Data Models

Reference actual SQLAlchemy models:

- **Plant Model**: See `app/models_async/grow.py` (Plant table with relationships)
- **User Model**: See `app/models_async/base.py` (User authentication model)
- **Dashboard Stats**: Computed from multiple tables (plants, activities, sensors)

### API Specifications

- **Plants API**: REST endpoints in `app/fastapi_app/routers/plants_api.py`
  - `GET /api/plants` - List plants with pagination
  - `POST /api/plants` - Create new plant
  - `PUT /api/plants/{id}` - Update plant
  - `DELETE /api/plants/{id}` - Delete plant

- **Dashboard API**: `app/fastapi_app/routers/dashboard.py`
  - `GET /api/dashboard/stats` - Aggregate statistics
  - Returns counts: total_plants, active_plants, strains, harvested

### API Client Implementation

- **HTTP Client**: `flutter_app/lib/core/api/api_client.dart` (Dio with interceptors)
- **Dashboard Service**: `flutter_app/lib/core/services/dashboard_api_client.dart` (TODO: Complete implementation)
- **Plants Service**: `flutter_app/lib/core/services/plants_api_service.dart` (TODO: Complete CRUD operations)

## Technical Debt and Known Issues

### Critical Technical Debt

1. **Incomplete Provider Implementations**: Many Riverpod providers are stub implementations
   - `dashboard_provider.dart` - Returns mock data instead of API calls
   - `plants_provider.dart` - CRUD operations not fully implemented
   - Impact: UI components cannot display real data

2. **Mixed Architecture Patterns**: Flutter app mixes different state management approaches
   - Some features use Riverpod providers correctly
   - Others have TODO comments for API integration
   - Inconsistent error handling patterns

3. **Backend Migration Incomplete**: Flask blueprints still exist alongside FastAPI
   - Some routes still use legacy Flask patterns
   - TODO: Complete migration to FastAPI routers
   - Risk: Maintenance complexity and inconsistent API patterns

4. **Testing Infrastructure Missing**: PRD requires comprehensive testing
   - Unit tests for providers and services mostly missing
   - Integration tests for API flows not implemented
   - Widget tests for UI components incomplete

### Workarounds and Gotchas

- **Provider Dependencies**: Some providers depend on mock services that return static data
- **API Error Handling**: Dio client has basic error handling but needs refinement for different HTTP status codes
- **Database Schema Evolution**: Models exist but migration scripts may be incomplete
- **Environment Configuration**: `.env` files exist but documentation unclear on required variables

## Integration Points and External Dependencies

### Internal Integration Points

- **Flutter ↔ FastAPI**: HTTP REST API with JWT authentication
- **Database Layer**: Async SQLAlchemy with PostgreSQL
- **File Storage**: Local file system for uploads (plants images, etc.)
- **WebSocket Support**: Real-time sensor data updates (implemented but not used in dashboard)

### External Dependencies Status

| Service  | Purpose  | Integration Status | Notes                      |
| -------- | -------- | ------------------ | -------------------------- |
| PostgreSQL | Primary database | ✅ Implemented | Async connections working |
| JWT Auth | User authentication | ✅ Implemented | Refresh token support |
| Flutter Local Storage | Offline data | ⚠️ Partial | Drift setup but not used |
| Firebase Analytics | Usage tracking | ✅ Implemented | Basic event tracking |
| Sensor APIs | Environmental data | ❌ Missing | Backend sensors exist but not connected |

## Development and Deployment

### Local Development Setup

1. **Backend Setup**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   # Set environment variables (.env file)
   uvicorn app.fastapi_app.main:app --reload
   ```

2. **Frontend Setup**:

   ```bash
   cd flutter_app
   flutter pub get
   flutter run -d chrome  # Web development
   flutter run -d emulator  # Mobile development
   ```

3. **Database**: PostgreSQL with asyncpg driver
4. **Environment Variables**: See `.env.example` (backend) and flutter dotenv setup

### Build and Deployment Process

- **Flutter Build**: `flutter build web` or `flutter build apk`
- **Backend Build**: Docker container with gunicorn
- **Deployment**: Manual deployment scripts exist
- **CI/CD**: Basic GitHub Actions setup but needs testing pipeline

## Testing Reality

### Current Test Coverage

- **Unit Tests**: Minimal - some model tests, few provider tests
- **Integration Tests**: None - PRD requires auth flow integration test
- **Widget Tests**: None - UI component testing not implemented
- **API Tests**: None - backend endpoint testing missing

### Testing Infrastructure

- **Frameworks**: Flutter test, Mockito for mocking
- **Test Organization**: `flutter_app/test/` directory exists but mostly empty
- **CI Integration**: GitHub Actions setup but test commands not configured

## Enhancement Impact Analysis

### Files That Will Need Modification

Based on Flutter verification PRD requirements:

**Phase 2 Feature Implementation:**

- `flutter_app/lib/features/dashboard/ui/dashboard_screen.dart` - Wire stats cards to real API data
- `flutter_app/lib/features/plants/ui/plants_list_screen.dart` - Complete plants list, detail, and CRUD operations
- `flutter_app/lib/core/providers/dashboard_provider.dart` - Replace mock data with API calls
- `flutter_app/lib/core/providers/plants_provider.dart` - Implement full CRUD operations
- `flutter_app/lib/core/services/dashboard_api_client.dart` - Complete API client implementation
- `flutter_app/lib/core/services/plants_api_service.dart` - Complete plants API service

**Testing Implementation:**

- `flutter_app/integration_test/auth_flow_test.dart` - Complete integration test (currently missing)
- `flutter_app/test/` - Add unit tests for providers and services
- Test utilities and mock setup

**Documentation:**

- `docs/FLUTTER_UI_GUIDELINES.md` - Create design system documentation
- `docs/TESTING_GUIDE.md` - Complete testing pyramid documentation
- `docs/FLUTTER_DEPLOYMENT.md` - Build and deployment procedures
- `docs/TEMPLATE_MAPPING.md` - Jinja to Flutter widget mapping

### New Files/Modules Needed

- Complete Freezed models for plants CRUD operations
- Additional provider files for complex state management
- Test fixtures and mock data for comprehensive testing
- Integration test utilities and page objects

### Integration Considerations

- **API Compatibility**: Backend endpoints exist but frontend integration incomplete
- **Error Handling**: Consistent error handling needed across providers
- **Loading States**: AsyncValue pattern implementation needed
- **Offline Support**: Drift integration for offline plant data
- **Authentication Flow**: JWT token refresh handling in API client

## Appendix - Useful Commands and Scripts

### Flutter Development Commands

```bash
cd flutter_app

# Development
flutter run -d chrome                    # Web development
flutter run -d emulator                  # Mobile development

# Testing
flutter test                             # Unit tests
flutter test integration_test/           # Integration tests

# Building
flutter build web                        # Web build
flutter build apk --release             # Android APK
flutter build ios --release             # iOS build

# Code generation
flutter pub run build_runner build       # Freezed/Riverpod generation
```

### Backend Development Commands

```bash
# Development
uvicorn app.fastapi_app.main:app --reload

# Database
alembic upgrade head                     # Run migrations
alembic revision --autogenerate          # Create new migration

# Testing
pytest                                   # Run tests
pytest --cov=app                        # Coverage report
```

### Debugging and Troubleshooting

- **Flutter Issues**: Check `flutter doctor` and device logs
- **Backend Issues**: Check FastAPI logs and PostgreSQL connections
- **API Issues**: Use browser dev tools or Postman for endpoint testing
- **State Issues**: Check Riverpod dev tools and provider scopes

## Success Criteria

- Dashboard displays real statistics from backend API
- Plants CRUD operations fully functional with proper error handling
- Integration tests pass with 80% coverage target
- Documentation covers UI guidelines, testing, and deployment
- Provider implementations follow AsyncValue patterns consistently
- API client handles authentication and error states properly
