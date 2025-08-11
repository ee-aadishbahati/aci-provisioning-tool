"""
Status and monitoring API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import json
from datetime import datetime, timedelta

from ..models.database import get_database

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ACI Provisioning Tool"
    }

@router.get("/stats")
async def get_statistics():
    """Get provisioning statistics"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT 
                status,
                COUNT(*) as count
            FROM provisioning_jobs
            GROUP BY status
        """)
        
        job_stats = {}
        for row in cursor.fetchall():
            job_stats[row["status"]] = row["count"]
        
        yesterday = datetime.utcnow() - timedelta(days=1)
        cursor = conn.execute("""
            SELECT COUNT(*) as count
            FROM provisioning_jobs
            WHERE created_at > ?
        """, (yesterday.isoformat(),))
        
        recent_jobs = cursor.fetchone()["count"]
        
        cursor = conn.execute("SELECT COUNT(*) as count FROM api_logs")
        total_api_calls = cursor.fetchone()["count"]
        
        conn.close()
        
        return {
            "job_statistics": job_stats,
            "recent_jobs_24h": recent_jobs,
            "total_api_calls": total_api_calls,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get statistics: {str(e)}")

@router.get("/templates")
async def list_templates():
    """List available configuration templates"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT id, name, type, description, created_at, updated_at
            FROM templates
            ORDER BY name
        """)
        
        templates = []
        for row in cursor.fetchall():
            templates.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["type"],
                "description": row["description"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            })
        
        conn.close()
        return templates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list templates: {str(e)}")

@router.get("/templates/{template_id}")
async def get_template(template_id: int):
    """Get a specific configuration template"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT * FROM templates WHERE id = ?
        """, (template_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Template not found")
        
        template_data = {
            "id": row["id"],
            "name": row["name"],
            "type": row["type"],
            "description": row["description"],
            "config": json.loads(row["config"]),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }
        
        conn.close()
        return template_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get template: {str(e)}")

@router.get("/logs/recent")
async def get_recent_logs(limit: int = 100):
    """Get recent task logs across all jobs"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT 
                tl.*,
                pj.name as job_name
            FROM task_logs tl
            JOIN provisioning_jobs pj ON tl.job_id = pj.id
            ORDER BY tl.timestamp DESC
            LIMIT ?
        """, (limit,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "id": row["id"],
                "job_id": row["job_id"],
                "job_name": row["job_name"],
                "task_name": row["task_name"],
                "status": row["status"],
                "message": row["message"],
                "details": json.loads(row["details"]) if row["details"] else None,
                "timestamp": row["timestamp"]
            })
        
        conn.close()
        return logs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")
