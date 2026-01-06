#!/usr/bin/env python3
"""
Comprehensive tests for Control Plane Orchestrator
"""

import pytest
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_plane.orchestrator import ControlPlaneOrchestrator

@pytest.fixture
async def orchestrator():
    """Create orchestrator instance for testing"""
    orch = ControlPlaneOrchestrator()
    yield orch
    orch.is_running = False

@pytest.mark.asyncio
async def test_register_workflow(orchestrator):
    """Test workflow registration"""
    workflow_id = "test-workflow"
    config = {"type": "async", "priority": "high"}
    
    await orchestrator.register_workflow(workflow_id, config)
    
    assert workflow_id in orchestrator.workflows
    assert orchestrator.workflows[workflow_id]['status'] == 'initialized'
    assert orchestrator.workflows[workflow_id]['run_count'] == 0
    print(f"✓ Workflow registration test passed")

@pytest.mark.asyncio
async def test_start_workflow(orchestrator):
    """Test workflow starting"""
    workflow_id = "test-workflow"
    await orchestrator.register_workflow(workflow_id, {})
    
    result = await orchestrator.start_workflow(workflow_id)
    
    assert result is True
    assert orchestrator.workflows[workflow_id]['status'] == 'running'
    assert orchestrator.workflows[workflow_id]['run_count'] == 1
    assert orchestrator.workflows[workflow_id]['last_run'] is not None
    print(f"✓ Workflow start test passed")

@pytest.mark.asyncio
async def test_stop_workflow(orchestrator):
    """Test workflow stopping"""
    workflow_id = "test-workflow"
    await orchestrator.register_workflow(workflow_id, {})
    await orchestrator.start_workflow(workflow_id)
    
    result = await orchestrator.stop_workflow(workflow_id)
    
    assert result is True
    assert orchestrator.workflows[workflow_id]['status'] == 'stopped'
    print(f"✓ Workflow stop test passed")

@pytest.mark.asyncio
async def test_health_check(orchestrator):
    """Test health check functionality"""
    service_name = "test-service"
    
    result = await orchestrator.health_check(service_name)
    
    assert result is True
    assert service_name in orchestrator.health_status
    assert orchestrator.health_status[service_name]['status'] == 'healthy'
    assert 'uptime_percentage' in orchestrator.health_status[service_name]
    print(f"✓ Health check test passed")

@pytest.mark.asyncio
async def test_auto_recovery(orchestrator):
    """Test automatic recovery mechanism"""
    service_name = "test-service"
    failure_type = "service_crash"
    
    await orchestrator.auto_recover(service_name, failure_type)
    
    assert len(orchestrator.recovery_history) > 0
    last_recovery = orchestrator.recovery_history[-1]
    assert last_recovery['service'] == service_name
    assert last_recovery['failure_type'] == failure_type
    assert last_recovery['success'] is True
    print(f"✓ Auto-recovery test passed")

@pytest.mark.asyncio
async def test_get_system_status(orchestrator):
    """Test system status retrieval"""
    await orchestrator.register_workflow("test-workflow", {})
    await orchestrator.health_check("test-service")
    
    status = await orchestrator.get_system_status()
    
    assert 'workflows' in status
    assert 'health_status' in status
    assert 'recovery_history' in status
    assert 'timestamp' in status
    print(f"✓ System status test passed")

@pytest.mark.asyncio
async def test_multiple_workflows(orchestrator):
    """Test managing multiple concurrent workflows"""
    workflow_ids = [f"workflow-{i}" for i in range(5)]
    
    for wid in workflow_ids:
        await orchestrator.register_workflow(wid, {})
        await orchestrator.start_workflow(wid)
    
    assert len(orchestrator.workflows) == 5
    for wid in workflow_ids:
        assert orchestrator.workflows[wid]['status'] == 'running'
    print(f"✓ Multiple workflows test passed")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNING ORCHESTRATOR TESTS")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
