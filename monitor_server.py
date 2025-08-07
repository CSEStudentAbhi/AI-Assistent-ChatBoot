#!/usr/bin/env python3
"""
Server Monitor for Abhishek Ambi's Portfolio Chatbot
Monitors auto-restart and periodic request functionality
"""

import requests
import time
import json
from datetime import datetime
import sys

def monitor_server(base_url="https://ai-assistent-chatboot.onrender.com"):
    """Monitor the server's auto-restart and periodic request functionality."""
    
    print("🔍 Portfolio Chatbot Server Monitor")
    print("=" * 50)
    
    while True:
        try:
            # Get server status
            status_response = requests.get(f"{base_url}/auto-restart/status", timeout=10)
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                print("🔍 Portfolio Chatbot Server Monitor")
                print("=" * 50)
                print(f"📅 Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print()
                
                # Auto-restart status
                print("🔄 Auto-Restart Status:")
                print(f"   Enabled: {'✅ Yes' if status_data['auto_restart_enabled'] else '❌ No'}")
                print(f"   Interval: {status_data['restart_interval_seconds']} seconds")
                print(f"   Server Uptime: {status_data['server_uptime_seconds']} seconds")
                print(f"   Next Restart In: {status_data['next_restart_in_seconds']} seconds")
                print(f"   Last Restart: {status_data['last_restart_time']}")
                print()
                
                # Periodic requests status
                print("📡 Periodic Requests Status:")
                print(f"   Enabled: {'✅ Yes' if status_data['periodic_requests_enabled'] else '❌ No'}")
                print()
                
                # Health check
                health_response = requests.get(f"{base_url}/health", timeout=10)
                if health_response.status_code == 200:
                    health_data = health_response.json()
                    print("💚 Server Health:")
                    print(f"   Status: {health_data['status']}")
                    print(f"   Chatbot Available: {'✅ Yes' if health_data['chatbot_available'] else '❌ No'}")
                    print(f"   API Version: {health_data['api_version']}")
                else:
                    print("❌ Health check failed")
                
                print()
                print("Press Ctrl+C to stop monitoring")
                
            else:
                print(f"❌ Failed to get server status: {status_response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {str(e)}")
            print("   Server might be restarting...")
        
        # Wait 5 seconds before next check
        time.sleep(5)

def test_periodic_requests(base_url="https://ai-assistent-chatboot.onrender.com"):
    """Test the periodic request functionality manually."""
    
    print("🧪 Testing Periodic Request Functionality")
    print("=" * 50)
    
    test_questions = [
        "What are your technical skills?",
        "Tell me about your projects",
        "What is your background?",
        "How can I contact you?",
        "Give me career advice"
    ]
    
    for i, question in enumerate(test_questions, 1):
        try:
            print(f"\n📝 Test {i}: {question}")
            
            response = requests.post(
                f"{base_url}/ask",
                json={'question': question},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success")
                print(f"   Status: {data['status']}")
                print(f"   Source: {data['response_source']}")
                print(f"   Answer Length: {len(data['answer'])} characters")
            else:
                print(f"   ❌ Failed - Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
        
        # Wait 2 seconds between tests
        time.sleep(2)
    
    print("\n✅ Periodic request testing completed")

def toggle_features(base_url="https://ai-assistent-chatboot.onrender.com"):
    """Toggle auto-restart and periodic request features."""
    
    print("⚙️ Feature Toggle")
    print("=" * 50)
    
    # Get current status
    try:
        status_response = requests.get(f"{base_url}/auto-restart/status", timeout=10)
        if status_response.status_code == 200:
            status_data = status_response.json()
            
            print("Current Settings:")
            print(f"   Auto-restart: {'Enabled' if status_data['auto_restart_enabled'] else 'Disabled'}")
            print(f"   Periodic requests: {'Enabled' if status_data['periodic_requests_enabled'] else 'Disabled'}")
            print()
            
            # Toggle auto-restart
            new_auto_restart = not status_data['auto_restart_enabled']
            toggle_response = requests.post(
                f"{base_url}/auto-restart/toggle",
                json={'auto_restart': new_auto_restart},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if toggle_response.status_code == 200:
                toggle_data = toggle_response.json()
                print("✅ Settings updated:")
                print(f"   Auto-restart: {'Enabled' if toggle_data['auto_restart_enabled'] else 'Disabled'}")
                print(f"   Periodic requests: {'Enabled' if toggle_data['periodic_requests_enabled'] else 'Disabled'}")
            else:
                print("❌ Failed to update settings")
                
        else:
            print("❌ Failed to get current status")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def trigger_restart(base_url="https://ai-assistent-chatboot.onrender.com"):
    """Manually trigger a server restart."""
    
    print("🔄 Triggering Manual Restart")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{base_url}/auto-restart/trigger",
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Restart triggered successfully!")
            print(f"   Status: {data['status']}")
            print(f"   Message: {data['message']}")
            print(f"   Restart Time: {data['restart_time']}")
            print(f"   Chatbot Available: {'Yes' if data['chatbot_available'] else 'No'}")
        else:
            print(f"❌ Failed to trigger restart - Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error triggering restart: {str(e)}")

def main():
    """Main function with command line interface."""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python monitor_server.py monitor    # Monitor server continuously")
        print("  python monitor_server.py test       # Test periodic requests")
        print("  python monitor_server.py toggle     # Toggle features")
        print("  python monitor_server.py restart    # Trigger manual restart")
        return
    
    command = sys.argv[1].lower()
    base_url = sys.argv[2] if len(sys.argv) > 2 else "https://ai-assistent-chatboot.onrender.com"
    
    if command == "monitor":
        monitor_server(base_url)
    elif command == "test":
        test_periodic_requests(base_url)
    elif command == "toggle":
        toggle_features(base_url)
    elif command == "restart":
        trigger_restart(base_url)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: monitor, test, toggle, restart")

if __name__ == "__main__":
    main()
