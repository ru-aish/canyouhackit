#!/usr/bin/env python3
"""
Team Creation Demo Script
Demonstrates the complete team creation flow including backend API and frontend integration
"""

import requests
import json
import sys
import time
from pathlib import Path

# API Configuration
API_BASE_URL = "http://localhost:5000/api"

def test_api_connection():
    """Test if the API server is running"""
    try:
        response = requests.get(f"{API_BASE_URL.replace('/api', '')}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
            return True
        else:
            print(f"❌ API server returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API server: {e}")
        print("💡 Make sure to start the server with: python3 run_server.py")
        return False

def create_test_user():
    """Create a test user for team creation"""
    user_data = {
        "name": "Alice Johnson",
        "email": "alice@hackbite.com",
        "password": "secure123",
        "profile_logo": "brain",
        "location": "New York",
        "experience": "advanced"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/register", json=user_data)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Created test user: {result['profile']['name']} (ID: {result['user_id']})")
            return result['user_id']
        else:
            print(f"❌ Failed to create user: {result.get('message')}")
            return None
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None

def create_test_team(leader_id):
    """Create a test team"""
    team_data = {
        "team_name": "AI Innovation Squad",
        "description": "Building revolutionary AI applications to solve real-world problems. Looking for passionate developers, designers, and data scientists.",
        "leader_id": leader_id,
        "max_members": 5,
        "application_deadline": "2025-09-20"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/teams", json=team_data)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Created team: {result['team']['team_name']} (ID: {result['team_id']})")
            return result['team_id']
        else:
            print(f"❌ Failed to create team: {result.get('message')}")
            return None
    except Exception as e:
        print(f"❌ Error creating team: {e}")
        return None

def list_teams():
    """List all teams"""
    try:
        response = requests.get(f"{API_BASE_URL}/teams")
        result = response.json()
        
        if result.get('success'):
            teams = result['teams']
            print(f"\n📋 Found {len(teams)} team(s):")
            for team in teams:
                print(f"  • {team['team_name']} (Leader: {team['leader_name']}, Members: {team['current_members']}/{team['max_members']})")
                print(f"    Status: {team['status']} | Created: {team['created_at']}")
                print(f"    Description: {team['description'][:80]}...")
            return teams
        else:
            print(f"❌ Failed to list teams: {result.get('message')}")
            return []
    except Exception as e:
        print(f"❌ Error listing teams: {e}")
        return []

def main():
    print("🚀 HackBite Team Creation Demo")
    print("=" * 50)
    
    # Test API connection
    if not test_api_connection():
        sys.exit(1)
    
    # Create test user
    print("\n👤 Creating test user...")
    user_id = create_test_user()
    if not user_id:
        sys.exit(1)
    
    # Create test team
    print("\n👥 Creating test team...")
    team_id = create_test_team(user_id)
    if not team_id:
        sys.exit(1)
    
    # List all teams
    print("\n📋 Listing all teams...")
    teams = list_teams()
    
    # Show frontend integration info
    print("\n🌐 Frontend Integration:")
    print("  Frontend page: frontend/hackathonpage/createateam.html")
    print("  The form now connects to the backend API")
    print("  Users can create teams through the web interface")
    
    print("\n✅ Demo completed successfully!")
    print("\n💡 Next steps:")
    print("  1. Open frontend/hackathonpage/createateam.html in a browser")
    print("  2. Fill out the team creation form")
    print("  3. The team will be created via the backend API")
    print("  4. Check the server logs to see the API calls")

if __name__ == "__main__":
    main()