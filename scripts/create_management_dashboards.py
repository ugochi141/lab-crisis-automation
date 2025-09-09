#!/usr/bin/env python3
"""
Create Management Dashboards
Sets up comprehensive dashboards for lab performance monitoring
"""

import os
import json
from datetime import datetime, timedelta
from notion_client import Client
import pandas as pd

class ManagementDashboardCreator:
    """Create comprehensive management dashboards"""
    
    def __init__(self, notion_token: str, databases: dict):
        self.notion = Client(auth=notion_token)
        self.databases = databases
        
    def create_all_dashboards(self):
        """Create all management dashboards"""
        print("🎯 Creating Management Dashboards...")
        
        # 1. Executive Summary Dashboard
        self.create_executive_dashboard()
        
        # 2. Real-Time Operations Dashboard
        self.create_realtime_dashboard()
        
        # 3. Staff Performance Dashboard
        self.create_staff_dashboard()
        
        # 4. Quality Metrics Dashboard
        self.create_quality_dashboard()
        
        # 5. Predictive Analytics Dashboard
        self.create_predictive_dashboard()
        
        print("✅ All dashboards created successfully!")
    
    def create_executive_dashboard(self):
        """Create executive summary dashboard"""
        print("📊 Creating Executive Summary Dashboard...")
        
        dashboard_content = """
# 🏥 Lab Performance Executive Dashboard

## 📈 Key Performance Indicators

### Current Status (Today)
- **TAT Compliance**: 35% (Target: 90%) 🔴
- **Wait Time**: 25 min (Target: 15 min) 🔴
- **Staff Utilization**: 67.6% (Target: 80%) 🟡
- **Error Rate**: 12% (Target: 5%) 🔴

### Critical Issues Requiring Immediate Attention
1. **TAT Crisis**: Only 35% meeting targets
2. **Staffing Shortage**: 3.3 FTE gap
3. **Behavioral Issues**: Staff sneaking off, hiding mistakes
4. **Quality Problems**: High error rate, poor reporting

### Action Items
- [ ] Emergency staff meeting today
- [ ] Implement real-time monitoring
- [ ] Begin progressive discipline
- [ ] Start emergency hiring process

### Financial Impact
- **Lost Productivity**: $2,500/day
- **Overtime Costs**: $1,200/day
- **Quality Issues**: $800/day
- **Total Daily Loss**: $4,500/day

---
*Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*
        """
        
        # Create executive dashboard page
        self.notion.pages.create(
            parent={"page_id": self.databases.get('management_dashboard')},
            properties={
                "Metric": {"title": [{"text": {"content": "Executive Summary"}}]},
                "Current Value": {"number": 35.0},
                "Target": {"number": 90.0},
                "Status": {"select": {"name": "🔴 Critical"}},
                "Last Updated": {"date": {"start": datetime.now().isoformat()}}
            }
        )
    
    def create_realtime_dashboard(self):
        """Create real-time operations dashboard"""
        print("⚡ Creating Real-Time Operations Dashboard...")
        
        # Create real-time metrics
        realtime_metrics = [
            {"metric": "Current Wait Time", "value": 25, "target": 15, "status": "🔴 Critical"},
            {"metric": "Active Stations", "value": 8, "target": 10, "status": "🟡 Warning"},
            {"metric": "Queue Length", "value": 15, "target": 5, "status": "🔴 Critical"},
            {"metric": "Staff Present", "value": 12, "target": 15, "status": "🟡 Warning"},
            {"metric": "TAT Success Rate", "value": 35, "target": 90, "status": "🔴 Critical"},
            {"metric": "Break Violations", "value": 3, "target": 0, "status": "🟡 Warning"}
        ]
        
        for metric in realtime_metrics:
            self.notion.pages.create(
                parent={"database_id": self.databases['management_dashboard']},
                properties={
                    "Metric": {"title": [{"text": {"content": metric["metric"]}}]},
                    "Current Value": {"number": metric["value"]},
                    "Target": {"number": metric["target"]},
                    "Status": {"select": {"name": metric["status"]}},
                    "Last Updated": {"date": {"start": datetime.now().isoformat()}}
                }
            )
    
    def create_staff_dashboard(self):
        """Create staff performance dashboard"""
        print("👥 Creating Staff Performance Dashboard...")
        
        # Sample staff performance data
        staff_performance = [
            {"employee": "Christina B.", "score": 85, "samples": 45, "status": "✅ Excellent"},
            {"employee": "Turi K.", "score": 78, "samples": 38, "status": "✅ Good"},
            {"employee": "John D.", "score": 45, "samples": 25, "status": "⚠️ Warning"},
            {"employee": "Sarah M.", "score": 92, "samples": 52, "status": "✅ Excellent"},
            {"employee": "Mike R.", "score": 25, "samples": 0, "status": "🔴 Critical"}
        ]
        
        for staff in staff_performance:
            self.notion.pages.create(
                parent={"database_id": self.databases['staff_performance_tracker']},
                properties={
                    "Employee": {"title": [{"text": {"content": staff["employee"]}}]},
                    "Date": {"date": {"start": datetime.now().isoformat()}},
                    "Samples Processed": {"number": staff["samples"]},
                    "Performance Score": {"number": staff["score"]},
                    "Action Required": {"select": {"name": staff["status"]}}
                }
            )
    
    def create_quality_dashboard(self):
        """Create quality metrics dashboard"""
        print("⚠️ Creating Quality Metrics Dashboard...")
        
        quality_metrics = [
            {"metric": "Hidden Errors", "value": 15, "target": 0, "status": "🔴 Critical"},
            {"metric": "Self-Reported Errors", "value": 3, "target": 15, "status": "🟡 Warning"},
            {"metric": "QC Failures", "value": 8, "target": 2, "status": "🔴 Critical"},
            {"metric": "Patient Complaints", "value": 5, "target": 1, "status": "🔴 Critical"},
            {"metric": "TAT Delays", "value": 45, "target": 10, "status": "🔴 Critical"}
        ]
        
        for metric in quality_metrics:
            self.notion.pages.create(
                parent={"database_id": self.databases['management_dashboard']},
                properties={
                    "Metric": {"title": [{"text": {"content": metric["metric"]}}]},
                    "Current Value": {"number": metric["value"]},
                    "Target": {"number": metric["target"]},
                    "Status": {"select": {"name": metric["status"]}},
                    "Last Updated": {"date": {"start": datetime.now().isoformat()}}
                }
            )
    
    def create_predictive_dashboard(self):
        """Create predictive analytics dashboard"""
        print("🔮 Creating Predictive Analytics Dashboard...")
        
        predictions = [
            {"metric": "Peak Volume Prediction", "value": 1700, "target": 1200, "status": "🟠 High"},
            {"metric": "Staff Shortage Risk", "value": 85, "target": 20, "status": "🔴 Critical"},
            {"metric": "TAT Failure Probability", "value": 75, "target": 10, "status": "🔴 Critical"},
            {"metric": "Equipment Failure Risk", "value": 30, "target": 10, "status": "🟡 Warning"},
            {"metric": "No-Show Prediction", "value": 45, "target": 20, "status": "🟠 High"}
        ]
        
        for prediction in predictions:
            self.notion.pages.create(
                parent={"database_id": self.databases['management_dashboard']},
                properties={
                    "Metric": {"title": [{"text": {"content": prediction["metric"]}}]},
                    "Current Value": {"number": prediction["value"]},
                    "Target": {"number": prediction["target"]},
                    "Status": {"select": {"name": prediction["status"]}},
                    "Last Updated": {"date": {"start": datetime.now().isoformat()}}
                }
            )
    
    def create_alert_rules(self):
        """Create automated alert rules"""
        print("🚨 Setting up Alert Rules...")
        
        alert_rules = [
            {
                "alert": "TAT Critical Alert",
                "condition": "TAT < 50%",
                "action": "Notify management immediately",
                "severity": "🔴 Critical"
            },
            {
                "alert": "Wait Time Alert",
                "condition": "Wait > 20 minutes",
                "action": "Open additional station",
                "severity": "🟠 High"
            },
            {
                "alert": "Staff Missing Alert",
                "condition": "Staff idle > 30 minutes",
                "action": "Page supervisor",
                "severity": "🟡 Warning"
            },
            {
                "alert": "Break Violation Alert",
                "condition": "Break > 15 minutes",
                "action": "Log violation",
                "severity": "🟡 Warning"
            }
        ]
        
        for rule in alert_rules:
            self.notion.pages.create(
                parent={"database_id": self.databases['active_alerts']},
                properties={
                    "Alert": {"title": [{"text": {"content": rule["alert"]}}]},
                    "Time": {"date": {"start": datetime.now().isoformat()}},
                    "Type": {"select": {"name": "System Rule"}},
                    "Severity": {"select": {"name": rule["severity"]}},
                    "Resolved": {"checkbox": False}
                }
            )

def main():
    """Main function to create all dashboards"""
    # Configuration
    notion_token = os.getenv('NOTION_API_TOKEN')
    if not notion_token:
        print("❌ NOTION_TOKEN environment variable not set")
        return
    
    # Database IDs (replace with your actual IDs)
    databases = {
        'management_dashboard': 'your_dashboard_db_id',
        'staff_performance_tracker': 'your_staff_db_id',
        'active_alerts': 'your_alerts_db_id'
    }
    
    # Create dashboard creator
    creator = ManagementDashboardCreator(notion_token, databases)
    
    # Create all dashboards
    creator.create_all_dashboards()
    
    # Create alert rules
    creator.create_alert_rules()
    
    print("🎉 All management dashboards created successfully!")

if __name__ == "__main__":
    main()
