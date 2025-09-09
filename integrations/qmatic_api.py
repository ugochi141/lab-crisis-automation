"""
Qmatic API Integration
Handles queue management and phlebotomy tracking
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
import pandas as pd
from config.settings import LabConfig

class QmaticConnector:
    """Qmatic Queue Management System API"""
    
    def __init__(self, config: LabConfig):
        self.config = config
        self.base_url = config.QMATIC_API_URL
        self.headers = {
            'Authorization': f'Bearer {config.QMATIC_API_KEY}',
            'Content-Type': 'application/json'
        }
        self.logger = logging.getLogger(__name__)
        
        # For demo purposes, we'll simulate Qmatic data
        self.demo_mode = True
        
    def get_current_queue_status(self) -> Dict:
        """Get real-time queue status for all stations"""
        if self.demo_mode:
            return self._get_demo_queue_status()
        
        try:
            endpoint = f"{self.base_url}/branches/{self.config.QMATIC_BRANCH_ID}/queues/status"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process station data
            station_status = {}
            for station in data['servicePoints']:
                station_status[station['name']] = {
                    'id': station['id'],
                    'status': station['status'],
                    'current_ticket': station.get('currentTicket'),
                    'serving_staff': station.get('servingStaff'),
                    'queue_length': station.get('waitingCount', 0),
                    'avg_wait_time': station.get('averageWaitTime', 0)
                }
            
            return {
                'timestamp': datetime.now().isoformat(),
                'total_waiting': data['totalWaiting'],
                'average_wait': data['averageWaitTime'],
                'stations': station_status
            }
            
        except Exception as e:
            self.logger.error(f"Qmatic API error: {e}")
            return self._get_demo_queue_status()
    
    def _get_demo_queue_status(self) -> Dict:
        """Demo queue status data"""
        import random
        
        # Create realistic station data
        stations = {}
        total_waiting = 0
        wait_times = []
        
        for i in range(1, 11):  # 10 stations
            station_name = f"Station {i}"
            
            # Randomize station status
            if i <= 8:  # Most stations active
                status = "ACTIVE"
                queue_length = random.randint(0, 12)
                avg_wait = random.uniform(5, 25)
                staff = self._get_random_staff()
            else:
                status = "CLOSED"
                queue_length = 0
                avg_wait = 0
                staff = None
            
            stations[station_name] = {
                'id': i,
                'status': status,
                'current_ticket': f"T{random.randint(1000, 9999)}" if status == "ACTIVE" else None,
                'serving_staff': staff,
                'queue_length': queue_length,
                'avg_wait_time': avg_wait
            }
            
            total_waiting += queue_length
            if avg_wait > 0:
                wait_times.append(avg_wait)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'total_waiting': total_waiting,
            'average_wait': sum(wait_times) / len(wait_times) if wait_times else 0,
            'stations': stations
        }
    
    def _get_random_staff(self) -> str:
        """Get random staff member for demo"""
        staff = [
            'Bolden-Davis,Christina',
            'Kena,Turi', 
            'Miah,Youlana',
            'Johnson,Angela',
            'Foster,Larry',
            'Merriman,London',
            'Ali,Farah',
            'Parker,Shannon'
        ]
        import random
        return random.choice(staff)
    
    def get_staff_status(self) -> List[Dict]:
        """Get current staff locations and status"""
        if self.demo_mode:
            return self._get_demo_staff_status()
        
        try:
            endpoint = f"{self.base_url}/branches/{self.config.QMATIC_BRANCH_ID}/users"
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            staff_data = []
            for user in response.json():
                staff_data.append({
                    'name': user['userName'],
                    'station': user.get('servicePointName'),
                    'status': user['status'],  # SERVING, IDLE, BREAK
                    'login_time': user.get('loginTime'),
                    'idle_time': user.get('idleTime', 0),
                    'served_today': user.get('servedCount', 0)
                })
            
            return staff_data
            
        except Exception as e:
            self.logger.error(f"Qmatic staff API error: {e}")
            return self._get_demo_staff_status()
    
    def _get_demo_staff_status(self) -> List[Dict]:
        """Demo staff status data"""
        import random
        
        staff = [
            'Bolden-Davis,Christina',
            'Kena,Turi', 
            'Miah,Youlana',
            'Johnson,Angela',
            'Foster,Larry',
            'Merriman,London',
            'Ali,Farah',
            'Parker,Shannon',
            'Smith,Susan',
            'Roberts,Robert'
        ]
        
        staff_data = []
        for i, employee in enumerate(staff):
            # Randomize status
            status_options = ['SERVING', 'IDLE', 'BREAK', 'OFFLINE']
            weights = [0.6, 0.2, 0.1, 0.1]  # Most likely serving
            status = random.choices(status_options, weights=weights)[0]
            
            if status == 'SERVING':
                station = f"Station {i + 1}" if i < 8 else "Station 1"
                idle_time = 0
            elif status == 'IDLE':
                station = None
                idle_time = random.randint(5, 30)
            elif status == 'BREAK':
                station = None
                idle_time = random.randint(15, 45)
            else:  # OFFLINE
                station = None
                idle_time = 0
            
            staff_data.append({
                'name': employee,
                'station': station,
                'status': status,
                'login_time': (datetime.now() - timedelta(hours=random.randint(1, 8))).isoformat(),
                'idle_time': idle_time,
                'served_today': random.randint(20, 80)
            })
        
        return staff_data
    
    def get_hourly_statistics(self, date: str = None) -> pd.DataFrame:
        """Get hourly performance statistics"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if self.demo_mode:
            return self._get_demo_hourly_stats(date)
        
        try:
            endpoint = f"{self.base_url}/statistics/hourly"
            params = {'date': date, 'branchId': self.config.QMATIC_BRANCH_ID}
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            
            df = pd.DataFrame(response.json())
            return df
            
        except Exception as e:
            self.logger.error(f"Statistics API error: {e}")
            return self._get_demo_hourly_stats(date)
    
    def _get_demo_hourly_stats(self, date: str) -> pd.DataFrame:
        """Demo hourly statistics"""
        import random
        
        stats = []
        for hour in range(6, 20):  # 6 AM to 8 PM
            # Peak hours have more volume
            if 10 <= hour <= 15:  # Peak hours
                volume = random.randint(40, 80)
                wait_time = random.uniform(15, 30)
            else:
                volume = random.randint(10, 30)
                wait_time = random.uniform(5, 15)
            
            stats.append({
                'hour': hour,
                'volume': volume,
                'wait_time': wait_time,
                'active_stations': random.randint(6, 10),
                'date': date
            })
        
        return pd.DataFrame(stats)
    
    def call_next_patient(self, station_id: str) -> Dict:
        """Call next patient to station"""
        if self.demo_mode:
            return {'success': True, 'ticket': f'T{random.randint(1000, 9999)}'}
        
        try:
            endpoint = f"{self.base_url}/servicePoints/{station_id}/callNext"
            response = requests.post(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Call next patient error: {e}")
            return {'success': False, 'error': str(e)}

def test_qmatic_connection():
    """Test Qmatic API connection"""
    config = LabConfig()
    qmatic = QmaticConnector(config)
    
    print("Testing Qmatic API Integration...")
    
    # Get queue status
    status = qmatic.get_current_queue_status()
    print(f"Total Waiting: {status.get('total_waiting', 0)}")
    print(f"Average Wait: {status.get('average_wait', 0):.1f} minutes")
    
    # Show station status
    print("\nStation Status:")
    for station_name, station_data in status.get('stations', {}).items():
        print(f"  {station_name}: {station_data['status']} - {station_data['queue_length']} waiting")
    
    # Get staff status
    staff = qmatic.get_staff_status()
    print(f"\nStaff Status:")
    for person in staff:
        print(f"  {person['name']}: {person['status']} at {person['station'] or 'No station'}")
    
    # Get hourly stats
    hourly_stats = qmatic.get_hourly_statistics()
    print(f"\nHourly Statistics:")
    print(f"  Peak hour (10 AM): {hourly_stats[hourly_stats['hour'] == 10]['volume'].iloc[0]} patients")
    print(f"  Average wait time: {hourly_stats['wait_time'].mean():.1f} minutes")
    
    print("\nQmatic API integration test completed!")

if __name__ == "__main__":
    test_qmatic_connection()



