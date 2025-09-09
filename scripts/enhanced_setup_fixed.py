#!/usr/bin/env python3
"""
Enhanced Lab Crisis Automation Setup
Fixes system failures and enhances error handling
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

def create_env_file():
    """Create .env file with proper configuration"""
    env_content = """# Lab Crisis Automation Environment Variables
# Fill in your actual values below

# Notion API Configuration
NOTION_API_TOKEN=your_notion_token_here
NOTION_VERSION=2022-06-28

# Notion Database IDs
NOTION_PERFORMANCE_DB_ID=your_performance_db_id_here
NOTION_INCIDENT_DB_ID=your_incident_db_id_here
NOTION_LAB_MANAGEMENT_CENTER=your_lab_management_center_id_here

# Power BI Configuration
POWERBI_WORKSPACE_ID=your_powerbi_workspace_id_here
POWERBI_MONITOR_DATASET_ID=your_monitor_dataset_id_here
POWERBI_MONITOR_PUSH_URL=your_monitor_push_url_here
POWERBI_METRICS_DATASET_ID=your_metrics_dataset_id_here
POWERBI_METRICS_PUSH_URL=your_metrics_push_url_here

# Teams Integration
TEAMS_WEBHOOK_URL=your_teams_webhook_url_here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/lab_automation.log
AUDIT_LOG_PATH=logs/audit_trail.log

# Alert Thresholds
TAT_THRESHOLD_MINUTES=30
PERFORMANCE_SCORE_THRESHOLD=60
ERROR_RATE_THRESHOLD=2
BREAK_TIME_THRESHOLD_MINUTES=15
QC_COMPLETION_THRESHOLD=95

# Operational Settings
MONITORING_INTERVAL_SECONDS=300
ALERT_COOLDOWN_MINUTES=15
MAX_RETRY_ATTEMPTS=3
REQUEST_TIMEOUT_SECONDS=30
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file")

def create_directories():
    """Create necessary directories"""
    dirs = ['logs', 'data', 'reports', 'backups']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Created directory: {dir_name}")

def fix_import_issues():
    """Fix common import and dependency issues"""
    try:
        import requests
        import pandas
        from notion_client import Client
        from dotenv import load_dotenv
        print("✅ All required packages are installed")
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing required packages...")
        os.system("pip install -r requirements.txt")

def create_enhanced_crisis_monitor():
    """Create enhanced crisis monitor with better error handling"""
    enhanced_monitor = '''#!/usr/bin/env python3
"""
Enhanced Lab Crisis Monitor
Robust error handling and comprehensive monitoring
"""

import os
import sys
import json
import time
import logging
import requests
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crisis_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedCrisisMonitor:
    def __init__(self):
        self.notion_token = os.getenv('NOTION_API_TOKEN')
        self.teams_webhook = os.getenv('TEAMS_WEBHOOK_URL')
        self.performance_db_id = os.getenv('NOTION_PERFORMANCE_DB_ID')
        self.incident_db_id = os.getenv('NOTION_INCIDENT_DB_ID')
        
        # Initialize Notion client with error handling
        try:
            if self.notion_token and self.notion_token != 'your_notion_token_here':
                self.notion = Client(auth=self.notion_token)
                logger.info("✅ Notion client initialized")
            else:
                self.notion = None
                logger.warning("⚠️ Notion token not configured")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Notion client: {e}")
            self.notion = None
    
    def check_system_health(self):
        """Comprehensive system health check"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'notion_connected': False,
            'teams_webhook_working': False,
            'databases_accessible': False,
            'overall_status': 'UNKNOWN'
        }
        
        # Check Notion connection
        if self.notion:
            try:
                # Test with a simple API call
                self.notion.users.me()
                health_status['notion_connected'] = True
                logger.info("✅ Notion connection verified")
            except Exception as e:
                logger.error(f"❌ Notion connection failed: {e}")
        
        # Check Teams webhook
        if self.teams_webhook and self.teams_webhook != 'your_teams_webhook_url_here':
            try:
                test_payload = {
                    "text": "🔍 Lab Crisis Monitor - System Health Check",
                    "timestamp": datetime.now().isoformat()
                }
                response = requests.post(self.teams_webhook, json=test_payload, timeout=10)
                if response.status_code == 200:
                    health_status['teams_webhook_working'] = True
                    logger.info("✅ Teams webhook verified")
                else:
                    logger.error(f"❌ Teams webhook failed: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Teams webhook error: {e}")
        
        # Check database accessibility
        if self.notion and self.performance_db_id and self.performance_db_id != 'your_performance_db_id_here':
            try:
                self.notion.databases.retrieve(database_id=self.performance_db_id)
                health_status['databases_accessible'] = True
                logger.info("✅ Performance database accessible")
            except Exception as e:
                logger.error(f"❌ Database access failed: {e}")
        
        # Determine overall status
        if health_status['notion_connected'] and health_status['teams_webhook_working']:
            health_status['overall_status'] = 'HEALTHY'
        elif health_status['notion_connected'] or health_status['teams_webhook_working']:
            health_status['overall_status'] = 'DEGRADED'
        else:
            health_status['overall_status'] = 'CRITICAL'
        
        return health_status
    
    def create_crisis_alert(self, alert_type, message, severity='HIGH'):
        """Create crisis alert with enhanced error handling"""
        if not self.notion or not self.incident_db_id:
            logger.error("❌ Cannot create alert: Notion not configured")
            return False
        
        try:
            alert_data = {
                "Alert Type": {"title": [{"text": {"content": alert_type}}]},
                "Message": {"rich_text": [{"text": {"content": message}}]},
                "Severity": {"select": {"name": severity}},
                "Timestamp": {"date": {"start": datetime.now().isoformat()}},
                "Status": {"select": {"name": "Active"}}
            }
            
            self.notion.pages.create(
                parent={"database_id": self.incident_db_id},
                properties=alert_data
            )
            logger.info(f"✅ Created {severity} alert: {alert_type}")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to create alert: {e}")
            return False
    
    def send_teams_alert(self, title, message, color="FF0000"):
        """Send Teams alert with retry logic"""
        if not self.teams_webhook or self.teams_webhook == 'your_teams_webhook_url_here':
            logger.warning("⚠️ Teams webhook not configured")
            return False
        
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": title,
            "sections": [{
                "activityTitle": title,
                "activitySubtitle": f"Lab Crisis Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "activityImage": "https://img.icons8.com/color/48/000000/warning.png",
                "text": message,
                "markdown": True
            }]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    self.teams_webhook, 
                    json=payload, 
                    timeout=10,
                    headers={'Content-Type': 'application/json'}
                )
                if response.status_code == 200:
                    logger.info("✅ Teams alert sent successfully")
                    return True
                else:
                    logger.warning(f"⚠️ Teams webhook returned {response.status_code}, attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"❌ Teams alert attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error("❌ All Teams alert attempts failed")
        return False
    
    def monitor_crisis_metrics(self):
        """Monitor crisis metrics with enhanced error handling"""
        logger.info("🔍 Starting crisis metrics monitoring...")
        
        # Simulate crisis metrics (replace with actual data source)
        crisis_metrics = {
            'tat_compliance': 35.0,  # Target: 90.0
            'wait_time': 25.0,       # Target: 15.0
            'staffing_gap': 3.3,     # Target: 0.0
            'error_rate': 12.0,      # Target: 5.0
            'staff_utilization': 67.6  # Target: 80.0
        }
        
        alerts_triggered = []
        
        # Check TAT Compliance
        if crisis_metrics['tat_compliance'] < 60:
            alert_msg = f"🚨 CRITICAL: TAT Compliance at {crisis_metrics['tat_compliance']}% (Target: 90%)"
            alerts_triggered.append(alert_msg)
            self.create_crisis_alert("TAT Compliance Crisis", alert_msg, "CRITICAL")
        
        # Check Wait Time
        if crisis_metrics['wait_time'] > 20:
            alert_msg = f"⚠️ HIGH: Wait time at {crisis_metrics['wait_time']} minutes (Target: 15 min)"
            alerts_triggered.append(alert_msg)
            self.create_crisis_alert("Wait Time Alert", alert_msg, "HIGH")
        
        # Check Staffing Gap
        if crisis_metrics['staffing_gap'] > 2:
            alert_msg = f"⚠️ HIGH: Staffing gap of {crisis_metrics['staffing_gap']} positions"
            alerts_triggered.append(alert_msg)
            self.create_crisis_alert("Staffing Crisis", alert_msg, "HIGH")
        
        # Check Error Rate
        if crisis_metrics['error_rate'] > 10:
            alert_msg = f"🚨 CRITICAL: Error rate at {crisis_metrics['error_rate']}% (Target: 5%)"
            alerts_triggered.append(alert_msg)
            self.create_crisis_alert("Error Rate Crisis", alert_msg, "CRITICAL")
        
        # Send Teams summary if alerts triggered
        if alerts_triggered:
            summary_msg = "\\n".join(alerts_triggered)
            self.send_teams_alert(
                "🚨 Lab Crisis Alerts",
                f"**Crisis Metrics Detected:**\\n\\n{summary_msg}\\n\\n**Immediate Action Required!**",
                "FF0000"
            )
        
        return crisis_metrics, alerts_triggered
    
    def run_monitoring_cycle(self):
        """Run a complete monitoring cycle"""
        logger.info("🔄 Starting monitoring cycle...")
        
        # Check system health first
        health = self.check_system_health()
        logger.info(f"System Health: {health['overall_status']}")
        
        if health['overall_status'] == 'CRITICAL':
            logger.error("❌ System health is critical, skipping monitoring cycle")
            return False
        
        # Monitor crisis metrics
        metrics, alerts = self.monitor_crisis_metrics()
        
        # Log results
        logger.info(f"📊 Crisis Metrics: {metrics}")
        logger.info(f"🚨 Alerts Triggered: {len(alerts)}")
        
        return True

def main():
    """Main execution function"""
    print("🏥 Enhanced Lab Crisis Monitor Starting...")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs('logs', exist_ok=True)
    
    # Initialize monitor
    monitor = EnhancedCrisisMonitor()
    
    # Run monitoring cycle
    success = monitor.run_monitoring_cycle()
    
    if success:
        print("✅ Monitoring cycle completed successfully")
    else:
        print("❌ Monitoring cycle failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open('scripts/enhanced_crisis_monitor.py', 'w') as f:
        f.write(enhanced_monitor)
    print("✅ Created enhanced crisis monitor")

def create_system_diagnostics():
    """Create comprehensive system diagnostics"""
    diagnostics = '''#!/usr/bin/env python3
"""
Lab Crisis System Diagnostics
Comprehensive health check and troubleshooting
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    """Check environment configuration"""
    print("🔍 Environment Configuration Check")
    print("-" * 40)
    
    required_vars = [
        'NOTION_API_TOKEN',
        'TEAMS_WEBHOOK_URL',
        'NOTION_PERFORMANCE_DB_ID',
        'NOTION_INCIDENT_DB_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == f'your_{var.lower()}_here':
            missing_vars.append(var)
            print(f"❌ {var}: Not configured")
        else:
            print(f"✅ {var}: Configured")
    
    if missing_vars:
        print(f"\\n⚠️ Missing configuration: {', '.join(missing_vars)}")
        print("Please update your .env file with actual values")
        return False
    
    return True

def check_notion_connection():
    """Check Notion API connection"""
    print("\\n🔍 Notion API Connection Check")
    print("-" * 40)
    
    token = os.getenv('NOTION_API_TOKEN')
    if not token or token == 'your_notion_token_here':
        print("❌ Notion token not configured")
        return False
    
    try:
        from notion_client import Client
        notion = Client(auth=token)
        user = notion.users.me()
        print(f"✅ Notion connected as: {user.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Notion connection failed: {e}")
        return False

def check_teams_webhook():
    """Check Teams webhook"""
    print("\\n🔍 Teams Webhook Check")
    print("-" * 40)
    
    webhook = os.getenv('TEAMS_WEBHOOK_URL')
    if not webhook or webhook == 'your_teams_webhook_url_here':
        print("❌ Teams webhook not configured")
        return False
    
    try:
        payload = {
            "text": f"🔍 Lab Crisis System - Health Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        response = requests.post(webhook, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Teams webhook working")
            return True
        else:
            print(f"❌ Teams webhook failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Teams webhook error: {e}")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print("\\n🔍 Dependencies Check")
    print("-" * 40)
    
    required_packages = [
        'requests',
        'pandas',
        'notion_client',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}: Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: Missing")
    
    if missing_packages:
        print(f"\\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all diagnostics"""
    print("🏥 Lab Crisis System Diagnostics")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        check_environment(),
        check_dependencies(),
        check_notion_connection(),
        check_teams_webhook()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print("\\n" + "=" * 50)
    print(f"📊 Diagnostic Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ All systems operational!")
        return True
    else:
        print("❌ Some issues detected. Please fix the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''
    
    with open('scripts/system_diagnostics.py', 'w') as f:
        f.write(diagnostics)
    print("✅ Created system diagnostics")

def main():
    """Main setup function"""
    print("🏥 Enhanced Lab Crisis Automation Setup")
    print("=" * 50)
    
    # Create .env file
    create_env_file()
    
    # Create directories
    create_directories()
    
    # Fix import issues
    fix_import_issues()
    
    # Create enhanced scripts
    create_enhanced_crisis_monitor()
    create_system_diagnostics()
    
    print("\n" + "=" * 50)
    print("✅ Enhanced setup completed!")
    print("\nNext steps:")
    print("1. Update .env file with your actual credentials")
    print("2. Run: python scripts/system_diagnostics.py")
    print("3. Run: python scripts/enhanced_crisis_monitor.py")

if __name__ == "__main__":
    main()
