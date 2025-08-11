"""
ACI Provisioning Tool - Main Entry Point
Standalone Windows executable for ACI fabric and NDO provisioning.
"""

import sys
import os
import threading
import webbrowser
import time
from pathlib import Path

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(application_path, 'backend'))

import uvicorn
from backend.main import app

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def open_browser():
    """Open the default browser to the application URL after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://localhost:8080')

def main():
    """Main application entry point"""
    print("Starting ACI Provisioning Tool...")
    print("Server will start on http://localhost:8080")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",  # Localhost only for security
            port=8080,
            log_level="info",
            access_log=False
        )
    except KeyboardInterrupt:
        print("\nShutting down ACI Provisioning Tool...")
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
