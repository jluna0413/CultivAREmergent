# Story: Fix Alembic Migrations

**ID:** STORY-GNFT-003
**Epic:** EPIC-GNFT-001
**Priority:** P0 (Critical Blocker)
**Status:** Ready for Dev

## 1. User Story
As a **System Administrator**, I need the **database migration system** to function correctly so that I can apply new schema changes (Genetics Marketplace tables) without error.

## 2. Context
The current Alembic state is broken (`Can't locate revision identified by '2025_11_07_0301'`). This prevents any new tables (`gnft_listings`, `orders`, etc.) from being created, blocking the entire Marketplace Epic.

## 3. Implementation Plan
1.  **Reset Migrations**: Remove all existing migration files in `alembic/versions`.
2.  **Clean Database**: Drop the `alembic_version` table in Postgres (and potentially recreate schema if needed).
3.  **Baseline Generation**: Run `alembic revision --autogenerate -m "Initial baseline"` to capture the current state.
4.  **Verification**: Apply `alembic upgrade head` and confirm it succeeds.

## 4. Acceptance Criteria
- [ ] Command `alembic upgrade head` runs without error.
- [ ] Database contains all 25+ new Marketplace tables defined in models.
- [ ] `alembic_version` table contains the valid current revision hash.

## 5. Technical Notes
- **Env**: Run inside `docker-compose` to ensure DB connectivity.
- **Models**: Ensure `app/models_async/__init__.py` imports all models so `target_metadata` sees them.
