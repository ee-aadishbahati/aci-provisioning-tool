"""
Pydantic models for ACI configuration
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class FabricType(str, Enum):
    IT = "it"
    OT = "ot"

class SiteCode(str, Enum):
    AUNTH = "AUNTH"  # Northern DC
    AUSTH = "AUSTH"  # Southern DC
    AUTER = "AUTER"  # Tertiary DC

class APICCredentials(BaseModel):
    host: str = Field(..., description="APIC IP address or hostname")
    username: str = Field(..., description="APIC username")
    password: str = Field(..., description="APIC password")
    port: int = Field(default=443, description="APIC HTTPS port")
    verify_ssl: bool = Field(default=False, description="Verify SSL certificates")

class TenantConfig(BaseModel):
    name: str = Field(..., description="Tenant name")
    description: Optional[str] = Field(None, description="Tenant description")

class VRFConfig(BaseModel):
    name: str = Field(..., description="VRF name")
    tenant: str = Field(..., description="Parent tenant")
    description: Optional[str] = Field(None, description="VRF description")
    enforcement: str = Field(default="enforced", description="Policy enforcement mode")

class BridgeDomainConfig(BaseModel):
    name: str = Field(..., description="Bridge domain name")
    tenant: str = Field(..., description="Parent tenant")
    vrf: str = Field(..., description="Associated VRF")
    subnet: Optional[str] = Field(None, description="Subnet (e.g., 10.1.1.1/24)")
    description: Optional[str] = Field(None, description="Bridge domain description")

class ApplicationProfileConfig(BaseModel):
    name: str = Field(..., description="Application profile name")
    tenant: str = Field(..., description="Parent tenant")
    description: Optional[str] = Field(None, description="Application profile description")

class EPGConfig(BaseModel):
    name: str = Field(..., description="EPG name")
    tenant: str = Field(..., description="Parent tenant")
    app_profile: str = Field(..., description="Parent application profile")
    bridge_domain: str = Field(..., description="Associated bridge domain")
    description: Optional[str] = Field(None, description="EPG description")

class FabricConfig(BaseModel):
    site_code: SiteCode = Field(..., description="Site code")
    fabric_type: FabricType = Field(..., description="Fabric type (IT/OT)")
    apic_credentials: APICCredentials = Field(..., description="APIC connection details")
    
    tenants: List[TenantConfig] = Field(default_factory=list, description="Tenants to create")
    vrfs: List[VRFConfig] = Field(default_factory=list, description="VRFs to create")
    bridge_domains: List[BridgeDomainConfig] = Field(default_factory=list, description="Bridge domains to create")
    app_profiles: List[ApplicationProfileConfig] = Field(default_factory=list, description="Application profiles to create")
    epgs: List[EPGConfig] = Field(default_factory=list, description="EPGs to create")

class ProvisioningJob(BaseModel):
    id: Optional[int] = Field(None, description="Job ID")
    name: str = Field(..., description="Job name")
    template_id: Optional[int] = Field(None, description="Template ID")
    fabric_config: FabricConfig = Field(..., description="Fabric configuration")
    status: str = Field(default="pending", description="Job status")
    progress: int = Field(default=0, description="Progress percentage")
    
class TaskLog(BaseModel):
    id: Optional[int] = Field(None, description="Log ID")
    job_id: int = Field(..., description="Job ID")
    task_name: str = Field(..., description="Task name")
    status: str = Field(..., description="Task status")
    message: Optional[str] = Field(None, description="Log message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")
