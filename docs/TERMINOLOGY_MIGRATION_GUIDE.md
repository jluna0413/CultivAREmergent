# Strain→Cultivar Terminology Migration Guide

## Overview

This document provides comprehensive guidance for the systematic migration from "strain" to "cultivar" terminology across the CultivAR platform. This change represents a shift from industry-standard terminology to more scientifically accurate language, better aligning with agricultural and horticultural standards.

## What Changed

### Terminology Shift
- **"Strain"** → **"Cultivar"** throughout the platform
- User-facing text updated to use "Cultivar" consistently
- API endpoints now use `/cultivars/*` as primary paths
- Database schema maintains backward compatibility
- All code, documentation, and tests updated

### Primary Changes by Layer

#### 1. Backend Models
- **Legacy Flask Models**: `Strain` class renamed to `Cultivar` with backward compatibility alias
- **Async Models**: Already used `Cultivar` terminology (no changes needed)
- **Database**: Column names remain `cultivar_id`, `cultivar_name` (already correct)
- **Relationships**: Updated to use `cultivar` relationship names

#### 2. API Layer
- **Primary Endpoints**: `/api/v1/cultivars/*` (new canonical endpoints)
- **Legacy Endpoints**: `/api/v1/strains/*` (maintained for backward compatibility)
- **Pydantic Models**: Renamed from `Strain*` to `Cultivar*`
- **Handler Modules**: Renamed from `strain_handlers` to `cultivar_handlers`
- **Activity Types**: Updated from `strain_add/edit/deleted` to `cultivar_add/edit/deleted`

#### 3. Frontend (Flutter)
- **Provider Classes**: Consolidated to single `CultivarProvider`
- **Widget Components**: Consolidated to single `CultivarCard` widget
- **Model Classes**: Updated to use `Cultivar` terminology
- **API Services**: Updated to use `/cultivars/*` endpoints
- **Screen Components**: All text and labels use "Cultivar" terminology

#### 4. Templates & JavaScript
- **HTML Templates**: Renamed `strains.html` → `cultivars.html`, etc.
- **Template Content**: All user-facing text updated to "Cultivar"
- **JavaScript Functions**: Updated endpoint calls and function names
- **CSS Classes**: Updated to use `cultivar-*` naming convention

#### 5. Testing
- **Test Files**: Renamed `test_strains.py` → `test_cultivars.py`
- **Test Functions**: Updated to use `cultivar` terminology
- **Test Data**: All test data uses "cultivar" descriptions
- **Integration Tests**: Updated API endpoint tests for both paths

#### 6. Documentation
- **User Guides**: All terminology updated to "Cultivar"
- **API Documentation**: References both `/cultivars/*` and `/strains/*`
- **Developer Docs**: Code examples use new terminology
- **Migration Guides**: This document and backward compatibility guide

## Backward Compatibility

### Maintained Compatibility Points

#### 1. Python Import Compatibility
```python
# These imports still work:
from app.models import Strain  # Points to Cultivar class
from app.models import Cultivar  # Direct import

# Both resolve to the same Cultivar class
assert Strain is Cultivar  # True
```

#### 2. API Endpoint Compatibility
```bash
# Both of these work:
GET /api/v1/cultivars/          # Primary endpoint
GET /api/v1/strains/            # Legacy alias (redirects to /cultivars)

POST /api/v1/cultivars/         # Primary endpoint
POST /api/v1/strains/           # Legacy alias (redirects to /cultivars)
```

#### 3. Database Schema Compatibility
- Existing `cultivar` table remains unchanged
- No database migration required
- All existing `cultivar_id` foreign keys continue to work
- No data loss or schema changes

#### 4. Flask Blueprint Compatibility
```python
# Both route definitions work:
@bp.route('/cultivars')     # New primary route
@bp.route('/strains')       # Legacy alias route (redirects)

# Both generate the same URLs:
url_for('cultivars.list')   # /cultivars
url_for('strains.list')     # /strains (legacy)
```

### Legacy Support Timeline
- **Phase 1** (Current): Both endpoints fully functional
- **Phase 2** (6 months): Legacy endpoints marked as deprecated
- **Phase 3** (12 months): Legacy endpoints emit deprecation warnings
- **Phase 4** (18 months): Legacy endpoints may be removed (configurable)

## Migration Guide for Developers

### If You're Using the Legacy API

#### Quick Fix (No Code Changes Required)
If you're using the legacy `/strains/*` endpoints, they will continue to work without any changes:

```python
# This will continue to work for now:
response = requests.get('https://api.example.com/api/v1/strains/')
```

#### Recommended Migration (Future-Proof)
Update your code to use the new endpoints:

```python
# Old (still works but deprecated):
response = requests.get('https://api.example.com/api/v1/strains/')

# New (recommended):
response = requests.get('https://api.example.com/api/v1/cultivars/')
```

### If You're Extending the Backend

#### Model Updates
```python
# Old way (still works):
from app.models import Strain

# New way (recommended):
from app.models import Cultivar

# Both are equivalent:
strain_instance = Strain(name="OG Kush")  # Works
cultivar_instance = Cultivar(name="OG Kush")  # Recommended

# Check compatibility:
assert isinstance(strain_instance, Cultivar)  # True
assert isinstance(cultivar_instance, Strain)  # True
```

#### Handler Updates
```python
# Old import (still works):
from app.handlers.strain_handlers import create_strain

# New import (recommended):
from app.handlers.cultivar_handlers import create_cultivar

# Both reference the same function:
assert create_strain is create_cultivar  # True
```

### If You're Working on the Frontend

#### Provider Usage
```dart
// Old provider (deprecated):
final strainsProvider = Provider.of<StrainsProvider>(context);

// New provider (recommended):
final cultivarProvider = Provider.of<CultivarProvider>(context);

// Both work the same way:
cultivarProvider.fetchCultivars(); // Works with both providers
```

#### Model Updates
```dart
// Old model (still works):
final strain = Strain(name: "OG Kush");

// New model (recommended):
final cultivar = Cultivar(name: "OG Kush");

// Both are equivalent:
assert(strain is Cultivar); // True
```

## API Changes

### Endpoint Comparison

| Old Endpoint | New Endpoint | Status |
|-------------|-------------|---------|
| `GET /api/v1/strains/` | `GET /api/v1/cultivars/` | ✅ Both Work |
| `POST /api/v1/strains/` | `POST /api/v1/cultivars/` | ✅ Both Work |
| `GET /api/v1/strains/{id}` | `GET /api/v1/cultivars/{id}` | ✅ Both Work |
| `PUT /api/v1/strains/{id}` | `PUT /api/v1/cultivars/{id}` | ✅ Both Work |
| `DELETE /api/v1/strains/{id}` | `DELETE /api/v1/cultivars/{id}` | ✅ Both Work |

### Response Format Changes

#### Old Response
```json
{
  "data": {
    "strain": {
      "id": 1,
      "name": "OG Kush",
      "type": "hybrid",
      "strain_url": "https://example.com/og-kush"
    }
  }
}
```

#### New Response
```json
{
  "data": {
    "cultivar": {
      "id": 1,
      "name": "OG Kush",
      "type": "hybrid",
      "cultivar_url": "https://example.com/og-kush"
    }
  }
}
```

## Database Changes

### No Schema Changes Required
The database schema already used `cultivar` table and column names, so no migration is needed:

```sql
-- This table already existed and continues to work:
SELECT * FROM cultivar WHERE name = 'OG Kush';

-- Foreign key relationships already used cultivar_id:
SELECT * FROM plant WHERE cultivar_id = 1;
```

## Testing Migration

### Running Tests
All tests have been updated and should pass with the new terminology:

```bash
# Backend tests
pytest tests/ -v

# Flutter tests
cd flutter_app && flutter test
```

### Test Migration
If you have custom tests that reference the old terminology:

```python
# Old test (update this):
def test_strain_creation():
    strain = create_strain(name="OG Kush")
    assert strain.name == "OG Kush"

# New test (recommended):
def test_cultivar_creation():
    cultivar = create_cultivar(name="OG Kush")
    assert cultivar.name == "OG Kush"
    # Legacy test still works:
    assert isinstance(cultivar, Strain)  # True
```

## Migration Validation

### Automated Validation
Use the validation script to check your migration status:

```bash
# Run validation
python scripts/validate_terminology_migration.py

# Strict validation (fails on any strain references)
python scripts/validate_terminology_migration.py --strict

# Check backward compatibility
python scripts/validate_terminology_migration.py --check-backward-compat
```

### Manual Verification Checklist

#### Backend Verification
- [ ] `Cultivar` class exists in `app/models/base_models.py`
- [ ] `Strain = Cultivar` alias exists for backward compatibility
- [ ] Both `/cultivars/*` and `/strains/*` API endpoints work
- [ ] All Pydantic models use `Cultivar*` naming
- [ ] Activity types use `cultivar_*` naming

#### Frontend Verification
- [ ] `CultivarProvider` exists and works
- [ ] `CultivarCard` widget renders correctly
- [ ] All Flutter models use `Cultivar` terminology
- [ ] API client uses `/cultivars/*` endpoints
- [ ] No duplicate provider/widget classes

#### Template Verification
- [ ] All HTML templates use "Cultivar" in user-facing text
- [ ] Template file names use `cultivar` (not `strain`)
- [ ] JavaScript endpoints point to `/cultivars/*`
- [ ] CSS classes use `cultivar-*` naming

## Troubleshooting

### Common Issues

#### Import Errors
**Problem**: `ImportError: cannot import name 'Strain'`
**Solution**: `Strain` is still importable via `from app.models import Strain`

#### API 404 Errors
**Problem**: Getting 404 on `/api/v1/strains/*`
**Solution**: Both endpoints should work. Check that the router is properly mounted.

#### Template Errors
**Problem**: Template not found errors
**Solution**: Templates were renamed. Use `cultivars.html` instead of `strains.html`

#### Flutter Build Errors
**Problem**: Provider not found errors
**Solution**: Use `CultivarProvider` instead of deprecated `StrainsProvider`

### Getting Help

1. **Check the validation script**: Run `python scripts/validate_terminology_migration.py`
2. **Review backward compatibility**: Check `docs/BACKWARD_COMPATIBILITY_STRATEGY.md`
3. **Check logs**: Look for deprecation warnings in application logs
4. **Test endpoints**: Verify both `/cultivars/*` and `/strains/*` work in your environment

## Rollback Procedure

If you need to rollback the migration:

### Emergency Rollback Steps
1. **Revert file changes**: Restore files from before migration
2. **Re-enable legacy routes**: Ensure `/strains/*` endpoints are available
3. **Database rollback**: No database changes, so no rollback needed
4. **Test functionality**: Verify legacy endpoints work correctly

### Note on Rollback
The migration was designed to be reversible, but we recommend using the new `cultivar` terminology going forward for better long-term support and consistency.

## Next Steps

### For Developers
1. **Update integrations**: Migrate from `/strains/*` to `/cultivars/*` endpoints
2. **Update imports**: Use `Cultivar` instead of `Strain` in new code
3. **Test thoroughly**: Run full test suite after migration
4. **Monitor for issues**: Watch for any unexpected behavior

### For Users
1. **No action required**: All existing functionality continues to work
2. **Updated UI**: You'll see "Cultivar" instead of "Strain" throughout the interface
3. **Same features**: All features and data remain exactly the same

### For Administrators
1. **Monitor endpoints**: Watch for any issues with the dual endpoint setup
2. **User communication**: Inform users about the terminology change
3. **Documentation updates**: Ensure all user documentation reflects the change

## Conclusion

This migration represents a significant but backward-compatible improvement to the CultivAR platform. The change to "cultivar" terminology aligns with industry standards and provides a more professional and scientifically accurate user experience.

All existing integrations, data, and functionality continue to work without any changes required. The new terminology provides better long-term maintainability and developer experience.

For questions or issues with this migration, please refer to the troubleshooting section or contact the development team.