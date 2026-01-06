#!/usr/bin/env python3
"""
Comprehensive test suite for Enhanced Control Plane Orchestrator
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from control_plane.orchestrator_enhanced import (
    ControlPlaneOrchestrator,
    CircuitBreaker,
    CircuitState
)

@pytest.mark.asyncio
class TestCircuitBreaker:
    """Test circuit breaker functionality"""
    
    async def test_circuit_breaker_closed_state(self):
        """Test normal operation in CLOSED state"""
        breaker = CircuitBreaker(failure_threshold=3)
        assert breaker.state == CircuitState.CLOSED
        assert breaker.can_execute() is True
        
    async def test_circuit_breaker_opens_on_failures(self):
        """Test circuit opens after threshold failures"""
        breaker = CircuitBreaker(failure_threshold=3)
        
        # Record failures
        for _ in range(3):
            breaker.record_failure()
            
        assert breaker.state == CircuitState.OPEN
        assert breaker.can_execute() is False
        
    async def test_circuit_breaker_half_open_recovery(self):
        """Test recovery through HALF_OPEN state"""
        breaker = CircuitBreaker(failure_threshold=2, timeout=1)
        
        # Trip the breaker
        breaker.record_failure()
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN
        
        # Wait for timeout
        await asyncio.sleep(1.5)
        
        # Should transition to HALF_OPEN
        assert breaker.can_execute() is True
        
        # Record successful calls to close circuit
        for _ in range(3):
            breaker.record_success()
            
        assert breaker.state == CircuitState.CLOSED
        
    async def test_circuit_breaker_state_reporting(self):
        """Test circuit breaker state reporting"""
        breaker = CircuitBreaker()
        state = breaker.get_state()
        
        assert 'state' in state
        assert 'failure_count' in state
        assert 'last_failure' in state
        assert state['state'] == 'closed'

@pytest.mark.asyncio
class TestOrchestratorEnhanced:
    """Test enhanced orchestrator functionality"""
    
    async def test_workflow_registration(self):
        """Test workflow registration"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_state.pkl")
        
        await orchestrator.register_workflow(
            'test-workflow',
            {'type': 'test', 'priority': 'high'}
        )
        
        assert 'test-workflow' in orchestrator.workflows
        assert orchestrator.workflows['test-workflow']['status'] == 'initialized'
        assert orchestrator.metrics['total_workflows'] == 1
        
        # Cleanup
        Path("test_state.pkl").unlink(missing_ok=True)
        
    async def test_workflow_lifecycle(self):
        """Test complete workflow lifecycle"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_state.pkl")
        
        # Register
        await orchestrator.register_workflow('lifecycle-test', {'type': 'test'})
        
        # Start
        result = await orchestrator.start_workflow('lifecycle-test')
        assert result is True
        assert orchestrator.workflows['lifecycle-test']['status'] == 'running'
        assert orchestrator.workflows['lifecycle-test']['run_count'] == 1
        
        # Stop
        result = await orchestrator.stop_workflow('lifecycle-test')
        assert result is True
        assert orchestrator.workflows['lifecycle-test']['status'] == 'stopped'
        
        # Cleanup
        Path("test_state.pkl").unlink(missing_ok=True)
        
    async def test_health_check_with_circuit_breaker(self):
        """Test health checks integrate with circuit breakers"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_state.pkl")
        
        # Perform health check
        result = await orchestrator.health_check('test-service')
        
        assert 'test-service' in orchestrator.health_status
        assert 'circuit_breaker' in orchestrator.health_status['test-service']
        
        # Cleanup
        Path("test_state.pkl").unlink(missing_ok=True)
        
    async def test_auto_recovery(self):
        """Test automatic recovery functionality"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_state.pkl")
        
        result = await orchestrator.auto_recover('test-service', 'service_crash')
        
        assert len(orchestrator.recovery_history) > 0
        assert orchestrator.recovery_history[0]['service'] == 'test-service'
        assert orchestrator.recovery_history[0]['success'] is True
        assert orchestrator.metrics['successful_recoveries'] > 0
        
        # Cleanup
        Path("test_state.pkl").unlink(missing_ok=True)
        
    async def test_state_persistence(self):
        """Test state save and load"""
        state_file = "test_persistence.pkl"
        
        # Create orchestrator and add data
        orch1 = ControlPlaneOrchestrator(state_file=state_file)
        await orch1.register_workflow('persist-test', {'type': 'test'})
        orch1._save_state()
        
        # Create new orchestrator and verify state loaded
        orch2 = ControlPlaneOrchestrator(state_file=state_file)
        assert 'persist-test' in orch2.workflows
        
        # Cleanup
        Path(state_file).unlink(missing_ok=True)
        
    async def test_system_status(self):
        """Test comprehensive status reporting"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_state.pkl")
        await orchestrator.register_workflow('status-test', {'type': 'test'})
        
        status = await orchestrator.get_system_status()
        
        assert 'workflows' in status
        assert 'health_status' in status
        assert 'recovery_history' in status
        assert 'circuit_breakers' in status
        assert 'metrics' in status
        assert 'uptime_seconds' in status['metrics']
        
        # Cleanup
        Path("test_state.pkl").unlink(missing_ok=True)
        
    async def test_graceful_shutdown(self):
        """Test graceful shutdown process"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_shutdown.pkl")
        await orchestrator.register_workflow('shutdown-test', {'type': 'test'})
        await orchestrator.start_workflow('shutdown-test')
        
        # Trigger shutdown
        await orchestrator.graceful_shutdown("TEST")
        
        assert orchestrator.is_running is False
        assert orchestrator.workflows['shutdown-test']['status'] == 'stopped'
        
        # Cleanup
        Path("test_shutdown.pkl").unlink(missing_ok=True)

@pytest.mark.asyncio
class TestConcurrentOperations:
    """Test concurrent workflow operations"""
    
    async def test_concurrent_workflow_execution(self):
        """Test multiple workflows running concurrently"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_concurrent.pkl")
        
        # Register multiple workflows
        workflows = ['wf1', 'wf2', 'wf3', 'wf4', 'wf5']
        for wf_id in workflows:
            await orchestrator.register_workflow(wf_id, {'type': 'concurrent'})
            
        # Start all concurrently
        results = await asyncio.gather(*[
            orchestrator.start_workflow(wf_id) for wf_id in workflows
        ])
        
        assert all(results)
        assert all(
            orchestrator.workflows[wf_id]['status'] == 'running'
            for wf_id in workflows
        )
        
        # Cleanup
        Path("test_concurrent.pkl").unlink(missing_ok=True)
        
    async def test_concurrent_health_checks(self):
        """Test concurrent health check operations"""
        orchestrator = ControlPlaneOrchestrator(state_file="test_health.pkl")
        
        services = ['svc1', 'svc2', 'svc3', 'svc4']
        
        # Perform concurrent health checks
        results = await asyncio.gather(*[
            orchestrator.health_check(svc) for svc in services
        ])
        
        # Verify all services checked
        assert all(svc in orchestrator.health_status for svc in services)
        
        # Cleanup
        Path("test_health.pkl").unlink(missing_ok=True)

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
