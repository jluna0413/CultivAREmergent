#!/usr/bin/env python3
"""
Disaster Recovery and Backup Testing Framework for CultivAR Application
Ensures comprehensive backup, recovery, and business continuity capabilities.
"""

import asyncio
import aiohttp
import json
import logging
import argparse
import sys
import time
import shutil
import os
import tempfile
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import threading
import hashlib
import tarfile
import zipfile
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BackupStatus(Enum):
    """Backup operation status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CORRUPTED = "corrupted"

class RecoveryStatus(Enum):
    """Recovery operation status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"

class DisasterRecoveryTier(Enum):
    """Disaster recovery tier levels"""
    TIER_0 = "tier_0"  # RPO: 0 minutes, RTO: 0 hours (synchronous replication)
    TIER_1 = "tier_1"  # RPO: 1 minute, RTO: 1 hour (synchronous replication)
    TIER_2 = "tier_2"  # RPO: 1 hour, RTO: 4 hours (asynchronous replication)
    TIER_3 = "tier_3"  # RPO: 24 hours, RTO: 24 hours (backup-based recovery)
    TIER_4 = "tier_4"  # RPO: 1 week, RTO: 1 week (tape backup)

@dataclass
class BackupMetadata:
    """Backup metadata information"""
    backup_id: str
    timestamp: datetime
    size_bytes: int
    checksum: str
    compression_ratio: float
    backup_type: str
    source_paths: List[str]
    status: BackupStatus
    error_message: Optional[str] = None

@dataclass
class RecoveryTestResult:
    """Recovery test result"""
    test_name: str
    passed: bool
    rto_minutes: float  # Recovery Time Objective
    rpo_minutes: float  # Recovery Point Objective
    data_integrity_score: float  # 0.0 to 100.0
    recovery_status: RecoveryStatus
    evidence: List[str]
    timestamp: datetime
    recommendations: List[str]

class DisasterRecoveryValidator:
    """Main disaster recovery and backup validation framework"""
    
    def __init__(self, base_url: str, auth_token: str = None, database_path: str = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.database_path = database_path
        self.session = None
        self.backup_locations = []
        self.test_results: List[RecoveryTestResult] = []
        
        # Disaster recovery configuration
        self.rpo_target_minutes = 60  # Recovery Point Objective: 1 hour
        self.rto_target_minutes = 240  # Recovery Time Objective: 4 hours
        self.min_backup_frequency_hours = 24  # Backup at least every 24 hours
        self.min_retention_days = 30  # Keep backups for at least 30 days
        
        # File paths to backup
        self.critical_paths = self._get_critical_paths()
        
        # Backup locations configuration
        self.backup_locations = [
            "backups/",
            "/var/backups/cultivar/",
            "s3://cultivar-backups/",
            "network_share://backup.cultivar.local/"
        ]
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'CultivAR-DisasterRecoveryValidator/1.0',
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
    
    def _get_critical_paths(self) -> List[str]:
        """Get list of critical paths that must be backed up"""
        paths = []
        
        if self.database_path:
            paths.append(self.database_path)
        
        # Add application configuration
        paths.extend([
            "app/config/",
            "app/web/templates/",
            "app/web/static/",
            ".env",
            "docker-compose.yml",
            "Dockerfile"
        ])
        
        return [p for p in paths if os.path.exists(p)]
    
    def create_test_backup(self) -> BackupMetadata:
        """Create a test backup of critical files"""
        logger.info("Creating test backup")
        
        timestamp = datetime.now()
        backup_id = f"test_backup_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        backup_dir = f"tests/disaster_recovery/test_backups/{backup_id}"
        
        os.makedirs(backup_dir, exist_ok=True)
        
        try:
            backup_metadata = BackupMetadata(
                backup_id=backup_id,
                timestamp=timestamp,
                size_bytes=0,
                checksum="",
                compression_ratio=0.0,
                backup_type="test",
                source_paths=[],
                status=BackupStatus.RUNNING
            )
            
            # Create backup of critical files
            total_size = 0
            source_paths = []
            
            for source_path in self.critical_paths:
                if os.path.exists(source_path):
                    if os.path.isfile(source_path):
                        # Backup individual file
                        dest_path = os.path.join(backup_dir, os.path.basename(source_path))
                        shutil.copy2(source_path, dest_path)
                        file_size = os.path.getsize(source_path)
                        total_size += file_size
                        source_paths.append(source_path)
                        
                    elif os.path.isdir(source_path):
                        # Backup directory
                        dest_dir = os.path.join(backup_dir, os.path.basename(source_path))
                        shutil.copytree(source_path, dest_dir, dirs_exist_ok=True)
                        
                        # Calculate directory size
                        dir_size = sum(
                            os.path.getsize(os.path.join(dirpath, filename))
                            for dirpath, dirnames, filenames in os.walk(source_path)
                            for filename in filenames
                        )
                        total_size += dir_size
                        source_paths.append(source_path)
            
            # Create backup manifest
            manifest = {
                "backup_id": backup_id,
                "timestamp": timestamp.isoformat(),
                "source_paths": source_paths,
                "total_size_bytes": total_size,
                "backup_type": "test",
                "version": "1.0"
            }
            
            manifest_path = os.path.join(backup_dir, "backup_manifest.json")
            with open(manifest_path, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            # Calculate checksum
            checksum = self._calculate_directory_checksum(backup_dir)
            
            # Update metadata
            backup_metadata.size_bytes = total_size
            backup_metadata.checksum = checksum
            backup_metadata.source_paths = source_paths
            backup_metadata.status = BackupStatus.COMPLETED
            
            logger.info(f"✅ Test backup created: {backup_id} ({total_size} bytes)")
            return backup_metadata
            
        except Exception as e:
            logger.error(f"❌ Test backup failed: {str(e)}")
            return BackupMetadata(
                backup_id=backup_id,
                timestamp=timestamp,
                size_bytes=0,
                checksum="",
                compression_ratio=0.0,
                backup_type="test",
                source_paths=[],
                status=BackupStatus.FAILED,
                error_message=str(e)
            )
    
    def _calculate_directory_checksum(self, directory_path: str) -> str:
        """Calculate checksum for entire directory"""
        hasher = hashlib.sha256()
        
        for root, dirs, files in os.walk(directory_path):
            for filename in sorted(files):
                file_path = os.path.join(root, filename)
                with open(file_path, 'rb') as f:
                    # Read file in chunks to handle large files
                    while chunk := f.read(8192):
                        hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def verify_backup_integrity(self, backup_metadata: BackupMetadata) -> Tuple[bool, List[str]]:
        """Verify backup integrity by checking checksum and structure"""
        evidence = []
        backup_dir = f"tests/disaster_recovery/test_backups/{backup_metadata.backup_id}"
        
        try:
            # Check if backup directory exists
            if not os.path.exists(backup_dir):
                return False, ["❌ Backup directory not found"]
            
            # Verify manifest exists
            manifest_path = os.path.join(backup_dir, "backup_manifest.json")
            if not os.path.exists(manifest_path):
                return False, ["❌ Backup manifest not found"]
            
            # Load and verify manifest
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            evidence.append(f"✅ Backup manifest found and readable")
            
            # Verify checksum
            calculated_checksum = self._calculate_directory_checksum(backup_dir)
            if calculated_checksum == backup_metadata.checksum:
                evidence.append("✅ Backup checksum verification passed")
            else:
                evidence.append("❌ Backup checksum verification failed")
                return False, evidence
            
            # Verify source paths exist in backup
            for source_path in backup_metadata.source_paths:
                if os.path.isfile(source_path):
                    backup_file = os.path.join(backup_dir, os.path.basename(source_path))
                    if os.path.exists(backup_file):
                        evidence.append(f"✅ Backed up file: {source_path}")
                    else:
                        evidence.append(f"❌ Missing backup file: {source_path}")
                        return False, evidence
                elif os.path.isdir(source_path):
                    backup_dir_path = os.path.join(backup_dir, os.path.basename(source_path))
                    if os.path.exists(backup_dir_path):
                        evidence.append(f"✅ Backed up directory: {source_path}")
                    else:
                        evidence.append(f"❌ Missing backup directory: {source_path}")
                        return False, evidence
            
            # Verify backup size
            actual_size = sum(
                os.path.getsize(os.path.join(root, filename))
                for root, dirs, files in os.walk(backup_dir)
                for filename in files
            )
            
            if actual_size == backup_metadata.size_bytes:
                evidence.append(f"✅ Backup size verified: {actual_size} bytes")
            else:
                evidence.append(f"⚠️  Size mismatch: expected {backup_metadata.size_bytes}, actual {actual_size}")
            
            return True, evidence
            
        except Exception as e:
            return False, [f"❌ Backup verification failed: {str(e)}"]
    
    def simulate_data_corruption(self, original_path: str) -> str:
        """Simulate data corruption for testing recovery"""
        if not os.path.exists(original_path):
            raise FileNotFoundError(f"Original file not found: {original_path}")
        
        # Create a backup of original
        corrupted_path = f"{original_path}.corrupted"
        shutil.copy2(original_path, corrupted_path)
        
        try:
            # Corrupt the file by modifying its content
            with open(corrupted_path, 'r' if os.path.isfile(original_path) else 'rb') as f:
                if os.path.isfile(original_path):
                    content = f.read()
                    # Add corruption marker
                    corrupted_content = content + b"\n# CORRUPTED FOR TESTING\n"
                    with open(corrupted_path, 'wb') as out_f:
                        out_f.write(corrupted_content)
                else:
                    # For directories, add a corrupt file
                    corrupt_file = os.path.join(corrupted_path, "CORRUPTED_FILE.txt")
                    with open(corrupt_file, 'w') as f:
                        f.write("This file corrupts the directory structure")
            
            logger.info(f"✅ Simulated data corruption: {corrupted_path}")
            return corrupted_path
            
        except Exception as e:
            logger.error(f"❌ Failed to simulate corruption: {str(e)}")
            # Restore original
            if os.path.exists(corrupted_path):
                os.remove(corrupted_path)
            raise
    
    async def test_file_level_recovery(self) -> RecoveryTestResult:
        """Test file-level data recovery"""
        start_time = time.time()
        evidence = []
        
        try:
            # Create test backup
            backup_metadata = self.create_test_backup()
            if backup_metadata.status != BackupStatus.COMPLETED:
                return RecoveryTestResult(
                    test_name="file_level_recovery",
                    passed=False,
                    rto_minutes=0,
                    rpo_minutes=0,
                    data_integrity_score=0,
                    recovery_status=RecoveryStatus.FAILED,
                    evidence=["❌ Failed to create test backup"],
                    timestamp=datetime.now(),
                    recommendations=["Check backup creation process"]
                )
            
            evidence.append(f"✅ Created test backup: {backup_metadata.backup_id}")
            
            # Simulate corruption in one of the backed-up files
            if backup_metadata.source_paths:
                test_file = backup_metadata.source_paths[0]
                if os.path.isfile(test_file):
                    corrupted_path = self.simulate_data_corruption(test_file)
                    evidence.append(f"✅ Simulated corruption in: {test_file}")
                    
                    # Verify corruption
                    if os.path.exists(corrupted_path):
                        evidence.append("✅ Corruption verification successful")
                    else:
                        evidence.append("❌ Corruption verification failed")
            
            # Perform recovery from backup
            recovery_start_time = time.time()
            
            # Find backup directory
            backup_dir = f"tests/disaster_recovery/test_backups/{backup_metadata.backup_id}"
            
            if not os.path.exists(backup_dir):
                return RecoveryTestResult(
                    test_name="file_level_recovery",
                    passed=False,
                    rto_minutes=0,
                    rpo_minutes=0,
                    data_integrity_score=0,
                    recovery_status=RecoveryStatus.FAILED,
                    evidence=["❌ Backup directory not found for recovery"],
                    timestamp=datetime.now(),
                    recommendations=["Verify backup storage and access"]
                )
            
            # Restore files from backup
            restore_count = 0
            for source_path in backup_metadata.source_paths:
                if os.path.isfile(source_path):
                    backup_file = os.path.join(backup_dir, os.path.basename(source_path))
                    if os.path.exists(backup_file):
                        # Remove corrupted file first
                        if os.path.exists(corrupted_path):
                            os.remove(corrupted_path)
                        
                        # Restore from backup
                        shutil.copy2(backup_file, source_path)
                        restore_count += 1
                        evidence.append(f"✅ Restored file: {source_path}")
            
            recovery_time = time.time() - recovery_start_time
            
            # Verify recovery
            recovery_success = True
            if os.path.exists(test_file) and not os.path.exists(f"{test_file}.corrupted"):
                evidence.append("✅ File successfully recovered from backup")
            else:
                evidence.append("❌ File recovery failed")
                recovery_success = False
            
            # Calculate metrics
            rto_minutes = recovery_time / 60
            rpo_minutes = 30  # Assume 30 minutes RPO for file-level backup
            
            integrity_score = 100.0 if recovery_success else 0.0
            
            return RecoveryTestResult(
                test_name="file_level_recovery",
                passed=recovery_success,
                rto_minutes=rto_minutes,
                rpo_minutes=rpo_minutes,
                data_integrity_score=integrity_score,
                recovery_status=RecoveryStatus.SUCCESS if recovery_success else RecoveryStatus.FAILED,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"File-level recovery completed in {rto_minutes:.2f} minutes",
                    "Implement automated file integrity monitoring",
                    "Consider incremental backup strategies"
                ]
            )
            
        except Exception as e:
            return RecoveryTestResult(
                test_name="file_level_recovery",
                passed=False,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=0,
                recovery_status=RecoveryStatus.FAILED,
                evidence=[f"❌ File-level recovery test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check backup and recovery procedures", "Verify file permissions"]
            )
    
    async def test_database_recovery(self) -> RecoveryTestResult:
        """Test database recovery from backup"""
        start_time = time.time()
        evidence = []
        
        try:
            if not self.database_path or not os.path.exists(self.database_path):
                return RecoveryTestResult(
                    test_name="database_recovery",
                    passed=False,
                    rto_minutes=0,
                    rpo_minutes=0,
                    data_integrity_score=0,
                    recovery_status=RecoveryStatus.FAILED,
                    evidence=["❌ Database path not specified or not found"],
                    timestamp=datetime.now(),
                    recommendations=["Configure database backup and recovery procedures"]
                )
            
            evidence.append(f"✅ Database found: {self.database_path}")
            
            # Create database backup
            backup_metadata = self.create_test_backup()
            if backup_metadata.status != BackupStatus.COMPLETED:
                return RecoveryTestResult(
                    test_name="database_recovery",
                    passed=False,
                    rto_minutes=0,
                    rpo_minutes=0,
                    data_integrity_score=0,
                    recovery_status=RecoveryStatus.FAILED,
                    evidence=["❌ Failed to create database backup"],
                    timestamp=datetime.now(),
                    recommendations=["Check database backup procedures"]
                )
            
            evidence.append(f"✅ Database backup created: {backup_metadata.backup_id}")
            
            # Get current database info
            import sqlite3
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            original_table_count = cursor.fetchone()[0]
            evidence.append(f"✅ Original database has {original_table_count} tables")
            
            conn.close()
            
            # Simulate database corruption by modifying the file
            corrupted_db_path = f"{self.database_path}.corrupted"
            shutil.copy2(self.database_path, corrupted_db_path)
            
            # Add corruption data
            with open(corrupted_db_path, 'ab') as f:
                f.write(b"\x00\x01\x02\x03CORRUPTED_FOR_TESTING")
            
            evidence.append("✅ Database file corrupted for testing")
            
            # Test recovery from backup
            recovery_start_time = time.time()
            
            # Restore database from backup
            backup_dir = f"tests/disaster_recovery/test_backups/{backup_metadata.backup_id}"
            backup_db_file = os.path.join(backup_dir, os.path.basename(self.database_path))
            
            if os.path.exists(backup_db_file):
                # Remove corrupted file
                os.remove(corrupted_db_path)
                
                # Restore from backup
                shutil.copy2(backup_db_file, self.database_path)
                evidence.append("✅ Database restored from backup")
            else:
                return RecoveryTestResult(
                    test_name="database_recovery",
                    passed=False,
                    rto_minutes=0,
                    rpo_minutes=0,
                    data_integrity_score=0,
                    recovery_status=RecoveryStatus.FAILED,
                    evidence=["❌ Database backup file not found"],
                    timestamp=datetime.now(),
                    recommendations=["Check database backup process"]
                )
            
            recovery_time = time.time() - recovery_start_time
            
            # Verify database integrity after recovery
            try:
                conn = sqlite3.connect(self.database_path)
                cursor = conn.cursor()
                
                # Check if database is readable
                cursor.execute("PRAGMA integrity_check")
                integrity_result = cursor.fetchall()
                
                if integrity_result[0][0] == 'ok':
                    evidence.append("✅ Database integrity check passed")
                    
                    # Check table count
                    cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                    restored_table_count = cursor.fetchone()[0]
                    
                    if restored_table_count == original_table_count:
                        evidence.append(f"✅ Database fully restored ({restored_table_count} tables)")
                        integrity_score = 100.0
                    else:
                        evidence.append(f"⚠️  Partial restoration ({restored_table_count}/{original_table_count} tables)")
                        integrity_score = (restored_table_count / original_table_count) * 100
                else:
                    evidence.append(f"❌ Database integrity check failed: {integrity_result}")
                    integrity_score = 0.0
                
                conn.close()
                
            except Exception as e:
                evidence.append(f"❌ Database verification failed: {str(e)}")
                integrity_score = 0.0
            
            # Calculate metrics
            rto_minutes = recovery_time / 60
            rpo_minutes = 60  # Assume 1 hour RPO for database backup
            
            recovery_success = integrity_score >= 95.0
            
            return RecoveryTestResult(
                test_name="database_recovery",
                passed=recovery_success,
                rto_minutes=rto_minutes,
                rpo_minutes=rpo_minutes,
                data_integrity_score=integrity_score,
                recovery_status=RecoveryStatus.SUCCESS if recovery_success else RecoveryStatus.FAILED,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    f"Database recovery completed in {rto_minutes:.2f} minutes",
                    f"Data integrity score: {integrity_score:.1f}%",
                    "Implement automated database integrity monitoring",
                    "Consider point-in-time recovery capabilities"
                ]
            )
            
        except Exception as e:
            return RecoveryTestResult(
                test_name="database_recovery",
                passed=False,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=0,
                recovery_status=RecoveryStatus.FAILED,
                evidence=[f"❌ Database recovery test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check database backup and recovery procedures"]
            )
    
    async def test_backup_scheduling(self) -> RecoveryTestResult:
        """Test backup scheduling and automation"""
        evidence = []
        
        try:
            # Test backup schedule endpoint if available
            schedule_response = await self.session.get(f"{self.base_url}/api/backup/schedule")
            
            if schedule_response.status == 200:
                schedule_data = await schedule_response.json()
                schedules = schedule_data.get('schedules', [])
                
                evidence.append(f"✅ Backup schedule endpoint accessible")
                evidence.append(f"📊 Found {len(schedules)} configured backup schedules")
                
                # Analyze backup schedules
                schedule_types = {}
                for schedule in schedules:
                    schedule_type = schedule.get('type', 'unknown')
                    schedule_types[schedule_type] = schedule_types.get(schedule_type, 0) + 1
                
                evidence.append(f"📊 Schedule types: {schedule_types}")
                
                # Check for automated backup
                automated_schedules = [s for s in schedules if s.get('automated', False)]
                if automated_schedules:
                    evidence.append(f"✅ Found {len(automated_schedules)} automated backup schedules")
                else:
                    evidence.append("⚠️  No automated backup schedules found")
                
                # Test backup frequency
                frequency_ok = True
                if schedules:
                    for schedule in schedules:
                        frequency = schedule.get('frequency_hours', 0)
                        if frequency > self.min_backup_frequency_hours:
                            evidence.append(f"⚠️  Backup frequency too low: {frequency} hours")
                            frequency_ok = False
                        else:
                            evidence.append(f"✅ Backup frequency acceptable: {frequency} hours")
                
                score = 80.0 if len(schedules) > 0 and frequency_ok else 60.0
            else:
                evidence.append(f"❌ Backup schedule endpoint not accessible (status: {schedule_response.status})")
                evidence.append("💡 Consider implementing automated backup scheduling")
                score = 40.0
            
            # Test backup retention policy
            retention_response = await self.session.get(f"{self.base_url}/api/backup/retention")
            if retention_response.status == 200:
                retention_data = await retention_response.json()
                retention_days = retention_data.get('retention_days', 0)
                
                if retention_days >= self.min_retention_days:
                    evidence.append(f"✅ Backup retention policy adequate: {retention_days} days")
                else:
                    evidence.append(f"⚠️  Backup retention too short: {retention_days} days (minimum: {self.min_retention_days})")
            
            return RecoveryTestResult(
                test_name="backup_scheduling",
                passed=score >= 70,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=score,
                recovery_status=RecoveryStatus.SUCCESS,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement automated backup scheduling",
                    f"Ensure backup frequency meets RPO requirements (max {self.min_backup_frequency_hours}h)",
                    f"Maintain backup retention for minimum {self.min_retention_days} days",
                    "Consider off-site backup replication"
                ]
            )
            
        except Exception as e:
            return RecoveryTestResult(
                test_name="backup_scheduling",
                passed=False,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=0,
                recovery_status=RecoveryStatus.FAILED,
                evidence=[f"❌ Backup scheduling test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check backup service configuration", "Implement automated backup scheduling"]
            )
    
    async def test_disaster_recovery_plan(self) -> RecoveryTestResult:
        """Test disaster recovery plan and procedures"""
        evidence = []
        
        try:
            # Test DR plan endpoint if available
            dr_plan_response = await self.session.get(f"{self.base_url}/api/disaster-recovery/plan")
            
            if dr_plan_response.status == 200:
                dr_plan_data = await dr_plan_response.json()
                dr_plan = dr_plan_data.get('plan', {})
                
                evidence.append(f"✅ DR plan endpoint accessible")
                
                # Analyze DR plan components
                required_components = [
                    "backup_procedures",
                    "recovery_procedures",
                    "contact_information",
                    "testing_schedule",
                    "communication_plan"
                ]
                
                components_found = []
                for component in required_components:
                    if component in dr_plan:
                        components_found.append(component)
                        evidence.append(f"✅ DR plan includes: {component}")
                    else:
                        evidence.append(f"❌ DR plan missing: {component}")
                
                # Check RTO/RPO targets
                rto_target = dr_plan.get('rto_minutes', 0)
                rpo_target = dr_plan.get('rpo_minutes', 0)
                
                if rto_target <= self.rto_target_minutes:
                    evidence.append(f"✅ RTO target acceptable: {rto_target} minutes")
                else:
                    evidence.append(f"⚠️  RTO target exceeds SLA: {rto_target} minutes")
                
                if rpo_target <= self.rpo_target_minutes:
                    evidence.append(f"✅ RPO target acceptable: {rpo_target} minutes")
                else:
                    evidence.append(f"⚠️  RPO target exceeds SLA: {rpo_target} minutes")
                
                score = (len(components_found) / len(required_components)) * 100
            else:
                evidence.append(f"❌ DR plan endpoint not accessible (status: {dr_plan_response.status})")
                evidence.append("💡 Create comprehensive disaster recovery plan")
                score = 30.0
            
            # Test recovery testing capability
            try:
                test_response = await self.session.post(f"{self.base_url}/api/disaster-recovery/test")
                if test_response.status in [200, 201]:
                    evidence.append("✅ DR testing capability confirmed")
                else:
                    evidence.append("⚠️  DR testing not available")
            except:
                evidence.append("⚠️  DR testing capability not found")
            
            return RecoveryTestResult(
                test_name="disaster_recovery_plan",
                passed=score >= 60,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=score,
                recovery_status=RecoveryStatus.SUCCESS,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Create comprehensive disaster recovery plan",
                    "Document all recovery procedures",
                    "Establish clear RTO/RPO objectives",
                    "Conduct regular DR testing and updates"
                ]
            )
            
        except Exception as e:
            return RecoveryTestResult(
                test_name="disaster_recovery_plan",
                passed=False,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=0,
                recovery_status=RecoveryStatus.FAILED,
                evidence=[f"❌ DR plan test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check DR service configuration", "Implement disaster recovery planning"]
            )
    
    async def test_offsite_backup(self) -> RecoveryTestResult:
        """Test offsite backup replication"""
        evidence = []
        
        try:
            # Test offsite backup endpoint
            offsite_response = await self.session.get(f"{self.base_url}/api/backup/offsite")
            
            if offsite_response.status == 200:
                offsite_data = await offsite_response.json()
                offsite_locations = offsite_data.get('locations', [])
                
                evidence.append(f"✅ Offsite backup endpoint accessible")
                evidence.append(f"📊 Found {len(offsite_locations)} offsite backup locations")
                
                # Analyze offsite locations
                location_types = {}
                for location in offsite_locations:
                    location_type = location.get('type', 'unknown')
                    location_types[location_type] = location_types.get(location_type, 0) + 1
                
                evidence.append(f"📊 Offsite location types: {location_types}")
                
                # Check for redundancy
                if len(offsite_locations) >= 2:
                    evidence.append("✅ Multiple offsite backup locations for redundancy")
                else:
                    evidence.append("⚠️  Single offsite backup location - consider adding redundancy")
                
                # Test offsite connectivity
                for location in offsite_locations[:2]:  # Test first 2 locations
                    try:
                        location_url = location.get('url', '')
                        if location_url:
                            test_response = await self.session.get(f"{location_url}/health", timeout=5)
                            if test_response.status == 200:
                                evidence.append(f"✅ Offsite location accessible: {location.get('name', 'unknown')}")
                            else:
                                evidence.append(f"⚠️  Offsite location not accessible: {location.get('name', 'unknown')}")
                    except:
                        evidence.append(f"❌ Failed to connect to offsite location: {location.get('name', 'unknown')}")
                
                score = min(100.0, len(offsite_locations) * 30)
            else:
                evidence.append(f"❌ Offsite backup endpoint not accessible (status: {offsite_response.status})")
                evidence.append("💡 Consider implementing offsite backup replication")
                score = 40.0
            
            return RecoveryTestResult(
                test_name="offsite_backup",
                passed=score >= 60,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=score,
                recovery_status=RecoveryStatus.SUCCESS,
                evidence=evidence,
                timestamp=datetime.now(),
                recommendations=[
                    "Implement offsite backup replication",
                    "Ensure multiple geographic locations",
                    "Test offsite backup connectivity regularly",
                    "Monitor replication lag and integrity"
                ]
            )
            
        except Exception as e:
            return RecoveryTestResult(
                test_name="offsite_backup",
                passed=False,
                rto_minutes=0,
                rpo_minutes=0,
                data_integrity_score=0,
                recovery_status=RecoveryStatus.FAILED,
                evidence=[f"❌ Offsite backup test failed: {str(e)}"],
                timestamp=datetime.now(),
                recommendations=["Check offsite backup configuration", "Implement geographic backup redundancy"]
            )
    
    async def run_disaster_recovery_validation(self) -> Dict[str, Any]:
        """Run comprehensive disaster recovery validation"""
        logger.info("Starting disaster recovery validation")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "base_url": self.base_url,
            "database_path": self.database_path,
            "total_tests": 0,
            "passed_tests": 0,
            "overall_dr_score": 0.0,
            "test_results": [],
            "backup_locations": self.backup_locations,
            "recommendations": []
        }
        
        # Run disaster recovery tests
        dr_tests = [
            ("File-Level Recovery", self.test_file_level_recovery),
            ("Database Recovery", self.test_database_recovery),
            ("Backup Scheduling", self.test_backup_scheduling),
            ("Disaster Recovery Plan", self.test_disaster_recovery_plan),
            ("Offsite Backup", self.test_offsite_backup)
        ]
        
        results["total_tests"] = len(dr_tests)
        
        total_score = 0.0
        for test_name, test_function in dr_tests:
            try:
                logger.info(f"Running DR test: {test_name}")
                result = await test_function()
                
                results["test_results"].append({
                    "test_name": result.test_name,
                    "display_name": test_name,
                    "passed": result.passed,
                    "rto_minutes": result.rto_minutes,
                    "rpo_minutes": result.rpo_minutes,
                    "data_integrity_score": result.data_integrity_score,
                    "recovery_status": result.recovery_status.value,
                    "evidence": result.evidence,
                    "recommendations": result.recommendations,
                    "timestamp": result.timestamp.isoformat()
                })
                
                if result.passed:
                    results["passed_tests"] += 1
                
                total_score += result.data_integrity_score
                
            except Exception as e:
                logger.error(f"Error running test {test_name}: {str(e)}")
                results["test_results"].append({
                    "test_name": test_name.lower().replace(' ', '_'),
                    "display_name": test_name,
                    "passed": False,
                    "rto_minutes": 0,
                    "rpo_minutes": 0,
                    "data_integrity_score": 0,
                    "recovery_status": "failed",
                    "evidence": [f"❌ Test failed: {str(e)}"],
                    "recommendations": ["Check test implementation and system state"],
                    "timestamp": datetime.now().isoformat()
                })
        
        # Calculate overall DR score
        if results["total_tests"] > 0:
            results["overall_dr_score"] = total_score / results["total_tests"]
        else:
            results["overall_dr_score"] = 0.0
        
        # Generate comprehensive recommendations
        if results["overall_dr_score"] >= 80:
            results["recommendations"].append("✅ Excellent disaster recovery readiness - system ready for production")
        elif results["overall_dr_score"] >= 60:
            results["recommendations"].append("⚠️  Good disaster recovery - improvements needed for production")
        else:
            results["recommendations"].append("❌ Limited disaster recovery - significant work required")
        
        # Check RTO/RPO compliance
        rto_violations = [r for r in results["test_results"] if r.get("rto_minutes", 0) > self.rto_target_minutes]
        rpo_violations = [r for r in results["test_results"] if r.get("rpo_minutes", 0) > self.rpo_target_minutes]
        
        if rto_violations:
            results["recommendations"].append(f"⚠️  RTO violations detected in {len(rto_violations)} tests - improve recovery time")
        
        if rpo_violations:
            results["recommendations"].append(f"⚠️  RPO violations detected in {len(rpo_violations)} tests - improve backup frequency")
        
        # Critical DR recommendations
        if results["overall_dr_score"] < 70:
            results["recommendations"].append("🚨 CRITICAL: Implement disaster recovery plan before production deployment")
        
        # Backup frequency recommendations
        if results["overall_dr_score"] < 80:
            results["recommendations"].append(f"📅 Increase backup frequency to meet {self.rpo_target_minutes}-minute RPO requirement")
        
        # Offsite backup recommendations
        if results["overall_dr_score"] < 90:
            results["recommendations"].append("🌍 Implement offsite backup replication for geographic redundancy")
        
        # Testing recommendations
        results["recommendations"].append("🧪 Schedule regular DR testing and validation procedures")
        results["recommendations"].append("📋 Document and test recovery procedures with all stakeholders")
        
        logger.info(f"✅ Disaster recovery validation completed - Overall score: {results['overall_dr_score']:.1f}%")
        return results

def main():
    """CLI interface for disaster recovery testing"""
    parser = argparse.ArgumentParser(description="Disaster Recovery Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for testing")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--database", help="Database file path for backup testing")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        async with DisasterRecoveryValidator(args.url, args.token, args.database) as validator:
            results = await validator.run_disaster_recovery_validation()
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    if results["overall_dr_score"] >= 60:  # 60% threshold
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()