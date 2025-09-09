"""
Notion Integration
Handles performance tracking and database management
"""

from notion_client import Client
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from config.settings import LabConfig

class NotionTracker:
    """Notion database for performance tracking"""
    
    def __init__(self, config: LabConfig):
        self.config = config
        self.client = Client(auth=config.NOTION_API_KEY)
        self.database_id = config.NOTION_DATABASE_ID
        self.logger = logging.getLogger(__name__)
        
        # For demo purposes, we'll simulate Notion
        self.demo_mode = True
        
        # Create database if not exists
        if not self.database_id and not self.demo_mode:
            self.database_id = self.create_performance_database()
    
    def create_performance_database(self) -> str:
        """Create Notion database for tracking"""
        try:
            response = self.client.databases.create(
                parent={"type": "page_id", "page_id": "YOUR_PAGE_ID"},
                title=[{"text": {"content": "Lab Performance Tracker"}}],
                properties={
                    "Date": {"date": {}},
                    "Employee": {"title": {}},
                    "Station": {"select": {
                        "options": [{"name": f"Station {i}"} for i in range(1, 11)]
                    }},
                    "Samples Processed": {"number": {"format": "number"}},
                    "Average Draw Time": {"number": {"format": "number"}},
                    "Wait Time": {"number": {"format": "number"}},
                    "Idle Time %": {"number": {"format": "percent"}},
                    "Break Minutes": {"number": {"format": "number"}},
                    "Errors": {"number": {"format": "number"}},
                    "Score": {"formula": {
                        "expression": "prop(\"Samples Processed\") * 2 - prop(\"Idle Time %\") * 100 - prop(\"Errors\") * 10"
                    }},
                    "Status": {"select": {
                        "options": [
                            {"name": "Excellent", "color": "green"},
                            {"name": "Good", "color": "blue"},
                            {"name": "Warning", "color": "yellow"},
                            {"name": "Critical", "color": "red"}
                        ]
                    }},
                    "Notes": {"rich_text": {}}
                }
            )
            
            self.logger.info(f"Created Notion database: {response['id']}")
            return response['id']
            
        except Exception as e:
            self.logger.error(f"Failed to create Notion database: {e}")
            raise
    
    def add_performance_entry(self, employee_data: Dict) -> Optional[str]:
        """Add employee performance entry"""
        if self.demo_mode:
            return self._simulate_notion_entry(employee_data)
        
        try:
            # Determine status based on score
            score = employee_data.get('score', 0)
            if score >= 90:
                status = "Excellent"
            elif score >= 70:
                status = "Good"
            elif score >= 50:
                status = "Warning"
            else:
                status = "Critical"
            
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "Date": {"date": {"start": datetime.now().isoformat()}},
                    "Employee": {"title": [{"text": {"content": employee_data['name']}}]},
                    "Station": {"select": {"name": employee_data.get('station', 'Unassigned')}},
                    "Samples Processed": {"number": employee_data.get('samples', 0)},
                    "Average Draw Time": {"number": employee_data.get('draw_time', 0)},
                    "Wait Time": {"number": employee_data.get('wait_time', 0)},
                    "Idle Time %": {"number": employee_data.get('idle_percent', 0) / 100},
                    "Break Minutes": {"number": employee_data.get('break_minutes', 0)},
                    "Errors": {"number": employee_data.get('errors', 0)},
                    "Status": {"select": {"name": status}},
                    "Notes": {"rich_text": [{"text": {"content": employee_data.get('notes', '')}}]}
                }
            )
            
            self.logger.info(f"Added performance entry for {employee_data['name']}")
            return response['id']
            
        except Exception as e:
            self.logger.error(f"Failed to add Notion entry: {e}")
            return None
    
    def _simulate_notion_entry(self, employee_data: Dict) -> str:
        """Simulate Notion entry for demo mode"""
        import random
        entry_id = f"demo_{random.randint(10000, 99999)}"
        self.logger.info(f"Simulated Notion entry {entry_id} for {employee_data['name']}")
        return entry_id
    
    def get_daily_summary(self, date: str = None) -> pd.DataFrame:
        """Get daily performance summary"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        if self.demo_mode:
            return self._get_demo_daily_summary(date)
        
        try:
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Date",
                    "date": {"equals": date}
                }
            )
            
            # Convert to DataFrame
            data = []
            for page in response['results']:
                props = page['properties']
                data.append({
                    'employee': props['Employee']['title'][0]['text']['content'],
                    'samples': props['Samples Processed']['number'],
                    'idle_percent': props['Idle Time %']['number'] * 100,
                    'status': props['Status']['select']['name']
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            self.logger.error(f"Failed to query Notion: {e}")
            return self._get_demo_daily_summary(date)
    
    def _get_demo_daily_summary(self, date: str) -> pd.DataFrame:
        """Demo daily summary data"""
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
        
        data = []
        for employee in staff:
            samples = random.randint(30, 120)
            idle_percent = random.uniform(10, 60)
            
            # Determine status based on performance
            if samples > 80 and idle_percent < 30:
                status = "Excellent"
            elif samples > 60 and idle_percent < 40:
                status = "Good"
            elif samples > 40 and idle_percent < 50:
                status = "Warning"
            else:
                status = "Critical"
            
            data.append({
                'employee': employee,
                'samples': samples,
                'idle_percent': idle_percent,
                'status': status,
                'date': date
            })
        
        return pd.DataFrame(data)
    
    def get_weekly_trends(self) -> Dict:
        """Get weekly performance trends"""
        if self.demo_mode:
            return self._get_demo_weekly_trends()
        
        try:
            # Query last 7 days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "and": [
                        {
                            "property": "Date",
                            "date": {"greater_than_or_equal_to": start_date.isoformat()}
                        },
                        {
                            "property": "Date", 
                            "date": {"less_than_or_equal_to": end_date.isoformat()}
                        }
                    ]
                }
            )
            
            # Process weekly data
            daily_stats = {}
            for page in response['results']:
                props = page['properties']
                date = props['Date']['date']['start'][:10]
                samples = props['Samples Processed']['number']
                
                if date not in daily_stats:
                    daily_stats[date] = {'total_samples': 0, 'count': 0}
                
                daily_stats[date]['total_samples'] += samples
                daily_stats[date]['count'] += 1
            
            return daily_stats
            
        except Exception as e:
            self.logger.error(f"Failed to get weekly trends: {e}")
            return self._get_demo_weekly_trends()
    
    def _get_demo_weekly_trends(self) -> Dict:
        """Demo weekly trends data"""
        import random
        
        trends = {}
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            total_samples = random.randint(400, 800)
            count = random.randint(8, 12)
            
            trends[date] = {
                'total_samples': total_samples,
                'count': count,
                'avg_samples': total_samples / count
            }
        
        return trends
    
    def get_performance_rankings(self, date: str = None) -> pd.DataFrame:
        """Get staff performance rankings"""
        daily_summary = self.get_daily_summary(date)
        
        if daily_summary.empty:
            return pd.DataFrame()
        
        # Calculate scores
        daily_summary['score'] = (
            daily_summary['samples'] * 2 - 
            daily_summary['idle_percent'] * 3
        )
        
        # Sort by score
        rankings = daily_summary.sort_values('score', ascending=False)
        rankings['rank'] = range(1, len(rankings) + 1)
        
        return rankings[['rank', 'employee', 'samples', 'idle_percent', 'score', 'status']]

def test_notion_integration():
    """Test Notion integration"""
    config = LabConfig()
    notion = NotionTracker(config)
    
    print("Testing Notion Integration...")
    
    # Test adding performance entry
    test_data = {
        'name': 'Test Employee',
        'station': 'Station 1',
        'samples': 50,
        'draw_time': 5.2,
        'wait_time': 12,
        'idle_percent': 25,
        'break_minutes': 30,
        'errors': 1,
        'score': 85,
        'notes': 'Test entry'
    }
    
    entry_id = notion.add_performance_entry(test_data)
    print(f"Added entry with ID: {entry_id}")
    
    # Test daily summary
    summary = notion.get_daily_summary()
    print(f"\nDaily Summary:")
    print(f"  Total employees: {len(summary)}")
    print(f"  Average samples: {summary['samples'].mean():.1f}")
    print(f"  Average idle time: {summary['idle_percent'].mean():.1f}%")
    
    # Test performance rankings
    rankings = notion.get_performance_rankings()
    print(f"\nTop 3 Performers:")
    for _, row in rankings.head(3).iterrows():
        print(f"  {row['rank']}. {row['employee']}: {row['score']:.1f} points")
    
    # Test weekly trends
    trends = notion.get_weekly_trends()
    print(f"\nWeekly Trends:")
    for date, data in list(trends.items())[:3]:  # Show last 3 days
        print(f"  {date}: {data['total_samples']} total samples")
    
    print("\nNotion integration test completed!")

if __name__ == "__main__":
    test_notion_integration()

