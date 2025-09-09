"""
Kaiser Permanente Lab Automation System
Enhanced Power BI Integration Client

Uses direct push URLs for optimal performance and compatibility
with your specific Power BI dataset schemas.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp
import json

from utils.audit_logger import AuditLogger


class EnhancedPowerBIClient:
    """
    Enhanced Power BI client using direct push URLs
    for optimal integration with Kaiser Permanente datasets.
    """
    
    def __init__(self, monitor_push_url: str, metrics_push_url: str):
        """
        Initialize enhanced Power BI client
        
        Args:
            monitor_push_url: Direct push URL for monitor dataset
            metrics_push_url: Direct push URL for metrics dataset
        """
        self.monitor_push_url = monitor_push_url
        self.metrics_push_url = metrics_push_url
        self.logger = logging.getLogger('enhanced_powerbi_client')
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
    
    async def _push_data(self, push_url: str, data: List[Dict[str, Any]], dataset_name: str) -> bool:
        """
        Push data directly to Power BI using push URL
        
        Args:
            push_url: Direct push URL for the dataset
            data: Data rows to push
            dataset_name: Name of dataset for logging
            
        Returns:
            Success status
        """
        if not data:
            self.logger.debug(f"No data to push to {dataset_name}")
            return True
        
        session = await self._ensure_session()
        
        try:
            # Prepare data payload
            payload = {"rows": data}
            
            async with session.post(
                url=push_url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    self.logger.info(f"Successfully pushed {len(data)} rows to {dataset_name}")
                    
                    # Log successful API call
                    self.audit_logger.log_api_call(
                        service="powerbi_enhanced",
                        method="POST",
                        endpoint=dataset_name,
                        status_code=response.status,
                        data_count=len(data)
                    )
                    
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(
                        f"Power BI push failed for {dataset_name}: "
                        f"Status {response.status}, Response: {error_text}"
                    )
                    return False
                    
        except Exception as e:
            self.logger.error(f"Failed to push data to {dataset_name}: {e}")
            return False
    
    async def update_performance_monitor(self, performance_data: List[Dict[str, Any]]) -> bool:
        """
        Update performance monitor dataset
        
        Args:
            performance_data: List of performance records
            
        Returns:
            Success status
        """
        try:
            # Transform data for Power BI monitor schema
            transformed_data = []
            
            for record in performance_data:
                # Create row compatible with your Power BI schema
                row = {
                    "Timestamp": datetime.now().isoformat(),
                    "StaffMember": record.get("staff_member", ""),
                    "Date": record.get("date", datetime.now().date().isoformat()),
                    "Shift": record.get("shift", ""),
                    "SamplesProcessed": record.get("samples_processed", 0),
                    "ErrorCount": record.get("error_count", 0),
                    "BreakTimeMinutes": record.get("break_time_minutes", 0),
                    "QCCompletionPercent": record.get("qc_completion_percent", 0),
                    "TATTargetMet": record.get("tat_target_met", False),
                    "PerformanceScore": record.get("performance_score", 0),
                    "Status": record.get("status", ""),
                    "Supervisor": record.get("supervisor", ""),
                    "Notes": record.get("notes", "")[:100]  # Limit length
                }
                transformed_data.append(row)
            
            # Push to Power BI
            success = await self._push_data(
                self.monitor_push_url,
                transformed_data,
                "Performance Monitor"
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update performance monitor: {e}")
            return False
    
    async def update_performance_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """
        Update performance metrics dataset
        
        Args:
            metrics_data: Metrics data
            
        Returns:
            Success status
        """
        try:
            # Create metrics row
            row = {
                "Timestamp": datetime.now().isoformat(),
                "TotalSamplesProcessed": metrics_data.get("total_samples", 0),
                "TotalErrors": metrics_data.get("total_errors", 0),
                "ErrorRate": metrics_data.get("error_rate", 0),
                "TATCompliance": metrics_data.get("tat_compliance", 0),
                "AveragePerformanceScore": metrics_data.get("avg_performance_score", 0),
                "ActiveStaffCount": metrics_data.get("active_staff", 0),
                "OpenIncidents": metrics_data.get("open_incidents", 0),
                "CriticalIncidents": metrics_data.get("critical_incidents", 0),
                "EquipmentStatus": metrics_data.get("equipment_status", "Unknown"),
                "QCStatus": metrics_data.get("qc_status", "Unknown"),
                "SystemHealth": metrics_data.get("system_health", "Normal")
            }
            
            # Push to Power BI
            success = await self._push_data(
                self.metrics_push_url,
                [row],
                "Performance Metrics"
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update performance metrics: {e}")
            return False
    
    async def update_incident_data(self, incident_data: List[Dict[str, Any]]) -> bool:
        """
        Update incident data in metrics dataset
        
        Args:
            incident_data: List of incident records
            
        Returns:
            Success status
        """
        try:
            # Transform incident data for metrics
            transformed_data = []
            
            for incident in incident_data:
                row = {
                    "Timestamp": datetime.now().isoformat(),
                    "IncidentID": incident.get("incident_id", ""),
                    "IncidentType": incident.get("incident_type", ""),
                    "Severity": incident.get("severity", ""),
                    "Impact": incident.get("impact", ""),
                    "Status": incident.get("status", ""),
                    "StaffMember": incident.get("staff_member", ""),
                    "Description": incident.get("description", "")[:100],
                    "RootCause": incident.get("root_cause", "")[:100],
                    "CorrectiveAction": incident.get("corrective_action", "")[:100]
                }
                transformed_data.append(row)
            
            # Push to Power BI metrics dataset
            success = await self._push_data(
                self.metrics_push_url,
                transformed_data,
                "Incident Data"
            )
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update incident data: {e}")
            return False
    
    async def update_operational_dashboard(self, operational_data: Dict[str, Any]) -> bool:
        """
        Update operational dashboard with real-time data
        
        Args:
            operational_data: Real-time operational metrics
            
        Returns:
            Success status
        """
        try:
            # Create comprehensive operational row
            row = {
                "Timestamp": datetime.now().isoformat(),
                "Date": datetime.now().date().isoformat(),
                "Time": datetime.now().time().strftime("%H:%M:%S"),
                "TotalSamplesProcessed": operational_data.get("total_samples_today", 0),
                "TotalErrors": operational_data.get("total_errors", 0),
                "ErrorRate": operational_data.get("error_rate", 0),
                "TATCompliance": operational_data.get("tat_compliance", 0),
                "AveragePerformanceScore": operational_data.get("avg_performance_score", 0),
                "ActiveStaffCount": operational_data.get("active_staff", 0),
                "OpenIncidents": operational_data.get("open_incidents", 0),
                "CriticalIncidents": operational_data.get("critical_incidents", 0),
                "EquipmentStatus": operational_data.get("equipment_status", "Normal"),
                "QCStatus": operational_data.get("qc_status", "Normal"),
                "SystemHealth": "Operational",
                "LastUpdated": datetime.now().isoformat()
            }
            
            # Push to both datasets for comprehensive coverage
            monitor_success = await self._push_data(
                self.monitor_push_url,
                [row],
                "Operational Monitor"
            )
            
            metrics_success = await self._push_data(
                self.metrics_push_url,
                [row],
                "Operational Metrics"
            )
            
            return monitor_success or metrics_success
            
        except Exception as e:
            self.logger.error(f"Failed to update operational dashboard: {e}")
            return False
    
    async def send_heartbeat(self) -> bool:
        """
        Send system heartbeat to Power BI
        
        Returns:
            Success status
        """
        try:
            heartbeat_data = {
                "Timestamp": datetime.now().isoformat(),
                "SystemStatus": "Online",
                "HeartbeatType": "System Health Check",
                "Value": 1,
                "Message": "Kaiser Permanente Lab Automation System Active"
            }
            
            success = await self._push_data(
                self.metrics_push_url,
                [heartbeat_data],
                "System Heartbeat"
            )
            
            if success:
                self.logger.debug("System heartbeat sent to Power BI")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to send heartbeat: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test Power BI connection with both datasets
        
        Returns:
            Connection status
        """
        try:
            # Test data for both datasets
            test_data = {
                "Timestamp": datetime.now().isoformat(),
                "TestField": "Connection Test",
                "Value": 1,
                "Status": "Testing"
            }
            
            # Test monitor dataset
            monitor_success = await self._push_data(
                self.monitor_push_url,
                [test_data],
                "Monitor Test"
            )
            
            # Test metrics dataset
            metrics_success = await self._push_data(
                self.metrics_push_url,
                [test_data],
                "Metrics Test"
            )
            
            overall_success = monitor_success or metrics_success
            
            if overall_success:
                self.logger.info("Power BI connection test successful")
            else:
                self.logger.error("Power BI connection test failed")
            
            return overall_success
            
        except Exception as e:
            self.logger.error(f"Power BI connection test error: {e}")
            return False
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()


async def create_enhanced_powerbi_client() -> EnhancedPowerBIClient:
    """
    Factory function to create enhanced Power BI client from environment
    
    Returns:
        Configured enhanced Power BI client
    """
    import os
    
    monitor_push_url = os.getenv('POWERBI_MONITOR_PUSH_URL')
    metrics_push_url = os.getenv('POWERBI_METRICS_PUSH_URL')
    
    if not monitor_push_url or not metrics_push_url:
        raise ValueError("Power BI push URLs not configured")
    
    return EnhancedPowerBIClient(monitor_push_url, metrics_push_url)

