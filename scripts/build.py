#!/usr/bin/env python3
"""
Build script for ACI Provisioning Tool
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def main():
    """Main build process"""
    project_root = Path(__file__).parent.parent
    frontend_path = project_root / "frontend"
    
    print("=== ACI Provisioning Tool Build Process ===")
    
    print("\n1. Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", cwd=project_root):
        print("Failed to install Python dependencies")
        return False
    
    print("\n2. Building frontend...")
    
    if not run_command("npm install", cwd=frontend_path):
        print("Failed to install Node.js dependencies")
        return False
    
    if not run_command("npm run build", cwd=frontend_path):
        print("Failed to build frontend")
        return False
    
    templates_path = project_root / "templates"
    templates_path.mkdir(exist_ok=True)
    
    print("\n3. Building executable with PyInstaller...")
    if not run_command("pyinstaller build.spec --clean", cwd=project_root):
        print("Failed to build executable")
        return False
    
    dist_path = project_root / "dist"
    exe_path_windows = dist_path / "aci-provisioning-tool.exe"
    exe_path_linux = dist_path / "aci-provisioning-tool"
    
    exe_path = exe_path_windows if exe_path_windows.exists() else exe_path_linux
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Build successful!")
        print(f"Executable: {exe_path}")
        print(f"Size: {size_mb:.1f} MB")
        
        if exe_path.name.endswith('.exe'):
            batch_content = """@echo off
echo Starting ACI Provisioning Tool...
echo Please wait while the application loads...
echo.
aci-provisioning-tool.exe
pause
"""
            batch_path = dist_path / "run-aci-tool.bat"
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            print(f"Batch file created: {batch_path}")
        else:
            shell_content = """#!/bin/bash
echo "Starting ACI Provisioning Tool..."
echo "Please wait while the application loads..."
echo ""
./aci-provisioning-tool
read -p "Press Enter to continue..."
"""
            shell_path = dist_path / "run-aci-tool.sh"
            with open(shell_path, 'w') as f:
                f.write(shell_content)
            shell_path.chmod(0o755)
            print(f"Shell script created: {shell_path}")
        
        return True
    else:
        print("\n❌ Build failed - executable not found")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
