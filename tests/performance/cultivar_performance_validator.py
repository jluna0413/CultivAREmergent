#!/usr/bin/env python3
"""
Comprehensive Performance and Load Testing Framework for CultivAR Application
Ensures system performance under various load conditions and stress scenarios.
"""

import asyncio
import aiohttp
import time
import json
import statistics
import logging
import argparse
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import threading
import psutil
import socket
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Performance metrics collector"""
    response_times: List[float]
    throughput: float
    error_rate: float
    success_rate: float
    concurrent_users: int
    total_requests: int
    failed_requests: int
    cpu_usage: float
    memory_usage: float
    network_io: Dict[str, float]
    timestamp: datetime
    
    @property
    def avg_response_time(self) -> float:
        return statistics.mean(self.response_times) if self.response_times else 0.0
    
    @property
    def p95_response_time(self) -> float:
        return statistics.quantiles(self.response_times, n=20)[18] if len(self.response_times) > 20 else (max(self.response_times) if self.response_times else 0.0)
    
    @property
    def p99_response_time(self) -> float:
        return statistics.quantiles(self.response_times, n=100)[98] if len(self.response_times) > 100 else (max(self.response_times) if self.response_times else 0.0)

class PerformanceTest:
    """Performance test scenario"""
    def __init__(self, name: str, endpoint: str, method: str = "GET", payload: Dict = None, weight: int = 1):
        self.name = name
        self.endpoint = endpoint
        self.method = method
        self.payload = payload
        self.weight = weight

class PerformanceLoadTester:
    """Main performance and load testing framework"""
    
    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = None
        self.test_results: List[PerformanceMetrics] = []
        self.stop_flag = threading.Event()
        
        # Performance thresholds
        self.max_response_time = 2.0  # seconds
        self.max_error_rate = 0.01    # 1%
        self.min_success_rate = 0.99  # 99%
        self.target_throughput = 100  # requests/second
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            connector=aiohttp.TCPConnector(limit=100),
            headers={
                'User-Agent': 'CultivAR-PerformanceTester/1.0',
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
    
    async def execute_endpoint_test(self, endpoint: str, method: str = "GET", payload: Dict = None, 
                                  timeout: float = 30.0) -> Tuple[float, int, bool]:
        """Execute a single endpoint test"""
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        start_time = time.time()
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url, timeout=timeout) as response:
                    await response.text()
                    status = response.status
            elif method.upper() == "POST":
                async with self.session.post(url, json=payload, timeout=timeout) as response:
                    await response.text()
                    status = response.status
            elif method.upper() == "PUT":
                async with self.session.put(url, json=payload, timeout=timeout) as response:
                    await response.text()
                    status = response.status
            elif method.upper() == "DELETE":
                async with self.session.delete(url, timeout=timeout) as response:
                    await response.text()
                    status = response.status
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = time.time() - start_time
            success = 200 <= status < 400
            return response_time, status, success
            
        except asyncio.TimeoutError:
            logger.warning(f"Timeout for {url}")
            return time.time() - start_time, 408, False
        except Exception as e:
            logger.error(f"Error executing {url}: {str(e)}")
            return time.time() - start_time, 500, False
    
    async def load_test(self, test_scenarios: List[PerformanceTest], 
                       concurrent_users: int, duration_seconds: int) -> PerformanceMetrics:
        """Execute load test with specified scenarios"""
        logger.info(f"Starting load test: {concurrent_users} users, {duration_seconds}s duration")
        
        self.stop_flag.clear()
        response_times = []
        total_requests = 0
        failed_requests = 0
        
        # Start system monitoring
        monitor_task = asyncio.create_task(self._monitor_system_resources())
        
        # Create user simulation tasks
        user_tasks = []
        for i in range(concurrent_users):
            user_task = asyncio.create_task(
                self._simulate_user_load(test_scenarios, response_times, total_requests, failed_requests, duration_seconds)
            )
            user_tasks.append(user_task)
        
        # Wait for all users to complete
        start_time = time.time()
        await asyncio.gather(*user_tasks, return_exceptions=True)
        end_time = time.time()
        
        # Stop monitoring
        self.stop_flag.set()
        await monitor_task
        
        # Calculate metrics
        actual_duration = end_time - start_time
        throughput = total_requests / actual_duration if actual_duration > 0 else 0
        error_rate = failed_requests / total_requests if total_requests > 0 else 0
        success_rate = 1 - error_rate
        
        # Get final system metrics
        system_metrics = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        network_io = psutil.net_io_counters()
        
        return PerformanceMetrics(
            response_times=response_times,
            throughput=throughput,
            error_rate=error_rate,
            success_rate=success_rate,
            concurrent_users=concurrent_users,
            total_requests=total_requests,
            failed_requests=failed_requests,
            cpu_usage=cpu_percent,
            memory_usage=system_metrics.percent,
            network_io={
                'bytes_sent': network_io.bytes_sent,
                'bytes_recv': network_io.bytes_recv
            },
            timestamp=datetime.now()
        )
    
    async def _simulate_user_load(self, test_scenarios: List[PerformanceTest], 
                                 response_times: List, total_requests: int, failed_requests: int,
                                 duration_seconds: int):
        """Simulate user behavior for load testing"""
        end_time = time.time() + duration_seconds
        
        # Weighted random scenario selection
        scenarios = []
        for scenario in test_scenarios:
            scenarios.extend([scenario] * scenario.weight)
        
        while time.time() < end_time and not self.stop_flag.is_set():
            if not scenarios:
                break
                
            scenario = scenarios[hash(str(threading.current_thread())) % len(scenarios)]
            
            try:
                response_time, status, success = await self.execute_endpoint_test(
                    scenario.endpoint, scenario.method, scenario.payload
                )
                
                response_times.append(response_time)
                with threading.Lock():
                    total_requests[0] += 1
                    if not success:
                        failed_requests[0] += 1
                
                # Simulate user think time
                await asyncio.sleep(0.1 + (hash(str(threading.current_thread())) % 100) / 1000.0)
                
            except Exception as e:
                logger.error(f"Error in user simulation: {str(e)}")
                with threading.Lock():
                    failed_requests[0] += 1
    
    async def _monitor_system_resources(self):
        """Monitor system resources during test execution"""
        logger.info("Starting system resource monitoring")
        
        while not self.stop_flag.is_set():
            try:
                # Monitor database connections, memory, CPU, disk I/O
                memory = psutil.virtual_memory()
                cpu = psutil.cpu_percent(interval=1)
                disk = psutil.disk_usage('/')
                network = psutil.net_io_counters()
                
                logger.debug(f"System Metrics - CPU: {cpu}%, Memory: {memory.percent}%, "
                           f"Disk: {disk.percent}%, Network: {network}")
                
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error monitoring system resources: {str(e)}")
                await asyncio.sleep(1)
    
    async def stress_test(self, test_scenarios: List[PerformanceTest], 
                         start_users: int, max_users: int, step: int, 
                         duration_per_step: int = 60) -> List[PerformanceMetrics]:
        """Execute stress test by gradually increasing load"""
        logger.info(f"Starting stress test: {start_users} to {max_users} users, step: {step}")
        
        results = []
        current_users = start_users
        
        while current_users <= max_users and not self.stop_flag.is_set():
            logger.info(f"Testing with {current_users} concurrent users")
            
            metrics = await self.load_test(test_scenarios, current_users, duration_per_step)
            results.append(metrics)
            
            # Check if system is degraded
            if metrics.error_rate > 0.05:  # 5% error rate threshold
                logger.warning(f"High error rate detected: {metrics.error_rate:.2%} at {current_users} users")
                break
            
            if metrics.avg_response_time > self.max_response_time:
                logger.warning(f"High response time detected: {metrics.avg_response_time:.2f}s at {current_users} users")
                break
            
            current_users += step
            
            # Cool down period
            await asyncio.sleep(5)
        
        return results
    
    async def endurance_test(self, test_scenarios: List[PerformanceTest], 
                           concurrent_users: int, duration_hours: int = 24) -> PerformanceMetrics:
        """Execute endurance test for extended period"""
        logger.info(f"Starting endurance test: {concurrent_users} users for {duration_hours} hours")
        
        duration_seconds = duration_hours * 3600
        return await self.load_test(test_scenarios, concurrent_users, duration_seconds)
    
    def validate_performance_requirements(self, metrics: PerformanceMetrics) -> Dict[str, bool]:
        """Validate if performance meets requirements"""
        results = {}
        
        results['response_time_ok'] = metrics.avg_response_time <= self.max_response_time
        results['error_rate_ok'] = metrics.error_rate <= self.max_error_rate
        results['success_rate_ok'] = metrics.success_rate >= self.min_success_rate
        results['throughput_ok'] = metrics.throughput >= self.target_throughput
        
        return results

def create_cultivar_test_scenarios() -> List[PerformanceTest]:
    """Create comprehensive test scenarios for CultivAR application"""
    scenarios = [
        # Authentication endpoints (high weight)
        PerformanceTest("User Login", "/api/auth/login", "POST", {"email": "test@example.com", "password": "test"}, 3),
        PerformanceTest("Token Refresh", "/api/auth/refresh", "POST", {}, 2),
        PerformanceTest("User Profile", "/api/auth/profile", "GET", {}, 2),
        
        # Plant management endpoints
        PerformanceTest("List Plants", "/api/plants", "GET", {}, 3),
        PerformanceTest("Create Plant", "/api/plants", "POST", {}, 1),
        PerformanceTest("Get Plant Details", "/api/plants/123", "GET", {}, 2),
        PerformanceTest("Update Plant", "/api/plants/123", "PUT", {}, 1),
        PerformanceTest("Delete Plant", "/api/plants/123", "DELETE", {}, 1),
        
        # Dashboard endpoints
        PerformanceTest("Dashboard Data", "/api/dashboard", "GET", {}, 3),
        PerformanceTest("Dashboard Stats", "/api/dashboard/stats", "GET", {}, 2),
        PerformanceTest("Recent Activity", "/api/dashboard/activity", "GET", {}, 2),
        
        # Sensor endpoints
        PerformanceTest("Sensor Data", "/api/sensors/data", "GET", {}, 3),
        PerformanceTest("Sensor List", "/api/sensors", "GET", {}, 2),
        PerformanceTest("Add Sensor Reading", "/api/sensors/readings", "POST", {}, 1),
        
        # Strain management
        PerformanceTest("List Strains", "/api/strains", "GET", {}, 2),
        PerformanceTest("Strain Details", "/api/strains/123", "GET", {}, 1),
        
        # Settings endpoints
        PerformanceTest("User Settings", "/api/settings", "GET", {}, 1),
        PerformanceTest("Update Settings", "/api/settings", "PUT", {}, 1),
        
        # Health check (very high weight)
        PerformanceTest("Health Check", "/health", "GET", {}, 5),
        PerformanceTest("API Health", "/api/health", "GET", {}, 5)
    ]
    
    return scenarios

async def run_performance_validation(base_url: str, auth_token: str = None, 
                                   test_type: str = "all") -> Dict[str, Any]:
    """Run comprehensive performance validation"""
    logger.info(f"Starting performance validation for {base_url}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "test_type": test_type,
        "load_tests": [],
        "stress_tests": [],
        "endurance_tests": [],
        "performance_requirements_met": {},
        "recommendations": []
    }
    
    async with PerformanceLoadTester(base_url, auth_token) as tester:
        scenarios = create_cultivar_test_scenarios()
        
        # Connection test
        try:
            response_time, status, success = await tester.execute_endpoint_test("/health")
            if not success:
                raise Exception(f"Health check failed: {status}")
            logger.info("✅ Connection test passed")
        except Exception as e:
            logger.error(f"❌ Connection test failed: {str(e)}")
            results["error"] = f"Connection test failed: {str(e)}"
            return results
        
        if test_type in ["all", "load"]:
            # Standard load test
            logger.info("🔄 Running load tests...")
            load_metrics = await tester.load_test(scenarios, 10, 120)  # 10 users, 2 minutes
            results["load_tests"].append(load_metrics.__dict__)
            
            validation = tester.validate_performance_requirements(load_metrics)
            results["performance_requirements_met"]["load_test"] = validation
            
            # Load test recommendations
            if not validation['response_time_ok']:
                results["recommendations"].append("Optimize database queries and implement caching")
            if not validation['error_rate_ok']:
                results["recommendations"].append("Review error handling and implement circuit breakers")
            if not validation['throughput_ok']:
                results["recommendations"].append("Consider horizontal scaling and load balancing")
        
        if test_type in ["all", "stress"]:
            # Stress test
            logger.info("🔄 Running stress tests...")
            stress_results = await tester.stress_test(scenarios, 5, 50, 5, 30)  # 5-50 users, step 5
            for metrics in stress_results:
                results["stress_tests"].append(metrics.__dict__)
            
            if stress_results:
                max_users_sustained = max(r.concurrent_users for r in stress_results 
                                        if r.error_rate <= 0.01)
                results["recommendations"].append(f"System can sustain {max_users_sustained} concurrent users")
        
        if test_type in ["all", "endurance"]:
            # Brief endurance test (30 minutes instead of 24 hours)
            logger.info("🔄 Running endurance tests...")
            endurance_metrics = await tester.endurance_test(scenarios, 5, 0.5)  # 5 users, 30 minutes
            results["endurance_tests"].append(endurance_metrics.__dict__)
            
            endurance_validation = tester.validate_performance_requirements(endurance_metrics)
            results["performance_requirements_met"]["endurance_test"] = endurance_validation
    
    # Generate comprehensive recommendations
    all_validations = []
    for category in results["performance_requirements_met"].values():
        all_validations.extend(category.values())
    
    if all(all_validations):
        results["recommendations"].append("✅ All performance requirements met - system ready for production")
    else:
        results["recommendations"].append("⚠️  Performance improvements needed before production deployment")
    
    logger.info("✅ Performance validation completed")
    return results

def main():
    """CLI interface for performance testing"""
    parser = argparse.ArgumentParser(description="CultivAR Performance Testing Framework")
    parser.add_argument("--url", required=True, help="Base URL for testing")
    parser.add_argument("--token", help="JWT authentication token")
    parser.add_argument("--test-type", choices=["load", "stress", "endurance", "all"], 
                       default="all", help="Type of test to run")
    parser.add_argument("--output", help="Output file for results (JSON)")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run validation
    async def run():
        results = await run_performance_validation(args.url, args.token, args.test_type)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, default=str))
        
        return results
    
    results = asyncio.run(run())
    
    # Exit with appropriate code
    performance_issues = any(not all(category.values()) 
                           for category in results.get("performance_requirements_met", {}).values())
    if performance_issues:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()