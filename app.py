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
import re
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class FallbackChatbot:
    """Fallback chatbot that provides responses without API key."""
    
    def __init__(self):
        self.knowledge_base = {
            'background': {
                'keywords': ['background', 'about', 'who', 'student', 'education'],
                'response': """**Abhishek Ambi - Personal Background**

• **Current Status**: Final year computer science student
• **Specializations**: Software development, data analysis, machine learning, computer vision
• **Career Goal**: Seeking forward-thinking organization supporting innovation and mentorship

**Personal Journey**:
• Born and raised in Mahalingpur, Karnataka
• Started educational journey at Jaycee English Medium School
• Completed SSLC in 2020 with 64% marks
• Pursued Diploma in Computer Science (2020-2023) with excellent performance (9.83 CGPA)
• Currently pursuing BE in Computer Science with strong academic record (8.26 CGPA)

**Education Details**:
1. **RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT BENGALURU**
   • Degree: BE in Computer Science & Engineering
   • CGPA: 8.26
   • Duration: 2023 - 2026

2. **K.L.E.SOCIETY'S POLYTECHNIC MAHALINGAPUR**
   • Degree: Diploma in Computer Science & Engineering
   • CGPA: 9.83
   • Duration: 2020 - 2023

3. **JAYCEE ENGLISH MEDIUM SCHOOL MAHALINGPUR**
   • SSLC (10th Standard)
   • Percentage: 64%
   • Passout Year: 2020
   • Location: Mahalingpur, Karnataka

**Personal Traits**:
• Dedicated and hardworking individual
• Strong problem-solving mindset
• Enjoys learning new technologies
• Team player with good communication skills
• Detail-oriented and quality-focused
• Self-motivated and goal-driven

**Key Interests**:
• Using code and insights to solve real-world problems
• Continuous learning and professional development
• Innovation and creative problem-solving"""
            },
            'projects': {
                'keywords': ['project', 'work', 'portfolio', 'developed', 'created'],
                'response': """**Abhishek's Project Portfolio**

**Total Projects**: 9 diverse applications

**Project List**:
1. **Meeting House** - MERN Stack online meeting application
2. **Shri Vagdevi Construction** - Real-time construction company website
3. **Quick Eats** - Hybrid cloud kitchen app
4. **Plant Disease Detection** - ML-based agricultural solution
5. **Object Detection** - YOLOv5 computer vision project
6. **Path Finder** - Algorithm visualization tool
7. **Todo List** - Java task management app
8. **C-Tutor** - AR-based educational platform
9. **Online Medicine Store** - Healthcare e-commerce platform

**Project Categories**:
• **Web Applications**: 4 projects
• **Mobile Applications**: 3 projects
• **Machine Learning**: 2 projects
• **Educational Tools**: 2 projects

Each project demonstrates different technical skills and problem-solving abilities."""
            },
            'skills': {
                'keywords': ['skill', 'technology', 'tech', 'programming', 'language', 'framework'],
                'response': """**Abhishek's Technical Skills**

**Programming Languages**:
• Python (Data Analysis, Machine Learning, Computer Vision)
• Java (Core & Advanced, Android Development)
• JavaScript (ES6+, Frontend & Backend)
• C++ (System Programming)
• PHP (Web Development)

**Frontend Technologies**:
• React.js (Advanced)
• React Native (Mobile Development)
• Angular (Frontend Framework)
• HTML5, CSS3
• Bootstrap (CSS Framework)
• Tailwind CSS (Utility-first CSS)

**Backend Technologies**:
• Node.js (Advanced)
• Express.js (RESTful APIs)
• API Development & Integration

**Database & Storage**:
• MongoDB (NoSQL)
• MySQL (Relational Database)
• Database Design & Optimization

**Mobile Development**:
• Android Studio
• Java for Android
• React Native
• Flutter (Cross-platform)

**Machine Learning & AI**:
• YOLOv5 (Object Detection)
• Computer Vision
• Data Analysis
• Machine Learning Algorithms

**Development Tools**:
• Git & GitHub (Version Control)
• VS Code, Eclipse, Postman
• RESTful API Design
• Agile Development Methodology

**Design & Creative Tools**:
• Canva (Graphic Design)
• Photoshop (Image Editing)
• Blender (3D Modeling)
• After Effects (Video Editing)

**Expertise Areas**:
• Full-stack development
• Mobile app development
• Machine learning and computer vision"""
            },
            'contact': {
                'keywords': ['contact', 'email', 'linkedin', 'github', 'reach', 'connect'],
                'response': """**Contact Information**

**Primary Contact Methods**:
• **Portfolio Website**: https://www.abhishekambi.info/
• **Email**: abhishekambi2003@gmail.com
• **LinkedIn**: linkedin.com/in/abhishekambi2003
• **GitHub**: github.com/CSEStudentAbhi

**Professional Status**:
• Open to collaboration opportunities
• Available for new projects and positions
• Active in developer communities
• Welcomes networking and mentorship

**Best Ways to Connect**:
1. **Professional Inquiries**: LinkedIn or Email
2. **Project Collaboration**: GitHub or Email
3. **Portfolio Review**: Website or LinkedIn
4. **General Questions**: Any of the above methods"""
            },
            'hobbies': {
                'keywords': ['hobby', 'hobbies', 'interest', 'interests', 'personal', 'activities', 'coding', 'reading', 'testing'],
                'response': """**Abhishek's Personal Interests & Hobbies**

**Primary Hobbies**:
• **Coding & Programming**: Passionate about writing code, solving problems, and building applications
• **Reading**: Enjoys reading technical books, programming documentation, and educational content
• **Testing & Quality Assurance**: Interested in software testing, debugging, and ensuring code quality

**Technical Interests**:
• **Learning New Technologies**: Constantly exploring new programming languages, frameworks, and tools
• **Problem Solving**: Enjoys tackling complex technical challenges and finding innovative solutions
• **Algorithm Practice**: Regular practice of data structures and algorithms for skill improvement
• **Project Building**: Creating personal projects to apply and showcase technical skills

**Professional Development**:
• **Open Source Contribution**: Interested in contributing to open-source projects and developer communities
• **Technical Writing**: Creating documentation, tutorials, and sharing knowledge with others
• **Networking**: Connecting with fellow developers and tech professionals

**Personal Development**:
• Continuous learning and skill enhancement
• Staying updated with latest technology trends
• Building a strong professional network
• Contributing to the developer community

**Why These Hobbies Matter**:
• Coding and testing skills directly enhance technical capabilities
• Reading keeps knowledge current and broadens perspectives
• Problem-solving practice improves analytical thinking
• Networking helps in career growth and opportunities"""
            },
            'career': {
                'keywords': ['career', 'advice', 'job', 'work', 'experience', 'future'],
                'response': """**Career Opportunities & Advice**

**Ideal Career Paths**:
• **Full-Stack Development** - Leveraging MERN stack expertise
• **Mobile App Development** - React Native and Android experience
• **Machine Learning/Computer Vision** - Academic project background
• **Data Analysis** - Python and ML skills
• **Software Engineering** - Comprehensive technical foundation

**Academic Strengths**:
• **BE CGPA**: 8.26 (Excellent academic performance)
• **Diploma CGPA**: 9.83 (Outstanding foundation)
• **SSLC**: 64% from Jaycee English Medium School, Mahalingpur (2020)
• **Project Portfolio**: 9 diverse applications
• **Technical Breadth**: Full-stack to ML/AI

**Career Advantages**:
• Strong theoretical foundation
• Practical project experience
• Diverse skill set
• Continuous learning mindset
• Problem-solving approach

**Recommended Focus Areas**:
1. **Immediate**: Full-stack and mobile development roles
2. **Short-term**: Machine learning and computer vision opportunities
3. **Long-term**: Leadership and innovation roles

**Target Organizations**:
• Forward-thinking tech companies
• Innovation-focused startups
• Organizations supporting mentorship
• Companies with learning culture"""
            },
            'default': {
                'response': """**Welcome to Abhishek Ambi's AI Assistant!**

**I can help you learn about**:
• Abhishek's background and education
• His projects and technical skills
• Personal interests and hobbies
• Career advice and opportunities
• How to contact him

**Available Information Categories**:
1. **Personal Background** - Education, experience, goals, personal journey
2. **Project Portfolio** - 9 diverse applications
3. **Technical Skills** - Programming, frameworks, tools
4. **Personal Interests & Hobbies** - Coding, reading, testing, and more
5. **Contact Information** - Professional networking
6. **Career Guidance** - Opportunities and advice

**Response Format**:
• All responses are organized in bullet points
• Information is structured with clear headers
• Unknown topics are handled gracefully with related context

Feel free to ask me anything about Abhishek's portfolio, hobbies, or career!"""
            }
        }
    
    def ask(self, question):
        """Provide intelligent response based on question content."""
        question_lower = question.lower()
        
        # Check each knowledge category
        for category, data in self.knowledge_base.items():
            if category == 'default':
                continue
                
            for keyword in data['keywords']:
                if keyword in question_lower:
                    return data['response']
        
        # Handle unknown topics gracefully
        return self._handle_unknown_topic(question)
    
    def _handle_unknown_topic(self, question):
        """Handle questions about unknown topics with related information."""
        question_lower = question.lower()
        
        # Check for specific unknown topics and provide related info
        if any(word in question_lower for word in ['salary', 'income', 'money', 'earnings']):
            return """**Salary & Compensation Information**

I don't have specific information about Abhishek's salary or earnings, but based on his background, I can tell you:

**Market Position**:
• Final year computer science student with strong academic record
• 9 diverse projects demonstrating technical skills
• Expertise in full-stack, mobile, and ML/AI development

**Typical Salary Ranges** (based on his skill set):
• **Entry-level positions**: Competitive market rates
• **Full-stack roles**: Industry standard compensation
• **ML/AI positions**: Premium salary packages

**Factors Affecting Compensation**:
• Strong academic performance (8.26 CGPA)
• Diverse technical skills
• Practical project experience
• Market demand for his skill set

For specific salary information, please contact Abhishek directly through his professional channels."""
        
        elif any(word in question_lower for word in ['hobby', 'interest', 'personal', 'life']):
            return """**Personal Interests & Hobbies**

I don't have specific information about Abhishek's personal hobbies, but based on his professional background, I can tell you:

**Professional Interests**:
• Software development and coding
• Machine learning and computer vision
• Problem-solving and innovation
• Continuous learning and skill development

**Academic Focus**:
• Computer science and engineering
• Data analysis and insights
• Technology and innovation
• Real-world problem solving

**Career Interests**:
• Joining forward-thinking organizations
• Mentorship and learning opportunities
• Innovation and creative solutions
• Professional growth and development

For personal interests and hobbies, please connect with Abhishek directly through his contact information."""
        
        elif any(word in question_lower for word in ['family', 'parents', 'siblings', 'personal']):
            return """**Personal & Family Information**

I don't have specific information about Abhishek's family or personal life, but I can tell you about his professional background:

**Professional Profile**:
• Final year computer science student
• Based in India
• Strong academic background
• Diverse technical skills

**Educational Journey**:
• Diploma from K.L.E.SOCIETY'S POLYTECHNIC MAHALINGAPUR
• Currently pursuing BE from RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT BENGALURU
• Excellent academic performance throughout

**Career Goals**:
• Seeking forward-thinking organizations
• Interested in innovation and mentorship
• Focus on professional development
• Passion for solving real-world problems

For personal information, please contact Abhishek directly through his professional channels."""
        
        else:
            return """**Information Request**

I don't have specific information about that topic, but based on Abhishek's background, I can tell you:

**Available Information Categories**:
1. **Professional Background** - Education, experience, skills
2. **Project Portfolio** - 9 diverse applications
3. **Technical Skills** - Programming, frameworks, tools
4. **Career Opportunities** - Job prospects and advice
5. **Contact Information** - Professional networking

**What I Know About Abhishek**:
• Final year computer science student
• Strong academic record (8.26 CGPA in BE, 9.83 in Diploma)
• 9 diverse projects in web, mobile, and ML/AI
• Expertise in full-stack development and machine learning
• Seeking opportunities in forward-thinking organizations

**To Get Specific Information**:
• Contact Abhishek directly through his professional channels
• Visit his portfolio website: https://www.abhishekambi.info/
• Connect on LinkedIn: linkedin.com/in/abhishekambi2003

Feel free to ask me about his professional background, projects, skills, or career opportunities!"""

# Initialize chatbot
try:
    chatbot = PortfolioChatbot(debug=False)
    chatbot_available = True
    print("✅ Chatbot initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize chatbot: {e}")
    chatbot_available = False
    print("🔄 Using fallback response system...")

# Initialize fallback chatbot
fallback_chatbot = FallbackChatbot()

# Server start time for uptime tracking
server_start_time = time.time()

@app.route('/')
def home():
    """Home endpoint with simple API documentation."""
    return jsonify({
        "message": "Abhishek Ambi's AI Assistant Chatbot API",
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
        
        # Get response from appropriate chatbot
        if chatbot_available:
            answer = chatbot.ask(question)
            response_source = "AI-powered"
        else:
            answer = fallback_chatbot.ask(question)
            response_source = "fallback"
        
        return jsonify({
            'question': question,
            'answer': answer,
            'status': 'success',
            'response_source': response_source,
            'chatbot_available': chatbot_available
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
    current_time = time.time()
    uptime = current_time - server_start_time
    
    return jsonify({
        'status': 'healthy',
        'chatbot_available': chatbot_available,
        'api_version': '1.0.0',
        'uptime_seconds': int(uptime)
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
    print("❓ Send POST requests to /ask with your questions")
    print("🛑 Press Ctrl+C to stop the server")
    
    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=7860) 