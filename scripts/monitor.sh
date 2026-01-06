#!/bin/bash

# Real-time Monitoring Script
# Monitor all services and auto-healing operations

NAMESPACE="async-automation"

echo "======================================"
echo "Async Automation Framework Monitor"
echo "======================================"
echo ""

while true; do
    clear
    echo "=== Deployment Status ==="
    kubectl get deployments -n $NAMESPACE 2>/dev/null || echo "No deployments found"
    
    echo ""
    echo "=== Pod Status ==="
    kubectl get pods -n $NAMESPACE 2>/dev/null || echo "No pods found"
    
    echo ""
    echo "=== HPA Status ==="
    kubectl get hpa -n $NAMESPACE 2>/dev/null || echo "No HPA found"
    
    echo ""
    echo "=== Recent Events ==="
    kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -5 2>/dev/null || echo "No events"
    
    echo ""
    echo "Refreshing in 5 seconds... (Press Ctrl+C to exit)"
    sleep 5
done
