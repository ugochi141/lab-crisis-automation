"""Alert manager for lab automation."""

class AlertManager:
    """Manages alerts for the lab automation system."""
    
    def __init__(self):
        self.alerts = []
        self.active_alerts = []
    
    def send_alert(self, message, level="info"):
        """Send an alert."""
        alert = {
            "message": message,
            "level": level,
            "timestamp": None
        }
        self.alerts.append(alert)
        if level in ["critical", "warning"]:
            self.active_alerts.append(alert)
        return True
    
    def clear_alert(self, alert_id):
        """Clear an alert."""
        if 0 <= alert_id < len(self.active_alerts):
            self.active_alerts.pop(alert_id)
            return True
        return False
    
    def get_active_alerts(self):
        """Get all active alerts."""
        return self.active_alerts