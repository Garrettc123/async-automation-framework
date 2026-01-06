#!/usr/bin/env python3
"""
Enhanced Control Plane Orchestrator with Graceful Shutdown & Circuit Breakers
Manages all automation workflows, self-healing, and recovery operations
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import signal
import pickle
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ControlPlaneOrchestrator")

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"      # Circuit breaker tripped
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker pattern for service resilience"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60, half_open_max_calls: int = 3):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_max_calls = half_open_max_calls
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        self.half_open_calls = 0
        
    def record_success(self):
        """Record successful call"""
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.half_open_calls >= self.half_open_max_calls:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.half_open_calls = 0
                logger.info("Circuit breaker CLOSED - service recovered")
        else:
            self.failure_count = max(0, self.failure_count - 1)
            
    def record_failure(self):
        """Record failed call"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker OPEN - failure threshold reached ({self.failure_count})")
            
    def can_execute(self) -> bool:
        """Check if call can proceed"""
        if self.state == CircuitState.CLOSED:
            return True
            
        if self.state == CircuitState.OPEN:
            if self.last_failure_time and \
               (datetime.now() - self.last_failure_time).seconds >= self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                logger.info("Circuit breaker HALF-OPEN - testing recovery")
                return True
            return False
            
        return True  # HALF_OPEN state
        
    def get_state(self) -> Dict[str, Any]:
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'last_failure': self.last_failure_time.isoformat() if self.last_failure_time else None
        }

class ControlPlaneOrchestrator:
    """Enhanced central orchestrator with graceful shutdown and persistence"""
    
    def __init__(self, state_file: str = "orchestrator_state.pkl"):
        self.workflows = {}
        self.health_status = {}
        self.recovery_history = []
        self.is_running = True
        self.shutdown_event = asyncio.Event()
        self.tasks = []
        self.circuit_breakers = {}
        self.state_file = Path(state_file)
        self.metrics = {
            'total_workflows': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'uptime_start': datetime.now()
        }
        
        # Load persisted state
        self._load_state()
        
    def _load_state(self):
        """Load persisted state from disk"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'rb') as f:
                    state = pickle.load(f)
                    self.workflows = state.get('workflows', {})
                    self.recovery_history = state.get('recovery_history', [])
                    self.metrics = state.get('metrics', self.metrics)
                    logger.info(f"State restored from {self.state_file}")
            except Exception as e:
                logger.error(f"Failed to load state: {e}")
                
    def _save_state(self):
        """Persist state to disk"""
        try:
            state = {
                'workflows': self.workflows,
                'recovery_history': self.recovery_history[-100:],  # Keep last 100
                'metrics': self.metrics,
                'saved_at': datetime.now().isoformat()
            }
            with open(self.state_file, 'wb') as f:
                pickle.dump(state, f)
            logger.info(f"State saved to {self.state_file}")
        except Exception as e:
            logger.error(f"Failed to save state: {e}")
        
    async def register_workflow(self, workflow_id: str, config: Dict[str, Any]):
        """Register a new automation workflow"""
        self.workflows[workflow_id] = {
            'config': config,
            'status': 'initialized',
            'last_run': None,
            'run_count': 0,
            'error_count': 0,
            'created_at': datetime.now().isoformat()
        }
        self.circuit_breakers[workflow_id] = CircuitBreaker()
        self.metrics['total_workflows'] += 1
        logger.info(f"Workflow registered: {workflow_id}")
        self._save_state()
        
    async def start_workflow(self, workflow_id: str) -> bool:
        """Start a registered workflow with circuit breaker protection"""
        if workflow_id not in self.workflows:
            logger.error(f"Workflow {workflow_id} not found")
            return False
            
        breaker = self.circuit_breakers.get(workflow_id)
        if breaker and not breaker.can_execute():
            logger.warning(f"Circuit breaker prevents starting {workflow_id}")
            return False
            
        workflow = self.workflows[workflow_id]
        workflow['status'] = 'running'
        workflow['last_run'] = datetime.now().isoformat()
        workflow['run_count'] += 1
        
        logger.info(f"Starting workflow: {workflow_id}")
        return True
        
    async def stop_workflow(self, workflow_id: str):
        """Stop a running workflow"""
        if workflow_id in self.workflows:
            self.workflows[workflow_id]['status'] = 'stopped'
            logger.info(f"Stopped workflow: {workflow_id}")
            return True
        return False
        
    async def health_check(self, service_name: str) -> bool:
        """Perform health check with circuit breaker protection"""
        breaker = self.circuit_breakers.get(service_name)
        if not breaker:
            self.circuit_breakers[service_name] = CircuitBreaker()
            breaker = self.circuit_breakers[service_name]
            
        if not breaker.can_execute():
            logger.warning(f"Circuit breaker OPEN for {service_name} - skipping health check")
            return False
            
        try:
            # Simulate health check with potential failure
            logger.info(f"Health check: {service_name}")
            
            # Simulate 10% failure rate for testing
            import random
            if random.random() < 0.1:
                raise Exception("Simulated health check failure")
                
            self.health_status[service_name] = {
                'status': 'healthy',
                'last_check': datetime.now().isoformat(),
                'uptime_percentage': 99.9,
                'circuit_breaker': breaker.get_state()
            }
            breaker.record_success()
            return True
            
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {str(e)}")
            breaker.record_failure()
            self.health_status[service_name] = {
                'status': 'unhealthy',
                'last_check': datetime.now().isoformat(),
                'error': str(e),
                'circuit_breaker': breaker.get_state()
            }
            return False
            
    async def auto_recover(self, service_name: str, failure_type: str) -> bool:
        """Automatic recovery for failed services"""
        logger.warning(f"Initiating auto-recovery for {service_name} (Failure: {failure_type})")
        
        recovery_steps = {
            'service_crash': ['restart_service', 'verify_health', 'restore_connections'],
            'memory_leak': ['clear_cache', 'restart_service', 'scale_resources'],
            'network_failure': ['reset_connections', 'update_routing', 'verify_connectivity'],
            'database_connection': ['reconnect_pool', 'verify_credentials', 'test_queries']
        }
        
        steps = recovery_steps.get(failure_type, ['restart_service'])
        success = True
        
        try:
            for step in steps:
                logger.info(f"Recovery step: {step}")
                await asyncio.sleep(1)  # Simulate recovery action
                
            self.metrics['successful_recoveries'] += 1
            
        except Exception as e:
            logger.error(f"Recovery failed: {e}")
            success = False
            self.metrics['failed_recoveries'] += 1
            
        self.recovery_history.append({
            'service': service_name,
            'failure_type': failure_type,
            'timestamp': datetime.now().isoformat(),
            'steps_executed': steps,
            'success': success
        })
        
        # Trim history
        if len(self.recovery_history) > 1000:
            self.recovery_history = self.recovery_history[-1000:]
            
        logger.info(f"Auto-recovery {'completed' if success else 'failed'} for {service_name}")
        return success
        
    async def monitor_all_services(self):
        """Continuous monitoring with graceful shutdown support"""
        try:
            while self.is_running:
                logger.info("Running comprehensive health checks...")
                
                services = ['revenue-engine', 'database', 'api-gateway', 'cache', 'queue', 'storage']
                
                for service in services:
                    if not self.is_running:
                        break
                        
                    health = await self.health_check(service)
                    if not health:
                        await self.auto_recover(service, 'service_crash')
                        
                # Check for shutdown with timeout
                try:
                    await asyncio.wait_for(self.shutdown_event.wait(), timeout=15.0)
                    break
                except asyncio.TimeoutError:
                    continue
                    
        except asyncio.CancelledError:
            logger.info("Monitoring task cancelled gracefully")
        finally:
            logger.info("Monitoring loop exited")
            
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status with metrics"""
        uptime = (datetime.now() - self.metrics['uptime_start']).total_seconds()
        
        return {
            'workflows': self.workflows,
            'health_status': self.health_status,
            'recovery_history': self.recovery_history[-10:],
            'circuit_breakers': {k: v.get_state() for k, v in self.circuit_breakers.items()},
            'metrics': {
                **self.metrics,
                'uptime_seconds': uptime,
                'uptime_formatted': str(timedelta(seconds=int(uptime)))
            },
            'timestamp': datetime.now().isoformat()
        }
        
    async def graceful_shutdown(self, signal_name: str = "SIGTERM"):
        """Gracefully shutdown all services"""
        logger.info(f"="*60)
        logger.info(f"Received {signal_name} - Initiating graceful shutdown")
        logger.info(f"="*60)
        
        self.is_running = False
        self.shutdown_event.set()
        
        # Stop all workflows
        logger.info("Stopping all workflows...")
        for workflow_id in list(self.workflows.keys()):
            await self.stop_workflow(workflow_id)
            
        # Cancel all running tasks
        logger.info("Cancelling monitoring tasks...")
        for task in self.tasks:
            if not task.done():
                task.cancel()
                
        # Wait for tasks to complete
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
            
        # Save final state
        logger.info("Persisting final state...")
        self._save_state()
        
        # Print final metrics
        status = await self.get_system_status()
        logger.info(f"Final Metrics: {json.dumps(status['metrics'], indent=2)}")
        
        logger.info("Graceful shutdown complete")
        
    async def start(self):
        """Start the control plane orchestrator with signal handling"""
        logger.info("="*60)
        logger.info("ENHANCED CONTROL PLANE ORCHESTRATOR STARTING")
        logger.info("="*60)
        
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self.graceful_shutdown(s.name))
            )
            
        # Start monitoring task
        monitor_task = asyncio.create_task(self.monitor_all_services())
        self.tasks.append(monitor_task)
        
        # Register default workflows
        await self.register_workflow('revenue-automation', {'type': 'async', 'priority': 'high'})
        await self.register_workflow('data-processing', {'type': 'batch', 'priority': 'medium'})
        await self.register_workflow('backup-sync', {'type': 'scheduled', 'priority': 'low'})
        
        # Start workflows
        for workflow_id in self.workflows.keys():
            await self.start_workflow(workflow_id)
            
        logger.info("All systems operational - entering monitoring loop")
        
        # Wait for shutdown
        await self.shutdown_event.wait()
        
        # Final cleanup
        await self.graceful_shutdown("Manual")

if __name__ == "__main__":
    orchestrator = ControlPlaneOrchestrator()
    try:
        asyncio.run(orchestrator.start())
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received")
