import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.globals import set_debug, set_verbose

# Load environment variables
load_dotenv()

class PortfolioChatbot:
    """
    A personalized AI assistant for Abhishek Ambi's portfolio
    that can answer questions about projects and provide career advice.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemma2-9b-it", debug: bool = False):
        """
        Initialize the portfolio chatbot.
        
        Args:
            api_key: Groq API key (if not provided, will try to get from environment)
            model: LLM model to use
            debug: Enable debug mode for LangChain
        """
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found. Please set GROQ_API_KEY environment variable or pass it directly.")
        
        self.model = model
        self.llm = ChatGroq(model=model, api_key=self.api_key)
        
        # Set debug mode if requested
        if debug:
            set_verbose(True)
            set_debug(True)
        
        # Initialize the chain
        self._setup_chain()
    
    def _setup_chain(self):
        """Setup the LangChain with prompt template."""
        self.prompt_template = PromptTemplate(
            input_variables=['user_input'],
            template=self._get_prompt_template()
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
        )
    
    def _get_prompt_template(self) -> str:
        """Get the prompt template with system and knowledge base."""
        return '''
system_prompt:
I am Abhishek Gangappa Ambi's AI assistant, designed to provide accurate, clear, and contextual answers about his portfolio and career. My primary objectives are to:
- Provide detailed information about Abhishek's projects and technical skills
- Offer career advice based on his expertise and experience
- Answer questions about his full-stack development capabilities
- Assist with portfolio-related inquiries

Abhishek is a full-stack developer with expertise in creating efficient and innovative solutions,
specializing in App development and Web development. With a commitment to excellence,
he brings both technical expertise and creative problem-solving to his work.

knowledge_prompt:
PROJECT PORTFOLIO:

1. Indian Meeting House
   - Technology: React, Node.js, MongoDB
   - Description: Developed an online meeting application with user authentication, 
     event management, and resource sharing for seamless collaboration.
   - Features: Real-time communication, user management, event scheduling

2. Online Notes Book
   - Technology: Android Studio, Java
   - Description: Designed and built an Android application for managing personal notes
   - Features: Secure user authentication, intuitive note management, and sharing capabilities

3. Path Finder
   - Technology: React
   - Description: Created a web application to visualize pathfinding algorithms
   - Features: Dijkstra's, DFS, BFS, A* algorithms visualization for finding shortest paths

4. Quick Eats
   - Technology: React Native, Express.js, MongoDB
   - Description: Developed a food ordering app with comprehensive features
   - Features: User authentication, order management, and payment integration

5. Online Medicine Store
   - Technology: React, Node.js, MongoDB
   - Description: Designed a web application for online medicine purchasing
   - Features: Simple cart system, product management, secure transactions

6. Todo List
   - Technology: Java
   - Description: Created a Java application for managing tasks
   - Features: Straightforward interface to boost productivity

7. Shri Vagdevi Construction (Real Time Project)
   - Technology: MERN Stack (MongoDB, Express.js, React, Node.js)
   - Website: shrivagdeviconstructions.com
   - Description: A comprehensive construction company website showcasing services and portfolio
   - Features: Modern responsive design, project galleries, client testimonials, contact forms,
     content management system, smooth front-end and back-end interaction

TECHNICAL SKILLS:
- Frontend: React, React Native, HTML, CSS, JavaScript
- Backend: Node.js, Express.js, Java
- Database: MongoDB
- Mobile Development: Android Studio, Java
- Full-Stack: MERN Stack expertise
- Version Control: Git
- Development Tools: VS Code, Android Studio

User Query: "{user_input}"

Answer:
'''
    
    def ask(self, question: str) -> str:
        """
        Ask a question to the portfolio chatbot.
        
        Args:
            question: The user's question
            
        Returns:
            The AI assistant's response
        """
        try:
            result = self.chain.run({"user_input": question})
            return result.strip()
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_project_info(self, project_name: str) -> str:
        """
        Get specific information about a project.
        
        Args:
            project_name: Name of the project
            
        Returns:
            Detailed information about the project
        """
        question = f"Tell me detailed information about the project: {project_name}"
        return self.ask(question)
    
    def list_projects(self) -> str:
        """
        Get a list of all projects.
        
        Returns:
            List of all projects
        """
        return self.ask("List all my projects with their technologies")
    
    def get_tech_recommendation(self) -> str:
        """
        Get technology recommendations based on portfolio.
        
        Returns:
            Technology recommendations
        """
        return self.ask("Based on my portfolio, which technologies should I focus on for career growth?")
    
    def get_skills_summary(self) -> str:
        """
        Get a summary of technical skills.
        
        Returns:
            Summary of technical skills
        """
        return self.ask("Summarize my technical skills based on my projects")


def main():
    """Main function to demonstrate the chatbot usage."""
    try:
        # Initialize the chatbot
        chatbot = PortfolioChatbot(debug=False)
        
        print("🤖 Abhishek Ambi's Portfolio Chatbot")
        print("=" * 50)
        print("Ask me anything about Abhishek's projects, skills, or career advice!")
        print("Type 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for using the portfolio chatbot.")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Abhishek Ambi's Assistant:")
            response = chatbot.ask(user_input)
            print(response)
            print("\n" + "-" * 50 + "\n")
    
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("Please set your GROQ_API_KEY environment variable or pass it directly.")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")


if __name__ == "__main__":
    main() 