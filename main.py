"""
ACI Provisioning Tool - Main Entry Point
Standalone Windows executable for ACI fabric and NDO provisioning.
"""

import sys
import os
import threading
import webbrowser
import time
import logging
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
    
    if getattr(sys, 'frozen', False):
        logging.disable(logging.CRITICAL)
        # Redirect stdin/stdout/stderr to avoid isatty issues
        sys.stdin = open(os.devnull, 'r')
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    try:
        # Use minimal uvicorn configuration for PyInstaller compatibility
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=8080,
            log_level="critical",  # Minimal logging
            access_log=False,
            use_colors=False,
            log_config=None,
            loop="asyncio"  # Explicit loop for PyInstaller
        )
        server = uvicorn.Server(config)
        server.run()
    except KeyboardInterrupt:
        if not getattr(sys, 'frozen', False):
            print("\nShutting down ACI Provisioning Tool...")
    except Exception as e:
        if not getattr(sys, 'frozen', False):
            print(f"Error starting server: {e}")
            input("Press Enter to exit...")
        else:
            # In PyInstaller mode, just exit silently to avoid stdin issues
            time.sleep(2)

if __name__ == "__main__":
    main()
