#!/bin/bash

# HackBite Backend Setup Script
# Run this to set up the complete backend environment

echo "🚀 Setting up HackBite Backend Environment..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv (faster Python package manager)..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# Check if virtual environment already exists
if [ -d "env" ]; then
    echo "📁 Virtual environment already exists, activating..."
    source env/bin/activate
else
    echo "🔧 Creating new virtual environment with uv..."
    uv venv env
    source env/bin/activate
fi

# Check if requirements are already installed
echo "🔍 Checking if dependencies are installed..."
python3 -c "
import sys
try:
    import flask
    import flask_cors
    import google.generativeai
    print('✅ All dependencies already installed')
    sys.exit(0)
except ImportError:
    print('📦 Dependencies need to be installed...')
    sys.exit(1)
" 2>/dev/null

# If dependencies check failed, install them with uv (much faster!)
if [ $? -ne 0 ]; then
    echo "📦 Installing Python dependencies with uv..."
    uv pip install -r requirements.txt
fi

# Test backend imports
echo "🧪 Testing backend imports..."
python3 -c "
try:
    import flask
    import flask_cors
    import google.generativeai
    print('✅ All backend modules imported successfully')
except ImportError as e:
    print(f'❌ Failed to import backend modules: {e}')
    print('💡 Make sure you are running from the correct directory and have installed requirements:')
    print('   uv pip install -r requirements.txt')
    exit(1)
"

# Set permissions
chmod +x run_server.py
chmod +w database 2>/dev/null || echo "⚠️  Database directory not found (will be created on first run)"

echo "✅ Setup complete!"
echo "🚀 To start the server, run: python3 run_server.py"
echo "🌐 The API will be available at: http://localhost:5000"
echo "📱 Open frontend/registration/login.html in your browser to test"

# Test import to verify installation
echo "🧪 Testing backend imports..."
python3 -c "
try:
    import flask
    import flask_cors
    print('✅ Flask modules imported successfully')
except ImportError as e:
    print(f'❌ Failed to import backend modules: {e}')
    print('💡 Make sure you are running from the correct directory and have installed requirements:')
    print('   PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install -r requirements.txt')
    exit(1)
"

# Set permissions
chmod +x run_server.py

echo "✅ Setup complete!"
echo "🚀 To start the server, run: python3 run_server.py"
echo "🌐 The API will be available at: http://localhost:5000"
echo "📱 Open frontend/registration/login.html in your browser to test"