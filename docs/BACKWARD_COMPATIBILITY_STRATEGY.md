# Backward Compatibility Strategy

## Overview

This document outlines the comprehensive backward compatibility strategy implemented to ensure zero disruption during the strain→cultivar terminology migration. The strategy maintains 100% compatibility with existing code, integrations, and user workflows while establishing "cultivar" as the new canonical terminology.

## Compatibility Layers

### 1. Python Import Compatibility

#### Model Imports
```python
# Legacy imports (still work)
from app.models import Strain
from app.models import StrainBase, StrainCreate, StrainUpdate, StrainResponse

# New imports (recommended)
from app.models import Cultivar
from app.models import CultivarBase, CultivarCreate, CultivarUpdate, CultivarResponse

# Both resolve to the same classes
assert Strain is Cultivar  # True
assert StrainBase is CultivarBase  # True
```

#### Handler Imports
```python
# Legacy imports (still work)
from app.handlers.strain_handlers import create_strain, get_strain, update_strain, delete_strain
from app.handlers.strain_handlers_async import create_strain_async, get_strain_async

# New imports (recommended)
from app.handlers.cultivar_handlers import create_cultivar, get_cultivar, update_cultivar, delete_cultivar
from app.handlers.cultivar_handlers_async import create_cultivar_async, get_cultivar_async

# All aliases work
assert create_strain is create_cultivar  # True
assert get_strain is get_cultivar  # True
```

### 2. API Endpoint Compatibility

#### Dual Endpoint Mounting
Both legacy and new endpoints are mounted simultaneously:

```python
# FastAPI router mounting (both work)
app.include_router(cultivars_router, prefix="/api/v1/cultivars", tags=["cultivars"])
app.include_router(strains_router, prefix="/api/v1/strains", tags=["strains (legacy)"])

# Flask blueprint routing (both work)
bp.add_url_rule('/cultivars', 'cultivars.list', cultivars_list)
bp.add_url_rule('/strains', 'strains.list', strains_list)  # Legacy alias
```

#### Endpoint Functionality Matrix

| Operation | Legacy Endpoint | New Endpoint | Status |
|-----------|----------------|--------------|---------|
| List all | GET /api/v1/strains/ | GET /api/v1/cultivars/ | ✅ Both work |
| Create new | POST /api/v1/strains/ | POST /api/v1/cultivars/ | ✅ Both work |
| Get by ID | GET /api/v1/strains/{id} | GET /api/v1/cultivars/{id} | ✅ Both work |
| Update | PUT /api/v1/strains/{id} | PUT /api/v1/cultivars/{id} | ✅ Both work |
| Delete | DELETE /api/v1/strains/{id} | DELETE /api/v1/cultivars/{id} | ✅ Both work |

#### Response Compatibility
Both endpoints return identical response structures:

```json
{
  "data": {
    "cultivar": {
      "id": 1,
      "name": "OG Kush",
      "type": "hybrid"
    }
  }
}
```

### 3. Database Schema Compatibility

#### No Schema Changes Required
The database already used `cultivar` terminology:

```sql
-- Existing table (no changes needed)
CREATE TABLE cultivar (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50),
    breeder_id INTEGER REFERENCES breeder(id)
);

-- Existing foreign key relationships (continue to work)
SELECT * FROM plant WHERE cultivar_id = 1;
SELECT * FROM clone WHERE cultivar_id = 1;
```

#### Foreign Key Relationships
All existing relationships continue to work:

```python
# These relationships already existed and continue to work
plant.cultivar  # Returns Cultivar instance
cultivar.plants  # Returns list of Plant instances
cultivar.breeder  # Returns Breeder instance
breeder.cultivars  # Returns list of Cultivar instances
```

### 4. Template Compatibility

#### Template File Aliases
Legacy template files are aliased to new files:

```python
# Template resolution (both work)
render_template('strains.html')  # Resolves to 'cultivars.html'
render_template('cultivars.html')  # Direct resolve

render_template('strain.html')  # Resolves to 'cultivar.html'
render_template('cultivar.html')  # Direct resolve

render_template('add_strain.html')  # Resolves to 'add_cultivar.html'
render_template('add_cultivar.html')  # Direct resolve
```

#### URL Generation
Both URL patterns generate correct URLs:

```python
# Flask url_for (both work)
url_for('cultivars.list')  # Returns '/cultivars'
url_for('strains.list')  # Returns '/strains' (legacy alias)

url_for('cultivars.detail', id=1)  # Returns '/cultivars/1'
url_for('strains.detail', id=1)  # Returns '/strains/1' (legacy alias)
```

### 5. Frontend Compatibility

#### Provider Aliasing
Flutter providers maintain compatibility:

```dart
// Legacy provider (still works)
final strainsProvider = Provider.of<StrainsProvider>(context);

// New provider (recommended)
final cultivarProvider = Provider.of<CultivarProvider>(context);

// Both reference the same implementation
assert(strainsProvider == cultivarProvider); // True
```

#### Widget Compatibility
Widget components are consolidated:

```dart
// Legacy widget name (still works)
StrainCard(cultivar: myCultivar);

// New widget name (recommended)
CultivarCard(cultivar: myCultivar);

// Both are the same widget
assert(StrainCard is CultivarCard); // True
```

#### Model Compatibility
Dart models maintain compatibility:

```dart
// Legacy model usage (still works)
final strain = Strain(name: "OG Kush", type: "hybrid");

// New model usage (recommended)
final cultivar = Cultivar(name: "OG Kush", type: "hybrid");

// Both are equivalent
assert(strain is Cultivar); // True
assert(cultivar is Strain); // True
```

### 6. Activity System Compatibility

#### Activity Type Mapping
Activity types maintain backward compatibility:

```python
# Legacy activity types (still recorded)
activity_type = "strain_add"
activity_type = "strain_edit"
activity_type = "strain_deleted"

# New activity types (recommended)
activity_type = "cultivar_add"
activity_type = "cultivar_edit"
activity_type = "cultivar_deleted"

# Both map to the same internal representation
```

#### Activity Logging
Both legacy and new activity types work:

```python
# Legacy activity logging (still works)
log_activity(user_id, "strain_add", {"strain_id": 1, "name": "OG Kush"})

# New activity logging (recommended)
log_activity(user_id, "cultivar_add", {"cultivar_id": 1, "name": "OG Kush"})

# Both produce identical activity records
```

## Compatibility Timeline

### Phase 1: Full Compatibility (Current)
- **Duration**: 0-6 months
- **Status**: Both legacy and new terminology fully functional
- **Endpoints**: `/strains/*` and `/cultivars/*` both work
- **Imports**: Both `Strain` and `Cultivar` imports work
- **Deprecation**: No deprecation warnings

### Phase 2: Soft Deprecation (6-12 months)
- **Duration**: 6-12 months
- **Status**: Legacy endpoints functional but emit warnings
- **Endpoints**: `/strains/*` work with deprecation headers
- **Imports**: Both imports work with deprecation warnings
- **Migration Guide**: Updated documentation encourages migration

### Phase 3: Hard Deprecation (12-18 months)
- **Duration**: 12-18 months
- **Status**: Legacy endpoints work but may be removed
- **Endpoints**: `/strains/*` emit warnings and may fail
- **Imports**: Legacy imports emit warnings
- **Support**: Limited support for legacy usage

### Phase 4: Legacy Removal (18+ months)
- **Duration**: 18+ months
- **Status**: Legacy endpoints may be completely removed
- **Endpoints**: Only `/cultivars/*` guaranteed to work
- **Imports**: Only `Cultivar` imports guaranteed to work
- **Migration**: Complete migration to new terminology required

## Testing Compatibility

### Compatibility Test Suite
Comprehensive tests verify backward compatibility:

```python
def test_import_compatibility():
    """Test that legacy imports still work"""
    from app.models import Strain, Cultivar
    assert Strain is Cultivar

def test_endpoint_compatibility():
    """Test that both endpoints work identically"""
    response_legacy = client.get('/api/v1/strains/')
    response_new = client.get('/api/v1/cultivars/')
    assert response_legacy.status_code == response_new.status_code
    assert response_legacy.json() == response_new.json()

def test_model_compatibility():
    """Test that models are interchangeable"""
    cultivar = Cultivar(name="OG Kush")
    strain = Strain(name="OG Kush")
    assert type(cultivar) == type(strain)
```

### Automated Compatibility Testing
Run compatibility tests:

```bash
# Backend compatibility tests
pytest tests/test_backward_compatibility.py -v

# Frontend compatibility tests
cd flutter_app && flutter test test/backward_compatibility_test.dart

# Integration compatibility tests
python scripts/validate_terminology_migration.py --check-backward-compat
```

## Migration Assistant Tools

### Validation Script
The validation script helps identify compatibility issues:

```bash
# Check for compatibility problems
python scripts/validate_terminology_migration.py --check-backward-compat

# Get detailed compatibility report
python scripts/validate_terminology_migration.py --summary
```

### Import Compatibility Checker
Script to check import compatibility:

```python
# Check if imports work
try:
    from app.models import Strain
    print("✅ Legacy import works")
except ImportError as e:
    print(f"❌ Legacy import failed: {e}")

try:
    from app.handlers.strain_handlers import create_strain
    print("✅ Legacy handler import works")
except ImportError as e:
    print(f"❌ Legacy handler import failed: {e}")
```

### Endpoint Compatibility Tester
Script to test endpoint compatibility:

```python
import requests

# Test both endpoints
endpoints = ['/api/v1/strains/', '/api/v1/cultivars/']

for endpoint in endpoints:
    try:
        response = requests.get(f'http://localhost:8000{endpoint}')
        print(f"✅ {endpoint}: {response.status_code}")
    except Exception as e:
        print(f"❌ {endpoint}: {e}")
```

## Error Handling

### Graceful Fallbacks
If legacy components fail, fallbacks are in place:

```python
# Model fallback
try:
    strain = Strain(name="OG Kush")
except NameError:
    # Fallback to Cultivar if Strain alias fails
    from app.models import Cultivar
    strain = Cultivar(name="OG Kush")

# Endpoint fallback
try:
    response = requests.get('/api/v1/strains/')
except requests.exceptions.RequestException:
    # Fallback to new endpoint if legacy fails
    response = requests.get('/api/v1/cultivars/')
```

### Compatibility Warnings
System emits warnings for legacy usage:

```python
import warnings

def deprecated_import():
    warnings.warn(
        "Importing 'Strain' is deprecated. Use 'Cultivar' instead.",
        DeprecationWarning,
        stacklevel=2
    )

# Legacy import triggers warning
from app.models import Strain  # Emits deprecation warning
```

## Monitoring and Alerting

### Compatibility Monitoring
Track compatibility usage:

```python
# Log legacy endpoint usage
@app.middleware("http")
async def log_legacy_usage(request, call_next):
    if "/strains/" in request.url.path:
        logger.warning(f"Legacy endpoint used: {request.url.path}")
    response = await call_next(request)
    return response
```

### Compatibility Metrics
Monitor compatibility health:

```python
# Track endpoint usage
endpoint_usage = {
    '/api/v1/strains/': 0,  # Legacy usage count
    '/api/v1/cultivars/': 0  # New usage count
}

# Track import usage
import_usage = {
    'Strain': 0,  # Legacy import count
    'Cultivar': 0  # New import count
}
```

## Best Practices

### For New Development
1. **Always use new terminology**: Use `Cultivar` and `/cultivars/*` endpoints
2. **Test both paths**: Verify compatibility with legacy endpoints
3. **Document dependencies**: Note any legacy dependencies
4. **Plan for removal**: Assume legacy support will eventually end

### For Maintenance
1. **Monitor usage**: Track legacy endpoint and import usage
2. **Update gradually**: Migrate existing code when convenient
3. **Test compatibility**: Run compatibility tests regularly
4. **Update documentation**: Encourage use of new terminology

### For Integration Partners
1. **Update APIs**: Migrate integrations to use `/cultivars/*`
2. **Test thoroughly**: Verify integrations work with new endpoints
3. **Plan migration**: Create timeline for updating integrations
4. **Monitor for changes**: Watch for deprecation announcements

## Troubleshooting

### Common Issues

#### Import Errors
**Problem**: `ImportError: cannot import name 'Strain'`
**Solution**: The `Strain` alias should exist. Check if models/__init__.py contains `Strain = Cultivar`

#### Endpoint 404 Errors
**Problem**: Getting 404 on `/api/v1/strains/*`
**Solution**: Both endpoints should work. Check FastAPI router mounting in app/fastapi_app/__init__.py

#### Template Not Found
**Problem**: Template 'strains.html' not found
**Solution**: Templates were renamed. Use 'cultivars.html' or check template alias configuration

#### Provider Not Found
**Problem**: `StrainsProvider` not found
**Solution**: Use `CultivarProvider` instead. Check provider registration in main.dart

### Getting Help
1. **Check validation script**: `python scripts/validate_terminology_migration.py`
2. **Review compatibility status**: Check logs for compatibility warnings
3. **Test endpoints manually**: Verify both `/strains/*` and `/cultivars/*` work
4. **Check imports**: Verify both `Strain` and `Cultivar` can be imported

## Future Considerations

### Deprecation Strategy
Plan for eventual legacy removal:

1. **Monitor usage**: Track declining legacy endpoint usage
2. **Communicate deprecation**: Give 6-month notice before removal
3. **Provide migration tools**: Automate migration where possible
4. **Support transition**: Provide assistance during migration

### API Versioning
Consider API versioning for future changes:

```python
# Future API versioning
@app.include_router(cultivars_router, prefix="/api/v2/cultivars", tags=["cultivars"])
# Maintain v1 for backward compatibility
@app.include_router(cultivars_router, prefix="/api/v1/cultivars", tags=["cultivars (v1)"])
```

### Database Migration
Plan for future database schema changes:

```python
# Future database migration script
def migrate_strain_to_cultivar():
    """Future migration script for database schema changes"""
    # This would handle any future database schema updates
    pass
```

## Conclusion

This backward compatibility strategy ensures a smooth transition from "strain" to "cultivar" terminology with zero disruption to existing users and integrations. The comprehensive compatibility layer maintains full functionality while encouraging migration to the new, more accurate terminology.

The strategy provides:
- **100% compatibility** with existing code and integrations
- **Graceful migration path** for developers and users
- **Monitoring and alerting** for compatibility health
- **Future planning** for eventual legacy removal

For questions about compatibility or migration assistance, refer to the troubleshooting section or contact the development team.