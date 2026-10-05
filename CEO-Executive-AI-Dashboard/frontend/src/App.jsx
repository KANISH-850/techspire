import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TechSpireShell from '../../shared/TechSpireShell';

function App() {
  return (
    <Router>
      <TechSpireShell activeModuleId="ceo">
        <Routes>
          <Route path="/" element={<Dashboard />} />
        </Routes>
      </TechSpireShell>
    </Router>
  );
}

export default App;
