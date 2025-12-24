"""
🔄 AUTOMATED END-TO-END VALIDATION FRAMEWORK FOR CULTIVAR APPLICATION
Comprehensive testing suite covering complete user workflows and business scenarios
"""

import asyncio
import pytest
import httpx
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import os
from dataclasses import dataclass
import logging

@dataclass
class E2ETestResult:
    """End-to-end test result"""
    workflow_name: str
    scenario_name: str
    passed: bool
    duration_ms: float
    details: str
    steps_completed: int
    total_steps: int
    evidence: Optional[Dict] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

class CultivarE2EValidator:
    """Comprehensive end-to-end validation for CultivAR workflows"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results: List[E2ETestResult] = []
        self.auth_tokens = {}
        self.headers = {}
        self.logger = logging.getLogger(__name__)
        self.test_users = []
        self.test_plants = []
        self.test_sensors = []
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def run_all_e2e_tests(self) -> Dict[str, Any]:
        """Run comprehensive end-to-end test suite"""
        print("🔄 Starting CultivAR End-to-End Validation Suite...")
        
        # Test workflow categories
        test_workflows = [
            ("Complete User Onboarding Workflow", self._test_user_onboarding_workflow),
            ("Plant Lifecycle Management Workflow", self._test_plant_lifecycle_workflow),
            ("Sensor Integration Workflow", self._test_sensor_integration_workflow),
            ("Dashboard Analytics Workflow", self._test_dashboard_analytics_workflow),
            ("Cross-Platform Sync Workflow", self._test_cross_platform_sync_workflow),
            ("Data Export/Import Workflow", self._test_data_export_import_workflow),
            ("Multi-User Collaboration Workflow", self._test_multi_user_workflow),
            ("Real-Time Monitoring Workflow", self._test_realtime_monitoring_workflow),
            ("Performance Under Load Workflow", self._test_performance_workflow),
            ("Error Recovery Workflow", self._test_error_recovery_workflow),
        ]
        
        for workflow_name, workflow_func in test_workflows:
            print(f"\n🎯 Running {workflow_name}...")
            await workflow_func()
            
        return self._generate_e2e_report()
    
    async def _test_user_onboarding_workflow(self):
        """Test complete user onboarding from registration to first plant"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 8
        
        try:
            # Step 1: User Registration
            username = f"e2e_user_{random.randint(1000, 9999)}"
            email = f"e2e_{random.randint(1000, 9999)}@example.com"
            
            register_data = {
                "username": username,
                "email": email,
                "password": "TestPassword123!",
                "full_name": "E2E Test User"
            }
            
            register_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/register",
                json=register_data
            )
            
            if register_response.status_code == 201:
                steps_completed += 1
                user_id = register_response.json().get("id")
                
                # Step 2: User Login
                login_response = await self.client.post(
                    f"{self.base_url}/api/v2/auth/login",
                    json={"username": username, "password": register_data["password"]}
                )
                
                if login_response.status_code == 200:
                    steps_completed += 1
                    tokens = login_response.json()
                    self.auth_tokens = tokens
                    self.headers = {
                        "Authorization": f"Bearer {tokens['access_token']}",
                        "Content-Type": "application/json"
                    }
                    
                    # Step 3: Get User Profile
                    profile_response = await self.client.get(
                        f"{self.base_url}/api/v2/auth/me",
                        headers=self.headers
                    )
                    
                    if profile_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 4: Create First Plant
                        plant_data = {
                            "name": "E2E Test Plant",
                            "description": "First plant for end-to-end testing",
                            "status_id": 1,  # Assuming status 1 exists
                            "is_clone": False,
                            "autoflower": False
                        }
                        
                        plant_response = await self.client.post(
                            f"{self.base_url}/api/v2/plants",
                            json=plant_data,
                            headers=self.headers
                        )
                        
                        if plant_response.status_code == 201:
                            steps_completed += 1
                            plant_id = plant_response.json().get("data", {}).get("id")
                            self.test_plants.append(plant_id)
                            
                            # Step 5: View Dashboard
                            dashboard_response = await self.client.get(
                                f"{self.base_url}/api/v2/dashboard",
                                headers=self.headers
                            )
                            
                            if dashboard_response.status_code == 200:
                                steps_completed += 1
                                
                                # Step 6: Update Plant Status
                                update_data = {"status_id": 2}  # Move to next status
                                update_response = await self.client.patch(
                                    f"{self.base_url}/api/v2/plants/{plant_id}",
                                    json=update_data,
                                    headers=self.headers
                                )
                                
                                if update_response.status_code == 200:
                                    steps_completed += 1
                                    
                                    # Step 7: Add Plant Measurement
                                    measurement_data = {
                                        "name": "Height",
                                        "value": 10.5,
                                        "unit": "cm"
                                    }
                                    
                                    measurement_response = await self.client.post(
                                        f"{self.base_url}/api/v2/plants/{plant_id}/measurements",
                                        json=measurement_data,
                                        headers=self.headers
                                    )
                                    
                                    if measurement_response.status_code == 201:
                                        steps_completed += 1
                                        
                                        # Step 8: Logout
                                        logout_response = await self.client.post(
                                            f"{self.base_url}/api/v2/auth/logout",
                                            headers=self.headers
                                        )
                                        
                                        if logout_response.status_code == 200:
                                            steps_completed += 1
                                            success = True
                                        else:
                                            success = False
                                    else:
                                        success = False
                                else:
                                    success = False
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"User onboarding workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Complete User Onboarding",
            scenario_name="New User Registration to First Plant",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Onboarding completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "username": username,
                "plant_created": len(self.test_plants) > 0,
                "final_status": "success" if success and steps_completed == total_steps else "partial_failure"
            }
        ))
    
    async def _test_plant_lifecycle_workflow(self):
        """Test complete plant lifecycle from seed to harvest"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 10
        
        try:
            # Ensure we have authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Create Seed Plant
            seed_plant_data = {
                "name": "Lifecycle Test Plant",
                "description": "Testing complete plant lifecycle",
                "status_id": 1,  # Seed status
                "is_clone": False,
                "autoflower": False,
                "cultivar_id": None  # Will be populated if cultivars exist
            }
            
            plant_response = await self.client.post(
                f"{self.base_url}/api/v2/plants",
                json=seed_plant_data,
                headers=self.headers
            )
            
            if plant_response.status_code == 201:
                steps_completed += 1
                plant_data = plant_response.json()
                plant_id = plant_data.get("data", {}).get("id")
                self.test_plants.append(plant_id)
                
                # Step 2: Move to Seedling Stage
                for status_id in [2, 3, 4]:  # Seedling, Vegetative, Flowering
                    update_response = await self.client.patch(
                        f"{self.base_url}/api/v2/plants/{plant_id}",
                        json={"status_id": status_id},
                        headers=self.headers
                    )
                    
                    if update_response.status_code == 200:
                        steps_completed += 1
                        
                        # Add measurements for each stage
                        measurement_types = ["Height", "Width", "Leaf Count"]
                        for measurement_type in measurement_types:
                            measurement_data = {
                                "name": measurement_type,
                                "value": random.uniform(1.0, 100.0),
                                "unit": "cm" if measurement_type != "Leaf Count" else "count"
                            }
                            
                            await self.client.post(
                                f"{self.base_url}/api/v2/plants/{plant_id}/measurements",
                                json=measurement_data,
                                headers=self.headers
                            )
                        
                        # Add activity log
                        activity_data = {
                            "activity_type": "status_change",
                            "description": f"Moved to status {status_id}",
                            "notes": "Automated lifecycle progression"
                        }
                        
                        await self.client.post(
                            f"{self.base_url}/api/v2/plants/{plant_id}/activities",
                            json=activity_data,
                            headers=self.headers
                        )
                    else:
                        break
                
                # Step 6: Record Harvest Data
                harvest_data = {
                    "harvest_weight": random.uniform(100.0, 500.0),
                    "harvest_date": datetime.utcnow().isoformat(),
                    "notes": "Automated harvest recording"
                }
                
                harvest_response = await self.client.patch(
                    f"{self.base_url}/api/v2/plants/{plant_id}",
                    json=harvest_data,
                    headers=self.headers
                )
                
                if harvest_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 7: Generate Plant Report
                    report_response = await self.client.get(
                        f"{self.base_url}/api/v2/plants/{plant_id}/report",
                        headers=self.headers
                    )
                    
                    if report_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 8: Export Plant Data
                        export_response = await self.client.post(
                            f"{self.base_url}/api/v2/plants/{plant_id}/export",
                            json={"format": "json"},
                            headers=self.headers
                        )
                        
                        if export_response.status_code == 200:
                            steps_completed += 1
                            
                            # Step 9: Archive Plant
                            archive_response = await self.client.patch(
                                f"{self.base_url}/api/v2/plants/{plant_id}",
                                json={"status_id": 5},  # Archived status
                                headers=self.headers
                            )
                            
                            if archive_response.status_code == 200:
                                steps_completed += 1
                                
                                # Step 10: View Plant History
                                history_response = await self.client.get(
                                    f"{self.base_url}/api/v2/plants/{plant_id}/history",
                                    headers=self.headers
                                )
                                
                                if history_response.status_code == 200:
                                    steps_completed += 1
                                    success = True
                                else:
                                    success = False
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Plant lifecycle workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Plant Lifecycle Management",
            scenario_name="Seed to Harvest Complete Cycle",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Lifecycle completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "plant_id": plant_id if 'plant_id' in locals() else None,
                "stages_completed": min(steps_completed - 1, 4),
                "measurements_added": steps_completed > 2,
                "harvest_recorded": steps_completed > 6
            }
        ))
    
    async def _test_sensor_integration_workflow(self):
        """Test complete sensor integration workflow"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 8
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Discover Sensors
            discovery_response = await self.client.get(
                f"{self.base_url}/api/v2/sensors/discover",
                headers=self.headers
            )
            
            if discovery_response.status_code == 200:
                steps_completed += 1
                
                # Step 2: Create Sensor Configuration
                sensor_config = {
                    "name": "E2E Test Sensor",
                    "sensor_type": "temperature",
                    "source": "manual",
                    "unit": "°F",
                    "zone_id": None  # Will be set if zones exist
                }
                
                sensor_response = await self.client.post(
                    f"{self.base_url}/api/v2/sensors",
                    json=sensor_config,
                    headers=self.headers
                )
                
                if sensor_response.status_code == 201:
                    steps_completed += 1
                    sensor_data = sensor_response.json()
                    sensor_id = sensor_data.get("data", {}).get("id")
                    self.test_sensors.append(sensor_id)
                    
                    # Step 3: Configure Sensor Alerts
                    alert_config = {
                        "temperature_min": 65.0,
                        "temperature_max": 85.0,
                        "enabled": True
                    }
                    
                    alert_response = await self.client.patch(
                        f"{self.base_url}/api/v2/sensors/{sensor_id}/alerts",
                        json=alert_config,
                        headers=self.headers
                    )
                    
                    if alert_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 4: Add Sensor Readings
                        readings = []
                        for i in range(5):
                            reading_data = {
                                "value": random.uniform(70.0, 80.0),
                                "unit": "°F",
                                "created_at": (datetime.utcnow() - timedelta(minutes=i)).isoformat()
                            }
                            readings.append(reading_data)
                        
                        readings_response = await self.client.post(
                            f"{self.base_url}/api/v2/sensors/{sensor_id}/readings",
                            json={"readings": readings},
                            headers=self.headers
                        )
                        
                        if readings_response.status_code == 201:
                            steps_completed += 1
                            
                            # Step 5: Get Sensor Statistics
                            stats_response = await self.client.get(
                                f"{self.base_url}/api/v2/sensors/{sensor_id}/stats",
                                headers=self.headers
                            )
                            
                            if stats_response.status_code == 200:
                                steps_completed += 1
                                
                                # Step 6: Generate Sensor Report
                                report_response = await self.client.get(
                                    f"{self.base_url}/api/v2/sensors/{sensor_id}/report",
                                    headers=self.headers
                                )
                                
                                if report_response.status_code == 200:
                                    steps_completed += 1
                                    
                                    # Step 7: Test Real-time Updates
                                    realtime_response = await self.client.get(
                                        f"{self.base_url}/api/v2/sensors/{sensor_id}/live",
                                        headers=self.headers
                                    )
                                    
                                    if realtime_response.status_code == 200:
                                        steps_completed += 1
                                        
                                        # Step 8: Export Sensor Data
                                        export_response = await self.client.post(
                                            f"{self.base_url}/api/v2/sensors/{sensor_id}/export",
                                            json={"format": "csv"},
                                            headers=self.headers
                                        )
                                        
                                        if export_response.status_code == 200:
                                            steps_completed += 1
                                            success = True
                                        else:
                                            success = False
                                    else:
                                        success = False
                                else:
                                    success = False
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Sensor integration workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Sensor Integration",
            scenario_name="Complete Sensor Setup to Data Export",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Sensor integration completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "sensor_id": sensor_id if 'sensor_id' in locals() else None,
                "readings_added": len(readings) if 'readings' in locals() else 0,
                "alerts_configured": steps_completed > 2,
                "data_exported": steps_completed > 7
            }
        ))
    
    async def _test_dashboard_analytics_workflow(self):
        """Test dashboard analytics and reporting"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 6
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Get Dashboard Overview
            dashboard_response = await self.client.get(
                f"{self.base_url}/api/v2/dashboard",
                headers=self.headers
            )
            
            if dashboard_response.status_code == 200:
                steps_completed += 1
                dashboard_data = dashboard_response.json()
                
                # Step 2: Get Plant Statistics
                stats_response = await self.client.get(
                    f"{self.base_url}/api/v2/plants/stats",
                    headers=self.headers
                )
                
                if stats_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 3: Get Sensor Statistics
                    sensor_stats_response = await self.client.get(
                        f"{self.base_url}/api/v2/sensors/stats",
                        headers=self.headers
                    )
                    
                    if sensor_stats_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 4: Generate Analytics Report
                        analytics_response = await self.client.get(
                            f"{self.base_url}/api/v2/analytics/overview",
                            headers=self.headers
                        )
                        
                        if analytics_response.status_code == 200:
                            steps_completed += 1
                            
                            # Step 5: Get Growth Predictions
                            predictions_response = await self.client.get(
                                f"{self.base_url}/api/v2/analytics/predictions",
                                headers=self.headers
                            )
                            
                            if predictions_response.status_code == 200:
                                steps_completed += 1
                                
                                # Step 6: Export Dashboard Data
                                export_response = await self.client.post(
                                    f"{self.base_url}/api/v2/analytics/export",
                                    json={"format": "pdf"},
                                    headers=self.headers
                                )
                                
                                if export_response.status_code == 200:
                                    steps_completed += 1
                                    success = True
                                else:
                                    success = False
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Dashboard analytics workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Dashboard Analytics",
            scenario_name="Complete Analytics and Reporting",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Analytics completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "dashboard_data_available": steps_completed > 0,
                "statistics_retrieved": steps_completed > 1,
                "analytics_generated": steps_completed > 3,
                "data_exported": steps_completed > 5
            }
        ))
    
    
    async def _test_cross_platform_sync_workflow(self):
        """Test cross-platform synchronization between web and mobile"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 6
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Create plant via API (simulating web app)
            plant_data = {
                "name": "Cross-Platform Test Plant",
                "description": "Testing sync between platforms",
                "status_id": 1,
                "is_clone": False,
                "autoflower": False
            }
            
            create_response = await self.client.post(
                f"{self.base_url}/api/v2/plants",
                json=plant_data,
                headers=self.headers
            )
            
            if create_response.status_code == 201:
                steps_completed += 1
                plant_id = create_response.json().get("data", {}).get("id")
                
                # Step 2: Verify plant appears in mobile API
                mobile_check_response = await self.client.get(
                    f"{self.base_url}/api/v2/plants/{plant_id}",
                    headers=self.headers
                )
                
                if mobile_check_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 3: Update plant status (mobile simulation)
                    update_data = {"status_id": 2}
                    update_response = await self.client.patch(
                        f"{self.base_url}/api/v2/plants/{plant_id}",
                        json=update_data,
                        headers=self.headers
                    )
                    
                    if update_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 4: Verify sync via web API
                        sync_check_response = await self.client.get(
                            f"{self.base_url}/api/v2/plants/{plant_id}",
                            headers=self.headers
                        )
                        
                        if sync_check_response.status_code == 200:
                            plant_data = sync_check_response.json()
                            if plant_data.get("data", {}).get("status_id") == 2:
                                steps_completed += 1
                                
                                # Step 5: Add measurement via web API
                                measurement_data = {
                                    "name": "Sync Test",
                                    "value": 15.0,
                                    "unit": "cm"
                                }
                                
                                measurement_response = await self.client.post(
                                    f"{self.base_url}/api/v2/plants/{plant_id}/measurements",
                                    json=measurement_data,
                                    headers=self.headers
                                )
                                
                                if measurement_response.status_code == 201:
                                    steps_completed += 1
                                    
                                    # Step 6: Verify measurement sync
                                    measurement_check = await self.client.get(
                                        f"{self.base_url}/api/v2/plants/{plant_id}/measurements",
                                        headers=self.headers
                                    )
                                    
                                    if measurement_check.status_code == 200:
                                        steps_completed += 1
                                        success = True
                                    else:
                                        success = False
                                else:
                                    success = False
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Cross-platform sync workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Cross-Platform Sync",
            scenario_name="Web-to-Mobile Data Synchronization",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Sync completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "plant_id": plant_id if 'plant_id' in locals() else None,
                "status_updated": steps_completed > 2,
                "measurements_synced": steps_completed > 5
            }
        ))
    
    async def _test_data_export_import_workflow(self):
        """Test data export and import functionality"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 5
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Export user data
            export_response = await self.client.post(
                f"{self.base_url}/api/v2/users/export",
                json={"format": "json"},
                headers=self.headers
            )
            
            if export_response.status_code == 200:
                steps_completed += 1
                export_data = export_response.json()
                
                # Step 2: Download backup file
                if "backup_url" in export_data:
                    backup_response = await self.client.get(
                        export_data["backup_url"],
                        headers=self.headers
                    )
                    
                    if backup_response.status_code == 200:
                        steps_completed += 1
                        
                        # Step 3: Validate exported data structure
                        data_valid = "plants" in export_data and "sensors" in export_data
                        if data_valid:
                            steps_completed += 1
                            
                            # Step 4: Import data back (if supported)
                            import_response = await self.client.post(
                                f"{self.base_url}/api/v2/users/import",
                                json=export_data,
                                headers=self.headers
                            )
                            
                            if import_response.status_code in [200, 201]:
                                steps_completed += 1
                                success = True
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Data export/import workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Data Export/Import",
            scenario_name="Complete Data Backup and Restore",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Export/Import completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "export_generated": steps_completed > 0,
                "backup_downloaded": steps_completed > 1,
                "data_validated": steps_completed > 2,
                "import_successful": steps_completed > 4
            }
        ))
    
    async def _test_multi_user_workflow(self):
        """Test multi-user collaboration features"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 6
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Create shared plant
            shared_plant_data = {
                "name": "Shared Multi-User Plant",
                "description": "Testing collaboration features",
                "status_id": 1,
                "is_clone": False,
                "autoflower": False,
                "shared": True
            }
            
            plant_response = await self.client.post(
                f"{self.base_url}/api/v2/plants",
                json=shared_plant_data,
                headers=self.headers
            )
            
            if plant_response.status_code == 201:
                steps_completed += 1
                plant_id = plant_response.json().get("data", {}).get("id")
                
                # Step 2: Get plant collaborators (should include current user)
                collaborators_response = await self.client.get(
                    f"{self.base_url}/api/v2/plants/{plant_id}/collaborators",
                    headers=self.headers
                )
                
                if collaborators_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 3: Add activity log (collaboration)
                    activity_data = {
                        "activity_type": "collaboration",
                        "description": "Added activity for collaboration test",
                        "notes": "Testing multi-user workflow"
                    }
                    
                    activity_response = await self.client.post(
                        f"{self.base_url}/api/v2/plants/{plant_id}/activities",
                        json=activity_data,
                        headers=self.headers
                    )
                    
                    if activity_response.status_code == 201:
                        steps_completed += 1
                        
                        # Step 4: Add plant measurement
                        measurement_data = {
                            "name": "Collaborative Height",
                            "value": 20.0,
                            "unit": "cm"
                        }
                        
                        measurement_response = await self.client.post(
                            f"{self.base_url}/api/v2/plants/{plant_id}/measurements",
                            json=measurement_data,
                            headers=self.headers
                        )
                        
                        if measurement_response.status_code == 201:
                            steps_completed += 1
                            
                            # Step 5: Get plant history (should show all activities)
                            history_response = await self.client.get(
                                f"{self.base_url}/api/v2/plants/{plant_id}/history",
                                headers=self.headers
                            )
                            
                            if history_response.status_code == 200:
                                steps_completed += 1
                                success = True
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Multi-user workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Multi-User Collaboration",
            scenario_name="Shared Plant Management",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Collaboration completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "shared_plant_created": steps_completed > 0,
                "collaborators_checked": steps_completed > 1,
                "activities_added": steps_completed > 2,
                "history_tracked": steps_completed > 5
            }
        ))
    
    async def _test_realtime_monitoring_workflow(self):
        """Test real-time monitoring and alerts"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 5
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Create sensor with real-time alerts
            sensor_config = {
                "name": "Realtime Test Sensor",
                "sensor_type": "temperature",
                "source": "manual",
                "unit": "°F",
                "realtime_enabled": True
            }
            
            sensor_response = await self.client.post(
                f"{self.base_url}/api/v2/sensors",
                json=sensor_config,
                headers=self.headers
            )
            
            if sensor_response.status_code == 201:
                steps_completed += 1
                sensor_id = sensor_response.json().get("data", {}).get("id")
                
                # Step 2: Configure real-time alerts
                alert_config = {
                    "realtime_alerts": True,
                    "temperature_threshold": 75.0,
                    "alert_frequency": "immediate"
                }
                
                alert_response = await self.client.patch(
                    f"{self.base_url}/api/v2/sensors/{sensor_id}/alerts",
                    json=alert_config,
                    headers=self.headers
                )
                
                if alert_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 3: Send multiple real-time readings
                    readings = []
                    for i in range(3):
                        reading_data = {
                            "value": 70.0 + (i * 2),
                            "unit": "°F",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        readings.append(reading_data)
                    
                    realtime_response = await self.client.post(
                        f"{self.base_url}/api/v2/sensors/{sensor_id}/readings",
                        json={"readings": readings, "realtime": True},
                        headers=self.headers
                    )
                    
                    if realtime_response.status_code == 201:
                        steps_completed += 1
                        
                        # Step 4: Check real-time data endpoint
                        live_data_response = await self.client.get(
                            f"{self.base_url}/api/v2/sensors/{sensor_id}/live",
                            headers=self.headers
                        )
                        
                        if live_data_response.status_code == 200:
                            steps_completed += 1
                            
                            # Step 5: Verify alert history
                            alerts_response = await self.client.get(
                                f"{self.base_url}/api/v2/sensors/{sensor_id}/alerts",
                                headers=self.headers
                            )
                            
                            if alerts_response.status_code == 200:
                                steps_completed += 1
                                success = True
                            else:
                                success = False
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Real-time monitoring workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Real-Time Monitoring",
            scenario_name="Live Data and Alert System",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Monitoring completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "sensor_created": steps_completed > 0,
                "alerts_configured": steps_completed > 1,
                "realtime_data": steps_completed > 2,
                "live_monitoring": steps_completed > 3
            }
        ))
    
    async def _test_performance_workflow(self):
        """Test system performance under load"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 4
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Test concurrent plant creation
            concurrent_plants = []
            for i in range(5):
                plant_data = {
                    "name": f"Performance Test Plant {i+1}",
                    "description": "Testing concurrent operations",
                    "status_id": 1,
                    "is_clone": False,
                    "autoflower": False
                }
                
                response = await self.client.post(
                    f"{self.base_url}/api/v2/plants",
                    json=plant_data,
                    headers=self.headers
                )
                
                if response.status_code == 201:
                    plant_id = response.json().get("data", {}).get("id")
                    concurrent_plants.append(plant_id)
            
            if len(concurrent_plants) >= 3:
                steps_completed += 1
                
                # Step 2: Test concurrent sensor readings
                if self.test_sensors:
                    sensor_id = self.test_sensors[0]
                    
                    for i in range(5):
                        reading_data = {
                            "value": random.uniform(65.0, 85.0),
                            "unit": "°F",
                            "timestamp": datetime.utcnow().isoformat()
                        }
                        
                        response = await self.client.post(
                            f"{self.base_url}/api/v2/sensors/{sensor_id}/readings",
                            json=reading_data,
                            headers=self.headers
                        )
                    
                    steps_completed += 1
                
                # Step 3: Test dashboard performance
                dashboard_response = await self.client.get(
                    f"{self.base_url}/api/v2/dashboard",
                    headers=self.headers
                )
                
                if dashboard_response.status_code == 200:
                    steps_completed += 1
                    
                    # Step 4: Test analytics performance
                    analytics_response = await self.client.get(
                        f"{self.base_url}/api/v2/analytics/overview",
                        headers=self.headers
                    )
                    
                    if analytics_response.status_code == 200:
                        steps_completed += 1
                        success = True
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Performance workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Performance Under Load",
            scenario_name="Concurrent Operations and System Response",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Performance test completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "concurrent_plants": len(concurrent_plants) if 'concurrent_plants' in locals() else 0,
                "load_handled": steps_completed > 1,
                "response_time": f"{duration:.0f}ms",
                "system_stable": success
            }
        ))
    
    async def _test_error_recovery_workflow(self):
        """Test system error recovery and resilience"""
        workflow_start = time.time()
        steps_completed = 0
        total_steps = 5
        
        try:
            # Ensure authentication
            if not self.auth_tokens:
                await self._authenticate_test_user()
            
            # Step 1: Test invalid data handling
            invalid_data = {
                "name": "",
                "description": None,
                "status_id": -999,
                "invalid_field": "should_be_ignored"
            }
            
            invalid_response = await self.client.post(
                f"{self.base_url}/api/v2/plants",
                json=invalid_data,
                headers=self.headers
            )
            
            # Should return validation error, not crash
            if invalid_response.status_code in [400, 422]:
                steps_completed += 1
                
                # Step 2: Test database connectivity recovery
                # Make several requests to test connection pooling
                for i in range(3):
                    response = await self.client.get(
                        f"{self.base_url}/api/v2/dashboard",
                        headers=self.headers
                    )
                    
                    if response.status_code == 200:
                        continue
                    else:
                        break
                else:
                    steps_completed += 1
                
                # Step 3: Test graceful degradation
                # Try to access non-existent resource
                not_found_response = await self.client.get(
                    f"{self.base_url}/api/v2/plants/99999",
                    headers=self.headers
                )
                
                if not_found_response.status_code == 404:
                    steps_completed += 1
                    
                    # Step 4: Test rate limiting recovery
                    # Make requests that might trigger rate limiting
                    rate_limit_responses = []
                    for i in range(10):
                        response = await self.client.get(
                            f"{self.base_url}/api/v2/plants/stats",
                            headers=self.headers
                        )
                        rate_limit_responses.append(response.status_code)
                    
                    # Should see either 200 or 429, never server error
                    server_errors = [s for s in rate_limit_responses if 500 <= s < 600]
                    if not server_errors:
                        steps_completed += 1
                        
                        # Step 5: Verify system health after stress test
                        health_response = await self.client.get(
                            f"{self.base_url}/health",
                            headers=self.headers
                        )
                        
                        if health_response.status_code == 200:
                            steps_completed += 1
                            success = True
                        else:
                            success = False
                    else:
                        success = False
                else:
                    success = False
            else:
                success = False
                
        except Exception as e:
            self.logger.error(f"Error recovery workflow failed: {e}")
            success = False
            
        duration = (time.time() - workflow_start) * 1000
        
        self.test_results.append(E2ETestResult(
            workflow_name="Error Recovery",
            scenario_name="System Resilience and Graceful Degradation",
            passed=success and steps_completed == total_steps,
            duration_ms=duration,
            details=f"Error recovery completed {steps_completed}/{total_steps} steps",
            steps_completed=steps_completed,
            total_steps=total_steps,
            evidence={
                "validation_handled": steps_completed > 0,
                "database_recovery": steps_completed > 1,
                "graceful_degradation": steps_completed > 2,
                "rate_limiting": steps_completed > 3,
                "system_healthy": success
            }
        ))
    async def _authenticate_test_user(self):
        """Helper method to authenticate a test user"""
        username = f"e2e_test_{random.randint(1000, 9999)}"
        user_data = {
            "username": username,
            "email": f"e2e_test_{random.randint(1000, 9999)}@example.com",
            "password": "TestPassword123!"
        }
        
        # Register user
        register_response = await self.client.post(
            f"{self.base_url}/api/v2/auth/register",
            json=user_data
        )
        
        if register_response.status_code == 201:
            # Login user
            login_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/login",
                json={"username": username, "password": user_data["password"]}
            )
            
            if login_response.status_code == 200:
                tokens = login_response.json()
                self.auth_tokens = tokens
                self.headers = {
                    "Authorization": f"Bearer {tokens['access_token']}",
                    "Content-Type": "application/json"
                }
                return True
                
        return False
    
    def _generate_e2e_report(self) -> Dict[str, Any]:
        """Generate comprehensive end-to-end test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        failed_tests = total_tests - passed_tests
        
        # Calculate average performance metrics
        avg_duration = sum(result.duration_ms for result in self.test_results) / total_tests if total_tests > 0 else 0
        total_steps = sum(result.total_steps for result in self.test_results)
        completed_steps = sum(result.steps_completed for result in self.test_results)
        
        # Categorize workflows
        workflow_performance = {}
        for result in self.test_results:
            workflow = result.workflow_name
            if workflow not in workflow_performance:
                workflow_performance[workflow] = {"total": 0, "passed": 0, "avg_duration": 0}
            
            workflow_performance[workflow]["total"] += 1
            if result.passed:
                workflow_performance[workflow]["passed"] += 1
        
        for workflow in workflow_performance:
            workflow_tests = [r for r in self.test_results if r.workflow_name == workflow]
            workflow_performance[workflow]["avg_duration"] = sum(r.duration_ms for r in workflow_tests) / len(workflow_tests)
        
        report = {
            "summary": {
                "total_workflows": total_tests,
                "passed_workflows": passed_tests,
                "failed_workflows": failed_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                "average_duration_ms": round(avg_duration, 2),
                "total_test_steps": total_steps,
                "completed_steps": completed_steps,
                "completion_rate": f"{(completed_steps/total_steps*100):.1f}%" if total_steps > 0 else "0%"
            },
            "workflow_performance": workflow_performance,
            "detailed_results": [
                {
                    "workflow_name": result.workflow_name,
                    "scenario_name": result.scenario_name,
                    "passed": result.passed,
                    "duration_ms": result.duration_ms,
                    "steps_completed": result.steps_completed,
                    "total_steps": result.total_steps,
                    "completion_rate": f"{(result.steps_completed/result.total_steps*100):.1f}%" if result.total_steps > 0 else "0%",
                    "details": result.details,
                    "evidence": result.evidence,
                    "timestamp": result.timestamp
                }
                for result in self.test_results
            ],
            "recommendations": self._generate_e2e_recommendations()
        }
        
        return report
    
    def _generate_e2e_recommendations(self) -> List[str]:
        """Generate end-to-end test recommendations"""
        recommendations = []
        
        failed_workflows = [r for r in self.test_results if not r.passed]
        
        if failed_workflows:
            recommendations.append("🚨 CRITICAL: Fix failed end-to-end workflows before production deployment")
            
            # Categorize failures
            critical_failures = [r for r in failed_workflows if r.steps_completed < r.total_steps * 0.5]
            partial_failures = [r for r in failed_workflows if r.steps_completed >= r.total_steps * 0.5]
            
            if critical_failures:
                recommendations.append("⚠️ HIGH: Address critical workflow failures (less than 50% completion)")
            
            if partial_failures:
                recommendations.append("📋 MEDIUM: Investigate partial workflow failures and missing features")
        
        # Performance recommendations
        slow_workflows = [r for r in self.test_results if r.duration_ms > 10000]  # > 10 seconds
        if slow_workflows:
            recommendations.append("⏱️ PERFORMANCE: Optimize slow workflows (>10s duration)")
        
        # Feature completeness recommendations
        onboarding_failed = any(r.workflow_name == "Complete User Onboarding" and not r.passed for r in failed_workflows)
        if onboarding_failed:
            recommendations.append("👥 USER EXPERIENCE: Fix user onboarding flow - critical for new users")
        
        sensor_failed = any(r.workflow_name == "Sensor Integration" and not r.passed for r in failed_workflows)
        if sensor_failed:
            recommendations.append("📡 IoT: Complete sensor integration implementation")
        
        # Success recommendations
        if not failed_workflows:
            recommendations.append("✅ All end-to-end workflows passing! System ready for user acceptance testing.")
            recommendations.append("🚀 Proceed with production deployment preparation")
        
        # Automation recommendations
        recommendations.append("🤖 Set up automated E2E testing in CI/CD pipeline")
        recommendations.append("📊 Monitor E2E test performance and success rates in production")
        
        return recommendations

# CLI interface for running E2E tests
async def main():
    """CLI interface for end-to-end validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR End-to-End Validation Suite")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the application")
    parser.add_argument("--output", help="Output file for E2E report (JSON)")
    parser.add_argument("--workflow", help="Specific workflow to test")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    async with CultivarE2EValidator(base_url=args.url) as validator:
        print(f"🔄 CultivAR End-to-End Validation Suite")
        print(f"📍 Testing application at: {args.url}")
        print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
        print("-" * 60)
        
        if args.workflow:
            # Run specific workflow
            workflow_map = {
                "onboarding": validator._test_user_onboarding_workflow,
                "plant_lifecycle": validator._test_plant_lifecycle_workflow,
                "sensor": validator._test_sensor_integration_workflow,
                "dashboard": validator._test_dashboard_analytics_workflow,
            }
            
            if args.workflow.lower() in workflow_map:
                print(f"🎯 Running specific workflow: {args.workflow}")
                await workflow_map[args.workflow.lower()]()
            else:
                print(f"❌ Unknown workflow: {args.workflow}")
                return
        else:
            # Run all workflows
            report = await validator.run_all_e2e_tests()
        
        # Display summary
        if 'report' in locals():
            summary = report["summary"]
            print(f"\n📊 E2E Test Summary:")
            print(f"   Total Workflows: {summary['total_workflows']}")
            print(f"   Passed: {summary['passed_workflows']} ✅")
            print(f"   Failed: {summary['failed_workflows']} ❌")
            print(f"   Success Rate: {summary['success_rate']}")
            print(f"   Average Duration: {summary['average_duration_ms']}ms")
            print(f"   Step Completion: {summary['completion_rate']}")
            
            # Display workflow performance
            print(f"\n🎯 Workflow Performance:")
            for workflow, stats in report["workflow_performance"].items():
                success_rate = f"{(stats['passed']/stats['total']*100):.1f}%"
                print(f"   {workflow}: {stats['passed']}/{stats['total']} ({success_rate}) - {stats['avg_duration']:.0f}ms avg")
            
            # Display failed workflows
            failed_workflows = [r for r in report["detailed_results"] if not r["passed"]]
            if failed_workflows:
                print(f"\n❌ Failed E2E Workflows ({len(failed_workflows)}):")
                for workflow in failed_workflows:
                    print(f"   - {workflow['workflow_name']}: {workflow['completion_rate']} complete - {workflow['details']}")
            
            # Display recommendations
            print(f"\n💡 E2E Recommendations:")
            for rec in report["recommendations"]:
                print(f"   {rec}")
            
            # Save report if requested
            if args.output:
                import json
                with open(args.output, 'w') as f:
                    json.dump(report, f, indent=2)
                print(f"\n📄 Detailed E2E report saved to: {args.output}")
        
        return report if 'report' in locals() else None

if __name__ == "__main__":
    asyncio.run(main())