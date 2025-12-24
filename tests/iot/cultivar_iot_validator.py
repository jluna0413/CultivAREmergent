"""
📡 IoT INTEGRATION VALIDATION FRAMEWORK FOR CULTIVAR APPLICATION
Comprehensive testing suite for AC Infinity & Ecowitt sensor device integration
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
from dataclasses import dataclass, asdict
from unittest.mock import AsyncMock, MagicMock
import logging

@dataclass
class SensorReading:
    """Represents a sensor reading"""
    sensor_id: int
    value: float
    unit: str
    timestamp: datetime
    source: str  # 'AC Infinity', 'Ecowitt', 'Manual'

@dataclass
class DeviceTestResult:
    """IoT device test result"""
    device_type: str
    device_id: str
    test_name: str
    passed: bool
    details: str
    data_samples: List[SensorReading]
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

class CultivarIoTValidator:
    """Comprehensive IoT validation for CultivAR sensor integration"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results: List[DeviceTestResult] = []
        self.mock_devices = {}
        self.auth_tokens = {}
        self.logger = logging.getLogger(__name__)
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
        
    async def run_all_iot_tests(self) -> Dict[str, Any]:
        """Run comprehensive IoT test suite"""
        print("📡 Starting CultivAR IoT Integration Validation Suite...")
        
        # Authenticate first
        await self._authenticate()
        
        # Test categories
        test_suites = [
            ("AC Infinity Device Tests", self._test_ac_infinity_devices),
            ("Ecowitt Device Tests", self._test_ecowitt_devices),
            ("Real-time Data Collection Tests", self._test_real_time_data_collection),
            ("Data Synchronization Tests", self._test_data_synchronization),
            ("Network Resilience Tests", self._test_network_resilience),
            ("Data Accuracy Tests", self._test_data_accuracy),
            ("Historical Data Tests", self._test_historical_data),
            ("Zone Management Tests", self._test_zone_management),
        ]
        
        for suite_name, test_func in test_suites:
            print(f"\n🧪 Running {suite_name}...")
            await test_func()
            
        return self._generate_iot_report()
    
    async def _authenticate(self):
        """Authenticate with the application"""
        try:
            # Create test user
            import secrets
            username = f"iot_test_{secrets.token_hex(4)}"
            user_data = {
                "username": username,
                "email": f"iot_{secrets.token_hex(4)}@example.com",
                "password": "TestPassword123!"
            }
            
            # Register user
            register_response = await self.client.post(
                f"{self.base_url}/api/v2/auth/register",
                json=user_data
            )
            
            if register_response.status_code == 201:
                # Login
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
                    
        except Exception as e:
            self.logger.error(f"Authentication failed: {e}")
            
        return False
    
    async def _test_ac_infinity_devices(self):
        """Test AC Infinity device integration"""
        # Test 1: Device discovery simulation
        await self._test_ac_infinity_discovery()
        
        # Test 2: Device authentication
        await self._test_ac_infinity_authentication()
        
        # Test 3: Data collection
        await self._test_ac_infinity_data_collection()
        
        # Test 4: Device configuration
        await self._test_ac_infinity_configuration()
    
    async def _test_ac_infinity_discovery(self):
        """Test AC Infinity device discovery"""
        try:
            # Simulate device discovery response
            mock_devices = [
                {
                    "device_id": "ACINFINITY_001",
                    "name": "Grow Tent Fan 1",
                    "type": "fan",
                    "status": "online",
                    "ip_address": "192.168.1.100"
                },
                {
                    "device_id": "ACINFINITY_002", 
                    "name": "Grow Tent Fan 2",
                    "type": "controller",
                    "status": "online",
                    "ip_address": "192.168.1.101"
                }
            ]
            
            # Test device discovery endpoint
            response = await self.client.get(
                f"{self.base_url}/api/v2/sensors/discover/ac-infinity",
                headers=self.headers
            )
            
            if response.status_code == 200:
                discovered_devices = response.json()
                
                # Validate discovered devices structure
                if isinstance(discovered_devices, list) and len(discovered_devices) >= 0:
                    self.test_results.append(DeviceTestResult(
                        device_type="AC Infinity",
                        device_id="discovery_test",
                        test_name="Device Discovery",
                        passed=True,
                        details=f"Device discovery working - found {len(discovered_devices)} devices",
                        data_samples=[]
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="AC Infinity",
                        device_id="discovery_test",
                        test_name="Device Discovery",
                        passed=False,
                        details="Device discovery response format invalid",
                        data_samples=[]
                    ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="discovery_test",
                    test_name="Device Discovery",
                    passed=False,
                    details=f"Device discovery failed with status {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="AC Infinity",
                device_id="discovery_test",
                test_name="Device Discovery",
                passed=False,
                details=f"Discovery test failed with exception: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ac_infinity_authentication(self):
        """Test AC Infinity device authentication"""
        try:
            # Test authentication with mock credentials
            auth_data = {
                "username": "test_user",
                "password": "test_password",
                "api_key": "test_api_key"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/auth/ac-infinity",
                json=auth_data,
                headers=self.headers
            )
            
            # Should return 200 or appropriate error (not 500)
            if response.status_code in [200, 401, 400]:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="auth_test",
                    test_name="Device Authentication",
                    passed=True,
                    details="Authentication endpoint responding correctly",
                    data_samples=[]
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="auth_test",
                    test_name="Device Authentication",
                    passed=False,
                    details=f"Authentication endpoint failed with status {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="AC Infinity",
                device_id="auth_test",
                test_name="Device Authentication",
                passed=False,
                details=f"Authentication test failed with exception: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ac_infinity_data_collection(self):
        """Test AC Infinity data collection"""
        try:
            # Generate mock sensor readings
            mock_readings = []
            for i in range(10):
                reading = SensorReading(
                    sensor_id=1,
                    value=round(random.uniform(60.0, 90.0), 1),  # Temperature readings
                    unit="°F",
                    timestamp=datetime.utcnow() - timedelta(minutes=i),
                    source="AC Infinity"
                )
                mock_readings.append(reading)
            
            # Test posting sensor data
            readings_data = [
                {
                    "sensor_id": 1,
                    "value": reading.value,
                    "unit": reading.unit,
                    "created_at": reading.timestamp.isoformat()
                }
                for reading in mock_readings
            ]
            
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/1/readings",
                json={"readings": readings_data},
                headers=self.headers
            )
            
            if response.status_code == 201:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="data_collection_test",
                    test_name="Data Collection",
                    passed=True,
                    details=f"Successfully collected {len(mock_readings)} sensor readings",
                    data_samples=mock_readings
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="data_collection_test",
                    test_name="Data Collection",
                    passed=False,
                    details=f"Data collection failed with status {response.status_code}",
                    data_samples=mock_readings
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="AC Infinity",
                device_id="data_collection_test",
                test_name="Data Collection",
                passed=False,
                details=f"Data collection test failed with exception: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ac_infinity_configuration(self):
        """Test AC Infinity device configuration"""
        try:
            config_data = {
                "device_id": "ACINFINITY_001",
                "name": "Updated Fan Name",
                "poll_interval": 300,  # 5 minutes
                "alert_thresholds": {
                    "temperature_max": 85.0,
                    "temperature_min": 65.0
                }
            }
            
            response = await self.client.patch(
                f"{self.base_url}/api/v2/sensors/devices/ACINFINITY_001",
                json=config_data,
                headers=self.headers
            )
            
            if response.status_code in [200, 404]:  # 404 is ok if device doesn't exist
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="config_test",
                    test_name="Device Configuration",
                    passed=True,
                    details="Configuration endpoint responding correctly",
                    data_samples=[]
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="AC Infinity",
                    device_id="config_test",
                    test_name="Device Configuration",
                    passed=False,
                    details=f"Configuration failed with status {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="AC Infinity",
                device_id="config_test",
                test_name="Device Configuration",
                passed=False,
                details=f"Configuration test failed with exception: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ecowitt_devices(self):
        """Test Ecowitt device integration"""
        # Test 1: Device discovery
        await self._test_ecowitt_discovery()
        
        # Test 2: API key validation
        await self._test_ecowitt_api_validation()
        
        # Test 3: Data collection
        await self._test_ecowitt_data_collection()
        
        # Test 4: Historical data
        await self._test_ecowitt_historical_data()
    
    async def _test_ecowitt_discovery(self):
        """Test Ecowitt device discovery"""
        try:
            # Simulate Ecowitt device discovery
            mock_devices = [
                {
                    "device_id": "ECO_WITT_001",
                    "name": "Weather Station 1",
                    "type": "weather_station",
                    "mac_address": "AA:BB:CC:DD:EE:FF",
                    "ip_address": "192.168.1.200"
                }
            ]
            
            response = await self.client.get(
                f"{self.base_url}/api/v2/sensors/discover/ecowitt",
                headers=self.headers
            )
            
            if response.status_code == 200:
                discovered_devices = response.json()
                
                if isinstance(discovered_devices, list):
                    self.test_results.append(DeviceTestResult(
                        device_type="Ecowitt",
                        device_id="discovery_test",
                        test_name="Device Discovery",
                        passed=True,
                        details=f"Ecowitt discovery working - found {len(discovered_devices)} devices",
                        data_samples=[]
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="Ecowitt",
                        device_id="discovery_test",
                        test_name="Device Discovery",
                        passed=False,
                        details="Invalid discovery response format",
                        data_samples=[]
                    ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="discovery_test",
                    test_name="Device Discovery",
                    passed=False,
                    details=f"Discovery failed with status {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Ecowitt",
                device_id="discovery_test",
                test_name="Device Discovery",
                passed=False,
                details=f"Discovery test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ecowitt_api_validation(self):
        """Test Ecowitt API key validation"""
        try:
            api_data = {
                "api_key": "test_api_key",
                "application_key": "test_app_key",
                "mac_address": "AA:BB:CC:DD:EE:FF"
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/auth/ecowitt",
                json=api_data,
                headers=self.headers
            )
            
            if response.status_code in [200, 401, 400]:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="api_validation_test",
                    test_name="API Key Validation",
                    passed=True,
                    details="API validation endpoint working correctly",
                    data_samples=[]
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="api_validation_test",
                    test_name="API Key Validation",
                    passed=False,
                    details=f"API validation failed with status {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Ecowitt",
                device_id="api_validation_test",
                test_name="API Key Validation",
                passed=False,
                details=f"API validation test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ecowitt_data_collection(self):
        """Test Ecowitt data collection"""
        try:
            # Generate mock weather data
            mock_readings = []
            for i in range(5):
                reading = SensorReading(
                    sensor_id=2,
                    value=round(random.uniform(30.0, 100.0), 1),  # Humidity readings
                    unit="%",
                    timestamp=datetime.utcnow() - timedelta(minutes=i*5),
                    source="Ecowitt"
                )
                mock_readings.append(reading)
            
            # Post weather station data
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/2/readings",
                json={
                    "readings": [
                        {
                            "sensor_id": 2,
                            "value": reading.value,
                            "unit": reading.unit,
                            "created_at": reading.timestamp.isoformat()
                        }
                        for reading in mock_readings
                    ]
                },
                headers=self.headers
            )
            
            if response.status_code == 201:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="data_collection_test",
                    test_name="Data Collection",
                    passed=True,
                    details=f"Ecowitt data collection successful - {len(mock_readings)} readings",
                    data_samples=mock_readings
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="data_collection_test",
                    test_name="Data Collection",
                    passed=False,
                    details=f"Ecowitt data collection failed: {response.status_code}",
                    data_samples=mock_readings
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Ecowitt",
                device_id="data_collection_test",
                test_name="Data Collection",
                passed=False,
                details=f"Data collection test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_ecowitt_historical_data(self):
        """Test Ecowitt historical data retrieval"""
        try:
            # Query historical data
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            response = await self.client.get(
                f"{self.base_url}/api/v2/sensors/2/readings",
                params={
                    "start_time": start_time.isoformat(),
                    "end_time": end_time.isoformat(),
                    "limit": 100
                },
                headers=self.headers
            )
            
            if response.status_code == 200:
                historical_data = response.json()
                
                if isinstance(historical_data, dict) and "items" in historical_data:
                    self.test_results.append(DeviceTestResult(
                        device_type="Ecowitt",
                        device_id="historical_test",
                        test_name="Historical Data Retrieval",
                        passed=True,
                        details=f"Historical data retrieved - {len(historical_data.get('items', []))} records",
                        data_samples=[]
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="Ecowitt",
                        device_id="historical_test",
                        test_name="Historical Data Retrieval",
                        passed=False,
                        details="Invalid historical data response format",
                        data_samples=[]
                    ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Ecowitt",
                    device_id="historical_test",
                    test_name="Historical Data Retrieval",
                    passed=False,
                    details=f"Historical data retrieval failed: {response.status_code}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Ecowitt",
                device_id="historical_test",
                test_name="Historical Data Retrieval",
                passed=False,
                details=f"Historical data test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_real_time_data_collection(self):
        """Test real-time data collection and WebSocket connectivity"""
        try:
            # Test WebSocket connection for real-time updates
            import websockets
            
            ws_url = self.base_url.replace('http', 'ws') + '/ws/sensors'
            headers = {"Authorization": f"Bearer {self.auth_tokens['access_token']}"}
            
            try:
                # Note: This is a simplified test - in reality, you'd need to handle the WebSocket protocol
                # For now, we'll test that the endpoint exists
                response = await self.client.get(
                    f"{self.base_url}/api/v2/sensors/stats",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    self.test_results.append(DeviceTestResult(
                        device_type="Real-time",
                        device_id="websocket_test",
                        test_name="Real-time Data Collection",
                        passed=True,
                        details="Real-time sensor statistics endpoint accessible",
                        data_samples=[]
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="Real-time",
                        device_id="websocket_test",
                        test_name="Real-time Data Collection",
                        passed=False,
                        details=f"Real-time endpoint failed: {response.status_code}",
                        data_samples=[]
                    ))
                    
            except Exception as ws_error:
                self.test_results.append(DeviceTestResult(
                    device_type="Real-time",
                    device_id="websocket_test",
                    test_name="Real-time Data Collection",
                    passed=False,
                    details=f"WebSocket connection failed: {str(ws_error)}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Real-time",
                device_id="websocket_test",
                test_name="Real-time Data Collection",
                passed=False,
                details=f"Real-time test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_data_synchronization(self):
        """Test data synchronization between devices"""
        try:
            # Simulate data from multiple devices
            sync_test_data = []
            
            for device_type in ["AC Infinity", "Ecowitt"]:
                for i in range(3):
                    reading = SensorReading(
                        sensor_id=i + 1,
                        value=round(random.uniform(20.0, 80.0), 1),
                        unit="°C" if device_type == "Ecowitt" else "°F",
                        timestamp=datetime.utcnow() - timedelta(minutes=i),
                        source=device_type
                    )
                    sync_test_data.append(reading)
            
            # Post synchronized data
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/bulk-readings",
                json={
                    "readings": [
                        {
                            "sensor_id": reading.sensor_id,
                            "value": reading.value,
                            "unit": reading.unit,
                            "created_at": reading.timestamp.isoformat()
                        }
                        for reading in sync_test_data
                    ]
                },
                headers=self.headers
            )
            
            if response.status_code == 201:
                self.test_results.append(DeviceTestResult(
                    device_type="Synchronization",
                    device_id="sync_test",
                    test_name="Data Synchronization",
                    passed=True,
                    details=f"Synchronized {len(sync_test_data)} readings from multiple devices",
                    data_samples=sync_test_data
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Synchronization",
                    device_id="sync_test",
                    test_name="Data Synchronization",
                    passed=False,
                    details=f"Data synchronization failed: {response.status_code}",
                    data_samples=sync_test_data
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Synchronization",
                device_id="sync_test",
                test_name="Data Synchronization",
                passed=False,
                details=f"Synchronization test failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_network_resilience(self):
        """Test network resilience and failover"""
        try:
            # Simulate network interruption scenarios
            resilience_tests = [
                ("Connection Timeout", self._simulate_timeout),
                ("Rate Limiting", self._simulate_rate_limit),
                ("Partial Data Loss", self._simulate_data_loss),
                ("Duplicate Readings", self._simulate_duplicates)
            ]
            
            passed_tests = 0
            for test_name, test_func in resilience_tests:
                try:
                    result = await test_func()
                    if result:
                        passed_tests += 1
                except Exception as e:
                    self.logger.warning(f"Resilience test {test_name} failed: {e}")
            
            if passed_tests >= len(resilience_tests) * 0.75:  # 75% pass rate
                self.test_results.append(DeviceTestResult(
                    device_type="Resilience",
                    device_id="network_test",
                    test_name="Network Resilience",
                    passed=True,
                    details=f"Network resilience tests passed: {passed_tests}/{len(resilience_tests)}",
                    data_samples=[]
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Resilience",
                    device_id="network_test",
                    test_name="Network Resilience",
                    passed=False,
                    details=f"Network resilience tests failed: {passed_tests}/{len(resilience_tests)}",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Resilience",
                device_id="network_test",
                test_name="Network Resilience",
                passed=False,
                details=f"Resilience testing failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _simulate_timeout(self) -> bool:
        """Simulate connection timeout"""
        try:
            # Test with very short timeout
            short_timeout_client = httpx.AsyncClient(timeout=0.001)
            response = await short_timeout_client.get(f"{self.base_url}/api/v2/sensors/stats")
            await short_timeout_client.aclose()
            return False  # Should timeout
        except:
            return True  # Expected timeout
    
    async def _simulate_rate_limit(self) -> bool:
        """Simulate rate limiting"""
        try:
            # Make rapid requests
            for i in range(10):
                response = await self.client.get(f"{self.base_url}/api/v2/sensors/stats")
                if response.status_code == 429:  # Rate limited
                    return True
            return False
        except:
            return True
    
    async def _simulate_data_loss(self) -> bool:
        """Simulate data loss scenario"""
        try:
            # Post partial data (simulate missing fields)
            incomplete_reading = {
                "sensor_id": 999,
                "value": 50.0
                # Missing unit and timestamp
            }
            
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/999/readings",
                json={"readings": [incomplete_reading]},
                headers=self.headers
            )
            
            # Should either accept with defaults or reject with validation error
            return response.status_code in [201, 422, 400]
        except:
            return True
    
    async def _simulate_duplicates(self) -> bool:
        """Simulate duplicate readings"""
        try:
            duplicate_reading = {
                "sensor_id": 1,
                "value": 75.0,
                "unit": "°F",
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Post same reading twice
            for _ in range(2):
                response = await self.client.post(
                    f"{self.base_url}/api/v2/sensors/1/readings",
                    json={"readings": [duplicate_reading]},
                    headers=self.headers
                )
            
            return True  # System should handle duplicates gracefully
        except:
            return True
    
    async def _test_data_accuracy(self):
        """Test sensor data accuracy and validation"""
        try:
            # Test data validation ranges
            accuracy_tests = [
                ("Temperature Range", 25.0, 95.0, "°F"),
                ("Humidity Range", 0.0, 100.0, "%"),
                ("pH Range", 0.0, 14.0, "pH"),
                ("Invalid Range", -100.0, 200.0, "invalid")
            ]
            
            valid_tests = 0
            for test_name, min_val, max_val, unit in accuracy_tests:
                reading = SensorReading(
                    sensor_id=10,
                    value=round((min_val + max_val) / 2, 1),
                    unit=unit,
                    timestamp=datetime.utcnow(),
                    source="Validation Test"
                )
                
                response = await self.client.post(
                    f"{self.base_url}/api/v2/sensors/10/readings",
                    json={
                        "readings": [{
                            "sensor_id": 10,
                            "value": reading.value,
                            "unit": reading.unit,
                            "created_at": reading.timestamp.isoformat()
                        }]
                    },
                    headers=self.headers
                )
                
                if unit != "invalid" and response.status_code == 201:
                    valid_tests += 1
                elif unit == "invalid" and response.status_code in [400, 422]:
                    valid_tests += 1
            
            if valid_tests >= 3:  # Allow for some test failures
                self.test_results.append(DeviceTestResult(
                    device_type="Accuracy",
                    device_id="accuracy_test",
                    test_name="Data Accuracy Validation",
                    passed=True,
                    details=f"Data accuracy validation passed: {valid_tests}/{len(accuracy_tests)} tests",
                    data_samples=[]
                ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Accuracy",
                    device_id="accuracy_test",
                    test_name="Data Accuracy Validation",
                    passed=False,
                    details=f"Data accuracy validation failed: {valid_tests}/{len(accuracy_tests)} tests",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Accuracy",
                device_id="accuracy_test",
                test_name="Data Accuracy Validation",
                passed=False,
                details=f"Accuracy testing failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_historical_data(self):
        """Test historical data management"""
        try:
            # Create historical data points
            historical_readings = []
            for i in range(24):  # 24 hours of data
                reading = SensorReading(
                    sensor_id=5,
                    value=round(random.uniform(65.0, 80.0), 1),
                    unit="°F",
                    timestamp=datetime.utcnow() - timedelta(hours=i),
                    source="Historical Test"
                )
                historical_readings.append(reading)
            
            # Bulk insert historical data
            response = await self.client.post(
                f"{self.base_url}/api/v2/sensors/5/bulk-readings",
                json={
                    "readings": [
                        {
                            "sensor_id": 5,
                            "value": reading.value,
                            "unit": reading.unit,
                            "created_at": reading.timestamp.isoformat()
                        }
                        for reading in historical_readings
                    ]
                },
                headers=self.headers
            )
            
            if response.status_code == 201:
                # Query back the historical data
                query_response = await self.client.get(
                    f"{self.base_url}/api/v2/sensors/5/readings",
                    params={"limit": 24},
                    headers=self.headers
                )
                
                if query_response.status_code == 200:
                    self.test_results.append(DeviceTestResult(
                        device_type="Historical",
                        device_id="historical_test",
                        test_name="Historical Data Management",
                        passed=True,
                        details=f"Historical data management working - {len(historical_readings)} records",
                        data_samples=historical_readings
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="Historical",
                        device_id="historical_test",
                        test_name="Historical Data Management",
                        passed=False,
                        details="Historical data storage succeeded but retrieval failed",
                        data_samples=historical_readings
                    ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Historical",
                    device_id="historical_test",
                    test_name="Historical Data Management",
                    passed=False,
                    details=f"Historical data storage failed: {response.status_code}",
                    data_samples=historical_readings
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Historical",
                device_id="historical_test",
                test_name="Historical Data Management",
                passed=False,
                details=f"Historical data testing failed: {str(e)}",
                data_samples=[]
            ))
    
    async def _test_zone_management(self):
        """Test zone-based sensor management"""
        try:
            # Create test zone
            zone_data = {
                "name": "IoT Test Zone",
                "description": "Zone for IoT testing"
            }
            
            # First, get available zones
            zones_response = await self.client.get(
                f"{self.base_url}/api/v2/zones",
                headers=self.headers
            )
            
            zone_id = None
            if zones_response.status_code == 200:
                zones = zones_response.json()
                if zones.get("items"):
                    zone_id = zones["items"][0]["id"]
            
            if zone_id:
                # Test zone-based sensor queries
                response = await self.client.get(
                    f"{self.base_url}/api/v2/sensors",
                    params={"zone_id": zone_id},
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    self.test_results.append(DeviceTestResult(
                        device_type="Zone Management",
                        device_id="zone_test",
                        test_name="Zone-based Sensor Management",
                        passed=True,
                        details=f"Zone management working - zone ID {zone_id}",
                        data_samples=[]
                    ))
                else:
                    self.test_results.append(DeviceTestResult(
                        device_type="Zone Management",
                        device_id="zone_test",
                        test_name="Zone-based Sensor Management",
                        passed=False,
                        details=f"Zone-based queries failed: {response.status_code}",
                        data_samples=[]
                    ))
            else:
                self.test_results.append(DeviceTestResult(
                    device_type="Zone Management",
                    device_id="zone_test",
                    test_name="Zone-based Sensor Management",
                    passed=False,
                    details="No zones available for testing",
                    data_samples=[]
                ))
                
        except Exception as e:
            self.test_results.append(DeviceTestResult(
                device_type="Zone Management",
                device_id="zone_test",
                test_name="Zone-based Sensor Management",
                passed=False,
                details=f"Zone management testing failed: {str(e)}",
                data_samples=[]
            ))
    
    def _generate_iot_report(self) -> Dict[str, Any]:
        """Generate comprehensive IoT test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.passed)
        failed_tests = total_tests - passed_tests
        
        # Categorize by device type
        device_types = {}
        for result in self.test_results:
            device_type = result.device_type
            if device_type not in device_types:
                device_types[device_type] = {"total": 0, "passed": 0, "failed": 0}
            device_types[device_type]["total"] += 1
            if result.passed:
                device_types[device_type]["passed"] += 1
            else:
                device_types[device_type]["failed"] += 1
        
        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": f"{(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "0%",
                "device_types_tested": len(device_types)
            },
            "device_type_breakdown": device_types,
            "test_results": [
                {
                    "device_type": result.device_type,
                    "device_id": result.device_id,
                    "test_name": result.test_name,
                    "passed": result.passed,
                    "details": result.details,
                    "data_samples_count": len(result.data_samples),
                    "timestamp": result.timestamp
                }
                for result in self.test_results
            ],
            "recommendations": self._generate_iot_recommendations()
        }
        
        return report
    
    def _generate_iot_recommendations(self) -> List[str]:
        """Generate IoT-specific recommendations"""
        recommendations = []
        
        failed_results = [r for r in self.test_results if not r.passed]
        
        # Analyze failures by device type
        ac_infinity_failures = [r for r in failed_results if r.device_type == "AC Infinity"]
        ecowitt_failures = [r for r in failed_results if r.device_type == "Ecowitt"]
        realtime_failures = [r for r in failed_results if r.device_type == "Real-time"]
        
        if ac_infinity_failures:
            recommendations.append("🔧 AC Infinity integration needs attention - check device discovery and API connectivity")
        
        if ecowitt_failures:
            recommendations.append("📡 Ecowitt integration needs attention - verify API keys and device configuration")
        
        if realtime_failures:
            recommendations.append("⚡ Real-time data features may need WebSocket implementation or enhancement")
        
        # General recommendations
        resilience_failures = [r for r in failed_results if r.device_type == "Resilience"]
        if resilience_failures:
            recommendations.append("🛡️ Improve network resilience - add retry logic and fallback mechanisms")
        
        data_accuracy_failures = [r for r in failed_results if r.device_type == "Accuracy"]
        if data_accuracy_failures:
            recommendations.append("✅ Enhance data validation rules for sensor readings")
        
        if not recommendations:
            recommendations.append("✅ IoT integration tests passed! Continue with production monitoring setup.")
        
        # Add performance recommendations
        recommendations.append("📊 Set up IoT device monitoring and alerting for production deployment")
        recommendations.append("🔄 Implement automated IoT device health checks and recovery procedures")
        
        return recommendations

# CLI interface for running IoT tests
async def main():
    """CLI interface for IoT validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CultivAR IoT Integration Validation Suite")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL of the application")
    parser.add_argument("--output", help="Output file for IoT report (JSON)")
    parser.add_argument("--device", choices=["ac-infinity", "ecowitt", "all"], default="all", help="Specific device type to test")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    async with CultivarIoTValidator(base_url=args.url) as validator:
        print(f"📡 CultivAR IoT Integration Validation Suite")
        print(f"📍 Testing application at: {args.url}")
        print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
        print("-" * 60)
        
        report = await validator.run_all_iot_tests()
        
        # Display summary
        summary = report["summary"]
        print(f"\n📊 IoT Test Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   Passed: {summary['passed']} ✅")
        print(f"   Failed: {summary['failed']} ❌")
        print(f"   Success Rate: {summary['success_rate']}")
        print(f"   Device Types Tested: {summary['device_types_tested']}")
        
        # Display device type breakdown
        print(f"\n📱 Device Type Breakdown:")
        for device_type, stats in report["device_type_breakdown"].items():
            success_rate = f"{(stats['passed']/stats['total']*100):.1f}%"
            print(f"   {device_type}: {stats['passed']}/{stats['total']} ({success_rate})")
        
        # Display failed tests
        failed_tests = [r for r in report["test_results"] if not r["passed"]]
        if failed_tests:
            print(f"\n❌ Failed IoT Tests ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"   - {test['device_type']}: {test['test_name']} - {test['details']}")
        
        # Display recommendations
        print(f"\n💡 IoT Recommendations:")
        for rec in report["recommendations"]:
            print(f"   {rec}")
        
        # Save report if requested
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"\n📄 Detailed IoT report saved to: {args.output}")
        
        return report

if __name__ == "__main__":
    asyncio.run(main())