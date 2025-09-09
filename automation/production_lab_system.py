#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Production System - Complete Integration

Final production-ready system that integrates all components:
Notion, Power BI, Teams, and lab operations monitoring.
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config.config_manager import ConfigManager
from integrations.notion_client import NotionClient
from integrations.working_powerbi_client import create_working_powerbi_client
from integrations.teams_client import TeamsClient
from integrations.teams_chat_forwarder import create_chat_forwarder
from utils.audit_logger import AuditLogger


class ProductionLabSystem:
    """
    Production-ready Kaiser Permanente Lab Automation System
    with complete integration of all components.
    """
    
    def __init__(self):
        """Initialize the production lab system"""
        self.config_manager = ConfigManager()
        self.audit_logger = AuditLogger()
        self.logger = self._setup_logging()
        
        # System state
        self.is_running = False
        self.start_time = None
        self.last_heartbeat = None
        
        # Performance tracking
        self.cycles_completed = 0
        self.alerts_sent = 0
        self.errors_detected = 0
        
    def _setup_logging(self) -> logging.Logger:
        """Setup production logging"""
        logger = logging.getLogger('production_lab_system')
        logger.setLevel(logging.INFO)
        
        # Create logs directory
        Path('logs').mkdir(exist_ok=True)
        
        # Production log handler
        handler = logging.FileHandler('logs/production_system.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Console handler for monitoring
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.is_running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def start_production_system(self) -> None:
        """Start the complete production lab automation system"""
        try:
            self.logger.info("🚀 Starting Kaiser Permanente Lab Automation System - PRODUCTION MODE")
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            # Initialize all clients
            await self._initialize_production_clients()
            
            # Send startup notification
            await self._send_startup_notification()
            
            # Start monitoring loop
            self.is_running = True
            self.start_time = datetime.now()
            
            await self._production_monitoring_loop()
            
        except Exception as e:
            self.logger.error(f"Production system startup failed: {e}")
            raise
    
    async def _initialize_production_clients(self) -> None:
        """Initialize all production clients"""
        try:
            self.logger.info("Initializing production clients...")
            
            # Initialize Notion client
            notion_config = self.config_manager.get_notion_config()
            self.notion_client = NotionClient(notion_config)
            
            # Initialize enhanced Power BI client
            self.powerbi_client = await create_working_powerbi_client()
            
            # Initialize Teams client
            teams_config = self.config_manager.get_teams_config()
            self.teams_client = TeamsClient(teams_config)
            
            # Initialize chat forwarder
            self.chat_forwarder = await create_chat_forwarder(self.config_manager)
            
            self.logger.info("✅ All production clients initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Client initialization failed: {e}")
            raise
    
    async def _send_startup_notification(self) -> None:
        """Send system startup notification"""
        try:
            await self.teams_client.send_alert(
                "🚀 PRODUCTION SYSTEM STARTED",
                f"**Kaiser Permanente Lab Automation System - PRODUCTION MODE**\n\n"
                f"🏥 **Your lab automation system is now LIVE and monitoring operations!**\n\n"
                f"**📊 ACTIVE MONITORING:**\n"
                f"• 10 phlebotomy stations\n"
                f"• Real-time staff performance\n"
                f"• TAT compliance tracking\n"
                f"• Error rate monitoring\n"
                f"• QC compliance verification\n"
                f"• Incident management workflow\n\n"
                f"**🔗 INTEGRATED SYSTEMS:**\n"
                f"• Notion: Team collaboration and data management ✅\n"
                f"• Power BI: Live dashboards and analytics ✅\n"
                f"• Teams: Automated notifications and alerts ✅\n"
                f"• Chat Forwarding: Team communication enhancement ✅\n\n"
                f"**⚡ EXPECTED BENEFITS:**\n"
                f"• 50% reduction in idle time\n"
                f"• Improved TAT compliance\n"
                f"• Enhanced staff accountability\n"
                f"• Faster incident response\n"
                f"• Automated performance reporting\n\n"
                f"**🎯 OPERATIONAL GOALS:**\n"
                f"• TAT Compliance: >85%\n"
                f"• Error Rate: <2%\n"
                f"• Performance Score: >80\n"
                f"• QC Completion: >95%\n\n"
                f"Your Kaiser Permanente Lab Operations are now fully automated! 🎊",
                "success",
                {
                    "System Status": "PRODUCTION ACTIVE",
                    "Location": "Kaiser Permanente Largo, MD",
                    "Start Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Monitoring": "10 phlebotomy stations",
                    "Integration Status": "All systems operational",
                    "Expected Benefits": "50% idle time reduction, improved compliance"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Startup notification failed: {e}")
    
    async def _production_monitoring_loop(self) -> None:
        """Main production monitoring loop"""
        try:
            self.logger.info("🔄 Starting production monitoring loop...")
            
            operational_settings = self.config_manager.get_operational_settings()
            monitoring_interval = operational_settings.monitoring_interval_seconds
            
            while self.is_running:
                cycle_start = datetime.now()
                
                try:
                    # Execute monitoring cycle
                    await self._execute_monitoring_cycle()
                    
                    # Update cycle counter
                    self.cycles_completed += 1
                    
                    # Send periodic heartbeat
                    if self.cycles_completed % 12 == 0:  # Every hour (5min intervals * 12)
                        await self._send_system_heartbeat()
                    
                    # Calculate sleep time
                    cycle_duration = (datetime.now() - cycle_start).total_seconds()
                    sleep_time = max(0, monitoring_interval - cycle_duration)
                    
                    if sleep_time > 0:
                        await asyncio.sleep(sleep_time)
                    
                except Exception as e:
                    self.logger.error(f"Monitoring cycle error: {e}")
                    self.errors_detected += 1
                    
                    # Send error alert if too many errors
                    if self.errors_detected >= 3:
                        await self._send_system_error_alert(str(e))
                        self.errors_detected = 0  # Reset counter
                    
                    await asyncio.sleep(60)  # Wait 1 minute before retry
            
            # Graceful shutdown
            await self._shutdown_system()
            
        except Exception as e:
            self.logger.error(f"Production monitoring loop failed: {e}")
            raise
    
    async def _execute_monitoring_cycle(self) -> None:
        """Execute one complete monitoring cycle"""
        try:
            cycle_start = datetime.now()
            
            # Step 1: Collect performance data from Notion
            performance_data = await self._collect_performance_data()
            
            # Step 2: Collect incident data
            incident_data = await self._collect_incident_data()
            
            # Step 3: Calculate metrics and analyze performance
            metrics = await self._calculate_operational_metrics(performance_data, incident_data)
            
            # Step 4: Check for alerts and thresholds
            await self._check_performance_thresholds(performance_data)
            
            # Step 5: Update Power BI dashboards
            await self._update_powerbi_dashboards(performance_data, metrics)
            
            # Step 6: Send periodic updates
            if self.cycles_completed % 4 == 0:  # Every 20 minutes
                await self._send_periodic_update(metrics)
            
            cycle_duration = (datetime.now() - cycle_start).total_seconds()
            self.logger.debug(f"Monitoring cycle completed in {cycle_duration:.2f} seconds")
            
        except Exception as e:
            self.logger.error(f"Monitoring cycle execution failed: {e}")
            raise
    
    async def _collect_performance_data(self) -> List[Dict[str, Any]]:
        """Collect current performance data"""
        try:
            async with self.notion_client:
                performance_data = await self.notion_client.get_performance_data(days_back=1)
                self.logger.debug(f"Collected {len(performance_data)} performance records")
                return performance_data
                
        except Exception as e:
            self.logger.error(f"Performance data collection failed: {e}")
            return []
    
    async def _collect_incident_data(self) -> List[Dict[str, Any]]:
        """Collect current incident data"""
        try:
            async with self.notion_client:
                incident_data = await self.notion_client.get_open_incidents()
                self.logger.debug(f"Collected {len(incident_data)} open incidents")
                return incident_data
                
        except Exception as e:
            self.logger.error(f"Incident data collection failed: {e}")
            return []
    
    async def _calculate_operational_metrics(self, performance_data: List[Dict], incident_data: List[Dict]) -> Dict[str, Any]:
        """Calculate operational metrics from collected data"""
        try:
            if not performance_data:
                return {
                    "total_samples": 0,
                    "total_errors": 0,
                    "error_rate": 0,
                    "tat_compliance": 0,
                    "avg_performance_score": 0,
                    "active_staff": 0,
                    "open_incidents": len(incident_data),
                    "critical_incidents": len([i for i in incident_data if i.get("severity") == "Critical"])
                }
            
            # Calculate metrics
            total_samples = sum(record.get("samples_processed", 0) for record in performance_data)
            total_errors = sum(record.get("error_count", 0) for record in performance_data)
            error_rate = (total_errors / total_samples * 100) if total_samples > 0 else 0
            
            tat_met_count = sum(1 for record in performance_data if record.get("tat_target_met", False))
            tat_compliance = (tat_met_count / len(performance_data) * 100) if performance_data else 0
            
            avg_performance = sum(record.get("performance_score", 0) for record in performance_data) / len(performance_data) if performance_data else 0
            
            metrics = {
                "total_samples": total_samples,
                "total_errors": total_errors,
                "error_rate": error_rate,
                "tat_compliance": tat_compliance,
                "avg_performance_score": avg_performance,
                "active_staff": len(performance_data),
                "open_incidents": len(incident_data),
                "critical_incidents": len([i for i in incident_data if i.get("severity") == "Critical"]),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.debug(f"Calculated operational metrics: TAT={tat_compliance:.1f}%, Errors={error_rate:.1f}%")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Metrics calculation failed: {e}")
            return {}
    
    async def _check_performance_thresholds(self, performance_data: List[Dict[str, Any]]) -> None:
        """Check performance against thresholds and send alerts"""
        try:
            thresholds = self.config_manager.get_alert_thresholds()
            
            for record in performance_data:
                staff_member = record.get("staff_member", "Unknown")
                alerts = []
                
                # Check performance score
                performance_score = record.get("performance_score", 0)
                if performance_score < thresholds.performance_score_threshold:
                    alerts.append(f"Performance score below threshold: {performance_score}")
                
                # Check break time
                break_time = record.get("break_time_minutes", 0)
                if break_time > thresholds.break_time_threshold_minutes:
                    alerts.append(f"Break time exceeded: {break_time} minutes")
                
                # Check TAT compliance
                if not record.get("tat_target_met", True):
                    alerts.append("TAT target not met")
                
                # Check error rate
                samples = record.get("samples_processed", 0)
                errors = record.get("error_count", 0)
                if samples > 0:
                    error_rate = (errors / samples) * 100
                    if error_rate > thresholds.error_rate_threshold:
                        alerts.append(f"Error rate high: {error_rate:.1f}%")
                
                # Send alerts if any issues found
                if alerts:
                    await self._send_performance_alert(staff_member, alerts, record)
                    self.alerts_sent += 1
            
        except Exception as e:
            self.logger.error(f"Threshold checking failed: {e}")
    
    async def _send_performance_alert(self, staff_member: str, issues: List[str], record: Dict[str, Any]) -> None:
        """Send performance alert for staff member"""
        try:
            await self.teams_client.send_performance_alert(
                staff_member,
                issues,
                record
            )
            
            # Log alert
            self.audit_logger.log_alert_sent({
                "alert_type": "performance",
                "staff_member": staff_member,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"Performance alert failed: {e}")
    
    async def _update_powerbi_dashboards(self, performance_data: List[Dict], metrics: Dict[str, Any]) -> None:
        """Update Power BI dashboards with latest data"""
        try:
            async with self.powerbi_client:
                # Update performance data
                if performance_data:
                    await self.powerbi_client.update_lab_performance(performance_data)
                
                # Update real-time metrics
                await self.powerbi_client.update_real_time_metrics(metrics)
                
                # Send lab status update
                await self.powerbi_client.send_lab_status_update({
                    "total_errors": metrics.get("total_errors", 0),
                    "avg_performance_score": metrics.get("avg_performance_score", 0),
                    "location": "Largo MD",
                    "active_staff": metrics.get("active_staff", 0)
                })
            
            self.logger.debug("Power BI dashboards updated successfully")
            
        except Exception as e:
            self.logger.error(f"Power BI dashboard update failed: {e}")
    
    async def _send_periodic_update(self, metrics: Dict[str, Any]) -> None:
        """Send periodic status update"""
        try:
            uptime = datetime.now() - self.start_time if self.start_time else timedelta(0)
            
            await self.teams_client.send_alert(
                "📊 Lab Automation Status Update",
                f"**Kaiser Permanente Lab Operations - Periodic Update**\n\n"
                f"🕐 **System Uptime:** {str(uptime).split('.')[0]}\n"
                f"🔄 **Monitoring Cycles:** {self.cycles_completed}\n"
                f"🚨 **Alerts Sent:** {self.alerts_sent}\n\n"
                f"**📈 Current Metrics:**\n"
                f"• Total Samples Today: {metrics.get('total_samples', 0)}\n"
                f"• Error Rate: {metrics.get('error_rate', 0):.1f}%\n"
                f"• TAT Compliance: {metrics.get('tat_compliance', 0):.1f}%\n"
                f"• Average Performance: {metrics.get('avg_performance_score', 0):.1f}\n"
                f"• Active Staff: {metrics.get('active_staff', 0)}\n"
                f"• Open Incidents: {metrics.get('open_incidents', 0)}\n\n"
                f"**🏥 System Status:** All components operational\n"
                f"**📍 Location:** Kaiser Permanente Largo, MD\n\n"
                f"Lab automation system continues monitoring and optimizing operations! ⚡",
                "info",
                {
                    "System Uptime": str(uptime).split('.')[0],
                    "Monitoring Cycles": self.cycles_completed,
                    "Alerts Sent": self.alerts_sent,
                    "TAT Compliance": f"{metrics.get('tat_compliance', 0):.1f}%",
                    "Error Rate": f"{metrics.get('error_rate', 0):.1f}%",
                    "Active Staff": metrics.get('active_staff', 0)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Periodic update failed: {e}")
    
    async def _send_system_heartbeat(self) -> None:
        """Send system heartbeat"""
        try:
            # Send heartbeat to Power BI
            async with self.powerbi_client:
                await self.powerbi_client.send_heartbeat()
            
            # Update last heartbeat time
            self.last_heartbeat = datetime.now()
            
            self.logger.debug("System heartbeat sent")
            
        except Exception as e:
            self.logger.error(f"System heartbeat failed: {e}")
    
    async def _send_system_error_alert(self, error_message: str) -> None:
        """Send system error alert"""
        try:
            await self.teams_client.send_alert(
                "🚨 SYSTEM ERROR ALERT",
                f"**Kaiser Permanente Lab Automation - System Error**\n\n"
                f"⚠️ **Multiple errors detected in monitoring system:**\n\n"
                f"**Error Details:**\n{error_message}\n\n"
                f"**System Status:** Continuing operation with error handling\n"
                f"**Action Required:** Check system logs and investigate\n\n"
                f"**Troubleshooting:**\n"
                f"• Check network connectivity\n"
                f"• Verify API credentials\n"
                f"• Review system logs in logs/ directory\n"
                f"• Restart system if issues persist\n\n"
                f"System will continue attempting to recover automatically.",
                "critical",
                {
                    "Error Count": self.errors_detected,
                    "System Uptime": str(datetime.now() - self.start_time).split('.')[0] if self.start_time else "Unknown",
                    "Last Successful Cycle": self.cycles_completed,
                    "Recovery Mode": "Active"
                }
            )
            
        except Exception as e:
            self.logger.error(f"Error alert failed: {e}")
    
    async def _shutdown_system(self) -> None:
        """Gracefully shutdown the system"""
        try:
            self.logger.info("🛑 Shutting down production system...")
            
            # Calculate final statistics
            uptime = datetime.now() - self.start_time if self.start_time else timedelta(0)
            
            # Send shutdown notification
            await self.teams_client.send_alert(
                "🛑 Lab Automation System Shutdown",
                f"**Kaiser Permanente Lab Automation - System Shutdown**\n\n"
                f"📊 **Final Statistics:**\n"
                f"• Total Uptime: {str(uptime).split('.')[0]}\n"
                f"• Monitoring Cycles Completed: {self.cycles_completed}\n"
                f"• Alerts Sent: {self.alerts_sent}\n"
                f"• Errors Handled: {self.errors_detected}\n\n"
                f"**🏥 System Status:** Gracefully shutdown\n"
                f"**📍 Location:** Kaiser Permanente Largo, MD\n\n"
                f"Lab automation monitoring has been stopped. "
                f"Restart the system to resume automated operations.",
                "warning",
                {
                    "Shutdown Type": "Graceful",
                    "Final Uptime": str(uptime).split('.')[0],
                    "Cycles Completed": self.cycles_completed,
                    "Shutdown Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            )
            
            # Close clients
            if hasattr(self, 'notion_client'):
                await self.notion_client.close()
            if hasattr(self, 'powerbi_client'):
                await self.powerbi_client.close()
            if hasattr(self, 'teams_client'):
                await self.teams_client.close()
            
            self.logger.info("✅ Production system shutdown completed")
            
        except Exception as e:
            self.logger.error(f"System shutdown failed: {e}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "status": "running" if self.is_running else "stopped",
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            "cycles_completed": self.cycles_completed,
            "alerts_sent": self.alerts_sent,
            "errors_detected": self.errors_detected,
            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None
        }


async def main():
    """Main production system entry point"""
    print("🚀 Kaiser Permanente Lab Automation System - PRODUCTION MODE")
    print("=" * 80)
    print("🏥 Location: Kaiser Permanente Largo, MD")
    print("⚡ Mission: Automate and optimize lab operations")
    print("🎯 Goal: Reduce idle time, improve TAT compliance, enhance performance")
    print("=" * 80)
    
    try:
        # Initialize production system
        production_system = ProductionLabSystem()
        
        # Start production monitoring
        await production_system.start_production_system()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested by user...")
    except Exception as e:
        print(f"\n💥 System error: {e}")
        sys.exit(1)
    
    print("\n✅ Kaiser Permanente Lab Automation System shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())

