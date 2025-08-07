# 🤖 Abhishek Ambi's Portfolio Chatbot

A sophisticated AI-powered portfolio chatbot that provides intelligent responses about Abhishek's projects, skills, education, and career advice. Built with Flask, LangChain, and Groq API, featuring auto-restart functionality and periodic request monitoring.

## 🚀 Features

### **AI-Powered Responses**
- **Groq API Integration**: Uses advanced language models for intelligent conversations
- **LangChain Framework**: Structured AI responses with comprehensive knowledge base
- **Fallback System**: Graceful degradation when AI is unavailable

### **Auto-Restart & Monitoring**
- **Automatic Restart**: Server restarts every 3 minutes to maintain freshness
- **Periodic Requests**: Sends automatic POST requests to keep the server active
- **Health Monitoring**: Real-time status tracking and health checks
- **Manual Control**: Toggle features and trigger restarts via API

### **Comprehensive Knowledge Base**
- **Personal Background**: Complete educational journey from SSLC to BE
- **Project Portfolio**: 9 diverse applications with detailed descriptions
- **Technical Skills**: Full-stack, mobile, ML/AI, and development tools
- **Personal Interests**: Hobbies including coding, reading, testing, and more
- **Career Guidance**: Professional advice and recommendations

## 📋 Prerequisites

- Python 3.8+
- Groq API key (get one from [console.groq.com](https://console.groq.com/))
- Required Python packages (see requirements.txt)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AI-Assistent-ChatBoot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
```bash
# Copy the example environment file
cp env_example.txt .env

# Edit .env file with your API key
nano .env
```

Add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🚀 Quick Start

### Start the Server
```bash
python simple_chatbot_api.py
```

The server will start with:
- Auto-restart enabled (every 3 minutes)
- Periodic requests enabled (every 3 minutes)
- Health monitoring active
- API available at `http://localhost:5000`

### Test the API
```bash
# Test basic functionality
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are your technical skills?"}'

# Check health status
curl http://localhost:5000/health

# Get auto-restart status
curl http://localhost:5000/auto-restart/status
```

## 📚 API Documentation

### Core Endpoints

#### `GET /`
Returns API information and usage instructions.

#### `POST /ask`
Send questions to the chatbot.

**Request:**
```json
{
    "question": "What are Abhishek's technical skills?"
}
```

**Response:**
```json
{
    "question": "What are Abhishek's technical skills?",
    "answer": "**Abhishek's Technical Skills**\n\n**Programming Languages**:\n• Python (Data Analysis, Machine Learning, Computer Vision)\n• Java (Core & Advanced, Android Development)\n...",
    "status": "success",
    "response_source": "AI-powered",
    "chatbot_available": true
}
```

#### `GET /health`
Health check endpoint with uptime and status information.

#### `GET /auto-restart/status`
Get auto-restart and periodic request status.

#### `POST /auto-restart/toggle`
Toggle auto-restart and periodic request features.

#### `POST /auto-restart/trigger`
Manually trigger a server restart.

## 🛠️ Monitoring & Management

### Monitor Server Status
```bash
# Real-time monitoring
python monitor_server.py monitor

# Test periodic requests
python monitor_server.py test

# Toggle features
python monitor_server.py toggle

# Trigger manual restart
python monitor_server.py restart
```

### Test Restart Functionality
```bash
# Test restart features
python test_restart.py test

# Monitor auto-restart for 10 minutes
python test_restart.py monitor 10
```

## 📊 Knowledge Base Categories

### 1. **Personal Background**
- Complete educational journey (SSLC to BE)
- Personal traits and characteristics
- Professional goals and aspirations

### 2. **Education History**
- **SSLC**: Jaycee English Medium School, Mahalingpur (64%, 2020)
- **Diploma**: K.L.E.SOCIETY'S POLYTECHNIC MAHALINGAPUR (9.83 CGPA, 2020-2023)
- **BE**: RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT BENGALURU (8.26 CGPA, 2023-2026)

### 3. **Project Portfolio (9 Projects)**
- **Meeting House**: MERN Stack online meeting application
- **Shri Vagdevi Construction**: Real-time construction company website
- **Quick Eats**: Hybrid cloud kitchen app
- **Plant Disease Detection**: ML-based agricultural solution
- **Object Detection**: YOLOv5 computer vision project
- **Path Finder**: Algorithm visualization tool
- **Todo List**: Java task management app
- **C-Tutor**: AR-based educational platform
- **Online Medicine Store**: Healthcare e-commerce platform

### 4. **Technical Skills**
- **Programming Languages**: Python, Java, JavaScript, C++, PHP
- **Frontend**: React.js, React Native, Angular, HTML5, CSS3
- **Backend**: Node.js, Express.js, API Development
- **Database**: MongoDB, MySQL
- **Mobile**: Android Studio, React Native, Flutter
- **ML/AI**: YOLOv5, Computer Vision, Data Analysis
- **Tools**: Git, VS Code, Postman, Canva, Photoshop

### 5. **Personal Interests & Hobbies**
- **Coding & Programming**: Building applications and solving problems
- **Reading**: Technical books and documentation
- **Testing & QA**: Software testing and debugging
- **Learning**: Exploring new technologies
- **Problem Solving**: Tackling complex challenges
- **Open Source**: Contributing to developer communities
- **Technical Writing**: Creating documentation and tutorials
- **Algorithm Practice**: Regular DSA practice
- **Project Building**: Creating personal projects
- **Networking**: Connecting with tech professionals

### 6. **Career Guidance**
- Ideal career paths and opportunities
- Technology recommendations
- Professional development advice
- Industry insights

## 🔧 Configuration

### Environment Variables
```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://yourdomain.com
LOG_LEVEL=INFO
```

### Auto-Restart Settings
- **Restart Interval**: 3 minutes (180 seconds)
- **Periodic Requests**: Every 3 minutes
- **Health Checks**: Every 30 seconds
- **Monitoring**: Real-time status updates

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```bash
   # Check if API key is set
   echo $GROQ_API_KEY
   
   # Or check .env file
   cat .env
   ```

2. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   
   # Kill the process
   kill -9 <PID>
   ```

3. **Auto-Restart Not Working**
   ```bash
   # Check auto-restart status
   curl http://localhost:5000/auto-restart/status
   
   # Toggle auto-restart
   curl -X POST http://localhost:5000/auto-restart/toggle \
     -H "Content-Type: application/json" \
     -d '{"auto_restart": true}'
   ```

### Debug Mode
```bash
# Run with debug logging
LOG_LEVEL=DEBUG python simple_chatbot_api.py
```

## 📈 Performance & Scaling

### Current Performance
- **Response Time**: < 2 seconds for most queries
- **Uptime**: 99.9% with auto-restart
- **Concurrent Users**: Supports multiple simultaneous requests
- **Memory Usage**: Optimized for low resource consumption

### Scaling Options
- **Horizontal Scaling**: Multiple server instances
- **Load Balancing**: Nginx reverse proxy
- **Caching**: Redis for frequently asked questions
- **Database**: MongoDB for conversation history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Abhishek Ambi**
- **Portfolio**: https://www.abhishekambi.info/
- **Email**: abhishekambi2003@gmail.com
- **LinkedIn**: linkedin.com/in/abhishekambi2003
- **GitHub**: github.com/CSEStudentAbhi

## 🙏 Acknowledgments

- **Groq**: For providing the AI API
- **LangChain**: For the AI framework
- **Flask**: For the web framework
- **Open Source Community**: For various libraries and tools

## 📞 Support

For support, email abhishekambi2003@gmail.com or create an issue in the repository.

---

**Made with ❤️ by Abhishek Ambi**
