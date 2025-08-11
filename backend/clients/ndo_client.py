"""
NDO (Nexus Dashboard Orchestrator) REST API Client
"""

import requests
import json
import urllib3
from typing import Dict, Any, Optional, List
import asyncio

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NDOClient:
    """NDO REST API client for multi-site orchestration"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 443, verify_ssl: bool = False):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{host}:{port}/mso/api/v1"
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.token = None
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    async def authenticate(self) -> Dict[str, Any]:
        """Authenticate with NDO and get session token"""
        try:
            auth_payload = {
                "username": self.username,
                "password": self.password
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                data=json.dumps(auth_payload),
                timeout=30
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                if "token" in auth_data:
                    self.token = auth_data["token"]
                    self.session.headers.update({
                        'Authorization': f'Bearer {self.token}'
                    })
                    return {"success": True, "token": self.token}
                else:
                    return {"success": False, "error": "Invalid authentication response"}
            else:
                return {"success": False, "error": f"Authentication failed: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Authentication error: {str(e)}"}
    
    async def test_connectivity(self) -> Dict[str, Any]:
        """Test connectivity to NDO"""
        try:
            response = self.session.get(
                f"{self.base_url}/platform/health",
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Connectivity test successful"}
            else:
                return {"success": False, "error": f"Connectivity test failed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"Connectivity error: {str(e)}"}
    
    async def get_sites(self) -> Dict[str, Any]:
        """Get list of sites managed by NDO"""
        try:
            response = self.session.get(
                f"{self.base_url}/sites",
                timeout=30
            )
            
            if response.status_code == 200:
                sites_data = response.json()
                return {"success": True, "sites": sites_data.get("sites", [])}
            else:
                return {"success": False, "error": f"Failed to get sites: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Sites query error: {str(e)}"}
    
    async def create_schema(self, schema_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a schema in NDO"""
        try:
            schema_payload = {
                "displayName": schema_config["name"],
                "description": schema_config.get("description", ""),
                "templates": []
            }
            
            for template in schema_config.get("templates", []):
                template_payload = {
                    "name": template["name"],
                    "displayName": template["name"],
                    "tenantId": template.get("tenant_id", ""),
                    "anps": [],
                    "vrfs": [],
                    "bds": [],
                    "contracts": [],
                    "filters": [],
                    "externalEpgs": [],
                    "serviceGraphs": [],
                    "intersiteL3outs": []
                }
                schema_payload["templates"].append(template_payload)
            
            response = self.session.post(
                f"{self.base_url}/schemas",
                data=json.dumps(schema_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                schema_data = response.json()
                return {"success": True, "schema_id": schema_data.get("id"), "message": f"Schema '{schema_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create schema: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Schema creation error: {str(e)}"}
    
    async def deploy_template(self, schema_id: str, template_name: str, sites: List[str]) -> Dict[str, Any]:
        """Deploy a template to specified sites"""
        try:
            deploy_payload = {
                "schemaId": schema_id,
                "templateName": template_name,
                "sites": sites
            }
            
            response = self.session.post(
                f"{self.base_url}/schemas/{schema_id}/templates/{template_name}/deploy",
                data=json.dumps(deploy_payload),
                timeout=60
            )
            
            if response.status_code in [200, 202]:
                deploy_data = response.json()
                return {"success": True, "deployment_id": deploy_data.get("id"), "message": f"Template '{template_name}' deployment started"}
            else:
                return {"success": False, "error": f"Failed to deploy template: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Template deployment error: {str(e)}"}
    
    async def get_deployment_status(self, deployment_id: str) -> Dict[str, Any]:
        """Get deployment status"""
        try:
            response = self.session.get(
                f"{self.base_url}/deployments/{deployment_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                deployment_data = response.json()
                return {"success": True, "deployment": deployment_data}
            else:
                return {"success": False, "error": f"Failed to get deployment status: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"Deployment status query error: {str(e)}"}
    
    async def create_tenant_in_template(self, schema_id: str, template_name: str, tenant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tenant in a schema template"""
        try:
            tenant_payload = {
                "name": tenant_config["name"],
                "displayName": tenant_config["name"],
                "description": tenant_config.get("description", "")
            }
            
            response = self.session.post(
                f"{self.base_url}/schemas/{schema_id}/templates/{template_name}/tenants",
                data=json.dumps(tenant_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"Tenant '{tenant_config['name']}' added to template"}
            else:
                return {"success": False, "error": f"Failed to create tenant in template: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Tenant creation error: {str(e)}"}
    
    async def create_vrf_in_template(self, schema_id: str, template_name: str, vrf_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a VRF in a schema template"""
        try:
            vrf_payload = {
                "name": vrf_config["name"],
                "displayName": vrf_config["name"],
                "description": vrf_config.get("description", ""),
                "vzAnyEnabled": vrf_config.get("vzany_enabled", False),
                "preferredGroup": vrf_config.get("preferred_group", False)
            }
            
            response = self.session.post(
                f"{self.base_url}/schemas/{schema_id}/templates/{template_name}/vrfs",
                data=json.dumps(vrf_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"VRF '{vrf_config['name']}' added to template"}
            else:
                return {"success": False, "error": f"Failed to create VRF in template: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"VRF creation error: {str(e)}"}
