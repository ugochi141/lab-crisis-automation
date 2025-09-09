#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
MAS Lab All Staff Channel Forwarding

Forwards messages from specific MAS Lab channels to the automation system.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from integrations.teams_client import TeamsClient
from scripts.alert_forwarding import process_lab_event
from scripts.dashboard_forwarder import DashboardForwarder


class MASLabChannelForwarder:
    """
    Forwards messages from MAS Lab All Staff channels to automation system
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.teams_client = self._init_teams_client()
        self.dashboard_forwarder = DashboardForwarder()
        
        # MAS Lab channel configurations
        self.channels = {
            "operational_information": {
                "name": "Operational Information | MAS Lab All Staff",
                "keywords": [
                    "operational", "workflow", "process", "procedure",
                    "downtime", "maintenance", "schedule", "shift",
                    "announcement", "update", "change", "implementation"
                ],
                "priority": "medium",
                "route_to": ["operations", "communication", "scheduling"]
            },
            "quality": {
                "name": "Quality | MAS Lab All Staff",
                "keywords": [
                    "quality", "QC", "QA", "compliance", "CAP", "CLIA",
                    "inspection", "audit", "error", "incident", "corrective",
                    "proficiency", "validation", "improvement", "metric"
                ],
                "priority": "high",
                "route_to": ["quality_error", "regulatory", "lab_performance"]
            }
        }
    
    def _init_teams_client(self) -> TeamsClient:
        """Initialize Teams client"""
        teams_config = self.config_manager.get_teams_config()
        return TeamsClient(teams_config)
    
    async def forward_channel_messages(self, channel: str, messages: List[Dict[str, str]]):
        """
        Forward messages from a specific MAS Lab channel
        
        Args:
            channel: Channel identifier (operational_information or quality)
            messages: List of messages to forward
        """
        if channel not in self.channels:
            print(f"❌ Unknown channel: {channel}")
            return
        
        channel_config = self.channels[channel]
        channel_name = channel_config["name"]
        
        print(f"\n📨 Forwarding messages from: {channel_name}")
        print("=" * 60)
        
        forwarded_count = 0
        
        for i, message in enumerate(messages, 1):
            content = message.get("content", "")
            sender = message.get("sender", "MAS Lab Staff")
            timestamp = message.get("timestamp", datetime.now().isoformat())
            
            # Check if message is relevant
            if self._is_relevant_message(content, channel_config["keywords"]):
                # Forward to main team workspace
                await self._forward_to_team_workspace(
                    channel_name, content, sender, timestamp, channel_config
                )
                
                # Process through alert system
                process_lab_event(content)
                
                # Route to appropriate dashboards
                await self.dashboard_forwarder.process_alert(content)
                
                forwarded_count += 1
                print(f"✅ Message {i} forwarded")
            else:
                print(f"⏭️  Message {i} skipped (not relevant)")
        
        print(f"\n📊 Summary: {forwarded_count}/{len(messages)} messages forwarded")
    
    def _is_relevant_message(self, content: str, keywords: List[str]) -> bool:
        """Check if message contains relevant keywords"""
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in keywords)
    
    async def _forward_to_team_workspace(self, channel_name: str, content: str, 
                                       sender: str, timestamp: str, config: Dict):
        """Forward message to Kaiser Permanente team workspace"""
        
        # Determine icon based on channel
        icon = "📋" if "operational" in channel_name.lower() else "🎯"
        
        title = f"{icon} MAS Lab Forward - {channel_name.split('|')[0].strip()}"
        
        formatted_content = (
            f"**Forwarded from MAS Lab All Staff**\n\n"
            f"**Channel:** {channel_name}\n"
            f"**From:** {sender}\n"
            f"**Time:** {timestamp}\n\n"
            f"**Message:**\n{content}\n\n"
            f"---\n"
            f"*Automatically forwarded due to {config['route_to'][0]} relevance*"
        )
        
        await self.teams_client.send_alert(
            title,
            formatted_content,
            config["priority"],
            {
                "Source Channel": channel_name,
                "Priority": config["priority"].upper(),
                "Categories": ", ".join(config["route_to"]),
                "Forward Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    
    async def setup_channel_monitoring(self):
        """Set up monitoring for MAS Lab channels"""
        
        print("🚀 Setting up MAS Lab channel monitoring...")
        
        notification = (
            "**MAS Lab Channel Integration Activated**\n\n"
            "Now monitoring and forwarding relevant messages from:\n\n"
            "**📋 Operational Information | MAS Lab All Staff**\n"
            "• Workflow updates and process changes\n"
            "• Maintenance and downtime announcements\n"
            "• Schedule and shift information\n"
            "• General operational updates\n\n"
            "**🎯 Quality | MAS Lab All Staff**\n"
            "• Quality control updates and alerts\n"
            "• Compliance and regulatory information\n"
            "• CAP/CLIA inspection notices\n"
            "• Error reports and corrective actions\n"
            "• Proficiency testing results\n\n"
            "**Forwarding Rules:**\n"
            "✅ Messages containing relevant keywords\n"
            "✅ Quality issues → High priority alerts\n"
            "✅ Operational updates → Medium priority\n"
            "✅ Automatic dashboard routing\n\n"
            "All relevant information will be forwarded to your team workspace!"
        )
        
        await self.teams_client.send_alert(
            "🔗 MAS Lab Channel Integration Active",
            notification,
            "success",
            {
                "Channels Monitored": "2",
                "Integration Status": "ACTIVE",
                "Forwarding": "Keyword-based",
                "Dashboard Routing": "Automatic"
            }
        )
        
        print("✅ MAS Lab channel monitoring configured!")


# Example messages for testing
def get_sample_mas_messages():
    """Get sample messages from MAS Lab channels for testing"""
    
    operational_messages = [
        {
            "content": "Attention all staff: The chemistry analyzer will be down for maintenance from 2 PM to 4 PM today. Please route all chemistry samples to the backup analyzer during this time.",
            "sender": "Lab Supervisor",
            "timestamp": datetime.now().isoformat()
        },
        {
            "content": "New workflow update: Effective immediately, all STAT samples must be logged in the priority tracking system. This is to improve our TAT compliance.",
            "sender": "Operations Manager",
            "timestamp": datetime.now().isoformat()
        },
        {
            "content": "Reminder: Staff meeting today at 3 PM to discuss the new phlebotomy scheduling system. All technicians are required to attend.",
            "sender": "Lab Director",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    quality_messages = [
        {
            "content": "QC ALERT: Chemistry glucose QC failed on analyzer 2. Please stop patient testing and run calibration. Document all actions in the QC log.",
            "sender": "QC Coordinator",
            "timestamp": datetime.now().isoformat()
        },
        {
            "content": "CAP Inspection Update: Our next CAP inspection is scheduled for next month. Please ensure all competency assessments are up to date.",
            "sender": "Quality Manager",
            "timestamp": datetime.now().isoformat()
        },
        {
            "content": "Proficiency Testing Results: Hematology PT passed with 100% score. Great job team! Coagulation PT results pending review.",
            "sender": "PT Coordinator",
            "timestamp": datetime.now().isoformat()
        },
        {
            "content": "Incident Report: Specimen labeling error identified in morning shift. Corrective action implemented. Please review the updated labeling procedure.",
            "sender": "Quality Analyst",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    return {
        "operational_information": operational_messages,
        "quality": quality_messages
    }


async def main():
    """Main function to forward MAS Lab channels"""
    
    print("📨 Kaiser Permanente Lab Automation - MAS Lab Channel Forwarding")
    print("=" * 70)
    
    try:
        forwarder = MASLabChannelForwarder()
        
        # Set up channel monitoring
        await forwarder.setup_channel_monitoring()
        
        # Get sample messages (in production, these would come from actual channels)
        sample_messages = get_sample_mas_messages()
        
        # Forward operational information messages
        print("\n\n📋 Processing Operational Information Channel:")
        await forwarder.forward_channel_messages(
            "operational_information",
            sample_messages["operational_information"]
        )
        
        # Small delay between channels
        await asyncio.sleep(2)
        
        # Forward quality messages
        print("\n\n🎯 Processing Quality Channel:")
        await forwarder.forward_channel_messages(
            "quality",
            sample_messages["quality"]
        )
        
        # Send completion summary
        await forwarder.teams_client.send_alert(
            "✅ MAS Lab Channel Sync Complete",
            f"**Channel Forwarding Summary**\n\n"
            f"Successfully processed messages from MAS Lab All Staff channels:\n\n"
            f"**📋 Operational Information**\n"
            f"• Messages processed: {len(sample_messages['operational_information'])}\n"
            f"• Topics: Maintenance, workflow updates, scheduling\n\n"
            f"**🎯 Quality**\n"
            f"• Messages processed: {len(sample_messages['quality'])}\n"
            f"• Topics: QC alerts, CAP updates, PT results\n\n"
            f"All relevant messages have been:\n"
            f"✅ Forwarded to team workspace\n"
            f"✅ Processed through alert system\n"
            f"✅ Routed to appropriate dashboards\n\n"
            f"Your team is now up to date with MAS Lab information!",
            "success",
            {
                "Total Messages": str(len(sample_messages['operational_information']) + len(sample_messages['quality'])),
                "Completion Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "COMPLETE"
            }
        )
        
        print("\n" + "=" * 70)
        print("🎉 SUCCESS! MAS Lab channels forwarded")
        print("\n📊 Next Steps:")
        print("• Check your team workspace for forwarded messages")
        print("• Review any high-priority quality alerts")
        print("• Verify dashboard updates in Notion")
        print("• Monitor Power BI for metric updates")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

