"""
Kaiser Permanente Lab Automation System
Core Automation Engine

Main orchestration module for lab operations automation
with HIPAA compliance, error handling, and audit logging.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path

from config.config_manager import ConfigManager
from integrations.notion_client import NotionClient
from integrations.powerbi_client import PowerBIClient
from integrations.teams_client import TeamsClient
from integrations.epic_beaker_client import EpicBeakerClient
from integrations.qmatic_api import QmaticConnector as QmaticClient
from integrations.biorad_client import BioRadClient
from integrations.hrconnect_client import HRConnectClient
from utils.audit_logger import AuditLogger
from utils.alert_manager import AlertManager
from utils.performance_calculator import PerformanceCalculator


@dataclass
class LabMetrics:
    """Lab performance metrics data structure"""
    timestamp: datetime
    staff_member: str
    shift: str
    samples_processed: int
    error_count: int
    break_time_minutes: int
    qc_completion_percent: float
    tat_target_met: bool
    performance_score: float
    supervisor: str
    notes: str = ""


@dataclass
class IncidentData:
    """Incident tracking data structure"""
    incident_id: str
    timestamp: datetime
    staff_member: str
    incident_type: str
    severity: str
    impact: str
    description: str
    root_cause: str = ""
    corrective_action: str = ""
    status: str = "Open"


class LabAutomationCore:
    """
    Core lab automation engine that orchestrates all integrations
    and provides real-time monitoring and alerting.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the lab automation core system
        
        Args:
            config_file: Path to configuration file
        """
        self.config_manager = ConfigManager(config_file)
        self.audit_logger = AuditLogger()
        self.logger = self._setup_logging()
        
        # Initialize clients
        self._initialize_clients()
        
        # Performance tracking
        self.performance_calculator = PerformanceCalculator()
        self.alert_manager = AlertManager(
            self.teams_client,
            self.config_manager.get_alert_thresholds()
        )
        
        # Operational state
        self.is_running = False
        self.last_alert_times: Dict[str, datetime] = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging system"""
        logger = logging.getLogger('lab_automation_core')
        
        # Create logs directory
        Path('logs').mkdir(exist_ok=True)
        
        # Configure logging level
        log_level = getattr(logging, self.config_manager._get_optional_env('LOG_LEVEL', 'INFO'))
        logger.setLevel(log_level)
        
        # File handler for general logs
        log_file = self.config_manager._get_optional_env('LOG_FILE_PATH', 'logs/lab_automation.log')
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler for real-time monitoring
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _initialize_clients(self) -> None:
        """Initialize all integration clients with health checks and auto-retry"""
        def safe_init(client_cls, config_func, name):
            for attempt in range(3):
                try:
                    client = client_cls(config_func())
                    self.logger.info(f"{name} client initialized (attempt {attempt+1})")
                    return client
                except Exception as e:
                    self.logger.warning(f"{name} client init failed (attempt {attempt+1}): {e}")
                    asyncio.sleep(1)
            self.logger.error(f"{name} client could not be initialized after 3 attempts")
            return None

        # Core integrations (required)
        self.notion_client = safe_init(NotionClient, self.config_manager.get_notion_config, "Notion")
        self.powerbi_client = safe_init(PowerBIClient, self.config_manager.get_powerbi_config, "PowerBI")
        self.teams_client = safe_init(TeamsClient, self.config_manager.get_teams_config, "Teams")

        # Optional integrations (may not be configured yet)
        self.epic_client = safe_init(EpicBeakerClient, self.config_manager.get_epic_beaker_config, "Epic Beaker")
        self.qmatic_client = safe_init(QmaticClient, self.config_manager.get_qmatic_config, "Qmatic")
        self.biorad_client = safe_init(BioRadClient, self.config_manager.get_biorad_config, "Bio-Rad Unity")
        self.hrconnect_client = safe_init(HRConnectClient, self.config_manager.get_hrconnect_config, "HR Connect")

        self.logger.info("Integration clients initialized with health checks.")

    def reload_clients(self):
        """Hot-reload all integration clients (e.g., after config change)"""
        self.logger.info("Reloading integration clients...")
        self._initialize_clients()
        self.logger.info("Integration clients reloaded.")
    
    async def start_monitoring(self) -> None:
        """Start the continuous monitoring loop with error resilience and auto-reload"""
        if self.is_running:
            self.logger.warning("Monitoring is already running")
            return

        self.is_running = True
        self.logger.info("Starting lab automation monitoring")

        # Send startup notification
        await self.teams_client.send_alert(
            "🚀 Lab Automation System Started",
            "Lab automation monitoring is now active.",
            "info"
        )

        operational_settings = self.config_manager.get_operational_settings()
        error_count = 0
        try:
            while self.is_running:
                try:
                    await self._monitoring_cycle()
                    error_count = 0  # Reset on success
                except Exception as e:
                    error_count += 1
                    self.logger.error(f"Monitoring cycle error (attempt {error_count}): {e}")
                    if error_count >= 3:
                        self.logger.error("Too many consecutive errors, reloading clients...")
                        self.reload_clients()
                        error_count = 0
                    await asyncio.sleep(5)
                await asyncio.sleep(operational_settings.monitoring_interval_seconds)
        except Exception as e:
            self.logger.error(f"Monitoring loop fatal error: {e}")
            await self.teams_client.send_alert(
                "🚨 System Error",
                f"Lab automation monitoring encountered an error: {e}",
                "critical"
            )
            raise
        finally:
            self.is_running = False
            self.logger.info("Lab automation monitoring stopped")
    
    async def stop_monitoring(self) -> None:
        """Stop the monitoring loop"""
        self.is_running = False
        self.logger.info("Stopping lab automation monitoring")
        
        await self.teams_client.send_alert(
            "🛑 Lab Automation System Stopped",
            "Lab automation monitoring has been stopped.",
            "warning"
        )
    
    async def _monitoring_cycle(self) -> None:
        """Execute one complete monitoring cycle"""
        try:
            self.logger.debug("Starting monitoring cycle")
            
            # Collect data from all sources
            tasks = [
                self._collect_performance_data(),
                self._collect_incident_data(),
                self._collect_queue_data(),
                self._collect_qc_data(),
                self._collect_equipment_status()
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results and handle any exceptions
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.logger.error(f"Task {i} failed: {result}")
            
            # Analyze performance and generate alerts
            await self._analyze_performance()
            
            # Update dashboards
            await self._update_dashboards()
            
            self.logger.debug("Monitoring cycle completed")
            
        except Exception as e:
            self.logger.error(f"Monitoring cycle error: {e}")
            raise
    
    async def _collect_performance_data(self) -> List[LabMetrics]:
        """Collect performance data from all sources"""
        try:
            # Get current performance data from Notion
            performance_data = await self.notion_client.get_performance_data()
            
            # Enhance with real-time data from lab systems
            if self.epic_client:
                epic_data = await self.epic_client.get_current_metrics()
                performance_data = self._merge_epic_data(performance_data, epic_data)
            
            return performance_data
            
        except Exception as e:
            self.logger.error(f"Failed to collect performance data: {e}")
            return []
    
    async def _collect_incident_data(self) -> List[IncidentData]:
        """Collect incident data from tracking systems"""
        try:
            # Get incidents from Notion
            incidents = await self.notion_client.get_open_incidents()
            
            # Check for new incidents from lab systems
            if self.epic_client:
                epic_incidents = await self.epic_client.get_new_incidents()
                incidents.extend(epic_incidents)
            
            return incidents
            
        except Exception as e:
            self.logger.error(f"Failed to collect incident data: {e}")
            return []
    
    async def _collect_queue_data(self) -> Dict[str, Any]:
        """Collect queue management data"""
        try:
            if not self.qmatic_client:
                return {}
            
            queue_data = await self.qmatic_client.get_queue_status()
            return queue_data
            
        except Exception as e:
            self.logger.error(f"Failed to collect queue data: {e}")
            return {}
    
    async def _collect_qc_data(self) -> Dict[str, Any]:
        """Collect QC data from Bio-Rad Unity"""
        try:
            if not self.biorad_client:
                return {}
            
            qc_data = await self.biorad_client.get_qc_status()
            return qc_data
            
        except Exception as e:
            self.logger.error(f"Failed to collect QC data: {e}")
            return {}
    
    async def _collect_equipment_status(self) -> Dict[str, Any]:
        """Collect equipment status from all systems"""
        try:
            equipment_status = {}
            
            if self.epic_client:
                equipment_status['epic'] = await self.epic_client.get_equipment_status()
            
            if self.biorad_client:
                equipment_status['biorad'] = await self.biorad_client.get_instrument_status()
            
            return equipment_status
            
        except Exception as e:
            self.logger.error(f"Failed to collect equipment status: {e}")
            return {}
    
    async def _analyze_performance(self) -> None:
        """Analyze performance data and generate alerts"""
        try:
            # Get current performance metrics
            performance_data = await self._collect_performance_data()
            
            if not performance_data:
                return
            
            # Analyze each staff member's performance
            for metrics in performance_data:
                await self._check_performance_thresholds(metrics)
            
            # Generate summary alerts
            await self._generate_summary_alerts(performance_data)
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
    
    async def _check_performance_thresholds(self, metrics: LabMetrics) -> None:
        """Check individual performance against thresholds"""
        thresholds = self.config_manager.get_alert_thresholds()
        alerts = []
        
        # Check TAT compliance
        if not metrics.tat_target_met:
            alerts.append(f"TAT target missed")
        
        # Check performance score
        if metrics.performance_score < thresholds.performance_score_threshold:
            alerts.append(f"Performance score low: {metrics.performance_score}")
        
        # Check error rate
        if metrics.samples_processed > 0:
            error_rate = (metrics.error_count / metrics.samples_processed) * 100
            if error_rate > thresholds.error_rate_threshold:
                alerts.append(f"Error rate high: {error_rate:.1f}%")
        
        # Check break time
        if metrics.break_time_minutes > thresholds.break_time_threshold_minutes:
            alerts.append(f"Break time exceeded: {metrics.break_time_minutes} minutes")
        
        # Check QC completion
        if metrics.qc_completion_percent < thresholds.qc_completion_threshold:
            alerts.append(f"QC completion low: {metrics.qc_completion_percent}%")
        
        # Send alerts if any issues found
        if alerts:
            await self._send_performance_alert(metrics.staff_member, alerts)
    
    async def _send_performance_alert(self, staff_member: str, issues: List[str]) -> None:
        """Send performance alert with cooldown"""
        alert_key = f"performance_{staff_member}"
        now = datetime.now()
        
        # Check cooldown
        if alert_key in self.last_alert_times:
            cooldown_minutes = self.config_manager.get_operational_settings().alert_cooldown_minutes
            if (now - self.last_alert_times[alert_key]).total_seconds() < (cooldown_minutes * 60):
                return
        
        # Send alert
        await self.alert_manager.send_performance_alert(staff_member, issues)
        self.last_alert_times[alert_key] = now
        
        # Log to audit trail
        self.audit_logger.log_alert(
            alert_type="performance",
            staff_member=staff_member,
            details={"issues": issues}
        )
    
    async def _generate_summary_alerts(self, performance_data: List[LabMetrics]) -> None:
        """Generate summary alerts for overall lab performance"""
        if not performance_data:
            return
        
        # Calculate summary statistics
        total_samples = sum(m.samples_processed for m in performance_data)
        total_errors = sum(m.error_count for m in performance_data)
        tat_compliance = sum(1 for m in performance_data if m.tat_target_met) / len(performance_data) * 100
        avg_performance = sum(m.performance_score for m in performance_data) / len(performance_data)
        
        # Check for summary alerts
        thresholds = self.config_manager.get_alert_thresholds()
        
        if tat_compliance < 85:  # Target TAT compliance
            await self.teams_client.send_alert(
                "📊 TAT Compliance Alert",
                f"Current TAT compliance: {tat_compliance:.1f}% (Target: 85%)",
                "warning"
            )
        
        if total_samples > 0:
            error_rate = (total_errors / total_samples) * 100
            if error_rate > thresholds.error_rate_threshold:
                await self.teams_client.send_alert(
                    "⚠️ Error Rate Alert",
                    f"Current error rate: {error_rate:.1f}% (Threshold: {thresholds.error_rate_threshold}%)",
                    "warning"
                )
    
    async def _update_dashboards(self) -> None:
        """Update Power BI dashboards with latest data"""
        try:
            # Get latest data
            performance_data = await self._collect_performance_data()
            incident_data = await self._collect_incident_data()
            
            # Update Power BI datasets
            if performance_data:
                await self.powerbi_client.update_performance_dataset(performance_data)
            
            if incident_data:
                await self.powerbi_client.update_incidents_dataset(incident_data)
            
            self.logger.debug("Dashboards updated successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to update dashboards: {e}")
    
    def _merge_epic_data(self, notion_data: List[LabMetrics], epic_data: Dict[str, Any]) -> List[LabMetrics]:
        """Merge Epic Beaker data with Notion performance data"""
        # Implementation depends on Epic Beaker API structure
        # This is a placeholder for the actual merging logic
        return notion_data
    
    async def create_incident(self, incident_data: IncidentData) -> str:
        """
        Create a new incident in the tracking system
        
        Args:
            incident_data: Incident information
            
        Returns:
            Created incident ID
        """
        try:
            # Create incident in Notion
            incident_id = await self.notion_client.create_incident(incident_data)
            
            # Send immediate alert for critical incidents
            if incident_data.severity == "Critical":
                await self.alert_manager.send_critical_incident_alert(incident_data)
            
            # Log to audit trail
            self.audit_logger.log_incident_creation(incident_data)
            
            self.logger.info(f"Incident {incident_id} created successfully")
            return incident_id
            
        except Exception as e:
            self.logger.error(f"Failed to create incident: {e}")
            raise
    
    async def update_performance_metrics(self, metrics: LabMetrics) -> None:
        """
        Update performance metrics in all systems
        
        Args:
            metrics: Performance metrics to update
        """
        try:
            # Update Notion database
            await self.notion_client.update_performance_metrics(metrics)
            
            # Update Power BI dataset
            await self.powerbi_client.update_performance_dataset([metrics])
            
            # Check for alerts
            await self._check_performance_thresholds(metrics)
            
            # Log to audit trail
            self.audit_logger.log_performance_update(metrics)
            
            self.logger.debug(f"Performance metrics updated for {metrics.staff_member}")
            
        except Exception as e:
            self.logger.error(f"Failed to update performance metrics: {e}")
            raise
    
    async def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard data
        
        Returns:
            Dictionary containing all dashboard data
        """
        try:
            # Collect all current data
            performance_data = await self._collect_performance_data()
            incident_data = await self._collect_incident_data()
            queue_data = await self._collect_queue_data()
            qc_data = await self._collect_qc_data()
            equipment_status = await self._collect_equipment_status()
            
            # Calculate summary statistics
            dashboard_data = {
                'timestamp': datetime.now().isoformat(),
                'performance': {
                    'staff_count': len(performance_data),
                    'total_samples': sum(m.samples_processed for m in performance_data),
                    'total_errors': sum(m.error_count for m in performance_data),
                    'avg_performance_score': sum(m.performance_score for m in performance_data) / len(performance_data) if performance_data else 0,
                    'tat_compliance': sum(1 for m in performance_data if m.tat_target_met) / len(performance_data) * 100 if performance_data else 0
                },
                'incidents': {
                    'total_open': len([i for i in incident_data if i.status == 'Open']),
                    'critical_count': len([i for i in incident_data if i.severity == 'Critical']),
                    'recent_incidents': incident_data[:5]  # Last 5 incidents
                },
                'queue_status': queue_data,
                'qc_status': qc_data,
                'equipment_status': equipment_status
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Failed to get dashboard data: {e}")
            raise


async def main():
    """Main entry point for lab automation system"""
    try:
        # Initialize the automation system
        lab_automation = LabAutomationCore()
        
        # Start monitoring
        await lab_automation.start_monitoring()
        
    except KeyboardInterrupt:
        print("\nShutting down lab automation system...")
        if 'lab_automation' in locals():
            await lab_automation.stop_monitoring()
    except Exception as e:
        print(f"Fatal error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

