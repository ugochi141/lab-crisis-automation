#!/usr/bin/env python3
"""
Notion Webhook Setup Helper
Helps set up and verify Notion webhook endpoints
"""

import asyncio
import aiohttp
import json
import os
import subprocess
import time
import signal
import sys
from dotenv import load_dotenv

load_dotenv()

class NotionWebhookSetup:
    def __init__(self):
        self.webhook_server_process = None
        self.webhook_port = int(os.getenv('WEBHOOK_PORT', 5000))
        self.notion_token = os.getenv('NOTION_API_TOKEN_PRIMARY') or os.getenv('NOTION_API_TOKEN')
        
    def start_webhook_server(self):
        """Start the webhook server in background"""
        print("🚀 Starting Notion webhook server...")
        
        try:
            self.webhook_server_process = subprocess.Popen([
                sys.executable, 'scripts/notion_webhook_server.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            if self.webhook_server_process.poll() is None:
                print(f"✅ Webhook server started on port {self.webhook_port}")
                return True
            else:
                print("❌ Failed to start webhook server")
                return False
                
        except Exception as e:
            print(f"❌ Error starting webhook server: {e}")
            return False
    
    def stop_webhook_server(self):
        """Stop the webhook server"""
        if self.webhook_server_process:
            print("🛑 Stopping webhook server...")
            self.webhook_server_process.terminate()
            self.webhook_server_process.wait()
            print("✅ Webhook server stopped")
    
    async def test_webhook_endpoint(self):
        """Test if webhook endpoint is accessible"""
        url = f"http://localhost:{self.webhook_port}/webhook/notion/verify"
        
        print(f"🧪 Testing webhook endpoint: {url}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ Webhook endpoint is accessible")
                        print(f"   Response: {data['message']}")
                        return True
                    else:
                        print(f"❌ Webhook endpoint returned {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Failed to connect to webhook endpoint: {e}")
            return False
    
    async def test_verification_challenge(self):
        """Test webhook verification challenge response"""
        url = f"http://localhost:{self.webhook_port}/webhook/notion/verify"
        
        print("🔐 Testing webhook verification challenge...")
        
        challenge_data = {
            "challenge": "test_challenge_12345"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=challenge_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('challenge') == challenge_data['challenge']:
                            print("✅ Webhook verification challenge works correctly")
                            return True
                        else:
                            print("❌ Webhook challenge response incorrect")
                            return False
                    else:
                        print(f"❌ Webhook challenge test failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Webhook challenge test error: {e}")
            return False
    
    def print_setup_instructions(self):
        """Print instructions for setting up the webhook in Notion"""
        print("\n" + "="*60)
        print("📋 NOTION WEBHOOK SETUP INSTRUCTIONS")
        print("="*60)
        print("\n1. Go to your Notion workspace settings")
        print("2. Navigate to 'Integrations' → 'Webhooks'")
        print("3. Click 'Add webhook'")
        print("4. Configure the webhook:")
        print(f"   • Endpoint URL: http://your-domain.com:{self.webhook_port}/webhook/notion")
        print("   • Secret: (optional, set NOTION_WEBHOOK_SECRET in .env)")
        print("   • Events: Select the events you want to monitor")
        print("\n5. For local testing, you'll need to expose your local server:")
        print(f"   • Use ngrok: ngrok http {self.webhook_port}")
        print("   • Or use a cloud service to host the webhook")
        print("\n6. For production, deploy the webhook server to:")
        print("   • Heroku, AWS Lambda, Google Cloud Functions, etc.")
        print("\n📝 Current webhook endpoints:")
        print(f"   • Main webhook: http://localhost:{self.webhook_port}/webhook/notion")
        print(f"   • Verification: http://localhost:{self.webhook_port}/webhook/notion/verify")
        print(f"   • Health check: http://localhost:{self.webhook_port}/health")
        print("\n" + "="*60)
    
    async def run_setup(self):
        """Run the complete webhook setup process"""
        print("🔧 Notion Webhook Setup")
        print("="*30)
        
        # Start webhook server
        if not self.start_webhook_server():
            return False
        
        try:
            # Test endpoint
            if not await self.test_webhook_endpoint():
                return False
            
            # Test verification
            if not await self.test_verification_challenge():
                return False
            
            print("\n✅ Webhook server is ready for verification!")
            
            # Print setup instructions
            self.print_setup_instructions()
            
            # Keep server running
            print("\n🔄 Webhook server is running. Press Ctrl+C to stop.")
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down...")
                
        finally:
            self.stop_webhook_server()
        
        return True

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Received interrupt signal. Shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Handle Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    setup = NotionWebhookSetup()
    
    try:
        asyncio.run(setup.run_setup())
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        if setup.webhook_server_process:
            setup.stop_webhook_server()