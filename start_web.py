#!/usr/bin/env python3
"""
Startup script for the Quiz Game Web Interface
"""

import sys
import subprocess
import os

def check_flask():
    """Check if Flask is installed"""
    try:
        import flask
        return True
    except ImportError:
        return False

def install_flask():
    """Install Flask using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🎯 Ultimate Quiz Game - Web Interface")
    print("=" * 50)
    
    # Check if Flask is available
    if not check_flask():
        print("❌ Flask is not installed.")
        print("\n📦 Installing Flask...")
        
        if install_flask():
            print("✅ Flask installed successfully!")
        else:
            print("❌ Failed to install Flask automatically.")
            print("\n📋 Please install Flask manually:")
            print("   pip3 install flask")
            print("   or")
            print("   python3 -m pip install flask")
            print("\nThen run: python3 app.py")
            return
    
    print("✅ Flask is available!")
    print("\n🚀 Starting the Quiz Game web server...")
    print("📍 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Quiz Game server stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Please check that all files are present and try again.")

if __name__ == "__main__":
    main()