import { useState, useCallback } from 'react'
import { Toast } from '../types'

let toastId = 0

const useToast = () => {
  const [toasts, setToasts] = useState<Toast[]>([])

  const addToast = useCallback((toast: Omit<Toast, 'id'>) => {
    const id = (++toastId).toString()
    const newToast: Toast = {
      ...toast,
      id,
      duration: toast.duration || 5000
    }

    setToasts(prev => [...prev, newToast])

    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id))
    }, newToast.duration)
  }, [])

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id))
  }, [])

  return { toasts, addToast, removeToast }
}

export { useToast }
