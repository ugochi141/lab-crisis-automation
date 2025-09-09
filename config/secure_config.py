"""
Secure Lab Configuration
Uses environment variables for sensitive data
"""

import os
from datetime import datetime

class SecureLabConfig:
    """Secure configuration class using environment variables"""
    
    def __init__(self):
        # Notion API Configuration
        self.NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN', '')
        self.NOTION_VERSION = "2022-06-28"
        
        # Notion Database IDs
        self.NOTION_PERFORMANCE_DB_ID = os.getenv('NOTION_PERFORMANCE_DB_ID', '')
        self.NOTION_INCIDENT_DB_ID = os.getenv('NOTION_INCIDENT_DB_ID', '')
        self.NOTION_LAB_MANAGEMENT_CENTER = os.getenv('NOTION_LAB_MANAGEMENT_CENTER', '')
        
        # Power BI Configuration
        self.POWERBI_WORKSPACE_ID = os.getenv('POWERBI_WORKSPACE_ID', '')
        self.POWERBI_MONITOR_DATASET_ID = os.getenv('POWERBI_MONITOR_DATASET_ID', '')
        self.POWERBI_MONITOR_PUSH_URL = os.getenv('POWERBI_MONITOR_PUSH_URL', '')
        
        self.POWERBI_METRICS_DATASET_ID = os.getenv('POWERBI_METRICS_DATASET_ID', '')
        self.POWERBI_METRICS_PUSH_URL = os.getenv('POWERBI_METRICS_PUSH_URL', '')
        
        # Teams Integration
        self.TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL', '')
        
        # Alert Thresholds
        self.CRISIS_THRESHOLDS = {
            'tat_critical': 50,
            'tat_warning': 70,
            'tat_target': 90,
            'wait_critical': 30,
            'wait_warning': 20,
            'wait_target': 15,
            'idle_max': 30,
            'break_max': 15,
            'staffing_gap': 3.3,
            'no_show_threshold': 50
        }
    
    def validate_config(self):
        """Validate that all required environment variables are set"""
        required_vars = [
            'NOTION_API_TOKEN',
            'NOTION_PERFORMANCE_DB_ID',
            'NOTION_INCIDENT_DB_ID',
            'TEAMS_WEBHOOK_URL'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
