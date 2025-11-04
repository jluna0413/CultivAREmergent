# Alembic Migration Framework for CultivAR Async Models

## Overview

This guide explains how to use the Alembic migration framework for managing database schema changes in the CultivAR application with async SQLAlchemy models.

## Current Setup

- **Configuration File**: `alembic.ini`
- **Environment Script**: `alembic/env.py`
- **Models Location**: `app/models_async/`
- **Migration Scripts**: `alembic/versions/`
- **Convenience Script**: `scripts/run_migrations.py`

## Database Support

The migration framework supports both:
- **SQLite** (development): `sqlite:///./cultivar.db`
- **PostgreSQL** (production): Use `DATABASE_URL` environment variable

## Basic Usage

### Using the Convenience Script

The easiest way to run migrations is using the provided Python script:

```bash
# Check current migration status
python scripts/run_migrations.py current

# Run all pending migrations
python scripts/run_migrations.py upgrade

# Upgrade to specific revision
python scripts/run_migrations.py upgrade --revision <revision_id>

# Downgrade to previous version
python scripts/run_migrations.py downgrade --revision -1

# Check for schema changes
python scripts/run_migrations.py check

# View migration history
python scripts/run_migrations.py history

# Create new migration
python scripts/run_migrations.py create --message "Description of changes"

# Use specific database
python scripts/run_migrations.py --database-url postgresql://user:pass@host/db upgrade
```

### Using Alembic Commands Directly

You can also use Alembic commands directly:

```bash
# Check current migration
alembic current

# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>

# Downgrade
alembic downgrade -1

# Create new migration
alembic revision --autogenerate -m "Your message"
```

## Environment Variables

- `DATABASE_URL`: Primary database URL (takes precedence)
- `ALEMBIC_DATABASE_URL`: Alternative database URL for Alembic

## Database URL Examples

```bash
# SQLite (default)
export DATABASE_URL="sqlite:///./cultivar.db"

# PostgreSQL
export DATABASE_URL="postgresql://username:password@localhost:5432/cultivar"

# PostgreSQL with async driver
export DATABASE_URL="postgresql+asyncpg://username:password@localhost:5432/cultivar"
```

## Migration Best Practices

### 1. Creating New Migrations

Always use `--autogenerate` to compare current models with database:

```bash
alembic revision --autogenerate -m "Add new user preferences"
```

### 2. Testing Migrations

Test migrations before applying to production:

```bash
# Test upgrade
alembic upgrade head

# Test downgrade
alembic downgrade -1

# Check for schema drift
alembic check
```

### 3. Production Deployment

For production environments:

```bash
# Always backup before migrations
# Run migrations during maintenance window
alembic upgrade head

# Verify application works
# Monitor for issues
```

## Current Schema

The baseline migration includes 24 tables covering:
- User management (`user`, `breeder`)
- Plant tracking (`plant`, `cultivar`, `status`, `zone`, `grow`)
- Sensor data (`sensor`, `sensor_data`, `stream`)
- Activities and analytics (`activity`, `plant_activity`, `activity_summary`)
- E-commerce (`product`, `order`, `order_item`)
- Content management (`blog_post`, `lead_magnet`, `lead_magnet_download`)
- Marketing (`waitlist`, `newsletter_subscriber`)
- System (`settings`, `extension`)
- Other (`measurement`, `plant_image`)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **Async Driver Warnings**: These are normal for migration operations
3. **Foreign Key Cycles**: SQLite may show warnings for complex relationships
4. **Missing Tables**: Run `alembic upgrade head` to apply migrations

### Getting Help

- Check current status: `alembic current`
- View history: `alembic history`
- Check for issues: `alembic check`
- Test connection: Run any migration command

## Integration with CI/CD

The migration framework is designed to work with automated deployment:

```bash
# In deployment script
python scripts/run_migrations.py check || exit 1
python scripts/run_migrations.py upgrade
```

## File Structure

```
alembic/
├── env.py              # Environment configuration
├── versions/           # Migration scripts
│   └── 2025_10_30_1855-3968dfa9e747_generate_baseline_schema_for_async_.py
├── script.py.mako      # Migration template
└── README             # Alembic documentation

scripts/
└── run_migrations.py  # Convenience wrapper script

app/models_async/
├── base.py            # SQLAlchemy base and metadata
└── [model files]      # Individual model definitions