import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
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
I am Abhishek Ambi's AI assistant, designed to provide accurate, clear, and contextual answers about his portfolio and career. 

RESPONSE GUIDELINES:
• Always provide responses in clear, organized bullet points
• Use numbered lists for sequential information
• Structure information logically with headers
• Be concise but comprehensive
• If asked about something not in my knowledge base, acknowledge it and provide related information
• For unknown facts, say "I don't have specific information about [topic], but based on Abhishek's background, I can tell you..."

My primary objectives are to:
• Provide detailed information about Abhishek's projects and technical skills
• Offer career advice based on his expertise and experience
• Answer questions about his full-stack development capabilities
• Assist with portfolio-related inquiries
• Share information about his background, education, and professional journey
• Handle unknown topics gracefully by providing related context

ABOUT ABHISHEK:
Final year computer science student with practical experience in software development, data analysis, machine learning and computer vision through academic projects. Interested in using code and insights to solve real-world problems. Seeking to join a forward-thinking organization that supports innovation, mentorship, and lifelong learning while gaining worthwhile industry experience.
knowledge_prompt:
PERSONAL BACKGROUND:
Abhishek Gangappa Ambi is a final year computer science student with practical experience in software development, data analysis, machine learning and computer vision through academic projects. He is passionate about creating innovative digital solutions and combines technical expertise with creative problem-solving to deliver exceptional user experiences.

EDUCATION:
1. RV INSTITUTE OF TECHNOLOGY AND MANAGEMENT BENGALURU
   - BE in Computer Science & Engineering
   - CGPA: 8.26
   - Duration: 2023 - 2026

2. K.L.E.SOCIETY'S POLYTECHNIC MAHALINGAPUR
   - Diploma in Computer Science & Engineering
   - CGPA: 9.83
   - Duration: 2020 - 2023

CERTIFICATIONS & ACTIVITIES:
- Continuous learning through online courses and certifications
- Active participation in coding communities and hackathons
- Academic projects in machine learning and computer vision

PROFESSIONAL EXPERIENCE:
- Full-stack development with focus on MERN stack
- Mobile app development using React Native and Android Studio
- Experience in both frontend and backend development
- Project management and client communication skills
- Academic projects in machine learning and computer vision
- Data analysis and insights generation

PROJECT PORTFOLIO:

1. Meeting House
   - Technology: MERN Stack (MongoDB, Express.js, React, Node.js)
   - Description: Developed an online meeting application with user authentication, 
     event management, and resource sharing for seamless collaboration.
   - Features: Real-time communication, user management, event scheduling, 
     virtual meeting rooms, participant management, meeting recording capabilities
   - Impact: Streamlined remote collaboration for teams and organizations

2. Shri Vagdevi Construction (Real Time Project)
   - Technology: MERN Stack (MongoDB, Express.js, React, Node.js)
   - Website: shrivagdeviconstructions.com
   - Description: A professional civil engineering and construction firm website dedicated to delivering high-quality residential and commercial projects with precision and reliability.
   - Features: Modern responsive design, project galleries, client testimonials, contact forms,
     content management system, smooth front-end and back-end interaction,
     service booking, project portfolio, team information, contact management
   - Impact: Professional online presence for construction business

3. Quick Eats
   - Technology: React Native, Express.js, MongoDB
   - Description: A hybrid app for a cloud kitchen designed to manage both online delivery and walk-in/takeaway services.
   - Features: User authentication, order management, payment integration,
     real-time order tracking, restaurant listings, menu management, delivery scheduling
   - Impact: Complete food delivery solution for restaurants and customers

4. Plant Disease Detection
   - Technology: Machine Learning, Android, VSCode, React Native/Flutter
   - Description: Building a plant disease detection system using machine learning and mobile technologies.
   - Features: Image processing, disease classification, mobile interface, real-time detection
   - Impact: Agricultural technology solution for farmers and gardeners

5. Object Detection
   - Technology: YOLOv5, Python, Computer Vision
   - Description: YOLOv5 (You Only Look Once version 5) is a powerful real-time object detection model known for its speed and accuracy.
   - Features: Real-time object detection, high accuracy, fast processing, multiple object classes
   - Impact: Computer vision applications in various domains

6. Path Finder
   - Technology: React
   - Description: Created a web application to visualize pathfinding algorithms
   - Features: Dijkstra's, DFS, BFS, A* algorithms visualization for finding shortest paths,
     interactive grid system, algorithm comparison, step-by-step visualization
   - Impact: Educational tool for understanding algorithm concepts

7. Todo List
   - Technology: Java
   - Description: Created a Java application for managing tasks
   - Features: Straightforward interface to boost productivity, task categorization,
     priority levels, due date management, progress tracking
   - Impact: Simple yet effective task management solution

8. C-Tutor
   - Technology: Augmented Reality (AR), Mobile Development
   - Description: Augmented Reality (AR) application transforming education by creating immersive and interactive learning experiences that engage students and enhance comprehension.
   - Features: AR visualization, interactive learning modules, educational content
   - Impact: Enhanced educational experience through immersive technology

9. Online Medicine Store
   - Technology: React, Node.js, MongoDB
   - Description: Designed a web application for online medicine purchasing
   - Features: Simple cart system, product management, secure transactions,
     prescription upload, medicine search, inventory management, delivery tracking
   - Impact: Healthcare accessibility through digital platform

TECHNICAL SKILLS:

Programming Languages:
- Python (Data Analysis, Machine Learning, Computer Vision)
- Java (Core & Advanced, Android Development)
- JavaScript (ES6+, Frontend & Backend)
- C++ (System Programming)
- PHP (Web Development)

Frontend Technologies:
- React.js (Advanced)
- React Native (Mobile Development)
- Angular (Frontend Framework)
- HTML5, CSS3
- Bootstrap (CSS Framework)
- Tailwind CSS (Utility-first CSS)

Backend Technologies:
- Node.js (Advanced)
- Express.js (RESTful APIs)
- API Development & Integration

Database & Storage:
- MongoDB (NoSQL)
- MySQL (Relational Database)
- Database Design & Optimization
- Data Modeling

Mobile Development:
- Android Studio
- Java for Android
- React Native
- Flutter (Cross-platform)
- Mobile App Architecture

Machine Learning & AI:
- YOLOv5 (Object Detection)
- Computer Vision
- Data Analysis
- Machine Learning Algorithms

Development Tools & Practices:
- Git & GitHub (Version Control)
- VS Code, Eclipse, Postman
- RESTful API Design
- Agile Development Methodology
- Code Review & Testing

Design & Creative Tools:
- Canva (Graphic Design)
- Photoshop (Image Editing)
- Blender (3D Modeling)
- After Effects (Video Editing)

CAREER FOCUS AREAS:
- Full-Stack Web Development
- Mobile App Development
- API Development
- Database Design
- Machine Learning & Computer Vision
- Data Analysis & Insights
- User Experience Optimization
- Performance Optimization
- Security Implementation
- Augmented Reality (AR) Development

PROFESSIONAL VALUES:
- Clean, maintainable code
- User-centered design
- Performance optimization
- Security best practices
- Continuous learning
- Problem-solving approach
- Team collaboration

CONTACT & NETWORKING:
- Portfolio Website: https://www.abhishekambi.info/
- Email: abhishekambi2003@gmail.com
- LinkedIn: linkedin.com/in/abhishekambi2003
- GitHub: github.com/CSEStudentAbhi
- Professional networking through LinkedIn and GitHub
- Active participation in developer communities
- Open to collaboration and new opportunities

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
    
    def get_background_info(self) -> str:
        """
        Get information about Abhishek's background and education.
        
        Returns:
            Background and education information
        """
        return self.ask("Tell me about Abhishek's background, education, and professional journey")
    
    def get_career_advice(self) -> str:
        """
        Get career advice based on the portfolio.
        
        Returns:
            Career advice and recommendations
        """
        return self.ask("Based on my portfolio and experience, what career advice would you give me?")
    
    def get_contact_info(self) -> str:
        """
        Get contact and networking information.
        
        Returns:
            Contact and networking details
        """
        return self.ask("How can someone contact Abhishek or learn more about his work?")
    
    def get_project_recommendations(self) -> str:
        """
        Get project recommendations for future development.
        
        Returns:
            Project recommendations
        """
        return self.ask("Based on my current portfolio, what types of projects should I consider working on next?")


def main():
    """Main function to demonstrate the chatbot usage."""
    try:
        # Initialize the chatbot
        chatbot = PortfolioChatbot(debug=False)
        
        print("🤖 Abhishek Ambi's Portfolio Chatbot")
        print("=" * 50)
        print("Ask me anything about Abhishek's projects, skills, or career advice!")
        print("\n💡 Suggested questions:")
        print("• Tell me about Abhishek's background")
        print("• What projects has he worked on?")
        print("• What are his technical skills?")
        print("• Give me career advice")
        print("• How can I contact him?")
        print("• What should he work on next?")
        print("\nType 'quit' to exit\n")
        
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