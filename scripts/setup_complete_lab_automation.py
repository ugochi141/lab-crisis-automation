#!/usr/bin/env python3
"""
Complete Lab Automation Setup Script
Sets up Notion databases, GitHub Actions, and Teams integration
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from notion_client import Client
import requests

class LabAutomationSetup:
    """Complete setup for lab automation system"""
    
    def __init__(self):
        self.setup_log = []
        self.databases = {}
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from environment or config file"""
        config = {
            'notion_token': os.getenv('NOTION_TOKEN'),
            'teams_webhook': os.getenv('TEAMS_WEBHOOK'),
            'parent_page_id': os.getenv('NOTION_PARENT_PAGE_ID'),
            'powerbi_endpoint': os.getenv('POWERBI_ENDPOINT'),
            'github_token': os.getenv('GITHUB_TOKEN'),
            'github_repo': os.getenv('GITHUB_REPOSITORY', 'your-org/lab-automation')
        }
        
        # Validate required config
        required = ['notion_token', 'teams_webhook', 'parent_page_id']
        missing = [key for key in required if not config[key]]
        
        if missing:
            print(f"❌ Missing required configuration: {', '.join(missing)}")
            print("\nPlease set these environment variables:")
            for key in missing:
                print(f"  export {key.upper()}=your_value_here")
            sys.exit(1)
            
        return config
    
    def log(self, message, level="INFO"):
        """Log setup progress"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        self.setup_log.append(log_entry)
    
    def setup_notion_databases(self):
        """Create all Notion databases"""
        self.log("🚀 Setting up Notion databases...")
        
        try:
            notion = Client(auth=self.config['notion_token'])
            
            # Test connection
            notion.search()
            self.log("✅ Notion connection successful")
            
            # Create databases
            databases_to_create = [
                {
                    'name': 'Staff Performance Tracker',
                    'emoji': '👥',
                    'properties': {
                        "Employee": {"title": {}},
                        "Date": {"date": {}},
                        "Station": {
                            "select": {
                                "options": [
                                    {"name": f"Station {i}", "color": "blue"} for i in range(1, 11)
                                ] + [
                                    {"name": "Lab Bench", "color": "green"},
                                    {"name": "QC Station", "color": "purple"},
                                    {"name": "Float", "color": "yellow"}
                                ]
                            }
                        },
                        "Status": {
                            "select": {
                                "options": [
                                    {"name": "✅ Active", "color": "green"},
                                    {"name": "☕ Break", "color": "yellow"},
                                    {"name": "⚠️ Idle", "color": "red"},
                                    {"name": "❌ Missing", "color": "red"}
                                ]
                            }
                        },
                        "Samples Processed": {"number": {"format": "number"}},
                        "Performance Score": {
                            "formula": {
                                "expression": "round(prop(\"Samples Processed\") * 2 - prop(\"Idle Minutes\") * 0.5 - prop(\"Errors Hidden\") * 10)"
                            }
                        },
                        "Alert Flag": {"checkbox": {}}
                    }
                },
                {
                    'name': 'Station Monitor',
                    'emoji': '🏥',
                    'properties': {
                        "Station": {"title": {}},
                        "Current Tech": {"rich_text": {}},
                        "Status": {
                            "select": {
                                "options": [
                                    {"name": "🟢 Open-Staffed", "color": "green"},
                                    {"name": "🟡 Open-Unstaffed", "color": "yellow"},
                                    {"name": "🔴 Closed", "color": "red"}
                                ]
                            }
                        },
                        "Current Wait (min)": {"number": {"format": "number"}},
                        "Queue Length": {"number": {"format": "number"}},
                        "Alert Active": {"checkbox": {}}
                    }
                },
                {
                    'name': 'Active Alerts',
                    'emoji': '🚨',
                    'properties': {
                        "Alert": {"title": {}},
                        "Time": {"date": {}},
                        "Type": {
                            "select": {
                                "options": [
                                    {"name": "Wait Time", "color": "orange"},
                                    {"name": "TAT Failure", "color": "red"},
                                    {"name": "Staff Missing", "color": "red"},
                                    {"name": "Break Violation", "color": "yellow"}
                                ]
                            }
                        },
                        "Severity": {
                            "select": {
                                "options": [
                                    {"name": "⚪ Info", "color": "gray"},
                                    {"name": "🟡 Warning", "color": "yellow"},
                                    {"name": "🟠 High", "color": "orange"},
                                    {"name": "🔴 Critical", "color": "red"}
                                ]
                            }
                        },
                        "Resolved": {"checkbox": {}}
                    }
                },
                {
                    'name': 'TAT Performance',
                    'emoji': '⏱️',
                    'properties': {
                        "Date": {"date": {}},
                        "Department": {
                            "select": {
                                "options": [
                                    {"name": "Phlebotomy", "color": "green"},
                                    {"name": "Chemistry", "color": "blue"},
                                    {"name": "Hematology", "color": "red"}
                                ]
                            }
                        },
                        "STAT TAT %": {"number": {"format": "percent"}},
                        "Routine TAT %": {"number": {"format": "percent"}},
                        "Target Met": {"checkbox": {}}
                    }
                },
                {
                    'name': 'Management Dashboard',
                    'emoji': '📊',
                    'properties': {
                        "Metric": {"title": {}},
                        "Current Value": {"number": {"format": "number"}},
                        "Target": {"number": {"format": "number"}},
                        "Status": {
                            "select": {
                                "options": [
                                    {"name": "✅ Meeting Target", "color": "green"},
                                    {"name": "⚠️ Below Target", "color": "yellow"},
                                    {"name": "🔴 Critical", "color": "red"}
                                ]
                            }
                        },
                        "Last Updated": {"date": {}}
                    }
                }
            ]
            
            for db_config in databases_to_create:
                self.log(f"Creating {db_config['name']}...")
                
                db = notion.databases.create(
                    parent={"page_id": self.config['parent_page_id']},
                    icon={"emoji": db_config['emoji']},
                    title=[{"text": {"content": db_config['name']}}],
                    properties=db_config['properties']
                )
                
                self.databases[db_config['name'].lower().replace(' ', '_')] = db['id']
                self.log(f"✅ Created {db_config['name']}: {db['id']}")
                time.sleep(1)  # Rate limiting
            
            self.log("✅ All Notion databases created successfully")
            return True
            
        except Exception as e:
            self.log(f"❌ Error creating Notion databases: {e}", "ERROR")
            return False
    
    def setup_github_secrets(self):
        """Setup GitHub repository secrets"""
        self.log("🔐 Setting up GitHub secrets...")
        
        secrets = {
            'NOTION_TOKEN': self.config['notion_token'],
            'TEAMS_WEBHOOK': self.config['teams_webhook'],
            'NOTION_ALERTS_DB_ID': self.databases.get('active_alerts'),
            'NOTION_DASHBOARD_DB_ID': self.databases.get('management_dashboard'),
            'POWERBI_ENDPOINT': self.config.get('powerbi_endpoint', '')
        }
        
        print("\n📋 Add these secrets to your GitHub repository:")
        print("   Go to: Settings → Secrets and variables → Actions")
        print("   Click 'New repository secret' for each:")
        print()
        
        for key, value in secrets.items():
            if value:
                print(f"   {key}: {value[:20]}...")
            else:
                print(f"   {key}: [Not configured]")
        
        self.log("✅ GitHub secrets configuration provided")
        return True
    
    def test_teams_webhook(self):
        """Test Teams webhook connection"""
        self.log("🔗 Testing Teams webhook...")
        
        try:
            test_message = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "00FF00",
                "summary": "Lab Automation Setup Test",
                "sections": [{
                    "activityTitle": "✅ Lab Automation Setup Complete",
                    "activitySubtitle": "System is ready for monitoring",
                    "facts": [
                        {"name": "Setup Time", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                        {"name": "Databases Created", "value": str(len(self.databases))},
                        {"name": "Status", "value": "Ready"}
                    ]
                }]
            }
            
            response = requests.post(
                self.config['teams_webhook'],
                json=test_message,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                self.log("✅ Teams webhook test successful")
                return True
            else:
                self.log(f"❌ Teams webhook test failed: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Teams webhook test error: {e}", "ERROR")
            return False
    
    def create_sample_data(self):
        """Create sample data for testing"""
        self.log("📊 Creating sample data...")
        
        try:
            notion = Client(auth=self.config['notion_token'])
            
            # Sample staff performance data
            staff_data = [
                {"Employee": "Christina B.", "Station": "Station 1", "Samples": 45, "Status": "✅ Active"},
                {"Employee": "Turi K.", "Station": "Station 2", "Samples": 38, "Status": "✅ Active"},
                {"Employee": "John D.", "Station": "Station 3", "Samples": 25, "Status": "⚠️ Idle"},
                {"Employee": "Sarah M.", "Station": "Lab Bench", "Samples": 52, "Status": "✅ Active"},
                {"Employee": "Mike R.", "Station": "Float", "Samples": 0, "Status": "❌ Missing"}
            ]
            
            for staff in staff_data:
                notion.pages.create(
                    parent={"database_id": self.databases['staff_performance_tracker']},
                    properties={
                        "Employee": {"title": [{"text": {"content": staff["Employee"]}}]},
                        "Date": {"date": {"start": datetime.now().isoformat()}},
                        "Station": {"select": {"name": staff["Station"]}},
                        "Status": {"select": {"name": staff["Status"]}},
                        "Samples Processed": {"number": staff["Samples"]}
                    }
                )
            
            # Sample alerts
            alert_data = [
                {"Alert": "High Wait Time at Station 1", "Type": "Wait Time", "Severity": "🟠 High"},
                {"Alert": "TAT Below Target - Chemistry", "Type": "TAT Failure", "Severity": "🔴 Critical"},
                {"Alert": "Staff Member Missing - Mike R.", "Type": "Staff Missing", "Severity": "🟡 Warning"}
            ]
            
            for alert in alert_data:
                notion.pages.create(
                    parent={"database_id": self.databases['active_alerts']},
                    properties={
                        "Alert": {"title": [{"text": {"content": alert["Alert"]}}]},
                        "Time": {"date": {"start": datetime.now().isoformat()}},
                        "Type": {"select": {"name": alert["Type"]}},
                        "Severity": {"select": {"name": alert["Severity"]}},
                        "Resolved": {"checkbox": False}
                    }
                )
            
            self.log("✅ Sample data created successfully")
            return True
            
        except Exception as e:
            self.log(f"❌ Error creating sample data: {e}", "ERROR")
            return False
    
    def generate_setup_report(self):
        """Generate setup completion report"""
        report = {
            "setup_time": datetime.now().isoformat(),
            "databases_created": len(self.databases),
            "database_ids": self.databases,
            "configuration": {
                "notion_configured": bool(self.config['notion_token']),
                "teams_configured": bool(self.config['teams_webhook']),
                "github_configured": bool(self.config['github_token'])
            },
            "next_steps": [
                "1. Add GitHub secrets to your repository",
                "2. Enable GitHub Actions in repository settings",
                "3. Test the alert forwarding system",
                "4. Configure Power BI integration (optional)",
                "5. Train your team on the new system"
            ]
        }
        
        # Save report
        with open('setup_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log("📄 Setup report saved to setup_report.json")
        return report
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        self.log("🚀 Starting complete lab automation setup...")
        self.log("=" * 60)
        
        success = True
        
        # Step 1: Create Notion databases
        if not self.setup_notion_databases():
            success = False
        
        # Step 2: Test Teams webhook
        if not self.test_teams_webhook():
            success = False
        
        # Step 3: Create sample data
        if not self.create_sample_data():
            success = False
        
        # Step 4: Setup GitHub secrets
        self.setup_github_secrets()
        
        # Step 5: Generate report
        report = self.generate_setup_report()
        
        self.log("=" * 60)
        if success:
            self.log("🎉 SETUP COMPLETE! Your lab automation system is ready.")
            self.log("📋 Next steps:")
            for step in report['next_steps']:
                self.log(f"   {step}")
        else:
            self.log("⚠️ Setup completed with some errors. Check the log above.")
        
        return success

def main():
    """Main setup function"""
    print("🏥 Lab Automation Setup")
    print("=" * 40)
    
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_ACTIONS'):
        print("Running in GitHub Actions environment")
    
    # Create setup instance
    setup = LabAutomationSetup()
    
    # Run complete setup
    success = setup.run_complete_setup()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
