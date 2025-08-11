import React from 'react'
import { CheckCircle, AlertCircle, Info, X } from 'lucide-react'
import { useToast } from '../hooks/useToast'

const Toaster: React.FC = () => {
  const { toasts, removeToast } = useToast()

  const getIcon = (type: string) => {
    switch (type) {
      case 'success': return CheckCircle
      case 'error': return AlertCircle
      case 'warning': return AlertCircle
      case 'info': return Info
      default: return Info
    }
  }

  const getColors = (type: string) => {
    switch (type) {
      case 'success': return 'bg-success-50 border-success-200 text-success-800'
      case 'error': return 'bg-error-50 border-error-200 text-error-800'
      case 'warning': return 'bg-warning-50 border-warning-200 text-warning-800'
      case 'info': return 'bg-primary-50 border-primary-200 text-primary-800'
      default: return 'bg-gray-50 border-gray-200 text-gray-800'
    }
  }

  return (
    <div className="fixed top-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => {
        const Icon = getIcon(toast.type)
        return (
          <div
            key={toast.id}
            className={`max-w-sm w-full border rounded-lg p-4 shadow-lg ${getColors(toast.type)}`}
          >
            <div className="flex items-start">
              <Icon className="w-5 h-5 mt-0.5 mr-3 flex-shrink-0" />
              <div className="flex-1">
                <h4 className="font-medium">{toast.title}</h4>
                {toast.message && (
                  <p className="mt-1 text-sm opacity-90">{toast.message}</p>
                )}
              </div>
              <button
                onClick={() => removeToast(toast.id)}
                className="ml-3 flex-shrink-0 opacity-70 hover:opacity-100"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default Toaster
