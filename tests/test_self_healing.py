#!/usr/bin/env python3
"""
Tests for Self-Healing Monitor
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from autonomous_orchestrator.self_healing_monitor import SelfHealingMonitor

@pytest.fixture
def monitor():
    """Create monitor instance"""
    return SelfHealingMonitor()

def test_monitor_initialization(monitor):
    """Test monitor initializes correctly"""
    assert monitor.check_interval == 15
    print("✓ Monitor initialization test passed")

def test_check_health(monitor):
    """Test health check execution"""
    # Should not raise exception
    monitor.check_health()
    print("✓ Health check test passed")

def test_remediate(monitor):
    """Test remediation logic"""
    # Should not raise exception
    monitor.remediate("test-service")
    print("✓ Remediation test passed")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNING SELF-HEALING MONITOR TESTS")
    print("="*60 + "\n")
    pytest.main([__file__, "-v", "-s"])
