#!/usr/bin/env python3
"""
Secure Lab Crisis Monitor
Uses environment variables for sensitive data
"""

import os
import sys
import json
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/crisis_monitor.log', mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        'NOTION_API_TOKEN',
        'TEAMS_WEBHOOK_URL'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    logger.info("All required environment variables are present")
    return True

def check_lab_metrics():
    """Check lab metrics (simplified version)"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
        "samples_processed": 150,
        "average_tat_minutes": 45,
        "critical_alerts": 0,
        "staff_on_duty": 8
    }
    
    logger.info(f"Lab metrics: {json.dumps(metrics, indent=2)}")
    return metrics

def send_teams_notification(metrics):
    """Send notification to Teams (simplified)"""
    try:
        webhook_url = os.environ.get('TEAMS_WEBHOOK_URL')
        if not webhook_url:
            logger.warning("Teams webhook URL not configured, skipping notification")
            return True
        
        # For GitHub Actions, we'll just log the notification
        logger.info(f"Would send Teams notification with metrics: {metrics}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send Teams notification: {e}")
        return False

def main():
    """Main monitoring function"""
    logger.info("Starting Secure Lab Crisis Monitor")
    
    # Validate environment
    if not validate_environment():
        logger.error("Environment validation failed")
        sys.exit(1)
    
    try:
        # Check lab metrics
        metrics = check_lab_metrics()
        
        # Determine if there's a crisis
        crisis_detected = metrics.get('critical_alerts', 0) > 0
        
        if crisis_detected:
            logger.warning("Crisis detected! Initiating response protocol")
            send_teams_notification(metrics)
        else:
            logger.info("No crisis detected. Lab operations normal")
        
        logger.info("Crisis monitoring completed successfully")
        return 0
        
    except Exception as e:
        logger.error(f"Crisis monitoring failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)