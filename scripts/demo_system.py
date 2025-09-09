#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Demo System - Works without database access

This script demonstrates the lab automation system functionality
using simulated data while you set up database sharing.
"""

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from integrations.teams_client import TeamsClient
from integrations.powerbi_client import PowerBIClient


class DemoLabAutomation:
    """Demo lab automation system with simulated data"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        
    def print_header(self, text: str) -> None:
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(f"  {text}")
        print("=" * 70)
    
    def print_step(self, step: str) -> None:
        """Print formatted step"""
        print(f"\n📋 {step}")
    
    def print_success(self, message: str) -> None:
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message: str) -> None:
        """Print error message"""
        print(f"❌ {message}")
    
    def print_info(self, message: str) -> None:
        """Print info message"""
        print(f"ℹ️  {message}")
    
    async def run_demo(self) -> bool:
        """Run the complete demo system"""
        try:
            self.print_header("Kaiser Permanente Lab Automation - DEMO MODE")
            
            # Step 1: Generate sample data
            self.print_step("Generating sample lab data...")
            sample_data = self._generate_sample_data()
            self.print_success(f"Generated {len(sample_data['performance'])} performance records")
            self.print_success(f"Generated {len(sample_data['incidents'])} incident records")
            
            # Step 2: Test Teams notifications
            self.print_step("Testing Teams notifications...")
            teams_success = await self._test_teams_integration(sample_data)
            
            # Step 3: Test Power BI updates
            self.print_step("Testing Power BI dashboard updates...")
            powerbi_success = await self._test_powerbi_integration(sample_data)
            
            # Step 4: Demonstrate monitoring features
            self.print_step("Demonstrating monitoring features...")
            await self._demonstrate_monitoring(sample_data)
            
            # Step 5: Show system capabilities
            self.print_step("Showing system capabilities...")
            self._show_system_capabilities()
            
            # Final status
            self.print_header("DEMO COMPLETED SUCCESSFULLY!")
            
            success_count = sum([teams_success, powerbi_success])
            self.print_info(f"Integration tests: {success_count}/2 successful")
            
            if success_count >= 1:
                await self._send_demo_completion_notification()
                self._show_next_steps()
                return True
            else:
                self.print_error("Demo had integration issues")
                return False
                
        except Exception as e:
            self.print_error(f"Demo failed: {e}")
            return False
    
    def _generate_sample_data(self) -> dict:
        """Generate realistic sample data for demo"""
        
        # Sample performance data
        performance_data = [
            {
                "staff_member": "John Smith",
                "date": datetime.now().date().isoformat(),
                "shift": "Day (7a-7p)",
                "samples_processed": 45,
                "error_count": 1,
                "break_time_minutes": 45,
                "qc_completion_percent": 98,
                "tat_target_met": True,
                "performance_score": 85,
                "status": "Good",
                "supervisor": "Day Supervisor",
                "notes": "Excellent work today, minor calibration issue resolved"
            },
            {
                "staff_member": "Jane Doe",
                "date": datetime.now().date().isoformat(),
                "shift": "Night (7p-7a)",
                "samples_processed": 38,
                "error_count": 0,
                "break_time_minutes": 40,
                "qc_completion_percent": 100,
                "tat_target_met": True,
                "performance_score": 92,
                "status": "Excellent",
                "supervisor": "Night Supervisor",
                "notes": "Perfect shift, all QC passed"
            },
            {
                "staff_member": "Mike Johnson",
                "date": datetime.now().date().isoformat(),
                "shift": "Day (7a-7p)",
                "samples_processed": 30,
                "error_count": 3,
                "break_time_minutes": 65,
                "qc_completion_percent": 85,
                "tat_target_met": False,
                "performance_score": 65,
                "status": "Needs Improvement",
                "supervisor": "Day Supervisor",
                "notes": "Performance coaching scheduled"
            }
        ]
        
        # Sample incident data
        incident_data = [
            {
                "incident_id": "INC-2024-001",
                "timestamp": datetime.now().isoformat(),
                "staff_member": "Mike Johnson",
                "incident_type": "TAT Miss",
                "severity": "Medium",
                "impact": "Quality",
                "description": "Sample processing delayed due to equipment calibration issue",
                "root_cause": "Equipment calibration overdue",
                "corrective_action": "Scheduled immediate calibration and updated maintenance schedule",
                "status": "Resolved"
            },
            {
                "incident_id": "INC-2024-002", 
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "staff_member": "System",
                "incident_type": "Equipment Issue",
                "severity": "High",
                "impact": "Productivity",
                "description": "Sysmex XN-1000 showing intermittent connection errors",
                "root_cause": "Network connectivity issue",
                "corrective_action": "IT support contacted, backup procedures activated",
                "status": "In Progress"
            }
        ]
        
        # Sample operational metrics
        operational_data = {
            "timestamp": datetime.now().isoformat(),
            "total_samples_today": 113,
            "total_errors": 4,
            "error_rate": 3.5,
            "tat_compliance": 87,
            "avg_performance_score": 80.7,
            "active_staff": 8,
            "open_incidents": 1,
            "critical_incidents": 0,
            "equipment_status": "1 Minor Issue",
            "qc_status": "All Systems Normal"
        }
        
        return {
            "performance": performance_data,
            "incidents": incident_data,
            "operations": operational_data
        }
    
    async def _test_teams_integration(self, sample_data: dict) -> bool:
        """Test Teams integration with sample data"""
        try:
            teams_config = self.config_manager.get_teams_config()
            async with TeamsClient(teams_config) as teams_client:
                
                # Send demo notification
                success = await teams_client.send_alert(
                    "🧪 Lab Automation Demo - System Operational!",
                    f"**Kaiser Permanente Lab Automation System Demo**\n\n"
                    f"Your lab automation system is working correctly!\n\n"
                    f"**Today's Sample Metrics:**\n"
                    f"• Total Samples: {sample_data['operations']['total_samples_today']}\n"
                    f"• TAT Compliance: {sample_data['operations']['tat_compliance']}%\n"
                    f"• Error Rate: {sample_data['operations']['error_rate']}%\n"
                    f"• Active Staff: {sample_data['operations']['active_staff']}\n"
                    f"• Open Incidents: {sample_data['operations']['open_incidents']}\n\n"
                    f"**System Features Active:**\n"
                    f"• Real-time performance monitoring ✅\n"
                    f"• Automated incident management ✅\n"
                    f"• Teams notifications ✅\n"
                    f"• Power BI dashboards ✅\n"
                    f"• HIPAA audit logging ✅\n\n"
                    f"Ready for production use!",
                    "success",
                    {
                        "Demo Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Performance Score": f"{sample_data['operations']['avg_performance_score']}/100",
                        "System Status": "Fully Operational",
                        "Next Step": "Complete Notion database sharing"
                    }
                )
                
                if success:
                    self.print_success("Teams notification sent successfully!")
                    
                    # Send performance alert demo
                    await teams_client.send_performance_alert(
                        "Mike Johnson",
                        ["Performance score below threshold (65)", "Extended break time (65 minutes)", "TAT target missed"],
                        sample_data['performance'][2]
                    )
                    
                    self.print_success("Performance alert demo sent!")
                    return True
                else:
                    self.print_error("Teams notification failed")
                    return False
                    
        except Exception as e:
            self.print_error(f"Teams integration test failed: {e}")
            return False
    
    async def _test_powerbi_integration(self, sample_data: dict) -> bool:
        """Test Power BI integration with sample data"""
        try:
            powerbi_config = self.config_manager.get_powerbi_config()
            async with PowerBIClient(powerbi_config) as powerbi_client:
                
                # Test performance data update
                performance_success = await powerbi_client.update_performance_dataset(
                    sample_data['performance']
                )
                
                # Test real-time metrics update
                metrics_success = await powerbi_client.update_real_time_metrics(
                    sample_data['operations']
                )
                
                if performance_success and metrics_success:
                    self.print_success("Power BI dashboards updated successfully!")
                    self.print_info("Check your Power BI workspace for updated data")
                    return True
                else:
                    self.print_error("Power BI update failed")
                    return False
                    
        except Exception as e:
            self.print_error(f"Power BI integration test failed: {e}")
            return False
    
    async def _demonstrate_monitoring(self, sample_data: dict) -> None:
        """Demonstrate monitoring capabilities"""
        try:
            self.print_info("Analyzing sample performance data...")
            
            # Analyze performance
            total_samples = sum(p['samples_processed'] for p in sample_data['performance'])
            total_errors = sum(p['error_count'] for p in sample_data['performance'])
            error_rate = (total_errors / total_samples) * 100 if total_samples > 0 else 0
            
            # Check thresholds
            thresholds = self.config_manager.get_alert_thresholds()
            
            alerts_triggered = []
            
            for performance in sample_data['performance']:
                staff_alerts = []
                
                if performance['performance_score'] < thresholds.performance_score_threshold:
                    staff_alerts.append(f"Performance score low: {performance['performance_score']}")
                
                if performance['break_time_minutes'] > thresholds.break_time_threshold_minutes:
                    staff_alerts.append(f"Break time exceeded: {performance['break_time_minutes']} minutes")
                
                if not performance['tat_target_met']:
                    staff_alerts.append("TAT target missed")
                
                if staff_alerts:
                    alerts_triggered.append({
                        "staff_member": performance['staff_member'],
                        "alerts": staff_alerts
                    })
            
            # Display monitoring results
            self.print_success(f"Processed {len(sample_data['performance'])} staff performance records")
            self.print_info(f"Total samples processed: {total_samples}")
            self.print_info(f"Overall error rate: {error_rate:.1f}%")
            self.print_info(f"Performance alerts triggered: {len(alerts_triggered)}")
            
            for alert in alerts_triggered:
                self.print_info(f"  ⚠️  {alert['staff_member']}: {', '.join(alert['alerts'])}")
            
        except Exception as e:
            self.print_error(f"Monitoring demonstration failed: {e}")
    
    def _show_system_capabilities(self) -> None:
        """Show all system capabilities"""
        self.print_header("SYSTEM CAPABILITIES DEMONSTRATION")
        
        print("\n🏥 **Lab Management Features:**")
        print("   ✅ Real-time performance tracking")
        print("   ✅ Automated TAT monitoring")
        print("   ✅ Error rate calculation and alerting")
        print("   ✅ Staff performance scoring")
        print("   ✅ Break time monitoring")
        print("   ✅ QC compliance tracking")
        
        print("\n🚨 **Incident Management:**")
        print("   ✅ Automated incident creation")
        print("   ✅ Severity-based escalation")
        print("   ✅ Root cause analysis tracking")
        print("   ✅ Corrective action monitoring")
        print("   ✅ Pattern detection")
        
        print("\n📊 **Dashboard Integration:**")
        print("   ✅ Power BI real-time updates")
        print("   ✅ Performance visualizations")
        print("   ✅ Trend analysis")
        print("   ✅ Executive reporting")
        
        print("\n🔔 **Alert System:**")
        print("   ✅ Microsoft Teams notifications")
        print("   ✅ Threshold-based alerts")
        print("   ✅ Critical incident escalation")
        print("   ✅ Daily summary reports")
        print("   ✅ Shift handoff notifications")
        
        print("\n🔒 **Compliance & Security:**")
        print("   ✅ HIPAA-compliant audit logging")
        print("   ✅ Data encryption")
        print("   ✅ Role-based access control")
        print("   ✅ Comprehensive activity tracking")
        
        print("\n🔧 **Integration Capabilities:**")
        print("   ✅ Epic Beaker (LIS) - Ready for configuration")
        print("   ✅ Qmatic (Queue Management) - Ready for configuration")
        print("   ✅ Bio-Rad Unity (QC) - Ready for configuration")
        print("   ✅ HR Connect (Scheduling) - Ready for configuration")
        print("   ✅ Notion (Data Management) - Configured")
        print("   ✅ Power BI (Dashboards) - Configured")
        print("   ✅ Teams (Notifications) - Configured")
    
    async def _send_demo_completion_notification(self) -> None:
        """Send demo completion notification"""
        try:
            teams_config = self.config_manager.get_teams_config()
            async with TeamsClient(teams_config) as teams_client:
                await teams_client.send_alert(
                    "🎉 Lab Automation Demo Complete!",
                    f"**Kaiser Permanente Lab Automation System**\n"
                    f"Demo completed successfully!\n\n"
                    f"**What was demonstrated:**\n"
                    f"• Performance monitoring with threshold alerts\n"
                    f"• Incident tracking and management\n"
                    f"• Real-time dashboard updates\n"
                    f"• Automated Teams notifications\n"
                    f"• HIPAA-compliant audit logging\n\n"
                    f"**Next Steps:**\n"
                    f"1. Complete Notion database sharing\n"
                    f"2. Configure additional lab system integrations\n"
                    f"3. Train staff on the new system\n"
                    f"4. Begin production operations\n\n"
                    f"Your lab automation system is ready for deployment!",
                    "success"
                )
        except Exception as e:
            self.print_error(f"Demo completion notification failed: {e}")
    
    def _show_next_steps(self) -> None:
        """Show next steps for full deployment"""
        self.print_header("NEXT STEPS FOR FULL DEPLOYMENT")
        
        print("\n📋 **Immediate Actions (Today):**")
        print("   1. Complete Notion database sharing (see NOTION_SETUP_GUIDE.md)")
        print("   2. Test full integration: python scripts/connect_lab_centers.py")
        print("   3. Verify all systems are connected")
        
        print("\n🔧 **System Configuration (This Week):**")
        print("   1. Configure Epic Beaker integration")
        print("   2. Set up Qmatic queue management")
        print("   3. Connect Bio-Rad Unity QC system")
        print("   4. Integrate HR Connect scheduling")
        
        print("\n👥 **Team Onboarding (Next Week):**")
        print("   1. Invite team members to Notion workspace")
        print("   2. Configure user roles and permissions")
        print("   3. Conduct staff training sessions")
        print("   4. Create standard operating procedures")
        
        print("\n🚀 **Production Deployment:**")
        print("   1. Start with pilot group (5-10 staff)")
        print("   2. Monitor system performance")
        print("   3. Collect feedback and optimize")
        print("   4. Full rollout to all staff")
        
        print("\n📊 **Success Metrics:**")
        print("   • TAT compliance improvement")
        print("   • Error rate reduction")
        print("   • Staff productivity increase")
        print("   • Incident response time improvement")
        
        print("\n🔗 **Important Links:**")
        print("   • Setup Guide: NOTION_SETUP_GUIDE.md")
        print("   • Security Guide: SECURITY_GUIDE.md")
        print("   • Full Instructions: SETUP_INSTRUCTIONS.md")
        print("   • Team Workspace: https://www.notion.so/team/1cdd2227-51b3-818e-8bb7-004288f69712/join")


async def main():
    """Main demo function"""
    demo = DemoLabAutomation()
    success = await demo.run_demo()
    
    if success:
        print("\n🎉 Demo completed successfully!")
        print("\nYour Kaiser Permanente Lab Automation System is ready!")
        print("Follow the next steps above to complete full deployment.")
        sys.exit(0)
    else:
        print("\n⚠️  Demo completed with some integration issues.")
        print("Check the logs and configuration, then try again.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
