#!/usr/bin/env python3
"""
Startup script for the Web-Based YouTube Downloader
Automatically finds an available port and starts the server
"""

import socket
import subprocess
import sys
import time
import os

def find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def start_server(port):
    """Start the web downloader server on the specified port"""
    print(f"🚀 Starting Web-Based YouTube Downloader on port {port}...")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("🌐 No installation required - works on any device!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Modify the port in web_downloader.py temporarily
    with open('web_downloader.py', 'r') as f:
        content = f.read()
    
    # Replace the port number
    content = content.replace('port=8080', f'port={port}')
    
    with open('web_downloader.py', 'w') as f:
        f.write(content)
    
    try:
        # Start the server
        subprocess.run([sys.executable, 'web_downloader.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎯 Web-Based YouTube Downloader Startup")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("❌ Virtual environment not found. Please run:")
        print("   python3 -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r web_requirements.txt")
        return
    
    # Check if web_downloader.py exists
    if not os.path.exists('web_downloader.py'):
        print("❌ web_downloader.py not found!")
        return
    
    # Find available port
    port = find_available_port()
    if port is None:
        print("❌ No available ports found!")
        return
    
    print(f"✅ Found available port: {port}")
    
    # Activate virtual environment and start server
    try:
        # Start the server
        start_server(port)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    main()
