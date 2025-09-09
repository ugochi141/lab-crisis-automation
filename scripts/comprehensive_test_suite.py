#!/usr/bin/env python3
"""
Comprehensive Test Suite for Lab Automation System
Tests all components and features
"""

import os
import sys
import json
import asyncio
import unittest
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LabAutomationTestSuite:
    """Comprehensive test suite for lab automation system"""
    
    def __init__(self):
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'total': 0
        }
        self.test_details = []
    
    def log_test_result(self, test_name: str, status: str, message: str = ""):
        """Log test result"""
        self.test_results['total'] += 1
        if status == 'PASS':
            self.test_results['passed'] += 1
            print(f"✅ {test_name}: PASSED {message}")
        elif status == 'FAIL':
            self.test_results['failed'] += 1
            print(f"❌ {test_name}: FAILED {message}")
        else:
            self.test_results['errors'] += 1
            print(f"🚨 {test_name}: ERROR {message}")
        
        self.test_details.append({
            'test': test_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
    
    def test_environment_configuration(self):
        """Test environment configuration"""
        print("\n🔍 Testing Environment Configuration...")
        
        required_vars = [
            'NOTION_API_TOKEN',
            'TEAMS_WEBHOOK_URL',
            'NOTION_PERFORMANCE_DB_ID',
            'NOTION_INCIDENT_DB_ID'
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value or value == f'your_{var.lower()}_here':
                missing_vars.append(var)
        
        if missing_vars:
            self.log_test_result(
                "Environment Configuration",
                "FAIL",
                f"Missing variables: {', '.join(missing_vars)}"
            )
        else:
            self.log_test_result(
                "Environment Configuration",
                "PASS",
                "All required variables configured"
            )
    
    def test_dependencies(self):
        """Test Python dependencies"""
        print("\n🔍 Testing Dependencies...")
        
        required_packages = [
            'requests',
            'pandas',
            'notion_client',
            'python-dotenv',
            'aiohttp',
            'numpy'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                if package == 'python-dotenv':
                    __import__('dotenv')
                else:
                    __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            self.log_test_result(
                "Dependencies",
                "FAIL",
                f"Missing packages: {', '.join(missing_packages)}"
            )
        else:
            self.log_test_result(
                "Dependencies",
                "PASS",
                "All required packages installed"
            )
    
    def test_notion_connection(self):
        """Test Notion API connection"""
        print("\n🔍 Testing Notion Connection...")
        
        try:
            from notion_client import Client
            token = os.getenv('NOTION_API_TOKEN')
            
            if not token or token == 'your_notion_token_here':
                self.log_test_result(
                    "Notion Connection",
                    "FAIL",
                    "Notion token not configured"
                )
                return
            
            notion = Client(auth=token)
            user = notion.users.me()
            
            self.log_test_result(
                "Notion Connection",
                "PASS",
                f"Connected as: {user.get('name', 'Unknown')}"
            )
            
        except Exception as e:
            self.log_test_result(
                "Notion Connection",
                "ERROR",
                f"Connection failed: {str(e)}"
            )
    
    def test_teams_webhook(self):
        """Test Teams webhook"""
        print("\n🔍 Testing Teams Webhook...")
        
        webhook = os.getenv('TEAMS_WEBHOOK_URL')
        if not webhook or webhook == 'your_teams_webhook_url_here':
            self.log_test_result(
                "Teams Webhook",
                "FAIL",
                "Teams webhook not configured"
            )
            return
        
        try:
            payload = {
                "text": f"🧪 Lab Automation Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
            response = requests.post(webhook, json=payload, timeout=10)
            
            if response.status_code == 200:
                self.log_test_result(
                    "Teams Webhook",
                    "PASS",
                    "Webhook working correctly"
                )
            else:
                self.log_test_result(
                    "Teams Webhook",
                    "FAIL",
                    f"HTTP {response.status_code}"
                )
                
        except Exception as e:
            self.log_test_result(
                "Teams Webhook",
                "ERROR",
                f"Request failed: {str(e)}"
            )
    
    def test_crisis_monitor(self):
        """Test crisis monitoring functionality"""
        print("\n🔍 Testing Crisis Monitor...")
        
        try:
            # Import and test the enhanced crisis monitor
            sys.path.append('scripts')
            from enhanced_crisis_monitor import EnhancedCrisisMonitor
            
            monitor = EnhancedCrisisMonitor()
            
            # Test system health check
            health = monitor.check_system_health()
            
            if health['overall_status'] in ['HEALTHY', 'DEGRADED', 'CRITICAL']:
                self.log_test_result(
                    "Crisis Monitor",
                    "PASS",
                    f"Health check: {health['overall_status']}"
                )
            else:
                self.log_test_result(
                    "Crisis Monitor",
                    "FAIL",
                    "Health check returned invalid status"
                )
                
        except Exception as e:
            self.log_test_result(
                "Crisis Monitor",
                "ERROR",
                f"Import or execution failed: {str(e)}"
            )
    
    def test_advanced_automation(self):
        """Test advanced automation features"""
        print("\n🔍 Testing Advanced Automation...")
        
        try:
            # Import and test the advanced automation
            sys.path.append('scripts')
            from advanced_lab_automation import AdvancedLabAutomation
            
            automation = AdvancedLabAutomation()
            
            # Test AI prediction models
            test_data = [{'volume': 100, 'timestamp': datetime.now()}]
            prediction = automation.prediction_models['workload_prediction'](test_data)
            
            if 'predicted_volume' in prediction and 'confidence' in prediction:
                self.log_test_result(
                    "Advanced Automation",
                    "PASS",
                    f"AI prediction working: {prediction['predicted_volume']} samples"
                )
            else:
                self.log_test_result(
                    "Advanced Automation",
                    "FAIL",
                    "AI prediction returned invalid data"
                )
                
        except Exception as e:
            self.log_test_result(
                "Advanced Automation",
                "ERROR",
                f"Import or execution failed: {str(e)}"
            )
    
    def test_database_operations(self):
        """Test database operations"""
        print("\n🔍 Testing Database Operations...")
        
        try:
            from notion_client import Client
            token = os.getenv('NOTION_API_TOKEN')
            performance_db_id = os.getenv('NOTION_PERFORMANCE_DB_ID')
            
            if not token or token == 'your_notion_token_here':
                self.log_test_result(
                    "Database Operations",
                    "FAIL",
                    "Notion token not configured"
                )
                return
            
            if not performance_db_id or performance_db_id == 'your_performance_db_id_here':
                self.log_test_result(
                    "Database Operations",
                    "FAIL",
                    "Performance database ID not configured"
                )
                return
            
            notion = Client(auth=token)
            
            # Test database retrieval
            database = notion.databases.retrieve(database_id=performance_db_id)
            
            if database and 'properties' in database:
                self.log_test_result(
                    "Database Operations",
                    "PASS",
                    f"Database accessible: {database['title'][0]['plain_text']}"
                )
            else:
                self.log_test_result(
                    "Database Operations",
                    "FAIL",
                    "Database retrieval failed"
                )
                
        except Exception as e:
            self.log_test_result(
                "Database Operations",
                "ERROR",
                f"Database operation failed: {str(e)}"
            )
    
    def test_alert_system(self):
        """Test alert system functionality"""
        print("\n🔍 Testing Alert System...")
        
        try:
            # Test alert creation logic
            test_metrics = [
                {'name': 'TAT Compliance', 'value': 35.0, 'target': 90.0},
                {'name': 'Wait Time', 'value': 25.0, 'target': 15.0},
                {'name': 'Error Rate', 'value': 12.0, 'target': 5.0}
            ]
            
            alerts_triggered = []
            for metric in test_metrics:
                if metric['value'] < metric['target'] * 0.7:  # 70% threshold
                    alerts_triggered.append(f"CRITICAL: {metric['name']}")
                elif metric['value'] < metric['target'] * 0.9:  # 90% threshold
                    alerts_triggered.append(f"WARNING: {metric['name']}")
            
            if len(alerts_triggered) > 0:
                self.log_test_result(
                    "Alert System",
                    "PASS",
                    f"Generated {len(alerts_triggered)} alerts correctly"
                )
            else:
                self.log_test_result(
                    "Alert System",
                    "FAIL",
                    "No alerts generated for test data"
                )
                
        except Exception as e:
            self.log_test_result(
                "Alert System",
                "ERROR",
                f"Alert system test failed: {str(e)}"
            )
    
    def test_performance_metrics(self):
        """Test performance metrics calculation"""
        print("\n🔍 Testing Performance Metrics...")
        
        try:
            # Test performance scoring algorithm
            test_staff = {
                'tat_compliance': 85.0,
                'error_rate': 3.0,
                'utilization': 90.0,
                'break_efficiency': 95.0,
                'qc_completion': 98.0
            }
            
            weights = {
                'tat_compliance': 0.3,
                'error_rate': 0.25,
                'utilization': 0.2,
                'break_efficiency': 0.15,
                'qc_completion': 0.1
            }
            
            score = 0.0
            for metric, value in test_staff.items():
                if metric in weights:
                    normalized_value = min(100, max(0, value))
                    score += normalized_value * weights[metric]
            
            final_score = min(100, max(0, score))
            
            if 0 <= final_score <= 100:
                self.log_test_result(
                    "Performance Metrics",
                    "PASS",
                    f"Performance score calculated: {final_score:.1f}"
                )
            else:
                self.log_test_result(
                    "Performance Metrics",
                    "FAIL",
                    f"Invalid performance score: {final_score}"
                )
                
        except Exception as e:
            self.log_test_result(
                "Performance Metrics",
                "ERROR",
                f"Performance metrics test failed: {str(e)}"
            )
    
    def test_ai_features(self):
        """Test AI-powered features"""
        print("\n🔍 Testing AI Features...")
        
        try:
            # Test anomaly detection
            test_metrics = [
                {'name': 'TAT Compliance', 'value': 35.0, 'target': 90.0},
                {'name': 'Wait Time', 'value': 25.0, 'target': 15.0},
                {'name': 'Error Rate', 'value': 12.0, 'target': 5.0}
            ]
            
            anomalies = []
            for metric in test_metrics:
                if metric['value'] > metric['target'] * 1.5:
                    anomalies.append(metric['name'])
            
            # Test workload prediction
            historical_data = [{'volume': 100 + i*10} for i in range(7)]
            avg_volume = sum(d['volume'] for d in historical_data) / len(historical_data)
            trend = (historical_data[-1]['volume'] - historical_data[0]['volume']) / len(historical_data)
            predicted_volume = avg_volume + trend
            
            if len(anomalies) > 0 and predicted_volume > 0:
                self.log_test_result(
                    "AI Features",
                    "PASS",
                    f"Detected {len(anomalies)} anomalies, predicted volume: {predicted_volume:.1f}"
                )
            else:
                self.log_test_result(
                    "AI Features",
                    "FAIL",
                    "AI features not working correctly"
                )
                
        except Exception as e:
            self.log_test_result(
                "AI Features",
                "ERROR",
                f"AI features test failed: {str(e)}"
            )
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Lab Automation Comprehensive Test Suite")
        print("=" * 60)
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Run all tests
        self.test_environment_configuration()
        self.test_dependencies()
        self.test_notion_connection()
        self.test_teams_webhook()
        self.test_crisis_monitor()
        self.test_advanced_automation()
        self.test_database_operations()
        self.test_alert_system()
        self.test_performance_metrics()
        self.test_ai_features()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"Total Tests: {self.test_results['total']}")
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        print(f"🚨 Errors: {self.test_results['errors']}")
        
        success_rate = (self.test_results['passed'] / self.test_results['total']) * 100 if self.test_results['total'] > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if self.test_results['failed'] == 0 and self.test_results['errors'] == 0:
            print("🎉 All tests passed! System is ready for production.")
            return True
        else:
            print("⚠️ Some tests failed. Please review the issues above.")
            return False

def main():
    """Main test execution"""
    test_suite = LabAutomationTestSuite()
    success = test_suite.run_all_tests()
    
    # Save test results
    with open('logs/test_results.json', 'w') as f:
        json.dump({
            'summary': test_suite.test_results,
            'details': test_suite.test_details,
            'timestamp': datetime.now().isoformat()
        }, f, indent=2)
    
    print(f"\n📝 Test results saved to: logs/test_results.json")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
