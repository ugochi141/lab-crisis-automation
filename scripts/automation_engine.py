"""
Main Lab Automation Engine
Coordinates all monitoring and alerts
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
import logging
from typing import Dict, List
import pandas as pd

# Import our modules
from integrations.epic_beaker import EpicBeakerConnector
from integrations.qmatic_api import QmaticConnector
from integrations.notion_tracker import NotionTracker
from scripts.alert_manager import AlertManager
from config.settings import LabConfig

class LabAutomationEngine:
    """Main automation engine for lab operations"""
    
    def __init__(self):
        # Load configuration
        self.config = LabConfig()
        
        # Initialize connections
        self.epic = EpicBeakerConnector(self.config)
        self.qmatic = QmaticConnector(self.config)
        self.notion = NotionTracker(self.config)
        
        # Initialize alert manager
        self.alert_manager = AlertManager(self.config)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Performance cache
        self.last_metrics = {}
        self.alerts_sent = set()
    
    async def morning_startup(self):
        """6 AM - Daily startup routine"""
        self.logger.info("Starting morning routine...")
        
        try:
            # Get current staffing
            staff_status = self.qmatic.get_staff_status()
            logged_in = [s for s in staff_status if s['status'] != 'OFFLINE']
            
            # Check if adequate staffing
            if len(logged_in) < 6:  # Minimum staff required
                self.alert_manager.send_alert(
                    f"Low staffing: Only {len(logged_in)} staff logged in",
                    level='WARNING'
                )
            
            # Send morning report
            morning_data = {
                'staff_count': len(logged_in),
                'pending_samples': len(self.epic.get_pending_samples()),
                'yesterday_tat': self.get_yesterday_performance()
            }
            
            self.logger.info(f"Morning routine completed: {len(logged_in)} staff logged in")
            
        except Exception as e:
            self.logger.error(f"Morning routine failed: {e}")
            self.alert_manager.send_critical(f"Morning routine error: {e}")
    
    async def monitor_real_time(self):
        """Continuous monitoring during operating hours"""
        self.logger.info("Starting real-time monitoring...")
        
        while datetime.now().hour < 20:  # Run until 8 PM
            try:
                # Get current metrics
                queue_status = self.qmatic.get_current_queue_status()
                tat_status = self.epic.get_current_tat()
                staff_status = self.qmatic.get_staff_status()
                
                # Check wait times
                avg_wait = queue_status.get('average_wait', 0)
                if avg_wait > 20:
                    await self.handle_high_wait_time(avg_wait, queue_status)
                
                # Check TAT
                if tat_status['success_rate'] < 70:
                    await self.handle_low_tat(tat_status)
                
                # Check idle staff
                idle_staff = [s for s in staff_status 
                             if s['status'] == 'IDLE' 
                             and s['idle_time'] > 15]
                
                if idle_staff:
                    await self.handle_idle_staff(idle_staff)
                
                # Update Notion tracking
                for staff in staff_status:
                    performance_data = self.calculate_performance_score(staff)
                    self.notion.add_performance_entry(performance_data)
                
                # Update dashboard metrics
                self.last_metrics = {
                    'timestamp': datetime.now(),
                    'wait_time': avg_wait,
                    'tat_rate': tat_status['success_rate'],
                    'staff_active': len([s for s in staff_status if s['status'] == 'SERVING']),
                    'queue_depth': queue_status.get('total_waiting', 0)
                }
                
                # Wait 5 minutes before next check
                await asyncio.sleep(300)
                
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error
    
    async def handle_high_wait_time(self, wait_time: float, queue_data: Dict):
        """Handle high wait time situation"""
        alert_key = f"high_wait_{datetime.now().hour}"
        
        if alert_key not in self.alerts_sent:
            self.alert_manager.alert_high_wait_time("Multiple Stations", wait_time)
            self.alerts_sent.add(alert_key)
    
    async def handle_low_tat(self, tat_data: Dict):
        """Handle low TAT performance"""
        alert_key = f"low_tat_{datetime.now().hour}"
        
        if alert_key not in self.alerts_sent:
            self.alert_manager.alert_low_tat(tat_data['success_rate'])
            self.alerts_sent.add(alert_key)
    
    async def handle_idle_staff(self, idle_staff: List[Dict]):
        """Handle idle staff"""
        for staff in idle_staff:
            self.alert_manager.alert_idle_staff(
                staff['name'], 
                staff['idle_time']
            )
    
    def calculate_performance_score(self, staff_data: Dict) -> Dict:
        """Calculate performance score for staff member"""
        samples = staff_data.get('served_today', 0)
        idle_time = staff_data.get('idle_time', 0)
        
        # Simple scoring algorithm
        score = 100
        score += samples * 2  # Bonus for samples processed
        score -= idle_time * 2  # Penalty for idle time
        
        return {
            'name': staff_data['name'],
            'station': staff_data.get('station', 'Unassigned'),
            'samples': samples,
            'idle_percent': idle_time,
            'score': max(0, score),
            'notes': f"Status: {staff_data['status']}"
        }
    
    def get_yesterday_performance(self) -> Dict:
        """Get yesterday's performance summary"""
        yesterday = datetime.now() - timedelta(days=1)
        return self.epic.get_daily_summary(yesterday)
    
    async def end_of_day(self):
        """4 PM - End of day processing"""
        self.logger.info("Starting end of day routine...")
        
        try:
            # Compile daily metrics
            daily_metrics = await self.compile_daily_metrics()
            
            # Generate performance reports
            staff_performance = self.notion.get_daily_summary()
            
            # Send summary email
            self.send_daily_summary(daily_metrics, staff_performance)
            
            # Reset alerts for tomorrow
            self.alerts_sent.clear()
            
            self.logger.info("End of day routine completed")
            
        except Exception as e:
            self.logger.error(f"End of day routine failed: {e}")
    
    async def compile_daily_metrics(self) -> Dict:
        """Compile daily performance metrics"""
        tat_data = self.epic.get_current_tat()
        queue_data = self.qmatic.get_current_queue_status()
        
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'tat_success_rate': tat_data['success_rate'],
            'avg_wait_time': queue_data.get('average_wait', 0),
            'total_patients': queue_data.get('total_waiting', 0),
            'staff_count': len(self.qmatic.get_staff_status())
        }
    
    def send_daily_summary(self, metrics: Dict, performance: pd.DataFrame):
        """Send daily summary email"""
        summary = f"""
Daily Lab Performance Summary - {metrics['date']}

Key Metrics:
- TAT Success Rate: {metrics['tat_success_rate']:.1f}%
- Average Wait Time: {metrics['avg_wait_time']:.1f} minutes
- Total Patients: {metrics['total_patients']}
- Staff Count: {metrics['staff_count']}

Top Performers:
"""
        
        if not performance.empty:
            top_3 = performance.nlargest(3, 'samples')
            for _, row in top_3.iterrows():
                summary += f"- {row['employee']}: {row['samples']} samples\n"
        
        self.alert_manager.send_info(summary)
    
    def run(self):
        """Main run loop"""
        # Schedule tasks
        schedule.every().day.at("06:00").do(
            lambda: asyncio.run(self.morning_startup())
        )
        schedule.every().day.at("07:00").do(
            lambda: asyncio.run(self.monitor_real_time())
        )
        schedule.every().day.at("16:00").do(
            lambda: asyncio.run(self.end_of_day())
        )
        
        self.logger.info("Lab Automation Engine started")
        
        # Run forever
        while True:
            schedule.run_pending()
            time.sleep(30)

if __name__ == "__main__":
    engine = LabAutomationEngine()
    engine.run()




