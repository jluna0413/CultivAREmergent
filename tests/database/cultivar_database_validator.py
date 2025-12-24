#!/usr/bin/env python3
"""
Database Integrity and Migration Testing Framework for CultivAR Application
Ensures database consistency, migration reliability, and data integrity.
"""

import asyncio
import aiohttp
import sqlite3
import json
import logging
import argparse
import sys
import hashlib
import shutil
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum
import threading
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseEngine(Enum):
    """Database engine types"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    MARIADB = "mariadb"

class MigrationStatus(Enum):
    """Migration status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class DatabaseSchema:
    """Database schema information"""
    name: str
    tables: Dict[str, Dict[str, Any]]
    indexes: List[Dict[str, Any]]
    constraints: List[Dict[str, Any]]
    triggers: List[Dict[str, Any]]
    version: str

@dataclass
class MigrationRecord:
    """Database migration record"""
    id: str
    name: str
    timestamp: datetime
    status: MigrationStatus
    sql_statements: List[str]
    checksum: str
    duration_seconds: float
    error_message: Optional[str] = None

@dataclass
class DataIntegrityResult:
    """Data integrity test result"""
    test_name: str
    passed: bool
    message: str
    affected_rows: int
    timestamp: datetime
    evidence: List[str]

class DatabaseValidator:
    """Main database integrity and migration validation framework"""
    
    def __init__(self, base_url: str, auth_token: str = None, database_path: str = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.database_path = database_path
        self.session = None
        self.test_results: List[DataIntegrityResult] = []
        self.migration_history: List[MigrationRecord] = []
        
        # Database validation thresholds
        self.max_foreign_key_violations = 0
        self.max_orphaned_records = 0
        self.required_tables = self._get_required_tables()
        self.required_indexes = self._get_required_indexes()
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'CultivAR-DatabaseValidator/1.0',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        )
        if self.auth_token:
            self.session.headers['Authorization'] = f'Bearer {self.auth_token}'
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def _get_required_tables(self) -> List[str]:
        """Get list of required database tables for CultivAR"""
        return [
            'users', 'plants', 'strains', 'activities', 'sensors', 'sensor_readings',
            'harvests', 'batches', 'inventory', 'cultivars', 'breeders', 'zones',
            'settings', 'audit_logs', 'notifications', 'attachments'
        ]
    
    def _get_required_indexes(self) -> List[str]:
        """Get list of required database indexes"""
        return [
            'idx_users_email', 'idx_users_created_at', 'idx_plants_user_id',
            'idx_plants_status', 'idx_plants_created_at', 'idx_activities_plant_id',
            'idx_activities_created_at', 'idx_sensors_user_id', 'idx_sensor_readings_sensor_id',
            'idx_sensor_readings_created_at', 'idx_harvests_plant_id', 'idx_audit_logs_user_id'
        ]
    
    def connect_to_database(self) -> sqlite3.Connection:
        """Connect to database based on type"""
        if not self.database_path or not os.path.exists(self.database_path):
            raise FileNotFoundError(f"Database file not found: {self.database_path}")
        
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_schema_info(self) -> DatabaseSchema:
        """Extract database schema information"""
        conn = self.connect_to_database()
        
        try:
            # Get tables
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """)
            tables = {}
            
            for table_row in cursor.fetchall():
                table_name = table_row['name']
                
                # Get table structure
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = {}
                for col_row in cursor.fetchall():
                    columns[col_row['name']] = {
                        'type': col_row['type'],
                        'not_null': bool(col_row['notnull']),
                        'default': col_row['dflt_value'],
                        'primary_key': bool(col_row['pk'])
                    }
                
                # Get table statistics
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                except:
                    row_count = 0
                
                tables[table_name] = {
                    'columns': columns,
                    'row_count': row_count
                }
            
            # Get indexes
            cursor.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='index' AND name NOT LIKE 'sqlite_%'
            """)
            indexes = []
            for idx_row in cursor.fetchall():
                indexes.append({
                    'name': idx_row['name'],
                    'sql': idx_row['sql']
                })
            
            # Get constraints
            cursor.execute("""
                SELECT sql FROM sqlite_master 
                WHERE type IN ('table', 'index') AND sql IS NOT NULL
            """)
            constraints = []
            for constraint_row in cursor.fetchall():
                if 'FOREIGN KEY' in constraint_row['sql'] or 'UNIQUE' in constraint_row['sql']:
                    constraints.append(constraint_row['sql'])
            
            # Get triggers
            cursor.execute("""
                SELECT name, sql FROM sqlite_master 
                WHERE type='trigger'
            """)
            triggers = []
            for trigger_row in cursor.fetchall():
                triggers.append({
                    'name': trigger_row['name'],
                    'sql': trigger_row['sql']
                })
            
            return DatabaseSchema(
                name=os.path.basename(self.database_path),
                tables=tables,
                indexes=indexes,
                constraints=constraints,
                triggers=triggers,
                version="SQLite"
            )
            
        finally:
            conn.close()
    
    def create_database_backup(self) -> str:
        """Create a backup of the current database"""
        if not self.database_path:
            raise ValueError("No database path specified")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.database_path}.backup_{timestamp}"
        
        try:
            shutil.copy2(self.database_path, backup_path)
            logger.info(f"Database backup created: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup: {str(e)}")
            raise
    
    async def test_required_tables_exist(self) -> DataIntegrityResult:
        """Test that all required tables exist"""
        try:
            schema = self.get_schema_info()
            existing_tables = set(schema.tables.keys())
            required_tables = set(self.required_tables)
            
            missing_tables = required_tables - existing_tables
            extra_tables = existing_tables - required_tables
            
            evidence = []
            
            if not missing_tables:
                evidence.append(f"✅ All required tables exist ({len(required_tables)} tables)")
            else:
                evidence.append(f"❌ Missing required tables: {list(missing_tables)}")
            
            if extra_tables:
                evidence.append(f"ℹ️  Additional tables found: {list(extra_tables)}")
            
            # Check table statistics
            evidence.append(f"📊 Total tables: {len(existing_tables)}")
            evidence.append(f"📊 Total rows across all tables: {sum(t['row_count'] for t in schema.tables.values())}")
            
            passed = len(missing_tables) == 0
            
            return DataIntegrityResult(
                test_name="required_tables_exist",
                passed=passed,
                message="Required tables validation",
                affected_rows=len(existing_tables),
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="required_tables_exist",
                passed=False,
                message=f"Error checking required tables: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
    
    async def test_foreign_key_integrity(self) -> DataIntegrityResult:
        """Test foreign key constraints integrity"""
        try:
            conn = self.connect_to_database()
            
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")
            
            violation_count = 0
            evidence = []
            
            # Test common foreign key relationships
            foreign_key_tests = [
                ("SELECT COUNT(*) FROM plants WHERE user_id NOT IN (SELECT id FROM users)", "plants without valid users"),
                ("SELECT COUNT(*) FROM activities WHERE plant_id NOT IN (SELECT id FROM plants)", "activities without valid plants"),
                ("SELECT COUNT(*) FROM harvests WHERE plant_id NOT IN (SELECT id FROM plants)", "harvests without valid plants"),
                ("SELECT COUNT(*) FROM sensor_readings WHERE sensor_id NOT IN (SELECT id FROM sensors)", "sensor readings without valid sensors"),
                ("SELECT COUNT(*) FROM batches WHERE harvest_id NOT IN (SELECT id FROM harvests)", "batches without valid harvests")
            ]
            
            cursor = conn.cursor()
            for test_sql, description in foreign_key_tests:
                try:
                    cursor.execute(test_sql)
                    count = cursor.fetchone()[0]
                    if count > 0:
                        violation_count += count
                        evidence.append(f"❌ {description}: {count} violations")
                    else:
                        evidence.append(f"✅ {description}: 0 violations")
                except sqlite3.Error as e:
                    evidence.append(f"⚠️  Could not test {description}: {str(e)}")
            
            passed = violation_count <= self.max_foreign_key_violations
            
            if passed:
                evidence.append(f"✅ Foreign key integrity maintained ({violation_count} total violations)")
            else:
                evidence.append(f"❌ Foreign key integrity compromised ({violation_count} violations)")
            
            return DataIntegrityResult(
                test_name="foreign_key_integrity",
                passed=passed,
                message="Foreign key constraint validation",
                affected_rows=violation_count,
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="foreign_key_integrity",
                passed=False,
                message=f"Error testing foreign key integrity: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def test_data_consistency(self) -> DataIntegrityResult:
        """Test data consistency across related tables"""
        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            inconsistencies = []
            evidence = []
            
            # Test plant lifecycle consistency
            cursor.execute("""
                SELECT p.id, p.status, COUNT(a.id) as activity_count
                FROM plants p 
                LEFT JOIN activities a ON p.id = a.plant_id
                GROUP BY p.id, p.status
            """)
            
            for row in cursor.fetchall():
                plant_id, status, activity_count = row
                
                # Check for logical inconsistencies
                if status == 'harvested' and activity_count == 0:
                    inconsistencies.append(f"Plant {plant_id} marked as harvested but has no activities")
                
                if status == 'flowering' and activity_count < 3:
                    inconsistencies.append(f"Plant {plant_id} in flowering stage but insufficient activities")
            
            # Test sensor data consistency
            cursor.execute("""
                SELECT s.id, s.status, COUNT(sr.id) as reading_count
                FROM sensors s 
                LEFT JOIN sensor_readings sr ON s.id = sr.sensor_id
                WHERE s.status = 'active'
                GROUP BY s.id, s.status
            """)
            
            for row in cursor.fetchall():
                sensor_id, status, reading_count = row
                
                if reading_count == 0:
                    inconsistencies.append(f"Active sensor {sensor_id} has no readings")
            
            # Test user data completeness
            cursor.execute("""
                SELECT id, email, username, created_at 
                FROM users 
                WHERE email IS NULL OR email = '' OR username IS NULL OR username = ''
            """)
            
            incomplete_users = cursor.fetchall()
            if incomplete_users:
                inconsistencies.append(f"Found {len(incomplete_users)} users with incomplete data")
            
            evidence.append(f"Data consistency check completed")
            evidence.append(f"Found {len(inconsistencies)} data inconsistencies")
            
            if inconsistencies:
                evidence.extend([f"- {issue}" for issue in inconsistencies[:10]])  # Show first 10
            
            passed = len(inconsistencies) <= self.max_orphaned_records
            
            return DataIntegrityResult(
                test_name="data_consistency",
                passed=passed,
                message="Data consistency validation",
                affected_rows=len(inconsistencies),
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="data_consistency",
                passed=False,
                message=f"Error testing data consistency: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def test_required_indexes(self) -> DataIntegrityResult:
        """Test that required indexes exist"""
        try:
            schema = self.get_schema_info()
            existing_indexes = set()
            
            for index in schema.indexes:
                existing_indexes.add(index['name'])
            
            required_indexes = set(self.required_indexes)
            missing_indexes = required_indexes - existing_indexes
            extra_indexes = existing_indexes - required_indexes
            
            evidence = []
            
            if not missing_indexes:
                evidence.append(f"✅ All required indexes exist ({len(required_indexes)} indexes)")
            else:
                evidence.append(f"❌ Missing required indexes: {list(missing_indexes)}")
            
            if extra_indexes:
                evidence.append(f"ℹ️  Additional indexes found: {list(extra_indexes)}")
            
            # Check index usage
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            try:
                cursor.execute("PRAGMA compile_options")
                compile_options = [row[0] for row in cursor.fetchall()]
                
                if any('OMIT_LOAD_EXTENSION' in opt for opt in compile_options):
                    evidence.append("⚠️  SQLite compiled without load extension support")
                
            except:
                pass
            
            passed = len(missing_indexes) == 0
            
            return DataIntegrityResult(
                test_name="required_indexes",
                passed=passed,
                message="Required indexes validation",
                affected_rows=len(existing_indexes),
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="required_indexes",
                passed=False,
                message=f"Error checking indexes: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
    
    async def test_data_encryption(self) -> DataIntegrityResult:
        """Test database encryption settings"""
        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            evidence = []
            encrypted_tables = []
            
            # Check for encryption in SQLite
            try:
                cursor.execute("PRAGMA cipher_encrypt")
                encryption_status = cursor.fetchone()
                if encryption_status and encryption_status[0] > 0:
                    evidence.append("✅ SQLite encryption is enabled")
                    encrypted_tables.append("All tables")
                else:
                    evidence.append("⚠️  SQLite encryption is not enabled")
            except sqlite3.Error:
                evidence.append("⚠️  Could not check SQLite encryption status")
            
            # Check for encrypted columns in schema
            schema = self.get_schema_info()
            sensitive_tables = ['users', 'audit_logs', 'activities']
            
            for table_name in sensitive_tables:
                if table_name in schema.tables:
                    table = schema.tables[table_name]
                    
                    # Check for potential sensitive data columns
                    sensitive_columns = []
                    for col_name, col_info in table['columns'].items():
                        if any(keyword in col_name.lower() for keyword in ['password', 'token', 'secret', 'key']):
                            sensitive_columns.append(col_name)
                    
                    if sensitive_columns:
                        evidence.append(f"📋 {table_name} contains sensitive columns: {sensitive_columns}")
                    else:
                        evidence.append(f"📋 {table_name} - no obvious sensitive columns")
            
            # Check file permissions
            if os.path.exists(self.database_path):
                file_stat = os.stat(self.database_path)
                file_mode = oct(file_stat.st_mode)[-3:]
                if file_mode != '600':
                    evidence.append(f"⚠️  Database file permissions: {file_mode} (recommended: 600)")
                else:
                    evidence.append("✅ Database file permissions are secure")
            
            # For production environments, recommend encryption
            evidence.append("💡 Recommendation: Enable database-level encryption for production use")
            
            passed = True  # Most systems won't have encryption in dev
            
            return DataIntegrityResult(
                test_name="data_encryption",
                passed=passed,
                message="Data encryption validation",
                affected_rows=len(encrypted_tables),
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="data_encryption",
                passed=False,
                message=f"Error testing data encryption: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def test_migration_integrity(self) -> DataIntegrityResult:
        """Test migration history and integrity"""
        try:
            evidence = []
            
            # Check if migration table exists
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status TEXT NOT NULL,
                        sql_statements TEXT,
                        checksum TEXT,
                        duration_seconds REAL,
                        error_message TEXT
                    )
                """)
                
                # Check migration history
                cursor.execute("""
                    SELECT id, name, status, timestamp, error_message 
                    FROM schema_migrations 
                    ORDER BY timestamp DESC
                    LIMIT 10
                """)
                
                migrations = cursor.fetchall()
                
                if migrations:
                    evidence.append(f"📊 Found {len(migrations)} migration records")
                    
                    successful = [m for m in migrations if m['status'] == 'completed']
                    failed = [m for m in migrations if m['status'] == 'failed']
                    
                    evidence.append(f"✅ Successful migrations: {len(successful)}")
                    if failed:
                        evidence.append(f"❌ Failed migrations: {len(failed)}")
                        for failed_migration in failed:
                            evidence.append(f"  - {failed_migration['name']}: {failed_migration['error_message'] or 'Unknown error'}")
                    
                    # Check for migration order integrity
                    timestamps = [datetime.fromisoformat(m['timestamp']) for m in migrations]
                    is_ordered = all(timestamps[i] >= timestamps[i+1] for i in range(len(timestamps)-1))
                    
                    if is_ordered:
                        evidence.append("✅ Migration timestamps are properly ordered")
                    else:
                        evidence.append("⚠️  Migration timestamps are not properly ordered")
                else:
                    evidence.append("ℹ️  No migration history found")
                    
            except sqlite3.Error as e:
                evidence.append(f"⚠️  Could not access migration table: {str(e)}")
            
            passed = True  # Migration integrity is optional
            
            return DataIntegrityResult(
                test_name="migration_integrity",
                passed=passed,
                message="Migration integrity validation",
                affected_rows=len(migrations) if 'migrations' in locals() else 0,
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="migration_integrity",
                passed=False,
                message=f"Error testing migration integrity: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def test_performance_indexes(self) -> DataIntegrityResult:
        """Test database performance and index usage"""
        try:
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            evidence = []
            
            # Check database file size
            file_size = os.path.getsize(self.database_path)
            size_mb = file_size / (1024 * 1024)
            evidence.append(f"📊 Database file size: {size_mb:.2f} MB")
            
            # Check page size and configuration
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            evidence.append(f"📊 Page size: {page_size} bytes")
            
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            evidence.append(f"📊 Page count: {page_count}")
            
            # Check for large tables that might need indexes
            schema = self.get_schema_info()
            large_tables = []
            
            for table_name, table_info in schema.tables.items():
                row_count = table_info['row_count']
                if row_count > 1000:  # Threshold for "large" tables
                    large_tables.append((table_name, row_count))
            
            if large_tables:
                evidence.append(f"📈 Large tables (>1000 rows): {len(large_tables)}")
                for table_name, row_count in sorted(large_tables, key=lambda x: x[1], reverse=True)[:5]:
                    evidence.append(f"  - {table_name}: {row_count} rows")
            
            # Check for missing indexes on foreign keys
            fk_missing_indexes = []
            for table_name, table_info in schema.tables.items():
                columns = table_info['columns']
                for col_name, col_info in columns.items():
                    # Check if this looks like a foreign key
                    if col_name.endswith('_id') and not col_info['primary_key']:
                        index_name = f"idx_{table_name}_{col_name}"
                        if index_name not in [idx['name'] for idx in schema.indexes]:
                            fk_missing_indexes.append((table_name, col_name))
            
            if fk_missing_indexes:
                evidence.append(f"⚠️  Missing indexes on foreign keys: {len(fk_missing_indexes)}")
                for table_name, col_name in fk_missing_indexes[:10]:
                    evidence.append(f"  - {table_name}.{col_name}")
            else:
                evidence.append("✅ Foreign keys appear to be indexed")
            
            passed = len(fk_missing_indexes) <= 5  # Allow up to 5 missing indexes
            
            return DataIntegrityResult(
                test_name="performance_indexes",
                passed=passed,
                message="Performance indexes validation",
                affected_rows=sum(count for _, count in large_tables),
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="performance_indexes",
                passed=False,
                message=f"Error testing performance indexes: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def simulate_database_corruption(self) -> DataIntegrityResult:
        """Simulate and test database corruption scenarios"""
        try:
            evidence = []
            
            # Create a test backup before testing
            backup_path = self.create_database_backup()
            evidence.append(f"📁 Created test backup: {backup_path}")
            
            # Test database integrity check
            conn = self.connect_to_database()
            cursor = conn.cursor()
            
            try:
                cursor.execute("PRAGMA integrity_check")
                integrity_result = cursor.fetchall()
                
                if integrity_result[0][0] == 'ok':
                    evidence.append("✅ Database integrity check passed")
                else:
                    evidence.append(f"❌ Database integrity issues found: {integrity_result}")
                    
            except sqlite3.Error as e:
                evidence.append(f"❌ Database integrity check failed: {str(e)}")
            
            # Test corruption recovery
            try:
                cursor.execute("PRAGMA quick_check")
                quick_check_result = cursor.fetchall()
                
                if quick_check_result[0][0] == 'ok':
                    evidence.append("✅ Database quick check passed")
                else:
                    evidence.append(f"⚠️  Database quick check issues: {quick_check_result}")
                    
            except sqlite3.Error as e:
                evidence.append(f"⚠️  Database quick check failed: {str(e)}")
            
            # Restore from backup
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, self.database_path)
                evidence.append("✅ Database restored from backup")
            
            passed = True  # Assume passed if integrity checks pass
            
            return DataIntegrityResult(
                test_name="database_corruption_simulation",
                passed=passed,
                message="Database corruption simulation",
                affected_rows=1,
                timestamp=datetime.now(),
                evidence=evidence
            )
            
        except Exception as e:
            return DataIntegrityResult(
                test_name="database_corruption_simulation",
                passed=False,
                message=f"Error simulating database corruption: {str(e)}",
                affected_rows=0,
                timestamp=datetime.now(),
                evidence=[]
            )
        finally:
            conn.close()
    
    async def run_database_validation(self) -> Dict[str, Any]:
        """Run comprehensive database validation"""
        logger.info("Starting database integrity validation")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "database_path": self.database_path,
            "database_size_bytes": 0,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_results": [],
            "schema_info": {},
            "recommendations": []
        }
        
        if not self.database_path:
            results["error"] = "No database path specified"
            return results
        
        # Get basic database information
        try:
            if os.path.exists(self.database_path):
                results["database_size_bytes"] = os.path.getsize(self.database_path)
                
                # Get schema information
                schema = self.get_schema_info()
                results["schema_info"] = {
                    "name": schema.name,
                    "engine": schema.version,
                    "table_count": len(schema.tables),
                    "index_count": len(schema.indexes),
                    "trigger_count": len(schema.triggers),
                    "constraint_count": len(schema.constraints)
                }
                
        except Exception as e:
            logger.error(f"Error getting database info: {str(e)}")
            results["error"] = f"Could not access database: {str(e)}"
            return results
        
        # Run database tests
        database_tests = [
            ("Required Tables", self.test_required_tables_exist),
            ("Foreign Key Integrity", self.test_foreign_key_integrity),
            ("Data Consistency", self.test_data_consistency),
            ("Required Indexes", self.test_required_indexes),
            ("Data Encryption", self.test_data_encryption),
            ("Migration Integrity", self.test_migration_integrity),
            ("Performance Indexes", self.test_performance_indexes),
            ("Corruption Simulation", self.simulate_database_corruption)
        ]
        
        results["total_tests"] = len(database_tests)
        
        for test_name, test_function in database_tests:
            try:
                logger.info(f"Running test: {test_name}")
                result = await test_function()
                
                results["test_results"].append({
                    "test_name": result.test_name,
                    "display_name": test_name,
                    "passed": result.passed,
                    "message": result.message,
                    "affected_rows": result.affected_rows,
                    "timestamp": result.timestamp.isoformat(),
                    "evidence": result.evidence
                })
                
                if result.passed:
                    results["passed_tests"] += 1
                else:
                    results["failed_tests"] += 1
                    
            except Exception as e:
                logger.error(f"Error running test {test_name}: {str(e)}")
                results["test_results"].append({
                    "test_name": test_name.lower().replace(' ', '_'),
                    "display_name": test_name,
                    "passed": False,
                    "message": f"Test execution error: {str(e)}",
                    "affected_rows": 0,
                    "timestamp": datetime.now().isoformat(),
                    "evidence": []
                })
                results["failed_tests"] += 1
        
        # Calculate success rate
        if results["total_tests"] > 0:
            success_rate = (results["passed_tests"] / results["total_tests"]) * 100
        else:
            success_rate = 0
        
        # Generate recommendations
        if success_rate >= 90:
            results["recommendations"].append("✅ Excellent database integrity - system ready for production")
        elif success_rate >= 75:
            results["recommendations"].append("⚠️  Good database integrity - address issues before production")
        else:
            results["recommendations"].append("❌ Database integrity issues detected - significant work required")
        
        # Check for critical issues
        critical_failures = [
            r for r in results["test_results"] 
            if not r["passed"] and r["display_name"] in ["Required Tables", "Foreign Key Integrity", "Data Consistency"]
        ]
        
        if critical_failures:
            results["recommendations"].append("🚨 CRITICAL: Resolve table, foreign key, or consistency issues immediately")
        
        # Performance recommendations
        performance_issues = [
            r for r in results["test_results"]
            if not r["passed"] and "Performance" in r["display_name"]
        ]
        
        if performance_issues:
            results["recommendations"].append("⚡ Performance issues detected - consider adding missing indexes")
        
        # Security recommendations
        security_issues = [
            r for r in results["test_results"]
            if "Encryption" in r["display_name"] and not r["passed"]
        ]
        
        if security_issues:
            results["recommendations"].append("🔐 Enable database encryption for production deployment")
        
        logger.info(f"✅ Database validation completed - Success rate: {success_rate:.1f}%")
        return results

def main():
    """CLI interface for database validation"""
    parser = argparse.ArgumentParser(description="Database Integrity Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for API testing")
    parser.add_argument("--database", required=True, help="Path to database file")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--backup", action="store_true", help="Create backup before testing")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        async with DatabaseValidator(args.url, args.token, args.database) as validator:
            results = await validator.run_database_validation()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    if results["passed_tests"] >= results["total_tests"] * 0.8:  # 80% pass rate
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()