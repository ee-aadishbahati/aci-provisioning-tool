"""
FastAPI Backend for ACI Provisioning Tool
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
from pathlib import Path

from .routes import provisioning, status
from .models.database import init_database

app = FastAPI(
    title="ACI Provisioning Tool",
    description="Automated ACI Fabric and NDO Provisioning",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(provisioning.router, prefix="/api/provisioning", tags=["provisioning"])
app.include_router(status.router, prefix="/api/status", tags=["status"])

def get_static_path():
    """Get path to static files (frontend build)"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'frontend')
    else:
        return os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')

static_path = get_static_path()
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    assets_path = os.path.join(static_path, 'assets')
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

@app.get("/")
async def read_root():
    """Serve the React frontend"""
    static_path = get_static_path()
    index_path = os.path.join(static_path, 'index.html')
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return {"message": "ACI Provisioning Tool API", "status": "running"}

@app.get("/vite.svg")
async def serve_vite_svg():
    """Serve the Vite SVG favicon"""
    static_path = get_static_path()
    vite_svg_path = os.path.join(static_path, 'vite.svg')
    if os.path.exists(vite_svg_path):
        return FileResponse(vite_svg_path, media_type="image/svg+xml")
    else:
        raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ACI Provisioning Tool"}

@app.on_event("startup")
async def startup_event():
    """Initialize database and other startup tasks"""
    init_database()
    print("ACI Provisioning Tool backend started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup tasks on shutdown"""
    print("ACI Provisioning Tool backend shutting down")
