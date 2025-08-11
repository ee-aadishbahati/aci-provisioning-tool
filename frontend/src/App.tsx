import React, { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import Sidebar from './components/Sidebar'
import Dashboard from './components/Dashboard'
import ConfigurationForm from './components/ConfigurationForm'
import JobsList from './components/JobsList'
import JobDetails from './components/JobDetails'
import Templates from './components/Templates'
import { Toaster } from './components/Toaster'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        
        <div className="flex">
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          
          <main className="flex-1 p-6 lg:ml-64">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/configure" element={<ConfigurationForm />} />
              <Route path="/jobs" element={<JobsList />} />
              <Route path="/jobs/:jobId" element={<JobDetails />} />
              <Route path="/templates" element={<Templates />} />
            </Routes>
          </main>
        </div>
        
        <Toaster />
      </div>
    </Router>
  )
}

export default App
