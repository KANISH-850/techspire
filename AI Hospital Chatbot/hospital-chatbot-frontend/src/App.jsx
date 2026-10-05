import React from 'react';
import { Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Chatbot from './pages/Chatbot';
import Dashboard from './pages/Dashboard';
import PredictiveAnalytics from './pages/PredictiveAnalytics';
import ReportBuilder from './pages/ReportBuilder';
import Procurement from './pages/Procurement';
import TechSpireShell from '../../../shared/TechSpireShell';
import './App.css';

function App() {
  const location = useLocation();
  const navigate = useNavigate();

  const getActiveModuleId = () => {
    const path = location.pathname;
    if (path.startsWith('/chatbot')) return 'chatbot';
    if (path.startsWith('/predictive-analytics')) return 'predictive';
    if (path.startsWith('/reports')) return 'reports';
    if (path.startsWith('/procurement')) return 'procurement';
    return 'ceo';
  };

  const handleNavigate = (mod) => {
    navigate(mod.path);
  };

  return (
    <TechSpireShell activeModuleId={getActiveModuleId()} onNavigate={handleNavigate}>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/predictive-analytics" element={<PredictiveAnalytics />} />
        <Route path="/reports" element={<ReportBuilder />} />
        <Route path="/procurement" element={<Procurement />} />
      </Routes>
    </TechSpireShell>
  );
}

export default App;
