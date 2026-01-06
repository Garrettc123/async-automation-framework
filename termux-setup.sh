#!/data/data/com.termux/files/usr/bin/bash

################################################################################
# TERMUX MOBILE DEPLOYMENT SETUP
# Purpose: Run enterprise automation from Android/Termux
# Platform: Android (Termux)
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
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║          TERMUX MOBILE COMMAND CENTER v1.0                    ║
║        Enterprise Automation on Android Device                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

check_termux() {
    if [ ! -d "/data/data/com.termux" ]; then
        log_error "This script must be run in Termux!"
        log_info "Install Termux from F-Droid: https://f-droid.org/packages/com.termux/"
        exit 1
    fi
    log_success "Termux environment detected"
}

install_prerequisites() {
    log_info "Installing Termux prerequisites..."
    
    # Update packages
    pkg update -y
    pkg upgrade -y
    
    # Install essential packages
    log_info "Installing essential tools..."
    pkg install -y \
        python \
        python-pip \
        git \
        openssh \
        curl \
        wget \
        nano \
        vim \
        tmux \
        tree \
        nodejs \
        root-repo
    
    # Install Python packages
    log_info "Installing Python dependencies..."
    pip install --upgrade pip
    pip install \
        aiohttp \
        asyncio \
        requests \
        python-dotenv \
        pyyaml \
        rich \
        click
    
    log_success "Prerequisites installed"
}

setup_storage() {
    log_info "Setting up storage access..."
    
    if [ ! -d "~/storage" ]; then
        termux-setup-storage
        log_success "Storage access granted"
    else
        log_info "Storage already configured"
    fi
}

clone_repository() {
    log_info "Cloning automation framework..."
    
    if [ -d "async-automation-framework" ]; then
        log_warning "Repository already exists, pulling latest..."
        cd async-automation-framework
        git pull origin main
        cd ..
    else
        git clone https://github.com/Garrettc123/async-automation-framework.git
    fi
    
    log_success "Repository ready"
}

install_lightweight_docker() {
    log_info "Installing lightweight container support..."
    
    # Install proot-distro for containerization
    pkg install -y proot-distro
    
    # Install Ubuntu in proot
    log_info "Setting up Ubuntu container..."
    proot-distro install ubuntu
    
    log_success "Container environment ready"
}

create_mobile_config() {
    log_info "Creating mobile-optimized configuration..."
    
    cd async-automation-framework
    
    cat > .env.mobile << 'EOF'
# Mobile Termux Configuration
MOBILE_MODE=true
LOW_RESOURCE_MODE=true
MAX_WORKERS=2
MEMORY_LIMIT=512M

# Cloud API Endpoints (Mobile-friendly)
REMOTE_CONTROL_ENABLED=true
API_ENDPOINT=https://your-api.com

# Notification Settings
TERMUX_NOTIFICATIONS=true
SENDGRID_API_KEY=
NTFY_WEBHOOK=

# Revenue Stream APIs (Add your keys)
STRIPE_API_KEY=
SHOPIFY_API_KEY=
AFFILIATE_API_KEY=
EOF

    log_success "Mobile configuration created"
    log_warning "Edit .env.mobile with your API keys: nano .env.mobile"
}

create_mobile_launcher() {
    log_info "Creating mobile launcher script..."
    
    cat > ~/automation-mobile.sh << 'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash

# Mobile Command Center Launcher
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd ~/async-automation-framework

show_mobile_menu() {
    clear
    echo -e "${GREEN}═══ MOBILE COMMAND CENTER ═══${NC}"
    echo ""
    echo "1. 🚀 Start Automation (Lightweight)"
    echo "2. 📊 Check System Status"
    echo "3. 📝 View Logs"
    echo "4. ⚙️  Configure Settings"
    echo "5. 🔄 Update Framework"
    echo "6. 📡 Remote Deploy to Cloud"
    echo "7. 🔔 Test Notifications"
    echo "8. 💰 Revenue Dashboard"
    echo "9. 🛑 Stop All Services"
    echo "10. 📱 Device Info"
    echo "0. ❌ Exit"
    echo ""
    echo -ne "${YELLOW}Select option: ${NC}"
}

start_automation() {
    echo -e "${BLUE}Starting lightweight automation...${NC}"
    
    # Run in background with tmux
    tmux new-session -d -s automation "python3 src/quantum_revenue_engine.py --mobile-mode"
    
    echo -e "${GREEN}Automation started in background (tmux session: automation)${NC}"
    echo "Attach with: tmux attach -t automation"
    
    # Send notification
    termux-notification --title "Automation Started" --content "Revenue engine running in background"
}

check_status() {
    echo -e "${BLUE}System Status:${NC}"
    echo ""
    
    # Check if automation is running
    if tmux has-session -t automation 2>/dev/null; then
        echo -e "${GREEN}✓ Automation: RUNNING${NC}"
    else
        echo -e "${YELLOW}○ Automation: STOPPED${NC}"
    fi
    
    # System resources
    echo ""
    echo -e "${BLUE}Device Resources:${NC}"
    echo "Battery: $(termux-battery-status | grep percentage | cut -d: -f2)"
    echo "WiFi: $(termux-wifi-connectioninfo | grep ssid | cut -d: -f2 || echo 'Not connected')"
    
    # Show running processes
    echo ""
    echo -e "${BLUE}Active Python Processes:${NC}"
    ps aux | grep python3 | grep -v grep || echo "None"
    
    read -p "Press Enter to continue..."
}

view_logs() {
    if [ -f "logs/automation.log" ]; then
        tail -n 50 logs/automation.log
    else
        echo "No logs found"
    fi
    read -p "Press Enter to continue..."
}

configure_settings() {
    nano .env.mobile
}

update_framework() {
    echo -e "${BLUE}Updating framework...${NC}"
    git pull origin main
    pip install -r requirements.txt --upgrade
    echo -e "${GREEN}Update complete${NC}"
    sleep 2
}

remote_deploy() {
    echo -e "${BLUE}Deploying to remote cloud...${NC}"
    
    # This would trigger deployment to your cloud infrastructure
    # via GitHub Actions or direct API calls
    
    echo "Options:"
    echo "1. Deploy via GitHub Actions"
    echo "2. Deploy via SSH to VPS"
    echo "3. Deploy to AWS Lambda"
    read -p "Choice: " deploy_choice
    
    case $deploy_choice in
        1)
            echo "Triggering GitHub Actions workflow..."
            # Use GitHub API to trigger workflow
            curl -X POST \
                -H "Accept: application/vnd.github.v3+json" \
                -H "Authorization: token $GITHUB_TOKEN" \
                https://api.github.com/repos/Garrettc123/async-automation-framework/actions/workflows/autonomous-deployment.yml/dispatches \
                -d '{"ref":"main"}'
            ;;
        2)
            echo "Enter VPS details:"
            read -p "Host: " vps_host
            read -p "User: " vps_user
            ssh ${vps_user}@${vps_host} "cd /opt/automation && git pull && ./deploy.sh"
            ;;
        3)
            echo "Deploying to AWS Lambda..."
            # Package and deploy to Lambda
            ;;
    esac
}

test_notifications() {
    echo -e "${BLUE}Testing notifications...${NC}"
    
    # Termux notification
    termux-notification \
        --title "Test Notification" \
        --content "Mobile automation is working!" \
        --button1 "Open" \
        --button1-action "termux-open-url https://github.com/Garrettc123/async-automation-framework"
    
    echo -e "${GREEN}Notification sent${NC}"
    sleep 2
}

revenue_dashboard() {
    echo -e "${GREEN}═══ REVENUE DASHBOARD ═══${NC}"
    echo ""
    
    if [ -f "revenue_data.json" ]; then
        python3 << 'DASHBOARD'
import json
from datetime import datetime

try:
    with open('revenue_data.json', 'r') as f:
        data = json.load(f)
    
    print(f"Last Updated: {data.get('timestamp', 'N/A')}")
    print(f"\nRevenue Streams:")
    for stream, value in data.get('streams', {}).items():
        print(f"  • {stream}: ${value:.2f}")
    
    total = sum(data.get('streams', {}).values())
    print(f"\nTotal: ${total:.2f}")
except:
    print("No revenue data available yet")
DASHBOARD
    else
        echo "No revenue data available"
    fi
    
    read -p "Press Enter to continue..."
}

stop_services() {
    echo -e "${YELLOW}Stopping all services...${NC}"
    
    # Kill tmux session
    tmux kill-session -t automation 2>/dev/null || true
    
    # Kill Python processes
    pkill -f "quantum_revenue_engine.py" || true
    
    echo -e "${GREEN}All services stopped${NC}"
    
    termux-notification --title "Services Stopped" --content "All automation services have been stopped"
    sleep 2
}

device_info() {
    echo -e "${BLUE}Device Information:${NC}"
    echo ""
    
    echo "Battery:"
    termux-battery-status
    echo ""
    
    echo "WiFi:"
    termux-wifi-connectioninfo
    echo ""
    
    echo "Storage:"
    df -h $HOME | tail -n 1
    echo ""
    
    echo "CPU Info:"
    cat /proc/cpuinfo | grep "model name" | head -n 1
    echo ""
    
    read -p "Press Enter to continue..."
}

# Main loop
while true; do
    show_mobile_menu
    read choice
    
    case $choice in
        1) start_automation ;;
        2) check_status ;;
        3) view_logs ;;
        4) configure_settings ;;
        5) update_framework ;;
        6) remote_deploy ;;
        7) test_notifications ;;
        8) revenue_dashboard ;;
        9) stop_services ;;
        10) device_info ;;
        0) exit 0 ;;
        *) echo "Invalid option" ;;
    esac
done
LAUNCHER

    chmod +x ~/automation-mobile.sh
    log_success "Mobile launcher created: ~/automation-mobile.sh"
}

setup_shortcuts() {
    log_info "Creating Termux shortcuts..."
    
    mkdir -p ~/.shortcuts
    
    # Main launcher shortcut
    cat > ~/.shortcuts/automation << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
~/automation-mobile.sh
EOF
    chmod +x ~/.shortcuts/automation
    
    # Quick start shortcut
    cat > ~/.shortcuts/start-automation << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/async-automation-framework
tmux new-session -d -s automation "python3 src/quantum_revenue_engine.py --mobile-mode"
termux-notification --title "Automation Started" --content "Running in background"
EOF
    chmod +x ~/.shortcuts/start-automation
    
    log_success "Shortcuts created - access from Termux widget"
}

setup_background_service() {
    log_info "Setting up background automation service..."
    
    # Install Termux:Boot for auto-start on device boot
    log_info "Install Termux:Boot from F-Droid to enable auto-start on phone boot"
    
    mkdir -p ~/.termux/boot
    cat > ~/.termux/boot/start-automation << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
termux-wake-lock
cd ~/async-automation-framework
tmux new-session -d -s automation "python3 src/quantum_revenue_engine.py --mobile-mode"
EOF
    chmod +x ~/.termux/boot/start-automation
    
    log_success "Boot script created"
}

create_notification_handler() {
    log_info "Creating notification handlers..."
    
    cd async-automation-framework
    mkdir -p src/mobile
    
    cat > src/mobile/notifications.py << 'EOF'
import subprocess
import json

class TermuxNotifications:
    @staticmethod
    def send(title, message, priority="normal"):
        """Send Termux notification"""
        cmd = [
            "termux-notification",
            "--title", title,
            "--content", message,
            "--priority", priority
        ]
        subprocess.run(cmd)
    
    @staticmethod
    def revenue_alert(amount, source):
        """Send revenue notification"""
        TermuxNotifications.send(
            "💰 Revenue Update",
            f"${amount:.2f} from {source}",
            "high"
        )
    
    @staticmethod
    def error_alert(error_msg):
        """Send error notification"""
        TermuxNotifications.send(
            "⚠️ Error Alert",
            error_msg,
            "high"
        )
EOF

    log_success "Notification handlers created"
}

show_next_steps() {
    clear
    log_success "Termux setup complete!"
    echo ""
    echo -e "${GREEN}═══ NEXT STEPS ═══${NC}"
    echo ""
    echo "1. Configure your API keys:"
    echo -e "   ${YELLOW}nano ~/async-automation-framework/.env.mobile${NC}"
    echo ""
    echo "2. Launch the mobile command center:"
    echo -e "   ${YELLOW}~/automation-mobile.sh${NC}"
    echo ""
    echo "3. Or use the quick shortcut:"
    echo -e "   ${YELLOW}automation${NC} (if shortcuts are enabled)"
    echo ""
    echo "4. Enable background running:"
    echo "   - Install Termux:Boot from F-Droid"
    echo "   - Grant auto-start permission"
    echo ""
    echo "5. Add Termux widget to home screen for quick access"
    echo ""
    echo -e "${BLUE}Additional Setup:${NC}"
    echo "   - GitHub token for remote deployments"
    echo "   - Cloud API credentials"
    echo "   - Notification webhook URLs"
    echo ""
}

# Main installation
main() {
    show_banner
    check_termux
    
    log_info "Starting Termux setup..."
    echo ""
    
    install_prerequisites
    setup_storage
    clone_repository
    install_lightweight_docker
    create_mobile_config
    create_mobile_launcher
    setup_shortcuts
    setup_background_service
    create_notification_handler
    
    show_next_steps
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
