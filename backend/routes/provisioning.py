"""
Provisioning API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import json
from datetime import datetime

from ..models.aci_models import ProvisioningJob, FabricConfig, TaskLog
from ..models.database import get_database
from ..services.provisioning import ProvisioningService

router = APIRouter()

@router.post("/jobs", response_model=Dict[str, Any])
async def create_provisioning_job(
    job_data: ProvisioningJob,
    background_tasks: BackgroundTasks
):
    """Create a new provisioning job"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            INSERT INTO provisioning_jobs (name, template_id, fabric_config, status)
            VALUES (?, ?, ?, ?)
        """, (
            job_data.name,
            job_data.template_id,
            json.dumps(job_data.fabric_config.dict()),
            "pending"
        ))
        
        job_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        provisioning_service = ProvisioningService()
        background_tasks.add_task(
            provisioning_service.execute_provisioning,
            job_id,
            job_data.fabric_config
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Provisioning job created and started"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")

@router.get("/jobs", response_model=List[Dict[str, Any]])
async def list_provisioning_jobs():
    """List all provisioning jobs"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT id, name, status, progress, created_at, started_at, completed_at
            FROM provisioning_jobs
            ORDER BY created_at DESC
        """)
        
        jobs = []
        for row in cursor.fetchall():
            jobs.append({
                "id": row["id"],
                "name": row["name"],
                "status": row["status"],
                "progress": row["progress"],
                "created_at": row["created_at"],
                "started_at": row["started_at"],
                "completed_at": row["completed_at"]
            })
        
        conn.close()
        return jobs
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")

@router.get("/jobs/{job_id}", response_model=Dict[str, Any])
async def get_provisioning_job(job_id: int):
    """Get details of a specific provisioning job"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT * FROM provisioning_jobs WHERE id = ?
        """, (job_id,))
        
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = {
            "id": row["id"],
            "name": row["name"],
            "template_id": row["template_id"],
            "fabric_config": json.loads(row["fabric_config"]),
            "status": row["status"],
            "progress": row["progress"],
            "created_at": row["created_at"],
            "started_at": row["started_at"],
            "completed_at": row["completed_at"]
        }
        
        conn.close()
        return job_data
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job: {str(e)}")

@router.get("/jobs/{job_id}/logs", response_model=List[Dict[str, Any]])
async def get_job_logs(job_id: int):
    """Get logs for a specific provisioning job"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        cursor = conn.execute("""
            SELECT * FROM task_logs 
            WHERE job_id = ? 
            ORDER BY timestamp ASC
        """, (job_id,))
        
        logs = []
        for row in cursor.fetchall():
            logs.append({
                "id": row["id"],
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

@router.delete("/jobs/{job_id}")
async def delete_provisioning_job(job_id: int):
    """Delete a provisioning job and its logs"""
    try:
        db = get_database()
        conn = db.get_connection()
        
        conn.execute("DELETE FROM task_logs WHERE job_id = ?", (job_id,))
        conn.execute("DELETE FROM api_logs WHERE job_id = ?", (job_id,))
        
        cursor = conn.execute("DELETE FROM provisioning_jobs WHERE id = ?", (job_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Job not found")
        
        conn.commit()
        conn.close()
        
        return {"message": "Job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete job: {str(e)}")

@router.post("/validate-config")
async def validate_configuration(config: FabricConfig):
    """Validate ACI configuration before provisioning"""
    try:
        provisioning_service = ProvisioningService()
        validation_result = await provisioning_service.validate_configuration(config)
        
        return {
            "valid": validation_result["valid"],
            "errors": validation_result.get("errors", []),
            "warnings": validation_result.get("warnings", [])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")
