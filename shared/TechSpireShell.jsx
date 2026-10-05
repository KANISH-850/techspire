import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, MessageSquare, LineChart, FileText, Package, 
  Sun, Moon, ShieldCheck, Activity, Layers, ExternalLink 
} from 'lucide-react';

const MODULES = [
  { id: 'ceo', name: 'CEO AI Dashboard', path: '/', port: 8004, icon: LayoutDashboard },
  { id: 'chatbot', name: 'Hospital AI Chatbot', path: '/chatbot', port: 8000, icon: MessageSquare },
  { id: 'predictive', name: 'Predictive Analytics', path: '/predictive-analytics', port: 8001, icon: LineChart },
  { id: 'reports', name: 'AI Report Builder', path: '/reports', port: 8002, icon: FileText },
  { id: 'procurement', name: 'AI Procurement', path: '/procurement', port: 8003, icon: Package }
];

export default function TechSpireShell({ activeModuleId = 'ceo', children, onNavigate }) {
  const [theme, setTheme] = useState(() => localStorage.getItem('techspire_theme') || 'dark');
  const [systemStatus, setSystemStatus] = useState('Online');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('techspire_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const handleNavClick = (mod) => {
    if (onNavigate) {
      onNavigate(mod);
    } else {
      // In standalone port mode, redirect or route if matching window location
      if (window.location.port && window.location.port !== String(mod.port)) {
        window.location.href = `http://localhost:${mod.port === 8004 ? 5173 : mod.port}`;
      } else {
        window.location.pathname = mod.path;
      }
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[var(--ts-bg)] text-[var(--ts-text-primary)] transition-colors duration-300">
      {/* Plug and Play Navigation Sidebar */}
      <aside className="w-64 bg-[var(--ts-bg-subtle)] border-r border-[var(--ts-border)] flex flex-col justify-between z-20 shadow-xl">
        <div>
          {/* Logo & Platform Title */}
          <div className="p-5 border-b border-[var(--ts-border)] flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-black text-lg shadow-lg shadow-cyan-500/20">
              T
            </div>
            <div>
              <h1 className="font-extrabold text-base tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
                TechSpire AI
              </h1>
              <p className="text-[10px] uppercase font-bold tracking-widest text-[var(--ts-text-muted)]">
                Enterprise Healthcare Suite
              </p>
            </div>
          </div>

          {/* Module Links */}
          <nav className="p-3 space-y-1">
            <div className="px-3 py-2 text-[11px] font-bold uppercase tracking-wider text-[var(--ts-text-muted)]">
              Modules
            </div>
            {MODULES.map(mod => {
              const Icon = mod.icon;
              const isActive = mod.id === activeModuleId;
              return (
                <button
                  key={mod.id}
                  onClick={() => handleNavClick(mod)}
                  className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                    isActive 
                      ? 'bg-gradient-to-r from-cyan-500/20 to-blue-600/20 text-cyan-400 border border-cyan-500/30 shadow-md shadow-cyan-500/10' 
                      : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)] hover:text-[var(--ts-text-primary)] border border-transparent'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-[var(--ts-text-muted)]'}`} />
                    <span>{mod.name}</span>
                  </div>
                  {isActive && <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Footer / System Status & Theme Controls */}
        <div className="p-4 border-t border-[var(--ts-border)] space-y-3 bg-[var(--ts-bg-floating)]/40">
          <div className="flex items-center justify-between px-2 text-xs">
            <span className="flex items-center gap-1.5 text-[var(--ts-text-secondary)]">
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              <span>Engine Status</span>
            </span>
            <span className="ts-badge ts-badge-success">{systemStatus}</span>
          </div>

          <button
            onClick={toggleTheme}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] text-xs font-semibold text-[var(--ts-text-secondary)] hover:text-[var(--ts-text-primary)] transition-colors"
          >
            <div className="flex items-center gap-2">
              {theme === 'dark' ? <Moon className="w-4 h-4 text-cyan-400" /> : <Sun className="w-4 h-4 text-amber-400" />}
              <span>{theme === 'dark' ? 'Dark Executive Mode' : 'Light Executive Mode'}</span>
            </div>
            <span className="text-[10px] text-[var(--ts-text-muted)] uppercase tracking-wider">Toggle</span>
          </button>
        </div>
      </aside>

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Header Bar */}
        <header className="h-16 px-6 border-b border-[var(--ts-border)] bg-[var(--ts-bg-subtle)]/80 backdrop-blur-md flex items-center justify-between z-10">
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-[var(--ts-text-muted)]">TechSpire Platform</span>
            <span className="text-[var(--ts-border)]">/</span>
            <span className="font-semibold text-sm text-[var(--ts-text-primary)]">
              {MODULES.find(m => m.id === activeModuleId)?.name || 'Executive Module'}
            </span>
            <span className="ts-badge ts-badge-cyan">Plug & Play Unified</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs font-medium text-[var(--ts-text-secondary)] bg-[var(--ts-card-bg)] px-3 py-1.5 rounded-lg border border-[var(--ts-border)]">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              <span>Single Theme Active</span>
            </div>
          </div>
        </header>

        {/* Content Body */}
        <main className="flex-1 overflow-auto p-6 bg-[var(--ts-bg)]">
          {children}
        </main>
      </div>
    </div>
  );
}
