#!/usr/bin/env python3
"""
Create Lab Monitoring Dashboard in Notion
Comprehensive dashboard for Kaiser Permanente Lab Operations
"""

import os
import json
from datetime import datetime
from pathlib import Path

def create_dashboard_structure():
    """Create the complete dashboard structure"""
    
    dashboard_config = {
        "dashboard_name": "Kaiser Permanente Lab Operations Command Center",
        "created": datetime.now().isoformat(),
        "version": "2.0.0",
        "databases": {
            "critical_alerts": {
                "name": "🚨 Critical Alerts Database",
                "description": "Real-time critical incidents requiring immediate response",
                "properties": {
                    "Alert ID": {"type": "title"},
                    "Timestamp": {"type": "date"},
                    "Priority": {"type": "select", "options": ["🔴 CRITICAL", "🟠 HIGH", "🟡 MEDIUM", "🟢 LOW"]},
                    "Category": {"type": "select", "options": [
                        "Patient Safety", "System Failure", "Staffing Crisis", 
                        "Equipment Down", "Critical Value", "Network Issue"
                    ]},
                    "Department": {"type": "select", "options": [
                        "Chemistry", "Hematology", "Microbiology", "Blood Bank", 
                        "Phlebotomy", "IT Systems", "Administration"
                    ]},
                    "Keyword Triggered": {"type": "rich_text"},
                    "Original Message": {"type": "rich_text"},
                    "Status": {"type": "select", "options": [
                        "🟥 Open", "🟨 In Progress", "🟩 Resolved", "🟦 Escalated"
                    ]},
                    "Assigned To": {"type": "people"},
                    "Resolution Time": {"type": "number"},
                    "Impact Level": {"type": "select", "options": ["1-Low", "2-Medium", "3-High", "4-Critical"]},
                    "Follow-up Required": {"type": "checkbox"}
                }
            },
            "staffing_tracking": {
                "name": "👥 Staffing & Attendance Tracker",
                "description": "Real-time staff availability and attendance monitoring",
                "properties": {
                    "Entry ID": {"type": "title"},
                    "Date": {"type": "date"},
                    "Employee Name": {"type": "rich_text"},
                    "Department": {"type": "select", "options": [
                        "Chemistry", "Hematology", "Microbiology", "Blood Bank", "Phlebotomy"
                    ]},
                    "Shift": {"type": "select", "options": ["Day", "Evening", "Night", "Weekend"]},
                    "Status": {"type": "select", "options": [
                        "✅ Present", "❌ Called Out", "⚠️ Late", "🏥 Medical Leave", 
                        "🏖️ Vacation", "🔄 Coverage Found", "🚨 No Coverage"
                    ]},
                    "Reason": {"type": "rich_text"},
                    "Coverage Status": {"type": "select", "options": [
                        "✅ Covered", "🔄 Finding Coverage", "🚨 No Coverage", "💰 Overtime"
                    ]},
                    "Notification Sent": {"type": "checkbox"},
                    "Pattern Flag": {"type": "checkbox"},
                    "Occurrence Count": {"type": "number"}
                }
            },
            "system_status": {
                "name": "🖥️ System Status Monitor",
                "description": "Track all lab systems, analyzers, and IT infrastructure",
                "properties": {
                    "System Name": {"type": "title"},
                    "Category": {"type": "select", "options": [
                        "Analyzer", "IT System", "Network", "Tube System", 
                        "LIMS", "Interface", "Backup System"
                    ]},
                    "Department": {"type": "select", "options": [
                        "Chemistry", "Hematology", "Microbiology", "Blood Bank", 
                        "IT", "All Departments"
                    ]},
                    "Status": {"type": "select", "options": [
                        "🟢 Online", "🟡 Warning", "🔴 Down", "🔧 Maintenance", "🔄 Restarting"
                    ]},
                    "Last Updated": {"type": "date"},
                    "Uptime %": {"type": "number"},
                    "Issue Description": {"type": "rich_text"},
                    "Service Called": {"type": "checkbox"},
                    "ETA Resolution": {"type": "date"},
                    "Impact Assessment": {"type": "rich_text"},
                    "Backup Available": {"type": "checkbox"}
                }
            },
            "hr_compliance": {
                "name": "📋 HR Compliance Tracker",
                "description": "Monitor FMLA, certifications, and compliance requirements",
                "properties": {
                    "Record ID": {"type": "title"},
                    "Employee Name": {"type": "rich_text"},
                    "Type": {"type": "select", "options": [
                        "FMLA", "Medical Leave", "Workers Comp", "Certification", 
                        "Training", "Disciplinary Action", "Performance Review"
                    ]},
                    "Status": {"type": "select", "options": [
                        "🟢 Current", "🟡 Due Soon", "🔴 Overdue", "📋 In Review", "✅ Completed"
                    ]},
                    "Due Date": {"type": "date"},
                    "Completion Date": {"type": "date"},
                    "Days Overdue": {"type": "formula"},
                    "Priority": {"type": "select", "options": ["Low", "Medium", "High", "Critical"]},
                    "Action Required": {"type": "rich_text"},
                    "Compliance Risk": {"type": "select", "options": ["Low", "Medium", "High"]}
                }
            },
            "performance_metrics": {
                "name": "📊 Performance Metrics Dashboard",
                "description": "Track KPIs, TAT, QC, and operational performance",
                "properties": {
                    "Metric Name": {"type": "title"},
                    "Date": {"type": "date"},
                    "Department": {"type": "select", "options": [
                        "Chemistry", "Hematology", "Microbiology", "Blood Bank", "Overall"
                    ]},
                    "Metric Type": {"type": "select", "options": [
                        "TAT", "QC Performance", "Productivity", "Error Rate", 
                        "Specimen Quality", "Staff Utilization"
                    ]},
                    "Target Value": {"type": "number"},
                    "Actual Value": {"type": "number"},
                    "Performance %": {"type": "formula"},
                    "Status": {"type": "select", "options": [
                        "🟢 On Target", "🟡 Below Target", "🔴 Critical"
                    ]},
                    "Trend": {"type": "select", "options": ["📈 Improving", "📊 Stable", "📉 Declining"]},
                    "Action Items": {"type": "rich_text"}
                }
            }
        },
        "views": {
            "command_center": {
                "name": "🎯 Command Center Overview",
                "type": "dashboard",
                "components": [
                    "Current Critical Alerts",
                    "System Status Summary", 
                    "Staffing Status",
                    "Performance Metrics",
                    "Compliance Alerts"
                ]
            },
            "realtime_alerts": {
                "name": "🚨 Real-Time Alert Monitor",
                "type": "table",
                "filter": "Status = Open OR In Progress",
                "sort": "Priority DESC, Timestamp DESC"
            },
            "staffing_board": {
                "name": "👥 Daily Staffing Board",
                "type": "kanban",
                "group_by": "Department",
                "filter": "Date = Today"
            },
            "system_health": {
                "name": "💚 System Health Dashboard",
                "type": "gallery",
                "group_by": "Department",
                "filter": "Status != Offline"
            }
        },
        "automation_rules": {
            "critical_escalation": {
                "name": "Critical Alert Auto-Escalation",
                "trigger": "New critical alert created",
                "condition": "Priority = CRITICAL AND no response in 5 minutes",
                "action": "Escalate to next level + send SMS"
            },
            "attendance_pattern": {
                "name": "Attendance Pattern Detection",
                "trigger": "New attendance record",
                "condition": "Same person, 3+ absences in 30 days",
                "action": "Flag for HR review + notify manager"
            },
            "compliance_reminder": {
                "name": "Compliance Due Date Alerts",
                "trigger": "Daily at 8:00 AM",
                "condition": "Due date within 7 days",
                "action": "Send reminder notification"
            }
        },
        "keyword_mapping": {
            "critical_alerts": [
                "STAT", "critical value", "panic value", "code blue", "code red", 
                "emergency", "patient safety", "wrong blood", "transfusion urgent",
                "contamination", "system down", "analyzer down", "instrument failure"
            ],
            "staffing_issues": [
                "calling out", "call out", "won't be in", "can't make it", "sick today",
                "no show", "absent", "need coverage", "short staffed", "no coverage"
            ],
            "system_status": [
                "system down", "analyzer down", "tube system down", "network down",
                "interface down", "maintenance", "is down", "is back up"
            ],
            "hr_compliance": [
                "FMLA", "medical leave", "workers comp", "injury", "disciplinary action",
                "performance review", "certification", "training", "compliance"
            ]
        }
    }
    
    return dashboard_config

def generate_notion_setup_guide():
    """Generate step-by-step Notion setup guide"""
    
    setup_guide = """
# 🏥 Kaiser Permanente Lab Monitoring Dashboard Setup Guide

## Phase 1: Database Creation

### 1. Critical Alerts Database 🚨
```
Name: 🚨 Critical Alerts Database
Properties:
- Alert ID (Title)
- Timestamp (Date & Time) 
- Priority (Select: 🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)
- Category (Select: Patient Safety, System Failure, Staffing Crisis, Equipment Down, Critical Value, Network Issue)
- Department (Select: Chemistry, Hematology, Microbiology, Blood Bank, Phlebotomy, IT Systems, Administration)
- Keyword Triggered (Text)
- Original Message (Text)
- Status (Select: 🟥 Open, 🟨 In Progress, 🟩 Resolved, 🟦 Escalated)
- Assigned To (People)
- Resolution Time (Number - minutes)
- Impact Level (Select: 1-Low, 2-Medium, 3-High, 4-Critical)
- Follow-up Required (Checkbox)
```

### 2. Staffing & Attendance Tracker 👥
```
Name: 👥 Staffing & Attendance Tracker
Properties:
- Entry ID (Title)
- Date (Date)
- Employee Name (Text)
- Department (Select: Chemistry, Hematology, Microbiology, Blood Bank, Phlebotomy)
- Shift (Select: Day, Evening, Night, Weekend)
- Status (Select: ✅ Present, ❌ Called Out, ⚠️ Late, 🏥 Medical Leave, 🏖️ Vacation, 🔄 Coverage Found, 🚨 No Coverage)
- Reason (Text)
- Coverage Status (Select: ✅ Covered, 🔄 Finding Coverage, 🚨 No Coverage, 💰 Overtime)
- Notification Sent (Checkbox)
- Pattern Flag (Checkbox)
- Occurrence Count (Number)
```

### 3. System Status Monitor 🖥️
```
Name: 🖥️ System Status Monitor
Properties:
- System Name (Title)
- Category (Select: Analyzer, IT System, Network, Tube System, LIMS, Interface, Backup System)
- Department (Select: Chemistry, Hematology, Microbiology, Blood Bank, IT, All Departments)
- Status (Select: 🟢 Online, 🟡 Warning, 🔴 Down, 🔧 Maintenance, 🔄 Restarting)
- Last Updated (Date & Time)
- Uptime % (Number)
- Issue Description (Text)
- Service Called (Checkbox)
- ETA Resolution (Date & Time)
- Impact Assessment (Text)
- Backup Available (Checkbox)
```

### 4. HR Compliance Tracker 📋
```
Name: 📋 HR Compliance Tracker
Properties:
- Record ID (Title)
- Employee Name (Text)
- Type (Select: FMLA, Medical Leave, Workers Comp, Certification, Training, Disciplinary Action, Performance Review)
- Status (Select: 🟢 Current, 🟡 Due Soon, 🔴 Overdue, 📋 In Review, ✅ Completed)
- Due Date (Date)
- Completion Date (Date)
- Days Overdue (Formula: if(prop("Due Date") < now() and prop("Status") != "✅ Completed", dateBetween(now(), prop("Due Date"), "days"), 0))
- Priority (Select: Low, Medium, High, Critical)
- Action Required (Text)
- Compliance Risk (Select: Low, Medium, High)
```

### 5. Performance Metrics Dashboard 📊
```
Name: 📊 Performance Metrics Dashboard  
Properties:
- Metric Name (Title)
- Date (Date)
- Department (Select: Chemistry, Hematology, Microbiology, Blood Bank, Overall)
- Metric Type (Select: TAT, QC Performance, Productivity, Error Rate, Specimen Quality, Staff Utilization)
- Target Value (Number)
- Actual Value (Number)
- Performance % (Formula: round((prop("Actual Value") / prop("Target Value")) * 100))
- Status (Select: 🟢 On Target, 🟡 Below Target, 🔴 Critical)
- Trend (Select: 📈 Improving, 📊 Stable, 📉 Declining)
- Action Items (Text)
```

## Phase 2: Dashboard Views

### Main Dashboard Page Layout:
```
# 🏥 Kaiser Permanente Lab Operations Command Center

## 🚨 Critical Alerts (Live Feed)
[Embed: Critical Alerts Database - Filter: Status = Open OR In Progress]

## 👥 Daily Staffing Status  
[Embed: Staffing Tracker - Filter: Date = Today, Group by Department]

## 🖥️ System Health Monitor
[Embed: System Status - Gallery view, Group by Department]

## 📊 Performance Dashboard
[Embed: Performance Metrics - Filter: Date = This Week]

## 📋 Compliance Alerts
[Embed: HR Compliance - Filter: Status = Overdue OR Due Soon]
```

## Phase 3: Power Automate Integration

### Power Automate Flow Configuration:
```
Trigger: When keyword detected in Teams
↓
Parse keyword and determine category
↓
Create record in appropriate Notion database
↓
Send notification based on priority
↓
Update dashboard views
```

### API Integration Points:
- Webhook URL for Power Automate
- Notion API for database updates  
- Teams API for notifications
- SMS API for critical alerts

## Phase 4: Automation Rules

### Template Automations to Set Up:
1. **Critical Escalation**: Auto-escalate unacknowledged critical alerts after 5 minutes
2. **Attendance Patterns**: Flag employees with 3+ absences in 30 days
3. **Compliance Reminders**: Daily check for items due within 7 days
4. **Performance Alerts**: Alert when metrics fall below target
5. **System Status Updates**: Auto-update system status from monitoring tools

## Phase 5: Testing & Go-Live

### Test Scenarios:
1. Send test Teams message with "STAT glucose critical value"
2. Post "calling out sick today" in channel
3. Send "chemistry analyzer down" alert
4. Test FMLA compliance reminder
5. Verify dashboard real-time updates

This comprehensive dashboard will provide complete visibility into your lab operations with automated alerting and tracking capabilities.
"""
    
    return setup_guide

def create_power_automate_templates():
    """Create Power Automate flow templates"""
    
    templates = {
        "critical_alert_flow": {
            "name": "Critical Lab Alert Handler",
            "trigger": "Teams message posted",
            "steps": [
                {
                    "condition": "Check if message contains critical keywords",
                    "keywords": ["STAT", "critical value", "emergency", "system down", "no coverage"]
                },
                {
                    "action": "Create Notion database entry",
                    "database": "Critical Alerts",
                    "fields": {
                        "Alert ID": "AUTO_GENERATE",
                        "Timestamp": "@{utcNow()}",
                        "Priority": "🔴 CRITICAL",
                        "Original Message": "@{triggerBody()['body']['content']}",
                        "Status": "🟥 Open"
                    }
                },
                {
                    "action": "Send Teams notification",
                    "mention": "@channel",
                    "message": "🚨 CRITICAL LAB ALERT: {keyword} detected"
                },
                {
                    "action": "Send SMS to on-call",
                    "condition": "If critical keywords detected"
                }
            ]
        },
        "staffing_alert_flow": {
            "name": "Staffing & Attendance Handler", 
            "trigger": "Teams message posted",
            "steps": [
                {
                    "condition": "Check if message contains staffing keywords",
                    "keywords": ["calling out", "sick today", "can't make it", "no coverage", "short staffed"]
                },
                {
                    "action": "Create Notion database entry",
                    "database": "Staffing & Attendance Tracker",
                    "fields": {
                        "Entry ID": "AUTO_GENERATE",
                        "Date": "@{utcNow()}",
                        "Status": "❌ Called Out",
                        "Notification Sent": True
                    }
                },
                {
                    "action": "Check for attendance patterns",
                    "condition": "If same person has 3+ recent absences"
                }
            ]
        }
    }
    
    return templates

def main():
    """Main function to create dashboard configuration"""
    
    print("🏥 Creating Kaiser Permanente Lab Monitoring Dashboard...")
    
    # Create dashboard structure
    dashboard_config = create_dashboard_structure()
    
    # Save configuration
    config_file = Path("notion_lab_dashboard_config.json")
    with open(config_file, 'w') as f:
        json.dump(dashboard_config, f, indent=2)
    
    # Generate setup guide
    setup_guide = generate_notion_setup_guide()
    guide_file = Path("Notion_Dashboard_Setup_Guide.md")
    with open(guide_file, 'w') as f:
        f.write(setup_guide)
    
    # Create Power Automate templates
    pa_templates = create_power_automate_templates()
    pa_file = Path("power_automate_templates.json")
    with open(pa_file, 'w') as f:
        json.dump(pa_templates, f, indent=2)
    
    print("✅ Dashboard configuration created!")
    print(f"📄 Configuration: {config_file}")
    print(f"📖 Setup Guide: {guide_file}")
    print(f"🔄 Power Automate Templates: {pa_file}")
    print("\n🎯 Next Steps:")
    print("1. Follow the setup guide to create Notion databases")
    print("2. Configure Power Automate flows with the templates")
    print("3. Test with sample keywords")
    print("4. Go live with real-time monitoring!")
    
    return 0

if __name__ == "__main__":
    exit(main())