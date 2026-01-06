#!/usr/bin/env python3
"""
Interactive Debug Console
Provides REPL-style debugging interface for live system interaction
"""

import asyncio
import logging
import cmd
import json
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InteractiveDebugger")

class DebugConsole(cmd.Cmd):
    """Interactive debugging console"""
    
    intro = """
╔═══════════════════════════════════════════════════════════════╗
║        ASYNC AUTOMATION FRAMEWORK - DEBUG CONSOLE            ║
║                                                               ║
║  Type 'help' for available commands                          ║
║  Type 'exit' or 'quit' to close                              ║
╚═══════════════════════════════════════════════════════════════╝
    """
    prompt = "(debug) > "
    
    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator
        self.loop = asyncio.get_event_loop()
        
    def do_status(self, arg):
        """Get system status: status"""
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        print(json.dumps(status, indent=2))
        
    def do_workflows(self, arg):
        """List all workflows: workflows"""
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        workflows = status['workflows']
        
        print("\n" + "="*70)
        print(f"{'ID':<30} {'Status':<15} {'Run Count':<12} {'Errors'}")
        print("="*70)
        
        for wf_id, wf_data in workflows.items():
            print(f"{wf_id:<30} {wf_data['status']:<15} "
                  f"{wf_data['run_count']:<12} {wf_data.get('error_count', 0)}")
                  
        print("="*70 + "\n")
        
    def do_health(self, arg):
        """Show health status: health [service_name]"""
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        health = status['health_status']
        
        if arg:
            # Show specific service
            if arg in health:
                print(json.dumps(health[arg], indent=2))
            else:
                print(f"Service '{arg}' not found")
        else:
            # Show all services
            print("\n" + "="*70)
            print(f"{'Service':<25} {'Status':<15} {'Last Check'}")
            print("="*70)
            
            for svc_name, svc_data in health.items():
                status_icon = '✓' if svc_data['status'] == 'healthy' else '✗'
                print(f"{status_icon} {svc_name:<23} {svc_data['status']:<15} "
                      f"{svc_data['last_check']}")
                      
            print("="*70 + "\n")
            
    def do_circuits(self, arg):
        """Show circuit breaker status: circuits"""
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        breakers = status['circuit_breakers']
        
        print("\n" + "="*70)
        print(f"{'Service':<30} {'State':<15} {'Failures'}")
        print("="*70)
        
        for svc, cb_data in breakers.items():
            state_icon = {'closed': '✓', 'open': '✗', 'half_open': '⟳'}.get(cb_data['state'], '?')
            print(f"{state_icon} {svc:<28} {cb_data['state']:<15} {cb_data['failure_count']}")
            
        print("="*70 + "\n")
        
    def do_recovery(self, arg):
        """Show recovery history: recovery [count]"""
        count = int(arg) if arg else 10
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        history = status['recovery_history'][-count:]
        
        print("\n" + "="*70)
        print("RECENT RECOVERY EVENTS")
        print("="*70)
        
        for event in history:
            success_icon = '✓' if event['success'] else '✗'
            print(f"\n{success_icon} {event['service']} - {event['failure_type']}")
            print(f"  Time: {event['timestamp']}")
            print(f"  Steps: {', '.join(event['steps_executed'])}")
            
        print("\n" + "="*70 + "\n")
        
    def do_start(self, arg):
        """Start a workflow: start <workflow_id>"""
        if not arg:
            print("Usage: start <workflow_id>")
            return
            
        result = self.loop.run_until_complete(self.orchestrator.start_workflow(arg))
        if result:
            print(f"✓ Workflow '{arg}' started successfully")
        else:
            print(f"✗ Failed to start workflow '{arg}'")
            
    def do_stop(self, arg):
        """Stop a workflow: stop <workflow_id>"""
        if not arg:
            print("Usage: stop <workflow_id>")
            return
            
        result = self.loop.run_until_complete(self.orchestrator.stop_workflow(arg))
        if result:
            print(f"✓ Workflow '{arg}' stopped successfully")
        else:
            print(f"✗ Failed to stop workflow '{arg}'")
            
    def do_check(self, arg):
        """Run health check: check <service_name>"""
        if not arg:
            print("Usage: check <service_name>")
            return
            
        result = self.loop.run_until_complete(self.orchestrator.health_check(arg))
        if result:
            print(f"✓ Health check passed for '{arg}'")
        else:
            print(f"✗ Health check failed for '{arg}'")
            
    def do_recover(self, arg):
        """Trigger recovery: recover <service_name> <failure_type>"""
        parts = arg.split()
        if len(parts) != 2:
            print("Usage: recover <service_name> <failure_type>")
            print("Failure types: service_crash, memory_leak, network_failure, database_connection")
            return
            
        service, failure = parts
        result = self.loop.run_until_complete(self.orchestrator.auto_recover(service, failure))
        if result:
            print(f"✓ Recovery completed for '{service}'")
        else:
            print(f"✗ Recovery failed for '{service}'")
            
    def do_metrics(self, arg):
        """Show system metrics: metrics"""
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        metrics = status['metrics']
        
        print("\n" + "="*70)
        print("SYSTEM METRICS")
        print("="*70)
        print(f"Total Workflows: {metrics['total_workflows']}")
        print(f"Successful Recoveries: {metrics['successful_recoveries']}")
        print(f"Failed Recoveries: {metrics['failed_recoveries']}")
        print(f"Uptime: {metrics['uptime_formatted']}")
        print(f"Uptime (seconds): {metrics['uptime_seconds']:.0f}")
        print("="*70 + "\n")
        
    def do_export(self, arg):
        """Export state to file: export [filename]"""
        filename = arg if arg else f"debug_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        status = self.loop.run_until_complete(self.orchestrator.get_system_status())
        
        try:
            with open(filename, 'w') as f:
                json.dump(status, f, indent=2)
            print(f"✓ State exported to {filename}")
        except Exception as e:
            print(f"✗ Export failed: {e}")
            
    def do_clear(self, arg):
        """Clear screen: clear"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.intro)
        
    def do_exit(self, arg):
        """Exit debugger: exit"""
        print("Goodbye!")
        return True
        
    def do_quit(self, arg):
        """Exit debugger: quit"""
        return self.do_exit(arg)
        
    def do_EOF(self, arg):
        """Handle Ctrl+D"""
        print()
        return self.do_exit(arg)

async def main():
    """Start interactive debugger"""
    from control_plane.orchestrator_enhanced import ControlPlaneOrchestrator
    
    # Create orchestrator
    orchestrator = ControlPlaneOrchestrator()
    
    # Register some test workflows
    await orchestrator.register_workflow('test-workflow-1', {'type': 'test'})
    await orchestrator.register_workflow('test-workflow-2', {'type': 'test'})
    
    # Start console
    console = DebugConsole(orchestrator)
    console.cmdloop()

if __name__ == "__main__":
    asyncio.run(main())
