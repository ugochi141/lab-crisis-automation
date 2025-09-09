#!/usr/bin/env python3
"""
Lab Crisis System Diagnostics
Comprehensive health check and troubleshooting
"""

import os
import sys
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    """Check environment configuration"""
    print("🔍 Environment Configuration Check")
    print("-" * 40)
    
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
            print(f"❌ {var}: Not configured")
        else:
            print(f"✅ {var}: Configured")
    
    if missing_vars:
        print(f"\n⚠️ Missing configuration: {', '.join(missing_vars)}")
        print("Please update your .env file with actual values")
        return False
    
    return True

def check_notion_connection():
    """Check Notion API connection"""
    print("\n🔍 Notion API Connection Check")
    print("-" * 40)
    
    token = os.getenv('NOTION_API_TOKEN')
    if not token or token == 'your_notion_token_here':
        print("❌ Notion token not configured")
        return False
    
    try:
        from notion_client import Client
        notion = Client(auth=token)
        user = notion.users.me()
        print(f"✅ Notion connected as: {user.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"❌ Notion connection failed: {e}")
        return False

def check_teams_webhook():
    """Check Teams webhook"""
    print("\n🔍 Teams Webhook Check")
    print("-" * 40)
    
    webhook = os.getenv('TEAMS_WEBHOOK_URL')
    if not webhook or webhook == 'your_teams_webhook_url_here':
        print("❌ Teams webhook not configured")
        return False
    
    try:
        payload = {
            "text": f"🔍 Lab Crisis System - Health Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        response = requests.post(webhook, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Teams webhook working")
            return True
        else:
            print(f"❌ Teams webhook failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Teams webhook error: {e}")
        return False

def check_dependencies():
    """Check Python dependencies"""
    print("\n🔍 Dependencies Check")
    print("-" * 40)
    
    required_packages = [
        'requests',
        'pandas',
        'notion_client',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}: Installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}: Missing")
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Run all diagnostics"""
    print("🏥 Lab Crisis System Diagnostics")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    checks = [
        check_environment(),
        check_dependencies(),
        check_notion_connection(),
        check_teams_webhook()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print("\n" + "=" * 50)
    print(f"📊 Diagnostic Summary: {passed}/{total} checks passed")
    
    if passed == total:
        print("✅ All systems operational!")
        return True
    else:
        print("❌ Some issues detected. Please fix the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
