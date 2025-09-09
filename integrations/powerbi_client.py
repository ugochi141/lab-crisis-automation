"""
Kaiser Permanente Lab Automation System
Power BI Integration Client

Handles real-time data streaming to Power BI datasets for
dashboard updates and performance visualization.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
import aiohttp
import json

from config.config_manager import PowerBIConfig
from utils.audit_logger import AuditLogger


class PowerBIClient:
    """
    Async client for Power BI REST API integration with
    real-time data streaming capabilities.
    """
    
    def __init__(self, config: PowerBIConfig):
        """
        Initialize Power BI client
        
        Args:
            config: Power BI configuration settings
        """
        self.config = config
        self.base_url = "https://api.powerbi.com/beta"
        self.logger = logging.getLogger('powerbi_client')
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
    
    def _get_dataset_url(self, dataset_id: str, api_key: str) -> str:
        """
        Construct dataset streaming URL
        
        Args:
            dataset_id: Power BI dataset ID
            api_key: Dataset API key
            
        Returns:
            Complete streaming URL
        """
        return (
            f"{self.base_url}/{self.config.workspace_id}/datasets/{dataset_id}/rows"
            f"?experience=power-bi&key={api_key}"
        )
    
    async def _stream_data(self, dataset_id: str, api_key: str, data: List[Dict[str, Any]]) -> bool:
        """
        Stream data to Power BI dataset
        
        Args:
            dataset_id: Target dataset ID
            api_key: Dataset API key
            data: Data rows to stream
            
        Returns:
            Success status
        """
        if not data:
            self.logger.debug("No data to stream")
            return True
        
        session = await self._ensure_session()
        url = self._get_dataset_url(dataset_id, api_key)
        
        try:
            # Prepare data payload
            payload = {"rows": data}
            
            async with session.post(
                url=url,
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    self.logger.info(f"Successfully streamed {len(data)} rows to dataset {dataset_id}")
                    
                    # Log successful API call
                    self.audit_logger.log_api_call(
                        service="powerbi",
                        method="POST",
                        endpoint=f"datasets/{dataset_id}/rows",
                        status_code=response.status,
                        data_count=len(data)
                    )
                    
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(
                        f"Power BI streaming failed for dataset {dataset_id}: "
                        f"Status {response.status}, Response: {error_text}"
                    )
                    return False
                    
        except Exception as e:
            self.logger.error(f"Failed to stream data to Power BI dataset {dataset_id}: {e}")
            return False
    
    async def update_performance_dataset(self, performance_data: List[Dict[str, Any]]) -> bool:
        """
        Update performance metrics dataset
        
        Args:
            performance_data: List of performance records
            
        Returns:
            Success status
        """
        try:
            # Transform data for Power BI schema
            transformed_data = []
            
            for record in performance_data:
                # Convert to Power BI compatible format
                row = {
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
                    "Notes": record.get("notes", ""),
                    "LastUpdated": datetime.now().isoformat()
                }
                transformed_data.append(row)
            
            # Stream to Power BI
            success = await self._stream_data(
                self.config.performance_dataset_id,
                self.config.performance_api_key,
                transformed_data
            )
            
            if success:
                self.logger.info(f"Updated performance dataset with {len(transformed_data)} records")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update performance dataset: {e}")
            return False
    
    async def update_incidents_dataset(self, incident_data: List[Dict[str, Any]]) -> bool:
        """
        Update incidents dataset
        
        Args:
            incident_data: List of incident records
            
        Returns:
            Success status
        """
        try:
            # Transform data for Power BI schema
            transformed_data = []
            
            for record in incident_data:
                # Convert to Power BI compatible format
                row = {
                    "IncidentID": record.get("incident_id", ""),
                    "DateTime": record.get("date_time", datetime.now().isoformat()),
                    "StaffMember": record.get("staff_member", ""),
                    "IncidentType": record.get("incident_type", ""),
                    "Severity": record.get("severity", ""),
                    "Impact": record.get("impact", ""),
                    "Status": record.get("status", ""),
                    "Description": record.get("description", ""),
                    "RootCause": record.get("root_cause", ""),
                    "CorrectiveAction": record.get("corrective_action", ""),
                    "FollowUpDate": record.get("follow_up_date", ""),
                    "PatternCount": record.get("pattern_count", 0),
                    "LastUpdated": datetime.now().isoformat()
                }
                transformed_data.append(row)
            
            # Stream to Power BI
            success = await self._stream_data(
                self.config.operations_dataset_id,
                self.config.operations_api_key,
                transformed_data
            )
            
            if success:
                self.logger.info(f"Updated incidents dataset with {len(transformed_data)} records")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update incidents dataset: {e}")
            return False
    
    async def update_real_time_metrics(self, metrics: Dict[str, Any]) -> bool:
        """
        Update real-time operational metrics
        
        Args:
            metrics: Real-time metrics data
            
        Returns:
            Success status
        """
        try:
            # Prepare real-time metrics row
            row = {
                "Timestamp": datetime.now().isoformat(),
                "TotalSamplesProcessed": metrics.get("total_samples", 0),
                "TotalErrors": metrics.get("total_errors", 0),
                "ErrorRate": metrics.get("error_rate", 0),
                "TATCompliance": metrics.get("tat_compliance", 0),
                "AveragePerformanceScore": metrics.get("avg_performance_score", 0),
                "ActiveStaffCount": metrics.get("active_staff", 0),
                "OpenIncidents": metrics.get("open_incidents", 0),
                "CriticalIncidents": metrics.get("critical_incidents", 0),
                "QueueWaitTime": metrics.get("queue_wait_time", 0),
                "EquipmentStatus": metrics.get("equipment_status", "Unknown"),
                "QCStatus": metrics.get("qc_status", "Unknown")
            }
            
            # Stream to performance dataset (real-time table)
            success = await self._stream_data(
                self.config.performance_dataset_id,
                self.config.performance_api_key,
                [row]
            )
            
            if success:
                self.logger.debug("Updated real-time metrics")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to update real-time metrics: {e}")
            return False
    
    async def update_queue_metrics(self, queue_data: Dict[str, Any]) -> bool:
        """
        Update queue management metrics
        
        Args:
            queue_data: Queue status and metrics
            
        Returns:
            Success status
        """
        try:
            if not queue_data:
                return True
            
            # Transform queue data
            rows = []
            
            # Overall queue statistics
            if "overall_stats" in queue_data:
                stats = queue_data["overall_stats"]
                row = {
                    "Timestamp": datetime.now().isoformat(),
                    "QueueType": "Overall",
                    "WaitingCount": stats.get("waiting_count", 0),
                    "AverageWaitTime": stats.get("average_wait_time", 0),
                    "MaxWaitTime": stats.get("max_wait_time", 0),
                    "ServedToday": stats.get("served_today", 0),
                    "ServiceRate": stats.get("service_rate", 0)
                }
                rows.append(row)
            
            # Individual station data
            if "stations" in queue_data:
                for station_id, station_data in queue_data["stations"].items():
                    row = {
                        "Timestamp": datetime.now().isoformat(),
                        "QueueType": f"Station_{station_id}",
                        "WaitingCount": station_data.get("waiting_count", 0),
                        "AverageWaitTime": station_data.get("average_wait_time", 0),
                        "MaxWaitTime": station_data.get("max_wait_time", 0),
                        "ServedToday": station_data.get("served_today", 0),
                        "ServiceRate": station_data.get("service_rate", 0),
                        "StaffMember": station_data.get("staff_member", ""),
                        "Status": station_data.get("status", "Unknown")
                    }
                    rows.append(row)
            
            if rows:
                success = await self._stream_data(
                    self.config.operations_dataset_id,
                    self.config.operations_api_key,
                    rows
                )
                
                if success:
                    self.logger.info(f"Updated queue metrics with {len(rows)} records")
                
                return success
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update queue metrics: {e}")
            return False
    
    async def update_equipment_status(self, equipment_data: Dict[str, Any]) -> bool:
        """
        Update equipment status metrics
        
        Args:
            equipment_data: Equipment status information
            
        Returns:
            Success status
        """
        try:
            if not equipment_data:
                return True
            
            rows = []
            timestamp = datetime.now().isoformat()
            
            # Process each equipment system
            for system_name, system_data in equipment_data.items():
                if isinstance(system_data, dict):
                    for equipment_id, equipment_info in system_data.items():
                        row = {
                            "Timestamp": timestamp,
                            "System": system_name,
                            "EquipmentID": equipment_id,
                            "Status": equipment_info.get("status", "Unknown"),
                            "LastMaintenance": equipment_info.get("last_maintenance", ""),
                            "NextMaintenance": equipment_info.get("next_maintenance", ""),
                            "ErrorCount": equipment_info.get("error_count", 0),
                            "UptimePercent": equipment_info.get("uptime_percent", 0),
                            "Temperature": equipment_info.get("temperature", 0),
                            "Alerts": equipment_info.get("alerts", "")
                        }
                        rows.append(row)
            
            if rows:
                success = await self._stream_data(
                    self.config.operations_dataset_id,
                    self.config.operations_api_key,
                    rows
                )
                
                if success:
                    self.logger.info(f"Updated equipment status with {len(rows)} records")
                
                return success
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update equipment status: {e}")
            return False
    
    async def clear_dataset(self, dataset_type: str = "performance") -> bool:
        """
        Clear dataset rows (for maintenance/reset)
        
        Args:
            dataset_type: Type of dataset to clear ('performance' or 'operations')
            
        Returns:
            Success status
        """
        try:
            if dataset_type == "performance":
                dataset_id = self.config.performance_dataset_id
                api_key = self.config.performance_api_key
            elif dataset_type == "operations":
                dataset_id = self.config.operations_dataset_id
                api_key = self.config.operations_api_key
            else:
                raise ValueError(f"Invalid dataset type: {dataset_type}")
            
            session = await self._ensure_session()
            url = f"{self.base_url}/{self.config.workspace_id}/datasets/{dataset_id}/rows"
            
            async with session.delete(url) as response:
                if response.status == 200:
                    self.logger.info(f"Successfully cleared {dataset_type} dataset")
                    
                    # Log the action
                    self.audit_logger.log_api_call(
                        service="powerbi",
                        method="DELETE",
                        endpoint=f"datasets/{dataset_id}/rows",
                        status_code=response.status
                    )
                    
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to clear dataset: Status {response.status}, Response: {error_text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Failed to clear dataset {dataset_type}: {e}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Test Power BI API connection
        
        Returns:
            Connection status
        """
        try:
            # Test with a minimal data row
            test_data = [{
                "TestField": "Connection Test",
                "Timestamp": datetime.now().isoformat()
            }]
            
            success = await self._stream_data(
                self.config.performance_dataset_id,
                self.config.performance_api_key,
                test_data
            )
            
            if success:
                self.logger.info("Power BI connection test successful")
            else:
                self.logger.error("Power BI connection test failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Power BI connection test error: {e}")
            return False
    
    async def close(self):
        """Close the client session"""
        if self.session:
            await self.session.close()
