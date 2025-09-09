"""
Kaiser Permanente Lab Automation System
Environment Setup Script

Sets up the complete lab automation environment with all dependencies,
configurations, and initial data structures.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
from typing import Dict, List, Any
import asyncio


class LabAutomationSetup:
    """
    Complete setup manager for the lab automation system
    """
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.required_dirs = [
            'logs',
            'config',
            'automation',
            'integrations',
            'utils',
            'scripts',
            'data',
            'reports'
        ]
        
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
    
    def create_directory_structure(self) -> None:
        """Create required directory structure"""
        self.print_step("Creating directory structure...")
        
        for dir_name in self.required_dirs:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)
            self.print_success(f"Created directory: {dir_name}")
    
    def install_python_dependencies(self) -> None:
        """Install required Python packages"""
        self.print_step("Installing Python dependencies...")
        
        requirements = [
            "aiohttp>=3.8.0",
            "asyncio",
            "python-dotenv>=0.19.0",
            "cryptography>=3.4.8",
            "pydantic>=1.8.0",
            "pandas>=1.3.0",
            "numpy>=1.21.0",
            "requests>=2.26.0",
            "python-dateutil>=2.8.2",
            "schedule>=1.1.0",
            "psutil>=5.8.0",
            "openpyxl>=3.0.9",
            "jinja2>=3.0.0",
            "click>=8.0.0"
        ]
        
        # Create requirements.txt
        requirements_file = self.project_root / "requirements.txt"
        with open(requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        self.print_success("Created requirements.txt")
        
        # Install packages
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            self.print_success("Installed Python dependencies")
        except subprocess.CalledProcessError as e:
            self.print_error(f"Failed to install dependencies: {e}")
    
    def create_environment_file(self) -> None:
        """Create .env file from template"""
        self.print_step("Creating environment configuration...")
        
        env_template_path = self.project_root / "config" / "env_template.txt"
        env_file_path = self.project_root / ".env"
        
        if env_template_path.exists() and not env_file_path.exists():
            shutil.copy(env_template_path, env_file_path)
            self.print_success("Created .env file from template")
            self.print_warning("Please edit .env file with your actual credentials")
        elif env_file_path.exists():
            self.print_warning(".env file already exists")
        else:
            self.print_error("Environment template not found")
    
    def create_logging_configuration(self) -> None:
        """Create logging configuration"""
        self.print_step("Setting up logging configuration...")
        
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                },
                "audit": {
                    "format": "%(asctime)s|%(levelname)s|AUDIT|%(message)s"
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "standard",
                    "stream": "ext://sys.stdout"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "standard",
                    "filename": "logs/lab_automation.log",
                    "maxBytes": 10485760,
                    "backupCount": 5
                },
                "audit": {
                    "class": "logging.FileHandler",
                    "level": "INFO",
                    "formatter": "audit",
                    "filename": "logs/audit_trail.log"
                }
            },
            "loggers": {
                "lab_automation": {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                    "propagate": False
                },
                "hipaa_audit": {
                    "level": "INFO",
                    "handlers": ["audit"],
                    "propagate": False
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["console"]
            }
        }
        
        config_file = self.project_root / "config" / "logging_config.json"
        with open(config_file, 'w') as f:
            json.dump(log_config, f, indent=2)
        
        self.print_success("Created logging configuration")
    
    def create_sample_data(self) -> None:
        """Create sample data files for testing"""
        self.print_step("Creating sample data files...")
        
        # Sample performance data
        sample_performance = [
            {
                "staff_member": "John Smith",
                "date": "2024-01-15",
                "shift": "Day (7a-7p)",
                "samples_processed": 45,
                "error_count": 1,
                "break_time_minutes": 45,
                "qc_completion_percent": 98,
                "tat_target_met": True,
                "performance_score": 85,
                "status": "Good"
            },
            {
                "staff_member": "Jane Doe",
                "date": "2024-01-15",
                "shift": "Night (7p-7a)",
                "samples_processed": 38,
                "error_count": 0,
                "break_time_minutes": 40,
                "qc_completion_percent": 100,
                "tat_target_met": True,
                "performance_score": 92,
                "status": "Excellent"
            }
        ]
        
        # Sample incident data
        sample_incidents = [
            {
                "incident_id": "INC-2024-001",
                "timestamp": "2024-01-15T10:30:00",
                "staff_member": "John Smith",
                "incident_type": "TAT Miss",
                "severity": "Medium",
                "impact": "Quality",
                "description": "Sample processing delayed due to equipment calibration",
                "status": "Open"
            }
        ]
        
        # Save sample data
        data_dir = self.project_root / "data"
        
        with open(data_dir / "sample_performance.json", 'w') as f:
            json.dump(sample_performance, f, indent=2)
        
        with open(data_dir / "sample_incidents.json", 'w') as f:
            json.dump(sample_incidents, f, indent=2)
        
        self.print_success("Created sample data files")
    
    def create_startup_scripts(self) -> None:
        """Create startup scripts for different platforms"""
        self.print_step("Creating startup scripts...")
        
        # Windows batch script
        windows_script = '''@echo off
echo Starting Kaiser Permanente Lab Automation System...
cd /d "%~dp0"
python -m automation.lab_automation_core
pause
'''
        
        with open(self.project_root / "start_lab_automation.bat", 'w') as f:
            f.write(windows_script)
        
        # Unix shell script
        unix_script = '''#!/bin/bash
echo "Starting Kaiser Permanente Lab Automation System..."
cd "$(dirname "$0")"
python -m automation.lab_automation_core
'''
        
        script_path = self.project_root / "start_lab_automation.sh"
        with open(script_path, 'w') as f:
            f.write(unix_script)
        
        # Make shell script executable
        try:
            script_path.chmod(0o755)
        except OSError:
            pass  # May fail on Windows
        
        self.print_success("Created startup scripts")
    
    def create_configuration_validator(self) -> None:
        """Create configuration validation script"""
        self.print_step("Creating configuration validator...")
        
        validator_script = '''#!/usr/bin/env python3
"""
Configuration Validator for Lab Automation System
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config_manager import ConfigManager

def main():
    print("Validating Lab Automation Configuration...")
    print("-" * 50)
    
    try:
        config_manager = ConfigManager()
        results = config_manager.validate_configuration()
        
        if results['valid']:
            print("✅ Configuration is valid!")
        else:
            print("❌ Configuration validation failed!")
            
        if results['errors']:
            print("\\nErrors:")
            for error in results['errors']:
                print(f"  - {error}")
                
        if results['warnings']:
            print("\\nWarnings:")
            for warning in results['warnings']:
                print(f"  - {warning}")
                
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        validator_path = self.project_root / "scripts" / "validate_config.py"
        with open(validator_path, 'w') as f:
            f.write(validator_script)
        
        self.print_success("Created configuration validator")
    
    def create_systemd_service(self) -> None:
        """Create systemd service file for Linux deployment"""
        self.print_step("Creating systemd service file...")
        
        service_content = f'''[Unit]
Description=Kaiser Permanente Lab Automation System
After=network.target
Wants=network.target

[Service]
Type=simple
User=labautomation
Group=labautomation
WorkingDirectory={self.project_root}
Environment=PYTHONPATH={self.project_root}
ExecStart=/usr/bin/python3 -m automation.lab_automation_core
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
'''
        
        service_file = self.project_root / "scripts" / "lab-automation.service"
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        self.print_success("Created systemd service file")
        self.print_warning("Copy lab-automation.service to /etc/systemd/system/ for system-wide installation")
    
    def create_docker_files(self) -> None:
        """Create Docker configuration files"""
        self.print_step("Creating Docker configuration...")
        
        dockerfile = '''FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Create non-root user
RUN useradd -m -u 1000 labuser && chown -R labuser:labuser /app
USER labuser

# Expose port (if needed for web interface)
EXPOSE 8000

# Run the application
CMD ["python", "-m", "automation.lab_automation_core"]
'''
        
        with open(self.project_root / "Dockerfile", 'w') as f:
            f.write(dockerfile)
        
        # Docker Compose file
        compose_content = '''version: '3.8'

services:
  lab-automation:
    build: .
    container_name: kaiser-lab-automation
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
      - ./.env:/app/.env:ro
    environment:
      - PYTHONPATH=/app
    networks:
      - lab-network

networks:
  lab-network:
    driver: bridge
'''
        
        with open(self.project_root / "docker-compose.yml", 'w') as f:
            f.write(compose_content)
        
        # Docker ignore file
        dockerignore = '''__pycache__
*.pyc
*.pyo
*.pyd
.git
.gitignore
README.md
.env
*.log
.pytest_cache
.coverage
'''
        
        with open(self.project_root / ".dockerignore", 'w') as f:
            f.write(dockerignore)
        
        self.print_success("Created Docker configuration files")
    
    def create_readme(self) -> None:
        """Create comprehensive README file"""
        self.print_step("Creating README documentation...")
        
        readme_content = '''# Kaiser Permanente Lab Automation System

## Overview

Comprehensive lab automation system for Kaiser Permanente Largo, MD location. 
Integrates Epic Beaker, Qmatic, Bio-Rad Unity, HRConnect, Notion, and Power BI 
for complete lab operations management.

## Features

- **Real-time Performance Monitoring**: Track TAT, error rates, staff performance
- **Automated Alerting**: Teams notifications for critical issues
- **Incident Management**: Comprehensive incident tracking and resolution
- **Dashboard Integration**: Power BI dashboards with live data
- **HIPAA Compliance**: Full audit logging and security features
- **Multi-system Integration**: Connect all lab systems seamlessly

## Quick Start

### 1. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp config/env_template.txt .env

# Edit .env with your credentials
nano .env
```

### 2. Configuration

```bash
# Validate configuration
python scripts/validate_config.py

# Test connections
python -c "from automation.lab_automation_core import LabAutomationCore; import asyncio; asyncio.run(LabAutomationCore().test_connections())"
```

### 3. Start System

```bash
# Manual start
python -m automation.lab_automation_core

# Or use startup script
./start_lab_automation.sh  # Linux/Mac
start_lab_automation.bat   # Windows
```

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Epic Beaker   │    │     Qmatic       │    │   Bio-Rad Unity │
│      (LIS)      │    │  (Queue Mgmt)    │    │   (QC Mgmt)     │
└─────────┬───────┘    └────────┬─────────┘    └─────────┬───────┘
          │                     │                        │
          └─────────────────────┼────────────────────────┘
                                │
                    ┌───────────▼──────────┐
                    │  Lab Automation Core │
                    │    (Central Hub)     │
                    └───────────┬──────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
    ┌─────▼─────┐      ┌────────▼────────┐     ┌─────▼──────┐
    │  Notion   │      │    Power BI     │     │   Teams    │
    │(Tracking) │      │  (Dashboards)   │     │ (Alerts)   │
    └───────────┘      └─────────────────┘     └────────────┘
```

## Configuration

### Environment Variables

Key configuration items in `.env`:

- `NOTION_API_TOKEN`: Notion integration token
- `POWERBI_*`: Power BI dataset IDs and API keys
- `TEAMS_WEBHOOK_URL`: Teams channel webhook
- `EPIC_BEAKER_*`: Epic Beaker connection details
- Alert thresholds and operational settings

### Alert Thresholds

- TAT Threshold: 30 minutes (configurable)
- Performance Score Threshold: 60 (configurable)
- Error Rate Threshold: 2% (configurable)
- Break Time Threshold: 60 minutes (configurable)

## Integration Details

### Notion Databases

- **Team Performance Dashboard**: Staff metrics and scores
- **Incident Tracking**: Error and issue management
- **Operations Monitoring**: Real-time status tracking

### Power BI Datasets

- **Performance Dataset**: Real-time performance metrics
- **Operations Dataset**: Incident and queue data

### Teams Alerts

- Performance threshold breaches
- Critical incidents
- System status changes
- Daily summaries

## Monitoring & Alerts

### Alert Types

1. **Critical**: Immediate attention required
2. **Warning**: Performance issues detected
3. **Info**: Status updates and summaries
4. **Performance**: Individual staff alerts

### Escalation Matrix

- Performance Score < 60: Manager notification
- 3+ incidents in 7 days: Coaching session scheduled
- Critical incidents: Immediate supervisor alert

## Compliance & Security

### HIPAA Compliance

- Comprehensive audit logging
- Data encryption in transit
- Access controls and authentication
- Data retention policies (7 years)

### Security Features

- Encrypted credential storage
- Secure API communications
- Audit trail integrity verification
- Role-based access controls

## Deployment Options

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f
```

### Systemd Service (Linux)

```bash
# Copy service file
sudo cp scripts/lab-automation.service /etc/systemd/system/

# Enable and start service
sudo systemctl enable lab-automation
sudo systemctl start lab-automation
```

## Troubleshooting

### Common Issues

1. **Connection Failures**: Check API credentials and network connectivity
2. **Alert Not Sending**: Verify Teams webhook URL
3. **Data Not Updating**: Check Notion database permissions
4. **Performance Issues**: Review log files in `logs/` directory

### Log Files

- `logs/lab_automation.log`: General system logs
- `logs/audit_trail.log`: HIPAA-compliant audit logs
- `logs/config_audit.log`: Configuration change logs

### Support

For technical support:
- Check logs for error details
- Validate configuration with `scripts/validate_config.py`
- Review Notion database permissions
- Verify API credentials and network connectivity

## Development

### Project Structure

```
├── automation/           # Core automation engine
├── config/              # Configuration management
├── integrations/        # External system clients
├── utils/               # Utility modules
├── scripts/             # Setup and maintenance scripts
├── logs/                # Log files
└── data/                # Sample and test data
```

### Adding New Integrations

1. Create client in `integrations/`
2. Add configuration to `config_manager.py`
3. Update core automation engine
4. Add tests and documentation

## License

Proprietary - Kaiser Permanente Internal Use Only
'''
        
        with open(self.project_root / "README.md", 'w') as f:
            f.write(readme_content)
        
        self.print_success("Created README documentation")
    
    def run_setup(self) -> None:
        """Run complete setup process"""
        self.print_header("Kaiser Permanente Lab Automation System Setup")
        
        try:
            self.create_directory_structure()
            self.install_python_dependencies()
            self.create_environment_file()
            self.create_logging_configuration()
            self.create_sample_data()
            self.create_startup_scripts()
            self.create_configuration_validator()
            self.create_systemd_service()
            self.create_docker_files()
            self.create_readme()
            
            self.print_header("Setup Complete!")
            print("\n🎉 Lab Automation System setup completed successfully!")
            print("\nNext steps:")
            print("1. Edit .env file with your actual credentials")
            print("2. Run: python scripts/validate_config.py")
            print("3. Start system: python -m automation.lab_automation_core")
            print("\nFor detailed instructions, see README.md")
            
        except Exception as e:
            self.print_error(f"Setup failed: {e}")
            sys.exit(1)


if __name__ == "__main__":
    setup = LabAutomationSetup()
    setup.run_setup()
