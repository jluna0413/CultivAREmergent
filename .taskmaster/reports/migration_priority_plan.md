# Prioritized Terminology Migration Plan (Strain → Cultivar)

Summary:
- Goal: systematic, non-destructive migration; maintain backward compatibility.
- Strategy: phased, prioritized by risk (API/auth/tests first).

High-level phases (priority order):
1. Unblock CI & Auth: ensure /api/v1/auth/register exists and tests pass
2. Backend models: finalize Cultivar aliases + DB compatibility
3. API routers/schemas: dual-mount cultivars/strains and pydantic rename
4. Frontend (Flutter): consolidate providers/widgets
5. Templates & JS: rename templates and AJAX endpoints
6. Tests: update tests to use cultivar endpoints/fields
7. Docs & cleanup: update docs, generate OpenAPI, deprecate strains

Priority file list (phase 1—3; immediate actions)
- Auth & routing (critical)
  - [`app/fastapi_app/routers/auth.py`](app/fastapi_app/routers/auth.py:65) — add/register handler or confirm register endpoint
  - [`app/fastapi_app/__init__.py`](app/fastapi_app/__init__.py:88) — verify router includes and prefixes
  - [`docs/generated/openapi.json`](docs/generated/openapi.json:1220) — verify auth paths

- Backend models (high)
  - [`app/models/base_models.py`](app/models/base_models.py:120) — Plant.cultivar_id, Cultivar class, alias `Strain = Cultivar`
  - [`app/models/__init__.py`](app/models/__init__.py:140) — exports and alias `Strain = Cultivar`
  - Alembic migrations directory — create non-destructive migration to add `strain_id` alias column (nullable) and populate mapping

- API layer (high)
  - [`app/fastapi_app/routers/cultivars.py`](app/fastapi_app/routers/cultivars.py:1) — ensure CRUD present
  - [`app/fastapi_app/routers/strains.py`](app/fastapi_app/routers/strains.py:1) — ensure legacy alias routes mount cultivars handlers
  - [`app/fastapi_app/models/cultivars.py`](app/fastapi_app/models/cultivars.py:1) — pydantic schema rename + aliases

- Tests (unblock)
  - [`tests/integration/test_auth.py`](tests/integration/test_auth.py:1) — verify endpoint used
  - All tests referencing `strain_id` — update to accept `cultivar_id` or keep backward compatible acceptance

- Templates & JS (medium)
  - [`app/web/templates/views/strains.html`](app/web/templates/views/strains.fixed.html:1) — rename to cultivars and update content
  - `app/web/static/js/strains-diagnostics.js` → rename and update AJAX endpoints

- Flutter (medium)
  - [`flutter_app/lib/core/state/strains_provider.dart`](flutter_app/lib/core/state/strains_provider.dart:1) and [`flutter_app/lib/core/providers/cultivar_provider.dart`](flutter_app/lib/core/providers/cultivar_provider.dart:497) — consolidate providers
  - widgets: `strain_card` → merge into `cultivar_card.dart`

Migration risk & mitigation
- Risk: DB schema mismatch — Mitigation: Alembic non-destructive migration adding nullable `strain_id` and triggers or mapping script; keep ORM aliases.
- Risk: External integrations using /strains — Mitigation: Dual-mount legacy `/api/v1/strains` returning deprecation header.
- Risk: Large test changes — Mitigation: update tests incrementally, keep compatibility where needed.

Immediate actionable checklist (max 7 atomic steps)
1. Add/confirm POST /api/v1/auth/register handler in [`app/fastapi_app/routers/auth.py`](app/fastapi_app/routers/auth.py:65). Run tests.
2. Create Alembic migration: add nullable `strain_id` to `plant` table + data backfill script.
3. Ensure `Strain = Cultivar` aliases present in [`app/models/base_models.py`](app/models/base_models.py:508) and [`app/models/__init__.py`](app/models/__init__.py:142).
4. Rename/verify Pydantic models file to [`app/fastapi_app/models/cultivars.py`](app/fastapi_app/models/cultivars.py:1) with aliases for old class names.
5. Dual-mount routers in [`app/fastapi_app/__init__.py`](app/fastapi_app/__init__.py:88) (already present) and add deprecation headers.
6. Run integration tests and fix failures iteratively (auth → plants → cultivars).
7. Consolidate Flutter providers/widgets and run flutter test.

Deliverables I'll produce next (upon your confirmation)
- Detailed per-file change list (rename plan) and patch set (PR-ready)
- Alembic migration file (non-destructive) and validation script
- Quick fix PR for auth register endpoint (optional) to unblock CI

Confirm I should produce the full per-file PR patch set now or first generate the Alembic migration file.