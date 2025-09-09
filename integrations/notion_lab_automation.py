"""
Complete Notion Lab Automation System
Handles all performance tracking, alerts, and team management
"""

from notion_client import Client
import pandas as pd
import json
import schedule
import time
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import requests
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class NotionLabAutomation:
    """
    Complete Notion-based lab management system
    Integrates with Epic, Qmatic, and Teams for real-time monitoring
    """
    
    def __init__(self, notion_token: str, teams_webhook: str = None):
        self.notion = Client(auth=notion_token)
        self.teams_webhook = teams_webhook
        self.databases = {}
        self.logger = self._setup_logging()
        
        # Performance thresholds from your data
        self.thresholds = {
            'tat_critical': 50,      # TAT < 50% = Critical
            'tat_warning': 70,       # TAT < 70% = Warning
            'tat_target': 90,        # TAT target = 90%
            'wait_critical': 30,     # Wait > 30 min = Critical
            'wait_warning': 20,      # Wait > 20 min = Warning
            'wait_target': 15,       # Wait target = 15 min
            'idle_max': 30,          # Idle > 30 min = Alert
            'break_max': 15,         # Break > 15 min = Violation
            'staffing_gap': 3.3      # 3.3 FTE shortage
        }
        
        self.logger.info("Notion Lab Automation System initialized")
    
    def _setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/notion_automation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def create_complete_lab_system(self, parent_page_id: str) -> Dict[str, str]:
        """
        Create complete lab management system in Notion
        Returns database IDs for all created databases
        """
        self.logger.info("Creating complete lab management system...")
        
        databases = {}
        
        # 1. Staff Performance Tracker
        databases['staff_performance'] = self._create_staff_performance_db(parent_page_id)
        
        # 2. Station Monitor
        databases['station_monitor'] = self._create_station_monitor_db(parent_page_id)
        
        # 3. Break & Attendance Log
        databases['break_tracker'] = self._create_break_tracker_db(parent_page_id)
        
        # 4. Quality & Error Tracking
        databases['quality_tracker'] = self._create_quality_tracker_db(parent_page_id)
        
        # 5. Active Alerts
        databases['alerts'] = self._create_alerts_db(parent_page_id)
        
        # 6. TAT Performance
        databases['tat_tracking'] = self._create_tat_tracking_db(parent_page_id)
        
        # 7. Management Dashboard
        databases['dashboard'] = self._create_dashboard_db(parent_page_id)
        
        # 8. Staff Accountability
        databases['accountability'] = self._create_accountability_db(parent_page_id)
        
        self.databases = databases
        self.logger.info(f"Created {len(databases)} databases successfully")
        
        return databases
    
    def _create_staff_performance_db(self, parent_page_id: str) -> str:
        """Create comprehensive staff performance database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "👥"},
            title=[{"text": {"content": "Staff Performance Tracker"}}],
            properties={
                "Employee": {"title": {}},
                "Date": {"date": {}},
                "Station": {
                    "select": {
                        "options": [
                            {"name": f"Station {i}", "color": "blue"} for i in range(1, 11)
                        ] + [
                            {"name": "Lab Bench", "color": "green"},
                            {"name": "QC Station", "color": "purple"},
                            {"name": "Float", "color": "yellow"},
                            {"name": "Break", "color": "orange"},
                            {"name": "Missing", "color": "red"}
                        ]
                    }
                },
                "Status": {
                    "select": {
                        "options": [
                            {"name": "✅ Active", "color": "green"},
                            {"name": "☕ Break", "color": "yellow"},
                            {"name": "🍽️ Lunch", "color": "orange"},
                            {"name": "⚠️ Idle", "color": "red"},
                            {"name": "❌ Missing", "color": "red"}
                        ]
                    }
                },
                "Samples Processed": {"number": {"format": "number"}},
                "Draw Time (min)": {"number": {"format": "number"}},
                "Wait Time (min)": {"number": {"format": "number"}},
                "Idle Minutes": {"number": {"format": "number"}},
                "Break Minutes": {"number": {"format": "number"}},
                "Errors Hidden": {"number": {"format": "number"}},
                "Errors Reported": {"number": {"format": "number"}},
                "TAT Compliance": {"number": {"format": "percent"}},
                "Performance Score": {
                    "formula": {
                        "expression": "round(prop(\"Samples Processed\") * 2 - prop(\"Idle Minutes\") * 0.5 - prop(\"Errors Hidden\") * 10 + prop(\"Errors Reported\") * 2)"
                    }
                },
                "Alert Flag": {"checkbox": {}},
                "Action Required": {
                    "select": {
                        "options": [
                            {"name": "None", "color": "gray"},
                            {"name": "Warning", "color": "yellow"},
                            {"name": "PIP", "color": "orange"},
                            {"name": "Termination", "color": "red"}
                        ]
                    }
                },
                "Last Updated": {"date": {}},
                "Supervisor Notes": {"rich_text": {}}
            }
        )['id']
    
    def _create_station_monitor_db(self, parent_page_id: str) -> str:
        """Create real-time station monitoring database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "🏥"},
            title=[{"text": {"content": "Station Real-Time Monitor"}}],
            properties={
                "Station": {"title": {}},
                "Current Tech": {"rich_text": {}},
                "Status": {
                    "select": {
                        "options": [
                            {"name": "🟢 Open-Staffed", "color": "green"},
                            {"name": "🟡 Open-Unstaffed", "color": "yellow"},
                            {"name": "🔴 Closed", "color": "red"},
                            {"name": "⚠️ Overflow", "color": "orange"}
                        ]
                    }
                },
                "Current Wait (min)": {"number": {"format": "number"}},
                "Queue Length": {"number": {"format": "number"}},
                "Samples/Hour": {"number": {"format": "number"}},
                "Efficiency %": {"number": {"format": "percent"}},
                "Alert Active": {"checkbox": {}},
                "Last Update": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )['id']
    
    def _create_break_tracker_db(self, parent_page_id: str) -> str:
        """Create break and attendance tracking database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "⏰"},
            title=[{"text": {"content": "Break & Attendance Log"}}],
            properties={
                "Employee": {"title": {}},
                "Type": {
                    "select": {
                        "options": [
                            {"name": "15min Break", "color": "green"},
                            {"name": "30min Lunch", "color": "blue"},
                            {"name": "Bathroom", "color": "gray"},
                            {"name": "Unauthorized", "color": "red"},
                            {"name": "No Show", "color": "red"},
                            {"name": "Late Arrival", "color": "orange"}
                        ]
                    }
                },
                "Start Time": {"date": {}},
                "End Time": {"date": {}},
                "Duration (min)": {
                    "formula": {
                        "expression": "if(empty(prop(\"End Time\")), dateBetween(now(), prop(\"Start Time\"), \"minutes\"), dateBetween(prop(\"End Time\"), prop(\"Start Time\"), \"minutes\"))"
                    }
                },
                "Violation": {"checkbox": {}},
                "Approved By": {"rich_text": {}},
                "Reason": {"rich_text": {}}
            }
        )['id']
    
    def _create_quality_tracker_db(self, parent_page_id: str) -> str:
        """Create quality and error tracking database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "⚠️"},
            title=[{"text": {"content": "Quality & Error Tracking"}}],
            properties={
                "Incident ID": {"title": {}},
                "Date": {"date": {}},
                "Employee": {"rich_text": {}},
                "Error Type": {
                    "select": {
                        "options": [
                            {"name": "Wrong Patient", "color": "red"},
                            {"name": "Wrong Test", "color": "red"},
                            {"name": "Mislabel", "color": "orange"},
                            {"name": "Hemolysis", "color": "yellow"},
                            {"name": "TAT Delay", "color": "blue"},
                            {"name": "QC Failure", "color": "purple"}
                        ]
                    }
                },
                "Severity": {
                    "select": {
                        "options": [
                            {"name": "Minor", "color": "yellow"},
                            {"name": "Major", "color": "orange"},
                            {"name": "Critical", "color": "red"}
                        ]
                    }
                },
                "Hidden Error": {"checkbox": {}},
                "Self-Reported": {"checkbox": {}},
                "Patient Impact": {"checkbox": {}},
                "Resolution": {"rich_text": {}},
                "Preventive Action": {"rich_text": {}}
            }
        )['id']
    
    def _create_alerts_db(self, parent_page_id: str) -> str:
        """Create active alerts database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "🚨"},
            title=[{"text": {"content": "Active Alerts"}}],
            properties={
                "Alert": {"title": {}},
                "Time": {"date": {}},
                "Type": {
                    "select": {
                        "options": [
                            {"name": "Wait Time", "color": "orange"},
                            {"name": "TAT Failure", "color": "red"},
                            {"name": "Staff Missing", "color": "red"},
                            {"name": "Break Violation", "color": "yellow"},
                            {"name": "Quality Issue", "color": "purple"},
                            {"name": "Equipment", "color": "blue"}
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
                "Station": {"rich_text": {}},
                "Employee": {"rich_text": {}},
                "Resolved": {"checkbox": {}},
                "Resolution Time": {"date": {}},
                "Action Taken": {"rich_text": {}}
            }
        )['id']
    
    def _create_tat_tracking_db(self, parent_page_id: str) -> str:
        """Create TAT performance tracking database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "⏱️"},
            title=[{"text": {"content": "TAT Performance Tracking"}}],
            properties={
                "Date": {"date": {}},
                "Shift": {
                    "select": {
                        "options": [
                            {"name": "Day (6AM-2PM)", "color": "blue"},
                            {"name": "Evening (2PM-10PM)", "color": "orange"},
                            {"name": "Night (10PM-6AM)", "color": "purple"}
                        ]
                    }
                },
                "Department": {
                    "select": {
                        "options": [
                            {"name": "Phlebotomy", "color": "green"},
                            {"name": "Chemistry", "color": "blue"},
                            {"name": "Hematology", "color": "red"},
                            {"name": "Microbiology", "color": "yellow"},
                            {"name": "Blood Bank", "color": "purple"}
                        ]
                    }
                },
                "STAT TAT %": {"number": {"format": "percent"}},
                "Routine TAT %": {"number": {"format": "percent"}},
                "Critical TAT %": {"number": {"format": "percent"}},
                "Overall TAT %": {"number": {"format": "percent"}},
                "Target Met": {"checkbox": {}},
                "Volume": {"number": {"format": "number"}},
                "Staff Count": {"number": {"format": "number"}},
                "Issues": {"rich_text": {}}
            }
        )['id']
    
    def _create_dashboard_db(self, parent_page_id: str) -> str:
        """Create management dashboard database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "📊"},
            title=[{"text": {"content": "Management Dashboard"}}],
            properties={
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
                "Trend": {
                    "select": {
                        "options": [
                            {"name": "📈 Improving", "color": "green"},
                            {"name": "📊 Stable", "color": "gray"},
                            {"name": "📉 Declining", "color": "red"}
                        ]
                    }
                },
                "Last Updated": {"date": {}},
                "Notes": {"rich_text": {}}
            }
        )['id']
    
    def _create_accountability_db(self, parent_page_id: str) -> str:
        """Create staff accountability tracking database"""
        return self.notion.databases.create(
            parent={"page_id": parent_page_id},
            icon={"emoji": "📋"},
            title=[{"text": {"content": "Staff Accountability"}}],
            properties={
                "Employee": {"title": {}},
                "Date": {"date": {}},
                "Performance Score": {"number": {"format": "number"}},
                "Violations": {"number": {"format": "number"}},
                "Warnings": {"number": {"format": "number"}},
                "PIP Status": {
                    "select": {
                        "options": [
                            {"name": "None", "color": "gray"},
                            {"name": "Active", "color": "orange"},
                            {"name": "Completed", "color": "green"},
                            {"name": "Failed", "color": "red"}
                        ]
                    }
                },
                "Disciplinary Action": {
                    "select": {
                        "options": [
                            {"name": "None", "color": "gray"},
                            {"name": "Verbal Warning", "color": "yellow"},
                            {"name": "Written Warning", "color": "orange"},
                            {"name": "Final Warning", "color": "red"},
                            {"name": "Termination", "color": "red"}
                        ]
                    }
                },
                "Next Review": {"date": {}},
                "Supervisor": {"rich_text": {}},
                "Notes": {"rich_text": {}}
            }
        )['id']
    
    async def send_teams_alert(self, alert_data: Dict) -> bool:
        """Send alert to Microsoft Teams"""
        if not self.teams_webhook:
            self.logger.warning("Teams webhook not configured")
            return False
        
        # Format message based on severity
        severity_colors = {
            "Info": "00FF00",
            "Warning": "FFFF00", 
            "High": "FFA500",
            "Critical": "FF0000"
        }
        
        color = severity_colors.get(alert_data.get('severity', 'Info'), "00FF00")
        
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color,
            "summary": f"Lab Alert: {alert_data.get('title', 'Unknown')}",
            "sections": [{
                "activityTitle": f"🚨 Lab Alert: {alert_data.get('title', 'Unknown')}",
                "activitySubtitle": f"Type: {alert_data.get('type', 'Unknown')}",
                "facts": [
                    {"name": "Time", "value": alert_data.get('time', 'Unknown')},
                    {"name": "Station", "value": alert_data.get('station', 'N/A')},
                    {"name": "Employee", "value": alert_data.get('employee', 'N/A')},
                    {"name": "Severity", "value": alert_data.get('severity', 'Unknown')}
                ],
                "markdown": True
            }]
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.teams_webhook, json=message) as response:
                    if response.status == 200:
                        self.logger.info(f"Alert sent to Teams: {alert_data.get('title')}")
                        return True
                    else:
                        self.logger.error(f"Failed to send Teams alert: {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"Error sending Teams alert: {e}")
            return False
    
    def create_alert(self, alert_type: str, severity: str, message: str, 
                    station: str = None, employee: str = None) -> str:
        """Create new alert in Notion and send to Teams"""
        alert_data = {
            "Alert": {"title": [{"text": {"content": message}}]},
            "Time": {"date": {"start": datetime.now().isoformat()}},
            "Type": {"select": {"name": alert_type}},
            "Severity": {"select": {"name": severity}},
            "Station": {"rich_text": [{"text": {"content": station or "N/A"}}]},
            "Employee": {"rich_text": [{"text": {"content": employee or "N/A"}}]},
            "Resolved": {"checkbox": False}
        }
        
        # Add to Notion
        try:
            alert_id = self.notion.pages.create(
                parent={"database_id": self.databases['alerts']},
                properties=alert_data
            )['id']
            
            # Send to Teams
            teams_alert = {
                'title': message,
                'type': alert_type,
                'severity': severity,
                'time': datetime.now().strftime("%H:%M"),
                'station': station or "N/A",
                'employee': employee or "N/A"
            }
            
            asyncio.create_task(self.send_teams_alert(teams_alert))
            
            self.logger.info(f"Alert created: {message}")
            return alert_id
            
        except Exception as e:
            self.logger.error(f"Error creating alert: {e}")
            return None
    
    def monitor_performance(self):
        """Monitor performance and create alerts automatically"""
        try:
            # Get current staff performance data
            staff_data = self.notion.databases.query(
                database_id=self.databases['staff_performance'],
                filter={
                    "property": "Date",
                    "date": {"equals": datetime.now().strftime("%Y-%m-%d")}
                }
            )
            
            for staff in staff_data['results']:
                props = staff['properties']
                
                # Check for performance issues
                performance_score = props.get('Performance Score', {}).get('formula', {}).get('number', 0)
                idle_minutes = props.get('Idle Minutes', {}).get('number', 0)
                break_minutes = props.get('Break Minutes', {}).get('number', 0)
                errors_hidden = props.get('Errors Hidden', {}).get('number', 0)
                
                # Create alerts based on thresholds
                if performance_score < 40:
                    self.create_alert(
                        "Staff Missing", "Critical",
                        f"Employee {props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')} has critical performance score: {performance_score}",
                        employee=props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
                    )
                
                if idle_minutes > self.thresholds['idle_max']:
                    self.create_alert(
                        "Staff Missing", "High",
                        f"Employee idle for {idle_minutes} minutes",
                        employee=props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
                    )
                
                if break_minutes > self.thresholds['break_max']:
                    self.create_alert(
                        "Break Violation", "Warning",
                        f"Employee break exceeded {break_minutes} minutes",
                        employee=props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
                    )
                
                if errors_hidden > 0:
                    self.create_alert(
                        "Quality Issue", "High",
                        f"Employee has {errors_hidden} hidden errors",
                        employee=props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
                    )
            
            self.logger.info("Performance monitoring completed")
            
        except Exception as e:
            self.logger.error(f"Error in performance monitoring: {e}")
    
    def start_automation(self):
        """Start the automated monitoring system"""
        self.logger.info("Starting lab automation system...")
        
        # Schedule monitoring tasks
        schedule.every(5).minutes.do(self.monitor_performance)
        schedule.every().hour.do(self.update_dashboard_metrics)
        schedule.every().day.at("06:00").do(self.daily_startup)
        schedule.every().day.at("18:00").do(self.daily_summary)
        
        # Run the scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def update_dashboard_metrics(self):
        """Update dashboard with current metrics"""
        try:
            # Calculate current metrics
            metrics = self._calculate_current_metrics()
            
            # Update dashboard database
            for metric_name, data in metrics.items():
                self.notion.pages.create(
                    parent={"database_id": self.databases['dashboard']},
                    properties={
                        "Metric": {"title": [{"text": {"content": metric_name}}]},
                        "Current Value": {"number": data['value']},
                        "Target": {"number": data['target']},
                        "Status": {"select": {"name": data['status']}},
                        "Trend": {"select": {"name": data['trend']}},
                        "Last Updated": {"date": {"start": datetime.now().isoformat()}}
                    }
                )
            
            self.logger.info("Dashboard metrics updated")
            
        except Exception as e:
            self.logger.error(f"Error updating dashboard: {e}")
    
    def _calculate_current_metrics(self) -> Dict:
        """Calculate current performance metrics"""
        # This would integrate with your actual data sources
        return {
            "TAT Compliance": {
                "value": 35.0,  # From your data
                "target": 90.0,
                "status": "🔴 Critical",
                "trend": "📉 Declining"
            },
            "Wait Time": {
                "value": 25.0,  # From your data
                "target": 15.0,
                "status": "🔴 Critical", 
                "trend": "📉 Declining"
            },
            "Staff Utilization": {
                "value": 67.6,  # From your data
                "target": 80.0,
                "status": "⚠️ Below Target",
                "trend": "📊 Stable"
            },
            "Error Rate": {
                "value": 12.0,  # From your data
                "target": 5.0,
                "status": "🔴 Critical",
                "trend": "📉 Declining"
            }
        }
    
    def daily_startup(self):
        """Daily startup routine"""
        self.logger.info("Running daily startup routine...")
        
        # Create daily performance entries for all staff
        # This would integrate with your HR system
        
        # Send morning summary to Teams
        morning_alert = {
            'title': 'Daily Lab Startup Complete',
            'type': 'Info',
            'severity': 'Info',
            'time': datetime.now().strftime("%H:%M"),
            'station': 'All',
            'employee': 'System'
        }
        
        asyncio.create_task(self.send_teams_alert(morning_alert))
    
    def daily_summary(self):
        """Daily summary routine"""
        self.logger.info("Running daily summary routine...")
        
        # Generate daily performance report
        # Send to management
        
        summary_alert = {
            'title': 'Daily Lab Performance Summary',
            'type': 'Info', 
            'severity': 'Info',
            'time': datetime.now().strftime("%H:%M"),
            'station': 'All',
            'employee': 'System'
        }
        
        asyncio.create_task(self.send_teams_alert(summary_alert))

# Example usage
if __name__ == "__main__":
    # Initialize the system
    automation = NotionLabAutomation(
        notion_token=os.getenv('NOTION_API_TOKEN'),
        teams_webhook=os.getenv('TEAMS_WEBHOOK_URL')
    )
    
    # Create the complete system
    parent_page_id = "your_parent_page_id_here"
    databases = automation.create_complete_lab_system(parent_page_id)
    
    print("Lab automation system created successfully!")
    print(f"Database IDs: {databases}")
    
    # Start monitoring
    automation.start_automation()
