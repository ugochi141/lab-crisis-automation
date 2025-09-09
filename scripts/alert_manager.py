"""
Alert Manager
Handles all lab alerts and notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from twilio.rest import Client
from datetime import datetime
import logging
from typing import List, Dict
from config.settings import LabConfig

class AlertManager:
    """Manage all lab alerts and notifications"""
    
    def __init__(self, config: LabConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Email setup
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.sender_email = "lab.automation@kp.org"
        
        # SMS setup (using Twilio as example)
        if config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN:
            self.twilio_client = Client(
                config.TWILIO_ACCOUNT_SID,
                config.TWILIO_AUTH_TOKEN
            )
            self.twilio_from = config.TWILIO_PHONE
        else:
            self.twilio_client = None
            self.twilio_from = None
        
        # Alert levels
        self.alert_levels = {
            'INFO': {'email': True, 'sms': False, 'dashboard': True},
            'WARNING': {'email': True, 'sms': False, 'dashboard': True},
            'URGENT': {'email': True, 'sms': True, 'dashboard': True},
            'CRITICAL': {'email': True, 'sms': True, 'dashboard': True, 'call': True}
        }
        
        # Recipients
        self.recipients = config.ALERT_RECIPIENTS
        
        # Track sent alerts to avoid spam
        self.sent_alerts = set()
    
    def send_alert(self, message: str, level: str = 'INFO', data: Dict = None):
        """Send alert based on level"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"[{level}] {timestamp}\n{message}"
        
        if data:
            full_message += f"\n\nData: {data}"
        
        # Log the alert
        self.logger.log(
            logging.WARNING if level in ['WARNING', 'URGENT'] else logging.INFO,
            full_message
        )
        
        # Get alert configuration
        alert_config = self.alert_levels.get(level, self.alert_levels['INFO'])
        
        # Send email
        if alert_config['email']:
            self.send_email(
                subject=f"Lab Alert: {level}",
                body=full_message,
                recipients=self.recipients['email'][level]
            )
        
        # Send SMS
        if alert_config['sms'] and self.twilio_client:
            self.send_sms(
                message=message[:160],  # SMS limit
                recipients=self.recipients['sms'][level]
            )
        
        # Update dashboard
        if alert_config['dashboard']:
            self.update_dashboard(level, message, data)
        
        # Make phone call for critical
        if alert_config.get('call') and self.twilio_client:
            self.make_call(message, self.recipients['sms']['CRITICAL'][0])
    
    def send_email(self, subject: str, body: str, recipients: List[str]):
        """Send email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # For demo, just log the email
            if self.config.SMTP_SERVER == 'smtp.hospital.local':
                self.logger.info(f"DEMO: Would send email to {recipients}")
                self.logger.info(f"Subject: {subject}")
                self.logger.info(f"Body: {body}")
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.send_message(msg)
            
            self.logger.info(f"Email sent to {recipients}")
            
        except Exception as e:
            self.logger.error(f"Email failed: {e}")
    
    def send_sms(self, message: str, recipients: List[str]):
        """Send SMS alert"""
        if not self.twilio_client:
            self.logger.info(f"DEMO: Would send SMS to {recipients}: {message}")
            return
        
        for number in recipients:
            try:
                message_obj = self.twilio_client.messages.create(
                    body=message,
                    from_=self.twilio_from,
                    to=number
                )
                self.logger.info(f"SMS sent to {number}")
                
            except Exception as e:
                self.logger.error(f"SMS failed to {number}: {e}")
    
    def make_call(self, message: str, number: str):
        """Make phone call for critical alerts"""
        if not self.twilio_client:
            self.logger.info(f"DEMO: Would call {number}: {message}")
            return
        
        try:
            call = self.twilio_client.calls.create(
                twiml=f'<Response><Say>{message}</Say></Response>',
                from_=self.twilio_from,
                to=number
            )
            self.logger.info(f"Call placed to {number}")
            
        except Exception as e:
            self.logger.error(f"Call failed: {e}")
    
    def update_dashboard(self, level: str, message: str, data: Dict = None):
        """Update dashboard with alert"""
        # This would update your Notion or web dashboard
        alert_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            'data': data
        }
        
        # Store in alert log
        self.log_alert(alert_data)
    
    def log_alert(self, alert_data: Dict):
        """Log alert to file"""
        import json
        import os
        
        log_file = 'logs/alerts.log'
        os.makedirs('logs', exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(json.dumps(alert_data) + '\n')
    
    # Convenience methods
    def send_info(self, message: str, data: Dict = None):
        self.send_alert(message, 'INFO', data)
    
    def send_warning(self, message: str, data: Dict = None):
        self.send_alert(message, 'WARNING', data)
    
    def send_urgent(self, message: str, data: Dict = None):
        self.send_alert(message, 'URGENT', data)
    
    def send_critical(self, message: str, data: Dict = None):
        self.send_alert(message, 'CRITICAL', data)
    
    # Specific alert methods
    def alert_high_wait_time(self, station: str, wait_time: float):
        """Alert for high wait times"""
        if wait_time > self.config.WAIT_TIME_CRITICAL:
            self.send_critical(
                f"CRITICAL: Station {station} wait time {wait_time:.0f} minutes",
                {'station': station, 'wait_time': wait_time}
            )
        elif wait_time > self.config.WAIT_TIME_WARNING:
            self.send_warning(
                f"WARNING: Station {station} wait time {wait_time:.0f} minutes",
                {'station': station, 'wait_time': wait_time}
            )
    
    def alert_low_tat(self, tat_rate: float):
        """Alert for low TAT performance"""
        if tat_rate < self.config.TAT_CRITICAL:
            self.send_critical(
                f"CRITICAL: TAT success rate {tat_rate:.1f}%",
                {'tat_rate': tat_rate}
            )
        elif tat_rate < self.config.TAT_WARNING:
            self.send_warning(
                f"WARNING: TAT success rate {tat_rate:.1f}%",
                {'tat_rate': tat_rate}
            )
    
    def alert_missing_staff(self, employee: str, minutes_missing: int):
        """Alert for missing staff"""
        if minutes_missing > 30:
            self.send_critical(
                f"CRITICAL: {employee} missing for {minutes_missing} minutes",
                {'employee': employee, 'minutes_missing': minutes_missing}
            )
        elif minutes_missing > 15:
            self.send_warning(
                f"WARNING: {employee} missing for {minutes_missing} minutes",
                {'employee': employee, 'minutes_missing': minutes_missing}
            )
    
    def alert_break_violation(self, employee: str, break_duration: int):
        """Alert for break time violations"""
        if break_duration > self.config.MAX_LUNCH_TIME:
            self.send_warning(
                f"WARNING: {employee} lunch break {break_duration} minutes",
                {'employee': employee, 'break_duration': break_duration}
            )
        elif break_duration > self.config.MAX_BREAK_TIME:
            self.send_info(
                f"INFO: {employee} break {break_duration} minutes",
                {'employee': employee, 'break_duration': break_duration}
            )
    
    def alert_idle_staff(self, employee: str, idle_percent: float):
        """Alert for idle staff"""
        if idle_percent > 50:
            self.send_warning(
                f"WARNING: {employee} idle {idle_percent:.1f}%",
                {'employee': employee, 'idle_percent': idle_percent}
            )
        elif idle_percent > 30:
            self.send_info(
                f"INFO: {employee} idle {idle_percent:.1f}%",
                {'employee': employee, 'idle_percent': idle_percent}
            )

def test_alert_system():
    """Test alert manager"""
    config = LabConfig()
    alert = AlertManager(config)
    
    print("Testing Alert Manager...")
    
    # Test different alert levels
    alert.send_info("Test info alert")
    alert.send_warning("Test warning alert")
    alert.send_urgent("Test urgent alert")
    alert.send_critical("Test critical alert")
    
    # Test specific alert methods
    alert.alert_high_wait_time("Station 4", 25)
    alert.alert_low_tat(45)
    alert.alert_missing_staff("Johnson,Angela", 20)
    alert.alert_break_violation("Smith,Susan", 45)
    alert.alert_idle_staff("Roberts,Robert", 60)
    
    print("\nAlert system test completed!")
    print("Check logs/alerts.log for alert history")

if __name__ == "__main__":
    test_alert_system()




