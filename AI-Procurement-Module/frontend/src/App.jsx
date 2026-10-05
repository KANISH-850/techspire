import React from 'react';
import Procurement from './pages/Procurement';
import TechSpireShell from '../../shared/TechSpireShell';

function App() {
  return (
    <TechSpireShell activeModuleId="procurement">
      <Procurement />
    </TechSpireShell>
  );
}

export default App;
