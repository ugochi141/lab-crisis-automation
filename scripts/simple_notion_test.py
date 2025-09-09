#!/usr/bin/env python3
"""
Simple Notion Connection Test
"""

import asyncio
import aiohttp
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_notion_connection():
    """Test Notion API connection"""
    
    # Load token from environment
    TOKEN = os.getenv('NOTION_API_TOKEN')
    
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # Test basic API access
            print("🧪 Testing Notion API connection...")
            
            # Try to list users (basic API test)
            async with session.get(
                "https://api.notion.com/v1/users",
                headers=headers
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ API Connection successful!")
                    print(f"   Found {len(data.get('results', []))} users")
                else:
                    print(f"❌ API Connection failed: {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
                    
        except Exception as e:
            print(f"❌ Connection test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_notion_connection())
