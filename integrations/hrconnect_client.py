"""HRConnect client for lab automation."""

class HRConnectClient:
    """Mock HRConnect client for testing."""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.connected = False
    
    def connect(self):
        """Connect to HRConnect system."""
        self.connected = True
        return True
    
    def get_staff_data(self):
        """Get staff data from HRConnect."""
        return {
            "status": "ok",
            "staff": []
        }
    
    def disconnect(self):
        """Disconnect from HRConnect system."""
        self.connected = False
        return True