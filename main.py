#!/usr/bin/env python3
"""
Main entry point for Railway deployment
"""

import sys
import os
from pathlib import Path

# Add the scripts directory to the path
current_dir = Path(__file__).parent
scripts_dir = current_dir / 'scripts'
sys.path.insert(0, str(scripts_dir))

# Import the Flask app from the webhook server
try:
    from notion_webhook_server import app
    print("✅ Successfully imported Flask app")
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    # Use PORT for cloud platforms (Railway, Heroku, etc.)
    port = int(os.getenv('PORT', 8080))
    
    print(f"🚀 Starting Notion Webhook Server on port {port}")
    print(f"📡 Webhook endpoint: /webhook/notion")
    print(f"✅ Verification endpoint: /webhook/notion/verify")
    print(f"🏥 Health check: /health")
    
    app.run(host='0.0.0.0', port=port, debug=False)