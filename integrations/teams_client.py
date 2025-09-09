"""
Kaiser Permanente Lab Automation System
Microsoft Teams Integration Client

Handles automated alerts and notifications through Teams webhooks
with rich formatting and escalation support.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp
import json

from config.config_manager import TeamsConfig
from utils.audit_logger import AuditLogger


class TeamsClient:
    """
    Async client for Microsoft Teams webhook integration
    with comprehensive alert formatting and delivery.
    """
    
    def __init__(self, config: TeamsConfig):
        """
        Initialize Teams client
        
        Args:
            config: Teams configuration settings
        """
        self.config = config
        self.logger = logging.getLogger('teams_client')
        self.audit_logger = AuditLogger()
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure session is available"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
        return self.session
    
    def _get_color_theme(self, alert_type: str) -> str:
        """
        Get color theme for alert type
        
        Args:
            alert_type: Type of alert
            
        Returns:
            Hex color code
        """
        color_map = {
            "critical": "#FF0000",  # Red
            "warning": "#FFA500",   # Orange
            "info": "#0078D4",      # Blue
            "success": "#00AA00",   # Green
            "performance": "#FFD700", # Gold
            "incident": "#FF4500",  # Red-Orange
            "system": "#800080"     # Purple
        }
        return color_map.get(alert_type.lower(), "#808080")  # Default gray
    
    def _create_adaptive_card(
        self, 
        title: str, 
        message: str, 
        alert_type: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create adaptive card for Teams message
        
        Args:
            title: Alert title
            message: Alert message
            alert_type: Type of alert
            details: Additional details to include
            
        Returns:
            Adaptive card payload
        """
        # Get appropriate color and emoji
        color = self._get_color_theme(alert_type)
        emoji_map = {
            "critical": "🚨",
            "warning": "⚠️",
            "info": "ℹ️",
            "success": "✅",
            "performance": "📊",
            "incident": "🔴",
            "system": "🔧"
        }
        emoji = emoji_map.get(alert_type.lower(), "📢")
        
        # Base card structure
        card = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.3",
                        "body": [
                            {
                                "type": "Container",
                                "style": "emphasis",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": f"{emoji} {title}",
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "color": "Attention" if alert_type in ["critical", "warning"] else "Default"
                                    }
                                ]
                            },
                            {
                                "type": "TextBlock",
                                "text": message,
                                "wrap": True,
                                "spacing": "Medium"
                            }
                        ]
                    }
                }
            ]
        }
        
        # Add timestamp
        card["attachments"][0]["content"]["body"].append({
            "type": "TextBlock",
            "text": f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "size": "Small",
            "color": "Accent",
            "spacing": "Medium"
        })
        
        # Add details if provided
        if details:
            facts = []
            for key, value in details.items():
                facts.append({
                    "title": key.replace("_", " ").title(),
                    "value": str(value)
                })
            
            if facts:
                card["attachments"][0]["content"]["body"].append({
                    "type": "FactSet",
                    "facts": facts,
                    "spacing": "Medium"
                })
        
        # Add action buttons for critical alerts
        if alert_type == "critical":
            card["attachments"][0]["content"]["actions"] = [
                {
                    "type": "Action.OpenUrl",
                    "title": "View Dashboard",
                    "url": "https://app.powerbi.com"  # Replace with actual dashboard URL
                },
                {
                    "type": "Action.OpenUrl",
                    "title": "View Notion",
                    "url": "https://notion.so"  # Replace with actual Notion URL
                }
            ]
        
        return card
    
    async def send_alert(
        self, 
        title: str, 
        message: str, 
        alert_type: str = "info",
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send alert to Teams channel
        
        Args:
            title: Alert title
            message: Alert message
            alert_type: Type of alert (critical, warning, info, success, etc.)
            details: Additional details to include
            
        Returns:
            Success status
        """
        try:
            session = await self._ensure_session()
            
            # Create adaptive card
            card_payload = self._create_adaptive_card(title, message, alert_type, details)
            
            # Send to Teams webhook
            async with session.post(
                self.config.webhook_url,
                json=card_payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    self.logger.info(f"Teams alert sent successfully: {title}")
                    
                    # Log to audit trail
                    self.audit_logger.log_alert_sent({
                        "service": "teams",
                        "title": title,
                        "alert_type": alert_type,
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Teams alert failed: Status {response.status}, Response: {error_text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Failed to send Teams alert: {e}")
            return False
    
    async def send_performance_alert(
        self, 
        staff_member: str, 
        issues: List[str],
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send performance-specific alert
        
        Args:
            staff_member: Staff member name
            issues: List of performance issues
            metrics: Performance metrics data
            
        Returns:
            Success status
        """
        title = f"Performance Alert: {staff_member}"
        message = f"Performance issues detected for {staff_member}:\n\n" + "\n".join(f"• {issue}" for issue in issues)
        
        details = {"Staff Member": staff_member}
        if metrics:
            details.update({
                "Performance Score": metrics.get("performance_score", "N/A"),
                "Samples Processed": metrics.get("samples_processed", "N/A"),
                "Error Count": metrics.get("error_count", "N/A"),
                "TAT Target Met": "Yes" if metrics.get("tat_target_met") else "No"
            })
        
        return await self.send_alert(title, message, "performance", details)
    
    async def send_incident_alert(
        self, 
        incident_data: Dict[str, Any],
        is_critical: bool = False
    ) -> bool:
        """
        Send incident alert
        
        Args:
            incident_data: Incident information
            is_critical: Whether this is a critical incident
            
        Returns:
            Success status
        """
        incident_id = incident_data.get("incident_id", "Unknown")
        severity = incident_data.get("severity", "Unknown")
        
        title = f"{'🚨 CRITICAL' if is_critical else '⚠️'} Incident Alert: {incident_id}"
        message = f"New incident reported:\n\n**Description:** {incident_data.get('description', 'No description provided')}"
        
        details = {
            "Incident ID": incident_id,
            "Severity": severity,
            "Type": incident_data.get("incident_type", "Unknown"),
            "Staff Member": incident_data.get("staff_member", "Unknown"),
            "Impact": incident_data.get("impact", "Unknown")
        }
        
        alert_type = "critical" if is_critical else "incident"
        return await self.send_alert(title, message, alert_type, details)
    
    async def send_system_status(
        self, 
        system_name: str, 
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send system status update
        
        Args:
            system_name: Name of the system
            status: Current status
            details: Additional system details
            
        Returns:
            Success status
        """
        status_emoji = {
            "online": "✅",
            "offline": "🔴",
            "maintenance": "🔧",
            "warning": "⚠️",
            "error": "❌"
        }
        
        emoji = status_emoji.get(status.lower(), "📊")
        title = f"{emoji} System Status: {system_name}"
        message = f"System **{system_name}** is currently **{status.upper()}**"
        
        alert_type = "critical" if status.lower() in ["offline", "error"] else "system"
        
        return await self.send_alert(title, message, alert_type, details)
    
    async def send_daily_summary(
        self, 
        summary_data: Dict[str, Any]
    ) -> bool:
        """
        Send daily performance summary
        
        Args:
            summary_data: Daily summary statistics
            
        Returns:
            Success status
        """
        title = "📊 Daily Lab Performance Summary"
        
        # Format summary message
        message = "Here's today's lab performance summary:"
        
        details = {
            "Total Samples": summary_data.get("total_samples", 0),
            "Error Rate": f"{summary_data.get('error_rate', 0):.1f}%",
            "TAT Compliance": f"{summary_data.get('tat_compliance', 0):.1f}%",
            "Average Performance": f"{summary_data.get('avg_performance', 0):.1f}",
            "Open Incidents": summary_data.get("open_incidents", 0),
            "Staff on Duty": summary_data.get("staff_count", 0)
        }
        
        # Determine alert type based on performance
        tat_compliance = summary_data.get("tat_compliance", 0)
        error_rate = summary_data.get("error_rate", 0)
        
        if tat_compliance < 75 or error_rate > 5:
            alert_type = "warning"
        elif tat_compliance > 90 and error_rate < 2:
            alert_type = "success"
        else:
            alert_type = "info"
        
        return await self.send_alert(title, message, alert_type, details)
    
    async def send_equipment_alert(
        self, 
        equipment_name: str, 
        alert_message: str,
        severity: str = "warning"
    ) -> bool:
        """
        Send equipment-specific alert
        
        Args:
            equipment_name: Name of equipment
            alert_message: Alert message
            severity: Alert severity
            
        Returns:
            Success status
        """
        title = f"🔧 Equipment Alert: {equipment_name}"
        
        details = {
            "Equipment": equipment_name,
            "Severity": severity.upper(),
            "Time": datetime.now().strftime("%H:%M:%S")
        }
        
        alert_type = "critical" if severity.lower() == "critical" else "warning"
        
        return await self.send_alert(title, alert_message, alert_type, details)
    
    async def send_shift_change_summary(
        self, 
        outgoing_shift: str,
        incoming_shift: str,
        handoff_data: Dict[str, Any]
    ) -> bool:
        """
        Send shift change summary
        
        Args:
            outgoing_shift: Name of outgoing shift
            incoming_shift: Name of incoming shift
            handoff_data: Shift handoff information
            
        Returns:
            Success status
        """
        title = f"🔄 Shift Change: {outgoing_shift} → {incoming_shift}"
        message = f"Shift handoff from **{outgoing_shift}** to **{incoming_shift}**"
        
        details = {
            "Outgoing Shift": outgoing_shift,
            "Incoming Shift": incoming_shift,
            "Samples Completed": handoff_data.get("samples_completed", 0),
            "Pending Issues": handoff_data.get("pending_issues", 0),
            "Equipment Status": handoff_data.get("equipment_status", "Normal"),
            "Special Notes": handoff_data.get("notes", "None")
        }
        
        return await self.send_alert(title, message, "info", details)
    
    async def test_connection(self) -> bool:
        """
        Test Teams webhook connection
        
        Returns:
            Connection status
        """
        try:
            test_title = "🧪 Connection Test"
            test_message = "This is a test message to verify Teams integration is working correctly."
            
            success = await self.send_alert(test_title, test_message, "info", {
                "Test Time": datetime.now().isoformat(),
                "System": "Lab Automation"
            })
            
            if success:
                self.logger.info("Teams connection test successful")
            else:
                self.logger.error("Teams connection test failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Teams connection test error: {e}")
            return False
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()

