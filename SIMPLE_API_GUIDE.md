# 🚀 Simple Portfolio Chatbot API Guide

A simple API that takes a question and returns an answer about Abhishek Ambi's portfolio.

## 🚀 Quick Start

### 1. Start the API Server
```bash
python simple_chatbot_api.py
```

You should see:
```
🚀 Starting Simple Portfolio Chatbot API...
📱 API will be available at: http://localhost:5000
❓ Send POST requests to /ask with your questions
🛑 Press Ctrl+C to stop the server
```

### 2. Test with Postman
Import `Simple_Chatbot_API.postman_collection.json` into Postman and start testing!

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API documentation |
| `GET` | `/health` | Health check |
| `POST` | `/ask` | Ask a question and get an answer |

## 🧪 How to Use

### Ask a Question
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are my strongest technical skills?"}'
```

### Response Format
```json
{
  "question": "What are my strongest technical skills?",
  "answer": "Based on your portfolio, your strongest technical skills include...",
  "status": "success"
}
```

## 📝 Example Questions

Try these questions:

1. **"What are my strongest technical skills?"**
2. **"Tell me about the Shri Vagdevi Construction project"**
3. **"Which technologies should I focus on for career growth?"**
4. **"List all my projects with their technologies"**
5. **"Summarize my experience with React"**
6. **"What makes me a good full-stack developer?"**
7. **"Tell me about the Quick Eats project"**

## 🔧 Testing with Postman

1. **Import the collection**: `Simple_Chatbot_API.postman_collection.json`
2. **Test Health Check**: Make sure the API is running
3. **Try the example questions**: Use the pre-configured requests
4. **Create your own**: Add new requests with your questions

## 📱 Testing with cURL

### Health Check
```bash
curl http://localhost:5000/health
```

### Ask About Skills
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are my strongest technical skills?"}'
```

### Ask About Projects
```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about the Shri Vagdevi Construction project"}'
```

## 🔧 Programmatic Usage

### Python
```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:5000/ask",
    json={"question": "What are my strongest technical skills?"}
)

result = response.json()
print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
```

### JavaScript
```javascript
// Ask a question
fetch('http://localhost:5000/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        question: 'What are my strongest technical skills?'
    })
})
.then(response => response.json())
.then(data => {
    console.log('Question:', data.question);
    console.log('Answer:', data.answer);
});
```

## ✅ Success Criteria

Your API is working if:

1. ✅ Health check returns `"status": "healthy"`
2. ✅ `/ask` endpoint responds with answers
3. ✅ No authentication required
4. ✅ Simple JSON request/response format

## 🚨 Error Handling

### Empty Question
```json
{
  "error": "Question cannot be empty",
  "status": "error"
}
```

### Invalid JSON
```json
{
  "error": "No JSON data provided",
  "status": "error"
}
```

### Chatbot Not Available
```json
{
  "error": "Chatbot not available. Please check your configuration.",
  "status": "error"
}
```

## 🎯 What You Can Ask

The chatbot knows about:

- **7 Projects**: Indian Meeting House, Online Notes Book, Path Finder, Quick Eats, Online Medicine Store, Todo List, Shri Vagdevi Construction
- **Technical Skills**: React, Node.js, MongoDB, Java, Android Studio, MERN Stack
- **Career Advice**: Technology recommendations, skill development
- **Personal Information**: Abhishek Ambi's background and expertise

## 🔍 Troubleshooting

### Common Issues

1. **Connection Refused**
   - Make sure the API server is running (`python simple_chatbot_api.py`)
   - Check if port 5000 is available

2. **Chatbot Not Available**
   - Check your `.env` file has the correct API key
   - Verify the API key is valid

3. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Make sure all dependencies are installed

## 🎉 That's It!

This is a **super simple API** that just:
1. Takes a question
2. Returns an answer
3. No authentication needed
4. No complex setup

Perfect for quick testing and integration!

---

**Simple, clean, and effective! 🚀** 