"""
Core provisioning service
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import traceback

from ..models.aci_models import FabricConfig
from ..models.database import get_database
from ..clients.apic_client import APICClient
from ..clients.ndo_client import NDOClient

class ProvisioningService:
    """Core service for ACI/NDO provisioning"""
    
    def __init__(self):
        self.db = get_database()
    
    async def execute_provisioning(self, job_id: int, config: FabricConfig):
        """Execute provisioning workflow"""
        try:
            self._update_job_status(job_id, "running", 0)
            self._log_task(job_id, "provisioning_start", "info", "Starting provisioning workflow")
            
            apic_client = APICClient(
                host=config.apic_credentials.host,
                username=config.apic_credentials.username,
                password=config.apic_credentials.password,
                port=config.apic_credentials.port,
                verify_ssl=config.apic_credentials.verify_ssl
            )
            
            self._log_task(job_id, "apic_auth", "info", "Authenticating with APIC")
            auth_result = await apic_client.authenticate()
            if not auth_result["success"]:
                raise Exception(f"APIC authentication failed: {auth_result['error']}")
            
            self._update_job_status(job_id, "running", 10)
            
            for i, tenant in enumerate(config.tenants):
                self._log_task(job_id, f"create_tenant_{tenant.name}", "info", f"Creating tenant: {tenant.name}")
                result = await apic_client.create_tenant(tenant.dict())
                if not result["success"]:
                    self._log_task(job_id, f"create_tenant_{tenant.name}", "error", f"Failed: {result['error']}")
                else:
                    self._log_task(job_id, f"create_tenant_{tenant.name}", "success", "Tenant created successfully")
                
                progress = 10 + (20 * (i + 1) / len(config.tenants))
                self._update_job_status(job_id, "running", int(progress))
            
            for i, vrf in enumerate(config.vrfs):
                self._log_task(job_id, f"create_vrf_{vrf.name}", "info", f"Creating VRF: {vrf.name}")
                result = await apic_client.create_vrf(vrf.dict())
                if not result["success"]:
                    self._log_task(job_id, f"create_vrf_{vrf.name}", "error", f"Failed: {result['error']}")
                else:
                    self._log_task(job_id, f"create_vrf_{vrf.name}", "success", "VRF created successfully")
                
                progress = 30 + (30 * (i + 1) / len(config.vrfs))
                self._update_job_status(job_id, "running", int(progress))
            
            for i, bd in enumerate(config.bridge_domains):
                self._log_task(job_id, f"create_bd_{bd.name}", "info", f"Creating Bridge Domain: {bd.name}")
                result = await apic_client.create_bridge_domain(bd.dict())
                if not result["success"]:
                    self._log_task(job_id, f"create_bd_{bd.name}", "error", f"Failed: {result['error']}")
                else:
                    self._log_task(job_id, f"create_bd_{bd.name}", "success", "Bridge Domain created successfully")
                
                progress = 60 + (30 * (i + 1) / len(config.bridge_domains))
                self._update_job_status(job_id, "running", int(progress))
            
            for i, app_profile in enumerate(config.app_profiles):
                self._log_task(job_id, f"create_ap_{app_profile.name}", "info", f"Creating Application Profile: {app_profile.name}")
                result = await apic_client.create_application_profile(app_profile.dict())
                if not result["success"]:
                    self._log_task(job_id, f"create_ap_{app_profile.name}", "error", f"Failed: {result['error']}")
                else:
                    self._log_task(job_id, f"create_ap_{app_profile.name}", "success", "Application Profile created successfully")
            
            for i, epg in enumerate(config.epgs):
                self._log_task(job_id, f"create_epg_{epg.name}", "info", f"Creating EPG: {epg.name}")
                result = await apic_client.create_epg(epg.dict())
                if not result["success"]:
                    self._log_task(job_id, f"create_epg_{epg.name}", "error", f"Failed: {result['error']}")
                else:
                    self._log_task(job_id, f"create_epg_{epg.name}", "success", "EPG created successfully")
            
            self._update_job_status(job_id, "completed", 100)
            self._log_task(job_id, "provisioning_complete", "success", "Provisioning workflow completed successfully")
            
        except Exception as e:
            error_msg = f"Provisioning failed: {str(e)}"
            self._log_task(job_id, "provisioning_error", "error", error_msg, {"traceback": traceback.format_exc()})
            self._update_job_status(job_id, "failed", None)
    
    async def validate_configuration(self, config: FabricConfig) -> Dict[str, Any]:
        """Validate configuration before provisioning"""
        errors = []
        warnings = []
        
        if not config.tenants:
            errors.append("At least one tenant must be specified")
        
        tenant_names = {t.name for t in config.tenants}
        for vrf in config.vrfs:
            if vrf.tenant not in tenant_names:
                errors.append(f"VRF '{vrf.name}' references non-existent tenant '{vrf.tenant}'")
        
        vrf_keys = {f"{vrf.tenant}.{vrf.name}" for vrf in config.vrfs}
        for bd in config.bridge_domains:
            if bd.tenant not in tenant_names:
                errors.append(f"Bridge Domain '{bd.name}' references non-existent tenant '{bd.tenant}'")
            
            vrf_key = f"{bd.tenant}.{bd.vrf}"
            if vrf_key not in vrf_keys:
                errors.append(f"Bridge Domain '{bd.name}' references non-existent VRF '{bd.vrf}' in tenant '{bd.tenant}'")
        
        try:
            apic_client = APICClient(
                host=config.apic_credentials.host,
                username=config.apic_credentials.username,
                password=config.apic_credentials.password,
                port=config.apic_credentials.port,
                verify_ssl=config.apic_credentials.verify_ssl
            )
            
            connectivity_result = await apic_client.test_connectivity()
            if not connectivity_result["success"]:
                errors.append(f"APIC connectivity test failed: {connectivity_result['error']}")
            
        except Exception as e:
            errors.append(f"APIC connectivity test error: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def _update_job_status(self, job_id: int, status: str, progress: int = None):
        """Update job status in database"""
        conn = self.db.get_connection()
        try:
            if progress is not None:
                conn.execute("""
                    UPDATE provisioning_jobs 
                    SET status = ?, progress = ?, 
                        started_at = CASE WHEN started_at IS NULL AND status = 'running' THEN CURRENT_TIMESTAMP ELSE started_at END,
                        completed_at = CASE WHEN status IN ('completed', 'failed') THEN CURRENT_TIMESTAMP ELSE completed_at END
                    WHERE id = ?
                """, (status, progress, job_id))
            else:
                conn.execute("""
                    UPDATE provisioning_jobs 
                    SET status = ?,
                        started_at = CASE WHEN started_at IS NULL AND status = 'running' THEN CURRENT_TIMESTAMP ELSE started_at END,
                        completed_at = CASE WHEN status IN ('completed', 'failed') THEN CURRENT_TIMESTAMP ELSE completed_at END
                    WHERE id = ?
                """, (status, job_id))
            conn.commit()
        finally:
            conn.close()
    
    def _log_task(self, job_id: int, task_name: str, status: str, message: str, details: Dict[str, Any] = None):
        """Log task execution"""
        conn = self.db.get_connection()
        try:
            conn.execute("""
                INSERT INTO task_logs (job_id, task_name, status, message, details)
                VALUES (?, ?, ?, ?, ?)
            """, (
                job_id,
                task_name,
                status,
                message,
                json.dumps(details) if details else None
            ))
            conn.commit()
        finally:
            conn.close()
