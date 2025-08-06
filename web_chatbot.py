#!/usr/bin/env python3
"""
Web interface for Abhishek Ambi's Portfolio Chatbot
A simple Flask web application for the portfolio chatbot.
"""

from flask import Flask, render_template, request, jsonify
from portfolio_chatbot import PortfolioChatbot
import os

app = Flask(__name__)

# Initialize chatbot
try:
    chatbot = PortfolioChatbot(debug=False)
    chatbot_available = True
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {e}")
    chatbot_available = False

@app.route('/')
def index():
    """Main page with chat interface."""
    return render_template('index.html', chatbot_available=chatbot_available)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    if not chatbot_available:
        return jsonify({
            'error': 'Chatbot not available. Please check your API key configuration.'
        }), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get response from chatbot
        response = chatbot.ask(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/api/projects')
def get_projects():
    """Get list of all projects."""
    if not chatbot_available:
        return jsonify({'error': 'Chatbot not available'}), 500
    
    try:
        projects = chatbot.list_projects()
        return jsonify({
            'projects': projects,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills')
def get_skills():
    """Get skills summary."""
    if not chatbot_available:
        return jsonify({'error': 'Chatbot not available'}), 500
    
    try:
        skills = chatbot.get_skills_summary()
        return jsonify({
            'skills': skills,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'chatbot_available': chatbot_available
    })

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create the HTML template
    html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Abhishek Ambi's Portfolio Chatbot</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .chat-container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            width: 90%;
            max-width: 600px;
            height: 80vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .chat-header h1 {
            font-size: 1.5rem;
            margin-bottom: 5px;
        }
        
        .chat-header p {
            opacity: 0.9;
            font-size: 0.9rem;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 15px;
            display: flex;
            align-items: flex-start;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: #667eea;
            color: white;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
        }
        
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        
        .input-group {
            display: flex;
            gap: 10px;
        }
        
        .chat-input input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .chat-input input:focus {
            border-color: #667eea;
        }
        
        .chat-input button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            transition: transform 0.2s;
        }
        
        .chat-input button:hover {
            transform: translateY(-2px);
        }
        
        .chat-input button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .error-message {
            background: #ff6b6b;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 18px;
            color: #666;
            font-style: italic;
        }
        
        .quick-actions {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        .quick-action {
            padding: 8px 16px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.3s;
        }
        
        .quick-action:hover {
            background: #5a6fd8;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h1>🤖 Abhishek Ambi's Portfolio Chatbot</h1>
            <p>Ask me anything about my projects, skills, or career advice!</p>
        </div>
        
        <div class="chat-messages" id="chatMessages">
            {% if chatbot_available %}
            <div class="message bot">
                <div class="message-content">
                    👋 Hello! I'm Abhishek Ambi's AI assistant. I can help you learn about my portfolio, projects, and provide career advice. What would you like to know?
                </div>
            </div>
            
            <div class="quick-actions">
                <button class="quick-action" onclick="askQuestion('List all my projects')">📋 My Projects</button>
                <button class="quick-action" onclick="askQuestion('What are my technical skills?')">💼 My Skills</button>
                <button class="quick-action" onclick="askQuestion('Tell me about Shri Vagdevi Construction')">🏗️ Latest Project</button>
                <button class="quick-action" onclick="askQuestion('What technologies should I focus on?')">🚀 Career Advice</button>
            </div>
            {% else %}
            <div class="error-message">
                ❌ Chatbot not available. Please check your API key configuration.
            </div>
            {% endif %}
        </div>
        
        <div class="typing-indicator" id="typingIndicator">
            🤖 Abhishek's assistant is typing...
        </div>
        
        <div class="chat-input">
            <div class="input-group">
                <input type="text" id="messageInput" placeholder="Ask me anything..." 
                       onkeypress="handleKeyPress(event)" {% if not chatbot_available %}disabled{% endif %}>
                <button onclick="sendMessage()" id="sendButton" {% if not chatbot_available %}disabled{% endif %}>
                    Send
                </button>
            </div>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send to server
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                hideTypingIndicator();
                
                if (data.error) {
                    addMessage('❌ Error: ' + data.error, 'bot');
                } else {
                    addMessage(data.response, 'bot');
                }
            })
            .catch(error => {
                hideTypingIndicator();
                addMessage('❌ Network error. Please try again.', 'bot');
            });
        }
        
        function askQuestion(question) {
            document.getElementById('messageInput').value = question;
            sendMessage();
        }
        
        function addMessage(content, sender) {
            const messagesContainer = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            messagesContainer.appendChild(messageDiv);
            
            // Scroll to bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'block';
            document.getElementById('sendButton').disabled = true;
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').style.display = 'none';
            document.getElementById('sendButton').disabled = false;
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
    </script>
</body>
</html>'''
    
    # Write the template file
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 