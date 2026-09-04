import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './modules/predictive/pages/Dashboard';

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Routes>
        <Route path="/" element={<Navigate to="/predictive-analytics" replace />} />
        <Route path="/predictive-analytics/*" element={<Dashboard />} />
      </Routes>
    </div>
  );
}

export default App;
