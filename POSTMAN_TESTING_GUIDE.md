# 🚀 Testing Portfolio Chatbot API with Postman

This guide will help you test your Portfolio Chatbot API using Postman.

## 📋 Prerequisites

1. **Postman installed** - Download from [postman.com](https://www.postman.com/downloads/)
2. **Python dependencies installed** - Run `pip install -r requirements.txt`
3. **API key configured** - Make sure your `.env` file has the correct API key

## 🚀 Quick Start

### 1. Start the API Server
```bash
python api_chatbot.py
```

You should see:
```
🚀 Starting Portfolio Chatbot API...
📱 API will be available at: http://localhost:5000
🔧 Postman collection available in the project
🛑 Press Ctrl+C to stop the server
```

### 2. Import Postman Collection
1. Open Postman
2. Click **Import** button
3. Select the file: `Portfolio_Chatbot_API.postman_collection.json`
4. The collection will be imported with all endpoints ready to test

## 📡 Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API documentation and available endpoints |
| `GET` | `/health` | Health check - verify API is running |
| `POST` | `/chat` | Send a message to the chatbot |
| `GET` | `/projects` | Get list of all projects |
| `GET` | `/projects/{project_name}` | Get specific project information |
| `GET` | `/skills` | Get technical skills summary |
| `GET` | `/recommendations` | Get career recommendations |

## 🧪 Testing Each Endpoint

### 1. Health Check
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/health`

**Expected Response:**
```json
{
    "status": "healthy",
    "chatbot_available": true,
    "api_version": "1.0.0",
    "timestamp": "current_timestamp"
}
```

### 2. API Documentation
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/`

**Expected Response:**
```json
{
    "message": "Abhishek Ambi's Portfolio Chatbot API",
    "version": "1.0.0",
    "status": "running",
    "chatbot_available": true,
    "endpoints": {...},
    "example_requests": {...}
}
```

### 3. Chat with Chatbot
**Request:**
- Method: `POST`
- URL: `http://localhost:5000/chat`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "message": "What are my strongest technical skills?"
}
```

**Expected Response:**
```json
{
    "message": "What are my strongest technical skills?",
    "response": "Based on your portfolio, your strongest technical skills include...",
    "status": "success",
    "timestamp": "current_timestamp"
}
```

### 4. Get All Projects
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/projects`

**Expected Response:**
```json
{
    "projects": "Here is the list of project names:\n\n1. Indian Meeting House\n2. Online Notes Book...",
    "status": "success",
    "count": 7
}
```

### 5. Get Specific Project Info
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/projects/Shri%20Vagdevi%20Construction`

**Expected Response:**
```json
{
    "project_name": "Shri Vagdevi Construction",
    "information": "Shri Vagdevi Construction is a comprehensive construction company website...",
    "status": "success"
}
```

### 6. Get Skills Summary
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/skills`

**Expected Response:**
```json
{
    "skills": "Based on your projects, your technical skills include...",
    "status": "success"
}
```

### 7. Get Career Recommendations
**Request:**
- Method: `GET`
- URL: `http://localhost:5000/recommendations`

**Expected Response:**
```json
{
    "recommendations": "Based on your portfolio, I recommend focusing on...",
    "status": "success"
}
```

## 🔧 Custom Test Requests

### Test Different Chat Questions
Try these messages in the `/chat` endpoint:

```json
{"message": "Tell me about the Quick Eats project"}
```
```json
{"message": "Which technologies should I focus on for career growth?"}
```
```json
{"message": "What makes me a good full-stack developer?"}
```
```json
{"message": "Summarize my experience with React"}
```
```json
{"message": "List all my projects with their technologies"}
```

### Test Different Projects
Try these project names in `/projects/{project_name}`:

- `Indian Meeting House`
- `Online Notes Book`
- `Path Finder`
- `Quick Eats`
- `Online Medicine Store`
- `Todo List`
- `Shri Vagdevi Construction`

## 🚨 Error Handling Tests

### Test Invalid Requests

1. **Empty Message:**
```json
{"message": ""}
```
Expected: 400 Bad Request

2. **No Message Field:**
```json
{}
```
Expected: 400 Bad Request

3. **Invalid Project Name:**
```
GET /projects/NonExistentProject
```
Expected: 500 Internal Server Error

4. **Wrong HTTP Method:**
```
POST /projects
```
Expected: 405 Method Not Allowed

## 📊 Response Status Codes

| Status Code | Meaning |
|-------------|---------|
| `200` | Success |
| `400` | Bad Request (invalid input) |
| `404` | Not Found (invalid endpoint) |
| `405` | Method Not Allowed |
| `500` | Internal Server Error |
| `503` | Service Unavailable (chatbot not available) |

## 🔍 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Make sure the API server is running (`python api_chatbot.py`)
   - Check if port 5000 is available

2. **Chatbot Not Available**
   - Check your `.env` file has the correct API key
   - Verify the API key is valid

3. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Make sure all dependencies are installed

4. **CORS Issues**
   - The API includes CORS headers for cross-origin requests
   - If testing from a browser, this should work automatically

### Debug Mode
To see detailed logs, modify `api_chatbot.py`:
```python
chatbot = PortfolioChatbot(debug=True)
```

## 📱 Testing with Other Tools

### cURL Examples
```bash
# Health check
curl http://localhost:5000/health

# Chat
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my skills?"}'

# Get projects
curl http://localhost:5000/projects
```

### JavaScript/Fetch
```javascript
// Chat with chatbot
fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'What are my strongest technical skills?'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## ✅ Success Criteria

Your API is working correctly if:

1. ✅ Health check returns `"status": "healthy"`
2. ✅ Chat endpoint responds with AI-generated answers
3. ✅ All GET endpoints return project/skills information
4. ✅ Error handling works for invalid requests
5. ✅ CORS is enabled for cross-origin requests

## 🎯 Next Steps

After testing with Postman, you can:

1. **Integrate with frontend applications**
2. **Deploy to cloud platforms** (Heroku, AWS, etc.)
3. **Add authentication** for production use
4. **Implement rate limiting** for API protection
5. **Add more endpoints** for additional functionality

---

**Happy Testing! 🚀** 