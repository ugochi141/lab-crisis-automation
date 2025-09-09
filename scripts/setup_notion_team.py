#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Notion Team Workspace Setup Script

Sets up and configures the Notion team workspace for lab automation operations.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from config.notion_team_config import NotionTeamManager
from integrations.teams_client import TeamsClient


class NotionTeamSetup:
    """Complete Notion team workspace setup orchestrator"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def print_header(self, text: str) -> None:
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)
    
    def print_step(self, step: str) -> None:
        """Print formatted step"""
        print(f"\n📋 {step}")
    
    def print_success(self, message: str) -> None:
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message: str) -> None:
        """Print error message"""
        print(f"❌ {message}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message"""
        print(f"⚠️  {message}")
    
    async def setup_team_workspace(self) -> bool:
        """Set up the complete team workspace"""
        try:
            self.print_header("Kaiser Permanente Lab Automation - Notion Team Setup")
            
            # Initialize team manager
            team_manager = NotionTeamManager(self.config_manager)
            
            # Step 1: Verify configuration
            self.print_step("Verifying configuration...")
            try:
                notion_config = self.config_manager.get_notion_config()
                self.print_success("Notion configuration verified")
            except Exception as e:
                self.print_error(f"Configuration error: {e}")
                return False
            
            # Step 2: Set up team workspace
            self.print_step("Setting up team workspace...")
            setup_results = await team_manager.setup_team_workspace()
            
            if setup_results.get("status") == "success":
                self.print_success("Team workspace setup completed")
                print(f"   Workspace ID: {setup_results.get('workspace_id')}")
                print(f"   Databases created: {setup_results.get('databases', {}).get('databases_created', 0)}")
                print(f"   Templates created: {setup_results.get('templates', {}).get('templates_created', 0)}")
            else:
                self.print_error(f"Workspace setup failed: {setup_results.get('error')}")
                return False
            
            # Step 3: Configure integration with automation system
            self.print_step("Integrating with automation system...")
            integration_success = await self._integrate_with_automation()
            
            if integration_success:
                self.print_success("Automation integration configured")
            else:
                self.print_warning("Automation integration partially configured")
            
            # Step 4: Set up team notifications
            self.print_step("Setting up team notifications...")
            notification_success = await self._setup_team_notifications()
            
            if notification_success:
                self.print_success("Team notifications configured")
            else:
                self.print_warning("Notification setup needs manual configuration")
            
            # Step 5: Create sample data
            self.print_step("Creating sample data...")
            await self._create_sample_data()
            self.print_success("Sample data created")
            
            # Step 6: Generate team invitation instructions
            self.print_step("Generating team setup instructions...")
            self._create_team_instructions()
            self.print_success("Team instructions created")
            
            # Final status
            self.print_header("Setup Complete!")
            print("\n🎉 Notion team workspace is now operational!")
            print("\nNext steps:")
            print("1. Share the team invitation link with your staff")
            print("2. Configure individual user permissions")
            print("3. Start the lab automation system")
            print("4. Test all integrations")
            print(f"\n🔗 Team Workspace: https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join")
            
            return True
            
        except Exception as e:
            self.print_error(f"Setup failed: {e}")
            return False
    
    async def _integrate_with_automation(self) -> bool:
        """Integrate team workspace with automation system"""
        try:
            # Update automation core to use team workspace
            integration_config = {
                "team_workspace_enabled": True,
                "workspace_id": "1cdd2227-51b3-818e-8bb7-004288f69712",
                "collaborative_features": {
                    "real_time_updates": True,
                    "team_notifications": True,
                    "shared_dashboards": True,
                    "role_based_access": True
                }
            }
            
            # Save integration configuration
            config_file = project_root / "config" / "team_integration.json"
            with open(config_file, 'w') as f:
                import json
                json.dump(integration_config, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Integration setup error: {e}")
            return False
    
    async def _setup_team_notifications(self) -> bool:
        """Set up team-wide notifications"""
        try:
            # Configure Teams notifications for the team workspace
            try:
                teams_config = self.config_manager.get_teams_config()
                async with TeamsClient(teams_config) as teams_client:
                    # Send setup notification
                    await teams_client.send_alert(
                        "🚀 Lab Automation Team Workspace Ready",
                        f"Your Kaiser Permanente Lab Automation team workspace is now operational!\n\n"
                        f"**Team Workspace:** https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join\n\n"
                        f"Features enabled:\n"
                        f"• Real-time performance tracking\n"
                        f"• Automated incident management\n"
                        f"• Team collaboration tools\n"
                        f"• Integrated alerting system",
                        "success",
                        {
                            "Workspace ID": "1cdd2227-51b3-818e-8bb7-004288f69712",
                            "Setup Date": "Today",
                            "Status": "Operational"
                        }
                    )
                return True
            except Exception:
                # Teams not configured yet, skip notification
                return False
                
        except Exception as e:
            print(f"Notification setup error: {e}")
            return False
    
    async def _create_sample_data(self) -> None:
        """Create sample data for testing"""
        try:
            # Create sample team data
            sample_team_data = {
                "team_members": [
                    {
                        "name": "Lab Manager",
                        "role": "Manager",
                        "permissions": "full_access",
                        "email": "manager@kaiserpermanente.org"
                    },
                    {
                        "name": "Day Supervisor", 
                        "role": "Supervisor",
                        "permissions": "supervisor_access",
                        "email": "day.supervisor@kaiserpermanente.org"
                    },
                    {
                        "name": "Night Supervisor",
                        "role": "Supervisor", 
                        "permissions": "supervisor_access",
                        "email": "night.supervisor@kaiserpermanente.org"
                    },
                    {
                        "name": "Lead Tech - Day",
                        "role": "Lead Technician",
                        "permissions": "lead_tech_access",
                        "email": "lead.day@kaiserpermanente.org"
                    },
                    {
                        "name": "Lead Tech - Night",
                        "role": "Lead Technician", 
                        "permissions": "lead_tech_access",
                        "email": "lead.night@kaiserpermanente.org"
                    }
                ],
                "sample_performance_data": [
                    {
                        "staff_member": "John Smith",
                        "date": "2024-01-15",
                        "shift": "Day (7a-7p)",
                        "samples_processed": 45,
                        "error_count": 1,
                        "performance_score": 85,
                        "status": "Good"
                    },
                    {
                        "staff_member": "Jane Doe", 
                        "date": "2024-01-15",
                        "shift": "Night (7p-7a)",
                        "samples_processed": 38,
                        "error_count": 0,
                        "performance_score": 92,
                        "status": "Excellent"
                    }
                ]
            }
            
            # Save sample data
            sample_file = project_root / "data" / "team_sample_data.json"
            with open(sample_file, 'w') as f:
                import json
                json.dump(sample_team_data, f, indent=2)
                
        except Exception as e:
            print(f"Sample data creation error: {e}")
    
    def _create_team_instructions(self) -> None:
        """Create team setup instructions"""
        instructions = '''# Kaiser Permanente Lab Automation Team Setup
## Team Workspace Instructions

### 🔗 Team Workspace Access
**Workspace URL:** https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join

### 👥 Team Member Roles & Permissions

#### Lab Manager
- **Full Access**: All databases and administrative functions
- **Responsibilities**: System oversight, configuration, reporting
- **Permissions**: Read, Write, Delete, Admin, Configure

#### Supervisors  
- **Supervisor Access**: Operational oversight and staff management
- **Responsibilities**: Performance monitoring, incident management, staff coaching
- **Permissions**: Read, Write, Alert Management, Performance Review

#### Lead Technicians
- **Lead Tech Access**: Technical operations and quality control
- **Responsibilities**: QC oversight, equipment monitoring, technical guidance
- **Permissions**: Read, Write, Performance Entry, QC Management

#### Technicians
- **Standard Access**: Data entry and basic monitoring
- **Responsibilities**: Daily performance entry, incident reporting
- **Permissions**: Read, Performance Entry, Incident Reporting

#### Quality Assurance
- **QA Access**: Quality oversight and compliance
- **Responsibilities**: Compliance monitoring, audit support
- **Permissions**: Read, Comment, QC Review, Compliance Reporting

### 🚀 Getting Started

1. **Join the Team Workspace**
   - Click the invitation link
   - Sign in with your Notion account
   - Accept the team invitation

2. **Familiarize Yourself with Databases**
   - Team Performance Dashboard
   - Incident Tracking System  
   - Real-Time Operations Monitor
   - Quality Control Tracker
   - Equipment Status Monitor

3. **Set Up Your Profile**
   - Add your profile photo
   - Set notification preferences
   - Configure your dashboard view

4. **Start Using the System**
   - Enter daily performance metrics
   - Report incidents when they occur
   - Monitor real-time operations
   - Collaborate with team members

### 📊 Key Features

- **Real-Time Collaboration**: Multiple users can work simultaneously
- **Automated Alerts**: Instant notifications for critical issues
- **Performance Tracking**: Individual and team performance metrics
- **Incident Management**: Comprehensive error tracking and resolution
- **Equipment Monitoring**: Real-time equipment status and maintenance
- **Quality Control**: QC compliance and testing status
- **Mobile Access**: Full functionality on mobile devices
- **Integration**: Connected to Power BI dashboards and Teams alerts

### 🔔 Notification Settings

The system will send notifications for:
- Critical incidents requiring immediate attention
- Performance threshold breaches
- Equipment failures or maintenance needs
- QC failures or out-of-range results
- Daily performance summaries
- System status changes

### 📱 Mobile App

Download the Notion mobile app for on-the-go access:
- iOS: App Store
- Android: Google Play Store

### 🆘 Support

For technical support:
- Check the system documentation
- Contact your Lab Manager
- Use the #lab-automation Teams channel
- Submit a ticket through IT support

### 🔒 Security & Compliance

- All data is HIPAA compliant
- Comprehensive audit logging
- Role-based access controls
- Secure data transmission
- Regular security updates

---

**Welcome to your new lab automation system!** 🎉
'''
        
        instructions_file = project_root / "TEAM_INSTRUCTIONS.md"
        with open(instructions_file, 'w') as f:
            f.write(instructions)


async def main():
    """Main setup function"""
    setup = NotionTeamSetup()
    success = await setup.setup_team_workspace()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
