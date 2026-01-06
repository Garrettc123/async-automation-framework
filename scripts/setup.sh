#!/bin/bash

# Async Automation Framework Setup Script
# This script sets up the entire framework for local development and production

set -e  # Exit on any error

echo "======================================"
echo "Async Automation Framework Setup"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function print_success {
    echo -e "${GREEN}✓ $1${NC}"
}

function print_error {
    echo -e "${RED}✗ $1${NC}"
}

function print_info {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check prerequisites
print_info "Checking prerequisites..."

command -v python3 >/dev/null 2>&1 || { print_error "Python 3 is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { print_error "Docker is required but not installed."; exit 1; }
command -v kubectl >/dev/null 2>&1 || print_info "kubectl not found - Kubernetes features will be limited"

print_success "Prerequisites check completed"

# Create virtual environment
print_info "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
print_success "Virtual environment created"

# Install dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_success "Dependencies installed"

# Create necessary directories
print_info "Creating directory structure..."
mkdir -p logs
mkdir -p data
mkdir -p backups
print_success "Directories created"

# Build Docker image
print_info "Building Docker image..."
docker build -t async-automation-framework:latest .
print_success "Docker image built"

# Test configuration
print_info "Testing configuration..."
python3 -c "import yaml; yaml.safe_load(open('control-plane/config.yaml'))"
print_success "Configuration validated"

echo ""
echo "======================================"
echo "Setup Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run locally: python autonomous-orchestrator/quantum-revenue-engine.py"
echo "3. Run with Docker: docker run -p 8080:8080 async-automation-framework:latest"
echo "4. Deploy to Kubernetes: kubectl apply -f k8s/"
echo ""
