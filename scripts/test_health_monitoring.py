#!/usr/bin/env python3
"""
Test script for FastAPI health monitoring and operational checks
Tests all health endpoints, observability features, and monitoring functionality
"""

import asyncio
import aiohttp
import json
import time
import sys
import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthMonitoringTester:
    """Test suite for FastAPI health monitoring functionality"""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.health_url = f"{base_url}/health"
        self.test_results = []
    
    async def test_all_health_endpoints(self) -> Dict[str, Any]:
        """Test all health check endpoints"""
        logger.info("Testing health check endpoints...")
        
        tests = [
            ("Main health check", "/"),
            ("Liveness probe", "/live"),
            ("Readiness probe", "/ready"),
            ("System status", "/status"),
            ("Application metrics", "/metrics"),
            ("Dependency health", "/dependencies"),
            ("Alert configuration", "/health/alert")
        ]
        
        results = {}
        
        async with aiohttp.ClientSession() as session:
            for test_name, endpoint in tests:
                try:
                    url = f"{self.health_url}{endpoint}"
                    start_time = time.time()
                    
                    async with session.get(url) as response:
                        response_time = time.time() - start_time
                        response_data = await response.json()
                        
                        results[test_name] = {
                            "status_code": response.status,
                            "response_time": response_time,
                            "success": response.status < 400,
                            "data": response_data
                        }
                        
                        logger.info(f"✓ {test_name}: {response.status} ({response_time:.3f}s)")
                        
                except Exception as e:
                    results[test_name] = {
                        "error": str(e),
                        "success": False
                    }
                    logger.error(f"✗ {test_name}: {str(e)}")
        
        return results
    
    async def test_monitoring_middleware(self) -> Dict[str, Any]:
        """Test request logging and monitoring middleware"""
        logger.info("Testing monitoring middleware...")
        
        async with aiohttp.ClientSession() as session:
            # Test various endpoints to trigger monitoring
            test_endpoints = [
                ("/api/v1/plants", "GET"),
                ("/api/v1/users/me", "GET"),
                ("/health/status", "GET")
            ]
            
            results = {}
            
            for endpoint, method in test_endpoints:
                try:
                    url = f"{self.base_url}{endpoint}"
                    start_time = time.time()
                    
                    async with session.request(method, url) as response:
                        response_time = time.time() - start_time
                        
                        # Check for monitoring headers
                        request_id = response.headers.get("X-Request-ID")
                        response_time_header = response.headers.get("X-Response-Time")
                        
                        results[endpoint] = {
                            "status_code": response.status,
                            "response_time": response_time,
                            "has_request_id": bool(request_id),
                            "has_response_time": bool(response_time_header),
                            "request_id": request_id,
                            "response_time_header": response_time_header
                        }
                        
                        logger.info(f"✓ {endpoint}: {response.status} - Request ID: {request_id}")
                        
                except Exception as e:
                    results[endpoint] = {
                        "error": str(e),
                        "success": False
                    }
                    logger.error(f"✗ {endpoint}: {str(e)}")
        
        return results
    
    async def test_metrics_collection(self) -> Dict[str, Any]:
        """Test metrics collection and export"""
        logger.info("Testing metrics collection...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # First, make some requests to generate metrics
                for i in range(5):
                    async with session.get(f"{self.base_url}/health") as response:
                        await response.json()
                
                # Get metrics
                async with session.get(f"{self.base_url}/health/metrics") as response:
                    metrics_data = await response.json()
                    
                    # Validate metrics structure
                    required_keys = ["timestamp", "application_metrics", "system_metrics"]
                    has_required_keys = all(key in metrics_data for key in required_keys)
                    
                    # Check application metrics
                    app_metrics = metrics_data.get("application_metrics", {})
                    required_app_metrics = ["uptime_seconds", "total_requests", "average_response_time", "error_rate_percent"]
                    has_app_metrics = all(key in app_metrics for key in required_app_metrics)
                    
                    # Check system metrics
                    sys_metrics = metrics_data.get("system_metrics", {})
                    required_sys_metrics = ["cpu_percent", "memory_percent", "disk_usage_percent"]
                    has_sys_metrics = all(key in sys_metrics for key in required_sys_metrics)
                    
                    return {
                        "metrics_available": bool(metrics_data),
                        "has_required_structure": has_required_keys,
                        "application_metrics_complete": has_app_metrics,
                        "system_metrics_complete": has_sys_metrics,
                        "total_requests_recorded": app_metrics.get("total_requests", 0),
                        "data": metrics_data
                    }
                    
        except Exception as e:
            logger.error(f"Metrics test failed: {str(e)}")
            return {
                "error": str(e),
                "success": False
            }
    
    async def test_health_status_codes(self) -> Dict[str, Any]:
        """Test that health endpoints return appropriate status codes"""
        logger.info("Testing health status codes...")
        
        async with aiohttp.ClientSession() as session:
            test_cases = [
                ("/health/", "Main health should return 200 for healthy system"),
                ("/health/live", "Liveness should return 200"),
                ("/health/ready", "Readiness should return 200 for ready system")
            ]
            
            results = {}
            
            for endpoint, description in test_cases:
                try:
                    url = f"{self.base_url}{endpoint}"
                    async with session.get(url) as response:
                        # Log the response data for debugging
                        if response.status >= 400:
                            response_data = await response.text()
                            logger.warning(f"Health endpoint {endpoint} returned {response.status}: {response_data}")
                        else:
                            response_data = await response.json()
                        
                        results[endpoint] = {
                            "status_code": response.status,
                            "expected_range": "2xx" if endpoint == "/health/" else "2xx",
                            "correct_status": 200 <= response.status < 300,
                            "data": response_data if response.status < 400 else str(response_data)[:200]
                        }
                        
                except Exception as e:
                    results[endpoint] = {
                        "error": str(e),
                        "success": False
                    }
                    logger.error(f"✗ {endpoint}: {str(e)}")
        
        return results
    
    async def test_middleware_observability(self) -> Dict[str, Any]:
        """Test middleware observability features"""
        logger.info("Testing middleware observability...")
        
        async with aiohttp.ClientSession() as session:
            # Make requests and check observability
            responses = []
            
            for i in range(3):
                async with session.get(f"{self.base_url}/api/v1/plants") as response:
                    response_info = {
                        "status": response.status,
                        "request_id": response.headers.get("X-Request-ID"),
                        "response_time": response.headers.get("X-Response-Time"),
                        "has_monitoring_headers": bool(response.headers.get("X-Request-ID"))
                    }
                    responses.append(response_info)
            
            # Check if all responses have unique request IDs
            request_ids = [r["request_id"] for r in responses if r["request_id"]]
            unique_request_ids = len(set(request_ids))
            
            return {
                "responses_tested": len(responses),
                "request_ids_generated": unique_request_ids,
                "all_have_request_ids": all(r["request_id"] for r in responses),
                "all_request_ids_unique": unique_request_ids == len(responses),
                "responses": responses
            }
    
    async def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run all health monitoring tests"""
        logger.info("Starting comprehensive health monitoring test...")
        
        # Test all components
        health_tests = await self.test_all_health_endpoints()
        monitoring_tests = await self.test_monitoring_middleware()
        metrics_tests = await self.test_metrics_collection()
        status_tests = await self.test_health_status_codes()
        observability_tests = await self.test_middleware_observability()
        
        # Calculate overall success rate
        all_tests = [
            health_tests, monitoring_tests, metrics_tests, 
            status_tests, observability_tests
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for test_group in all_tests:
            for test_name, result in test_group.items():
                total_tests += 1
                if (isinstance(result, dict) and (result.get("success", True) or result.get("status_code", 200) < 400)) or isinstance(result, bool):
                    passed_tests += 1
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Overall results
        results = {
            "overall_success_rate": success_rate,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "health_endpoints": health_tests,
            "monitoring_middleware": monitoring_tests,
            "metrics_collection": metrics_tests,
            "status_codes": status_tests,
            "observability": observability_tests,
            "test_completed_at": time.time()
        }
        
        # Log summary
        logger.info(f"Test completed: {passed_tests}/{total_tests} passed ({success_rate:.1f}%)")
        
        return results

async def main():
    """Main test execution"""
    print("FastAPI Health Monitoring Test Suite")
    print("=" * 50)
    
    tester = HealthMonitoringTester()
    
    try:
        # Run comprehensive tests
        results = await tester.run_comprehensive_test()
        
        # Save results to file
        with open("health_monitoring_test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\nTest Results Summary:")
        print(f"Success Rate: {results['overall_success_rate']:.1f}%")
        print(f"Passed: {results['passed_tests']}/{results['total_tests']}")
        
        if results['overall_success_rate'] >= 80:
            print("\n✅ Health monitoring tests PASSED")
            return 0
        else:
            print("\n❌ Health monitoring tests FAILED")
            print("Check health_monitoring_test_results.json for details")
            return 1
            
    except Exception as e:
        logger.error(f"Test execution failed: {str(e)}")
        print(f"\n❌ Test execution failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)