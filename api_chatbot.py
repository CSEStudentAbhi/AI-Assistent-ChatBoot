#!/usr/bin/env python3
"""
REST API for Abhishek Ambi's Portfolio Chatbot
A Flask REST API with API key authentication that can be tested with Postman.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from portfolio_chatbot import PortfolioChatbot
from api_key_manager import APIKeyManager
import os
from dotenv import load_dotenv
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize chatbot and API key manager
try:
    chatbot = PortfolioChatbot(debug=False)
    chatbot_available = True
    print("✅ Chatbot initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {e}")
    chatbot_available = False

# Initialize API key manager
api_key_manager = APIKeyManager()

def require_api_key(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'API key required',
                'status': 'error',
                'message': 'Please provide an API key in the X-API-Key header'
            }), 401
        
        # Validate API key
        key_info = api_key_manager.validate_api_key(api_key)
        if not key_info:
            return jsonify({
                'error': 'Invalid API key',
                'status': 'error',
                'message': 'The provided API key is invalid or expired'
            }), 401
        
        # Add key info to request context
        request.api_key_info = key_info
        return f(*args, **kwargs)
    
    return decorated_function

def require_permission(permission):
    """Decorator to require specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get('X-API-Key')
            
            if not api_key_manager.has_permission(api_key, permission):
                return jsonify({
                    'error': 'Insufficient permissions',
                    'status': 'error',
                    'message': f'API key does not have {permission} permission'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def home():
    """Home endpoint with API documentation."""
    return jsonify({
        "message": "Abhishek Ambi's Portfolio Chatbot API",
        "version": "2.0.0",
        "status": "running",
        "chatbot_available": chatbot_available,
        "authentication": "API Key required (X-API-Key header)",
        "endpoints": {
            "POST /chat": "Send a message to the chatbot (requires 'chat' permission)",
            "GET /projects": "Get list of all projects (requires 'projects' permission)",
            "GET /projects/<project_name>": "Get specific project information (requires 'projects' permission)",
            "GET /skills": "Get technical skills summary (requires 'skills' permission)",
            "GET /recommendations": "Get career recommendations (requires 'recommendations' permission)",
            "GET /health": "Health check endpoint (no authentication required)",
            "POST /auth/generate-key": "Generate new API key (admin only)",
            "GET /auth/keys": "List API keys (admin only)",
            "POST /auth/revoke-key": "Revoke API key (admin only)"
        },
        "example_requests": {
            "chat": {
                "method": "POST",
                "url": "/chat",
                "headers": {
                    "X-API-Key": "your_api_key_here",
                    "Content-Type": "application/json"
                },
                "body": {
                    "message": "What are my strongest technical skills?"
                }
            },
            "projects": {
                "method": "GET",
                "url": "/projects",
                "headers": {
                    "X-API-Key": "your_api_key_here"
                }
            }
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    
    GET /health
    """
    return jsonify({
        'status': 'healthy',
        'chatbot_available': chatbot_available,
        'api_version': '2.0.0',
        'authentication_enabled': True,
        'api_key_stats': api_key_manager.get_api_key_stats()
    })

@app.route('/chat', methods=['POST'])
@require_api_key
@require_permission('chat')
def chat():
    """
    Send a message to the chatbot.
    
    POST /chat
    Headers: X-API-Key: your_api_key_here
    Body: {"message": "Your question here"}
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available. Please check your API key configuration.',
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
        
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'error': 'Message cannot be empty',
                'status': 'error'
            }), 400
        
        # Get response from chatbot
        response = chatbot.ask(message)
        
        return jsonify({
            'message': message,
            'response': response,
            'status': 'success',
            'api_key_used': request.api_key_info.name,
            'usage_count': request.api_key_info.usage_count
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/projects', methods=['GET'])
@require_api_key
@require_permission('projects')
def get_projects():
    """
    Get list of all projects.
    
    GET /projects
    Headers: X-API-Key: your_api_key_here
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available',
            'status': 'error'
        }), 503
    
    try:
        projects = chatbot.list_projects()
        return jsonify({
            'projects': projects,
            'status': 'success',
            'count': len(projects.split('\n')) if projects else 0,
            'api_key_used': request.api_key_info.name
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/projects/<project_name>', methods=['GET'])
@require_api_key
@require_permission('projects')
def get_project_info(project_name):
    """
    Get specific project information.
    
    GET /projects/<project_name>
    Headers: X-API-Key: your_api_key_here
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available',
            'status': 'error'
        }), 503
    
    try:
        project_info = chatbot.get_project_info(project_name)
        return jsonify({
            'project_name': project_name,
            'information': project_info,
            'status': 'success',
            'api_key_used': request.api_key_info.name
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/skills', methods=['GET'])
@require_api_key
@require_permission('skills')
def get_skills():
    """
    Get technical skills summary.
    
    GET /skills
    Headers: X-API-Key: your_api_key_here
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available',
            'status': 'error'
        }), 503
    
    try:
        skills = chatbot.get_skills_summary()
        return jsonify({
            'skills': skills,
            'status': 'success',
            'api_key_used': request.api_key_info.name
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/recommendations', methods=['GET'])
@require_api_key
@require_permission('recommendations')
def get_recommendations():
    """
    Get career recommendations.
    
    GET /recommendations
    Headers: X-API-Key: your_api_key_here
    """
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available',
            'status': 'error'
        }), 503
    
    try:
        recommendations = chatbot.get_tech_recommendation()
        return jsonify({
            'recommendations': recommendations,
            'status': 'success',
            'api_key_used': request.api_key_info.name
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# API Key Management Endpoints (Admin only)
@app.route('/auth/generate-key', methods=['POST'])
def generate_api_key():
    """
    Generate a new API key.
    
    POST /auth/generate-key
    Body: {
        "name": "Key name",
        "description": "Key description",
        "expires_in_days": 365,
        "permissions": ["chat", "projects", "skills", "recommendations"]
    }
    """
    try:
        data = request.get_json() or {}
        
        name = data.get('name', 'New API Key')
        description = data.get('description', '')
        expires_in_days = data.get('expires_in_days', 365)
        permissions = data.get('permissions', ['chat', 'projects', 'skills', 'recommendations'])
        
        api_key = api_key_manager.generate_api_key(
            name=name,
            description=description,
            expires_in_days=expires_in_days,
            permissions=permissions
        )
        
        return jsonify({
            'api_key': api_key,
            'name': name,
            'description': description,
            'expires_in_days': expires_in_days,
            'permissions': permissions,
            'status': 'success',
            'message': 'API key generated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/auth/keys', methods=['GET'])
def list_api_keys():
    """
    List all API keys.
    
    GET /auth/keys
    """
    try:
        keys = api_key_manager.list_api_keys()
        stats = api_key_manager.get_api_key_stats()
        
        return jsonify({
            'keys': keys,
            'stats': stats,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/auth/revoke-key', methods=['POST'])
def revoke_api_key():
    """
    Revoke an API key.
    
    POST /auth/revoke-key
    Body: {"api_key": "key_to_revoke"}
    """
    try:
        data = request.get_json()
        
        if not data or 'api_key' not in data:
            return jsonify({
                'error': 'API key required',
                'status': 'error'
            }), 400
        
        api_key = data['api_key']
        success = api_key_manager.revoke_api_key(api_key)
        
        if success:
            return jsonify({
                'message': 'API key revoked successfully',
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'API key not found',
                'status': 'error'
            }), 404
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'status': 'error',
        'available_endpoints': [
            'GET /',
            'POST /chat',
            'GET /projects',
            'GET /projects/<project_name>',
            'GET /skills',
            'GET /recommendations',
            'GET /health',
            'POST /auth/generate-key',
            'GET /auth/keys',
            'POST /auth/revoke-key'
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
    print("🚀 Starting Portfolio Chatbot API with Authentication...")
    print("📱 API will be available at: http://localhost:5000")
    print("🔑 API Key authentication is required for most endpoints")
    print("🔧 Postman collection available in the project")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Create initial API key if none exist
    if not api_key_manager.keys:
        print("\n🔑 No API keys found. Creating initial API key...")
        from api_key_manager import create_initial_api_key
        create_initial_api_key()
        print("\n✅ Initial API key created! Use it in your requests.")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 