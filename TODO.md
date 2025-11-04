# CultivAR Backend Implementation Plan

## Phase 1: Infrastructure & Router Setup
- [ ] 1.1 Wire admin router in FastAPI app (`app/fastapi_app/__init__.py`)
- [ ] 1.2 Verify all routers are included in FastAPI app initialization
- [ ] 1.3 Update API documentation structure for `/api/v1/*` routing

## Phase 2: Documentation Updates  
- [ ] 2.1 Update `docs/API-Parity.md` with current router status
- [ ] 2.2 Document remaining gaps (users, activities, sensors)
- [ ] 2.3 Link endpoints to Pydantic schemas
- [ ] 2.4 Update deployment and test documentation

## Phase 3: Async Standardization
- [ ] 3.1 Convert auth.py to AsyncSession usage
- [ ] 3.2 Ensure all routers import from `app.models_async.*`
- [ ] 3.3 Update dependencies.py for async database patterns
- [ ] 3.4 Remove sync session dependencies and mocks

## Phase 4: API Structure Separation
- [ ] 4.1 Separate Plants API: pure JSON endpoints under `/api/v1/plants`
- [ ] 4.2 Keep legacy HTML flows under `/plants`
- [ ] 4.3 Create proper Pydantic request/response models
- [ ] 4.4 Implement pagination for API endpoints

## Phase 5: Migration Infrastructure
- [ ] 5.1 Initialize Alembic for database migrations
- [ ] 5.2 Generate baseline revision covering models_async
- [ ] 5.3 Document migration workflow
- [ ] 5.4 Include in deployment checklist

## Phase 6: Quality Assurance & CI
- [ ] 6.1 Fix backend blockers (bug-101 to bug-105)
- [ ] 6.2 Add CI workflows with lint/tests
- [ ] 6.3 Generate OpenAPI snapshot with diff
- [ ] 6.4 Create integration tests
- [ ] 6.5 Update test plan with acceptance criteria

## Phase 7: Final Integration & Tagging
- [ ] 7.1 Verify route map passes (no duplicate prefixes)
- [ ] 7.2 Test Auth E2E with real DB and AsyncSession
- [ ] 7.3 Validate all JSON-only endpoints under `/api/v1/*`
- [ ] 7.4 Confirm Alembic migrations run green in CI
- [ ] 7.5 Tag backend v2.0.0-beta

## Phase 8: Flutter UI Migration Preparation
- [ ] 8.1 Scaffold Flutter lib/ structure
- [ ] 8.2 Create AuthService, ApiClient, GoRouter setup
- [ ] 8.3 Implement Dashboard→Plants→Strains flows
- [ ] 8.4 Add Flutter golden tests and integration tests
- [ ] 8.5 Prepare phased rollout with feature flags
