#!/usr/bin/env python3
"""
Test script for auto-restart functionality
"""

import requests
import time
import json
from datetime import datetime

def test_restart_functionality(base_url="http://localhost:5000"):
    """Test the restart functionality."""
    
    print("🧪 Testing Auto-Restart Functionality")
    print("=" * 50)
    
    # Test 1: Check initial status
    print("\n📋 Test 1: Initial Status")
    try:
        response = requests.get(f"{base_url}/auto-restart/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Server Status: {data['auto_restart_enabled']}")
            print(f"   ✅ Uptime: {data['server_uptime_seconds']} seconds")
            print(f"   ✅ Next Restart: {data['next_restart_in_seconds']} seconds")
        else:
            print(f"   ❌ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 2: Trigger manual restart
    print("\n🔄 Test 2: Manual Restart")
    try:
        response = requests.post(
            f"{base_url}/auto-restart/trigger",
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Restart Status: {data['status']}")
            print(f"   ✅ Message: {data['message']}")
            print(f"   ✅ Chatbot Available: {data['chatbot_available']}")
        else:
            print(f"   ❌ Restart failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 3: Check status after restart
    print("\n📋 Test 3: Status After Restart")
    time.sleep(2)  # Wait for restart to complete
    try:
        response = requests.get(f"{base_url}/auto-restart/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Server Status: {data['auto_restart_enabled']}")
            print(f"   ✅ Uptime: {data['server_uptime_seconds']} seconds")
            print(f"   ✅ Next Restart: {data['next_restart_in_seconds']} seconds")
        else:
            print(f"   ❌ Failed to get status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    # Test 4: Test API functionality after restart
    print("\n📝 Test 4: API Functionality After Restart")
    try:
        response = requests.post(
            f"{base_url}/ask",
            json={'question': 'What are your technical skills?'},
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Status: {data['status']}")
            print(f"   ✅ Response Source: {data['response_source']}")
            print(f"   ✅ Answer Length: {len(data['answer'])} characters")
        else:
            print(f"   ❌ API failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print("\n✅ Restart functionality testing completed!")

def monitor_auto_restart(base_url="http://localhost:5000", duration_minutes=5):
    """Monitor the auto-restart functionality for a specified duration."""
    
    print(f"🔍 Monitoring Auto-Restart for {duration_minutes} minutes")
    print("=" * 50)
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    while time.time() < end_time:
        try:
            response = requests.get(f"{base_url}/auto-restart/status", timeout=10)
            if response.status_code == 200:
                data = response.json()
                current_time = datetime.now().strftime('%H:%M:%S')
                uptime = data['server_uptime_seconds']
                next_restart = data['next_restart_in_seconds']
                
                print(f"[{current_time}] Uptime: {uptime}s | Next Restart: {next_restart}s")
                
                # Check if restart just happened
                if uptime < 60:  # Less than 1 minute uptime
                    print(f"   🔄 Restart detected at {current_time}!")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Status check failed")
                
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Connection error: {str(e)}")
        
        time.sleep(30)  # Check every 30 seconds
    
    print("\n✅ Monitoring completed!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_restart.py test      # Test restart functionality")
        print("  python test_restart.py monitor   # Monitor auto-restart")
        print("  python test_restart.py monitor 10 # Monitor for 10 minutes")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:5000"
    
    if command == "test":
        test_restart_functionality(base_url)
    elif command == "monitor":
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        monitor_auto_restart(base_url, duration)
    else:
        print(f"Unknown command: {command}")
        print("Available commands: test, monitor")
