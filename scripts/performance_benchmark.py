"""
Performance Benchmarking Framework for CultivAR Application
Compares async vs sync performance across different operations.
"""

import asyncio
import time
import psutil
import sys
import os
from typing import Dict, List, Callable, Any
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
import json

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    name: str
    operation_type: str  # 'async' or 'sync'
    execution_time: float
    memory_usage_mb: float
    success: bool
    error_message: str = ""
    throughput_ops_per_sec: float = 0.0
    timestamp: str = ""

class PerformanceBenchmark:
    """Comprehensive performance benchmarking framework."""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.process = psutil.Process()
        
    @contextmanager
    def measure_performance(self, operation_name: str, operation_type: str):
        """Context manager to measure performance metrics."""
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        success = True
        error_message = ""
        
        try:
            yield
        except Exception as e:
            success = False
            error_message = str(e)
            raise
        finally:
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            result = BenchmarkResult(
                name=operation_name,
                operation_type=operation_type,
                execution_time=execution_time,
                memory_usage_mb=memory_delta,
                success=success,
                error_message=error_message,
                timestamp=datetime.now().isoformat()
            )
            
            self.results.append(result)
            
    def run_sync_operation(self, func: Callable, operation_name: str, *args, **kwargs):
        """Run a synchronous operation and measure performance."""
        with self.measure_performance(operation_name, 'sync'):
            return func(*args, **kwargs)
            
    async def run_async_operation(self, func: Callable, operation_name: str, *args, **kwargs):
        """Run an asynchronous operation and measure performance."""
        with self.measure_performance(operation_name, 'async'):
            return await func(*args, **kwargs)
            
    def run_concurrent_async_operations(self, func: Callable, operation_name: str, 
                                       concurrency_level: int = 10, *args, **kwargs):
        """Run multiple async operations concurrently."""
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        async def run_single():
            return await func(*args, **kwargs)
            
        # Create tasks for concurrent execution
        tasks = [run_single() for _ in range(concurrency_level)]
        results = []
        
        try:
            results = asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            success = False
            error_message = str(e)
        else:
            success = True
            error_message = ""
        finally:
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Calculate throughput
            throughput = concurrency_level / execution_time if execution_time > 0 else 0
            
            result = BenchmarkResult(
                name=f"{operation_name}_concurrent_{concurrency_level}",
                operation_type='async_concurrent',
                execution_time=execution_time,
                memory_usage_mb=memory_delta,
                success=success,
                error_message=error_message if not success else "",
                throughput_ops_per_sec=throughput
            )
            
            self.results.append(result)
            return results
            
    def run_load_test(self, func: Callable, operation_name: str, 
                     concurrent_requests: int = 100, requests_per_second: float = 10.0):
        """Run a load test with specified concurrent requests."""
        start_time = time.perf_counter()
        start_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
        async def single_request():
            return await func()
            
        # Calculate delay between batches to control rate
        batch_delay = 1.0 / requests_per_second
        
        async def load_test():
            batch_size = min(concurrent_requests, 20)  # Process in small batches
            total_requests = 0
            successful_requests = 0
            failed_requests = 0
            
            for i in range(0, concurrent_requests, batch_size):
                batch = [single_request() for _ in range(min(batch_size, concurrent_requests - i))]
                
                try:
                    results = await asyncio.gather(*batch, return_exceptions=True)
                    for result in results:
                        total_requests += 1
                        if isinstance(result, Exception):
                            failed_requests += 1
                        else:
                            successful_requests += 1
                except Exception as e:
                    failed_requests += len(batch)
                    
                if batch_delay > 0:
                    await asyncio.sleep(batch_delay)
                    
        try:
            asyncio.run(load_test())
            success = True
            error_message = ""
        except Exception as e:
            success = False
            error_message = str(e)
        finally:
            end_time = time.perf_counter()
            end_memory = self.process.memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            throughput = successful_requests / execution_time if execution_time > 0 else 0
            
            result = BenchmarkResult(
                name=f"{operation_name}_load_test_{concurrent_requests}_req",
                operation_type='load_test',
                execution_time=execution_time,
                memory_usage_mb=memory_delta,
                success=success,
                error_message=error_message if not success else "",
                throughput_ops_per_sec=throughput
            )
            
            self.results.append(result)
            
    def generate_report(self, output_file: str = None) -> str:
        """Generate a comprehensive performance report."""
        report_lines = [
            "=" * 80,
            "CULTIVAR ASYNC PERFORMANCE BENCHMARK REPORT",
            "=" * 80,
            f"Generated: {datetime.now().isoformat()}",
            f"Total benchmarks run: {len(self.results)}",
            ""
        ]
        
        # Group results by operation name
        async_results = []
        sync_results = []
        concurrent_results = []
        
        for result in self.results:
            if result.operation_type == 'async':
                async_results.append(result)
            elif result.operation_type == 'sync':
                sync_results.append(result)
            elif result.operation_type == 'async_concurrent':
                concurrent_results.append(result)
                
        # Summary statistics
        if async_results and sync_results:
            report_lines.extend([
                "ASYNC vs SYNC COMPARISON",
                "-" * 40,
                f"Async operations: {len(async_results)}",
                f"Sync operations: {len(sync_results)}",
                ""
            ])
            
            # Compare average performance
            async_avg_time = sum(r.execution_time for r in async_results) / len(async_results)
            sync_avg_time = sum(r.execution_time for r in sync_results) / len(sync_results)
            
            async_avg_memory = sum(abs(r.memory_usage_mb) for r in async_results) / len(async_results)
            sync_avg_memory = sum(abs(r.memory_usage_mb) for r in sync_results) / len(sync_results)
            
            time_improvement = ((sync_avg_time - async_avg_time) / sync_avg_time * 100) if sync_avg_time > 0 else 0
            memory_improvement = ((sync_avg_memory - async_avg_memory) / sync_avg_memory * 100) if sync_avg_memory > 0 else 0
            
            report_lines.extend([
                f"Average execution time:",
                f"  Async: {async_avg_time:.4f}s",
                f"  Sync:  {sync_avg_time:.4f}s",
                f"  Improvement: {time_improvement:+.2f}%",
                "",
                f"Average memory usage:",
                f"  Async: {async_avg_memory:.2f}MB",
                f"  Sync:  {sync_avg_memory:.2f}MB",
                f"  Improvement: {memory_improvement:+.2f}%",
                ""
            ])
            
        # Detailed results
        report_lines.extend([
            "DETAILED RESULTS",
            "-" * 40
        ])
        
        for result in self.results:
            status = "✓ SUCCESS" if result.success else "✗ FAILED"
            report_lines.extend([
                f"{status} - {result.name}",
                f"  Type: {result.operation_type}",
                f"  Time: {result.execution_time:.4f}s",
                f"  Memory: {result.memory_usage_mb:+.2f}MB",
                f"  Throughput: {result.throughput_ops_per_sec:.2f} ops/sec",
                f"  Timestamp: {result.timestamp}",
            ])
            
            if result.error_message:
                report_lines.append(f"  Error: {result.error_message}")
                
            report_lines.append("")
            
        # Throughput analysis for concurrent operations
        if concurrent_results:
            report_lines.extend([
                "CONCURRENT PERFORMANCE ANALYSIS",
                "-" * 40
            ])
            
            for result in concurrent_results:
                report_lines.extend([
                    f"{result.name}:",
                    f"  Operations per second: {result.throughput_ops_per_sec:.2f}",
                    f"  Total execution time: {result.execution_time:.4f}s",
                    f"  Memory usage: {result.memory_usage_mb:+.2f}MB",
                    ""
                ])
                
        report_text = "\n".join(report_lines)
        
        # Save to file if specified
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
                
        return report_text
        
    def save_json_results(self, output_file: str):
        """Save results in JSON format for further analysis."""
        json_results = []
        for result in self.results:
            json_results.append({
                'name': result.name,
                'operation_type': result.operation_type,
                'execution_time': result.execution_time,
                'memory_usage_mb': result.memory_usage_mb,
                'success': result.success,
                'error_message': result.error_message,
                'throughput_ops_per_sec': result.throughput_ops_per_sec,
                'timestamp': result.timestamp
            })
            
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)


# Example usage and test functions
async def test_async_database_operations():
    """Test async database operations."""
    try:
        from models_async import get_async_session
        from handlers.user_handlers_async import get_user_statistics
        
        async with get_async_session() as session:
            result = await get_user_statistics(session)
            return result
    except Exception as e:
        print(f"Error in async database test: {e}")
        return None


def test_sync_database_operations():
    """Test sync database operations for comparison."""
    try:
        from models import db, User
        # Simulate sync operation
        user_count = db.session.query(User).count()
        return {'total_users': user_count}
    except Exception as e:
        print(f"Error in sync database test: {e}")
        return None


def run_async_performance_benchmarks():
    """Run comprehensive async performance benchmarks."""
    benchmark = PerformanceBenchmark()
    
    print("🚀 Starting CultivAR Async Performance Benchmark...")
    
    # Test 1: Basic async vs sync comparison
    print("Running async vs sync database operations comparison...")
    
    # Run async test
    async def async_db_test():
        return await test_async_database_operations()
        
    asyncio.run(benchmark.run_async_operation(async_db_test, "Database Query Async"))
    
    # Run sync test
    benchmark.run_sync_operation(test_sync_database_operations, "Database Query Sync")
    
    # Test 2: Concurrent operations
    print("Testing concurrent operations...")
    
    async def concurrent_test():
        return await test_async_database_operations()
        
    benchmark.run_concurrent_async_operations(concurrent_test, "Concurrent DB Queries", concurrency_level=10)
    
    # Test 3: Load testing
    print("Running load test...")
    
    async def load_test():
        return await test_async_database_operations()
        
    benchmark.run_load_test(load_test, "Load Test DB Queries", concurrent_requests=50, requests_per_second=5.0)
    
    # Generate and display report
    print("\n📊 Generating performance report...")
    report = benchmark.generate_report()
    print("\n" + report)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    benchmark.save_json_results(f"scripts/performance_results_{timestamp}.json")
    
    return benchmark


if __name__ == "__main__":
    run_async_performance_benchmarks()