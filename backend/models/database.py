"""
Database models and initialization
"""

import sqlite3
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
import threading

class Database:
    """Thread-safe SQLite database wrapper"""
    
    def __init__(self, db_path: str = "aci_provisioning.db"):
        self.db_path = db_path
        self._lock = threading.RLock()
        self.init_tables()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_tables(self):
        """Initialize database tables"""
        with self._lock:
            conn = self.get_connection()
            try:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS templates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        type TEXT NOT NULL,
                        description TEXT,
                        config JSON NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS provisioning_jobs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        template_id INTEGER,
                        fabric_config JSON NOT NULL,
                        status TEXT DEFAULT 'pending',
                        progress INTEGER DEFAULT 0,
                        started_at TIMESTAMP,
                        completed_at TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (template_id) REFERENCES templates (id)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS task_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_id INTEGER NOT NULL,
                        task_name TEXT NOT NULL,
                        status TEXT NOT NULL,
                        message TEXT,
                        details JSON,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (job_id) REFERENCES provisioning_jobs (id)
                    )
                """)
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS api_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_id INTEGER,
                        endpoint TEXT NOT NULL,
                        method TEXT NOT NULL,
                        request_data JSON,
                        response_data JSON,
                        status_code INTEGER,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (job_id) REFERENCES provisioning_jobs (id)
                    )
                """)
                
                conn.commit()
                self._insert_default_templates(conn)
                
            finally:
                conn.close()
    
    def _insert_default_templates(self, conn):
        """Insert default configuration templates"""
        default_templates = [
            {
                "name": "Basic ACI Fabric",
                "type": "fabric",
                "description": "Basic ACI fabric configuration with common tenants",
                "config": {
                    "tenants": [
                        {"name": "common", "description": "Common tenant"},
                        {"name": "mgmt", "description": "Management tenant"}
                    ],
                    "vrfs": [
                        {"name": "prod_vrf", "tenant": "common", "enforcement": "enforced"},
                        {"name": "dev_vrf", "tenant": "common", "enforcement": "unenforced"}
                    ],
                    "bridge_domains": [
                        {"name": "web_bd", "tenant": "common", "vrf": "prod_vrf", "subnet": "10.1.1.1/24"},
                        {"name": "app_bd", "tenant": "common", "vrf": "prod_vrf", "subnet": "10.1.2.1/24"}
                    ]
                }
            },
            {
                "name": "NDO Multi-Site Policy",
                "type": "ndo",
                "description": "Multi-site policy template for NDO",
                "config": {
                    "schema": {
                        "name": "multi_site_schema",
                        "templates": [
                            {
                                "name": "common_template",
                                "tenants": ["common"],
                                "sites": ["site1", "site2"]
                            }
                        ]
                    }
                }
            }
        ]
        
        for template in default_templates:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO templates (name, type, description, config)
                    VALUES (?, ?, ?, ?)
                """, (
                    template["name"],
                    template["type"],
                    template["description"],
                    json.dumps(template["config"])
                ))
            except sqlite3.IntegrityError:
                pass

_db_instance = None
_db_lock = threading.Lock()

def get_database() -> Database:
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        with _db_lock:
            if _db_instance is None:
                _db_instance = Database()
    return _db_instance

def init_database():
    """Initialize the database"""
    get_database()
    print("Database initialized successfully")
