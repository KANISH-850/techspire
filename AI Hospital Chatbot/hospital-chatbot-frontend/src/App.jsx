import React from 'react';
import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, LineChart, FileText, Package } from 'lucide-react';
import Chatbot from './pages/Chatbot';
import Dashboard from './pages/Dashboard';
import PredictiveAnalytics from './pages/PredictiveAnalytics';
import ReportBuilder from './pages/ReportBuilder';
import Procurement from './pages/Procurement';
import './App.css';

function App() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'CEO Dashboard', icon: LayoutDashboard },
    { path: '/chatbot', label: 'AI Chatbot', icon: MessageSquare },
    { path: '/predictive-analytics', label: 'Predictive Analytics', icon: LineChart },
    { path: '/reports', label: 'Report Builder', icon: FileText },
    { path: '/procurement', label: 'Procurement', icon: Package }
  ];

  return (
    <div className="flex h-screen bg-[#F8FAFC]">
      {/* Global Sidebar for HMS Modules */}
      <aside className="w-64 bg-[#0F172A] text-white flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <h1 className="text-xl font-bold flex items-center gap-2 text-white">
            <span className="text-[#38BDF8]">✚</span> HealthSync AI
          </h1>
        </div>
        <nav className="flex-1 py-4">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-6 py-3 transition-colors ${
                  isActive 
                    ? 'bg-[#1E293B] text-white border-l-4 border-[#38BDF8]' 
                    : 'text-gray-400 hover:bg-[#1E293B] hover:text-white border-l-4 border-transparent'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-auto flex flex-col relative">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/chatbot" element={<Chatbot />} />
          <Route path="/predictive-analytics" element={<PredictiveAnalytics />} />
          <Route path="/reports" element={<ReportBuilder />} />
          <Route path="/procurement" element={<Procurement />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
