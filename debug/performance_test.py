#!/usr/bin/env python3
"""
Performance testing and benchmarking
"""

import asyncio
import time
import sys
import os
from statistics import mean, median, stdev

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_plane.orchestrator import ControlPlaneOrchestrator

async def benchmark_workflow_registration(iterations=100):
    """Benchmark workflow registration performance"""
    orchestrator = ControlPlaneOrchestrator()
    times = []
    
    print(f"\nBenchmarking workflow registration ({iterations} iterations)...")
    
    for i in range(iterations):
        start = time.perf_counter()
        await orchestrator.register_workflow(f"workflow-{i}", {})
        end = time.perf_counter()
        times.append((end - start) * 1000)  # Convert to ms
        
    print(f"  Mean: {mean(times):.4f}ms")
    print(f"  Median: {median(times):.4f}ms")
    print(f"  Std Dev: {stdev(times):.4f}ms")
    print(f"  Min: {min(times):.4f}ms")
    print(f"  Max: {max(times):.4f}ms")
    
async def benchmark_health_checks(iterations=100):
    """Benchmark health check performance"""
    orchestrator = ControlPlaneOrchestrator()
    times = []
    
    print(f"\nBenchmarking health checks ({iterations} iterations)...")
    
    for i in range(iterations):
        start = time.perf_counter()
        await orchestrator.health_check(f"service-{i % 10}")
        end = time.perf_counter()
        times.append((end - start) * 1000)
        
    print(f"  Mean: {mean(times):.4f}ms")
    print(f"  Median: {median(times):.4f}ms")
    print(f"  Std Dev: {stdev(times):.4f}ms")
    
async def benchmark_concurrent_operations(concurrent_tasks=50):
    """Benchmark concurrent operation handling"""
    orchestrator = ControlPlaneOrchestrator()
    
    print(f"\nBenchmarking {concurrent_tasks} concurrent operations...")
    
    async def mixed_operation(idx):
        await orchestrator.register_workflow(f"wf-{idx}", {})
        await orchestrator.start_workflow(f"wf-{idx}")
        await orchestrator.health_check(f"service-{idx}")
        
    start = time.perf_counter()
    await asyncio.gather(*[mixed_operation(i) for i in range(concurrent_tasks)])
    end = time.perf_counter()
    
    total_time = (end - start) * 1000
    ops_per_second = (concurrent_tasks * 3) / (total_time / 1000)
    
    print(f"  Total Time: {total_time:.2f}ms")
    print(f"  Operations/Second: {ops_per_second:.2f}")
    print(f"  Average per operation: {total_time / (concurrent_tasks * 3):.4f}ms")

async def main():
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARKS")
    print("="*60)
    
    await benchmark_workflow_registration()
    await benchmark_health_checks()
    await benchmark_concurrent_operations()
    
    print("\n" + "="*60)
    print("BENCHMARKS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
