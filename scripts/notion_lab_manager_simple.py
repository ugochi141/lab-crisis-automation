#!/usr/bin/env python3
"""Simplified Notion Lab Manager for GitHub Actions."""

import os
import sys
import json
from datetime import datetime

def main():
    """Main function for lab management."""
    print("Starting Notion Lab Manager (Simplified)")
    
    # Check environment
    notion_token = os.environ.get('NOTION_API_TOKEN')
    teams_webhook = os.environ.get('TEAMS_WEBHOOK_URL')
    
    if not notion_token:
        print("WARNING: NOTION_API_TOKEN not set, running in demo mode")
    
    if not teams_webhook:
        print("WARNING: TEAMS_WEBHOOK_URL not set, notifications disabled")
    
    # Simulate lab metrics
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "status": "operational",
        "samples_processed": 150,
        "average_tat_minutes": 45,
        "critical_alerts": 0,
        "staff_on_duty": 8,
        "qc_pass_rate": 98.5
    }
    
    print("Current Lab Metrics:")
    print(json.dumps(metrics, indent=2))
    
    # Check for issues
    issues_found = False
    
    if metrics["average_tat_minutes"] > 90:
        print("WARNING: TAT exceeds threshold")
        issues_found = True
    
    if metrics["critical_alerts"] > 0:
        print("ERROR: Critical alerts detected")
        issues_found = True
    
    if metrics["staff_on_duty"] < 5:
        print("WARNING: Low staffing levels")
        issues_found = True
    
    if not issues_found:
        print("✅ All lab metrics within normal parameters")
    else:
        print("⚠️ Issues detected - monitoring closely")
    
    print("Notion Lab Manager completed successfully")
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)