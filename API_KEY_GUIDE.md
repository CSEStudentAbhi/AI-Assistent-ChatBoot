# 🔑 API Key Authentication Guide

This guide explains how to use the API key authentication system for Abhishek Ambi's Portfolio Chatbot API.

## 🚀 Quick Start

### 1. Generate Your First API Key
```bash
python api_key_manager.py
```

This will create an initial API key that you can use for testing.

### 2. Start the API Server
```bash
python api_chatbot.py
```

The server will automatically create an initial API key if none exist.

### 3. Use the API Key in Requests
Add the `X-API-Key` header to your requests:
```
X-API-Key: your_generated_api_key_here
```

## 📋 API Key Features

### 🔐 **Security Features**
- **Secure Generation**: Uses cryptographically secure random tokens
- **Hashed Storage**: API keys are hashed before storage
- **Expiration**: Keys can have expiration dates
- **Permissions**: Granular permission system
- **Usage Tracking**: Track key usage and last used time

### 🎯 **Permission System**
Each API key can have specific permissions:
- `chat` - Access to chatbot conversations
- `projects` - Access to project information
- `skills` - Access to skills summary
- `recommendations` - Access to career recommendations

## 🔧 API Key Management

### Generate New API Key
```bash
# Using the API
curl -X POST http://localhost:5000/auth/generate-key \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "description": "Key for my application",
    "expires_in_days": 365,
    "permissions": ["chat", "projects", "skills", "recommendations"]
  }'
```

### List All API Keys
```bash
curl http://localhost:5000/auth/keys
```

### Revoke API Key
```bash
curl -X POST http://localhost:5000/auth/revoke-key \
  -H "Content-Type: application/json" \
  -d '{"api_key": "key_to_revoke"}'
```

## 📡 API Endpoints with Authentication

### Public Endpoints (No API Key Required)
- `GET /` - API documentation
- `GET /health` - Health check
- `POST /auth/generate-key` - Generate new API key
- `GET /auth/keys` - List API keys
- `POST /auth/revoke-key` - Revoke API key

### Protected Endpoints (API Key Required)
- `POST /chat` - Chat with chatbot (requires `chat` permission)
- `GET /projects` - List all projects (requires `projects` permission)
- `GET /projects/{name}` - Get specific project (requires `projects` permission)
- `GET /skills` - Get skills summary (requires `skills` permission)
- `GET /recommendations` - Get career advice (requires `recommendations` permission)

## 🧪 Testing with Postman

### 1. Import the Updated Collection
Import `Portfolio_Chatbot_API.postman_collection.json` into Postman.

### 2. Set Your API Key
1. Open the collection
2. Go to **Variables** tab
3. Set `api_key` variable to your generated API key

### 3. Test Authentication
1. First, test **Health Check** (no auth required)
2. Then test **Generate API Key** to create a new key
3. Use the generated key in other requests

## 📝 Example Requests

### Chat with Bot
```bash
curl -X POST http://localhost:5000/chat \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{"message": "What are my strongest technical skills?"}'
```

### Get Projects
```bash
curl -H "X-API-Key: your_api_key_here" \
  http://localhost:5000/projects
```

### Get Specific Project
```bash
curl -H "X-API-Key: your_api_key_here" \
  "http://localhost:5000/projects/Shri%20Vagdevi%20Construction"
```

## 🔍 Response Examples

### Successful Response
```json
{
  "message": "What are my strongest technical skills?",
  "response": "Based on your portfolio...",
  "status": "success",
  "api_key_used": "My API Key",
  "usage_count": 5
}
```

### Authentication Error
```json
{
  "error": "API key required",
  "status": "error",
  "message": "Please provide an API key in the X-API-Key header"
}
```

### Permission Error
```json
{
  "error": "Insufficient permissions",
  "status": "error",
  "message": "API key does not have chat permission"
}
```

## 🛡️ Security Best Practices

### 1. **Keep API Keys Secure**
- Never commit API keys to version control
- Store keys in environment variables
- Use different keys for different applications

### 2. **Key Management**
- Regularly rotate API keys
- Set appropriate expiration dates
- Grant minimal required permissions

### 3. **Monitoring**
- Monitor key usage statistics
- Revoke unused or compromised keys
- Check for unusual usage patterns

## 📊 API Key Statistics

The system tracks:
- **Total keys**: Number of keys created
- **Active keys**: Currently valid keys
- **Expired keys**: Keys past expiration date
- **Total usage**: Combined usage count
- **Individual usage**: Per-key usage tracking

## 🔧 Programmatic Usage

### Python Example
```python
import requests

# Your API key
api_key = "your_api_key_here"

# Headers for all requests
headers = {
    "X-API-Key": api_key,
    "Content-Type": "application/json"
}

# Chat with bot
response = requests.post(
    "http://localhost:5000/chat",
    headers=headers,
    json={"message": "What are my skills?"}
)

print(response.json())
```

### JavaScript Example
```javascript
const apiKey = 'your_api_key_here';

fetch('http://localhost:5000/chat', {
    method: 'POST',
    headers: {
        'X-API-Key': apiKey,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        message: 'What are my strongest technical skills?'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🚨 Troubleshooting

### Common Issues

1. **"API key required" error**
   - Make sure you're including the `X-API-Key` header
   - Check that the header name is exactly `X-API-Key`

2. **"Invalid API key" error**
   - Verify your API key is correct
   - Check if the key has expired
   - Ensure the key hasn't been revoked

3. **"Insufficient permissions" error**
   - Check what permissions your key has
   - Generate a new key with the required permissions

4. **Key not working**
   - Regenerate a new API key
   - Check the API key format (should start with `abhishek_`)

## 📈 Advanced Features

### Custom Permissions
You can create API keys with specific permissions:
```json
{
  "name": "Read-only Key",
  "permissions": ["projects", "skills"],
  "expires_in_days": 30
}
```

### Key Expiration
Set expiration dates for temporary access:
```json
{
  "name": "Temporary Access",
  "expires_in_days": 7
}
```

### Usage Monitoring
Track how your API keys are being used:
```bash
curl http://localhost:5000/auth/keys
```

## 🎯 Next Steps

1. **Generate your first API key**
2. **Test the authentication system**
3. **Set up proper key management**
4. **Integrate with your applications**
5. **Monitor usage and security**

---

**Your portfolio chatbot now has enterprise-grade API key authentication! 🔐** 