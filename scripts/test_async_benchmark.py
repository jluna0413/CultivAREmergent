#!/usr/bin/env python3
"""
Simple Async Performance Benchmark for CultivAR
Tests async vs sync performance comparison
"""

import asyncio
import time
import psutil

def test_sync_operation():
    """Simulate a synchronous database operation."""
    time.sleep(0.001)  # Simulate I/O delay
    return "sync_result"

async def test_async_operation():
    """Simulate an asynchronous database operation."""
    await asyncio.sleep(0.001)  # Simulate async I/O delay
    return "async_result"

def measure_sync_performance(iterations=100):
    """Measure synchronous performance."""
    process = psutil.Process()
    start_time = time.perf_counter()
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    results = []
    for _ in range(iterations):
        result = test_sync_operation()
        results.append(result)
    
    end_time = time.perf_counter()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    execution_time = end_time - start_time
    memory_delta = end_memory - start_memory
    throughput = iterations / execution_time if execution_time > 0 else 0
    
    return {
        'execution_time': execution_time,
        'memory_delta': memory_delta,
        'throughput': throughput,
        'iterations': iterations
    }

async def measure_async_performance(iterations=100):
    """Measure asynchronous performance."""
    process = psutil.Process()
    start_time = time.perf_counter()
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    tasks = [test_async_operation() for _ in range(iterations)]
    results = await asyncio.gather(*tasks)
    
    end_time = time.perf_counter()
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    execution_time = end_time - start_time
    memory_delta = end_memory - start_memory
    throughput = iterations / execution_time if execution_time > 0 else 0
    
    return {
        'execution_time': execution_time,
        'memory_delta': memory_delta,
        'throughput': throughput,
        'iterations': iterations
    }

async def run_benchmark():
    """Run the complete async performance benchmark."""
    print("=" * 60)
    print("CULTIVAR ASYNC PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    iterations = 100
    
    # Test synchronous operations
    print(f"\nTesting {iterations} synchronous operations...")
    sync_results = measure_sync_performance(iterations)
    
    print("SYNC RESULTS:")
    print(f"  Execution time: {sync_results['execution_time']:.4f}s")
    print(f"  Memory delta: {sync_results['memory_delta']:+.2f}MB")
    print(f"  Throughput: {sync_results['throughput']:.2f} ops/sec")
    
    # Test asynchronous operations
    print(f"\nTesting {iterations} asynchronous operations...")
    async_results = await measure_async_performance(iterations)
    
    print("ASYNC RESULTS:")
    print(f"  Execution time: {async_results['execution_time']:.4f}s")
    print(f"  Memory delta: {async_results['memory_delta']:+.2f}MB")
    print(f"  Throughput: {async_results['throughput']:.2f} ops/sec")
    
    # Calculate performance improvements
    time_improvement = ((sync_results['execution_time'] - async_results['execution_time']) / sync_results['execution_time'] * 100) if sync_results['execution_time'] > 0 else 0
    throughput_improvement = ((async_results['throughput'] - sync_results['throughput']) / sync_results['throughput'] * 100) if sync_results['throughput'] > 0 else 0
    
    print("\nPERFORMANCE COMPARISON:")
    print(f"  Time improvement: {time_improvement:+.2f}%")
    print(f"  Throughput improvement: {throughput_improvement:+.2f}%")
    print(f"  Memory difference: {async_results['memory_delta'] - sync_results['memory_delta']:+.2f}MB")
    
    # Test concurrent operations
    print(f"\nTesting concurrent operations...")
    concurrent_iterations = 50
    concurrent_results = await measure_async_performance(concurrent_iterations)
    
    print("CONCURRENT ASYNC RESULTS:")
    print(f"  Execution time: {concurrent_results['execution_time']:.4f}s")
    print(f"  Throughput: {concurrent_results['throughput']:.2f} ops/sec")
    
    # Load testing simulation
    print(f"\nSimulating load test...")
    load_iterations = 100
    process = psutil.Process()
    start_time = time.perf_counter()
    
    # Process in batches to simulate realistic load
    batch_size = 10
    for i in range(0, load_iterations, batch_size):
        batch = [test_async_operation() for _ in range(min(batch_size, load_iterations - i))]
        await asyncio.gather(*batch)
    
    load_time = time.perf_counter() - start_time
    load_throughput = load_iterations / load_time if load_time > 0 else 0
    
    print("LOAD TEST RESULTS:")
    print(f"  Execution time: {load_time:.4f}s")
    print(f"  Throughput: {load_throughput:.2f} ops/sec")
    print(f"  Batches processed: {load_iterations // batch_size}")
    
    # Summary
    print("\n" + "=" * 60)
    print("BENCHMARK SUMMARY")
    print("=" * 60)
    print(f"Async operations show {time_improvement:+.2f}% improvement in execution time")
    print(f"Async operations show {throughput_improvement:+.2f}% improvement in throughput")
    print(f"Concurrent processing achieves {concurrent_results['throughput']:.2f} ops/sec")
    print(f"Load testing achieves {load_throughput:.2f} ops/sec")
    
    return {
        'sync': sync_results,
        'async': async_results,
        'concurrent': concurrent_results,
        'load': {'time': load_time, 'throughput': load_throughput},
        'improvements': {
            'time': time_improvement,
            'throughput': throughput_improvement
        }
    }

if __name__ == "__main__":
    asyncio.run(run_benchmark())