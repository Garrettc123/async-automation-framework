# Setup Guide

## Prerequisites

- Python 3.9+
- Docker 20.10+
- kubectl 1.21+
- AWS CLI 2.0+ (for production deployment)
- Git

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Garrettc123/async-automation-framework.git
cd async-automation-framework
```

### 2. Run Setup Script
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- Create Python virtual environment
- Install all dependencies
- Build Docker image
- Validate configuration

### 3. Test Locally

#### Option A: Python Virtual Environment
```bash
source venv/bin/activate
python autonomous-orchestrator/quantum-revenue-engine.py
```

#### Option B: Docker
```bash
docker run -p 8080:8080 async-automation-framework:latest
```

#### Option C: Docker Compose
```bash
docker-compose up
```

## Production Deployment

### 1. Configure AWS Credentials
```bash
aws configure
```

### 2. Create EKS Cluster
```bash
eksctl create cluster --name async-automation --region us-west-2 --nodegroup-name standard-workers --node-type t3.medium --nodes 3 --nodes-min 3 --nodes-max 10
```

### 3. Configure kubectl
```bash
aws eks update-kubeconfig --name async-automation --region us-west-2
```

### 4. Set GitHub Secrets

In your GitHub repository, add these secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (e.g., us-west-2)

### 5. Deploy to Kubernetes
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh latest
```

## Configuration

Edit `control-plane/config.yaml` to customize:
- Health check intervals
- Auto-recovery strategies
- Service endpoints
- Resource limits
- Logging settings

## Monitoring

### Real-time Monitoring
```bash
chmod +x scripts/monitor.sh
./scripts/monitor.sh
```

### View Logs
```bash
kubectl logs -f deployment/revenue-engine -n async-automation
```

### Check Health
```bash
kubectl get pods -n async-automation
kubectl get hpa -n async-automation
```

## Troubleshooting

### Issue: Pods not starting
**Solution:**
```bash
kubectl describe pod <pod-name> -n async-automation
kubectl logs <pod-name> -n async-automation
```

### Issue: Auto-recovery not triggering
**Solution:**
- Check health probe configuration in `k8s/deployment.yaml`
- Verify monitoring interval in `control-plane/config.yaml`
- Review logs for error messages

### Issue: Deployment fails
**Solution:**
```bash
kubectl rollout status deployment/revenue-engine -n async-automation
kubectl rollout undo deployment/revenue-engine -n async-automation
```

## Next Steps

1. Customize workflows in `control-plane/orchestrator.py`
2. Add custom recovery strategies in `autonomous-orchestrator/self-healing-monitor.py`
3. Configure alerts and notifications
4. Set up monitoring dashboards
5. Implement backup strategies
