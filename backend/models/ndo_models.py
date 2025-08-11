"""
Pydantic models for NDO configuration
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class NDOCredentials(BaseModel):
    host: str = Field(..., description="NDO IP address or hostname")
    username: str = Field(..., description="NDO username")
    password: str = Field(..., description="NDO password")
    port: int = Field(default=443, description="NDO HTTPS port")
    verify_ssl: bool = Field(default=False, description="Verify SSL certificates")

class SiteConfig(BaseModel):
    name: str = Field(..., description="Site name")
    apic_host: str = Field(..., description="APIC host for this site")
    site_id: str = Field(..., description="Site ID")

class SchemaTemplate(BaseModel):
    name: str = Field(..., description="Template name")
    tenants: List[str] = Field(..., description="Associated tenants")
    sites: List[str] = Field(..., description="Deployed sites")

class SchemaConfig(BaseModel):
    name: str = Field(..., description="Schema name")
    templates: List[SchemaTemplate] = Field(..., description="Schema templates")

class NDOConfig(BaseModel):
    ndo_credentials: NDOCredentials = Field(..., description="NDO connection details")
    sites: List[SiteConfig] = Field(..., description="Sites to manage")
    schemas: List[SchemaConfig] = Field(..., description="Schemas to create")
