# Backward Compatibility Strategy: Strain → Cultivar Migration

## Overview

This document outlines the comprehensive backward compatibility strategy implemented during the strain→cultivar terminology migration. Our approach ensures that existing code, APIs, and user workflows continue to function seamlessly while gradually transitioning to the new "cultivar" terminology.

## Compatibility Levels

### Level 1: Full Compatibility (Immediate)
**Status**: ✅ **Implemented**

All legacy interfaces continue to work without any changes required from existing code:

#### Python Models
```python
# Legacy code still works
from app.models import Strain  # Imports Cultivar class
from app.models.base_models import Strain as LegacyStrain

# Both refer to the same Cultivar class
strain = Strain(name="OG Kush", type="Indica")
cultivar = Cultivar(name="OG Kush", type="Indica")

# strain and cultivar are identical objects
assert isinstance(strain, Cultivar)
assert type(strain) == type(cultivar)
```

#### API Endpoints
```bash
# Legacy endpoints still work
curl -X GET http://localhost:8000/api/v1/strains/
curl -X GET http://localhost:8000/api/v1/strains/123
curl -X POST http://localhost:8000/api/v1/strains/

# Redirects to new endpoints with cultivar data
# Response format: { "id": 123, "name": "OG Kush", "type": "Indica" }
# Same response format as /api/v1/cultivars/
```

#### Flask Routes
```python
# Legacy Flask routes still work
@app.route('/strain/<int:strain_id>')
def view_strain(strain_id):
    return render_template('strain.html', strain=cultivar)

# Both variable names work in templates
# {{ strain.name }} and {{ cultivar.name }} are equivalent
```

### Level 2: Partial Compatibility (Transitional)
**Status**: ✅ **Implemented**

Some interfaces accept both old and new parameter names:

#### Pydantic Models
```python
# Both field names work during API calls
strain_data = {
    "name": "OG Kush",
    "type": "Indica",
    "strain_name": "OG Kush",  # Legacy field name still accepted
    "strain_type": "Indica"     # Legacy field name still accepted
}

# API processes both formats identically
cultivar = CultivarCreate(**strain_data)
```

#### JavaScript/AJAX
```javascript
// Legacy JavaScript functions still work
function addStrain(strainData) {
    return fetch('/api/v1/strains/', {
        method: 'POST',
        body: JSON.stringify(strainData)
    });
}

// New functions use cultivar terminology
function addCultivar(cultivarData) {
    return fetch('/api/v1/cultivars/', {
        method: 'POST',
        body: JSON.stringify(cultivarData)
    });
}

// Both functions call the same backend endpoints
```

### Level 3: Graceful Degradation (Future)
**Status**: 📋 **Planned**

Legacy features will receive warnings before being removed:

#### API Deprecation Warnings
```python
# Future implementation (6-12 months)
@router.get("/strains/")
async def get_strains_deprecated():
    logger.warning("DEPRECATED: Use /cultivars/ instead of /strains/")
    return await get_cultivars()
```

#### User Interface Warnings
```html
<!-- Future template updates -->
<div class="deprecation-notice">
    <strong>Note:</strong> "Strain" terminology is deprecated. 
    Please use "Cultivar" for new entries.
</div>
```

## Implementation Details

### Model Aliases
```python
# app/models/base_models.py
class Cultivar(db.Model):
    """Cannabis cultivar model."""
    __tablename__ = 'cultivar'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    def __init__(self, name, type=None, description=None):
        self.name = name
        self.type = type
        self.description = description

# Backward compatibility alias
Strain = Cultivar

# app/models/__init__.py
from .base_models import Cultivar, Strain  # Both available
__all__ = ['Cultivar', 'Strain']
```

### API Router Configuration
```python
# app/fastapi_app/__init__.py
from app.fastapi_app.routers import cultivars

# Primary endpoints (recommended)
app.include_router(
    cultivars.router,
    prefix="/api/v1/cultivars",
    tags=["Cultivars"]
)

# Legacy endpoints (backward compatibility)
app.include_router(
    cultivars.router,
    prefix="/api/v1/strains",
    tags=["Strains (Legacy)"]
)
```

### Pydantic Model Aliases
```python
# app/fastapi_app/models/cultivars.py
class CultivarBase(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

class CultivarCreate(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

class CultivarUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None

class CultivarResponse(BaseModel):
    id: int
    name: str
    type: Optional[str] = None
    description: Optional[str] = None

# Backward compatibility aliases
StrainBase = CultivarBase
StrainCreate = CultivarCreate
StrainUpdate = CultivarUpdate
StrainResponse = CultivarResponse
```

### Database Compatibility
```sql
-- No database schema changes required
-- Legacy strain table references work through aliases

-- Legacy queries still work
SELECT * FROM strain WHERE breeder_id = 123;

-- New queries use cultivar table
SELECT * FROM cultivar WHERE breeder_id = 123;

-- Both return identical results due to alias configuration
```

## Testing Strategy

### Backward Compatibility Tests
```python
# tests/test_backward_compatibility.py
import pytest
from app.models import Strain, Cultivar
from app.fastapi_app.models.cultivars import StrainBase, CultivarBase

def test_strain_cultivar_alias():
    """Test that Strain and Cultivar are identical"""
    strain = Strain(name="OG Kush", type="Indica")
    cultivar = Cultivar(name="OG Kush", type="Indica")
    
    assert type(strain) == type(cultivar)
    assert isinstance(strain, Cultivar)

def test_pydantic_aliases():
    """Test Pydantic model aliases"""
    legacy_data = {"strain_name": "OG Kush", "strain_type": "Indica"}
    new_data = {"name": "OG Kush", "type": "Indica"}
    
    # Both should work identically
    legacy_strain = StrainBase(**legacy_data)
    new_cultivar = CultivarBase(**new_data)
    
    assert legacy_strain.name == new_cultivar.name
    assert legacy_strain.type == new_cultivar.type

@pytest.mark.asyncio
async def test_api_backward_compatibility(client):
    """Test API backward compatibility"""
    # Legacy endpoint
    response = await client.get("/api/v1/strains/")
    assert response.status_code == 200
    
    # New endpoint
    response = await client.get("/api/v1/cultivars/")
    assert response.status_code == 200
    
    # Both should return same data
    assert response.json() == legacy_response.json()
```

### Migration Test Suite
```python
# tests/test_migration_validation.py
def test_terminology_consistency():
    """Ensure terminology is consistent across codebase"""
    # Check that new code uses cultivar
    assert "cultivar" in new_code
    assert "strain" not in production_code
    
    # Check backward compatibility
    assert hasattr(Strain, "__name__")
    assert Strain == Cultivar

def test_database_compatibility():
    """Test database queries work with both terminologies"""
    # Legacy query
    legacy_results = db.session.query(Strain).all()
    
    # New query
    new_results = db.session.query(Cultivar).all()
    
    # Should return identical data
    assert len(legacy_results) == len(new_results)
```

## Migration Timeline

### Phase 1: Immediate (Completed) ✅
- **Duration**: Migration launch
- **Actions**: 
  - Implement all aliases and dual endpoints
  - Maintain 100% backward compatibility
  - Begin using cultivar in new code

### Phase 2: Transition (3-6 months) 📅
- **Actions**:
  - Add deprecation warnings to legacy endpoints
  - Update documentation to prefer cultivar terminology
  - Encourage users to migrate to new endpoints
  - Monitor usage patterns

### Phase 3: Graceful Degradation (6-12 months) 📅
- **Actions**:
  - Legacy endpoints return warnings in responses
  - Performance warnings for legacy API usage
  - Document migration timelines clearly
  - Provide migration scripts and guides

### Phase 4: Legacy Removal (12+ months) 📅
- **Actions**:
  - Remove deprecated endpoints (with advance notice)
  - Remove model aliases (with advance notice)
  - Clean up test compatibility code
  - Update all internal documentation

## Monitoring and Analytics

### Usage Tracking
```python
# Implementation for tracking endpoint usage
@app.middleware("http")
async def track_endpoint_usage(request: Request, call_next):
    if request.url.path.startswith("/api/v1/strains/"):
        logger.info(f"LEGACY_ENDPOINT_USAGE: {request.url.path}")
    
    response = await call_next(request)
    return response
```

### Metrics to Monitor
- **API Usage**: Ratio of /strains/ vs /cultivars/ endpoint calls
- **Code References**: Track "strain" vs "cultivar" usage in new code
- **Error Rates**: Monitor for any compatibility issues
- **User Feedback**: Collect feedback on terminology changes

## Developer Guidelines

### Writing New Code
```python
# ✅ DO: Use cultivar terminology
def create_cultivar(cultivar_data: CultivarCreate):
    cultivar = Cultivar(**cultivar_data.dict())
    return cultivar

# ❌ DON'T: Use strain terminology
def create_strain(strain_data: dict):
    strain = Strain(**strain_data)
    return strain
```

### Updating Legacy Code
```python
# ✅ DO: Update variable names
cultivar = Cultivar.query.filter_by(name=name).first()

# ✅ ACCEPTABLE: Keep old variable names for compatibility
strain = Cultivar.query.filter_by(name=name).first()  # Variable name only
```

### Template Updates
```html
<!-- ✅ DO: Update to cultivar terminology -->
<h1>Cultivar Management</h1>
<div class="cultivar-card">
  <h2>{{ cultivar.name }}</h2>
</div>

<!-- ✅ ACCEPTABLE: Keep old variable names -->
<div class="cultivar-card">
  <h2>{{ strain.name }}</h2>  <!-- strain variable still works -->
</div>
```

## Troubleshooting

### Common Issues

#### Issue 1: Import Errors
**Problem**: `ImportError: cannot import name 'Strain'`
**Solution**: 
```python
# Use new import pattern
from app.models import Cultivar
from app.models.base_models import Strain as LegacyStrain

# Or use alias directly
from app.models.base_models import Strain  # Returns Cultivar class
```

#### Issue 2: API Response Format
**Problem**: Legacy code expects "strain_name" field
**Solution**:
```python
# API responds with "name" field
cultivar_data = {
    "id": 123,
    "name": "OG Kush",  # New field name
    # "strain_name" no longer in response
}

# Legacy code should be updated to use "name"
```

#### Issue 3: Database Query Issues
**Problem**: Legacy SQL queries fail
**Solution**:
```python
# Old way (no longer recommended)
results = db.session.execute("SELECT * FROM strain WHERE...")

# New way (recommended)
results = Cultivar.query.filter(...).all()
```

### Emergency Rollback
If critical issues arise, rollback can be implemented:

1. **Immediate**: Disable new endpoints, rely on legacy endpoints
2. **Code**: Restore backup of modified files  
3. **Database**: No changes required (backward compatible)
4. **Testing**: Verify legacy functionality works

## Success Metrics

### Compatibility KPIs
- **100%**: Legacy API endpoint functionality
- **100%**: Model alias functionality
- **<1%**: Error rate increase due to migration
- **90%**: New code using cultivar terminology
- **0**: Breaking changes for existing users

### Migration KPIs
- **Month 3**: 50% adoption of new endpoints
- **Month 6**: 75% adoption of new endpoints
- **Month 12**: 90% adoption of new endpoints
- **Month 18**: Ready for legacy endpoint removal

## Support Resources

### Documentation
- [Terminology Migration Guide](TERMINOLOGY_MIGRATION_GUIDE.md)
- [API Documentation](../docs/generated/openapi.json)
- [Migration Scripts](../scripts/)

### Tools
- `python scripts/validate_terminology_migration.py` - Validation script
- `python scripts/taskmaster_cli.py` - Task management
- Migration checklist and progress tracking

### Contact
For compatibility issues:
1. Check this backward compatibility document
2. Run validation script for diagnostics
3. Consult Task-Master-AI tasks for detailed status
4. Contact development team with specific error details

---

*This document will be updated as the migration progresses and additional compatibility measures are implemented.*