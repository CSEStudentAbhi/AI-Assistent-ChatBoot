#!/usr/bin/env python3
"""
Cleanup and Push Script
This script helps clean up the repository and push safely without exposing secrets.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a git command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False
    return True

def main():
    print("🧹 Repository Cleanup and Safe Push")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("❌ Not in a git repository. Please run this script from your project root.")
        return
    
    # Step 1: Remove the problematic file from git tracking
    print("\n📋 Step 1: Remove problematic files from git tracking")
    
    # Remove the original notebook with hardcoded API key
    if os.path.exists('GenAiBootCamp.ipynb'):
        print("⚠️  Found GenAiBootCamp.ipynb with hardcoded API key")
        print("   This file will be removed from git tracking")
        run_command('git rm --cached GenAiBootCamp.ipynb', "Remove notebook from git tracking")
    
    # Step 2: Add the clean notebook
    if os.path.exists('GenAiBootCamp_Clean.ipynb'):
        print("\n📋 Step 2: Add clean notebook")
        run_command('git add GenAiBootCamp_Clean.ipynb', "Add clean notebook")
    
    # Step 3: Update .gitignore
    print("\n📋 Step 3: Update .gitignore")
    run_command('git add .gitignore', "Add updated .gitignore")
    
    # Step 4: Add other safe files
    print("\n📋 Step 4: Add other project files")
    safe_files = [
        'simple_chatbot_api.py',
        'portfolio_chatbot.py',
        'requirements.txt',
        'README.md',
        'SIMPLE_API_GUIDE.md',
        'Simple_Chatbot_API.postman_collection.json',
        'test_chatbot.py',
        'web_chatbot.py'
    ]
    
    for file in safe_files:
        if os.path.exists(file):
            run_command(f'git add {file}', f"Add {file}")
    
    # Step 5: Commit changes
    print("\n📋 Step 5: Commit changes")
    commit_message = "feat: Add simple chatbot API and clean up repository\n\n- Add simple_chatbot_api.py for easy question-answer API\n- Remove hardcoded API keys from notebook\n- Update .gitignore to prevent future secret exposure\n- Add comprehensive documentation and Postman collection"
    
    if run_command(f'git commit -m "{commit_message}"', "Commit changes"):
        print("\n✅ Repository cleaned and committed successfully!")
        
        # Step 6: Push to remote
        print("\n📋 Step 6: Push to remote repository")
        if run_command('git push origin main', "Push to remote"):
            print("\n🎉 Successfully pushed to GitHub!")
            print("\n📝 Next steps:")
            print("1. Use the simple API: python simple_chatbot_api.py")
            print("2. Test with Postman using Simple_Chatbot_API.postman_collection.json")
            print("3. Keep your API keys in .env file (not in code)")
        else:
            print("\n❌ Failed to push. You may need to:")
            print("1. Check your GitHub credentials")
            print("2. Resolve any remaining conflicts")
            print("3. Try: git push --force-with-lease origin main")
    else:
        print("\n❌ Failed to commit changes")

if __name__ == "__main__":
    main() 