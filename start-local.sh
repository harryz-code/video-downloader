#!/bin/bash

echo "🚀 Starting YouTube Downloader (Railway Backend)"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Start Railway backend server (serves both frontend and API)
echo "🐍 Starting Railway backend on port 8080..."
echo "📱 Frontend and API: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"

# Start the Railway app
python railway_app.py
