# Database Migration Workflow Guide

## Overview

This document describes the Alembic database migration workflow for the CultivAR project using `app.models_async.*` modules.

## Migration Setup

### Initial Configuration

**Alembic Configuration Files:**
- `alembic.ini` - Main configuration file with database URL and logging settings
- `alembic/env.py` - Environment configuration for async models
- `alembic/versions/` - Migration scripts directory

### Database URL Configuration

The database URL is configured in `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///./cultivar_async.db
```

**Note:** For production, update this to use your production database URL.

## Migration Commands

### Generate New Migration
```bash
# Create new migration with automatic table detection
alembic revision --autogenerate -m "Description of changes"

# Create empty migration (manual coding)
alembic revision -m "Description of changes"
```

### Apply Migrations
```bash
# Upgrade to latest migration
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade to previous migration
alembic downgrade -1

# Show current migration version
alembic current

# Show migration history
alembic history
```

### Development Workflow

1. **Make Model Changes**: Modify `app.models_async/*.py` files
2. **Generate Migration**: Use `alembic revision --autogenerate`
3. **Review Migration**: Check generated script in `alembic/versions/`
4. **Apply Migration**: Run `alembic upgrade head`
5. **Test Changes**: Verify database schema and application functionality

## Important Notes

### Async Models Support
- Alembic runs migrations synchronously even for async models
- The `env.py` is configured to work with `app.models_async.*` modules
- Async driver warnings are expected when using SQLite with async models

### Migration Best Practices
- **Additive Changes Only**: Only add tables/columns, don't remove in production
- **Idempotent Migrations**: Migrations should be safe to run multiple times
- **Backup First**: Always backup database before major migrations
- **Test Migrations**: Test migrations on staging environment first

### Common Issues

**Async Driver Warnings**: These are normal for SQLite and don't affect functionality.

**Import Errors**: If you see import errors, check that:
- All model modules are in `app.models_async.*`
- The `env.py` path configuration is correct
- Python path includes the project root directory

### Production Deployment

Include migration commands in deployment checklist:
1. Run `alembic upgrade head` after code deployment
2. Verify migration success with `alembic current`
3. Check application health after migration

## File Structure
```
alembic/
├── alembic.ini           # Configuration
├── env.py               # Environment setup
├── versions/            # Migration scripts
│   └── 2025_10_30_1259-80e76a32dc4f_initial_migration_for_async_models.py
└── script.py.mako       # Migration template
```

## Model Modules Coverage
- `app.models_async.auth` - User authentication models
- `app.models_async.grow` - Plant growing models  
- `app.models_async.sensors` - Sensor data models
- `app.models_async.settings` - Application settings models
- `app.models_async.commerce` - E-commerce models
- `app.models_async.marketing` - Marketing models
