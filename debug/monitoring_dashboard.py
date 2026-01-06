#!/usr/bin/env python3
"""
Real-Time Monitoring Dashboard
Provides live visualization of system health, workflows, and metrics
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import json
from collections import deque

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MonitoringDashboard")

class MonitoringDashboard:
    """Real-time monitoring and visualization"""
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.metrics_history = deque(maxlen=100)
        self.alert_threshold = {
            'error_rate': 0.05,  # 5%
            'response_time': 1000,  # ms
            'cpu_usage': 80,  # %
            'memory_usage': 85  # %
        }
        self.alerts = []
        
    async def collect_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics"""
        status = await self.orchestrator.get_system_status()
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'workflows': {
                'total': len(status['workflows']),
                'running': sum(1 for w in status['workflows'].values() if w['status'] == 'running'),
                'stopped': sum(1 for w in status['workflows'].values() if w['status'] == 'stopped'),
                'errors': sum(w.get('error_count', 0) for w in status['workflows'].values())
            },
            'health': {
                'healthy': sum(1 for h in status['health_status'].values() if h['status'] == 'healthy'),
                'unhealthy': sum(1 for h in status['health_status'].values() if h['status'] == 'unhealthy'),
                'total': len(status['health_status'])
            },
            'circuit_breakers': {
                'closed': sum(1 for cb in status['circuit_breakers'].values() if cb['state'] == 'closed'),
                'open': sum(1 for cb in status['circuit_breakers'].values() if cb['state'] == 'open'),
                'half_open': sum(1 for cb in status['circuit_breakers'].values() if cb['state'] == 'half_open')
            },
            'recovery': {
                'successful': status['metrics']['successful_recoveries'],
                'failed': status['metrics']['failed_recoveries'],
                'total': status['metrics']['successful_recoveries'] + status['metrics']['failed_recoveries']
            },
            'uptime': status['metrics']['uptime_formatted']
        }
        
        self.metrics_history.append(metrics)
        return metrics
        
    async def check_alerts(self, metrics: Dict[str, Any]):
        """Check for alert conditions"""
        # Check error rate
        total_workflows = metrics['workflows']['total']
        if total_workflows > 0:
            error_rate = metrics['workflows']['errors'] / total_workflows
            if error_rate > self.alert_threshold['error_rate']:
                self.alerts.append({
                    'severity': 'WARNING',
                    'message': f"High error rate: {error_rate:.2%}",
                    'timestamp': datetime.now().isoformat()
                })
                
        # Check unhealthy services
        if metrics['health']['unhealthy'] > 0:
            self.alerts.append({
                'severity': 'CRITICAL',
                'message': f"{metrics['health']['unhealthy']} services unhealthy",
                'timestamp': datetime.now().isoformat()
            })
            
        # Check circuit breakers
        if metrics['circuit_breakers']['open'] > 0:
            self.alerts.append({
                'severity': 'WARNING',
                'message': f"{metrics['circuit_breakers']['open']} circuit breakers OPEN",
                'timestamp': datetime.now().isoformat()
            })
            
        # Trim alerts
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
            
    def render_dashboard(self, metrics: Dict[str, Any]):
        """Render text-based dashboard"""
        print("\n" + "="*80)
        print(f"{'SYSTEM MONITORING DASHBOARD':^80}")
        print(f"{'Last Updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^80}")
        print("="*80)
        
        # Workflows Section
        print(f"\n{'WORKFLOWS':-^80}")
        print(f"  Total: {metrics['workflows']['total']}  |  "
              f"Running: {metrics['workflows']['running']}  |  "
              f"Stopped: {metrics['workflows']['stopped']}  |  "
              f"Errors: {metrics['workflows']['errors']}")
        
        # Health Status
        print(f"\n{'SERVICE HEALTH':-^80}")
        total = metrics['health']['total']
        healthy = metrics['health']['healthy']
        unhealthy = metrics['health']['unhealthy']
        health_pct = (healthy / total * 100) if total > 0 else 0
        
        health_bar = self._create_bar(health_pct, 40)
        print(f"  {health_bar} {health_pct:.1f}%")
        print(f"  Healthy: {healthy} | Unhealthy: {unhealthy} | Total: {total}")
        
        # Circuit Breakers
        print(f"\n{'CIRCUIT BREAKERS':-^80}")
        print(f"  Closed: {metrics['circuit_breakers']['closed']}  |  "
              f"Open: {metrics['circuit_breakers']['open']}  |  "
              f"Half-Open: {metrics['circuit_breakers']['half_open']}")
        
        # Recovery Stats
        print(f"\n{'AUTO-RECOVERY':-^80}")
        total_recoveries = metrics['recovery']['total']
        successful = metrics['recovery']['successful']
        success_rate = (successful / total_recoveries * 100) if total_recoveries > 0 else 0
        
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Successful: {successful} | Failed: {metrics['recovery']['failed']} | Total: {total_recoveries}")
        
        # System Uptime
        print(f"\n{'SYSTEM INFO':-^80}")
        print(f"  Uptime: {metrics['uptime']}")
        
        # Recent Alerts
        if self.alerts:
            print(f"\n{'RECENT ALERTS':-^80}")
            for alert in self.alerts[-5:]:
                severity_color = alert['severity']
                print(f"  [{severity_color}] {alert['message']} - {alert['timestamp']}")
        
        print("\n" + "="*80 + "\n")
        
    def _create_bar(self, percentage: float, width: int = 40) -> str:
        """Create ASCII progress bar"""
        filled = int(width * percentage / 100)
        bar = '█' * filled + '░' * (width - filled)
        return f"[{bar}]"
        
    async def start_monitoring(self, interval: int = 5):
        """Start continuous monitoring loop"""
        logger.info("Starting monitoring dashboard...")
        
        try:
            while True:
                # Collect metrics
                metrics = await self.collect_metrics()
                
                # Check for alerts
                await self.check_alerts(metrics)
                
                # Render dashboard
                self.render_dashboard(metrics)
                
                # Wait for next update
                await asyncio.sleep(interval)
                
        except asyncio.CancelledError:
            logger.info("Monitoring dashboard stopped")
            
    async def export_metrics(self, filename: str = "metrics_export.json"):
        """Export metrics history to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(list(self.metrics_history), f, indent=2)
            logger.info(f"Metrics exported to {filename}")
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")

if __name__ == "__main__":
    # Example usage
    from control_plane.orchestrator_enhanced import ControlPlaneOrchestrator
    
    async def main():
        orchestrator = ControlPlaneOrchestrator()
        dashboard = MonitoringDashboard(orchestrator)
        
        # Start orchestrator in background
        orch_task = asyncio.create_task(orchestrator.start())
        
        # Start monitoring
        await dashboard.start_monitoring(interval=5)
        
    asyncio.run(main())
