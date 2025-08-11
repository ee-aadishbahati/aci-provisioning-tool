export interface APICCredentials {
  host: string
  username: string
  password: string
  port: number
  verify_ssl: boolean
}

export interface NDOCredentials {
  host: string
  username: string
  password: string
  port: number
  verify_ssl: boolean
}

export interface TenantConfig {
  name: string
  description?: string
}

export interface VRFConfig {
  name: string
  tenant: string
  description?: string
  enforcement: string
}

export interface BridgeDomainConfig {
  name: string
  tenant: string
  vrf: string
  subnet?: string
  description?: string
}

export interface ApplicationProfileConfig {
  name: string
  tenant: string
  description?: string
}

export interface EPGConfig {
  name: string
  tenant: string
  app_profile: string
  bridge_domain: string
  description?: string
}

export interface FabricConfig {
  site_code: 'AUNTH' | 'AUSTH' | 'AUTER'
  fabric_type: 'it' | 'ot'
  apic_credentials: APICCredentials
  tenants: TenantConfig[]
  vrfs: VRFConfig[]
  bridge_domains: BridgeDomainConfig[]
  app_profiles: ApplicationProfileConfig[]
  epgs: EPGConfig[]
}

export interface ProvisioningJob {
  id?: number
  name: string
  template_id?: number
  fabric_config: FabricConfig
  status: 'pending' | 'running' | 'completed' | 'failed'
  progress: number
  created_at?: string
  started_at?: string
  completed_at?: string
}

export interface TaskLog {
  id: number
  job_id: number
  task_name: string
  status: 'info' | 'success' | 'error' | 'warning'
  message: string
  details?: any
  timestamp: string
}

export interface Template {
  id: number
  name: string
  type: 'fabric' | 'ndo'
  description: string
  config: any
  created_at: string
  updated_at: string
}

export interface ValidationResult {
  valid: boolean
  errors: string[]
  warnings: string[]
}

export interface Statistics {
  job_statistics: Record<string, number>
  recent_jobs_24h: number
  total_api_calls: number
  timestamp: string
}

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message?: string
  duration?: number
}
