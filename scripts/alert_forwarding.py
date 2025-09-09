#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Alert Forwarding Implementation

Processes events and forwards appropriate alerts to Teams based on
comprehensive keyword triggers and thresholds.
"""

import os
import re
import asyncio
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import requests
from dotenv import load_dotenv

from comprehensive_alert_keywords import (
    ALERT_KEYWORDS, TRIGGER_PATTERNS, SCHEDULED_TRIGGERS,
    ESCALATION_TRIGGERS, METRIC_THRESHOLDS, COMBINED_TRIGGERS
)

load_dotenv()


class AlertForwarder:
    """
    Intelligent alert forwarding system that routes alerts
    based on keywords, thresholds, and patterns.
    """
    
    def __init__(self):
        self.webhook_url = os.getenv("TEAMS_WEBHOOK_URL")
        self.keywords = ALERT_KEYWORDS
        self.patterns = TRIGGER_PATTERNS
        self.thresholds = METRIC_THRESHOLDS
        
    def check_triggers(self, message: str, metrics: Dict = None) -> Tuple[bool, str, str]:
        """
        Check if message or metrics trigger an alert
        Returns: (should_forward, priority, category)
        """
        message_lower = message.lower()
        
        # Check immediate alert patterns - highest priority
        for pattern in self.patterns["immediate_alert"]:
            if pattern.lower() in message_lower:
                return True, "high", "critical"
        
        # Check escalation patterns
        for pattern in self.patterns["escalation_required"]:
            if pattern.lower() in message_lower:
                return True, "high", "escalation"
        
        # Check keyword categories
        for category, config in self.keywords.items():
            for keyword in config["keywords"]:
                if keyword.lower() in message_lower:
                    # Check if metrics exceed thresholds
                    if metrics and self.check_thresholds(metrics, config.get("thresholds", {})):
                        return True, config["priority"], category
                    # Forward if keyword alone for high priority
                    elif config["priority"] == "high":
                        return True, config["priority"], category
        
        # Check for trend alerts
        for pattern in self.patterns["trend_alerts"]:
            if pattern.lower() in message_lower:
                return True, "medium", "trend"
        
        return False, None, None
    
    def check_thresholds(self, metrics: Dict, thresholds: Dict) -> bool:
        """Check if metrics exceed defined thresholds"""
        for metric, threshold in thresholds.items():
            if metric in metrics:
                value = metrics[metric]
                if ">" in threshold:
                    limit = float(threshold.replace(">", "").strip())
                    if value > limit:
                        return True
                elif "<" in threshold:
                    limit = float(threshold.replace("<", "").strip())
                    if value < limit:
                        return True
                elif threshold == "any":
                    return True
        return False
    
    def determine_escalation_level(self, message: str, category: str) -> str:
        """Determine who should be notified based on escalation matrix"""
        message_lower = message.lower()
        
        for level, triggers in ESCALATION_TRIGGERS.items():
            for trigger in triggers:
                if trigger.lower() in message_lower:
                    return level
        
        # Default escalation based on category
        high_escalation_categories = ["critical", "incident", "regulatory", "patient"]
        if category in high_escalation_categories:
            return "manager_notification"
        
        return "immediate_supervisor"
    
    def check_combined_conditions(self, active_conditions: List[str]) -> Optional[Dict]:
        """Check for combined trigger conditions that require special handling"""
        for scenario, config in COMBINED_TRIGGERS.items():
            required_conditions = config["conditions"]
            if all(cond in active_conditions for cond in required_conditions):
                return {
                    "scenario": scenario,
                    "action": config["action"],
                    "priority": "critical"
                }
        return None
    
    def format_teams_message(self, title: str, content: str, category: str, 
                           priority: str, metrics: Dict = None, 
                           escalation_level: str = None) -> Dict:
        """Format message for Teams webhook with rich content"""
        
        color = self.keywords.get(category, {}).get("color", "0078D4")
        
        # Priority icons
        icons = {
            "high": "🚨",
            "medium": "⚠️",
            "low": "ℹ️",
            "critical": "🆘"
        }
        
        # Build facts list
        facts = [
            {"name": "Priority", "value": priority.upper()},
            {"name": "Category", "value": category.replace("_", " ").title()},
            {"name": "Time", "value": datetime.now().strftime("%H:%M:%S")},
            {"name": "Source", "value": "Lab Automation System"}
        ]
        
        if escalation_level:
            facts.append({"name": "Escalation", "value": escalation_level.replace("_", " ").title()})
        
        if metrics:
            # Add key metrics to facts
            for key, value in list(metrics.items())[:3]:  # Show top 3 metrics
                facts.append({"name": key.replace("_", " ").title(), "value": str(value)})
        
        # Build actions based on category
        actions = [{
            "@type": "OpenUri",
            "name": "View Dashboard",
            "targets": [{
                "os": "default",
                "uri": "https://app.powerbi.com/groups/3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1"
            }]
        }]
        
        # Add category-specific actions
        if category in ["incident", "critical"]:
            actions.append({
                "@type": "OpenUri",
                "name": "Open Incident Tracker",
                "targets": [{
                    "os": "default",
                    "uri": "https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2"
                }]
            })
        elif category == "performance":
            actions.append({
                "@type": "OpenUri",
                "name": "View Performance",
                "targets": [{
                    "os": "default",
                    "uri": "https://www.notion.so/c1500b1816b14018beabe2b826ccafe9"
                }]
            })
        
        message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "summary": title,
            "themeColor": color,
            "title": f"{icons.get(priority, 'ℹ️')} {title}",
            "sections": [{
                "activityTitle": f"Lab Alert - {category.upper()}",
                "activitySubtitle": f"Kaiser Permanente Laboratory - Largo, MD",
                "text": content,
                "facts": facts
            }],
            "potentialAction": actions
        }
        
        return message
    
    def forward_to_teams(self, title: str, content: str, category: str, 
                        priority: str, metrics: Dict = None) -> bool:
        """Forward alert to Teams with appropriate formatting"""
        
        try:
            # Determine escalation level
            escalation_level = self.determine_escalation_level(content, category)
            
            # Format message
            message = self.format_teams_message(
                title, content, category, priority, metrics, escalation_level
            )
            
            # Send to Teams
            response = requests.post(self.webhook_url, json=message)
            
            if response.status_code == 200:
                print(f"✅ Alert forwarded to Teams: {category}/{priority}")
                return True
            else:
                print(f"❌ Failed to forward alert: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"💥 Error forwarding alert: {e}")
            return False


class ScheduledAlertManager:
    """
    Manages scheduled alerts based on time triggers
    """
    
    def __init__(self, alert_forwarder: AlertForwarder):
        self.forwarder = alert_forwarder
        self.schedules = SCHEDULED_TRIGGERS
        
    async def check_scheduled_alerts(self):
        """Check and send scheduled alerts based on current time"""
        current_time = datetime.now().strftime("%H:%M")
        current_day_time = f"{datetime.now().strftime('%A')} {current_time}"
        
        for schedule_type, config in self.schedules.items():
            if "times" in config and current_time in config["times"]:
                await self.send_scheduled_alert(schedule_type, config["dashboards"])
            elif "day_time" in config and config["day_time"] in current_day_time:
                await self.send_scheduled_alert(schedule_type, config["dashboards"])
    
    async def send_scheduled_alert(self, schedule_type: str, dashboards: List[str]):
        """Send scheduled alert for specified dashboards"""
        
        title = f"Scheduled {schedule_type.replace('_', ' ').title()}"
        content = f"Time for {schedule_type.replace('_', ' ')}. Please review the following dashboards:\n\n"
        
        for dashboard in dashboards:
            content += f"• {dashboard.replace('_', ' ').title()}\n"
        
        self.forwarder.forward_to_teams(
            title,
            content,
            "operations",
            "low"
        )


def process_lab_event(event_text: str, metrics: Dict = None):
    """Process a lab event and forward if triggered"""
    
    forwarder = AlertForwarder()
    should_forward, priority, category = forwarder.check_triggers(event_text, metrics)
    
    if should_forward:
        # Enhance title based on category
        title_map = {
            "critical": "CRITICAL ALERT",
            "incident": "Incident Report",
            "performance": "Performance Alert",
            "quality": "Quality Issue",
            "staffing": "Staffing Update",
            "equipment": "Equipment Alert",
            "patient": "Patient Care Alert",
            "regulatory": "Compliance Alert",
            "supplies": "Supply Alert",
            "operations": "Operations Update",
            "trend": "Trend Alert",
            "escalation": "Escalation Required"
        }
        
        title = title_map.get(category, "Lab Alert")
        
        forwarder.forward_to_teams(
            title,
            event_text,
            category,
            priority,
            metrics
        )
        
        return True
    else:
        print("ℹ️ No trigger conditions met")
        return False


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Kaiser Permanente Lab Alert System")
    print("=" * 60)
    
    # Test various real-world scenarios
    test_scenarios = [
        # Critical scenarios
        ("All chemistry analyzers are offline - urgent maintenance required", None),
        ("Critical value glucose 25 mg/dL not called within 5 minutes", {"callback_time": 6}),
        ("Multiple QC failures on Sysmex XN-2000 - testing stopped", {"qc_failures": 3}),
        
        # Performance issues
        ("Current TAT for routine CBC is 75 minutes", {"TAT": 75, "test_type": "routine"}),
        ("Chemistry bench has 150 pending samples", {"pending_samples": 150, "bench": "chemistry"}),
        
        # Staffing issues
        ("Three technologists called out for evening shift", {"callouts": 3, "shift": "evening"}),
        ("Tech on break for 90 minutes without coverage", {"break_duration": 90}),
        
        # Quality issues
        ("Contamination detected in coagulation specimens from draw station 3", None),
        ("CAP proficiency testing failure for PT/INR", {"test": "PT", "result": "fail"}),
        
        # Equipment issues
        ("Cobas analyzer showing calibration error - unable to run CMP", None),
        ("Blood bank Echo down - using manual crossmatch", {"downtime": 45}),
        
        # Regulatory
        ("CAP inspection deficiency noted for temperature logs", None),
        ("CLIA compliance audit scheduled for next week", None),
        
        # Patient impact
        ("STAT troponin delayed 55 minutes for ED patient", {"TAT": 55, "priority": "STAT"}),
        ("Wrong blood type reported - immediate correction issued", None),
        
        # Supplies
        ("Urinalysis test strips expiring tomorrow - 2 boxes remaining", {"days_to_expiry": 1}),
        ("Chemistry reagent for glucose at 15% of par level", {"stock_level": 15}),
        
        # Daily operations
        ("Daily performance summary ready for review", None),
        ("Shift change report - all stations covered", None)
    ]
    
    print("\n📊 Running test scenarios:\n")
    
    forwarded = 0
    for i, (event, metrics) in enumerate(test_scenarios, 1):
        print(f"{i}. Testing: {event[:60]}...")
        if process_lab_event(event, metrics):
            forwarded += 1
        print()
    
    print(f"\n📈 Results: {forwarded}/{len(test_scenarios)} alerts would be forwarded")
    print("\n✅ Alert system test complete!")

