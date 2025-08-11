import axios, { AxiosInstance, AxiosResponse } from 'axios'
import { 
  ProvisioningJob, 
  TaskLog, 
  Template, 
  ValidationResult, 
  Statistics,
  FabricConfig 
} from '../types'

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
        return config
      },
      (error) => {
        console.error('API Request Error:', error)
        return Promise.reject(error)
      }
    )

    this.client.interceptors.response.use(
      (response) => {
        console.log(`API Response: ${response.status} ${response.config.url}`)
        return response
      },
      (error) => {
        console.error('API Response Error:', error.response?.data || error.message)
        return Promise.reject(error)
      }
    )
  }

  async healthCheck(): Promise<any> {
    const response = await this.client.get('/status/health')
    return response.data
  }

  async getStatistics(): Promise<Statistics> {
    const response = await this.client.get('/status/stats')
    return response.data
  }

  async getTemplates(): Promise<Template[]> {
    const response = await this.client.get('/status/templates')
    return response.data
  }

  async getTemplate(id: number): Promise<Template> {
    const response = await this.client.get(`/status/templates/${id}`)
    return response.data
  }

  async createProvisioningJob(job: ProvisioningJob): Promise<any> {
    const response = await this.client.post('/provisioning/jobs', job)
    return response.data
  }

  async getProvisioningJobs(): Promise<ProvisioningJob[]> {
    const response = await this.client.get('/provisioning/jobs')
    return response.data
  }

  async getProvisioningJob(id: number): Promise<ProvisioningJob> {
    const response = await this.client.get(`/provisioning/jobs/${id}`)
    return response.data
  }

  async deleteProvisioningJob(id: number): Promise<any> {
    const response = await this.client.delete(`/provisioning/jobs/${id}`)
    return response.data
  }

  async getJobLogs(jobId: number): Promise<TaskLog[]> {
    const response = await this.client.get(`/provisioning/jobs/${jobId}/logs`)
    return response.data
  }

  async validateConfiguration(config: FabricConfig): Promise<ValidationResult> {
    const response = await this.client.post('/provisioning/validate-config', config)
    return response.data
  }

  async getRecentLogs(limit: number = 100): Promise<TaskLog[]> {
    const response = await this.client.get(`/status/logs/recent?limit=${limit}`)
    return response.data
  }
}

export const apiService = new ApiService()
export default apiService
