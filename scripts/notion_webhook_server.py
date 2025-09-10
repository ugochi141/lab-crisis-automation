#!/usr/bin/env python3
"""
Notion Webhook Verification Server
Handles Notion webhook verification and event processing
"""

from flask import Flask, request, jsonify
import json
import hmac
import hashlib
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Webhook configuration
WEBHOOK_SECRET = os.getenv('NOTION_WEBHOOK_SECRET', 'your_webhook_secret_here')

@app.route('/webhook/notion', methods=['POST'])
def notion_webhook():
    """Handle Notion webhook events"""
    
    try:
        # Get request data
        payload = request.get_data()
        signature = request.headers.get('Notion-Webhook-Signature')
        
        logger.info(f"Received webhook request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        
        # Check if this is a verification request
        if request.headers.get('Notion-Webhook-Type') == 'url_verification':
            logger.info("Handling URL verification challenge")
            
            # Parse the challenge
            try:
                data = json.loads(payload)
                challenge = data.get('challenge')
                
                if challenge:
                    logger.info(f"Responding to challenge: {challenge}")
                    return jsonify({'challenge': challenge}), 200
                else:
                    logger.error("No challenge found in verification request")
                    return jsonify({'error': 'No challenge found'}), 400
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse verification payload: {e}")
                return jsonify({'error': 'Invalid JSON'}), 400
        
        # Verify webhook signature for regular events
        if not verify_signature(payload, signature):
            logger.error("Webhook signature verification failed")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Process webhook event
        try:
            event_data = json.loads(payload)
            return process_webhook_event(event_data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse webhook payload: {e}")
            return jsonify({'error': 'Invalid JSON'}), 400
            
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook/notion/verify', methods=['GET', 'POST'])
def notion_webhook_verify():
    """Simple endpoint for testing webhook connectivity"""
    
    if request.method == 'GET':
        return jsonify({
            'status': 'ready',
            'message': 'Notion webhook endpoint is ready for verification',
            'timestamp': datetime.now().isoformat()
        }), 200
    
    # Handle POST verification
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Check for verification challenge
            if data and 'challenge' in data:
                challenge = data['challenge']
                logger.info(f"Verification challenge received: {challenge}")
                return jsonify({'challenge': challenge}), 200
            
            return jsonify({
                'status': 'received',
                'message': 'Webhook test received successfully',
                'data': data
            }), 200
            
        except Exception as e:
            logger.error(f"Verification error: {e}")
            return jsonify({'error': str(e)}), 400

def verify_signature(payload, signature):
    """Verify webhook signature"""
    
    if not signature or not WEBHOOK_SECRET:
        logger.warning("No signature or secret provided - skipping verification")
        return True  # Allow for testing without signature
    
    try:
        # Calculate expected signature
        expected_signature = hmac.new(
            WEBHOOK_SECRET.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures
        return hmac.compare_digest(signature, expected_signature)
        
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False

def process_webhook_event(event_data):
    """Process incoming webhook event"""
    
    event_type = event_data.get('type')
    logger.info(f"Processing webhook event: {event_type}")
    
    try:
        if event_type == 'page.updated':
            return handle_page_updated(event_data)
        elif event_type == 'database.updated':
            return handle_database_updated(event_data)
        else:
            logger.info(f"Unhandled event type: {event_type}")
            return jsonify({'status': 'ignored', 'event_type': event_type}), 200
            
    except Exception as e:
        logger.error(f"Event processing error: {e}")
        return jsonify({'error': 'Event processing failed'}), 500

def handle_page_updated(event_data):
    """Handle page update events"""
    
    page_id = event_data.get('page_id')
    logger.info(f"Page updated: {page_id}")
    
    # Add your page update logic here
    # For example: sync with Teams, trigger alerts, etc.
    
    return jsonify({'status': 'processed', 'event': 'page.updated'}), 200

def handle_database_updated(event_data):
    """Handle database update events"""
    
    database_id = event_data.get('database_id')
    logger.info(f"Database updated: {database_id}")
    
    # Add your database update logic here
    # For example: refresh dashboard, send notifications, etc.
    
    return jsonify({'status': 'processed', 'event': 'database.updated'}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'notion-webhook-server',
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Use PORT for cloud platforms (Heroku, Railway, etc.) or WEBHOOK_PORT for local
    port = int(os.getenv('PORT', os.getenv('WEBHOOK_PORT', 8080)))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    flask_env = os.getenv('FLASK_ENV', 'development')
    
    print(f"🚀 Starting Notion Webhook Server on port {port}")
    print(f"🌐 Environment: {flask_env}")
    print(f"📡 Webhook endpoint: /webhook/notion")
    print(f"✅ Verification endpoint: /webhook/notion/verify")
    print(f"🏥 Health check: /health")
    
    if flask_env == 'production':
        # Production settings
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development settings
        print(f"🔗 Local access: http://localhost:{port}")
        app.run(host='0.0.0.0', port=port, debug=debug)