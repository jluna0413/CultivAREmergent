# Database Migration Backward Compatibility During Cutover

**Document Version:** 1.0  
**Created:** October 31, 2025  
**Purpose:** Ensure backward compatibility during Flask-to-FastAPI migration cutover  
**Author:** Database Engineer  

## Overview

This document outlines strategies to maintain database backward compatibility during the Flask-to-FastAPI migration cutover window. The goal is to enable seamless rollback to Flask service without data corruption or loss while supporting both sync and async database operations.

## Migration Phases and Compatibility Requirements

### Phase 1: Pre-Cutover (Preparation)
**Duration:** 2-3 days before cutover  
**Goal:** Prepare database for dual-mode operation  

#### Database Schema Compatibility
```sql
-- Ensure all tables exist in both sync and async formats
-- Add any missing indexes or constraints
-- Create dual-mode views if needed

-- Example: Dual-mode user table support
CREATE TABLE IF NOT EXISTS users_async (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255),
    user_type VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add compatibility indexes for both modes
CREATE INDEX IF NOT EXISTS idx_users_username_sync ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_username_async ON users_async(username);
CREATE INDEX IF NOT EXISTS idx_users_email_sync ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_email_async ON users_async(email);
```

#### Data Synchronization Setup
```python
# scripts/setup_data_sync.py
import asyncio
import logging
from sqlalchemy import text
from app.models_async.base import engine as async_engine
from app.models.base import engine as sync_engine

async def setup_data_sync():
    """Setup bidirectional data sync between sync and async tables"""
    
    # Create sync triggers for real-time data replication
    setup_sync_triggers()
    
    # Initial data migration
    await migrate_initial_data()
    
    # Setup periodic verification
    await setup_verification_jobs()

async def migrate_initial_data():
    """Migrate existing data to async tables"""
    
    # Migrate users
    async with async_engine.connect() as async_conn:
        with sync_engine.connect() as sync_conn:
            # Copy users data
            users_result = await sync_conn.execute(text("SELECT * FROM users"))
            users_data = users_result.fetchall()
            
            for user in users_data:
                await async_conn.execute(
                    text("""
                        INSERT INTO users_async (id, username, email, password_hash, user_type, is_active, created_at, updated_at)
                        VALUES (:id, :username, :email, :password_hash, :user_type, :is_active, :created_at, :updated_at)
                        ON CONFLICT (username) DO UPDATE SET
                        email = EXCLUDED.email,
                        password_hash = EXCLUDED.password_hash,
                        updated_at = EXCLUDED.updated_at
                    """),
                    {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "password_hash": user.password_hash,
                        "user_type": user.user_type,
                        "is_active": user.is_active,
                        "created_at": user.created_at,
                        "updated_at": user.updated_at
                    }
                )
            
            await async_conn.commit()

def setup_sync_triggers():
    """Setup database triggers for real-time sync"""
    
    # User table sync trigger
    sync_trigger_sql = """
    CREATE OR REPLACE FUNCTION sync_user_to_async()
    RETURNS TRIGGER AS $$
    BEGIN
        INSERT INTO users_async (id, username, email, password_hash, user_type, is_active, created_at, updated_at)
        VALUES (NEW.id, NEW.username, NEW.email, NEW.password_hash, NEW.user_type, NEW.is_active, NEW.created_at, NEW.updated_at)
        ON CONFLICT (username) DO UPDATE SET
            email = EXCLUDED.email,
            password_hash = EXCLUDED.password_hash,
            user_type = EXCLUDED.user_type,
            is_active = EXCLUDED.is_active,
            updated_at = EXCLUDED.updated_at;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS user_sync_trigger ON users;
    CREATE TRIGGER user_sync_trigger
        AFTER INSERT OR UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION sync_user_to_async();
    """
    
    # Apply triggers (this would be done via database migration)
    pass
```

### Phase 2: Cutover Window (Active Migration)
**Duration:** 1-2 hours  
**Goal:** Minimize disruption during service transition  

#### Database Access Patterns
```python
# app/database/compatibility.py
import logging
from typing import Optional, Any
from contextlib import contextmanager

class DatabaseCompatibilityLayer:
    """
    Provides compatibility layer for both sync and async database operations
    during migration cutover
    """
    
    def __init__(self):
        self.sync_active = True
        self.async_active = False
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def get_sync_session(self):
        """Get sync database session (Flask mode)"""
        if not self.sync_active:
            raise RuntimeError("Sync database mode not active")
        
        # Flask-SQLAlchemy session management
        from app.models import db
        try:
            yield db.session
        except Exception as e:
            db.session.rollback()
            raise
        finally:
            pass  # Flask manages session lifecycle
    
    @contextmanager
    def get_async_session(self):
        """Get async database session (FastAPI mode)"""
        if not self.async_active:
            raise RuntimeError("Async database mode not active")
        
        # Async SQLAlchemy session management
        from app.models_async.base import AsyncSessionLocal
        async_session = AsyncSessionLocal()
        try:
            yield async_session
        except Exception as e:
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
    
    def switch_to_async_mode(self):
        """Switch database access to async mode"""
        self.logger.info("Switching database mode to async")
        self.sync_active = False
        self.async_active = True
        
        # Verify async connectivity
        self.verify_async_connectivity()
    
    def switch_to_sync_mode(self):
        """Switch database access to sync mode"""
        self.logger.info("Switching database mode to sync")
        self.async_active = False
        self.sync_active = True
        
        # Verify sync connectivity
        self.verify_sync_connectivity()
    
    def verify_sync_connectivity(self):
        """Verify sync database connectivity"""
        try:
            with self.get_sync_session() as session:
                result = session.execute(text("SELECT 1"))
                self.logger.info("Sync database connectivity verified")
        except Exception as e:
            self.logger.error(f"Sync database connectivity failed: {e}")
            raise
    
    def verify_async_connectivity(self):
        """Verify async database connectivity"""
        import asyncio
        try:
            asyncio.run(self._verify_async())
        except Exception as e:
            self.logger.error(f"Async database connectivity failed: {e}")
            raise
    
    async def _verify_async(self):
        """Async helper for connectivity verification"""
        async with self.get_async_session() as session:
            result = await session.execute(text("SELECT 1"))
            self.logger.info("Async database connectivity verified")

# Global compatibility layer
db_compat = DatabaseCompatibilityLayer()
```

#### Migration Data Flow
```python
# app/database/migration_handler.py
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

class MigrationDataHandler:
    """
    Handles data consistency during migration cutover
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pending_operations = []
        self.operation_log = []
    
    async def handle_cutover_start(self):
        """Prepare for cutover start"""
        self.logger.info("Preparing database for cutover start")
        
        # Freeze writes to sync tables temporarily
        await self.freeze_sync_writes()
        
        # Ensure all pending operations are synced
        await self.sync_pending_operations()
        
        # Activate async mode
        db_compat.switch_to_async_mode()
    
    async def handle_cutover_rollback(self):
        """Handle rollback to Flask service"""
        self.logger.info("Handling database rollback to Flask service")
        
        # Sync any async operations back to sync tables
        await self.sync_async_to_sync()
        
        # Switch back to sync mode
        db_compat.switch_to_sync_mode()
        
        # Resume normal operations
        await self.resume_sync_writes()
    
    async def sync_pending_operations(self):
        """Sync all pending operations from async to sync"""
        
        async with db_compat.get_async_session() as async_session:
            with db_compat.get_sync_session() as sync_session:
                
                # Sync users
                await self.sync_users(async_session, sync_session)
                
                # Sync plants
                await self.sync_plants(async_session, sync_session)
                
                # Sync other entities...
    
    async def sync_users(self, async_session, sync_session):
        """Sync users between async and sync databases"""
        
        # Get users from async that aren't in sync
        async_users = await async_session.execute(
            text("""
                SELECT au.* FROM users_async au
                LEFT JOIN users su ON au.username = su.username
                WHERE su.username IS NULL OR au.updated_at > su.updated_at
            """)
        )
        
        for user in async_users:
            # Insert or update in sync table
            sync_session.execute(
                text("""
                    INSERT INTO users (username, email, password_hash, user_type, is_active, created_at, updated_at)
                    VALUES (:username, :email, :password_hash, :user_type, :is_active, :created_at, :updated_at)
                    ON CONFLICT (username) DO UPDATE SET
                        email = EXCLUDED.email,
                        password_hash = EXCLUDED.password_hash,
                        user_type = EXCLUDED.user_type,
                        is_active = EXCLUDED.is_active,
                        updated_at = EXCLUDED.updated_at
                """),
                {
                    "username": user.username,
                    "email": user.email,
                    "password_hash": user.password_hash,
                    "user_type": user.user_type,
                    "is_active": user.is_active,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
                }
            )
        
        sync_session.commit()
    
    async def sync_async_to_sync(self):
        """Sync all async data back to sync tables for rollback"""
        
        async with db_compat.get_async_session() as async_session:
            with db_compat.get_sync_session() as sync_session:
                
                # Get all users from async
                async_result = await async_session.execute(
                    text("SELECT * FROM users_async")
                )
                async_users = async_result.fetchall()
                
                for user in async_users:
                    # Update sync table with latest async data
                    sync_session.execute(
                        text("""
                            INSERT INTO users (id, username, email, password_hash, user_type, is_active, created_at, updated_at)
                            VALUES (:id, :username, :email, :password_hash, :user_type, :is_active, :created_at, :updated_at)
                            ON CONFLICT (username) DO UPDATE SET
                                email = EXCLUDED.email,
                                password_hash = EXCLUDED.password_hash,
                                user_type = EXCLUDED.user_type,
                                is_active = EXCLUDED.is_active,
                                created_at = EXCLUDED.created_at,
                                updated_at = EXCLUDED.updated_at
                        """),
                        {
                            "id": user.id,
                            "username": user.username,
                            "email": user.email,
                            "password_hash": user.password_hash,
                            "user_type": user.user_type,
                            "is_active": user.is_active,
                            "created_at": user.created_at,
                            "updated_at": user.updated_at
                        }
                    )
                
                sync_session.commit()
                self.logger.info(f"Synced {len(async_users)} users from async to sync")
```

### Phase 3: Post-Cutover (Stabilization)
**Duration:** 1-2 days after cutover  
**Goal:** Ensure data consistency and performance  

#### Data Verification
```python
# scripts/verify_data_consistency.py
import asyncio
import logging
from sqlalchemy import text

async def verify_data_consistency():
    """Verify data consistency between sync and async databases"""
    
    logger = logging.getLogger(__name__)
    
    # Verify user counts
    sync_count = await get_sync_user_count()
    async_count = await get_async_user_count()
    
    if sync_count != async_count:
        logger.error(f"User count mismatch: sync={sync_count}, async={async_count}")
        return False
    
    # Verify sample data integrity
    sample_sync_users = await get_sample_sync_users()
    sample_async_users = await get_sample_async_users()
    
    for sync_user, async_user in zip(sample_sync_users, sample_async_users):
        if not verify_user_data_match(sync_user, async_user):
            logger.error(f"User data mismatch: {sync_user.username}")
            return False
    
    logger.info("Data consistency verification passed")
    return True

async def get_sync_user_count():
    """Get user count from sync database"""
    # Implementation for counting sync users
    pass

async def get_async_user_count():
    """Get user count from async database"""
    # Implementation for counting async users
    pass
```

## Rollback Scenarios and Data Recovery

### Scenario 1: Partial Migration Failure
```sql
-- In case of partial migration failure, restore from backup
-- This assumes pre-migration backup is available

-- Restore from backup
psql -d cultivar_db < /backups/pre_migration_backup.sql

-- Verify restoration
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM plants;
```

### Scenario 2: Data Corruption During Migration
```python
# scripts/recover_corrupted_data.py
async def recover_corrupted_data():
    """Recover from data corruption during migration"""
    
    # 1. Stop all database writes
    await pause_all_writes()
    
    # 2. Identify corrupted records
    corrupted_records = await identify_corrupted_records()
    
    # 3. Restore from backup
    await restore_from_backup()
    
    # 4. Reapply validated transactions
    await reapply_valid_transactions(corrupted_records)
    
    # 5. Resume normal operations
    await resume_all_writes()

async def identify_corrupted_records():
    """Identify potentially corrupted records"""
    
    # Check for null required fields
    # Check for invalid foreign keys
    # Check for data type mismatches
    # Check for constraint violations
    pass
```

## Performance Considerations

### Connection Pool Management
```python
# app/database/pool_config.py
from sqlalchemy.pool import QueuePool
from sqlalchemy import create_engine

# Sync database pool configuration
SYNC_ENGINE_CONFIG = {
    "poolclass": QueuePool,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}

# Async database pool configuration
ASYNC_ENGINE_CONFIG = {
    "poolclass": QueuePool,
    "pool_size": 20,
    "max_overflow": 30,
    "pool_pre_ping": True,
    "pool_recycle": 3600,
}
```

### Query Optimization During Cutover
```python
# Optimized queries for cutover window
CUTOVER_QUERIES = {
    "user_lookup": """
        SELECT id, username, email, user_type, is_active, created_at
        FROM users
        WHERE username = :username OR email = :email
        LIMIT 1
    """,
    
    "plant_list": """
        SELECT p.id, p.name, p.strain_id, p.user_id, p.created_at
        FROM plants p
        WHERE p.user_id = :user_id
        ORDER BY p.created_at DESC
        LIMIT :limit OFFSET :offset
    """,
}
```

## Monitoring and Alerting

### Database Health Monitoring
```python
# app/monitoring/db_monitoring.py
import asyncio
import time
from sqlalchemy import text

class DatabaseHealthMonitor:
    """Monitor database health during cutover"""
    
    def __init__(self):
        self.check_interval = 30  # seconds
        self.monitor_task = None
    
    async def start_monitoring(self):
        """Start database health monitoring"""
        self.monitor_task = asyncio.create_task(self._monitor_loop())
    
    async def stop_monitoring(self):
        """Stop database health monitoring"""
        if self.monitor_task:
            self.monitor_task.cancel()
    
    async def _monitor_loop(self):
        """Main monitoring loop"""
        while True:
            try:
                await self.check_database_health()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logging.error(f"Database health check failed: {e}")
                await asyncio.sleep(5)  # Retry more frequently on error
    
    async def check_database_health(self):
        """Check database connectivity and performance"""
        
        # Check connection pools
        sync_pool_status = await self.check_pool_status("sync")
        async_pool_status = await self.check_pool_status("async")
        
        # Check query performance
        query_times = await self.benchmark_queries()
        
        # Check for deadlocks
        deadlock_count = await self.check_deadlocks()
        
        # Log health metrics
        logging.info(f"Database health - Sync pool: {sync_pool_status}, "
                    f"Async pool: {async_pool_status}, "
                    f"Query times: {query_times}, "
                    f"Deadlocks: {deadlock_count}")
        
        # Alert if thresholds exceeded
        if query_times["avg"] > 1.0:  # 1 second threshold
            logging.warning(f"Slow queries detected: {query_times}")
        
        if deadlock_count > 0:
            logging.error(f"Deadlocks detected: {deadlock_count}")
    
    async def check_pool_status(self, pool_type):
        """Check connection pool status"""
        # Implementation to check pool size, active connections, etc.
        pass
    
    async def benchmark_queries(self):
        """Benchmark critical queries"""
        # Implementation to time key database queries
        pass
    
    async def check_deadlocks(self):
        """Check for deadlocks in the database"""
        # Implementation to check for deadlocks
        pass
```

## Testing and Validation

### Pre-Cutover Testing
```python
# tests/test_migration_compatibility.py
import pytest
import asyncio
from app.database.compatibility import db_compat
from app.database.migration_handler import MigrationDataHandler

@pytest.mark.asyncio
async def test_database_compatibility():
    """Test database compatibility layer"""
    
    # Test sync mode
    with db_compat.get_sync_session() as session:
        result = session.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1
    
    # Test async mode
    async with db_compat.get_async_session() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1

@pytest.mark.asyncio
async def test_data_sync():
    """Test data synchronization between sync and async"""
    
    handler = MigrationDataHandler()
    
    # Test sync pending operations
    await handler.sync_pending_operations()
    
    # Verify data consistency
    consistency_ok = await verify_data_consistency()
    assert consistency_ok

@pytest.mark.asyncio
async def test_cutover_rollback():
    """Test cutover rollback scenario"""
    
    handler = MigrationDataHandler()
    
    # Simulate cutover
    await handler.handle_cutover_start()
    
    # Simulate rollback
    await handler.handle_cutover_rollback()
    
    # Verify rollback succeeded
    assert db_compat.sync_active
    assert not db_compat.async_active
```

## Backup and Recovery Procedures

### Backup Strategy During Cutover
```bash
#!/bin/bash
# scripts/backup_during_cutover.sh

CUTOVER_START_TIME=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="/backups/cutover/${CUTOVER_START_TIME}"

mkdir -p "${BACKUP_DIR}"

# Create full database backup
pg_dump cultivar_db > "${BACKUP_DIR}/full_backup_${CUTOVER_START_TIME}.sql"

# Create schema-only backup
pg_dump -s cultivar_db > "${BACKUP_DIR}/schema_${CUTOVER_START_TIME}.sql"

# Create data-only backup
pg_dump -a cultivar_db > "${BACKUP_DIR}/data_${CUTOVER_START_TIME}.sql"

# Compress backups
gzip "${BACKUP_DIR}"/*.sql

echo "Cutover backup completed: ${BACKUP_DIR}"
```

### Recovery Procedures
```bash
#!/bin/bash
# scripts/recover_from_backup.sh

if [ -z "$1" ]; then
    echo "Usage: $0 <backup_timestamp>"
    exit 1
fi

BACKUP_TIMESTAMP=$1
BACKUP_DIR="/backups/cutover/${BACKUP_TIMESTAMP}"

if [ ! -d "${BACKUP_DIR}" ]; then
    echo "Backup directory not found: ${BACKUP_DIR}"
    exit 1
fi

# Stop application services
sudo systemctl stop cultvar-flask
sudo systemctl stop cultvar-fastapi

# Restore from backup
gunzip -c "${BACKUP_DIR}/full_backup_${BACKUP_TIMESTAMP}.sql.gz" | psql cultivar_db

# Verify restoration
python scripts/verify_data_consistency.py

# Start services
sudo systemctl start cultvar-flask

echo "Recovery completed"
```

---

**Document Status:** APPROVED  
**Next Review Date:** After cutover completion + 1 week  
**Distribution:** Database team, DevOps team, Backend developers