#!/usr/bin/env python3
"""
Integration tests for complete system
"""

import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_plane.orchestrator import ControlPlaneOrchestrator
from autonomous_orchestrator.quantum_revenue_engine import QuantumRevenueEngine
from autonomous_orchestrator.self_healing_monitor import SelfHealingMonitor

@pytest.mark.asyncio
async def test_full_system_integration():
    """Test complete system working together"""
    print("\nStarting full system integration test...")
    
    # Initialize all components
    orchestrator = ControlPlaneOrchestrator()
    revenue_engine = QuantumRevenueEngine()
    monitor = SelfHealingMonitor()
    
    # Register workflows
    await orchestrator.register_workflow("revenue-stream-1", {"type": "async"})
    await orchestrator.register_workflow("revenue-stream-2", {"type": "async"})
    
    # Start workflows
    await orchestrator.start_workflow("revenue-stream-1")
    await orchestrator.start_workflow("revenue-stream-2")
    
    # Check health
    health = await orchestrator.health_check("revenue-engine")
    assert health is True
    
    # Simulate failure and recovery
    await orchestrator.auto_recover("revenue-engine", "service_crash")
    
    # Get system status
    status = await orchestrator.get_system_status()
    
    assert len(status['workflows']) >= 2
    assert len(status['recovery_history']) >= 1
    
    orchestrator.is_running = False
    revenue_engine.is_running = False
    
    print("✓ Full system integration test passed")
    print(f"  - Workflows registered: {len(status['workflows'])}")
    print(f"  - Health checks performed: {len(status['health_status'])}")
    print(f"  - Recovery events: {len(status['recovery_history'])}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNING INTEGRATION TESTS")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
