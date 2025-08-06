#!/usr/bin/env python3
"""
Simple Chatbot API for Abhishek Ambi's Portfolio
A simple Flask API that takes a question and returns an answer.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from portfolio_chatbot import PortfolioChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize chatbot
try:
    chatbot = PortfolioChatbot(debug=False)
    chatbot_available = True
    print("✅ Chatbot initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {e}")
    chatbot_available = False

@app.route('/')
def home():
    """Home endpoint with simple API documentation."""
    return jsonify({
        "message": "Abhishek Ambi's Simple Portfolio Chatbot API",
        "version": "1.0.0",
        "status": "running",
        "chatbot_available": chatbot_available,
        "usage": {
            "method": "POST",
            "url": "/ask",
            "body": {
                "question": "Your question here"
            },
            "example": {
                "question": "What are my strongest technical skills?"
            }
        }
    })

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Ask a question and get an answer.
    
    POST /ask
    Body: {"question": "Your question here"}
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available. Please check your configuration.',
            'status': 'error'
        }), 503
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400
        
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'error': 'Question cannot be empty',
                'status': 'error'
            }), 400
        
        # Get response from chatbot
        answer = chatbot.ask(question)
        
        return jsonify({
            'question': question,
            'answer': answer,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    GET /health
    """
    return jsonify({
        'status': 'healthy',
        'chatbot_available': chatbot_available,
        'api_version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': [
            'GET /',
            'POST /ask',
            'GET /health'
        ]
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        'error': 'Method not allowed',
        'status': 'error'
    }), 405

if __name__ == '__main__':
    print("🚀 Starting Simple Portfolio Chatbot API...")
    print("📱 API will be available at: http://localhost:5000")
    print("❓ Send POST requests to /ask with your questions")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 