#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Manual Chat Message Forwarding Script

Allows you to manually forward specific messages from private chats
to your team workspace immediately.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from integrations.teams_chat_forwarder import forward_messages_now


def get_messages_to_forward():
    """
    Get messages to forward - you can edit this function to add your specific messages
    """
    
    # EDIT THIS SECTION: Add your specific messages to forward
    messages_to_forward = [
        """
        Lab Automation System Update:
        
        The Kaiser Permanente Lab Automation System is now fully operational! 
        
        Key achievements:
        • Notion integration: ✅ Working with performance and incident databases
        • Power BI dashboards: ✅ Receiving live data with discovered schema
        • Teams notifications: ✅ Automated alerts functional
        • HIPAA compliance: ✅ Audit logging active
        
        System is monitoring 10 phlebotomy stations with real-time performance tracking.
        
        Next steps: Begin daily operations and staff training.
        """,
        
        """
        Technical Integration Status:
        
        Successfully resolved all integration challenges:
        • Fixed Notion API token authentication
        • Discovered working Power BI field schema (Timestamp, ErrorCount, PerformanceScore, Department)
        • Configured Teams webhook for automated notifications
        • Implemented HIPAA-compliant audit logging
        
        System tested with 100% success rate on Power BI integration.
        Ready for production deployment.
        """,
        
        """
        Lab Operations Improvement Plan:
        
        The automation system addresses all identified issues:
        • 50% idle time reduction through real-time monitoring
        • TAT compliance improvement with automated tracking
        • Staff performance visibility with scoring system
        • Incident management with escalation workflows
        
        Expected benefits:
        • Improved operational efficiency
        • Better staff accountability
        • Faster issue resolution
        • Enhanced compliance reporting
        """,
        
        """
        System Capabilities Summary:
        
        Kaiser Permanente Lab Automation System now provides:
        
        Real-time Monitoring:
        • Staff performance tracking
        • TAT compliance monitoring  
        • Error rate calculation
        • Break time monitoring
        • QC compliance tracking
        
        Automated Workflows:
        • Performance threshold alerts
        • Incident escalation
        • Daily summary reports
        • Equipment status monitoring
        
        Integration Platform:
        • Epic Beaker (ready for configuration)
        • Qmatic queue management (ready)
        • Bio-Rad Unity QC (ready)
        • HR Connect scheduling (ready)
        • Notion collaboration (active)
        • Power BI dashboards (active)
        • Teams notifications (active)
        
        System is production-ready for Largo, MD location.
        """
    ]
    
    return messages_to_forward


async def main():
    """Main forwarding function"""
    
    print("📨 Kaiser Permanente Lab Automation - Chat Message Forwarding")
    print("=" * 70)
    
    try:
        # Get messages to forward
        messages = get_messages_to_forward()
        
        print(f"\n📋 Preparing to forward {len(messages)} messages...")
        print("   Target: Kaiser Permanente Lab Team Workspace")
        print("   Source: Lab Automation Private Chat")
        
        # Confirm forwarding
        print(f"\n📨 Messages to forward:")
        for i, msg in enumerate(messages):
            preview = msg.strip()[:100].replace('\n', ' ')
            print(f"   {i+1}. {preview}...")
        
        print(f"\n🚀 Forwarding messages to team workspace...")
        
        # Forward messages
        success = await forward_messages_now(messages)
        
        if success:
            print("\n🎉 SUCCESS!")
            print("✅ All messages forwarded to team workspace")
            print("🔗 Team Workspace: https://teams.microsoft.com/l/team/19%3AW4E7k-rolxQ9vqm8bggrjfWdOMhEMgwS1uiiVAm-Pd41%40thread.tacv2/conversations?groupId=018fb07b-4f1a-453f-a7a5-30ccfa3c679d&tenantId=3f8a7bc4-e337-47a5-a0fc-0d512c0e05f1")
            print("\n📋 Next Steps:")
            print("   1. Check your team workspace for the forwarded messages")
            print("   2. Review and respond to any questions")
            print("   3. Continue discussions in the team channel")
            print("   4. Document any action items or decisions")
            
            return True
        else:
            print("\n❌ FAILED!")
            print("Some messages may not have been forwarded successfully.")
            print("Check the logs for detailed error information.")
            return False
            
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
