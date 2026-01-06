#!/bin/bash

################################################################################
# UNIFIED COMMAND CENTER - Master Control for All Systems
# Created: January 6, 2026
# Purpose: Single entry point to manage entire infrastructure
################################################################################

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

show_banner() {
    clear
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║              UNIFIED COMMAND CENTER v1.0                          ║
║         Enterprise Automation & Orchestration System              ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

show_menu() {
    echo ""
    echo -e "${BLUE}═══ MAIN MENU ═══${NC}"
    echo "1.  🚀 Full System Deployment (End-to-End)"
    echo "2.  ⚙️  Infrastructure Setup (AWS/K8s)"
    echo "3.  🔑 Configure Secrets & Credentials"
    echo "4.  🐳 Build & Test Docker Containers"
    echo "5.  📊 System Health Dashboard"
    echo "6.  📈 Monitor All Services"
    echo "7.  🔄 Deploy Specific Service"
    echo "8.  🛑 Stop All Services"
    echo "9.  📝 View Logs (Real-time)"
    echo "10. 🔧 Run Tests Suite"
    echo "11. 🔐 Security Scan"
    echo "12. 📦 Backup & Recovery"
    echo "13. 🔄 Update All Systems"
    echo "14. 📊 Generate Reports"
    echo "15. ⚡ Quick Actions Menu"
    echo "0.  ❌ Exit"
    echo ""
    echo -ne "${YELLOW}Select option: ${NC}"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    local missing_tools=()
    
    command -v docker >/dev/null 2>&1 || missing_tools+=("docker")
    command -v kubectl >/dev/null 2>&1 || missing_tools+=("kubectl")
    command -v aws >/dev/null 2>&1 || missing_tools+=("aws-cli")
    command -v python3 >/dev/null 2>&1 || missing_tools+=("python3")
    command -v git >/dev/null 2>&1 || missing_tools+=("git")
    
    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_warning "Missing tools: ${missing_tools[*]}"
        log_info "Installing missing tools..."
        # Auto-install based on OS
        if [[ "$OSTYPE" == "darwin"* ]]; then
            brew install ${missing_tools[*]}
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            sudo apt-get update && sudo apt-get install -y ${missing_tools[*]}
        fi
    fi
    
    log_success "Prerequisites check complete"
}

full_deployment() {
    log_info "Starting full system deployment..."
    
    echo ""
    echo -e "${YELLOW}This will deploy:${NC}"
    echo "  • AWS Infrastructure (EKS, ECR, VPC)"
    echo "  • Kubernetes Cluster"
    echo "  • All Microservices"
    echo "  • Monitoring Stack"
    echo "  • Security Configurations"
    echo ""
    read -p "Continue? (yes/no): " confirm
    
    if [[ $confirm != "yes" ]]; then
        log_warning "Deployment cancelled"
        return
    fi
    
    # Step 1: Infrastructure
    log_info "[1/5] Setting up AWS infrastructure..."
    bash scripts/setup.sh
    
    # Step 2: Build containers
    log_info "[2/5] Building Docker containers..."
    docker build -t async-framework:latest .
    
    # Step 3: Configure secrets
    log_info "[3/5] Configuring secrets..."
    configure_secrets
    
    # Step 4: Deploy to Kubernetes
    log_info "[4/5] Deploying to Kubernetes..."
    bash scripts/deploy.sh
    
    # Step 5: Verify deployment
    log_info "[5/5] Verifying deployment..."
    kubectl get pods --all-namespaces
    
    log_success "Full deployment complete!"
    log_info "Access dashboard at: http://localhost:8080"
}

infrastructure_setup() {
    log_info "Setting up infrastructure..."
    
    echo "Select infrastructure:"
    echo "1. AWS (EKS + ECR)"
    echo "2. Local (Docker + Minikube)"
    echo "3. Custom"
    read -p "Choice: " infra_choice
    
    case $infra_choice in
        1)
            log_info "Setting up AWS infrastructure..."
            # Create EKS cluster
            aws eks create-cluster --name automation-cluster \
                --role-arn arn:aws:iam::ACCOUNT:role/eks-service-role \
                --resources-vpc-config subnetIds=subnet-xxx,subnet-yyy
            
            # Create ECR repository
            aws ecr create-repository --repository-name async-framework
            
            log_success "AWS infrastructure created"
            ;;
        2)
            log_info "Setting up local environment..."
            minikube start --cpus 4 --memory 8192
            log_success "Local environment ready"
            ;;
        3)
            log_info "Custom setup - edit scripts/setup.sh"
            ;;
    esac
}

configure_secrets() {
    log_info "Configuring secrets and credentials..."
    
    if [ ! -f .env ]; then
        log_info "Creating .env file from template..."
        cat > .env << EOF
# AWS Credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-west-2

# Application Secrets
DATABASE_URL=
REDIS_URL=
API_KEY=
WEBHOOK_URL=

# Revenue Stream APIs
STRIPE_API_KEY=
SHOPIFY_API_KEY=
AFFILIATE_API_KEY=
AD_NETWORK_API_KEY=
SAAS_API_KEY=
EOF
        log_warning "Please edit .env file with your credentials"
        ${EDITOR:-nano} .env
    fi
    
    # Apply secrets to Kubernetes
    kubectl create secret generic app-secrets --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
    
    log_success "Secrets configured"
}

build_containers() {
    log_info "Building Docker containers..."
    
    docker build -t async-framework:latest .
    docker tag async-framework:latest async-framework:$(date +%Y%m%d-%H%M%S)
    
    log_success "Containers built successfully"
    
    read -p "Push to registry? (yes/no): " push_confirm
    if [[ $push_confirm == "yes" ]]; then
        docker push async-framework:latest
    fi
}

system_health() {
    log_info "System Health Dashboard"
    echo ""
    
    # Kubernetes status
    echo -e "${BLUE}Kubernetes Cluster:${NC}"
    kubectl cluster-info
    echo ""
    
    # Pods status
    echo -e "${BLUE}Pods Status:${NC}"
    kubectl get pods --all-namespaces
    echo ""
    
    # Services status
    echo -e "${BLUE}Services:${NC}"
    kubectl get services --all-namespaces
    echo ""
    
    # Resource usage
    echo -e "${BLUE}Resource Usage:${NC}"
    kubectl top nodes 2>/dev/null || log_warning "Metrics server not available"
    
    read -p "Press Enter to continue..."
}

monitor_services() {
    log_info "Launching monitoring dashboard..."
    
    # Start monitoring script in background
    bash scripts/monitor.sh &
    MONITOR_PID=$!
    
    log_info "Monitoring active (PID: $MONITOR_PID)"
    log_info "Press Ctrl+C to stop monitoring"
    
    wait $MONITOR_PID
}

deploy_service() {
    log_info "Available services:"
    kubectl get deployments --all-namespaces
    echo ""
    
    read -p "Enter service name to deploy: " service_name
    
    if [ -z "$service_name" ]; then
        log_error "Service name required"
        return
    fi
    
    log_info "Deploying $service_name..."
    kubectl rollout restart deployment/$service_name
    kubectl rollout status deployment/$service_name
    
    log_success "$service_name deployed"
}

stop_all() {
    log_warning "Stopping all services..."
    
    read -p "Are you sure? This will stop EVERYTHING (yes/no): " confirm
    if [[ $confirm != "yes" ]]; then
        log_info "Cancelled"
        return
    fi
    
    kubectl delete deployments --all --all-namespaces
    docker stop $(docker ps -q) 2>/dev/null || true
    
    log_success "All services stopped"
}

view_logs() {
    log_info "Available pods:"
    kubectl get pods --all-namespaces
    echo ""
    
    read -p "Enter pod name: " pod_name
    read -p "Enter namespace (default: default): " namespace
    namespace=${namespace:-default}
    
    log_info "Streaming logs for $pod_name..."
    kubectl logs -f $pod_name -n $namespace
}

run_tests() {
    log_info "Running test suite..."
    bash scripts/run_tests.sh
    
    log_info "Test results:"
    cat test_results.txt 2>/dev/null || log_warning "No test results found"
}

security_scan() {
    log_info "Running security scan..."
    
    # Container security scan
    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
        aquasec/trivy image async-framework:latest
    
    # Kubernetes security scan
    kubectl auth can-i --list
    
    log_success "Security scan complete"
}

backup_recovery() {
    echo "1. Backup current state"
    echo "2. Restore from backup"
    echo "3. List backups"
    read -p "Choice: " backup_choice
    
    case $backup_choice in
        1)
            log_info "Creating backup..."
            timestamp=$(date +%Y%m%d-%H%M%S)
            kubectl get all --all-namespaces -o yaml > backup-$timestamp.yaml
            log_success "Backup saved: backup-$timestamp.yaml"
            ;;
        2)
            ls -1 backup-*.yaml
            read -p "Enter backup file: " backup_file
            kubectl apply -f $backup_file
            log_success "Restored from $backup_file"
            ;;
        3)
            ls -lh backup-*.yaml
            ;;
    esac
}

update_systems() {
    log_info "Updating all systems..."
    
    # Pull latest code
    git pull origin main
    
    # Rebuild containers
    docker build -t async-framework:latest .
    
    # Rolling update
    kubectl set image deployment/revenue-engine revenue-engine=async-framework:latest
    
    log_success "Systems updated"
}

generate_reports() {
    log_info "Generating system reports..."
    
    timestamp=$(date +%Y%m%d-%H%M%S)
    report_file="report-$timestamp.txt"
    
    {
        echo "System Report - $timestamp"
        echo "="*50
        echo ""
        echo "Cluster Info:"
        kubectl cluster-info
        echo ""
        echo "Resource Usage:"
        kubectl top nodes
        echo ""
        echo "Pod Status:"
        kubectl get pods --all-namespaces
        echo ""
        echo "Recent Events:"
        kubectl get events --sort-by='.lastTimestamp'
    } > $report_file
    
    log_success "Report saved: $report_file"
    cat $report_file
}

quick_actions() {
    echo ""
    echo -e "${BLUE}═══ QUICK ACTIONS ═══${NC}"
    echo "1. Restart all pods"
    echo "2. Scale deployment"
    echo "3. Update config"
    echo "4. Emergency rollback"
    echo "5. Clear cache"
    read -p "Choice: " qa_choice
    
    case $qa_choice in
        1)
            kubectl rollout restart deployment --all
            ;;
        2)
            read -p "Deployment name: " dep_name
            read -p "Replicas: " replicas
            kubectl scale deployment/$dep_name --replicas=$replicas
            ;;
        4)
            kubectl rollout undo deployment/revenue-engine
            ;;
        5)
            kubectl exec -it $(kubectl get pod -l app=cache -o jsonpath="{.items[0].metadata.name}") -- redis-cli FLUSHALL
            ;;
    esac
}

# Main execution
main() {
    show_banner
    check_prerequisites
    
    while true; do
        show_menu
        read choice
        
        case $choice in
            1) full_deployment ;;
            2) infrastructure_setup ;;
            3) configure_secrets ;;
            4) build_containers ;;
            5) system_health ;;
            6) monitor_services ;;
            7) deploy_service ;;
            8) stop_all ;;
            9) view_logs ;;
            10) run_tests ;;
            11) security_scan ;;
            12) backup_recovery ;;
            13) update_systems ;;
            14) generate_reports ;;
            15) quick_actions ;;
            0) 
                log_info "Exiting command center..."
                exit 0
                ;;
            *) 
                log_error "Invalid option"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
