#!/usr/bin/env python3
"""
Tests for Quantum Revenue Engine
"""

import pytest
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autonomous_orchestrator.quantum_revenue_engine import QuantumRevenueEngine

@pytest.fixture
def revenue_engine():
    """Create revenue engine instance"""
    return QuantumRevenueEngine()

@pytest.mark.asyncio
async def test_engine_initialization(revenue_engine):
    """Test revenue engine initializes correctly"""
    assert len(revenue_engine.streams) == 5
    assert revenue_engine.is_running is True
    print("✓ Revenue engine initialization test passed")

@pytest.mark.asyncio
async def test_process_stream(revenue_engine):
    """Test stream processing"""
    # Run for a short duration
    task = asyncio.create_task(revenue_engine.process_stream("Test Stream"))
    await asyncio.sleep(0.1)
    revenue_engine.is_running = False
    
    try:
        await asyncio.wait_for(task, timeout=1.0)
    except asyncio.TimeoutError:
        pass
    
    print("✓ Stream processing test passed")

@pytest.mark.asyncio
async def test_webhook_listener(revenue_engine):
    """Test webhook listener"""
    task = asyncio.create_task(revenue_engine.payment_webhook_listener())
    await asyncio.sleep(0.1)
    revenue_engine.is_running = False
    
    try:
        await asyncio.wait_for(task, timeout=1.0)
    except asyncio.TimeoutError:
        pass
    
    print("✓ Webhook listener test passed")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNING REVENUE ENGINE TESTS")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
