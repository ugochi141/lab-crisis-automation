"""
Complete Lab Management System
Using your specific Notion, Power BI, and Teams credentials
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from notion_client import Client
import requests
import schedule
import time

from config.lab_config import LabConfig

class NotionLabManager:
    """
    Complete lab management system using your specific databases
    """
    
    def __init__(self):
        self.config = LabConfig()
        self.notion = Client(auth=self.config.NOTION_API_TOKEN)
        self.logger = self._setup_logging()
        
        # Track sent alerts to avoid spam
        self.sent_alerts = set()
        self.last_alert_time = {}
        
        self.logger.info("Lab Management System initialized with your credentials")
    
    def _setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/lab_management.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    async def send_teams_alert(self, alert_data: Dict) -> bool:
        """Send alert to your Kaiser Permanente Teams channel"""
        try:
            # Format message based on severity
            severity_colors = {
                "⚪ Info": "00FF00",
                "🟡 Warning": "FFFF00", 
                "🟠 High": "FFA500",
                "🔴 Critical": "FF0000"
            }
            
            color = severity_colors.get(alert_data.get('severity', '⚪ Info'), "00FF00")
            
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
                        {"name": "Severity", "value": alert_data.get('severity', 'Unknown')},
                        {"name": "Action Required", "value": alert_data.get('action', 'Review immediately')}
                    ],
                    "markdown": True
                }]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.TEAMS_WEBHOOK_URL, 
                    json=message,
                    headers=self.config.get_teams_headers(),
                    timeout=10
                ) as response:
                    if response.status == 200:
                        self.logger.info(f"Alert sent to Teams: {alert_data.get('title')}")
                        return True
                    else:
                        self.logger.error(f"Failed to send Teams alert: {response.status}")
                        return False
        except Exception as e:
            self.logger.error(f"Error sending Teams alert: {e}")
            return False
    
    def create_performance_alert(self, alert_type: str, severity: str, message: str, 
                               station: str = None, employee: str = None, 
                               action: str = None) -> str:
        """Create new alert in your Notion Performance database"""
        try:
            alert_data = {
                "Alert": {"title": [{"text": {"content": message}}]},
                "Time": {"date": {"start": datetime.now().isoformat()}},
                "Type": {"select": {"name": alert_type}},
                "Severity": {"select": {"name": severity}},
                "Station": {"rich_text": [{"text": {"content": station or "N/A"}}]},
                "Employee": {"rich_text": [{"text": {"content": employee or "N/A"}}]},
                "Action Required": {"rich_text": [{"text": {"content": action or "Review immediately"}}]},
                "Resolved": {"checkbox": False}
            }
            
            # Add to your Performance database
            alert_id = self.notion.pages.create(
                parent={"database_id": self.config.NOTION_PERFORMANCE_DB_ID},
                properties=alert_data
            )['id']
            
            # Send to Teams
            teams_alert = {
                'title': message,
                'type': alert_type,
                'severity': severity,
                'time': datetime.now().strftime("%H:%M"),
                'station': station or "N/A",
                'employee': employee or "N/A",
                'action': action or "Review immediately"
            }
            
            asyncio.create_task(self.send_teams_alert(teams_alert))
            
            self.logger.info(f"Performance alert created: {message}")
            return alert_id
            
        except Exception as e:
            self.logger.error(f"Error creating performance alert: {e}")
            return None
    
    def create_incident_alert(self, incident_type: str, severity: str, description: str,
                            employee: str = None, station: str = None) -> str:
        """Create incident in your Notion Incident database"""
        try:
            incident_data = {
                "Incident": {"title": [{"text": {"content": description}}]},
                "Date": {"date": {"start": datetime.now().isoformat()}},
                "Type": {"select": {"name": incident_type}},
                "Severity": {"select": {"name": severity}},
                "Employee": {"rich_text": [{"text": {"content": employee or "N/A"}}]},
                "Station": {"rich_text": [{"text": {"content": station or "N/A"}}]},
                "Status": {"select": {"name": "Open"}},
                "Resolution": {"rich_text": [{"text": {"content": "Pending investigation"}}]}
            }
            
            incident_id = self.notion.pages.create(
                parent={"database_id": self.config.NOTION_INCIDENT_DB_ID},
                properties=incident_data
            )['id']
            
            self.logger.info(f"Incident created: {description}")
            return incident_id
            
        except Exception as e:
            self.logger.error(f"Error creating incident: {e}")
            return None
    
    def push_to_powerbi_monitor(self, data: Dict) -> bool:
        """Push monitoring data to your Power BI Monitor dataset"""
        try:
            payload = [{
                "timestamp": datetime.now().isoformat(),
                "station": data.get('station', 'Unknown'),
                "employee": data.get('employee', 'Unknown'),
                "wait_time": data.get('wait_time', 0),
                "tat_percentage": data.get('tat_percentage', 0),
                "samples_processed": data.get('samples_processed', 0),
                "idle_minutes": data.get('idle_minutes', 0),
                "break_minutes": data.get('break_minutes', 0),
                "performance_score": data.get('performance_score', 0),
                "alert_level": data.get('alert_level', 'Info')
            }]
            
            response = requests.post(
                self.config.POWERBI_MONITOR_PUSH_URL,
                json=payload,
                headers=self.config.get_powerbi_headers(),
                timeout=self.config.REQUEST_TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                self.logger.info("Data pushed to Power BI Monitor successfully")
                return True
            else:
                self.logger.error(f"Power BI Monitor push failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error pushing to Power BI Monitor: {e}")
            return False
    
    def push_to_powerbi_metrics(self, metrics: Dict) -> bool:
        """Push lab metrics to your Power BI Metrics dataset"""
        try:
            payload = [{
                "timestamp": datetime.now().isoformat(),
                "overall_tat_percentage": metrics.get('overall_tat', 35.0),  # Your current crisis
                "average_wait_time": metrics.get('avg_wait_time', 25.0),
                "staff_utilization": metrics.get('staff_utilization', 67.6),
                "error_rate": metrics.get('error_rate', 12.0),
                "break_violations": metrics.get('break_violations', 0),
                "no_shows": metrics.get('no_shows', 0),
                "staffing_gap": metrics.get('staffing_gap', 3.3),
                "critical_alerts": metrics.get('critical_alerts', 0),
                "performance_trend": metrics.get('performance_trend', 'Declining')
            }]
            
            response = requests.post(
                self.config.POWERBI_METRICS_PUSH_URL,
                json=payload,
                headers=self.config.get_powerbi_headers(),
                timeout=self.config.REQUEST_TIMEOUT_SECONDS
            )
            
            if response.status_code == 200:
                self.logger.info("Metrics pushed to Power BI successfully")
                return True
            else:
                self.logger.error(f"Power BI Metrics push failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error pushing to Power BI Metrics: {e}")
            return False
    
    def monitor_staff_performance(self):
        """Monitor staff performance and create alerts"""
        self.logger.info("Monitoring staff performance...")
        
        try:
            # Get current staff data from your Performance database
            staff_data = self.notion.databases.query(
                database_id=self.config.NOTION_PERFORMANCE_DB_ID,
                filter={
                    "property": "Date",
                    "date": {"equals": datetime.now().strftime("%Y-%m-%d")}
                }
            )
            
            critical_alerts = 0
            
            for staff in staff_data['results']:
                props = staff['properties']
                
                # Extract staff data
                employee_name = props.get('Employee', {}).get('title', [{}])[0].get('text', {}).get('content', 'Unknown')
                samples = props.get('Samples Processed', {}).get('number', 0)
                idle_minutes = props.get('Idle Minutes', {}).get('number', 0)
                break_minutes = props.get('Break Minutes', {}).get('number', 0)
                errors_hidden = props.get('Errors Hidden', {}).get('number', 0)
                tat_compliance = props.get('TAT Compliance', {}).get('number', 0)
                
                # Calculate performance score
                staff_data_dict = {
                    'samples_processed': samples,
                    'idle_minutes': idle_minutes,
                    'break_minutes': break_minutes,
                    'errors_hidden': errors_hidden,
                    'tat_compliance': tat_compliance
                }
                
                performance_score = self.config.calculate_performance_score(staff_data_dict)
                
                # Check for critical issues
                if performance_score < 40:
                    self.create_performance_alert(
                        "Staff Performance", "🔴 Critical",
                        f"CRITICAL: {employee_name} has performance score {performance_score} - Immediate action required",
                        employee=employee_name,
                        action="Place on PIP or consider termination"
                    )
                    critical_alerts += 1
                
                if idle_minutes > self.config.CRISIS_THRESHOLDS['idle_max']:
                    self.create_performance_alert(
                        "Staff Missing", "🟠 High",
                        f"ALERT: {employee_name} idle for {idle_minutes} minutes",
                        employee=employee_name,
                        action="Page employee and find coverage"
                    )
                
                if break_minutes > self.config.CRISIS_THRESHOLDS['break_max']:
                    self.create_performance_alert(
                        "Break Violation", "🟡 Warning",
                        f"VIOLATION: {employee_name} break exceeded {break_minutes} minutes",
                        employee=employee_name,
                        action="Log violation and issue warning"
                    )
                
                if errors_hidden > 0:
                    self.create_incident_alert(
                        "Quality Issue", "🔴 Critical",
                        f"INCIDENT: {employee_name} has {errors_hidden} hidden errors",
                        employee=employee_name
                    )
                
                # Push individual staff data to Power BI
                self.push_to_powerbi_monitor({
                    'employee': employee_name,
                    'samples_processed': samples,
                    'idle_minutes': idle_minutes,
                    'break_minutes': break_minutes,
                    'performance_score': performance_score,
                    'alert_level': 'Critical' if performance_score < 40 else 'Warning' if performance_score < 60 else 'Info'
                })
            
            # Push overall metrics to Power BI
            self.push_to_powerbi_metrics({
                'overall_tat': 35.0,  # Your current crisis data
                'avg_wait_time': 25.0,
                'staff_utilization': 67.6,
                'error_rate': 12.0,
                'critical_alerts': critical_alerts,
                'performance_trend': 'Declining'
            })
            
            self.logger.info(f"Performance monitoring completed. Critical alerts: {critical_alerts}")
            
        except Exception as e:
            self.logger.error(f"Error in performance monitoring: {e}")
    
    def monitor_tat_performance(self):
        """Monitor TAT performance and create alerts"""
        self.logger.info("Monitoring TAT performance...")
        
        try:
            # Your current TAT crisis: 35% compliance (need 90%)
            current_tat = 35.0
            target_tat = 90.0
            
            if current_tat < self.config.CRISIS_THRESHOLDS['tat_critical']:
                self.create_performance_alert(
                    "TAT Crisis", "🔴 Critical",
                    f"CRISIS: TAT compliance only {current_tat}% (target: {target_tat}%) - Immediate intervention required",
                    action="Deploy all available staff, open additional stations, escalate to management"
                )
            
            # Monitor individual department TAT
            departments = [
                {"name": "Phlebotomy", "tat": 51, "target": 85},
                {"name": "Chemistry", "tat": 45, "target": 90},
                {"name": "Hematology", "tat": 38, "target": 90},
                {"name": "Blood Bank", "tat": 42, "target": 95}
            ]
            
            for dept in departments:
                if dept['tat'] < 50:  # Critical threshold
                    self.create_performance_alert(
                        "Department TAT", "🔴 Critical",
                        f"CRISIS: {dept['name']} TAT only {dept['tat']}% (target: {dept['target']}%)",
                        action="Reallocate staff, check equipment, review processes"
                    )
            
        except Exception as e:
            self.logger.error(f"Error monitoring TAT: {e}")
    
    def monitor_wait_times(self):
        """Monitor wait times and create alerts"""
        self.logger.info("Monitoring wait times...")
        
        try:
            # Your current crisis: 25+ minute wait times (target: 15 min)
            current_wait = 25.0
            target_wait = 15.0
            
            if current_wait > self.config.CRISIS_THRESHOLDS['wait_critical']:
                self.create_performance_alert(
                    "Wait Time Crisis", "🔴 Critical",
                    f"CRISIS: Average wait time {current_wait} minutes (target: {target_wait} min) - Patients waiting too long",
                    action="Open additional stations, deploy float staff, notify management"
                )
            
            # Monitor individual stations
            stations = [
                {"name": "Station 1", "wait": 30, "status": "Overflow"},
                {"name": "Station 2", "wait": 25, "status": "High"},
                {"name": "Station 3", "wait": 35, "status": "Critical"},
                {"name": "Station 4", "wait": 20, "status": "Warning"}
            ]
            
            for station in stations:
                if station['wait'] > 20:
                    self.create_performance_alert(
                        "Station Wait Time", "🟠 High",
                        f"ALERT: {station['name']} wait time {station['wait']} minutes - {station['status']}",
                        station=station['name'],
                        action="Deploy additional staff or open overflow station"
                    )
            
        except Exception as e:
            self.logger.error(f"Error monitoring wait times: {e}")
    
    def check_staffing_crisis(self):
        """Check staffing crisis and create alerts"""
        self.logger.info("Checking staffing crisis...")
        
        try:
            # Your current crisis: 3.3 FTE shortage
            current_staff = 28.75
            needed_staff = 32.05
            gap = 3.3
            
            if gap > 2.0:  # Critical staffing shortage
                self.create_performance_alert(
                    "Staffing Crisis", "🔴 Critical",
                    f"CRISIS: {gap} FTE shortage ({current_staff}/{needed_staff}) - Cannot meet demand",
                    action="Emergency hiring, overtime approval, temporary staff, management coverage"
                )
            
            # Check shift coverage
            shifts = [
                {"name": "Day Shift", "needed": 12, "present": 10, "gap": 2},
                {"name": "Evening Shift", "needed": 8, "present": 6, "gap": 2},
                {"name": "Night Shift", "needed": 4, "present": 3, "gap": 1}
            ]
            
            for shift in shifts:
                if shift['gap'] > 1:
                    self.create_performance_alert(
                        "Shift Coverage", "🟠 High",
                        f"ALERT: {shift['name']} understaffed by {shift['gap']} FTE",
                        action="Call in float staff, approve overtime, management coverage"
                    )
            
        except Exception as e:
            self.logger.error(f"Error checking staffing: {e}")
    
    def run_crisis_monitoring(self):
        """Run complete crisis monitoring cycle"""
        self.logger.info("🚨 Running crisis monitoring cycle...")
        
        # Monitor all critical areas
        self.monitor_staff_performance()
        self.monitor_tat_performance()
        self.monitor_wait_times()
        self.check_staffing_crisis()
        
        self.logger.info("✅ Crisis monitoring cycle completed")
    
    def start_automation(self):
        """Start the automated monitoring system"""
        self.logger.info("🚀 Starting lab automation system...")
        
        # Schedule monitoring tasks
        schedule.every(5).minutes.do(self.run_crisis_monitoring)
        schedule.every().hour.do(self.send_daily_summary)
        schedule.every().day.at("06:00").do(self.morning_startup)
        schedule.every().day.at("18:00").do(self.evening_summary)
        
        # Run the scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def morning_startup(self):
        """Daily morning startup routine"""
        self.logger.info("🌅 Running morning startup routine...")
        
        # Send morning summary to Teams
        morning_alert = {
            'title': 'Daily Lab Startup - Crisis Mode',
            'type': 'System',
            'severity': '🟡 Warning',
            'time': datetime.now().strftime("%H:%M"),
            'station': 'All',
            'employee': 'System',
            'action': 'Review overnight alerts and prepare for crisis management'
        }
        
        asyncio.create_task(self.send_teams_alert(morning_alert))
    
    def evening_summary(self):
        """Daily evening summary routine"""
        self.logger.info("🌆 Running evening summary routine...")
        
        # Send evening summary to Teams
        evening_alert = {
            'title': 'Daily Lab Summary - Crisis Status',
            'type': 'System',
            'severity': '🟡 Warning',
            'time': datetime.now().strftime("%H:%M"),
            'station': 'All',
            'employee': 'System',
            'action': 'Review daily performance and plan tomorrow\'s crisis response'
        }
        
        asyncio.create_task(self.send_teams_alert(evening_alert))
    
    def send_daily_summary(self):
        """Send hourly summary during business hours"""
        current_hour = datetime.now().hour
        if 6 <= current_hour <= 20:  # Business hours
            summary_alert = {
                'title': f'Hourly Lab Status - {datetime.now().strftime("%H:%M")}',
                'type': 'Status',
                'severity': '⚪ Info',
                'time': datetime.now().strftime("%H:%M"),
                'station': 'All',
                'employee': 'System',
                'action': 'Continue monitoring and responding to alerts'
            }
            
            asyncio.create_task(self.send_teams_alert(summary_alert))

# Example usage
if __name__ == "__main__":
    # Initialize the system
    lab_manager = NotionLabManager()
    
    # Run a single monitoring cycle
    lab_manager.run_crisis_monitoring()
    
    # Or start continuous monitoring
    # lab_manager.start_automation()
