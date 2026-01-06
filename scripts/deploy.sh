#!/bin/bash

# Production Deployment Script
# Deploys the async automation framework to Kubernetes with zero downtime

set -e

echo "======================================"
echo "Async Automation Framework Deployment"
echo "======================================"

# Configuration
NAMESPACE="async-automation"
RELEASE_NAME="async-framework"
IMAGE_TAG="${1:-latest}"

echo "Deploying version: $IMAGE_TAG"

# Create namespace if it doesn't exist
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Apply Kubernetes configurations
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml -n $NAMESPACE
kubectl apply -f k8s/hpa.yaml -n $NAMESPACE

# Wait for rollout
echo "Waiting for deployment to complete..."
kubectl rollout status deployment/revenue-engine -n $NAMESPACE --timeout=300s

# Verify deployment
echo "Verifying deployment health..."
kubectl get pods -n $NAMESPACE
kubectl get svc -n $NAMESPACE
kubectl get hpa -n $NAMESPACE

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Access your service:"
kubectl get svc revenue-engine-svc -n $NAMESPACE
