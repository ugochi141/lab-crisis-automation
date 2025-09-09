#!/usr/bin/env python3
"""
Start Continuous Crisis Monitoring
Runs every 5 minutes to monitor your lab crisis
"""

import time
import schedule
from datetime import datetime
from working_crisis_monitor import monitor_crisis

def run_monitoring_cycle():
    """Run one monitoring cycle"""
    print(f"\n🔄 Running crisis monitoring cycle at {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    try:
        monitor_crisis()
        print("✅ Monitoring cycle completed successfully")
    except Exception as e:
        print(f"❌ Error in monitoring cycle: {e}")
    
    print("=" * 60)

def start_continuous_monitoring():
    """Start continuous monitoring every 5 minutes"""
    print("🚨 Starting Continuous Lab Crisis Monitoring")
    print("=" * 60)
    print("This will monitor your lab crisis every 5 minutes")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Schedule monitoring every 5 minutes
    schedule.every(5).minutes.do(run_monitoring_cycle)
    
    # Run initial cycle
    run_monitoring_cycle()
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
        print("Crisis monitoring system shut down")

if __name__ == "__main__":
    start_continuous_monitoring()
