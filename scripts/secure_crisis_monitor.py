#!/usr/bin/env python3
"""
Secure Lab Crisis Monitor
Uses environment variables for sensitive data
"""

import os
import requests
import json
from datetime import datetime
from notion_client import Client
from config.secure_config import SecureLabConfig

def load_config():
    """Load configuration from environment variables"""
    config = SecureLabConfig()
    try:
        config.validate_config()
        return config
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set the required environment variables:")
        print("  export NOTION_API_TOKEN='your_token_here'")
        print("  export NOTION_PERFORMANCE_DB_ID='your_db_id_here'")
        print("  export NOTION_INCIDENT_DB_ID='your_incident_db_id_here'")
        print("  export TEAMS_WEBHOOK_URL='your_webhook_url_here'")
        return None

def send_teams_alert(webhook_url, alert_data):
    """Send alert to Teams"""
    try:
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": alert_data.get('color', 'FF0000'),
            "summary": f"Lab Crisis Alert: {alert_data.get('title', 'Unknown')}",
            "sections": [{
                "activityTitle": f"🚨 Lab Crisis Alert: {alert_data.get('title', 'Unknown')}",
                "activitySubtitle": f"Type: {alert_data.get('type', 'Unknown')} | Severity: {alert_data.get('severity', 'Unknown')}",
                "facts": [
                    {"name": "Time", "value": alert_data.get('time', 'Unknown')},
                    {"name": "Staff Member", "value": alert_data.get('staff', 'N/A')},
                    {"name": "Current Value", "value": alert_data.get('current', 'N/A')},
                    {"name": "Target", "value": alert_data.get('target', 'N/A')},
                    {"name": "Action Required", "value": alert_data.get('action', 'Review immediately')}
                ],
                "markdown": True
            }]
        }
        
        response = requests.post(
            webhook_url,
            json=message,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ Alert sent to Teams: {alert_data.get('title')}")
            return True
        else:
            print(f"❌ Teams alert failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Teams alert error: {e}")
        return False

def create_performance_entry(notion, db_id, staff_data):
    """Create performance entry in Notion database"""
    try:
        # Calculate performance score
        samples = staff_data.get('samples', 0)
        errors = staff_data.get('errors', 0)
        break_time = staff_data.get('break_time', 0)
        qc_completion = staff_data.get('qc_completion', 0)
        
        performance_score = max(0, samples * 2 - errors * 10 - break_time * 0.5 + qc_completion * 0.1)
        
        entry_data = {
            "Staff Member": {"title": [{"text": {"content": staff_data.get('name', 'Unknown')}}]},
            "Date": {"date": {"start": datetime.now().isoformat()}},
            "Samples Processed": {"number": samples},
            "Error Count": {"number": errors},
            "Break Time (mins)": {"number": break_time},
            "QC Completion %": {"number": qc_completion},
            "TAT Target Met": {"checkbox": qc_completion >= 90},
            "Status": {"select": {"name": staff_data.get('status', 'Active')}},
            "Shift": {"select": {"name": staff_data.get('shift', 'Day')}},
            "Notes": {"rich_text": [{"text": {"content": staff_data.get('notes', 'Crisis monitoring entry')}}]}
        }
        
        entry_id = notion.pages.create(
            parent={"database_id": db_id},
            properties=entry_data
        )['id']
        
        print(f"✅ Performance entry created for {staff_data.get('name')}")
        return entry_id
        
    except Exception as e:
        print(f"❌ Error creating performance entry: {e}")
        return None

def create_incident_entry(notion, db_id, incident_data):
    """Create incident entry in Notion database"""
    try:
        entry_data = {
            "Incident ID": {"title": [{"text": {"content": incident_data.get('id', f"CRISIS-{datetime.now().strftime('%Y%m%d%H%M')}")}}]},
            "Date/Time": {"date": {"start": datetime.now().isoformat()}},
            "Description": {"rich_text": [{"text": {"content": incident_data.get('description', 'Crisis incident')}}]},
            "Incident Type": {"select": {"name": incident_data.get('type', 'Performance')}},
            "Severity": {"select": {"name": incident_data.get('severity', 'High')}},
            "Staff Member": {"select": {"name": incident_data.get('staff', 'System')}},
            "Impact": {"select": {"name": incident_data.get('impact', 'High')}},
            "Status": {"select": {"name": "Open"}},
            "Root Cause": {"rich_text": [{"text": {"content": incident_data.get('root_cause', 'Under investigation')}}]},
            "Corrective Action": {"rich_text": [{"text": {"content": incident_data.get('action', 'Immediate intervention required')}}]},
            "Follow-up Date": {"date": {"start": (datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)).isoformat()}}
        }
        
        entry_id = notion.pages.create(
            parent={"database_id": db_id},
            properties=entry_data
        )['id']
        
        print(f"✅ Incident entry created: {incident_data.get('id')}")
        return entry_id
        
    except Exception as e:
        print(f"❌ Error creating incident entry: {e}")
        return None

def monitor_crisis():
    """Monitor lab crisis and create alerts"""
    print("🚨 Starting Secure Lab Crisis Monitoring...")
    
    # Load configuration
    config = load_config()
    if not config:
        return False
    
    notion = Client(auth=config.NOTION_API_TOKEN)
    
    # Your current crisis data
    crisis_data = {
        'tat_compliance': 35.0,  # Only 35% meeting targets
        'wait_time': 25.0,       # 25+ minute wait times
        'staffing_gap': 3.3,     # 3.3 FTE shortage
        'error_rate': 12.0,      # 12% error rate
        'staff_utilization': 67.6 # Only 67.6% utilization
    }
    
    # Sample staff data
    staff_data = [
        {'name': 'Christina B.', 'samples': 45, 'errors': 2, 'break_time': 20, 'qc_completion': 85, 'status': 'Active'},
        {'name': 'Turi K.', 'samples': 38, 'errors': 1, 'break_time': 15, 'qc_completion': 90, 'status': 'Active'},
        {'name': 'John D.', 'samples': 25, 'errors': 5, 'break_time': 45, 'qc_completion': 70, 'status': 'Idle'},
        {'name': 'Sarah M.', 'samples': 52, 'errors': 1, 'break_time': 10, 'qc_completion': 95, 'status': 'Active'},
        {'name': 'Mike R.', 'samples': 0, 'errors': 0, 'break_time': 120, 'qc_completion': 0, 'status': 'Missing'}
    ]
    
    # Create performance entries for all staff
    for staff in staff_data:
        create_performance_entry(notion, config.NOTION_PERFORMANCE_DB_ID, staff)
    
    # Check for critical issues and create alerts
    alerts_sent = 0
    
    # TAT Crisis Alert
    if crisis_data['tat_compliance'] < config.CRISIS_THRESHOLDS['tat_critical']:
        alert_data = {
            'title': 'TAT Crisis - Immediate Action Required',
            'type': 'TAT Failure',
            'severity': 'Critical',
            'time': datetime.now().strftime('%H:%M'),
            'staff': 'All Staff',
            'current': f"{crisis_data['tat_compliance']}%",
            'target': '90%',
            'action': 'Deploy all available staff, open additional stations, escalate to management',
            'color': 'FF0000'
        }
        send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
        alerts_sent += 1
        
        # Create incident
        create_incident_entry(notion, config.NOTION_INCIDENT_DB_ID, {
            'id': f"TAT-CRISIS-{datetime.now().strftime('%Y%m%d%H%M')}",
            'description': f"TAT compliance critically low at {crisis_data['tat_compliance']}%",
            'type': 'Performance',
            'severity': 'Critical',
            'staff': 'All Staff',
            'impact': 'High',
            'root_cause': 'Insufficient staffing and process inefficiencies',
            'action': 'Emergency staffing deployment and process review'
        })
    
    # Wait Time Crisis Alert
    if crisis_data['wait_time'] > config.CRISIS_THRESHOLDS['wait_warning']:
        alert_data = {
            'title': 'Wait Time Crisis - Patients Waiting Too Long',
            'type': 'Wait Time',
            'severity': 'Critical',
            'time': datetime.now().strftime('%H:%M'),
            'staff': 'All Staff',
            'current': f"{crisis_data['wait_time']} minutes",
            'target': '15 minutes',
            'action': 'Open additional stations, deploy float staff, notify management',
            'color': 'FF0000'
        }
        send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
        alerts_sent += 1
    
    # Staffing Crisis Alert
    if crisis_data['staffing_gap'] > 2:
        alert_data = {
            'title': 'Staffing Crisis - Cannot Meet Demand',
            'type': 'Staffing',
            'severity': 'Critical',
            'time': datetime.now().strftime('%H:%M'),
            'staff': 'Management',
            'current': f"{28.75} FTE",
            'target': f"{32.05} FTE",
            'action': 'Emergency hiring, overtime approval, temporary staff, management coverage',
            'color': 'FF0000'
        }
        send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
        alerts_sent += 1
    
    # Check individual staff performance
    for staff in staff_data:
        if staff['samples'] < 20 and staff['status'] == 'Active':
            alert_data = {
                'title': f'Low Performance Alert - {staff["name"]}',
                'type': 'Staff Performance',
                'severity': 'High',
                'time': datetime.now().strftime('%H:%M'),
                'staff': staff['name'],
                'current': f"{staff['samples']} samples",
                'target': '40+ samples',
                'action': 'Review performance and provide coaching',
                'color': 'FFA500'
            }
            send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
            alerts_sent += 1
        
        if staff['break_time'] > config.CRISIS_THRESHOLDS['break_max']:
            alert_data = {
                'title': f'Break Violation - {staff["name"]}',
                'type': 'Break Violation',
                'severity': 'Warning',
                'time': datetime.now().strftime('%H:%M'),
                'staff': staff['name'],
                'current': f"{staff['break_time']} minutes",
                'target': '15 minutes max',
                'action': 'Log violation and issue warning',
                'color': 'FFFF00'
            }
            send_teams_alert(config.TEAMS_WEBHOOK_URL, alert_data)
            alerts_sent += 1
    
    print(f"🎯 Crisis monitoring completed. {alerts_sent} alerts sent to Teams.")
    print("📊 Performance data added to Notion databases.")
    print("🚨 Incident reports created for critical issues.")
    return True

if __name__ == "__main__":
    monitor_crisis()
