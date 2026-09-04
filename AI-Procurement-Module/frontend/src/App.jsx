import React from 'react'
import Procurement from './pages/Procurement'

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">TechSpire HMS</span>
            </div>
          </div>
        </div>
      </nav>
      <main>
        <Procurement />
      </main>
    </div>
  )
}

export default App
