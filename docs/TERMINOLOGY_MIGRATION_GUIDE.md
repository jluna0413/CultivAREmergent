# Terminology Migration Guide: Strain → Cultivar

## Overview

This document provides a comprehensive guide to the systematic migration from "strain" to "cultivar" terminology across the CultivAR Emergant platform. This migration standardizes our botanical language while maintaining full backward compatibility.

## Migration Background

**Why "Cultivar"?**
- Cannabis varieties are technically "cultivars" (cultivated varieties), not "strains"
- Aligns with scientific botanical terminology
- Eliminates confusion with microbial strain terminology
- Provides clearer distinction in scientific contexts

**Migration Scope:**
- 100+ files across 7 layers: database, ORM, API, frontend, templates, tests, documentation
- Maintains backward compatibility during transition period
- Zero breaking changes for existing users

## What Changed

### 1. Database Layer
```sql
-- Before: strain table
SELECT * FROM strain WHERE breeder_id = 123;

-- After: cultivar table (async models already used this)
SELECT * FROM cultivar WHERE breeder_id = 123;

-- Legacy models still reference strain table for compatibility
```

### 2. Python Models
```python
# Before
class Strain(db.Model):
    def __init__(self, strain_name, strain_type):
        self.strain_name = strain_name
        self.strain_type = strain_type

# After
class Cultivar(db.Model):
    def __init__(self, name, type):  # More concise
        self.name = name
        self.type = type

# Backward compatibility
Strain = Cultivar  # Alias for transition period
```

### 3. API Endpoints
```python
# Before: /api/v1/strains/*
GET /api/v1/strains/           # List all strains
GET /api/v1/strains/{id}       # Get specific strain
POST /api/v1/strains/          # Create strain

# After: /api/v1/cultivars/* (primary)
GET /api/v1/cultivars/         # List all cultivars
GET /api/v1/cultivars/{id}     # Get specific cultivar
POST /api/v1/cultivars/        # Create cultivar

# Backward compatibility: /api/v1/strains/* (deprecated but functional)
GET /api/v1/strains/           # Still works, redirects to /cultivars
```

### 4. Pydantic Schemas
```python
# Before
class StrainBase(BaseModel):
    strain_name: str
    strain_type: str

# After
class CultivarBase(BaseModel):
    name: str              # Simpler field name
    type: str              # Type is implied in context
    # All other fields maintained

# Backward compatibility
StrainBase = CultivarBase  # Alias
```

### 5. Flutter/Dart Code
```dart
// Before
class StrainProvider extends ChangeNotifier {
  List<Strain> strains = [];
  Future<void> fetchStrains() async {
    final response = await http.get('/api/v1/strains/');
    // ...
  }
}

// After
class CultivarProvider extends ChangeNotifier {
  List<Cultivar> cultivars = [];  // More appropriate name
  Future<void> fetchCultivars() async {
    final response = await http.get('/api/v1/cultivars/');
    // All functionality preserved
  }
}
```

### 6. Templates (HTML)
```html
<!-- Before -->
<h1>Strain Management</h1>
<div class="strain-card">
  <h2>{{ strain.name }}</h2>
  <p>Strain Type: {{ strain.type }}</p>
  <a href="/strain/{{ strain.id }}">View Details</a>
</div>

<!-- After -->
<h1>Cultivar Management</h1>
<div class="cultivar-card">
  <h2>{{ cultivar.name }}</h2>
  <p>Cultivar Type: {{ cultivar.type }}</p>
  <a href="/cultivar/{{ cultivar.id }}">View Details</a>
</div>
```

### 7. JavaScript Functions
```javascript
// Before
function initStrainForm() {
    $.ajax({
        url: '/strains',
        type: 'POST',
        data: formData,
        success: function(response) {
            window.location.href = '/strain/' + response.strain_id;
        }
    });
}

// After
function initCultivarForm() {
    $.ajax({
        url: '/cultivars',
        type: 'POST',
        data: formData,
        success: function(response) {
            window.location.href = '/cultivar/' + response.cultivar_id;
        }
    });
}
```

## Migration Phases Completed

### ✅ Phase 1: Backend Models Migration
- `Strain` class renamed to `Cultivar` in Flask models
- `Strain = Cultivar` alias maintained for backward compatibility
- Foreign keys updated from `strain_id` to `cultivar_id`
- All model relationships updated

### ✅ Phase 2: API Layer Migration
- Pydantic schemas renamed: `StrainBase` → `CultivarBase`, etc.
- FastAPI routers mounted at both `/api/v1/cultivars/` and `/api/v1/strains/`
- Handler modules renamed: `strain_handlers.py` → `cultivar_handlers.py`
- Activity types updated: `strain_add` → `cultivar_add`

### ✅ Phase 3: Flutter Frontend Migration
- Provider consolidation (no duplicates found)
- Widget consolidation (no duplicates found)
- All Flutter imports updated to use cultivar terminology
- Models aligned with backend schema

### ✅ Phase 4: Templates and JavaScript Migration
- HTML templates renamed and updated
- JavaScript functions updated
- AJAX endpoints updated to use `/cultivars/`
- CSS classes updated

### ✅ Phase 5: Test Suite Migration
- Test files updated to use cultivar terminology
- Test data updated
- API endpoint tests updated
- Backward compatibility tests maintained

### ✅ Phase 6: Documentation Migration
- 36+ markdown files updated
- API documentation updated
- User guides updated
- Developer docs updated

### 🔄 Phase 7: Validation and Cleanup (In Progress)
- Comprehensive validation script
- Migration guides and documentation
- Final verification and cleanup

## Backward Compatibility Strategy

### Maintained Compatibility
1. **Model Aliases**: `Strain = Cultivar` throughout codebase
2. **Dual API Endpoints**: Both `/cultivars/` and `/strains/` work
3. **Database Compatibility**: Legacy queries still work with aliases
4. **Test Backward Compatibility**: Tests verify both old and new terminology

### Deprecation Timeline
- **Immediate**: All new code should use "cultivar"
- **Short-term** (3-6 months): Legacy aliases maintained
- **Long-term** (6-12 months): Legacy endpoints deprecated with warnings
- **Future**: Legacy terms may be removed after user notification

## Testing the Migration

### Backend Tests
```bash
# Run all tests to ensure no regressions
pytest tests/ -v

# Test specific functionality
pytest tests/integration/test_cultivars.py -v
pytest tests/integration/test_cultivars_integration.py -v
```

### API Testing
```bash
# Test new endpoints
curl -X GET http://localhost:8000/api/v1/cultivars/

# Test backward compatibility
curl -X GET http://localhost:8000/api/v1/strains/
```

### Frontend Testing
```bash
cd flutter_app
flutter test
flutter analyze
```

## Manual Verification Steps

### 1. Check API Endpoints
- [ ] `/api/v1/cultivars/` returns cultivar data
- [ ] `/api/v1/strains/` returns same data (backward compatibility)
- [ ] API documentation shows both endpoint sets

### 2. Check Database
- [ ] `Cultivar` class imports correctly
- [ ] `Strain` alias works for legacy code
- [ ] All queries execute without errors

### 3. Check Frontend
- [ ] Flutter app compiles without errors
- [ ] Provider functionality works
- [ ] UI displays "Cultivar" terminology

### 4. Check Templates
- [ ] HTML templates render correctly
- [ ] JavaScript functions execute properly
- [ ] No console errors in browser

### 5. Check Tests
- [ ] All tests pass
- [ ] Both old and new terminology tests work
- [ ] No test failures

## Common Issues and Solutions

### Issue 1: Import Errors
**Problem**: `ModuleNotFoundError: No module named 'strains'`
**Solution**: Update imports to use new module names
```python
# Before
from app.fastapi_app.models.strains import StrainBase

# After
from app.fastapi_app.models.cultivars import CultivarBase
```

### Issue 2: Template Rendering Errors
**Problem**: Template variables not found
**Solution**: Update template variables to use new names
```html
<!-- Before -->
{{ strain.name }}

<!-- After -->
{{ cultivar.name }}
```

### Issue 3: API Response Format
**Problem**: API returns different field names
**Solution**: Update frontend to handle both formats
```dart
// Handle both old and new field names
final name = cultivarData['name'] ?? cultivarData['strain_name'];
```

## Rollback Procedure

If issues are encountered, the migration can be rolled back:

1. **Database**: No changes required (backward compatible)
2. **Code**: Restore backup of modified files
3. **API**: Disable new endpoints, rely on legacy endpoints
4. **Frontend**: Revert to previous provider implementation

## Best Practices for Future Development

### Code Standards
- Always use "cultivar" in new code
- Use aliases when interfacing with legacy code
- Document any use of legacy terminology
- Include backward compatibility tests

### Testing Guidelines
- Test both new and legacy interfaces
- Verify backward compatibility periodically
- Include terminology validation in CI/CD
- Maintain comprehensive test coverage

### Documentation
- Update all documentation with correct terminology
- Include migration notes in future changes
- Maintain this guide as reference
- Train team members on new terminology

## Support and Contact

For questions about this migration:
- Review this migration guide
- Check validation script output
- Consult Task-Master-AI tasks for detailed implementation
- Contact the development team

## Changelog

**Version 1.0** (November 2025)
- Initial terminology migration guide
- Comprehensive backward compatibility strategy
- Complete migration documentation
- Validation and testing procedures

---

*This guide will be updated as the migration progresses and additional documentation is created.*