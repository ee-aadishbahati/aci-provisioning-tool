import React from 'react'
import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Settings, 
  List, 
  FileText, 
  X,
  Activity,
  Network
} from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const navItems = [
    { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/configure', icon: Settings, label: 'Configure' },
    { to: '/jobs', icon: List, label: 'Jobs' },
    { to: '/templates', icon: FileText, label: 'Templates' },
  ]

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 z-50 w-64 h-full bg-white border-r border-gray-200 transition-transform duration-300
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:z-auto
      `}>
        <div className="flex items-center justify-between p-6 border-b border-gray-200 lg:hidden">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <span className="text-lg font-semibold">ACI Tool</span>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <nav className="p-4 space-y-2">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => `
                flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors
                ${isActive 
                  ? 'bg-primary-50 text-primary-700 border-r-2 border-primary-600' 
                  : 'text-gray-700 hover:bg-gray-100'
                }
              `}
              onClick={() => window.innerWidth < 1024 && onClose()}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-4 left-4 right-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Network className="w-4 h-4 text-gray-600" />
              <span className="text-sm font-medium text-gray-900">Status</span>
            </div>
            <div className="text-xs text-gray-600">
              <div className="flex justify-between">
                <span>Backend:</span>
                <span className="text-success-600">Online</span>
              </div>
              <div className="flex justify-between">
                <span>Database:</span>
                <span className="text-success-600">Ready</span>
              </div>
            </div>
          </div>
        </div>
      </aside>
    </>
  )
}

export default Sidebar
