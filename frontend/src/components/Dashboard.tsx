import React, { useState, useEffect } from 'react'
import { 
  Activity, 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  TrendingUp,
  Server,
  Network,
  Database
} from 'lucide-react'
import { Statistics, ProvisioningJob } from '../types'
import apiService from '../services/api'
import { useToast } from '../hooks/useToast'

const Dashboard: React.FC = () => {
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [recentJobs, setRecentJobs] = useState<ProvisioningJob[]>([])
  const [loading, setLoading] = useState(true)
  const { addToast } = useToast()

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      const [statsData, jobsData] = await Promise.all([
        apiService.getStatistics(),
        apiService.getProvisioningJobs()
      ])
      
      setStatistics(statsData)
      setRecentJobs(jobsData.slice(0, 5)) // Show only 5 most recent
    } catch (error) {
      console.error('Failed to load dashboard data:', error)
      addToast({
        type: 'error',
        title: 'Error',
        message: 'Failed to load dashboard data'
      })
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-success-600 bg-success-50'
      case 'running': return 'text-primary-600 bg-primary-50'
      case 'failed': return 'text-error-600 bg-error-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return CheckCircle
      case 'running': return Activity
      case 'failed': return AlertCircle
      default: return Clock
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of ACI provisioning activities</p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Jobs</p>
              <p className="text-2xl font-bold text-gray-900">
                {statistics ? Object.values(statistics.job_statistics).reduce((a, b) => a + b, 0) : 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <Activity className="w-6 h-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Completed</p>
              <p className="text-2xl font-bold text-success-600">
                {statistics?.job_statistics.completed || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
              <CheckCircle className="w-6 h-6 text-success-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Running</p>
              <p className="text-2xl font-bold text-primary-600">
                {statistics?.job_statistics.running || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Failed</p>
              <p className="text-2xl font-bold text-error-600">
                {statistics?.job_statistics.failed || 0}
              </p>
            </div>
            <div className="w-12 h-12 bg-error-100 rounded-lg flex items-center justify-center">
              <AlertCircle className="w-6 h-6 text-error-600" />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Jobs */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">Recent Jobs</h2>
            <TrendingUp className="w-5 h-5 text-gray-400" />
          </div>
          
          <div className="space-y-3">
            {recentJobs.length > 0 ? (
              recentJobs.map((job) => {
                const StatusIcon = getStatusIcon(job.status)
                return (
                  <div key={job.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <StatusIcon className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="font-medium text-gray-900">{job.name}</p>
                        <p className="text-sm text-gray-600">
                          {job.fabric_config.site_code} - {job.fabric_config.fabric_type.toUpperCase()}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>
                      {job.status === 'running' && (
                        <div className="mt-1">
                          <div className="progress-bar w-16">
                            <div 
                              className="progress-fill" 
                              style={{ width: `${job.progress}%` }}
                            />
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )
              })
            ) : (
              <div className="text-center py-8 text-gray-500">
                <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No jobs found</p>
              </div>
            )}
          </div>
        </div>

        {/* System Status */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">System Status</h2>
            <Server className="w-5 h-5 text-gray-400" />
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                  <Server className="w-4 h-4 text-success-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Backend Service</p>
                  <p className="text-sm text-gray-600">FastAPI Server</p>
                </div>
              </div>
              <span className="px-2 py-1 bg-success-100 text-success-700 rounded-full text-xs font-medium">
                Online
              </span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
                  <Database className="w-4 h-4 text-success-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">Database</p>
                  <p className="text-sm text-gray-600">SQLite Storage</p>
                </div>
              </div>
              <span className="px-2 py-1 bg-success-100 text-success-700 rounded-full text-xs font-medium">
                Ready
              </span>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-primary-100 rounded-lg flex items-center justify-center">
                  <Network className="w-4 h-4 text-primary-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">API Calls</p>
                  <p className="text-sm text-gray-600">Total Requests</p>
                </div>
              </div>
              <span className="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
                {statistics?.total_api_calls || 0}
              </span>
            </div>

            <div className="pt-4 border-t border-gray-200">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">Last 24 hours</span>
                <span className="font-medium text-gray-900">
                  {statistics?.recent_jobs_24h || 0} jobs
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
