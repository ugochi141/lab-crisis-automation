"""
Lab Automation Configuration
Kaiser Permanente Largo Lab
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Any
import json
from datetime import datetime

@dataclass
class LabConfig:
    """Configuration for lab automation system"""
    
    # Lab Information
    LAB_NAME = "Kaiser Permanente Largo Lab"
    LAB_LOCATION = "Largo, MD"
    TOTAL_STATIONS = 10
    PEAK_HOURS = [(10, 15)]  # 10am to 3pm
    
    # Epic Beaker Configuration
    EPIC_SERVER = os.getenv('EPIC_SERVER', 'epic.hospital.local')
    EPIC_DATABASE = os.getenv('EPIC_DB', 'LAB_RESULTS')
    EPIC_USER = os.getenv('EPIC_USER', 'lab_automation')
    EPIC_PASSWORD = os.getenv('EPIC_PASS', '')
    
    # Qmatic Configuration  
    QMATIC_API_URL = os.getenv('QMATIC_URL', 'http://qmatic.hospital.local/api/v1')
    QMATIC_API_KEY = os.getenv('QMATIC_KEY', '')
    QMATIC_BRANCH_ID = 'LARGO'
    
    # Bio-Rad Unity
    BIORAD_SERVER = os.getenv('BIORAD_SERVER', 'biorad.hospital.local')
    BIORAD_USER = os.getenv('BIORAD_USER', 'qc_automation')
    
    # Notion Configuration
    NOTION_API_KEY = os.getenv('NOTION_KEY', '')
    NOTION_DATABASE_ID = os.getenv('NOTION_DB', '')
    
    # Alert Configuration
    SMTP_SERVER = 'smtp.hospital.local'
    SMTP_PORT = 587
    ALERT_EMAIL = 'lab.manager@kp.org'
    SMS_GATEWAY = 'sms.hospital.local'
    
    # Twilio Configuration (for SMS alerts)
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_TOKEN', '')
    TWILIO_PHONE = os.getenv('TWILIO_PHONE', '')
    
    # Performance Thresholds
    TAT_TARGET = 90  # percent
    WAIT_TIME_TARGET = 15  # minutes
    IDLE_TIME_MAX = 30  # percent
    BREAK_TIME_MAX = 15  # minutes
    LUNCH_TIME_MAX = 30  # minutes
    
    # Alert Thresholds
    WAIT_TIME_WARNING = 15  # Yellow alert
    WAIT_TIME_CRITICAL = 20  # Red alert
    TAT_WARNING = 70  # Yellow
    TAT_CRITICAL = 50  # Red
    MAX_IDLE_TIME = 15  # Minutes before alert
    MAX_BREAK_TIME = 15  # Standard break
    MAX_LUNCH_TIME = 30  # Lunch break
    
    # Volume triggers
    PEAK_HOUR_START = 10  # 10 AM
    PEAK_HOUR_END = 15  # 3 PM
    HIGH_VOLUME = 50  # Patients/hour
    
    # Staff Configuration
    FLOAT_TEAM_NUMBERS = [
        '+1234567890',  # Manager
        '+0987654321'   # Supervisor
    ]
    
    # Recipients for different alert levels
    ALERT_RECIPIENTS = {
        'email': {
            'INFO': ['lab.manager@kp.org'],
            'WARNING': ['lab.manager@kp.org', 'supervisor@kp.org'],
            'URGENT': ['lab.manager@kp.org', 'supervisor@kp.org', 'director@kp.org'],
            'CRITICAL': ['lab.manager@kp.org', 'supervisor@kp.org', 'director@kp.org', 'admin@kp.org']
        },
        'sms': {
            'URGENT': ['+1234567890'],  # Manager
            'CRITICAL': ['+1234567890', '+0987654321']  # Manager and Director
        }
    }
    
    @classmethod
    def load_from_file(cls, filepath: str = 'config/config.json'):
        """Load configuration from JSON file"""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save_to_file(self, filepath: str = 'config/config.json'):
        """Save configuration to JSON file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

# Initialize configuration
config = LabConfig()
config.save_to_file()

# Create environment file template
def create_env_template():
    """Create .env template file"""
    env_content = """
# Lab Automation Environment Variables
# Copy this file to .env and fill in your actual values

# Epic Beaker
EPIC_SERVER=epic.hospital.local
EPIC_DB=LAB_RESULTS
EPIC_USER=lab_automation
EPIC_PASS=your_password_here

# Qmatic
QMATIC_URL=http://qmatic.hospital.local/api/v1
QMATIC_KEY=your_api_key_here

# Bio-Rad Unity
BIORAD_SERVER=biorad.hospital.local
BIORAD_USER=qc_automation

# Notion
NOTION_KEY=your_notion_api_key_here
NOTION_DB=your_database_id_here

# Twilio (for SMS alerts)
TWILIO_SID=your_twilio_sid_here
TWILIO_TOKEN=your_twilio_token_here
TWILIO_PHONE=your_twilio_phone_here
"""
    
    with open('.env.template', 'w') as f:
        f.write(env_content)
    
    print("Created .env.template file")
    print("Copy to .env and fill in your actual values")

if __name__ == "__main__":
    create_env_template()
    print("Configuration setup complete!")



