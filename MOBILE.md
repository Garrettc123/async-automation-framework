# 📱 Mobile Deployment Guide - Termux

Run your entire enterprise automation system from your Android phone using Termux!

## 🚀 One-Command Setup

### Install Termux
1. **Download Termux** from [F-Droid](https://f-droid.org/packages/com.termux/) (NOT Google Play)
2. **Open Termux** and run:

```bash
curl -sL https://raw.githubusercontent.com/Garrettc123/async-automation-framework/main/termux-setup.sh | bash
```

That's it! The script automatically:
- ✅ Installs all prerequisites
- ✅ Clones the automation framework
- ✅ Creates mobile-optimized launcher
- ✅ Sets up background services
- ✅ Configures shortcuts & widgets

## 📱 Mobile Command Center Features

Once installed, launch with:
```bash
~/automation-mobile.sh
```

### Available Operations

1. **🚀 Start Automation** - Lightweight background execution
2. **📊 System Status** - Battery, WiFi, running processes
3. **📝 View Logs** - Real-time monitoring
4. **⚙️ Configure Settings** - Edit API keys & config
5. **🔄 Update Framework** - Pull latest code
6. **📡 Remote Deploy** - Trigger cloud deployments
7. **🔔 Test Notifications** - Verify alerts
8. **💰 Revenue Dashboard** - View earnings
9. **🛑 Stop Services** - Emergency shutdown
10. **📱 Device Info** - Hardware & resource stats

## ⚡ Quick Start Examples

### Launch on Phone Boot
1. Install [Termux:Boot](https://f-droid.org/packages/com.termux.boot/) from F-Droid
2. Grant auto-start permission
3. Automation starts automatically when phone boots!

### Add Home Screen Widget
1. Install [Termux:Widget](https://f-droid.org/packages/com.termux.widget/)
2. Add widget to home screen
3. Tap "automation" shortcut to launch instantly

### Background Operation
```bash
# Start in background with tmux
~/automation-mobile.sh
# Select option 1 (Start Automation)

# Detach and let it run
# Automation continues even when Termux is closed
```

## 🔧 Configuration

### Edit Mobile Settings
```bash
cd ~/async-automation-framework
nano .env.mobile
```

**Key Settings:**
```bash
# Resource limits for mobile
MOBILE_MODE=true
LOW_RESOURCE_MODE=true
MAX_WORKERS=2
MEMORY_LIMIT=512M

# API Keys
STRIPE_API_KEY=sk_live_...
SHOPIFY_API_KEY=shpat_...
AFFILIATE_API_KEY=...

# Notifications
TERMUX_NOTIFICATIONS=true
NTFY_WEBHOOK=https://ntfy.sh/your-topic
```

## 📡 Remote Cloud Deployment

Deploy to your cloud infrastructure FROM your phone:

### Option 1: GitHub Actions
```bash
# In mobile command center:
# Select: 6 (Remote Deploy) → 1 (GitHub Actions)

# Requires: GITHUB_TOKEN in .env.mobile
```

### Option 2: Direct SSH to VPS
```bash
# In mobile command center:
# Select: 6 (Remote Deploy) → 2 (SSH to VPS)

# Enter your server details
# Automation deploys automatically
```

### Option 3: AWS Lambda
```bash
# In mobile command center:
# Select: 6 (Remote Deploy) → 3 (AWS Lambda)
```

## 🔔 Push Notifications

Get real-time alerts on your phone:

### Built-in Termux Notifications
- Revenue updates
- Error alerts
- Deployment status
- System health warnings

### External Webhooks
```bash
# Configure in .env.mobile
NTFY_WEBHOOK=https://ntfy.sh/your-automation
SENDGRID_API_KEY=SG.xxx  # Email alerts
TWILIO_WEBHOOK=...        # SMS alerts
```

## 💾 Resource Management

### Optimized for Mobile
- **Low Memory Mode**: Runs in 512MB RAM
- **Battery Efficient**: Minimal wake locks
- **Bandwidth Aware**: Compresses API calls
- **Background Safe**: Survives app switching

### Monitor Resources
```bash
# In mobile command center:
# Select: 2 (System Status)

# Shows:
# - Battery level & status
# - WiFi connection
# - Storage usage
# - CPU load
# - Running processes
```

## 🛡️ Security on Mobile

### Storage Permissions
```bash
# Termux has isolated storage
# Grant access if needed:
termux-setup-storage
```

### SSH Access
```bash
# Run SSH server on phone
pkg install openssh
sshd

# Connect from computer:
ssh u0_a123@192.168.1.100 -p 8022
```

### API Key Security
- Keys stored in `~/.env.mobile` (not synced)
- File permissions: `chmod 600 .env.mobile`
- Never commit to Git

## 🔄 Auto-Updates

### Keep Framework Updated
```bash
# Manual update:
~/automation-mobile.sh
# Select: 5 (Update Framework)

# Or via cron:
pkg install cronie
crontab -e
# Add: 0 */6 * * * cd ~/async-automation-framework && git pull
```

## 🐛 Troubleshooting

### Automation Won't Start
```bash
# Check Python version
python --version  # Should be 3.x

# Reinstall dependencies
pip install -r ~/async-automation-framework/requirements.txt
```

### Permission Denied
```bash
# Make scripts executable
chmod +x ~/automation-mobile.sh
chmod +x ~/async-automation-framework/termux-setup.sh
```

### Background Process Killed
```bash
# Enable wake lock
termux-wake-lock

# Disable battery optimization for Termux:
# Settings → Apps → Termux → Battery → Unrestricted
```

### No Notifications
```bash
# Test notification system
termux-notification --title "Test" --content "Working!"

# If fails, reinstall Termux:API
pkg install termux-api
```

## 📊 Mobile Dashboard

### View Revenue Stats
```bash
# In mobile command center:
# Select: 8 (Revenue Dashboard)

# Real-time display:
# ┌─────────────────────┐
# │ Stripe:    $1,234.56│
# │ Shopify:     $890.00│
# │ Affiliate:   $456.78│
# │ Total:     $2,581.34│
# └─────────────────────┘
```

### Live Logs
```bash
# Stream logs in real-time
# Select: 3 (View Logs)

# Or manually:
tail -f ~/async-automation-framework/logs/automation.log
```

## 🌐 Use Cases

### 1. **Travel Management**
- Monitor automation while traveling
- Deploy fixes from anywhere
- Receive instant revenue alerts

### 2. **24/7 Uptime**
- Phone stays on and connected
- Cheaper than VPS for light workloads
- Instant notifications on issues

### 3. **Development Testing**
- Test mobile-responsive deployments
- Debug on actual mobile hardware
- Quick prototyping on-the-go

### 4. **Emergency Control**
- Stop runaway processes remotely
- Rollback deployments instantly
- Check status during outages

## 🔗 Integration with Desktop

### Sync Configs
```bash
# On phone (Termux):
cd ~/async-automation-framework
git add .env.mobile
git commit -m "Update mobile config"
git push

# On desktop:
git pull
cp .env.mobile .env
```

### Remote Control Desktop from Phone
```bash
# SSH from Termux to your desktop:
ssh user@desktop-ip
cd /path/to/automation
./command-center.sh
```

## 📦 Additional Apps

### Recommended F-Droid Apps
- **Termux** - Main terminal
- **Termux:API** - System integration
- **Termux:Boot** - Auto-start on boot
- **Termux:Widget** - Home screen shortcuts
- **Termux:Styling** - Customize appearance

### Optional Enhancements
```bash
# Install extras
pkg install termux-api termux-tools

# Better terminal
pkg install zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

## 🎯 Performance Tips

1. **Use WiFi**: Avoid mobile data for heavy operations
2. **Keep Charged**: Background tasks drain battery
3. **Close Other Apps**: Free up RAM
4. **Disable Bloat**: Remove unnecessary Android apps
5. **Use tmux**: Persist sessions across reconnects

## 📱 Supported Devices

- **Android 7.0+** (recommended: Android 10+)
- **ARM/ARM64** architecture
- **Minimum 2GB RAM** (4GB recommended)
- **500MB free storage**
- **WiFi or mobile data**

## 🆘 Support

### Get Help
- [GitHub Issues](https://github.com/Garrettc123/async-automation-framework/issues)
- [Termux Wiki](https://wiki.termux.com)
- [Termux Reddit](https://reddit.com/r/termux)

### Report Mobile-Specific Issues
Include:
- Android version
- Device model
- Termux version (`termux-info`)
- Error logs

---

**Ready to automate from your pocket?** 🚀

Install now:
```bash
curl -sL https://raw.githubusercontent.com/Garrettc123/async-automation-framework/main/termux-setup.sh | bash
```
