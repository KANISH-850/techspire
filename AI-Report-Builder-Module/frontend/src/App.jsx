import React from 'react'
import ReportBuilder from './modules/reports/pages/ReportBuilder'

function App() {
  return (
    <div className="min-h-screen">
      <nav className="bg-white shadow-sm border-b border-slate-200 px-6 py-4 no-print">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">AI</span>
            </div>
            <h1 className="text-xl font-semibold text-slate-800">Report Builder</h1>
          </div>
        </div>
      </nav>
      
      <main>
        <ReportBuilder />
      </main>
    </div>
  )
}

export default App
