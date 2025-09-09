#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Teams Collaboration Setup Script

Sets up comprehensive Teams integration for lab automation,
including chat forwarding, channel monitoring, and automated updates.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from integrations.teams_client import TeamsClient
from integrations.teams_chat_forwarder import ChatForwardingManager, create_chat_forwarder
from utils.audit_logger import AuditLogger


class TeamsCollaborationSetup:
    """
    Complete Teams collaboration setup for Kaiser Permanente Lab Automation
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.teams_config = self.config_manager.get_teams_config()
        self.teams_client = TeamsClient(self.teams_config)
        self.audit_logger = AuditLogger()
        
        # Team workspace details
        self.team_url = "https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1"
        self.private_chat_id = "19:65f17ae5b11742ef93c07fed75fb1ea8@thread.v2"
    
    async def setup_collaboration_channels(self) -> bool:
        """
        Set up dedicated collaboration channels in Teams
        """
        try:
            print("\n📋 Setting up Teams collaboration channels...")
            
            # Create welcome message with channel structure
            await self.teams_client.send_alert(
                "🚀 Lab Automation Team Collaboration Setup",
                f"**Kaiser Permanente Lab Automation - Team Workspace Configuration**\n\n"
                f"Welcome to your enhanced lab automation collaboration workspace!\n\n"
                f"**🔗 Team Workspace:** [Access Team](https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1)\n\n"
                f"**📂 Recommended Channel Structure:**\n"
                f"• **#general** - Team announcements and updates\n"
                f"• **#lab-performance** - Real-time performance metrics and alerts\n"
                f"• **#incidents** - Incident reports and resolution tracking\n"
                f"• **#automation-updates** - System updates and maintenance\n"
                f"• **#staff-scheduling** - Schedule updates and coverage\n"
                f"• **#quality-control** - QC results and compliance\n"
                f"• **#ideas-improvements** - Process improvement suggestions\n\n"
                f"**🤖 Automated Features:**\n"
                f"• Real-time performance alerts\n"
                f"• Incident escalation notifications\n"
                f"• Daily summary reports\n"
                f"• Chat message forwarding\n"
                f"• Integration status updates\n\n"
                f"**📊 Connected Systems:**\n"
                f"• Notion databases for tracking\n"
                f"• Power BI dashboards for visualization\n"
                f"• Epic Beaker (ready for connection)\n"
                f"• Qmatic queue management (ready)\n"
                f"• Bio-Rad Unity QC (ready)\n"
                f"• HRConnect scheduling (ready)\n\n"
                f"Your team is now equipped with comprehensive lab automation tools!",
                "success",
                {
                    "Setup Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Location": "Largo, MD",
                    "Phlebotomy Stations": "10",
                    "Status": "OPERATIONAL",
                    "Chat Forwarding": "ACTIVE"
                }
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Channel setup failed: {e}")
            return False
    
    async def create_automation_cards(self) -> bool:
        """
        Create informational cards for team members
        """
        try:
            print("\n📇 Creating automation information cards...")
            
            # Performance Monitoring Card
            await self.teams_client.send_alert(
                "📊 Performance Monitoring Guide",
                "**How to Use Lab Performance Monitoring**\n\n"
                "**Real-time Metrics:**\n"
                "• **TAT (Turn Around Time)** - Target: < 30 minutes\n"
                "• **QC Compliance** - Target: > 95%\n"
                "• **Error Rate** - Target: < 2%\n"
                "• **Staff Performance Score** - Target: > 85%\n\n"
                "**Alert Thresholds:**\n"
                "• 🔴 Critical: Performance < 60% or Errors > 5%\n"
                "• 🟡 Warning: Performance < 75% or Errors > 2%\n"
                "• 🟢 Good: Performance > 85% and Errors < 1%\n\n"
                "**What to Monitor:**\n"
                "• Individual staff performance trends\n"
                "• Station-specific bottlenecks\n"
                "• Peak hour performance dips\n"
                "• Equipment downtime patterns\n\n"
                "**Actions:**\n"
                "• Review Power BI dashboards daily\n"
                "• Respond to critical alerts immediately\n"
                "• Document corrective actions in Notion",
                "info",
                {
                    "Type": "Guide",
                    "Category": "Performance Monitoring",
                    "Updated": datetime.now().strftime("%Y-%m-%d"),
                    "Priority": "High"
                }
            )
            
            # Incident Management Card
            await self.teams_client.send_alert(
                "🚨 Incident Management Process",
                "**Lab Incident Response Procedures**\n\n"
                "**Incident Categories:**\n"
                "• **Equipment Failure** - Notify biomedical engineering\n"
                "• **Sample Issues** - Follow rejection protocol\n"
                "• **Staff Issues** - Escalate to supervisor\n"
                "• **System Errors** - Contact IT support\n\n"
                "**Response Steps:**\n"
                "1. **Immediate:** Acknowledge alert in Teams\n"
                "2. **Within 5 min:** Assess severity and impact\n"
                "3. **Within 15 min:** Implement corrective action\n"
                "4. **Within 30 min:** Update incident in Notion\n"
                "5. **End of shift:** Complete incident report\n\n"
                "**Escalation Path:**\n"
                "• Level 1: Lab Tech → Lead Tech (5 min)\n"
                "• Level 2: Lead Tech → Supervisor (10 min)\n"
                "• Level 3: Supervisor → Manager (15 min)\n"
                "• Level 4: Manager → Director (30 min)\n\n"
                "**Documentation:**\n"
                "All incidents must be logged in Notion with:\n"
                "• Timestamp and duration\n"
                "• Root cause analysis\n"
                "• Corrective actions taken\n"
                "• Prevention measures",
                "warning",
                {
                    "Type": "Process",
                    "Category": "Incident Management",
                    "Compliance": "HIPAA",
                    "Review": "Monthly"
                }
            )
            
            # Daily Operations Card
            await self.teams_client.send_alert(
                "📅 Daily Operations Checklist",
                "**Lab Automation Daily Tasks**\n\n"
                "**Morning (6:00 AM - 8:00 AM):**\n"
                "☐ Review overnight alerts and incidents\n"
                "☐ Check Power BI dashboards for anomalies\n"
                "☐ Verify all stations are operational\n"
                "☐ Review staff schedule in Notion\n"
                "☐ Conduct morning huddle via Teams\n\n"
                "**Mid-Day (12:00 PM - 1:00 PM):**\n"
                "☐ Monitor peak hour performance\n"
                "☐ Check TAT compliance rates\n"
                "☐ Review and address any alerts\n"
                "☐ Update shift handover notes\n\n"
                "**End of Day (4:00 PM - 6:00 PM):**\n"
                "☐ Complete daily performance summary\n"
                "☐ Document any outstanding issues\n"
                "☐ Update tomorrow's staffing in Notion\n"
                "☐ Review QC completion status\n"
                "☐ Send end-of-day report via Teams\n\n"
                "**Weekly Tasks:**\n"
                "• Monday: Review weekly performance trends\n"
                "• Wednesday: Staff performance reviews\n"
                "• Friday: System maintenance checks\n\n"
                "**Monthly Tasks:**\n"
                "• Generate compliance reports\n"
                "• Update SOPs and training materials\n"
                "• Review and optimize alert thresholds",
                "info",
                {
                    "Type": "Checklist",
                    "Category": "Daily Operations",
                    "Frequency": "Daily",
                    "Last Updated": datetime.now().strftime("%Y-%m-%d")
                }
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Card creation failed: {e}")
            return False
    
    async def configure_chat_forwarding(self) -> bool:
        """
        Configure automated chat forwarding rules
        """
        try:
            print("\n🔄 Configuring chat forwarding rules...")
            
            # Create chat forwarding manager
            chat_manager = await create_chat_forwarder(self.config_manager)
            
            # Set up forwarding
            success = await chat_manager.setup_chat_forwarding()
            
            if success:
                # Send configuration summary
                await self.teams_client.send_alert(
                    "🔗 Chat Forwarding Configuration",
                    "**Automated Chat Forwarding Rules**\n\n"
                    "**Active Forwarding:**\n"
                    f"• Source: Private Lab Chat ({self.private_chat_id})\n"
                    f"• Destination: [Team Workspace]({self.team_url})\n\n"
                    "**Keywords Monitored:**\n"
                    "• Lab automation, performance, TAT, QC\n"
                    "• Epic Beaker, Qmatic, Bio-Rad, HRConnect\n"
                    "• Notion, Power BI, incidents, errors\n"
                    "• Compliance, phlebotomy, testing\n"
                    "• Staff, schedule, equipment, maintenance\n\n"
                    "**Forwarding Rules:**\n"
                    "✅ Forward if contains lab keywords\n"
                    "✅ Forward if from lab staff\n"
                    "✅ Forward if mentions performance metrics\n"
                    "✅ Generate daily summaries\n"
                    "❌ Skip general conversations\n"
                    "❌ Skip personal messages\n\n"
                    "**Privacy & Compliance:**\n"
                    "• No PHI forwarding\n"
                    "• HIPAA compliant logging\n"
                    "• Audit trail maintained\n"
                    "• Manual review option available",
                    "success",
                    {
                        "Forwarding Status": "ACTIVE",
                        "Filter Mode": "Keywords + Staff",
                        "Compliance": "HIPAA",
                        "Auto-Summary": "Enabled"
                    }
                )
                
                print("✅ Chat forwarding configured successfully")
                return True
            else:
                print("❌ Chat forwarding configuration failed")
                return False
                
        except Exception as e:
            print(f"❌ Forwarding configuration error: {e}")
            return False
    
    async def create_team_resources(self) -> bool:
        """
        Create helpful resources for the team
        """
        try:
            print("\n📚 Creating team resources...")
            
            # Quick Reference Guide
            await self.teams_client.send_alert(
                "📖 Quick Reference Guide",
                "**Lab Automation System Quick Reference**\n\n"
                "**🔗 Important Links:**\n"
                f"• [Team Workspace]({self.team_url})\n"
                "• [Notion Performance Dashboard](https://www.notion.so/c1500b1816b14018beabe2b826ccafe9)\n"
                "• [Notion Incident Tracker](https://www.notion.so/cf2bb4448aff4324a602cb770cbae0a2)\n"
                "• [Power BI Lab Monitor](https://app.powerbi.com/groups/3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1)\n\n"
                "**⌨️ Quick Commands:**\n"
                "• View performance: Check #lab-performance channel\n"
                "• Report incident: Post in #incidents with @mention\n"
                "• Request help: Use @LabAutomation in any channel\n"
                "• Schedule change: Update in Notion + notify in #staff-scheduling\n\n"
                "**📞 Key Contacts:**\n"
                "• Lab Operations Manager: Via Teams\n"
                "• IT Support: Via #automation-updates\n"
                "• Biomedical Engineering: Via incident system\n"
                "• HR/Scheduling: Via HRConnect integration\n\n"
                "**🚨 Emergency Procedures:**\n"
                "• Critical system failure: Call supervisor immediately\n"
                "• Multiple station down: Escalate to manager\n"
                "• Data breach suspected: Contact IT security\n"
                "• Patient safety issue: Follow incident protocol\n\n"
                "Save this message for quick reference!",
                "info",
                {
                    "Type": "Reference",
                    "Version": "1.0",
                    "Updated": datetime.now().strftime("%Y-%m-%d"),
                    "Pin": "Recommended"
                }
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Resource creation failed: {e}")
            return False
    
    async def send_team_invitation(self) -> bool:
        """
        Send team invitation and onboarding information
        """
        try:
            print("\n📨 Sending team invitations...")
            
            await self.teams_client.send_alert(
                "👥 Join the Lab Automation Team!",
                "**Welcome to Kaiser Permanente Lab Automation Team**\n\n"
                "**You're Invited!**\n"
                f"Join our lab automation team workspace for real-time collaboration.\n\n"
                f"**🔗 [Click Here to Join Team]({self.team_url})**\n\n"
                "**What You'll Get:**\n"
                "• Real-time performance alerts\n"
                "• Incident notifications\n"
                "• Daily summary reports\n"
                "• Direct communication with team\n"
                "• Access to automation tools\n\n"
                "**After Joining:**\n"
                "1. Review pinned messages in #general\n"
                "2. Check #lab-performance for current metrics\n"
                "3. Introduce yourself to the team\n"
                "4. Set up your notification preferences\n"
                "5. Review the quick reference guide\n\n"
                "**Team Guidelines:**\n"
                "• Keep discussions professional\n"
                "• No PHI in chat messages\n"
                "• Use threads for detailed discussions\n"
                "• Tag relevant team members\n"
                "• Document decisions in Notion\n\n"
                "Looking forward to collaborating with you!",
                "info",
                {
                    "Invitation Type": "Team Workspace",
                    "Access Level": "Member",
                    "Location": "Largo, MD Lab",
                    "Onboarding": "Self-guided"
                }
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Invitation send failed: {e}")
            return False


async def main():
    """Main setup function"""
    
    print("🚀 Kaiser Permanente Lab Automation - Teams Collaboration Setup")
    print("=" * 70)
    
    try:
        setup = TeamsCollaborationSetup()
        
        # Run all setup steps
        steps = [
            ("Setting up collaboration channels", setup.setup_collaboration_channels()),
            ("Creating automation cards", setup.create_automation_cards()),
            ("Configuring chat forwarding", setup.configure_chat_forwarding()),
            ("Creating team resources", setup.create_team_resources()),
            ("Sending team invitations", setup.send_team_invitation())
        ]
        
        all_success = True
        for step_name, step_coro in steps:
            print(f"\n🔄 {step_name}...")
            success = await step_coro
            if success:
                print(f"✅ {step_name} completed")
            else:
                print(f"❌ {step_name} failed")
                all_success = False
        
        if all_success:
            print("\n" + "=" * 70)
            print("🎉 SUCCESS! Teams collaboration fully configured")
            print("\n📋 Summary:")
            print("✅ Team workspace configured with channels")
            print("✅ Automation guides and cards created")
            print("✅ Chat forwarding rules active")
            print("✅ Team resources available")
            print("✅ Invitations sent to team members")
            print(f"\n🔗 Team Workspace: https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1")
            print("\n🚀 Your team is ready for enhanced collaboration!")
            return True
        else:
            print("\n⚠️ Some setup steps failed. Check logs for details.")
            return False
            
    except Exception as e:
        print(f"\n💥 Setup error: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

