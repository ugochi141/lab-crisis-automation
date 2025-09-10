#!/usr/bin/env python3
"""
Integration Test Suite for Kaiser Lab Alert System
Tests Notion, Power Automate, and GitHub integrations
"""

import os
import json
import requests
from datetime import datetime
import time

class LabAlertTester:
    """Test suite for lab alert system integration"""
    
    def __init__(self):
        self.notion_token = os.environ.get('NOTION_API_TOKEN')
        self.notion_db_id = os.environ.get('NOTION_ALERTS_DB_ID') 
        self.teams_webhook = os.environ.get('TEAMS_WEBHOOK_URL')
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.github_repo = os.environ.get('GITHUB_REPOSITORY', 'ugochi141/lab-crisis-automation')
        
        self.test_results = []
        
    def log_result(self, test_name, success, message="", details=None):
        """Log test result"""
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
    def test_notion_connection(self):
        """Test Notion API connection"""
        if not self.notion_token:
            self.log_result("Notion Connection", False, "NOTION_API_TOKEN not set")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Notion-Version': '2022-06-28'
        }
        
        try:
            response = requests.get('https://api.notion.com/v1/users/me', headers=headers)
            if response.status_code == 200:
                user_info = response.json()
                self.log_result("Notion Connection", True, f"Connected as {user_info.get('name', 'Unknown')}")
                return True
            else:
                self.log_result("Notion Connection", False, f"API returned {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Notion Connection", False, f"Exception: {e}")
            return False
    
    def test_notion_database(self):
        """Test Notion database access"""
        if not self.notion_token or not self.notion_db_id:
            self.log_result("Notion Database", False, "Token or Database ID not set")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Notion-Version': '2022-06-28'
        }
        
        try:
            response = requests.get(f'https://api.notion.com/v1/databases/{self.notion_db_id}', headers=headers)
            if response.status_code == 200:
                db_info = response.json()
                self.log_result("Notion Database", True, f"Database accessible: {db_info.get('title', [{}])[0].get('text', {}).get('content', 'Unknown')}")
                return True
            else:
                self.log_result("Notion Database", False, f"Database not accessible: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Notion Database", False, f"Exception: {e}")
            return False
    
    def test_create_notion_entry(self):
        """Test creating a Notion database entry"""
        if not self.notion_token or not self.notion_db_id:
            self.log_result("Create Notion Entry", False, "Token or Database ID not set")
            return False
            
        headers = {
            'Authorization': f'Bearer {self.notion_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        
        test_data = {
            'parent': {'database_id': self.notion_db_id},
            'properties': {
                'Alert ID': {
                    'title': [{'text': {'content': f'TEST-{datetime.now().strftime("%Y%m%d-%H%M%S")}'}}]
                },
                'Severity': {
                    'select': {'name': '🔴 Critical'}
                },
                'Message': {
                    'rich_text': [{'text': {'content': 'Integration test alert - please ignore'}}]
                },
                'Timestamp': {
                    'date': {'start': datetime.now().isoformat()}
                },
                'Status': {
                    'select': {'name': '🟥 Open'}
                },
                'Source': {
                    'select': {'name': 'Manual Entry'}
                }
            }
        }
        
        try:
            response = requests.post('https://api.notion.com/v1/pages', headers=headers, json=test_data)
            if response.status_code == 200:
                page_info = response.json()
                self.log_result("Create Notion Entry", True, f"Entry created: {page_info.get('id')}")
                return True
            else:
                self.log_result("Create Notion Entry", False, f"Failed to create entry: {response.status_code}", response.text)
                return False
        except Exception as e:
            self.log_result("Create Notion Entry", False, f"Exception: {e}")
            return False
    
    def test_teams_webhook(self):
        """Test Teams webhook notification"""
        if not self.teams_webhook:
            self.log_result("Teams Webhook", False, "TEAMS_WEBHOOK_URL not set")
            return False
            
        test_message = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "FF0000",
            "summary": "Integration Test Alert",
            "sections": [{
                "activityTitle": "🧪 INTEGRATION TEST",
                "activitySubtitle": "Kaiser Lab Alert System Test",
                "facts": [
                    {"name": "Test Type", "value": "Teams Webhook"},
                    {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
                    {"name": "Status", "value": "Testing webhook functionality"}
                ],
                "markdown": True
            }]
        }
        
        try:
            response = requests.post(self.teams_webhook, json=test_message)
            if response.status_code == 200:
                self.log_result("Teams Webhook", True, "Test message sent successfully")
                return True
            else:
                self.log_result("Teams Webhook", False, f"Failed to send message: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("Teams Webhook", False, f"Exception: {e}")
            return False
    
    def test_github_dispatch(self):
        """Test GitHub repository dispatch"""
        if not self.github_token:
            self.log_result("GitHub Dispatch", False, "GITHUB_TOKEN not set")
            return False
            
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.everest-preview+json',
            'Content-Type': 'application/json'
        }
        
        dispatch_data = {
            'event_type': 'lab_alert',
            'client_payload': {
                'message': 'Integration test alert - automated testing',
                'severity': 'Critical',
                'timestamp': datetime.now().isoformat(),
                'sender': 'Integration Tester',
                'department': 'IT Systems',
                'alert_id': f'TEST-{datetime.now().strftime("%Y%m%d-%H%M%S")}'
            }
        }
        
        try:
            response = requests.post(
                f'https://api.github.com/repos/{self.github_repo}/dispatches',
                headers=headers,
                json=dispatch_data
            )
            if response.status_code == 204:
                self.log_result("GitHub Dispatch", True, "Repository dispatch sent successfully")
                return True
            else:
                self.log_result("GitHub Dispatch", False, f"Failed to send dispatch: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("GitHub Dispatch", False, f"Exception: {e}")
            return False
    
    def test_keyword_detection(self):
        """Test keyword detection logic"""
        test_messages = [
            ("Chemistry analyzer down - need STAT coverage", ["stat", "coverage", "analyzer down"], "Critical"),
            ("Calling out sick today - can't make it in", ["calling out", "sick today"], "High"),
            ("Running late due to traffic", ["late"], "Medium"),
            ("FMLA paperwork due next week", ["fmla"], "Compliance"),
            ("Schedule change for tomorrow", ["schedule"], "Low")
        ]
        
        keyword_categories = {
            'critical': ['stat', 'critical value', 'emergency', 'system down', 'analyzer down', 'no coverage'],
            'high': ['calling out', 'sick today', 'short staffed', 'qc failure'],
            'medium': ['late', 'supplies low', 'maintenance'],
            'compliance': ['fmla', 'medical leave', 'disciplinary action'],
            'low': ['schedule', 'vacation', 'attendance']
        }
        
        all_passed = True
        for message, expected_keywords, expected_severity in test_messages:
            message_lower = message.lower()
            detected_keywords = []
            detected_severity = "Low"
            
            # Check for keywords
            for category, keywords in keyword_categories.items():
                for keyword in keywords:
                    if keyword in message_lower:
                        detected_keywords.append(keyword)
                        if category == 'critical':
                            detected_severity = "Critical"
                        elif category == 'high' and detected_severity not in ['Critical']:
                            detected_severity = "High"
                        elif category == 'medium' and detected_severity not in ['Critical', 'High']:
                            detected_severity = "Medium"
                        elif category == 'compliance' and detected_severity not in ['Critical', 'High', 'Medium']:
                            detected_severity = "Compliance"
            
            # Validate results
            keywords_match = any(keyword in detected_keywords for keyword in expected_keywords)
            severity_match = detected_severity == expected_severity
            
            if keywords_match and severity_match:
                self.log_result(f"Keyword Detection: {message[:30]}...", True, f"Detected: {detected_keywords}, Severity: {detected_severity}")
            else:
                self.log_result(f"Keyword Detection: {message[:30]}...", False, f"Expected: {expected_keywords}/{expected_severity}, Got: {detected_keywords}/{detected_severity}")
                all_passed = False
        
        return all_passed
    
    def run_comprehensive_test(self):
        """Run all integration tests"""
        print("🧪 Starting Kaiser Lab Alert System Integration Tests")
        print("=" * 60)
        
        # Test individual components
        self.test_notion_connection()
        self.test_notion_database()
        self.test_create_notion_entry()
        self.test_teams_webhook()
        self.test_github_dispatch()
        self.test_keyword_detection()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = len([r for r in self.test_results if r['success']])
        failed = len([r for r in self.test_results if not r['success']])
        total = len(self.test_results)
        
        print(f"✅ Passed: {passed}/{total}")
        print(f"❌ Failed: {failed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  • {result['test']}: {result['message']}")
        
        # Save detailed results
        results_file = f"integration_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                'summary': {
                    'total_tests': total,
                    'passed': passed,
                    'failed': failed,
                    'success_rate': (passed/total)*100,
                    'test_date': datetime.now().isoformat()
                },
                'results': self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: {results_file}")
        
        return failed == 0

def main():
    """Main test function"""
    print("🏥 Kaiser Permanente Lab Alert System - Integration Test Suite")
    print("Testing all components: Notion, Teams, GitHub, and Keyword Detection")
    print("")
    
    # Check environment variables
    required_vars = ['NOTION_API_TOKEN', 'NOTION_ALERTS_DB_ID']
    optional_vars = ['TEAMS_WEBHOOK_URL', 'GITHUB_TOKEN']
    
    print("🔍 Environment Check:")
    for var in required_vars:
        if os.environ.get(var):
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ❌ {var}: Missing (REQUIRED)")
    
    for var in optional_vars:
        if os.environ.get(var):
            print(f"  ✅ {var}: Configured")
        else:
            print(f"  ⚠️  {var}: Missing (optional)")
    
    print("")
    
    # Run tests
    tester = LabAlertTester()
    success = tester.run_comprehensive_test()
    
    if success:
        print("\n🎉 ALL TESTS PASSED! Your integration is ready for production.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the issues above.")
        return 1

if __name__ == "__main__":
    exit(main())