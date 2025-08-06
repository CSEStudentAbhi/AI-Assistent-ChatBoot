# Abhishek Ambi's Portfolio Chatbot 🤖

A personalized AI assistant built with LangChain and Groq that can answer questions about Abhishek Gangappa Ambi's portfolio, projects, and provide career advice.

## Features ✨

- **Portfolio Information**: Detailed information about all 7 projects
- **Technical Skills**: Comprehensive overview of technical expertise
- **Career Advice**: Personalized recommendations based on portfolio
- **Interactive Chat**: Natural conversation interface
- **Secure API Handling**: Environment variable-based API key management
- **Error Handling**: Robust error handling and user feedback

## Projects Covered 📁

1. **Indian Meeting House** - React/Node.js/MongoDB meeting app
2. **Online Notes Book** - Android Studio/Java notes app
3. **Path Finder** - React pathfinding visualization
4. **Quick Eats** - React Native food ordering app
5. **Online Medicine Store** - React/Node.js/MongoDB e-commerce
6. **Todo List** - Java task management app
7. **Shri Vagdevi Construction** - MERN stack construction website

## Installation 🚀

### 1. Clone or Download
```bash
git clone <repository-url>
cd Chat_Bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# Copy the example file
cp env_example.txt .env
```

Edit the `.env` file and add your Groq API key:
```env
GROQ_API_KEY=your_actual_groq_api_key_here
DEBUG_MODE=false
```

### 4. Get Your Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up/Login to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Usage 💻

### Interactive Mode
Run the chatbot in interactive mode:
```bash
python portfolio_chatbot.py
```

Example conversation:
```
🤖 Abhishek Ambi's Portfolio Chatbot
==================================================
Ask me anything about Abhishek's projects, skills, or career advice!
Type 'quit' to exit

You: Tell me about Shri Vagdevi Construction project

🤖 Abhishek Ambi's Assistant:
Shri Vagdevi Construction is a comprehensive construction company website built using the MERN stack (MongoDB, Express.js, React, Node.js). The project showcases the company's services and portfolio with modern responsive design, project galleries, client testimonials, and contact forms. It features a content management system for easy content updates and smooth front-end and back-end interaction. The website is live at shrivagdeviconstructions.com.

--------------------------------------------------

You: What technologies should I focus on?

🤖 Abhishek Ambi's Assistant:
Based on your portfolio, I recommend focusing on React and the MERN stack as your primary technologies. You have extensive experience with React across multiple projects, and the MERN stack is highly in demand. Additionally, consider expanding your knowledge in cloud services (AWS/Azure), TypeScript for better type safety, and modern frontend frameworks like Next.js. Your Java skills are also valuable for enterprise applications.

--------------------------------------------------
```

### Programmatic Usage
```python
from portfolio_chatbot import PortfolioChatbot

# Initialize the chatbot
chatbot = PortfolioChatbot()

# Ask specific questions
response = chatbot.ask("What are my strongest technical skills?")
print(response)

# Get project information
project_info = chatbot.get_project_info("Quick Eats")
print(project_info)

# List all projects
projects = chatbot.list_projects()
print(projects)

# Get career advice
advice = chatbot.get_tech_recommendation()
print(advice)
```

## API Methods 📚

### Core Methods
- `ask(question: str)` - Ask any question about the portfolio
- `get_project_info(project_name: str)` - Get detailed project information
- `list_projects()` - Get list of all projects with technologies
- `get_tech_recommendation()` - Get technology recommendations
- `get_skills_summary()` - Get technical skills summary

### Configuration
- `PortfolioChatbot(api_key=None, model="gemma2-9b-it", debug=False)`
  - `api_key`: Your Groq API key (optional if set in .env)
  - `model`: LLM model to use (default: gemma2-9b-it)
  - `debug`: Enable LangChain debug mode

## Security 🔒

- **API Key Protection**: API keys are stored in environment variables
- **No Hardcoding**: No sensitive information in source code
- **Error Handling**: Graceful error handling without exposing sensitive data

## Technical Stack 🛠️

- **Language**: Python 3.8+
- **AI Framework**: LangChain
- **LLM Provider**: Groq (gemma2-9b-it model)
- **Environment**: python-dotenv
- **Error Handling**: Built-in exception handling

## Troubleshooting 🔧

### Common Issues

1. **API Key Error**
   ```
   ❌ Configuration Error: API key not found
   ```
   **Solution**: Make sure your `.env` file exists and contains the correct API key

2. **Import Error**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   **Solution**: Install dependencies with `pip install -r requirements.txt`

3. **Network Error**
   ```
   ConnectionError: Unable to connect to Groq API
   ```
   **Solution**: Check your internet connection and API key validity

### Debug Mode
Enable debug mode to see detailed LangChain logs:
```python
chatbot = PortfolioChatbot(debug=True)
```

## Contributing 🤝

Feel free to contribute to this project by:
- Adding new features
- Improving the prompt template
- Enhancing error handling
- Adding more project information

## License 📄

This project is open source and available under the MIT License.

## Contact 📧

For questions or support, contact Abhishek Gangappa Ambi.

---

**Note**: Make sure to keep your API key secure and never commit it to version control! 