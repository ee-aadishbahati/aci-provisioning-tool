# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Get the directory containing this spec file
spec_root = os.path.dirname(os.path.abspath(SPEC))

# Define paths
backend_path = os.path.join(spec_root, 'backend')
frontend_dist_path = os.path.join(spec_root, 'frontend', 'dist')
templates_path = os.path.join(spec_root, 'templates')

# Data files to include
datas = []

# Include frontend build files
if os.path.exists(frontend_dist_path):
    datas.append((frontend_dist_path, 'frontend'))

# Include templates
if os.path.exists(templates_path):
    datas.append((templates_path, 'templates'))

# Include SSL certificates
cert_files = [
    'certifi/cacert.pem',
]

# Hidden imports for PyInstaller
hiddenimports = [
    'uvicorn.lifespan.on',
    'uvicorn.lifespan.off',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets.websockets_impl',
    'uvicorn.protocols.http.httptools_impl',
    'uvicorn.protocols.http.h11_impl',
    'uvicorn.loops.auto',
    'uvicorn.loops.asyncio',
    'uvicorn.logging',
    'logging.config',
    'logging.handlers',
    'fastapi.routing',
    'fastapi.encoders',
    'pydantic.json',
    'email.mime.multipart',
    'email.mime.text',
    'email.mime.base',
    'sqlite3',
    'json',
    'threading',
    'requests.adapters',
    'urllib3.util.retry',
    'urllib3.util.connection',
    'urllib3.connection',
    'urllib3.connectionpool',
    'urllib3.poolmanager',
    'urllib3.response',
    'certifi',
]

a = Analysis(
    ['main.py'],
    pathex=[spec_root, backend_path],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
        'torch',
        'tensorflow',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Filter out unnecessary files
def filter_binaries(binaries):
    """Filter out unnecessary binary files to reduce size"""
    excluded_patterns = [
        'api-ms-win-',
        'ucrtbase.dll',
        'msvcp140.dll',
        'vcruntime140.dll',
        'concrt140.dll',
    ]
    
    filtered = []
    for binary in binaries:
        name = binary[0].lower()
        if not any(pattern in name for pattern in excluded_patterns):
            filtered.append(binary)
    
    return filtered

a.binaries = filter_binaries(a.binaries)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='aci-provisioning-tool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Enable console for proper stdin/stdout handling
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if available
    version_file=None,  # Add version file here if needed
)
