import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './auth/AuthContext';
import ProtectedRoute from './auth/ProtectedRoute';
import TechSpireShell from './components/layout/TechSpireShell';

// Pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import Appointments from './pages/Appointments';
import Admissions from './pages/Admissions';
import Beds from './pages/Beds';
import Chatbot from './pages/Chatbot';
import PredictiveAnalytics from './pages/PredictiveAnalytics';
import Reports from './pages/Reports';
import Inventory from './pages/Inventory';
import Procurement from './pages/Procurement';

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Authentication Route */}
          <Route path="/login" element={<Login />} />

          {/* Protected Routes in Unified TechSpire Shell */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <TechSpireShell>
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/patients" element={<Patients />} />
                    <Route path="/appointments" element={<Appointments />} />
                    <Route path="/admissions" element={<Admissions />} />
                    <Route path="/beds" element={<Beds />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/predictive" element={<PredictiveAnalytics />} />
                    <Route path="/predictive-analytics" element={<Navigate to="/predictive" replace />} />
                    <Route path="/reports" element={<Reports />} />
                    <Route path="/inventory" element={<Inventory />} />
                    <Route path="/procurement" element={<Procurement />} />
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </TechSpireShell>
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
