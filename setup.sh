#!/bin/bash

# HackBite Backend Setup Script
# Run this to set up the complete backend environment

echo "🚀 Setting up HackBite Backend Environment..."

# Create necessary directories
mkdir -p database
mkdir -p logs

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install requirements if pip is available
if command -v pip &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
elif command -v pip3 &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    pip3 install -r requirements.txt
else
    echo "⚠️  pip not found. Please install dependencies manually:"
    echo "   pip install flask flask-cors"
fi

# Set permissions
chmod +x run_server.py
chmod +w database

echo "✅ Setup complete!"
echo "🚀 To start the server, run: python3 run_server.py"
echo "🌐 The API will be available at: http://localhost:5000"
echo "📱 Open frontend/registration/login.html in your browser to test"