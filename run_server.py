#!/usr/bin/env python3
"""
HackBite Backend Server
Self-contained backend API server for hackathon team formation

Usage:
    python3 run_server.py [--port PORT] [--host HOST]

Default: http://localhost:5000
"""

import sys
import os
import argparse
from pathlib import Path

# Add the current directory and backend directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
backend_dir = current_dir / "backend"
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(backend_dir))

# Import our backend modules
try:
    from api_server import app, initialize_app
except ImportError as e:
    print(f"❌ Failed to import backend modules: {e}")
    print("💡 Make sure you're running from the correct directory and have installed requirements:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='HackBite Backend API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run server on (default: 5000)')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    
    args = parser.parse_args()
    
    print("🚀 Starting HackBite Backend Server...")
    print(f"📂 Working directory: {current_dir}")
    print(f"🌐 Server will be available at: http://localhost:{args.port}")
    print("=" * 60)
    
    # Initialize the Flask application
    if not initialize_app():
        print("❌ Failed to initialize application. Exiting...")
        sys.exit(1)
    
    # Start the server
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()