"""
Kaiser Permanente Lab Automation System
Teams Chat Forwarding Integration

Automates forwarding of relevant lab discussions from private chats
to the main team workspace for better collaboration and visibility.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import aiohttp
import json
import re

from integrations.teams_client import TeamsClient
from utils.audit_logger import AuditLogger


class TeamsChatForwarder:
    """
    Automated chat forwarding system for Teams integration
    with the Kaiser Permanente Lab Automation System.
    """
    
    def __init__(self, teams_client: TeamsClient, config: Dict[str, Any]):
        """
        Initialize chat forwarder
        
        Args:
            teams_client: Teams client for sending messages
            config: Forwarding configuration
        """
        self.teams_client = teams_client
        self.config = config
        self.logger = logging.getLogger('teams_chat_forwarder')
        self.audit_logger = AuditLogger()
        
        # Extract team and chat information from URLs
        self.source_chat_id = "19:65f17ae5b11742ef93c07fed75fb1ea8@thread.v2"
        self.target_team_id = "19:W4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41@thread.tacv2"
        self.group_id = "018fb07b-4f1a-453f-a7a5-30ccfa3c679d"
        self.tenant_id = "3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1"
        
        # Lab automation keywords for filtering
        self.lab_keywords = [
            "lab automation", "performance", "tat", "qc", "quality control",
            "epic beaker", "qmatic", "bio-rad", "hrconnect", "notion",
            "powerbi", "power bi", "incident", "error", "compliance",
            "phlebotomy", "samples", "testing", "equipment", "maintenance",
            "staff", "schedule", "shift", "break time", "kaiser permanente",
            "largo", "md", "laboratory", "operations", "monitoring",
            "dashboard", "alert", "notification", "automation", "workflow"
        ]
    
    async def forward_relevant_messages(self, messages: List[Dict[str, Any]]) -> bool:
        """
        Forward relevant lab automation messages to team workspace
        
        Args:
            messages: List of messages to evaluate and potentially forward
            
        Returns:
            Success status
        """
        try:
            forwarded_count = 0
            
            for message in messages:
                if await self._is_lab_relevant(message):
                    success = await self._forward_message(message)
                    if success:
                        forwarded_count += 1
            
            self.logger.info(f"Forwarded {forwarded_count} relevant messages to team workspace")
            
            # Log forwarding activity
            self.audit_logger.log_system_event(
                "CHAT_FORWARDING",
                f"Forwarded {forwarded_count} messages to team workspace",
                {
                    "source_chat": self.source_chat_id,
                    "target_team": self.target_team_id,
                    "messages_processed": len(messages),
                    "messages_forwarded": forwarded_count
                }
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Message forwarding failed: {e}")
            return False
    
    async def _is_lab_relevant(self, message: Dict[str, Any]) -> bool:
        """
        Determine if a message is relevant to lab automation
        
        Args:
            message: Message to evaluate
            
        Returns:
            True if message should be forwarded
        """
        try:
            content = message.get("content", "").lower()
            sender = message.get("sender", "").lower()
            
            # Check for lab automation keywords
            for keyword in self.lab_keywords:
                if keyword in content:
                    return True
            
            # Check for specific lab system mentions
            lab_systems = ["epic", "beaker", "qmatic", "biorad", "unity", "notion", "powerbi"]
            for system in lab_systems:
                if system in content:
                    return True
            
            # Check for performance-related terms
            performance_terms = ["performance", "score", "metric", "compliance", "error", "incident"]
            for term in performance_terms:
                if term in content:
                    return True
            
            # Check if sender is a lab staff member (if configured)
            lab_staff = self.config.get("lab_staff_emails", [])
            if lab_staff and any(staff_email in sender for staff_email in lab_staff):
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Relevance check failed: {e}")
            return False
    
    async def _forward_message(self, message: Dict[str, Any]) -> bool:
        """
        Forward a single message to the team workspace
        
        Args:
            message: Message to forward
            
        Returns:
            Success status
        """
        try:
            # Extract message details
            content = message.get("content", "")
            sender = message.get("sender", "Unknown")
            timestamp = message.get("timestamp", datetime.now().isoformat())
            
            # Format forwarded message
            forwarded_title = "📨 Lab Automation Discussion Forward"
            forwarded_content = (
                f"**Forwarded from Lab Automation Chat**\n\n"
                f"**From:** {sender}\n"
                f"**Time:** {timestamp}\n"
                f"**Message:**\n{content}\n\n"
                f"---\n"
                f"*This message was automatically forwarded because it contains "
                f"lab automation-related content relevant to team operations.*"
            )
            
            # Send to team workspace via webhook
            success = await self.teams_client.send_alert(
                forwarded_title,
                forwarded_content,
                "info",
                {
                    "Original Sender": sender,
                    "Forward Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Source": "Lab Automation Private Chat",
                    "Relevance": "Lab Operations"
                }
            )
            
            if success:
                self.logger.debug(f"Forwarded message from {sender}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to forward message: {e}")
            return False
    
    async def forward_chat_summary(self, chat_summary: str, participants: List[str]) -> bool:
        """
        Forward a summary of important chat discussions
        
        Args:
            chat_summary: Summary of the chat discussion
            participants: List of chat participants
            
        Returns:
            Success status
        """
        try:
            title = "📋 Lab Automation Chat Summary"
            content = (
                f"**Lab Automation Discussion Summary**\n\n"
                f"**Participants:** {', '.join(participants)}\n"
                f"**Summary:**\n{chat_summary}\n\n"
                f"**Key Topics Discussed:**\n"
                f"• Lab operations and performance\n"
                f"• System integration updates\n"
                f"• Process improvements\n"
                f"• Technical discussions\n\n"
                f"---\n"
                f"*This summary was generated from lab automation-related discussions "
                f"to keep the team informed of important developments.*"
            )
            
            success = await self.teams_client.send_alert(
                title,
                content,
                "info",
                {
                    "Participants": f"{len(participants)} people",
                    "Summary Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Discussion Type": "Lab Automation",
                    "Action Required": "Review and follow up as needed"
                }
            )
            
            if success:
                self.logger.info("Chat summary forwarded to team workspace")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to forward chat summary: {e}")
            return False
    
    async def create_discussion_thread(self, topic: str, initial_message: str) -> bool:
        """
        Create a new discussion thread in the team workspace
        
        Args:
            topic: Discussion topic
            initial_message: Initial message content
            
        Returns:
            Success status
        """
        try:
            title = f"💬 Lab Discussion: {topic}"
            content = (
                f"**New Lab Automation Discussion Started**\n\n"
                f"**Topic:** {topic}\n\n"
                f"**Initial Message:**\n{initial_message}\n\n"
                f"**Discussion Guidelines:**\n"
                f"• Keep discussions focused on lab operations\n"
                f"• Tag relevant team members for input\n"
                f"• Document decisions and action items\n"
                f"• Follow up on implementation\n\n"
                f"---\n"
                f"*This discussion was initiated from lab automation chat forwarding.*"
            )
            
            success = await self.teams_client.send_alert(
                title,
                content,
                "info",
                {
                    "Discussion Topic": topic,
                    "Started By": "Lab Automation System",
                    "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Type": "Team Discussion",
                    "Action": "Participate and provide input"
                }
            )
            
            if success:
                self.logger.info(f"Discussion thread created: {topic}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to create discussion thread: {e}")
            return False


class ChatForwardingManager:
    """
    Manages the complete chat forwarding workflow for lab automation
    """
    
    def __init__(self, config_manager):
        """
        Initialize chat forwarding manager
        
        Args:
            config_manager: Configuration manager instance
        """
        self.config_manager = config_manager
        self.logger = logging.getLogger('chat_forwarding_manager')
        
    async def setup_chat_forwarding(self) -> bool:
        """
        Set up automated chat forwarding system
        
        Returns:
            Setup success status
        """
        try:
            self.logger.info("Setting up Teams chat forwarding system...")
            
            # Initialize Teams client
            teams_config = self.config_manager.get_teams_config()
            teams_client = TeamsClient(teams_config)
            
            # Configure forwarding settings
            forwarding_config = {
                "source_chat_id": "19:65f17ae5b11742ef93c07fed75fb1ea8@thread.v2",
                "target_team_id": "19:W4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41@thread.tacv2",
                "group_id": "018fb07b-4f1a-453f-a7a5-30ccfa3c679d",
                "tenant_id": "3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1",
                "lab_staff_emails": [
                    # Add your lab staff emails here for better filtering
                    "@kaiserpermanente.org"
                ],
                "forwarding_enabled": True,
                "auto_summary": True
            }
            
            # Create chat forwarder
            chat_forwarder = TeamsChatForwarder(teams_client, forwarding_config)
            
            # Send setup notification
            await teams_client.send_alert(
                "🔗 Chat Forwarding System Activated",
                f"**Kaiser Permanente Lab Automation - Chat Forwarding Setup**\n\n"
                f"✅ **Chat forwarding system is now active!**\n\n"
                f"**Configuration:**\n"
                f"• Source: Private lab automation chat\n"
                f"• Destination: Main team workspace\n"
                f"• Filtering: Lab automation keywords\n"
                f"• Auto-summary: Enabled\n\n"
                f"**What gets forwarded:**\n"
                f"• Lab automation discussions\n"
                f"• Performance-related conversations\n"
                f"• System integration updates\n"
                f"• Technical troubleshooting\n"
                f"• Process improvement ideas\n\n"
                f"**Team Workspace:** [Kaiser Permanente Lab Team](https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1)\n\n"
                f"Your team will now stay informed of all important lab automation discussions!",
                "success",
                {
                    "Forwarding Status": "ACTIVE",
                    "Source Chat": "Lab Automation Private",
                    "Target Team": "Kaiser Permanente Lab Team",
                    "Setup Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Auto-filtering": "Enabled"
                }
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Chat forwarding setup failed: {e}")
            return False
    
    async def forward_specific_messages(self, messages_to_forward: List[str]) -> bool:
        """
        Forward specific messages manually
        
        Args:
            messages_to_forward: List of message contents to forward
            
        Returns:
            Success status
        """
        try:
            teams_config = self.config_manager.get_teams_config()
            
            async with TeamsClient(teams_config) as teams_client:
                for i, message_content in enumerate(messages_to_forward):
                    # Format and send each message
                    title = f"📨 Lab Chat Forward #{i+1}"
                    content = (
                        f"**Forwarded Lab Automation Message**\n\n"
                        f"**Content:**\n{message_content}\n\n"
                        f"**Context:** Important lab automation discussion\n"
                        f"**Action:** Review and respond as needed\n\n"
                        f"---\n"
                        f"*Forwarded to keep team informed of lab operations discussions*"
                    )
                    
                    await teams_client.send_alert(
                        title,
                        content,
                        "info",
                        {
                            "Message Number": f"{i+1} of {len(messages_to_forward)}",
                            "Forward Time": datetime.now().strftime("%H:%M:%S"),
                            "Source": "Lab Automation Chat",
                            "Type": "Manual Forward"
                        }
                    )
                    
                    # Small delay between messages
                    await asyncio.sleep(1)
                
                # Send completion summary
                await teams_client.send_alert(
                    "✅ Chat Forwarding Complete",
                    f"**Message Forwarding Summary**\n\n"
                    f"Successfully forwarded **{len(messages_to_forward)} messages** "
                    f"from lab automation discussions to the team workspace.\n\n"
                    f"**Team Action Items:**\n"
                    f"• Review forwarded messages\n"
                    f"• Respond to any questions or concerns\n"
                    f"• Follow up on action items\n"
                    f"• Continue discussions in team channel\n\n"
                    f"**Team Workspace:** [View Team Discussions](https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1)",
                    "success",
                    {
                        "Messages Forwarded": len(messages_to_forward),
                        "Completion Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Status": "COMPLETE",
                        "Next Steps": "Review and respond in team workspace"
                    }
                )
                
                return True
                
        except Exception as e:
            self.logger.error(f"Specific message forwarding failed: {e}")
            return False
    
    async def _is_lab_relevant(self, message: Dict[str, Any]) -> bool:
        """Check if message is relevant to lab automation"""
        content = message.get("content", "").lower()
        
        # Check for lab automation keywords
        for keyword in self.lab_keywords:
            if keyword in content:
                return True
        
        return False


async def create_chat_forwarder(config_manager) -> ChatForwardingManager:
    """
    Create and configure chat forwarding manager
    
    Args:
        config_manager: Configuration manager instance
        
    Returns:
        Configured chat forwarding manager
    """
    return ChatForwardingManager(config_manager)


# Manual forwarding function for immediate use
async def forward_messages_now(messages_to_forward: List[str]) -> bool:
    """
    Immediately forward specified messages to team workspace
    
    Args:
        messages_to_forward: List of message contents to forward
        
    Returns:
        Success status
    """
    try:
        from config.config_manager import ConfigManager
        
        config_manager = ConfigManager()
        chat_manager = await create_chat_forwarder(config_manager)
        
        success = await chat_manager.forward_specific_messages(messages_to_forward)
        
        if success:
            print(f"✅ Successfully forwarded {len(messages_to_forward)} messages to team workspace")
            print("🔗 Team Workspace: https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1")
        else:
            print("❌ Message forwarding failed")
        
        return success
        
    except Exception as e:
        print(f"💥 Forwarding error: {e}")
        return False
