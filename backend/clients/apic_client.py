"""
APIC REST API Client
"""

import requests
import json
import urllib3
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APICClient:
    """APIC REST API client for ACI provisioning"""
    
    def __init__(self, host: str, username: str, password: str, port: int = 443, verify_ssl: bool = False):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{host}:{port}/api"
        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.token = None
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    async def authenticate(self) -> Dict[str, Any]:
        """Authenticate with APIC and get session token"""
        try:
            auth_payload = {
                "aaaUser": {
                    "attributes": {
                        "name": self.username,
                        "pwd": self.password
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/aaaLogin.json",
                data=json.dumps(auth_payload),
                timeout=30
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                if "imdata" in auth_data and len(auth_data["imdata"]) > 0:
                    self.token = auth_data["imdata"][0]["aaaLogin"]["attributes"]["token"]
                    self.session.headers.update({
                        'APIC-Cookie': self.token
                    })
                    return {"success": True, "token": self.token}
                else:
                    return {"success": False, "error": "Invalid authentication response"}
            else:
                return {"success": False, "error": f"Authentication failed: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Authentication error: {str(e)}"}
    
    async def test_connectivity(self) -> Dict[str, Any]:
        """Test connectivity to APIC"""
        try:
            response = self.session.get(
                f"{self.base_url}/class/topSystem.json",
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Connectivity test successful"}
            else:
                return {"success": False, "error": f"Connectivity test failed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"Connectivity error: {str(e)}"}
    
    async def create_tenant(self, tenant_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tenant in ACI"""
        try:
            tenant_payload = {
                "fvTenant": {
                    "attributes": {
                        "name": tenant_config["name"],
                        "descr": tenant_config.get("description", ""),
                        "status": "created"
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/node/mo/uni/tn-{tenant_config['name']}.json",
                data=json.dumps(tenant_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"Tenant '{tenant_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create tenant: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Tenant creation error: {str(e)}"}
    
    async def create_vrf(self, vrf_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a VRF (Context) in ACI"""
        try:
            vrf_payload = {
                "fvCtx": {
                    "attributes": {
                        "name": vrf_config["name"],
                        "descr": vrf_config.get("description", ""),
                        "pcEnfPref": vrf_config.get("enforcement", "enforced"),
                        "status": "created"
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/node/mo/uni/tn-{vrf_config['tenant']}/ctx-{vrf_config['name']}.json",
                data=json.dumps(vrf_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"VRF '{vrf_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create VRF: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"VRF creation error: {str(e)}"}
    
    async def create_bridge_domain(self, bd_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Bridge Domain in ACI"""
        try:
            bd_payload = {
                "fvBD": {
                    "attributes": {
                        "name": bd_config["name"],
                        "descr": bd_config.get("description", ""),
                        "status": "created"
                    },
                    "children": [
                        {
                            "fvRsCtx": {
                                "attributes": {
                                    "tnFvCtxName": bd_config["vrf"]
                                }
                            }
                        }
                    ]
                }
            }
            
            if bd_config.get("subnet"):
                subnet_payload = {
                    "fvSubnet": {
                        "attributes": {
                            "ip": bd_config["subnet"],
                            "scope": "public",
                            "status": "created"
                        }
                    }
                }
                bd_payload["fvBD"]["children"].append(subnet_payload)
            
            response = self.session.post(
                f"{self.base_url}/node/mo/uni/tn-{bd_config['tenant']}/BD-{bd_config['name']}.json",
                data=json.dumps(bd_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"Bridge Domain '{bd_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create Bridge Domain: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Bridge Domain creation error: {str(e)}"}
    
    async def create_application_profile(self, ap_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create an Application Profile in ACI"""
        try:
            ap_payload = {
                "fvAp": {
                    "attributes": {
                        "name": ap_config["name"],
                        "descr": ap_config.get("description", ""),
                        "status": "created"
                    }
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/node/mo/uni/tn-{ap_config['tenant']}/ap-{ap_config['name']}.json",
                data=json.dumps(ap_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"Application Profile '{ap_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create Application Profile: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"Application Profile creation error: {str(e)}"}
    
    async def create_epg(self, epg_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create an EPG (Endpoint Group) in ACI"""
        try:
            epg_payload = {
                "fvAEPg": {
                    "attributes": {
                        "name": epg_config["name"],
                        "descr": epg_config.get("description", ""),
                        "status": "created"
                    },
                    "children": [
                        {
                            "fvRsBd": {
                                "attributes": {
                                    "tnFvBDName": epg_config["bridge_domain"]
                                }
                            }
                        }
                    ]
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/node/mo/uni/tn-{epg_config['tenant']}/ap-{epg_config['app_profile']}/epg-{epg_config['name']}.json",
                data=json.dumps(epg_payload),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "message": f"EPG '{epg_config['name']}' created successfully"}
            else:
                return {"success": False, "error": f"Failed to create EPG: {response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"success": False, "error": f"EPG creation error: {str(e)}"}
    
    async def get_fabric_nodes(self) -> Dict[str, Any]:
        """Get fabric node information"""
        try:
            response = self.session.get(
                f"{self.base_url}/class/fabricNode.json",
                timeout=30
            )
            
            if response.status_code == 200:
                nodes_data = response.json()
                nodes = []
                for node_data in nodes_data.get("imdata", []):
                    node = node_data["fabricNode"]["attributes"]
                    nodes.append({
                        "id": node["id"],
                        "name": node["name"],
                        "role": node["role"],
                        "model": node["model"],
                        "serial": node["serial"]
                    })
                
                return {"success": True, "nodes": nodes}
            else:
                return {"success": False, "error": f"Failed to get fabric nodes: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": f"Fabric nodes query error: {str(e)}"}
