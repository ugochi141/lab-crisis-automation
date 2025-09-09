#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Dashboard-Specific Alert Forwarding

Routes alerts to appropriate Notion dashboards and Power BI visualizations
based on keyword matching and metric thresholds.
"""

import os
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

from comprehensive_alert_keywords import (
    DASHBOARD_KEYWORD_TRIGGERS, DEPARTMENT_TRIGGERS,
    METRIC_THRESHOLDS, SCHEDULED_TRIGGERS
)
from config.config_manager import ConfigManager
from integrations.notion_client import NotionClient
from integrations.teams_client import TeamsClient
from integrations.working_powerbi_client import create_working_powerbi_client
from utils.audit_logger import AuditLogger


class DashboardForwarder:
    """
    Intelligent dashboard routing system that forwards alerts
    to the appropriate Notion databases and Power BI dashboards.
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.notion_client = self._init_notion_client()
        self.powerbi_client = create_working_powerbi_client()
        self.teams_client = self._init_teams_client()
        self.triggers = DASHBOARD_KEYWORD_TRIGGERS
        self.departments = DEPARTMENT_TRIGGERS
        self.logger = logging.getLogger('dashboard_forwarder')
        self.audit_logger = AuditLogger()
        
    def _init_notion_client(self) -> NotionClient:
        """Initialize Notion client with configuration"""
        notion_config = self.config_manager.get_notion_config()
        return NotionClient(notion_config)
    
    def _init_teams_client(self) -> TeamsClient:
        """Initialize Teams client with configuration"""
        teams_config = self.config_manager.get_teams_config()
        return TeamsClient(teams_config)
    
    async def route_to_dashboard(self, message: str, metrics: dict = None) -> List[Dict]:
        """
        Route alerts to appropriate dashboards based on keywords
        
        Args:
            message: Alert message content
            metrics: Associated metrics
            
        Returns:
            List of matched dashboards with routing information
        """
        matched_dashboards = []
        message_lower = message.lower()
        
        # Check dashboard-specific keywords
        for dashboard, config in self.triggers.items():
            for keyword in config.get("keywords", []):
                if keyword in message_lower:
                    priority = self.determine_priority(dashboard, message, metrics)
                    
                    dashboard_info = {
                        "dashboard": dashboard,
                        "database_id": config.get("database_id") or config.get("database_ids", [None])[0],
                        "database_ids": config.get("database_ids", []),
                        "priority": priority,
                        "auto_triggers": config.get("auto_triggers", {}),
                        "matched_keyword": keyword
                    }
                    
                    matched_dashboards.append(dashboard_info)
                    break
        
        # Check department-specific triggers
        for dept, config in self.departments.items():
            for keyword in config["keywords"]:
                if keyword in message_lower:
                    matched_dashboards.append({
                        "dashboard": f"department_{dept}",
                        "department": dept,
                        "instruments": config["instruments"],
                        "priority": self.determine_priority(dept, message, metrics)
                    })
                    break
        
        # Log routing decision
        self.audit_logger.log_system_event(
            "ALERT_ROUTING",
            f"Routed alert to {len(matched_dashboards)} dashboards",
            {
                "message_preview": message[:100],
                "matched_dashboards": [d["dashboard"] for d in matched_dashboards],
                "has_metrics": metrics is not None
            }
        )
        
        return matched_dashboards
    
    def determine_priority(self, dashboard: str, message: str, metrics: dict = None) -> str:
        """
        Determine alert priority based on dashboard type, content, and metrics
        
        Args:
            dashboard: Dashboard identifier
            message: Alert message
            metrics: Associated metrics
            
        Returns:
            Priority level (high, medium, low)
        """
        message_lower = message.lower()
        
        # High priority dashboards
        high_priority_dashboards = [
            "critical_values", "active_alerts", "quality_error",
            "patient", "incident", "regulatory"
        ]
        
        # Urgent keywords that override dashboard priority
        urgent_keywords = [
            "critical", "urgent", "stat", "emergency", "immediate",
            "patient safety", "wrong blood", "contamination"
        ]
        
        # Check for urgent keywords first
        for keyword in urgent_keywords:
            if keyword in message_lower:
                return "high"
        
        # Check if high priority dashboard
        if dashboard in high_priority_dashboards:
            return "high"
        
        # Check metrics against thresholds
        if metrics:
            priority = self._check_metric_priority(dashboard, metrics)
            if priority:
                return priority
        
        # Department-specific priorities
        critical_departments = ["blood_bank", "molecular", "microbiology"]
        if dashboard.startswith("department_") and any(dept in dashboard for dept in critical_departments):
            return "medium"
        
        # Default priorities by dashboard type
        priority_map = {
            "staff_performance": "low" if not metrics else "medium",
            "station_monitor": "medium",
            "break_attendance": "low",
            "inventory": "low",
            "scheduling": "low",
            "communication": "low",
            "lab_performance": "medium",
            "it_projects": "low"
        }
        
        return priority_map.get(dashboard, "low")
    
    def _check_metric_priority(self, dashboard: str, metrics: dict) -> Optional[str]:
        """Check metrics against thresholds to determine priority"""
        
        # Staff performance thresholds
        if dashboard == "staff_performance" and "score" in metrics:
            if metrics["score"] < 60:
                return "high"
            elif metrics["score"] < 70:
                return "medium"
        
        # TAT thresholds
        if "TAT" in metrics:
            tat_thresholds = METRIC_THRESHOLDS["tat_critical"]
            test_type = metrics.get("test_type", "routine")
            threshold = tat_thresholds.get(test_type, 60)
            
            if metrics["TAT"] > threshold * 1.5:
                return "high"
            elif metrics["TAT"] > threshold:
                return "medium"
        
        # Error rate thresholds
        if "error_rate" in metrics:
            error_thresholds = METRIC_THRESHOLDS["error_rates"]
            if metrics["error_rate"] > error_thresholds["critical"]:
                return "high"
            elif metrics["error_rate"] > error_thresholds["warning"]:
                return "medium"
        
        # QC compliance thresholds
        if dashboard == "quality_error" and "QC_compliance" in metrics:
            if metrics["QC_compliance"] < METRIC_THRESHOLDS["qc_compliance"]["minimum"]:
                return "high"
        
        return None
    
    async def forward_to_notion(self, dashboard_info: Dict, message: str, metrics: Dict = None):
        """
        Create an entry in the appropriate Notion database
        
        Args:
            dashboard_info: Dashboard routing information
            message: Alert message
            metrics: Associated metrics
        """
        try:
            database_id = dashboard_info.get("database_id")
            if not database_id:
                self.logger.warning(f"No database ID for dashboard: {dashboard_info['dashboard']}")
                return
            
            # Prepare properties based on dashboard type
            properties = self._prepare_notion_properties(dashboard_info, message, metrics)
            
            # Create page in Notion
            result = await self.notion_client.create_page(
                database_id=database_id,
                properties=properties
            )
            
            if result:
                self.logger.info(f"Alert logged to Notion dashboard: {dashboard_info['dashboard']}")
            
        except Exception as e:
            self.logger.error(f"Failed to forward to Notion: {e}")
    
    def _prepare_notion_properties(self, dashboard_info: Dict, message: str, metrics: Dict = None) -> Dict:
        """Prepare properties for Notion page creation based on dashboard type"""
        
        dashboard = dashboard_info["dashboard"]
        timestamp = datetime.now().isoformat()
        
        # Base properties common to most dashboards
        properties = {
            "Title": {"title": [{"text": {"content": message[:100]}}]},
            "Description": {"rich_text": [{"text": {"content": message}}]},
            "Timestamp": {"date": {"start": timestamp}},
            "Priority": {"select": {"name": dashboard_info["priority"].title()}},
            "Status": {"select": {"name": "New"}}
        }
        
        # Dashboard-specific properties
        if dashboard == "staff_performance" and metrics:
            properties.update({
                "Staff Member": {"rich_text": [{"text": {"content": metrics.get("staff_name", "Unknown")}}]},
                "Performance Score": {"number": metrics.get("score", 0)},
                "Shift": {"select": {"name": metrics.get("shift", "Day")}}
            })
        
        elif dashboard == "quality_error" and metrics:
            properties.update({
                "Error Type": {"select": {"name": metrics.get("error_type", "Other")}},
                "Department": {"select": {"name": metrics.get("department", "General")}},
                "Severity": {"select": {"name": dashboard_info["priority"].title()}}
            })
        
        elif dashboard == "active_alerts":
            properties.update({
                "Alert Type": {"select": {"name": dashboard_info.get("matched_keyword", "General")}},
                "Requires Action": {"checkbox": dashboard_info["priority"] == "high"}
            })
        
        elif dashboard == "lab_performance" and metrics:
            properties.update({
                "TAT Minutes": {"number": metrics.get("TAT", 0)},
                "Volume": {"number": metrics.get("volume", 0)},
                "Compliance Rate": {"number": metrics.get("compliance_rate", 0)}
            })
        
        return properties
    
    async def forward_to_powerbi(self, dashboard_info: Dict, metrics: Dict):
        """
        Push metrics to appropriate Power BI dataset
        
        Args:
            dashboard_info: Dashboard routing information
            metrics: Metrics to push
        """
        try:
            dashboard = dashboard_info["dashboard"]
            
            # Map dashboard to Power BI dataset
            if dashboard in ["lab_performance", "staff_performance", "quality_error"]:
                # Performance monitoring dataset
                data = {
                    "Timestamp": datetime.utcnow().isoformat() + "Z",
                    "Department": metrics.get("department", "General"),
                    "ErrorCount": metrics.get("error_count", 0),
                    "PerformanceScore": metrics.get("performance_score", 85)
                }
                
                await self.powerbi_client.push_performance_update(data)
                
            elif dashboard in ["active_alerts", "critical_values"]:
                # Status update for alerts
                await self.powerbi_client.push_status_update(
                    dashboard_info["priority"],
                    message=dashboard_info.get("matched_keyword", "Alert")
                )
            
            self.logger.info(f"Metrics pushed to Power BI for dashboard: {dashboard}")
            
        except Exception as e:
            self.logger.error(f"Failed to push to Power BI: {e}")
    
    async def send_dashboard_notification(self, dashboard_info: Dict, message: str):
        """
        Send Teams notification about dashboard update
        
        Args:
            dashboard_info: Dashboard routing information  
            message: Alert message
        """
        try:
            dashboard_name = dashboard_info["dashboard"].replace("_", " ").title()
            priority_emoji = {
                "high": "🚨",
                "medium": "⚠️",
                "low": "ℹ️"
            }
            
            title = f"{priority_emoji[dashboard_info['priority']]} {dashboard_name} Update"
            
            # Build notification content
            content = f"**Alert routed to {dashboard_name}**\n\n"
            content += f"**Message:** {message}\n\n"
            
            if dashboard_info.get("database_id"):
                content += f"**Notion Dashboard:** View in Notion\n"
            
            content += f"**Priority:** {dashboard_info['priority'].upper()}\n"
            content += f"**Time:** {datetime.now().strftime('%H:%M:%S')}\n"
            
            # Add dashboard-specific links
            dashboard_links = {
                "lab_performance": "https://www.notion.so/c1500b1816b14018beabe2b826ccafe9",
                "quality_error": "https://www.notion.so/264d222751b3816baabcf476e43682ab",
                "staff_performance": "https://www.notion.so/264d222751b381ee84baeba1415e8c32",
                "active_alerts": "https://www.notion.so/264d222751b381f1963ef16d40c5b8ff"
            }
            
            if dashboard_info["dashboard"] in dashboard_links:
                content += f"\n[Open Dashboard]({dashboard_links[dashboard_info['dashboard']]})"
            
            await self.teams_client.send_alert(
                title,
                content,
                dashboard_info["priority"],
                {
                    "Dashboard": dashboard_name,
                    "Keyword Match": dashboard_info.get("matched_keyword", "N/A")
                }
            )
            
        except Exception as e:
            self.logger.error(f"Failed to send Teams notification: {e}")
    
    async def process_alert(self, message: str, metrics: Dict = None):
        """
        Complete alert processing workflow
        
        Args:
            message: Alert message
            metrics: Associated metrics
        """
        try:
            # Route to dashboards
            matched_dashboards = await self.route_to_dashboard(message, metrics)
            
            if not matched_dashboards:
                self.logger.info("No dashboard matches found for alert")
                return
            
            # Process each matched dashboard
            for dashboard_info in matched_dashboards:
                # Log to Notion
                await self.forward_to_notion(dashboard_info, message, metrics)
                
                # Push metrics to Power BI if available
                if metrics:
                    await self.forward_to_powerbi(dashboard_info, metrics)
                
                # Send Teams notification for high priority
                if dashboard_info["priority"] in ["high", "medium"]:
                    await self.send_dashboard_notification(dashboard_info, message)
            
            self.logger.info(f"Alert processed and routed to {len(matched_dashboards)} dashboards")
            
        except Exception as e:
            self.logger.error(f"Alert processing failed: {e}")


# Example usage
async def main():
    """Test dashboard forwarding with various scenarios"""
    
    print("🎯 Testing Dashboard-Specific Alert Forwarding")
    print("=" * 60)
    
    forwarder = DashboardForwarder()
    
    # Test scenarios for different dashboards
    test_scenarios = [
        # Staff Performance
        ("Tech John Smith performance score dropped to 65%", {
            "staff_name": "John Smith",
            "score": 65,
            "shift": "Day",
            "department": "Chemistry"
        }),
        
        # Quality Error  
        ("QC failure on Cobas chemistry analyzer - glucose out of range", {
            "error_type": "QC Failure",
            "instrument": "Cobas",
            "test": "Glucose",
            "department": "Chemistry",
            "error_count": 1
        }),
        
        # Station Monitor
        ("Hematology station 2 unmanned for 20 minutes", {
            "station": "Hematology-2",
            "unmanned_duration": 20,
            "pending_samples": 15
        }),
        
        # Break & Attendance
        ("Tech late arrival - 3rd occurrence this month", {
            "staff_name": "Jane Doe",
            "occurrence_type": "Tardy",
            "occurrence_count": 3
        }),
        
        # Critical Values
        ("Critical value potassium 6.8 requires immediate callback", {
            "test": "Potassium",
            "value": 6.8,
            "patient_id": "12345",
            "priority": "STAT"
        })
    ]
    
    print("\n📊 Processing test alerts:\n")
    
    for message, metrics in test_scenarios:
        print(f"📨 Processing: {message}")
        await forwarder.process_alert(message, metrics)
        print("✅ Processed\n")
        await asyncio.sleep(1)  # Small delay between tests
    
    print("✅ Dashboard forwarding test complete!")


if __name__ == "__main__":
    asyncio.run(main())
