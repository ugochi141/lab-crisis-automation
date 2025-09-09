import os
import time
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from notion_client import Client
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import schedule
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============ CONFIGURATION ============
CONFIG = {
    'NOTION_TOKEN': os.getenv('NOTION_API_TOKEN'),  # Get from environment
    'LOCAL_FOLDER': '/Users/ugochi141/Desktop/LabAutomation/data',  # Your specific path
    'DATABASES': {
        'tat_tracking': 'YOUR_DATABASE_ID_1',
        'staff_performance': 'YOUR_DATABASE_ID_2',
        'station_status': 'YOUR_DATABASE_ID_3',
        'alerts': 'YOUR_DATABASE_ID_4',
        'dashboard': 'YOUR_DATABASE_ID_5',
        'qc_tracking': 'YOUR_DATABASE_ID_6',
        'attendance': 'YOUR_DATABASE_ID_7'
    },
    'FILE_MAPPINGS': {
        'tat_report.csv': 'tat_tracking',
        'staff_daily.xlsx': 'staff_performance',
        'stations.json': 'station_status',
        'alerts.txt': 'alerts',
        'dashboard.csv': 'dashboard',
        'qc_results.csv': 'qc_tracking',
        'attendance.xlsx': 'attendance'
    },
    'THRESHOLDS': {
        'TAT_CRITICAL': 50,
        'TAT_WARNING': 70,
        'TAT_TARGET': 90,
        'WAIT_TIME_CRITICAL': 30,
        'WAIT_TIME_WARNING': 20,
        'WAIT_TIME_TARGET': 15,
        'IDLE_TIME_MAX': 30
    }
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/Users/ugochi141/Desktop/LabAutomation/notion_sync.log'),
        logging.StreamHandler()
    ]
)

class NotionUpdater:
    """Syncs local files to Notion databases"""
    
    def __init__(self):
        self.notion = Client(auth=CONFIG['NOTION_TOKEN'])
        self.local_folder = Path(CONFIG['LOCAL_FOLDER'])
        self.last_sync = {}
        
        # Create folder if doesn't exist
        self.local_folder.mkdir(parents=True, exist_ok=True)
        
        logging.info(f"Monitoring folder: {self.local_folder}")
    
    def process_csv_file(self, filepath, database_name):
        """Process CSV files and upload to Notion"""
        try:
            df = pd.read_csv(filepath)
            database_id = CONFIG['DATABASES'][database_name]
            
            for _, row in df.iterrows():
                if database_name == 'tat_tracking':
                    self.update_tat_tracking(row, database_id)
                elif database_name == 'dashboard':
                    self.update_dashboard(row, database_id)
                elif database_name == 'qc_tracking':
                    self.update_qc_tracking(row, database_id)
                    
            logging.info(f"✓ Synced {filepath} to {database_name}")
            
        except Exception as e:
            logging.error(f"✗ Error processing {filepath}: {e}")
    
    def process_excel_file(self, filepath, database_name):
        """Process Excel files and upload to Notion"""
        try:
            df = pd.read_excel(filepath)
            database_id = CONFIG['DATABASES'][database_name]
            
            for _, row in df.iterrows():
                if database_name == 'staff_performance':
                    self.update_staff_performance(row, database_id)
                elif database_name == 'attendance':
                    self.update_attendance(row, database_id)
                    
            logging.info(f"✓ Synced {filepath} to {database_name}")
            
        except Exception as e:
            logging.error(f"✗ Error processing {filepath}: {e}")
    
    def process_json_file(self, filepath, database_name):
        """Process JSON files and upload to Notion"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            database_id = CONFIG['DATABASES'][database_name]
            
            if database_name == 'station_status':
                for station in data.get('stations', []):
                    self.update_station_status(station, database_id)
                    
            logging.info(f"✓ Synced {filepath} to {database_name}")
            
        except Exception as e:
            logging.error(f"✗ Error processing {filepath}: {e}")
    
    def process_text_file(self, filepath, database_name):
        """Process text alert files"""
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            database_id = CONFIG['DATABASES'][database_name]
            
            for line in lines:
                if line.strip():
                    self.create_alert(line.strip(), database_id)
                    
            logging.info(f"✓ Synced {filepath} to {database_name}")
            
        except Exception as e:
            logging.error(f"✗ Error processing {filepath}: {e}")
    
    def update_tat_tracking(self, row, database_id):
        """Update TAT tracking in Notion"""
        tat_minutes = float(row.get('tat_minutes', 0))
        met_target = tat_minutes <= 45
        
        properties = {
            "Sample ID": {"title": [{"text": {"content": str(row.get('sample_id', ''))}}]},
            "Patient ID": {"rich_text": [{"text": {"content": str(row.get('patient_id', 'Unknown'))}}]},
            "Test Code": {"rich_text": [{"text": {"content": str(row.get('test_code', ''))}}]},
            "TAT Minutes": {"number": tat_minutes},
            "Met Target": {"checkbox": met_target},
            "Technician": {"rich_text": [{"text": {"content": str(row.get('tech', ''))}}]},
            "Collect Time": {"rich_text": [{"text": {"content": str(row.get('collect_time', ''))}}]},
            "Result Time": {"rich_text": [{"text": {"content": str(row.get('result_time', ''))}}]},
            "Timestamp": {"date": {"start": datetime.now().isoformat()}}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
    
    def update_staff_performance(self, row, database_id):
        """Update staff performance in Notion"""
        # Calculate score
        score = self.calculate_score(row)
        
        # Determine status
        if score >= 85:
            status = "Excellent"
        elif score >= 70:
            status = "Good"
        elif score >= 50:
            status = "Needs Improvement"
        else:
            status = "Critical"
        
        properties = {
            "Name": {"title": [{"text": {"content": str(row.get('employee', ''))}}]},
            "Samples Processed": {"number": int(row.get('samples', 0))},
            "Average Draw Time": {"number": float(row.get('draw_time', 0))},
            "Idle Percentage": {"number": float(row.get('idle_percent', 0))},
            "Break Minutes": {"number": float(row.get('break_minutes', 0))},
            "Errors": {"number": int(row.get('errors', 0))},
            "Score": {"number": score},
            "Status": {"select": {"name": status}},
            "Date": {"date": {"start": datetime.now().date().isoformat()}}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        
        # Alert if score is critically low
        if score < 50:
            self.create_performance_alert(row.get('employee', ''), score)
    
    def update_station_status(self, station_data, database_id):
        """Update station status in Notion"""
        wait_time = float(station_data.get('wait_time', 0))
        queue_length = int(station_data.get('queue_length', 0))
        
        # Determine station status
        if wait_time > 30:
            status = "CRITICAL"
            color = "red"
        elif wait_time > 20:
            status = "WARNING"
            color = "orange"
        elif station_data.get('is_open', True):
            status = "ACTIVE"
            color = "green"
        else:
            status = "CLOSED"
            color = "gray"
        
        properties = {
            "Station": {"title": [{"text": {"content": str(station_data.get('name', ''))}}]},
            "Current Tech": {"rich_text": [{"text": {"content": str(station_data.get('tech', 'Unassigned'))}}]},
            "Wait Time": {"number": wait_time},
            "Queue Length": {"number": queue_length},
            "Patients Served": {"number": int(station_data.get('patients_served', 0))},
            "Status": {"select": {"name": status}},
            "Last Update": {"date": {"start": datetime.now().isoformat()}}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
    
    def update_dashboard(self, row, database_id):
        """Update dashboard metrics in Notion"""
        wait_time = float(row.get('wait_time', 0))
        tat_rate = float(row.get('tat_rate', 0))
        staff_count = int(row.get('staff_count', 0))
        queue_depth = int(row.get('queue_depth', 0))
        
        # Determine overall status
        if wait_time > CONFIG['THRESHOLDS']['WAIT_TIME_CRITICAL'] or tat_rate < CONFIG['THRESHOLDS']['TAT_CRITICAL']:
            status = "CRITICAL"
        elif wait_time > CONFIG['THRESHOLDS']['WAIT_TIME_WARNING'] or tat_rate < CONFIG['THRESHOLDS']['TAT_WARNING']:
            status = "WARNING"
        else:
            status = "NORMAL"
        
        properties = {
            "Timestamp": {"title": [{"text": {"content": datetime.now().strftime('%Y-%m-%d %H:%M')}}]},
            "Wait Time": {"number": wait_time},
            "TAT Rate": {"number": tat_rate},
            "Staff Count": {"number": staff_count},
            "Queue Depth": {"number": queue_depth},
            "Stations Active": {"number": int(row.get('stations_active', 0))},
            "Status": {"select": {"name": status}}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        
        # Send alert if critical
        if status == "CRITICAL":
            self.send_critical_alert(wait_time, tat_rate)
    
    def update_qc_tracking(self, row, database_id):
        """Update QC tracking in Notion"""
        result = float(row.get('result', 0))
        mean = float(row.get('mean', 0))
        sd = float(row.get('sd', 1))
        
        # Calculate z-score
        z_score = (result - mean) / sd if sd > 0 else 0
        passed = abs(z_score) <= 2
        
        properties = {
            "Instrument": {"title": [{"text": {"content": str(row.get('instrument', ''))}}]},
            "Test": {"rich_text": [{"text": {"content": str(row.get('test', ''))}}]},
            "Level": {"select": {"name": str(row.get('level', 'Unknown'))}},
            "Result": {"number": result},
            "Mean": {"number": mean},
            "SD": {"number": sd},
            "Z-Score": {"number": round(z_score, 2)},
            "Pass/Fail": {"select": {"name": "PASS" if passed else "FAIL"}},
            "Operator": {"rich_text": [{"text": {"content": str(row.get('operator', ''))}}]},
            "Timestamp": {"date": {"start": datetime.now().isoformat()}}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        
        # Alert if QC failed
        if not passed:
            self.create_qc_alert(row.get('instrument', ''), row.get('test', ''), z_score)
    
    def update_attendance(self, row, database_id):
        """Update attendance tracking in Notion"""
        scheduled_in = str(row.get('scheduled_in', ''))
        actual_in = str(row.get('actual_in', ''))
        
        # Calculate late minutes
        late_minutes = 0
        if scheduled_in and actual_in and actual_in != 'Absent':
            try:
                sched = datetime.strptime(scheduled_in, '%H:%M')
                actual = datetime.strptime(actual_in, '%H:%M')
                if actual > sched:
                    late_minutes = (actual - sched).seconds / 60
            except:
                pass
        
        properties = {
            "Employee": {"title": [{"text": {"content": str(row.get('employee', ''))}}]},
            "Date": {"date": {"start": datetime.now().date().isoformat()}},
            "Scheduled In": {"rich_text": [{"text": {"content": scheduled_in}}]},
            "Actual In": {"rich_text": [{"text": {"content": actual_in or 'Absent'}}]},
            "Late Minutes": {"number": late_minutes},
            "Status": {"select": {"name": "Present" if actual_in else "Absent"}},
            "Scheduled Hours": {"number": float(row.get('scheduled_hours', 0))},
            "Actual Hours": {"number": float(row.get('actual_hours', 0))}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
    
    def calculate_score(self, row):
        """Calculate performance score (matching previous logic)"""
        score = 0
        
        # Productivity (40 points)
        samples = int(row.get('samples', 0))
        expected_samples = 120  # 15 per hour * 8 hours
        if samples > 0:
            score += min(40, (samples / expected_samples) * 40)
        
        # Speed (20 points)
        draw_time = float(row.get('draw_time', 10))
        if draw_time <= 4:
            score += 20
        elif draw_time <= 5:
            score += 15
        elif draw_time <= 6:
            score += 10
        else:
            score += 0
        
        # Attendance (20 points)
        idle = float(row.get('idle_percent', 50))
        if idle < 20:
            score += 20
        elif idle < 30:
            score += 15
        elif idle < 40:
            score += 10
        
        # Quality (20 points base, minus errors)
        errors = int(row.get('errors', 0))
        score += 20
        score -= (errors * 5)
        
        # Break compliance penalty
        break_minutes = float(row.get('break_minutes', 0))
        if break_minutes > 60:
            score -= 10
        
        return max(0, min(100, score))
    
    def create_alert(self, message, database_id):
        """Create alert in Notion"""
        # Determine alert type
        if "CRITICAL" in message.upper():
            alert_type = "CRITICAL"
        elif "WARNING" in message.upper():
            alert_type = "WARNING"
        else:
            alert_type = "INFO"
        
        properties = {
            "Alert": {"title": [{"text": {"content": message}}]},
            "Type": {"select": {"name": alert_type}},
            "Timestamp": {"date": {"start": datetime.now().isoformat()}},
            "Acknowledged": {"checkbox": False}
        }
        
        self.notion.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
    
    def send_critical_alert(self, wait_time, tat_rate):
        """Log critical alerts"""
        alert_msg = f"CRITICAL: Wait {wait_time:.0f}min, TAT {tat_rate:.0f}%"
        logging.critical(alert_msg)
        
        # Create alert in Notion
        self.notion.pages.create(
            parent={"database_id": CONFIG['DATABASES']['alerts']},
            properties={
                "Alert": {"title": [{"text": {"content": alert_msg}}]},
                "Type": {"select": {"name": "CRITICAL"}},
                "Timestamp": {"date": {"start": datetime.now().isoformat()}},
                "Acknowledged": {"checkbox": False}
            }
        )
    
    def create_performance_alert(self, employee, score):
        """Create performance alert"""
        alert_msg = f"Performance Alert: {employee} scored {score:.0f} (Critical)"
        logging.warning(alert_msg)
        
        self.notion.pages.create(
            parent={"database_id": CONFIG['DATABASES']['alerts']},
            properties={
                "Alert": {"title": [{"text": {"content": alert_msg}}]},
                "Type": {"select": {"name": "WARNING"}},
                "Timestamp": {"date": {"start": datetime.now().isoformat()}},
                "Acknowledged": {"checkbox": False}
            }
        )
    
    def create_qc_alert(self, instrument, test, z_score):
        """Create QC failure alert"""
        alert_msg = f"QC FAILURE: {instrument} - {test} (Z-score: {z_score:.2f})"
        logging.error(alert_msg)
        
        self.notion.pages.create(
            parent={"database_id": CONFIG['DATABASES']['alerts']},
            properties={
                "Alert": {"title": [{"text": {"content": alert_msg}}]},
                "Type": {"select": {"name": "CRITICAL"}},
                "Timestamp": {"date": {"start": datetime.now().isoformat()}},
                "Acknowledged": {"checkbox": False}
            }
        )
    
    def scan_folder(self):
        """Scan folder for new/modified files"""
        logging.info("Scanning folder for changes...")
        
        for filename, database in CONFIG['FILE_MAPPINGS'].items():
            filepath = self.local_folder / filename
            
            if filepath.exists():
                # Check if file was modified
                mtime = filepath.stat().st_mtime
                last_sync = self.last_sync.get(filename, 0)
                
                if mtime > last_sync:
                    logging.info(f"Processing {filename}...")
                    
                    if filename.endswith('.csv'):
                        self.process_csv_file(filepath, database)
                    elif filename.endswith('.xlsx'):
                        self.process_excel_file(filepath, database)
                    elif filename.endswith('.json'):
                        self.process_json_file(filepath, database)
                    elif filename.endswith('.txt'):
                        self.process_text_file(filepath, database)
                    
                    self.last_sync[filename] = mtime
    
    def create_sample_files(self):
        """Create sample files for testing"""
        logging.info("Creating sample files for testing...")
        
        # Sample TAT report
        tat_data = pd.DataFrame({
            'sample_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'patient_id': ['P101', 'P102', 'P103', 'P104', 'P105'],
            'test_code': ['CBC', 'CMP', 'CBC', 'BMP', 'Lipid'],
            'tat_minutes': [35, 52, 41, 38, 67],
            'tech': ['John S', 'Mary D', 'Bob K', 'John S', 'Sarah L'],
            'collect_time': ['08:00', '08:15', '08:30', '08:45', '09:00'],
            'result_time': ['08:35', '09:07', '09:11', '09:23', '10:07']
        })
        tat_data.to_csv(self.local_folder / 'tat_report.csv', index=False)
        
        # Sample staff performance
        staff_data = pd.DataFrame({
            'employee': ['John S', 'Mary D', 'Bob K', 'Sarah L', 'Mike R'],
            'samples': [95, 102, 78, 45, 88],
            'draw_time': [4.2, 4.5, 5.1, 7.8, 4.8],
            'idle_percent': [22, 18, 35, 55, 28],
            'break_minutes': [45, 42, 38, 85, 50],
            'errors': [1, 0, 2, 4, 1]
        })
        staff_data.to_excel(self.local_folder / 'staff_daily.xlsx', index=False)
        
        # Sample station status
        stations_data = {
            "stations": [
                {"name": "Station 1", "tech": "John S", "wait_time": 12, "queue_length": 3, "patients_served": 45, "is_open": True},
                {"name": "Station 2", "tech": "Mary D", "wait_time": 8, "queue_length": 2, "patients_served": 52, "is_open": True},
                {"name": "Station 3", "tech": "Bob K", "wait_time": 25, "queue_length": 8, "patients_served": 38, "is_open": True},
                {"name": "Station 4", "tech": "Unassigned", "wait_time": 0, "queue_length": 0, "patients_served": 0, "is_open": False},
                {"name": "Station 5", "tech": "Sarah L", "wait_time": 35, "queue_length": 12, "patients_served": 28, "is_open": True}
            ]
        }
        with open(self.local_folder / 'stations.json', 'w') as f:
            json.dump(stations_data, f, indent=2)
        
        # Sample dashboard metrics
        dashboard_data = pd.DataFrame({
            'wait_time': [22],
            'tat_rate': [67],
            'staff_count': [14],
            'queue_depth': [43],
            'stations_active': [7]
        })
        dashboard_data.to_csv(self.local_folder / 'dashboard.csv', index=False)
        
        # Sample alerts
        with open(self.local_folder / 'alerts.txt', 'w') as f:
            f.write("WARNING: Station 3 wait time exceeding 20 minutes\n")
            f.write("CRITICAL: TAT rate dropped below 70%\n")
            f.write("INFO: Morning QC completed successfully\n")
        
        logging.info("Sample files created successfully")

class FileWatcher(FileSystemEventHandler):
    """Watch for file changes"""
    
    def __init__(self, updater):
        self.updater = updater
    
    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            time.sleep(1)  # Wait for write to complete
            self.updater.scan_folder()
    
    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"File created: {event.src_path}")
            time.sleep(1)
            self.updater.scan_folder()

def main():
    """Main function"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║             Lab Automation - Notion Data Sync                    ║
    ║                                                                  ║
    ║   Monitoring: /Users/ugochi141/Desktop/LabAutomation/data       ║
    ║   Status: Active                                                 ║
    ║   Press Ctrl+C to stop                                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Initialize updater
    updater = NotionUpdater()
    
    # Check if sample files exist, create if not
    sample_files_exist = any(
        (updater.local_folder / filename).exists() 
        for filename in CONFIG['FILE_MAPPINGS'].keys()
    )
    
    if not sample_files_exist:
        print("\n📝 No data files found. Creating sample files...")
        updater.create_sample_files()
        print("✅ Sample files created. You can now modify them to test the sync.\n")
    
    # Initial scan
    updater.scan_folder()
    
    # Set up file watcher
    event_handler = FileWatcher(updater)
    observer = Observer()
    observer.schedule(event_handler, CONFIG['LOCAL_FOLDER'], recursive=False)
    observer.start()
    
    # Schedule periodic scans
    schedule.every(5).minutes.do(updater.scan_folder)
    
    # Show status
    print("\n📊 Monitoring these files:")
    for filename, database in CONFIG['FILE_MAPPINGS'].items():
        filepath = updater.local_folder / filename
        status = "✅ Found" if filepath.exists() else "❌ Not found"
        print(f"   {filename:20} → {database:20} [{status}]")
    
    print("\n🔄 Sync Status:")
    print("   • Real-time monitoring: Active")
    print("   • Periodic scan: Every 5 minutes")
    print("   • Log file: notion_sync.log")
    print("\n" + "="*70 + "\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n\n⏹ Stopped monitoring")
        logging.info("Stopped monitoring")
    
    observer.join()

if __name__ == "__main__":
    # Installation instructions
    print("""
    📦 First-time setup? Install required packages:
    
    pip install notion-client pandas openpyxl watchdog schedule
    
    Then update CONFIG section with:
    1. Your Notion API key
    2. Your database IDs
    
    """)
    
    # Check if required packages are installed
    required_packages = ['notion_client', 'pandas', 'watchdog', 'schedule']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install notion-client pandas openpyxl watchdog schedule")
        print("")
        input("Press Enter to continue anyway...")
    
    main()
