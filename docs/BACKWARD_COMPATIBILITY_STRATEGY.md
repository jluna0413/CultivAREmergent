# Strain→Cultivar Migration: Backward Compatibility Strategy

## Overview

This document outlines the backward compatibility strategy implemented during the strain-to-cultivar terminology migration to ensure existing code continues to function while transitioning to the new terminology.

## Implementation Strategy

### 1. Class Aliases

**Location**: `app/models/base_models.py`

```python
# Primary class definition
class Cultivar(db.Model):
    __tablename__ = 'cultivar'
    # ... all class implementation ...

# Backward compatibility alias
Strain = Cultivar
```

**Purpose**: Existing code using `Strain` continues to work without modification.

### 2. Pydantic Model Compatibility

**Location**: `app/fastapi_app/models/cultivars.py`

```python
# Primary models
class CultivarBase(BaseModel):
    # ... implementation ...

# Backward compatibility aliases (optional, if needed)
StrainBase = CultivarBase
StrainCreate = CultivarCreate
StrainUpdate = CultivarUpdate
StrainResponse = CultivarResponse
```

### 3. Import Compatibility

**Location**: `app/models/__init__.py`

```python
# Export both names for compatibility
from .base_models import Cultivar, Strain

# Both names point to the same class
# Strain = Cultivar  # Already defined in base_models.py
```

### 4. API Endpoint Dual-Mounting

**Location**: `app/fastapi_app/__init__.py`

```python
# Mount both the new and legacy endpoints
app.include_router(cultivars_router, prefix="/api/v1/cultivars", tags=["cultivars"])
app.include_router(cultivars_router, prefix="/api/v1/strains", tags=["strains-legacy"])
```

**Note**: The legacy `/api/v1/strains/*` endpoints are deprecated and will be removed in a future version.

### 5. Activity Type Compatibility

**Location**: `app/handlers/activity_handlers.py`

```python
# Both old and new activity types are logged for compatibility
activity_type = "cultivar_add"  # New standard
legacy_activity_type = "strain_add"  # For backward compatibility

# Both can be used in the same system
```

### 6. Database Schema Compatibility

The database schema remains unchanged. The `cultivar` table and columns (`cultivar_id`, `cultivar_name`, etc.) were already in place. No migration scripts are required.

## Migration Guide for Developers

### For Python Code

**Before (Legacy)**:
```python
from app.models import Strain

class Plant:
    def __init__(self, strain: Strain):
        self.strain = strain
        self.strain_name = strain.name
```

**After (Recommended)**:
```python
from app.models import Cultivar

class Plant:
    def __init__(self, cultivar: Cultivar):
        self.cultivar = cultivar
        self.cultivar_name = cultivar.name
```

**Still Compatible** (during transition):
```python
from app.models import Strain  # Points to Cultivar

class Plant:
    def __init__(self, strain: Strain):
        self.cultivar = strain  # Compatible assignment
        self.cultivar_name = strain.name
```

### For API Integration

**Legacy Endpoints** (still working):
```bash
GET /api/v1/strains/
POST /api/v1/strains/
GET /api/v1/strains/{id}
```

**Recommended New Endpoints**:
```bash
GET /api/v1/cultivars/
POST /api/v1/cultivars/
GET /api/v1/cultivars/{id}
```

## Validation and Testing

Run the validation script to check compliance:

```bash
python scripts/validate_terminology_migration.py --strict
```

This will identify any remaining legacy references that need attention.