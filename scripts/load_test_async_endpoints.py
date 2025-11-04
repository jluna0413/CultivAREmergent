#!/usr/bin/env python3
"""
Load Testing Script for Async Endpoints
Tests concurrent request handling and performance under load
"""

import asyncio
import aiohttp
import time
import psutil
import json
from typing import List, Dict, Any
from datetime import datetime

class AsyncLoadTester:
    """Load testing framework for async endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.results = []
        
    async def test_endpoint(self, endpoint: str, method: str = "GET", 
                          data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Test a single endpoint and measure performance."""
        url = f"{self.base_url}{endpoint}"
        if headers is None:
            headers = {"Content-Type": "application/json"}
            
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            async with aiohttp.ClientSession() as session:
                if method.upper() == "GET":
                    async with session.get(url, headers=headers) as response:
                        response_text = await response.text()
                        status_code = response.status
                elif method.upper() == "POST":
                    async with session.post(url, json=data, headers=headers) as response:
                        response_text = await response.text()
                        status_code = response.status
                else:
                    raise ValueError(f"Unsupported method: {method}")
                    
            end_time = time.perf_counter()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            success = 200 <= status_code < 300
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "execution_time": execution_time,
                "memory_delta": memory_delta,
                "success": success,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            return {
                "endpoint": endpoint,
                "method": method,
                "status_code": 0,
                "execution_time": execution_time,
                "memory_delta": 0,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def run_load_test(self, endpoint: str, concurrent_requests: int = 100,
                          requests_per_second: float = 10.0, method: str = "GET"):
        """Run a load test against an endpoint."""
        print(f"Starting load test on {endpoint}")
        print(f"Concurrent requests: {concurrent_requests}")
        print(f"Target rate: {requests_per_second} req/sec")
        print("-" * 50)
        
        start_time = time.perf_counter()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Calculate batch size and delay
        batch_size = min(concurrent_requests, 20)
        batch_delay = 1.0 / requests_per_second
        
        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        
        # Process requests in batches
        for i in range(0, concurrent_requests, batch_size):
            batch = min(batch_size, concurrent_requests - i)
            tasks = [self.test_endpoint(endpoint, method) for _ in range(batch)]
            
            try:
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in batch_results:
                    total_requests += 1
                    if isinstance(result, dict) and result.get("success"):
                        successful_requests += 1
                    else:
                        failed_requests += 1
                        
            except Exception as e:
                failed_requests += batch
                print(f"Batch error: {e}")
            
            # Rate limiting delay
            if batch_delay > 0:
                await asyncio.sleep(batch_delay)
        
        end_time = time.perf_counter()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        # Calculate metrics
        execution_time = end_time - start_time
        memory_delta = end_memory - start_memory
        actual_rate = total_requests / execution_time if execution_time > 0 else 0
        success_rate = (successful_requests / total_requests * 100) if total_requests > 0 else 0
        
        summary = {
            "endpoint": endpoint,
            "method": method,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": success_rate,
            "execution_time": execution_time,
            "memory_delta": memory_delta,
            "actual_rate": actual_rate,
            "target_rate": requests_per_second,
            "timestamp": datetime.now().isoformat()
        }
        
        # Print results
        print(f"Load Test Results:")
        print(f"  Total requests: {total_requests}")
        print(f"  Successful: {successful_requests}")
        print(f"  Failed: {failed_requests}")
        print(f"  Success rate: {success_rate:.2f}%")
        print(f"  Execution time: {execution_time:.4f}s")
        print(f"  Target rate: {requests_per_second:.2f} req/sec")
        print(f"  Actual rate: {actual_rate:.2f} req/sec")
        print(f"  Memory delta: {memory_delta:+.2f}MB")
        
        return summary
    
    async def test_multiple_endpoints(self, endpoints: List[str]):
        """Test multiple endpoints concurrently."""
        print("Testing multiple endpoints concurrently...")
        
        tasks = []
        for endpoint in endpoints:
            task = self.run_load_test(endpoint, concurrent_requests=50, requests_per_second=5.0)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    def save_results(self, results: List[Dict], filename: str = None):
        """Save test results to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scripts/load_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to: {filename}")

async def run_comprehensive_load_test():
    """Run comprehensive load tests on key endpoints."""
    load_tester = AsyncLoadTester()
    
    # Define test endpoints (adjust based on your Flask app routes)
    test_endpoints = [
        "/auth/login",
        "/auth/signup", 
        "/dashboard",
        "/strains",
        "/market",
        "/newsletter/subscribe"
    ]
    
    print("CULTIVAR ASYNC LOAD TESTING")
    print("=" * 60)
    
    # Test 1: Single endpoint with different loads
    print("\n1. Testing dashboard endpoint with increasing load...")
    await load_tester.run_load_test("/dashboard", concurrent_requests=100, requests_per_second=10.0)
    
    # Test 2: Authentication endpoints under load
    print("\n2. Testing authentication endpoints under load...")
    auth_results = await load_tester.test_multiple_endpoints([
        "/auth/login",
        "/auth/signup"
    ])
    
    # Test 3: API endpoints concurrent testing
    print("\n3. Testing API endpoints concurrently...")
    api_results = await load_tester.test_multiple_endpoints([
        "/strains",
        "/market",
        "/newsletter/subscribe"
    ])
    
    # Test 4: Stress test
    print("\n4. Running stress test...")
    stress_results = await load_tester.run_load_test(
        "/dashboard", 
        concurrent_requests=200, 
        requests_per_second=20.0
    )
    
    # Save all results
    all_results = [stress_results]
    load_tester.save_results(all_results)
    
    print("\n" + "=" * 60)
    print("LOAD TESTING COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_load_test())