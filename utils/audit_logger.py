"""
Kaiser Permanente Lab Automation System
HIPAA-Compliant Audit Logger

Provides comprehensive audit logging for all system activities
with HIPAA compliance and security features.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import hashlib
import os


class AuditLogger:
    """
    HIPAA-compliant audit logger that tracks all system activities
    with secure logging and data integrity verification.
    """
    
    def __init__(self, audit_file: Optional[str] = None):
        """
        Initialize audit logger
        
        Args:
            audit_file: Path to audit log file
        """
        self.audit_file = audit_file or "logs/audit_trail.log"
        self.logger = self._setup_audit_logger()
        self._ensure_log_directory()
    
    def _setup_audit_logger(self) -> logging.Logger:
        """Setup dedicated audit logger with security features"""
        audit_logger = logging.getLogger('hipaa_audit')
        audit_logger.setLevel(logging.INFO)
        
        # Ensure logs directory exists
        Path(self.audit_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Create secure file handler
        file_handler = logging.FileHandler(
            self.audit_file,
            mode='a',
            encoding='utf-8'
        )
        
        # HIPAA-compliant audit format
        formatter = logging.Formatter(
            '%(asctime)s|%(levelname)s|AUDIT|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        audit_logger.addHandler(file_handler)
        
        # Prevent propagation to root logger
        audit_logger.propagate = False
        
        return audit_logger
    
    def _ensure_log_directory(self) -> None:
        """Ensure audit log directory exists with proper permissions"""
        log_dir = Path(self.audit_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Set restrictive permissions (owner read/write only)
        try:
            os.chmod(log_dir, 0o700)
            if Path(self.audit_file).exists():
                os.chmod(self.audit_file, 0o600)
        except OSError:
            # Permission setting may fail on some systems
            pass
    
    def _generate_entry_hash(self, entry_data: Dict[str, Any]) -> str:
        """
        Generate hash for audit entry integrity verification
        
        Args:
            entry_data: Audit entry data
            
        Returns:
            SHA-256 hash of entry
        """
        entry_json = json.dumps(entry_data, sort_keys=True)
        return hashlib.sha256(entry_json.encode()).hexdigest()[:16]
    
    def _log_audit_entry(
        self, 
        event_type: str,
        action: str,
        details: Dict[str, Any],
        user_id: Optional[str] = None,
        patient_id: Optional[str] = None
    ) -> None:
        """
        Log audit entry with HIPAA compliance
        
        Args:
            event_type: Type of event (ACCESS, MODIFY, DELETE, etc.)
            action: Specific action taken
            details: Event details
            user_id: User identifier (if applicable)
            patient_id: Patient identifier (if applicable) - will be hashed
        """
        # Prepare audit entry
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "action": action,
            "user_id": user_id or "SYSTEM",
            "session_id": details.get("session_id", "N/A"),
            "source_ip": details.get("source_ip", "INTERNAL"),
            "details": details
        }
        
        # Hash patient ID if provided (HIPAA compliance)
        if patient_id:
            audit_entry["patient_id_hash"] = hashlib.sha256(
                patient_id.encode()
            ).hexdigest()[:16]
        
        # Generate integrity hash
        audit_entry["integrity_hash"] = self._generate_entry_hash(audit_entry)
        
        # Log the entry
        self.logger.info(json.dumps(audit_entry))
    
    def log_user_access(
        self, 
        user_id: str, 
        resource: str,
        action: str = "ACCESS",
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log user access to system resources
        
        Args:
            user_id: User identifier
            resource: Resource accessed
            action: Type of access
            details: Additional details
        """
        audit_details = {
            "resource": resource,
            "access_type": action,
            **(details or {})
        }
        
        self._log_audit_entry(
            event_type="USER_ACCESS",
            action=f"{action}_{resource}",
            details=audit_details,
            user_id=user_id
        )
    
    def log_data_modification(
        self, 
        user_id: str,
        data_type: str,
        record_id: str,
        action: str,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log data modification events
        
        Args:
            user_id: User making the change
            data_type: Type of data modified
            record_id: Record identifier
            action: Type of modification (CREATE, UPDATE, DELETE)
            old_values: Previous values
            new_values: New values
        """
        audit_details = {
            "data_type": data_type,
            "record_id": record_id,
            "modification_type": action
        }
        
        # Include change details for updates
        if action == "UPDATE" and old_values and new_values:
            changes = {}
            for key in new_values:
                if key in old_values and old_values[key] != new_values[key]:
                    changes[key] = {
                        "old": str(old_values[key])[:100],  # Limit length
                        "new": str(new_values[key])[:100]
                    }
            audit_details["changes"] = changes
        
        self._log_audit_entry(
            event_type="DATA_MODIFICATION",
            action=f"{action}_{data_type}",
            details=audit_details,
            user_id=user_id
        )
    
    def log_api_call(
        self,
        service: str,
        method: str,
        endpoint: str,
        status_code: int,
        user_id: Optional[str] = None,
        data_count: Optional[int] = None
    ) -> None:
        """
        Log API calls to external services
        
        Args:
            service: Service name (notion, powerbi, etc.)
            method: HTTP method
            endpoint: API endpoint
            status_code: Response status code
            user_id: User identifier
            data_count: Number of records processed
        """
        audit_details = {
            "service": service,
            "method": method,
            "endpoint": endpoint,
            "status_code": status_code
        }
        
        if data_count is not None:
            audit_details["data_count"] = data_count
        
        self._log_audit_entry(
            event_type="API_CALL",
            action=f"{method}_{service}",
            details=audit_details,
            user_id=user_id
        )
    
    def log_alert_sent(self, alert_data: Dict[str, Any]) -> None:
        """
        Log alert notifications sent
        
        Args:
            alert_data: Alert information
        """
        self._log_audit_entry(
            event_type="ALERT_SENT",
            action=f"ALERT_{alert_data.get('alert_type', 'UNKNOWN').upper()}",
            details=alert_data
        )
    
    def log_performance_update(self, metrics_data: Dict[str, Any]) -> None:
        """
        Log performance metrics updates
        
        Args:
            metrics_data: Performance metrics
        """
        audit_details = {
            "staff_member": metrics_data.get("staff_member"),
            "date": metrics_data.get("date"),
            "action": metrics_data.get("action", "UPDATE"),
            "page_id": metrics_data.get("page_id")
        }
        
        self._log_audit_entry(
            event_type="PERFORMANCE_UPDATE",
            action="UPDATE_PERFORMANCE_METRICS",
            details=audit_details
        )
    
    def log_incident_creation(self, incident_data: Dict[str, Any]) -> None:
        """
        Log incident creation
        
        Args:
            incident_data: Incident information
        """
        audit_details = {
            "incident_id": incident_data.get("incident_id"),
            "staff_member": incident_data.get("staff_member"),
            "severity": incident_data.get("severity"),
            "incident_type": incident_data.get("incident_type"),
            "page_id": incident_data.get("page_id")
        }
        
        self._log_audit_entry(
            event_type="INCIDENT_CREATED",
            action="CREATE_INCIDENT",
            details=audit_details
        )
    
    def log_system_event(
        self,
        event_type: str,
        description: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log general system events
        
        Args:
            event_type: Type of system event
            description: Event description
            details: Additional details
        """
        audit_details = {
            "description": description,
            **(details or {})
        }
        
        self._log_audit_entry(
            event_type="SYSTEM_EVENT",
            action=event_type,
            details=audit_details
        )
    
    def log_authentication_event(
        self,
        user_id: str,
        event_type: str,
        success: bool,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log authentication events
        
        Args:
            user_id: User identifier
            event_type: Type of auth event (LOGIN, LOGOUT, etc.)
            success: Whether the event was successful
            details: Additional details
        """
        audit_details = {
            "auth_event": event_type,
            "success": success,
            **(details or {})
        }
        
        self._log_audit_entry(
            event_type="AUTHENTICATION",
            action=f"{event_type}_{'SUCCESS' if success else 'FAILURE'}",
            details=audit_details,
            user_id=user_id
        )
    
    def log_configuration_change(
        self,
        user_id: str,
        config_type: str,
        changes: Dict[str, Any]
    ) -> None:
        """
        Log configuration changes
        
        Args:
            user_id: User making the change
            config_type: Type of configuration
            changes: Configuration changes
        """
        audit_details = {
            "config_type": config_type,
            "changes": changes
        }
        
        self._log_audit_entry(
            event_type="CONFIGURATION_CHANGE",
            action=f"MODIFY_{config_type.upper()}",
            details=audit_details,
            user_id=user_id
        )
    
    def log_data_export(
        self,
        user_id: str,
        data_type: str,
        record_count: int,
        export_format: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log data export events (important for HIPAA compliance)
        
        Args:
            user_id: User performing export
            data_type: Type of data exported
            record_count: Number of records exported
            export_format: Format of export
            filters: Export filters applied
        """
        audit_details = {
            "data_type": data_type,
            "record_count": record_count,
            "export_format": export_format,
            "filters": filters or {}
        }
        
        self._log_audit_entry(
            event_type="DATA_EXPORT",
            action=f"EXPORT_{data_type.upper()}",
            details=audit_details,
            user_id=user_id
        )
    
    def get_audit_summary(self, days: int = 1) -> Dict[str, Any]:
        """
        Get audit summary for the specified number of days
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Audit summary statistics
        """
        try:
            if not Path(self.audit_file).exists():
                return {"error": "Audit file not found"}
            
            # This is a simplified implementation
            # In production, you might want to use a database for better querying
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            event_counts = {}
            user_activity = {}
            
            with open(self.audit_file, 'r') as f:
                for line in f:
                    try:
                        # Parse log line
                        parts = line.strip().split('|')
                        if len(parts) >= 4 and parts[2] == 'AUDIT':
                            audit_data = json.loads(parts[3])
                            
                            # Check if within date range
                            event_time = datetime.fromisoformat(
                                audit_data['timestamp']
                            ).timestamp()
                            
                            if event_time >= cutoff_date:
                                event_type = audit_data['event_type']
                                user_id = audit_data.get('user_id', 'UNKNOWN')
                                
                                # Count events
                                event_counts[event_type] = event_counts.get(event_type, 0) + 1
                                
                                # Count user activity
                                if user_id not in user_activity:
                                    user_activity[user_id] = {}
                                user_activity[user_id][event_type] = \
                                    user_activity[user_id].get(event_type, 0) + 1
                    
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
            
            return {
                "period_days": days,
                "total_events": sum(event_counts.values()),
                "event_counts": event_counts,
                "active_users": len(user_activity),
                "user_activity": user_activity
            }
            
        except Exception as e:
            return {"error": f"Failed to generate audit summary: {e}"}
    
    def verify_audit_integrity(self, days: int = 1) -> Dict[str, Any]:
        """
        Verify audit log integrity using stored hashes
        
        Args:
            days: Number of days to verify
            
        Returns:
            Integrity verification results
        """
        try:
            if not Path(self.audit_file).exists():
                return {"error": "Audit file not found"}
            
            cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
            total_entries = 0
            verified_entries = 0
            integrity_errors = []
            
            with open(self.audit_file, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        parts = line.strip().split('|')
                        if len(parts) >= 4 and parts[2] == 'AUDIT':
                            audit_data = json.loads(parts[3])
                            
                            # Check if within date range
                            event_time = datetime.fromisoformat(
                                audit_data['timestamp']
                            ).timestamp()
                            
                            if event_time >= cutoff_date:
                                total_entries += 1
                                
                                # Verify integrity hash
                                stored_hash = audit_data.pop('integrity_hash', None)
                                calculated_hash = self._generate_entry_hash(audit_data)
                                
                                if stored_hash == calculated_hash:
                                    verified_entries += 1
                                else:
                                    integrity_errors.append({
                                        "line": line_num,
                                        "timestamp": audit_data.get('timestamp'),
                                        "event_type": audit_data.get('event_type')
                                    })
                    
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
            
            return {
                "period_days": days,
                "total_entries": total_entries,
                "verified_entries": verified_entries,
                "integrity_errors": len(integrity_errors),
                "error_details": integrity_errors[:10],  # Limit to first 10
                "integrity_percentage": (verified_entries / total_entries * 100) if total_entries > 0 else 0
            }
            
        except Exception as e:
            return {"error": f"Failed to verify audit integrity: {e}"}

