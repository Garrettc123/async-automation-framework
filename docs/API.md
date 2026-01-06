# API Documentation

## Control Plane API

The Control Plane Orchestrator provides programmatic control over all automation workflows.

### Workflow Management

#### Register Workflow
```python
await orchestrator.register_workflow(
    workflow_id="custom-workflow",
    config={
        'type': 'async',
        'priority': 'high',
        'timeout': 300,
        'retry_policy': {
            'max_retries': 3,
            'backoff': 'exponential'
        }
    }
)
```

#### Start Workflow
```python
await orchestrator.start_workflow("custom-workflow")
```

#### Stop Workflow
```python
await orchestrator.stop_workflow("custom-workflow")
```

### Health Monitoring

#### Check Service Health
```python
is_healthy = await orchestrator.health_check("revenue-engine")
```

#### Get System Status
```python
status = await orchestrator.get_system_status()
print(status)
```

**Response:**
```json
{
    "workflows": {
        "revenue-automation": {
            "status": "running",
            "last_run": "2026-01-06T07:27:00",
            "run_count": 42,
            "error_count": 0
        }
    },
    "health_status": {
        "revenue-engine": {
            "status": "healthy",
            "uptime_percentage": 99.9
        }
    },
    "recovery_history": [],
    "timestamp": "2026-01-06T07:27:30"
}
```

### Auto-Recovery

#### Trigger Manual Recovery
```python
await orchestrator.auto_recover(
    service_name="database",
    failure_type="connection_timeout"
)
```

#### Recovery Types
- `service_crash`: Service process failure
- `memory_leak`: Memory exhaustion
- `network_failure`: Network connectivity issues
- `database_connection`: Database connection failures

## Revenue Engine API

### Process Revenue Stream
```python
engine = QuantumRevenueEngine()
await engine.process_stream("stream-name")
```

### Webhook Listener
```python
await engine.payment_webhook_listener()
```

## Self-Healing Monitor API

### Start Monitoring
```python
monitor = SelfHealingMonitor()
monitor.start()
```

### Manual Health Check
```python
monitor.check_health()
```

### Trigger Remediation
```python
monitor.remediate("service-name")
```

## Configuration

All API endpoints respect the configuration in `control-plane/config.yaml`.

### Custom Configuration
```python
import yaml

with open('control-plane/config.yaml') as f:
    config = yaml.safe_load(f)
    
# Modify as needed
config['monitoring']['health_check_interval'] = 30
```

## Error Handling

All API calls include comprehensive error handling:

```python
try:
    await orchestrator.start_workflow("workflow-id")
except WorkflowNotFoundError:
    logger.error("Workflow not registered")
except WorkflowAlreadyRunningError:
    logger.warning("Workflow already in progress")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
```

## Logging

All API operations are logged with timestamps and context:

```
2026-01-06 07:27:00 - ControlPlaneOrchestrator - INFO - Workflow registered: custom-workflow
2026-01-06 07:27:01 - ControlPlaneOrchestrator - INFO - Starting workflow: custom-workflow
2026-01-06 07:27:15 - SelfHealingMonitor - WARNING - database is UNHEALTHY. Initiating auto-remediation.
```
