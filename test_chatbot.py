#!/usr/bin/env python3
"""
Test script for Abhishek Ambi's Portfolio Chatbot
This script demonstrates various functionalities of the chatbot.
"""

from portfolio_chatbot import PortfolioChatbot
import os

def test_chatbot():
    """Test the portfolio chatbot with various questions."""
    
    # Check if API key is available
    if not os.getenv('GROQ_API_KEY'):
        print("❌ GROQ_API_KEY not found in environment variables.")
        print("Please set your API key in the .env file or as an environment variable.")
        return
    
    try:
        # Initialize the chatbot
        print("🚀 Initializing Portfolio Chatbot...")
        chatbot = PortfolioChatbot(debug=False)
        print("✅ Chatbot initialized successfully!\n")
        
        # Test questions
        test_questions = [
            "What is your name and what do you do?",
            "List all my projects with their technologies",
            "Tell me about the Shri Vagdevi Construction project",
            "What are my strongest technical skills?",
            "Which technologies should I focus on for career growth?",
            "Summarize my experience with React",
            "What makes me a good full-stack developer?"
        ]
        
        print("🧪 Running Test Questions...")
        print("=" * 60)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n📝 Test {i}: {question}")
            print("-" * 40)
            
            try:
                response = chatbot.ask(question)
                print(f"🤖 Response: {response}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            print("-" * 40)
        
        # Test specific methods
        print("\n🔧 Testing Specific Methods...")
        print("=" * 60)
        
        # Test project listing
        print("\n📋 Testing project listing:")
        try:
            projects = chatbot.list_projects()
            print(projects)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test project info
        print("\n🏗️ Testing project info for 'Quick Eats':")
        try:
            project_info = chatbot.get_project_info("Quick Eats")
            print(project_info)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test skills summary
        print("\n💼 Testing skills summary:")
        try:
            skills = chatbot.get_skills_summary()
            print(skills)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")

def quick_test():
    """Quick test with a single question."""
    try:
        chatbot = PortfolioChatbot()
        response = chatbot.ask("What is your name and what do you do?")
        print("🤖 Quick Test Response:")
        print(response)
    except Exception as e:
        print(f"❌ Quick test failed: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_test()
    else:
        test_chatbot() 