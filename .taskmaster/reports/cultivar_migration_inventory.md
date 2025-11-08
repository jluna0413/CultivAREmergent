# Cultivar Migration Inventory Report

Summary
- Total legacy matches found: 300+ (case-insensitive search for strain*)
- Scope: models, API, ORM, tests, frontend, templates, docs

Key findings
- Models:
  - [`app/models/base_models.py`](app/models/base_models.py:296) defines `class Cultivar` and fields; backward alias [`app/models/base_models.py`](app/models/base_models.py:508) `Strain = Cultivar`.
  - [`app/models/__init__.py`](app/models/__init__.py:142) exports `Cultivar` and sets `Strain` alias.
- Pydantic schemas:
  - Legacy compatibility shim: [`app/fastapi_app/models/strains.py`](app/fastapi_app/models/strains.py:32) imports from cultivars and defines `Strain*` aliases with DeprecationWarning.
- API routing / OpenAPI:
  - OpenAPI still exposes `/api/v1/strains/` paths (generated docs include many legacy routes).
- ORM and DB usage:
  - Plant model uses `cultivar_id` and `cultivar_url` (code updated).
  - Numerous code locations still reference `strain_id` in filters and tests; DB schema preserved per decision.
- Frontend and templates:
  - Many templates still contain user-facing "Strain" terms; templates such as [`app/web/templates/views/cultivar.html`](app/web/templates/views/cultivar.html:141) include modal ids/labels referencing strain.
  - Flutter app contains both `cultivar` model files and legacy `strain` fields/variables (deprecated comments present).
- Tests and CI:
  - Tests reference `strain_id` and `/strains` endpoints; many tests were updated but several integration tests still use legacy query params.
- Documentation:
  - Docs and marketing materials contain "strain" in many places; migration docs exist documenting aliases.

Deprecation / backward compatibility verification
- `app/fastapi_app/models/strains.py` emits a DeprecationWarning at import (lines 32-36) — verified.
- Model alias `Strain = Cultivar` present in [`app/models/base_models.py`](app/models/base_models.py:508) and [`app/models/__init__.py`](app/models/__init__.py:142).
- OpenAPI includes both `/cultivars` and `/strains` (legacy mounted) — verify runtime deprecation header behavior during integration testing.

Classification of findings (recommended treatment)
- Safe code-only alias/rename (no DB change): update Python code, Pydantic schemas, Flask blueprints to use Cultivar names but keep legacy Strain aliases.
- Templates/UI text: update user-facing text to Cultivar; keep variable names acceptable for backward compatibility (e.g., allow strain variable in templates).
- Tests: update tests to prefer cultivar naming but accept legacy query params; create migration tests that assert both endpoints work.
- DB schema: no destructive changes; do not rename columns. Use code aliases and, if later desired, create non-destructive Alembic migration separately.

Prioritized patch list (short-term, minimal risk)
1. Ensure all model alias lines exist and are exported (`Strain = Cultivar`) — verify [`app/models/base_models.py`](app/models/base_models.py:508) and [`app/models/__init__.py`](app/models/__init__.py:142).
2. Convert remaining Pydantic/routers to import cultivars primary and maintain strains shim (already implemented in [`app/fastapi_app/models/strains.py`](app/fastapi_app/models/strains.py:10)).
3. Replace in-code occurrences of `strain_id` usage in tests and filters with acceptance handling for both `strain_id` and `cultivar_id` query params.
4. Update templates: rename labels and modal ids to Cultivar while keeping variable alias comments.
5. Update Flutter code: consolidate providers (remove `strains_provider.dart`), keep legacy `Strain` class in provider with @Deprecated comments (already present in [`flutter_app/lib/core/providers/cultivar_provider.dart`](flutter_app/lib/core/providers/cultivar_provider.dart:498)).
6. Regenerate OpenAPI docs after code changes; ensure legacy routes include deprecation notice and header.

Long-term (phase 2)
- Consider non-destructive DB alias columns and controlled migration with Alembic (separate change window).
- Audit external integrations and webhooks that may call /strains endpoints and notify integrators.

Action items I will perform next (with your approval)
- Produce a CSV inventory of all found matches (file paths, line numbers, text snippet) excluding node_modules and build/minified vendor files.
- Create a prioritized patch PR list with one-file-per-commit suggestions (code-only fixes).
- Optionally implement safe code-only fixes in a branch and run targeted tests.

Notes and constraints
- Per your decision, vendor/minified files excluded from replacements.
- Database schema will be preserved for now; code-only aliases used for backward compatibility.

Where to review the raw data
- Inventory and reports will be written to `.taskmaster/reports/cultivar_migration_inventory.md` and `.taskmaster/reports/cultivar_migration_matches.csv` (generated next).

Ready to proceed to generate the full CSV inventory and prioritized patch list. Approve and I will switch to code mode to create artifacts and implement safe fixes, or I can just produce the CSV and patch list for review first.

End of report.