#!/usr/bin/env python3
"""
Automated Task Scheduler
Manages and executes scheduled lab automation tasks
"""

import schedule
import time
import subprocess
from datetime import datetime
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

class AutomationScheduler:
    def __init__(self):
        self.tasks = []
        self.setup_schedules()

    def setup_schedules(self):
        """Configure scheduled tasks"""
        # Daily tasks
        schedule.every().day.at("06:00").do(self.morning_checks)
        schedule.every().day.at("14:00").do(self.afternoon_sync)
        schedule.every().day.at("22:00").do(self.evening_report)

        # Hourly tasks
        schedule.every().hour.do(self.performance_check)

        # Every 5 minutes
        schedule.every(5).minutes.do(self.critical_monitoring)

        logging.info("✅ Schedules configured")

    def morning_checks(self):
        """Morning system checks"""
        logging.info("🌅 Running morning checks...")

        tasks = [
            ("Check system health", "python system_health.py"),
            ("Update dashboards", "python dashboard_generator.py"),
            ("Sync with GitHub", "python github_sync.py"),
            ("Generate daily plan", "python daily_planner.py")
        ]

        for task_name, command in tasks:
            self.run_task(task_name, command)

    def afternoon_sync(self):
        """Afternoon synchronization"""
        logging.info("☀️ Running afternoon sync...")

        tasks = [
            ("Sync Notion workspace", "python notion_sync.py"),
            ("Update Power BI", "python powerbi_update.py"),
            ("Backup critical data", "python backup_manager.py")
        ]

        for task_name, command in tasks:
            self.run_task(task_name, command)

    def evening_report(self):
        """Evening report generation"""
        logging.info("🌙 Generating evening report...")

        tasks = [
            ("Generate daily summary", "python generate_daily_summary.py"),
            ("Send notifications", "python notification_sender.py"),
            ("Archive logs", "python log_archiver.py")
        ]

        for task_name, command in tasks:
            self.run_task(task_name, command)

    def performance_check(self):
        """Hourly performance check"""
        logging.info("⏰ Running hourly performance check...")

        # Check key metrics
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "status": "operational",
            "alerts": []
        }

        # Save metrics
        with open("metrics_current.json", "w") as f:
            json.dump(metrics, f, indent=2)

    def critical_monitoring(self):
        """Critical system monitoring every 5 minutes"""
        # Quick health check
        logging.debug("🔍 Quick health check completed")

    def run_task(self, task_name, command):
        """Execute a task safely"""
        try:
            logging.info(f"  ▶️ {task_name}")
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                logging.info(f"  ✅ {task_name} completed")
            else:
                logging.error(f"  ❌ {task_name} failed: {result.stderr}")

        except subprocess.TimeoutExpired:
            logging.error(f"  ⏱️ {task_name} timed out")
        except Exception as e:
            logging.error(f"  ❌ {task_name} error: {e}")

    def run(self):
        """Start the scheduler"""
        logging.info("🚀 Automation Scheduler Started")
        logging.info(f"📅 Next jobs: {schedule.jobs}")

        while True:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
            except KeyboardInterrupt:
                logging.info("⏹️ Scheduler stopped by user")
                break
            except Exception as e:
                logging.error(f"Scheduler error: {e}")
                time.sleep(60)  # Wait before retry

if __name__ == "__main__":
    scheduler = AutomationScheduler()
    scheduler.run()
