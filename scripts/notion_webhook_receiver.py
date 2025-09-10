#!/usr/bin/env python3
"""
Simple Notion Webhook Receiver
Logs all incoming webhook requests for debugging
"""

import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
import logging

# Setup logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('notion_webhook_requests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/webhook', methods=['POST', 'GET'])
def webhook_handler():
    """Handle all webhook requests from Notion"""
    try:
        logger.info(f"=== Received {request.method} request ===")
        logger.info(f"URL: {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        if request.method == 'POST':
            # Get raw data
            raw_data = request.get_data(as_text=True)
            logger.info(f"Raw Body: {raw_data}")
            
            # Try to parse as JSON
            try:
                json_data = request.get_json()
                logger.info(f"JSON Data: {json.dumps(json_data, indent=2)}")
                
                # Check for verification token
                if 'verification' in json_data:
                    verification_token = json_data.get('verification')
                    logger.info(f"🔑 VERIFICATION TOKEN RECEIVED: {verification_token}")
                    
                    # Notion expects just the token string as plain text response
                    return verification_token, 200
                    
            except Exception as e:
                logger.info(f"Could not parse as JSON: {e}")
            
            # Save request to file for analysis
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"webhook_request_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump({
                    'timestamp': timestamp,
                    'headers': dict(request.headers),
                    'body': raw_data,
                    'url': request.url,
                    'method': request.method
                }, f, indent=2)
            logger.info(f"Request saved to {filename}")
            
            return jsonify({"status": "received"}), 200
            
        else:  # GET request
            return jsonify({
                "status": "webhook receiver running",
                "timestamp": datetime.now().isoformat(),
                "message": "Waiting for Notion verification token..."
            }), 200
            
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Notion Webhook Receiver...")
    print("📡 Webhook endpoint: http://localhost:5001/webhook")
    print("🔍 All requests will be logged to notion_webhook_requests.log")
    print("⏳ Waiting for Notion verification token...")
    print("\n👉 Configure your Notion webhook to point to:")
    print("   https://kaiserpermanente.webhook.office.com/webhook")
    print("   (or your ngrok/public URL if testing locally)")
    
    app.run(host='0.0.0.0', port=5001, debug=True)