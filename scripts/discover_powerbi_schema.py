#!/usr/bin/env python3
"""
Kaiser Permanente Lab Automation System
Power BI Schema Discovery Script

Discovers the exact field names required for your Power BI datasets.
"""

import os
import json
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

def test_minimal_fields():
    """Test with minimal field combinations to discover schema"""
    
    print("🔍 Discovering Power BI Dataset Schema...")
    print("=" * 60)
    
    # Common field name variations to try
    field_variations = [
        # Basic timestamp variations
        {"DateTime": datetime.now(timezone.utc).isoformat()},
        {"Timestamp": datetime.now(timezone.utc).isoformat()},
        {"Date": datetime.now(timezone.utc).date().isoformat()},
        {"Time": datetime.now(timezone.utc).time().isoformat()},
        
        # Single field tests
        {"Value": 1},
        {"Count": 1},
        {"Score": 85.5},
        {"Status": "Active"},
        {"Name": "Test"},
        {"ID": "TEST001"},
        
        # Lab-specific field attempts
        {"StaffMember": "Test User"},
        {"Staff": "Test User"},
        {"Employee": "Test User"},
        {"Technician": "Test User"},
        
        {"Samples": 25},
        {"SampleCount": 25},
        {"ProcessedSamples": 25},
        
        {"Errors": 1},
        {"ErrorCount": 1},
        {"ErrorRate": 2.5},
        
        {"TAT": 95.0},
        {"TATCompliance": 95.0},
        {"Compliance": 95.0},
        
        {"Performance": 88.5},
        {"PerformanceScore": 88.5},
        {"Score": 88.5},
        
        {"QC": 98.0},
        {"QCCompliance": 98.0},
        {"Quality": 98.0},
        
        {"Shift": "Day"},
        {"ShiftType": "Day"},
        {"Department": "Lab A"},
        {"Unit": "Lab A"},
        
        # Try empty object to see what fields are expected
        {}
    ]
    
    monitor_url = os.getenv("POWERBI_MONITOR_PUSH_URL")
    metrics_url = os.getenv("POWERBI_METRICS_PUSH_URL")
    
    print("\n📊 Testing Lab Performance Monitor Dataset...")
    print("-" * 40)
    
    successful_fields = []
    
    for i, test_data in enumerate(field_variations):
        try:
            response = requests.post(
                monitor_url,
                data=json.dumps([test_data]),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ SUCCESS #{i+1}: {test_data}")
                successful_fields.append(("Monitor", test_data))
            else:
                error_msg = response.text
                # Extract field name from error message
                if "Column" in error_msg and "was not found" in error_msg:
                    # Try to extract the expected field name from error
                    import re
                    match = re.search(r"Column '<pi>(.*?)</pi>' was not found", error_msg)
                    if match:
                        missing_field = match.group(1)
                        print(f"❌ Test #{i+1}: Missing field '{missing_field}'")
                    else:
                        print(f"❌ Test #{i+1}: {error_msg[:100]}...")
                else:
                    print(f"⚠️  Test #{i+1}: {response.status_code} - {error_msg[:100]}...")
                    
        except Exception as e:
            print(f"💥 Test #{i+1}: Error - {str(e)[:50]}...")
    
    print(f"\n📈 Testing Lab Performance Metrics Dataset...")
    print("-" * 40)
    
    for i, test_data in enumerate(field_variations):
        try:
            response = requests.post(
                metrics_url,
                data=json.dumps([test_data]),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ SUCCESS #{i+1}: {test_data}")
                successful_fields.append(("Metrics", test_data))
            else:
                error_msg = response.text
                if "Column" in error_msg and "was not found" in error_msg:
                    import re
                    match = re.search(r"Column '<pi>(.*?)</pi>' was not found", error_msg)
                    if match:
                        missing_field = match.group(1)
                        print(f"❌ Test #{i+1}: Missing field '{missing_field}'")
                    else:
                        print(f"❌ Test #{i+1}: {error_msg[:100]}...")
                else:
                    print(f"⚠️  Test #{i+1}: {response.status_code} - {error_msg[:100]}...")
                    
        except Exception as e:
            print(f"💥 Test #{i+1}: Error - {str(e)[:50]}...")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎯 DISCOVERY RESULTS")
    print("=" * 60)
    
    if successful_fields:
        print("✅ Successful field combinations:")
        for dataset, fields in successful_fields:
            print(f"   {dataset}: {fields}")
    else:
        print("❌ No successful field combinations found.")
        print("   This suggests the datasets may require specific field names.")
        print("   Check your Power BI streaming dataset configuration.")
    
    return successful_fields

def try_common_schemas():
    """Try common Power BI streaming dataset schemas"""
    
    print("\n🔬 Trying Common Power BI Schemas...")
    print("=" * 60)
    
    # Common streaming dataset schemas
    schemas_to_try = [
        # Schema 1: Basic lab monitoring
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "value": 85.5,
            "category": "performance"
        },
        
        # Schema 2: Simple metrics
        {
            "date": datetime.now(timezone.utc).date().isoformat(),
            "time": datetime.now(timezone.utc).time().strftime("%H:%M:%S"),
            "metric": 85.5,
            "status": "normal"
        },
        
        # Schema 3: Lab performance
        {
            "EventTime": datetime.now(timezone.utc).isoformat(),
            "MetricName": "Performance",
            "MetricValue": 85.5,
            "Unit": "Lab A"
        },
        
        # Schema 4: Minimal required
        {
            "id": 1,
            "value": 85.5
        },
        
        # Schema 5: Just timestamp
        {
            "ts": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    monitor_url = os.getenv("POWERBI_MONITOR_PUSH_URL")
    
    for i, schema in enumerate(schemas_to_try):
        print(f"\n📊 Testing Schema #{i+1}: {schema}")
        
        try:
            response = requests.post(
                monitor_url,
                data=json.dumps([schema]),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ SUCCESS! Schema #{i+1} works!")
                return schema
            else:
                print(f"❌ Failed: {response.text[:150]}...")
                
        except Exception as e:
            print(f"💥 Error: {str(e)}")
    
    return None

def create_working_powerbi_client():
    """Create a Power BI client that works with discovered schema"""
    
    print("\n🔧 Creating Working Power BI Integration...")
    print("=" * 60)
    
    # Try the most basic possible data structure
    basic_test = {
        "DateTime": datetime.now(timezone.utc).isoformat(),
        "Value": 1,
        "Status": "Test"
    }
    
    monitor_url = os.getenv("POWERBI_MONITOR_PUSH_URL")
    
    try:
        response = requests.post(
            monitor_url,
            data=json.dumps([basic_test]),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Basic test successful!")
            print("   Power BI is accepting data with this structure:")
            print(f"   {basic_test}")
            
            # Try to send lab-relevant data
            lab_data = {
                "DateTime": datetime.now(timezone.utc).isoformat(),
                "Value": 88.5,
                "Status": "Kaiser Permanente Lab Automation Active"
            }
            
            response2 = requests.post(
                monitor_url,
                data=json.dumps([lab_data]),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response2.status_code == 200:
                print("✅ Lab data sent successfully!")
                print("   Your Power BI dashboard should now show:")
                print(f"   {lab_data}")
                return True
            else:
                print(f"⚠️  Lab data failed: {response2.text}")
                return False
                
        else:
            print(f"❌ Basic test failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return False

def main():
    """Main discovery function"""
    
    print("🚀 Kaiser Permanente Lab Automation - Power BI Schema Discovery")
    print("=" * 80)
    
    # Check environment variables
    monitor_url = os.getenv("POWERBI_MONITOR_PUSH_URL")
    metrics_url = os.getenv("POWERBI_METRICS_PUSH_URL")
    
    if not monitor_url or not metrics_url:
        print("❌ Power BI URLs not found in environment variables")
        return False
    
    print(f"📊 Monitor URL: {monitor_url[:50]}...")
    print(f"📈 Metrics URL: {metrics_url[:50]}...")
    
    # Run discovery tests
    successful_fields = test_minimal_fields()
    
    if not successful_fields:
        # Try common schemas
        working_schema = try_common_schemas()
        
        if not working_schema:
            # Try basic integration
            basic_success = create_working_powerbi_client()
            
            if basic_success:
                print("\n🎉 SUCCESS! Basic Power BI integration is working!")
                print("   You can now build upon this basic structure.")
            else:
                print("\n❌ Unable to establish Power BI connection.")
                print("   Please check your Power BI streaming dataset configuration.")
                return False
        else:
            print(f"\n🎉 SUCCESS! Found working schema: {working_schema}")
    else:
        print(f"\n🎉 SUCCESS! Found {len(successful_fields)} working field combinations!")
    
    print("\n📋 Next Steps:")
    print("1. Use the working field structure discovered above")
    print("2. Update the enhanced_powerbi_client.py with correct field names")
    print("3. Test the full lab automation system")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

