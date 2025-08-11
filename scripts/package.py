#!/usr/bin/env python3
"""
Packaging script for ACI Provisioning Tool
Creates a distributable package with documentation
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_package():
    """Create distributable package"""
    project_root = Path(__file__).parent.parent
    dist_path = project_root / "dist"
    exe_path = dist_path / "aci-provisioning-tool.exe"
    
    if not exe_path.exists():
        print("❌ Executable not found. Run build.py first.")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"aci-provisioning-tool-{timestamp}"
    package_path = dist_path / package_name
    
    if package_path.exists():
        shutil.rmtree(package_path)
    
    package_path.mkdir()
    
    shutil.copy2(exe_path, package_path / "aci-provisioning-tool.exe")
    
    batch_path = dist_path / "run-aci-tool.bat"
    if batch_path.exists():
        shutil.copy2(batch_path, package_path / "run-aci-tool.bat")
    
    readme_content = f"""# ACI Provisioning Tool v1.0.0

Standalone Windows executable for automated ACI fabric and Nexus Dashboard Orchestrator (NDO) provisioning.

1. Extract all files to a folder on your Windows machine
2. Double-click `aci-provisioning-tool.exe` to start the application
3. The application will open in your default web browser

1. **Dashboard**: View system status and recent provisioning jobs
2. **Configure**: Set up ACI fabric configurations and credentials
3. **Jobs**: Monitor and manage provisioning jobs
4. **Templates**: Manage configuration templates

- Windows 10/11 (64-bit)
- No internet connection required (offline operation)
- Minimum 4GB RAM recommended
- 100MB free disk space

- Real ACI APIC REST API integration
- NDO multi-site orchestration support
- Template-based configuration management
- Progress tracking and logging
- Offline operation capability

- All credentials are stored locally and encrypted
- API communications use HTTPS with certificate validation
- Audit logs are maintained for compliance

For technical support, contact: aadish.bahati@essentialenergy.com.au

- Build Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Version: 1.0.0
- Architecture: Windows x64

---
Copyright © 2025 Essential Energy. All rights reserved.
"""
    
    with open(package_path / "README.txt", 'w') as f:
        f.write(readme_content)
    
    zip_path = dist_path / f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_path.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_path)
                zipf.write(file_path, arcname)
    
    exe_size_mb = exe_path.stat().st_size / (1024 * 1024)
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    print(f"✅ Package created successfully!")
    print(f"Package folder: {package_path}")
    print(f"ZIP package: {zip_path}")
    print(f"Executable size: {exe_size_mb:.1f} MB")
    print(f"ZIP size: {zip_size_mb:.1f} MB")
    
    return True

if __name__ == "__main__":
    success = create_package()
    sys.exit(0 if success else 1)
