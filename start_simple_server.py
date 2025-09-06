#!/usr/bin/env python3
"""
Simple server start script without AI dependencies
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from backend.api_server import app, initialize_app
    
    print("🚀 Starting HackBite Server (Simple Mode)...")
    
    if initialize_app():
        print("✅ Server initialized successfully")
        print("📍 Server running at: http://localhost:5000")
        print("📍 Find People: http://localhost:5000/../frontend/findpeople/index.html")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("❌ Failed to initialize server")
        exit(1)
        
except ImportError as e:
    print(f"❌ Failed to import modules: {e}")
    print("💡 Install missing packages with:")
    print("   pip install flask flask-cors requests beautifulsoup4 PyPDF2 python-dotenv")
    exit(1)
except Exception as e:
    print(f"❌ Server startup failed: {e}")
    exit(1)