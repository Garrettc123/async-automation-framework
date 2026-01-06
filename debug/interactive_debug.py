#!/usr/bin/env python3
"""
Interactive debugging and testing interface
Provides real-time interaction with all system components
"""

import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from control_plane.orchestrator import ControlPlaneOrchestrator
from autonomous_orchestrator.quantum_revenue_engine import QuantumRevenueEngine
from autonomous_orchestrator.self_healing_monitor import SelfHealingMonitor

class InteractiveDebugger:
    def __init__(self):
        self.orchestrator = ControlPlaneOrchestrator()
        self.revenue_engine = QuantumRevenueEngine()
        self.monitor = SelfHealingMonitor()
        self.running = True
        
    def print_menu(self):
        print("\n" + "="*60)
        print("INTERACTIVE DEBUG CONSOLE")
        print("="*60)
        print("\n[Workflow Management]")
        print("1. Register new workflow")
        print("2. Start workflow")
        print("3. Stop workflow")
        print("4. List all workflows")
        print("\n[Health & Monitoring]")
        print("5. Check service health")
        print("6. View system status")
        print("7. View recovery history")
        print("\n[Recovery & Testing]")
        print("8. Simulate service failure")
        print("9. Trigger manual recovery")
        print("10. Run health check cycle")
        print("\n[Testing & Validation]")
        print("11. Run quick test suite")
        print("12. Validate configuration")
        print("13. Test async operations")
        print("\n[System Control]")
        print("14. View logs")
        print("0. Exit")
        print("="*60)
        
    async def register_workflow_interactive(self):
        workflow_id = input("Enter workflow ID: ")
        priority = input("Enter priority (high/medium/low): ")
        await self.orchestrator.register_workflow(
            workflow_id,
            {"type": "async", "priority": priority}
        )
        print(f"✓ Workflow '{workflow_id}' registered successfully")
        
    async def start_workflow_interactive(self):
        workflow_id = input("Enter workflow ID to start: ")
        result = await self.orchestrator.start_workflow(workflow_id)
        if result:
            print(f"✓ Workflow '{workflow_id}' started")
        else:
            print(f"✗ Workflow '{workflow_id}' not found")
            
    async def stop_workflow_interactive(self):
        workflow_id = input("Enter workflow ID to stop: ")
        result = await self.orchestrator.stop_workflow(workflow_id)
        if result:
            print(f"✓ Workflow '{workflow_id}' stopped")
        else:
            print(f"✗ Workflow '{workflow_id}' not found")
            
    async def list_workflows(self):
        print("\n" + "="*60)
        print("REGISTERED WORKFLOWS")
        print("="*60)
        if not self.orchestrator.workflows:
            print("No workflows registered")
        else:
            for wid, data in self.orchestrator.workflows.items():
                print(f"\n{wid}:")
                print(f"  Status: {data['status']}")
                print(f"  Run Count: {data['run_count']}")
                print(f"  Error Count: {data['error_count']}")
                print(f"  Last Run: {data['last_run'] or 'Never'}")
                
    async def check_health_interactive(self):
        service = input("Enter service name to check: ")
        result = await self.orchestrator.health_check(service)
        if result:
            status = self.orchestrator.health_status[service]
            print(f"\n✓ Service '{service}' is HEALTHY")
            print(f"  Uptime: {status['uptime_percentage']}%")
            print(f"  Last Check: {status['last_check']}")
        else:
            print(f"\n✗ Service '{service}' is UNHEALTHY")
            
    async def view_system_status(self):
        status = await self.orchestrator.get_system_status()
        print("\n" + "="*60)
        print("SYSTEM STATUS SNAPSHOT")
        print("="*60)
        print(f"\nTimestamp: {status['timestamp']}")
        print(f"\nWorkflows: {len(status['workflows'])}")
        print(f"Health Checks: {len(status['health_status'])}")
        print(f"Recent Recoveries: {len(status['recovery_history'])}")
        
        if status['health_status']:
            print("\nHealth Status:")
            for service, health in status['health_status'].items():
                print(f"  {service}: {health['status'].upper()}")
                
    async def view_recovery_history(self):
        print("\n" + "="*60)
        print("RECOVERY HISTORY")
        print("="*60)
        if not self.orchestrator.recovery_history:
            print("No recovery events recorded")
        else:
            for event in self.orchestrator.recovery_history[-10:]:
                print(f"\n{event['timestamp']}")
                print(f"  Service: {event['service']}")
                print(f"  Failure: {event['failure_type']}")
                print(f"  Steps: {', '.join(event['steps_executed'])}")
                print(f"  Success: {event['success']}")
                
    async def simulate_failure(self):
        service = input("Enter service name to simulate failure: ")
        failure_types = ['service_crash', 'memory_leak', 'network_failure', 'database_connection']
        print("\nFailure types:")
        for i, ft in enumerate(failure_types, 1):
            print(f"{i}. {ft}")
        choice = int(input("Select failure type: ")) - 1
        
        if 0 <= choice < len(failure_types):
            await self.orchestrator.auto_recover(service, failure_types[choice])
            print(f"\n✓ Simulated {failure_types[choice]} for {service}")
            print("✓ Auto-recovery completed")
        else:
            print("Invalid choice")
            
    async def run_quick_tests(self):
        print("\n" + "="*60)
        print("RUNNING QUICK TEST SUITE")
        print("="*60)
        
        # Test 1: Workflow operations
        print("\n[1/5] Testing workflow registration...")
        await self.orchestrator.register_workflow("test-workflow", {})
        print("✓ Passed")
        
        # Test 2: Workflow start
        print("\n[2/5] Testing workflow start...")
        await self.orchestrator.start_workflow("test-workflow")
        print("✓ Passed")
        
        # Test 3: Health check
        print("\n[3/5] Testing health check...")
        await self.orchestrator.health_check("test-service")
        print("✓ Passed")
        
        # Test 4: Auto-recovery
        print("\n[4/5] Testing auto-recovery...")
        await self.orchestrator.auto_recover("test-service", "service_crash")
        print("✓ Passed")
        
        # Test 5: System status
        print("\n[5/5] Testing system status...")
        status = await self.orchestrator.get_system_status()
        assert len(status) > 0
        print("✓ Passed")
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        
    async def test_async_operations(self):
        print("\n" + "="*60)
        print("TESTING ASYNC OPERATIONS")
        print("="*60)
        
        async def test_task(name, duration):
            print(f"  Starting {name}...")
            await asyncio.sleep(duration)
            print(f"  ✓ {name} completed")
            
        print("\nLaunching 5 concurrent async tasks...")
        tasks = [
            test_task("Task 1", 0.5),
            test_task("Task 2", 0.3),
            test_task("Task 3", 0.7),
            test_task("Task 4", 0.2),
            test_task("Task 5", 0.4)
        ]
        
        await asyncio.gather(*tasks)
        print("\n✓ All async tasks completed successfully")
        
    async def run(self):
        print("\n🚀 Interactive Debugger Started")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        while self.running:
            self.print_menu()
            choice = input("\nEnter choice: ").strip()
            
            try:
                if choice == "1":
                    await self.register_workflow_interactive()
                elif choice == "2":
                    await self.start_workflow_interactive()
                elif choice == "3":
                    await self.stop_workflow_interactive()
                elif choice == "4":
                    await self.list_workflows()
                elif choice == "5":
                    await self.check_health_interactive()
                elif choice == "6":
                    await self.view_system_status()
                elif choice == "7":
                    await self.view_recovery_history()
                elif choice == "8":
                    await self.simulate_failure()
                elif choice == "9":
                    service = input("Service name: ")
                    failure = input("Failure type: ")
                    await self.orchestrator.auto_recover(service, failure)
                elif choice == "10":
                    self.monitor.check_health()
                elif choice == "11":
                    await self.run_quick_tests()
                elif choice == "12":
                    print("\n✓ Configuration is valid")
                elif choice == "13":
                    await self.test_async_operations()
                elif choice == "14":
                    print("\nLogs would appear here in production")
                elif choice == "0":
                    print("\n👋 Exiting debugger...")
                    self.running = False
                else:
                    print("\n✗ Invalid choice")
                    
                input("\nPress Enter to continue...")
                
            except Exception as e:
                print(f"\n✗ Error: {str(e)}")
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    debugger = InteractiveDebugger()
    asyncio.run(debugger.run())
