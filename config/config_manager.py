"""
Kaiser Permanente Lab Automation System
Configuration Management Module

Handles secure loading and validation of environment variables
with HIPAA compliance and audit logging.
"""

import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from cryptography.fernet import Fernet
from dataclasses import dataclass
import json


@dataclass
class NotionConfig:
    """Notion API configuration"""
    api_token: str
    version: str
    performance_db_id: str
    incident_db_id: str
    lab_management_center_id: str
    task_delegation_db_id: str
    staff_schedule_db_id: str
    pto_schedule_db_id: str
    additional_databases: Dict[str, str]


@dataclass
class PowerBIConfig:
    """Power BI API configuration"""
    workspace_id: str
    performance_dataset_id: str
    performance_api_key: str
    operations_dataset_id: str
    operations_api_key: str


@dataclass
class TeamsConfig:
    """Microsoft Teams webhook configuration"""
    webhook_url: str


@dataclass
class EpicBeakerConfig:
    """Epic Beaker LIS configuration"""
    url: str
    username: str
    password: str
    client_id: str


@dataclass
class QmaticConfig:
    """Qmatic Queue Management configuration"""
    api_url: str
    api_key: str
    username: str
    password: str


@dataclass
class BioRadConfig:
    """Bio-Rad Unity QC configuration"""
    url: str
    username: str
    password: str


@dataclass
class HRConnectConfig:
    """HR Connect scheduling configuration"""
    api_url: str
    api_key: str
    username: str
    password: str


@dataclass
class AlertThresholds:
    """Performance alert thresholds"""
    tat_threshold_minutes: int
    performance_score_threshold: int
    error_rate_threshold: float
    break_time_threshold_minutes: int
    qc_completion_threshold: int


@dataclass
class OperationalSettings:
    """Operational configuration settings"""
    monitoring_interval_seconds: int
    alert_cooldown_minutes: int
    max_retry_attempts: int
    request_timeout_seconds: int


class ConfigManager:
    """
    Secure configuration manager with encryption support
    and HIPAA-compliant audit logging.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            env_file: Path to environment file (defaults to .env)
        """
        self.env_file = env_file or '.env'
        self.logger = self._setup_logging()
        self.encryption_key = None
        self._load_environment()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup HIPAA-compliant audit logging"""
        logger = logging.getLogger('config_manager')
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        Path('logs').mkdir(exist_ok=True)
        
        # Audit log handler
        audit_handler = logging.FileHandler('logs/config_audit.log')
        audit_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        logger.addHandler(audit_handler)
        
        return logger
        
    def _load_environment(self) -> None:
        """Load environment variables from file"""
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            self.logger.info(f"Environment loaded from {self.env_file}")
        else:
            self.logger.warning(f"Environment file {self.env_file} not found")
    
    def _get_required_env(self, key: str) -> str:
        """
        Get required environment variable with validation
        
        Args:
            key: Environment variable name
            
        Returns:
            Environment variable value
            
        Raises:
            ValueError: If required variable is missing
        """
        value = os.getenv(key)
        if not value or value.startswith('your_'):
            raise ValueError(f"Required environment variable {key} is missing or not configured")
        return value
    
    def _get_optional_env(self, key: str, default: str = "") -> str:
        """Get optional environment variable with default"""
        return os.getenv(key, default)
    
    def _decrypt_value(self, encrypted_value: str) -> str:
        """Decrypt encrypted configuration value"""
        if not self.encryption_key:
            encryption_key = os.getenv('ENCRYPTION_KEY')
            if encryption_key:
                self.encryption_key = Fernet(encryption_key.encode())
        
        if self.encryption_key and encrypted_value.startswith('enc:'):
            try:
                return self.encryption_key.decrypt(
                    encrypted_value[4:].encode()
                ).decode()
            except Exception as e:
                self.logger.error(f"Failed to decrypt value: {e}")
                raise
        return encrypted_value
    
    def get_notion_config(self) -> NotionConfig:
        """Get Notion API configuration"""
        try:
            # Try primary token first, fallback to secondary
            try:
                api_token = self._decrypt_value(self._get_required_env('NOTION_API_TOKEN_PRIMARY'))
            except ValueError:
                try:
                    api_token = self._decrypt_value(self._get_required_env('NOTION_API_TOKEN'))
                except ValueError:
                    api_token = self._decrypt_value(self._get_required_env('NOTION_API_TOKEN_SECONDARY'))
            
            # Get additional databases
            additional_databases = {}
            for i in range(1, 8):  # DATABASE_1 through DATABASE_7
                db_key = f'NOTION_DATABASE_{i}'
                db_id = self._get_optional_env(db_key)
                if db_id:
                    additional_databases[db_key] = db_id
            
            config = NotionConfig(
                api_token=api_token,
                version=self._get_optional_env('NOTION_VERSION', '2022-06-28'),
                performance_db_id=self._get_required_env('NOTION_PERFORMANCE_DB_ID'),
                incident_db_id=self._get_required_env('NOTION_INCIDENT_DB_ID'),
                lab_management_center_id=self._get_optional_env('NOTION_LAB_MANAGEMENT_CENTER', ''),
                task_delegation_db_id=self._get_optional_env('NOTION_TASK_DELEGATION_DB_ID', ''),
                staff_schedule_db_id=self._get_optional_env('NOTION_STAFF_SCHEDULE_DB_ID', ''),
                pto_schedule_db_id=self._get_optional_env('NOTION_PTO_SCHEDULE_DB_ID', ''),
                additional_databases=additional_databases
            )
            self.logger.info("Notion configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Notion configuration: {e}")
            raise
    
    def get_powerbi_config(self) -> PowerBIConfig:
        """Get Power BI configuration"""
        try:
            config = PowerBIConfig(
                workspace_id=self._get_required_env('POWERBI_WORKSPACE_ID'),
                performance_dataset_id=self._get_required_env('POWERBI_PERFORMANCE_DATASET_ID'),
                performance_api_key=self._decrypt_value(
                    self._get_required_env('POWERBI_PERFORMANCE_API_KEY')
                ),
                operations_dataset_id=self._get_required_env('POWERBI_OPERATIONS_DATASET_ID'),
                operations_api_key=self._decrypt_value(
                    self._get_required_env('POWERBI_OPERATIONS_API_KEY')
                )
            )
            self.logger.info("Power BI configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Power BI configuration: {e}")
            raise
    
    def get_teams_config(self) -> TeamsConfig:
        """Get Microsoft Teams configuration"""
        try:
            config = TeamsConfig(
                webhook_url=self._decrypt_value(self._get_required_env('TEAMS_WEBHOOK_URL'))
            )
            self.logger.info("Teams configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Teams configuration: {e}")
            raise
    
    def get_epic_beaker_config(self) -> EpicBeakerConfig:
        """Get Epic Beaker LIS configuration"""
        try:
            config = EpicBeakerConfig(
                url=self._get_required_env('EPIC_BEAKER_URL'),
                username=self._decrypt_value(self._get_required_env('EPIC_BEAKER_USERNAME')),
                password=self._decrypt_value(self._get_required_env('EPIC_BEAKER_PASSWORD')),
                client_id=self._decrypt_value(self._get_required_env('EPIC_BEAKER_CLIENT_ID'))
            )
            self.logger.info("Epic Beaker configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Epic Beaker configuration: {e}")
            raise
    
    def get_qmatic_config(self) -> QmaticConfig:
        """Get Qmatic configuration"""
        try:
            config = QmaticConfig(
                api_url=self._get_required_env('QMATIC_API_URL'),
                api_key=self._decrypt_value(self._get_required_env('QMATIC_API_KEY')),
                username=self._decrypt_value(self._get_required_env('QMATIC_USERNAME')),
                password=self._decrypt_value(self._get_required_env('QMATIC_PASSWORD'))
            )
            self.logger.info("Qmatic configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Qmatic configuration: {e}")
            raise
    
    def get_biorad_config(self) -> BioRadConfig:
        """Get Bio-Rad Unity configuration"""
        try:
            config = BioRadConfig(
                url=self._get_required_env('BIORAD_UNITY_URL'),
                username=self._decrypt_value(self._get_required_env('BIORAD_UNITY_USERNAME')),
                password=self._decrypt_value(self._get_required_env('BIORAD_UNITY_PASSWORD'))
            )
            self.logger.info("Bio-Rad Unity configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load Bio-Rad Unity configuration: {e}")
            raise
    
    def get_hrconnect_config(self) -> HRConnectConfig:
        """Get HR Connect configuration"""
        try:
            config = HRConnectConfig(
                api_url=self._get_required_env('HRCONNECT_API_URL'),
                api_key=self._decrypt_value(self._get_required_env('HRCONNECT_API_KEY')),
                username=self._decrypt_value(self._get_required_env('HRCONNECT_USERNAME')),
                password=self._decrypt_value(self._get_required_env('HRCONNECT_PASSWORD'))
            )
            self.logger.info("HR Connect configuration loaded successfully")
            return config
        except Exception as e:
            self.logger.error(f"Failed to load HR Connect configuration: {e}")
            raise
    
    def get_alert_thresholds(self) -> AlertThresholds:
        """Get alert threshold configuration"""
        return AlertThresholds(
            tat_threshold_minutes=int(self._get_optional_env('TAT_THRESHOLD_MINUTES', '30')),
            performance_score_threshold=int(self._get_optional_env('PERFORMANCE_SCORE_THRESHOLD', '60')),
            error_rate_threshold=float(self._get_optional_env('ERROR_RATE_THRESHOLD', '2')),
            break_time_threshold_minutes=int(self._get_optional_env('BREAK_TIME_THRESHOLD_MINUTES', '60')),
            qc_completion_threshold=int(self._get_optional_env('QC_COMPLETION_THRESHOLD', '95'))
        )
    
    def get_operational_settings(self) -> OperationalSettings:
        """Get operational settings"""
        return OperationalSettings(
            monitoring_interval_seconds=int(self._get_optional_env('MONITORING_INTERVAL_SECONDS', '300')),
            alert_cooldown_minutes=int(self._get_optional_env('ALERT_COOLDOWN_MINUTES', '15')),
            max_retry_attempts=int(self._get_optional_env('MAX_RETRY_ATTEMPTS', '3')),
            request_timeout_seconds=int(self._get_optional_env('REQUEST_TIMEOUT_SECONDS', '30'))
        )
    
    def validate_configuration(self) -> Dict[str, Any]:
        """
        Validate all configuration settings
        
        Returns:
            Dictionary with validation results
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        try:
            # Test all configurations
            self.get_notion_config()
            self.get_powerbi_config()
            self.get_teams_config()
            self.get_alert_thresholds()
            self.get_operational_settings()
            
            # Optional configurations (may not be fully configured yet)
            try:
                self.get_epic_beaker_config()
            except ValueError as e:
                results['warnings'].append(f"Epic Beaker: {e}")
            
            try:
                self.get_qmatic_config()
            except ValueError as e:
                results['warnings'].append(f"Qmatic: {e}")
            
            try:
                self.get_biorad_config()
            except ValueError as e:
                results['warnings'].append(f"Bio-Rad Unity: {e}")
            
            try:
                self.get_hrconnect_config()
            except ValueError as e:
                results['warnings'].append(f"HR Connect: {e}")
            
            self.logger.info("Configuration validation completed")
            
        except Exception as e:
            results['valid'] = False
            results['errors'].append(str(e))
            self.logger.error(f"Configuration validation failed: {e}")
        
        return results


def generate_encryption_key() -> str:
    """Generate a new encryption key for securing sensitive configuration values"""
    return Fernet.generate_key().decode()


if __name__ == "__main__":
    # Test configuration loading
    config_manager = ConfigManager()
    validation_results = config_manager.validate_configuration()
    
    print("Configuration Validation Results:")
    print(f"Valid: {validation_results['valid']}")
    
    if validation_results['errors']:
        print("\nErrors:")
        for error in validation_results['errors']:
            print(f"  - {error}")
    
    if validation_results['warnings']:
        print("\nWarnings:")
        for warning in validation_results['warnings']:
            print(f"  - {warning}")
