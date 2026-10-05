import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../auth/AuthContext';
import { 
  LayoutDashboard, MessageSquare, LineChart, FileText, Package, 
  Users, Calendar, Activity, Bed, ShoppingCart, Sun, Moon, 
  ShieldCheck, LogOut, User as UserIcon
} from 'lucide-react';

const MODULES = [
  { id: 'dashboard', name: 'CEO AI Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { id: 'patients', name: 'Patients', path: '/patients', icon: Users },
  { id: 'appointments', name: 'Appointments', path: '/appointments', icon: Calendar },
  { id: 'admissions', name: 'Admissions', path: '/admissions', icon: Activity },
  { id: 'beds', name: 'Bed Management', path: '/beds', icon: Bed },
  { id: 'chatbot', name: 'Hospital AI Chatbot', path: '/chatbot', icon: MessageSquare },
  { id: 'predictive', name: 'Predictive Analytics', path: '/predictive', icon: LineChart },
  { id: 'reports', name: 'AI Report Builder', path: '/reports', icon: FileText },
  { id: 'inventory', name: 'Inventory', path: '/inventory', icon: Package },
  { id: 'procurement', name: 'AI Procurement', path: '/procurement', icon: ShoppingCart },
];

export default function TechSpireShell({ children }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  
  const [theme, setTheme] = useState(() => localStorage.getItem('techspire_theme') || 'dark');
  const [systemStatus] = useState('Online');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('techspire_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  const getActiveModuleId = () => {
    const path = location.pathname;
    if (path.startsWith('/patients')) return 'patients';
    if (path.startsWith('/appointments')) return 'appointments';
    if (path.startsWith('/admissions')) return 'admissions';
    if (path.startsWith('/beds')) return 'beds';
    if (path.startsWith('/chatbot')) return 'chatbot';
    if (path.startsWith('/predictive')) return 'predictive';
    if (path.startsWith('/reports')) return 'reports';
    if (path.startsWith('/inventory')) return 'inventory';
    if (path.startsWith('/procurement')) return 'procurement';
    return 'dashboard';
  };

  const activeModuleId = getActiveModuleId();
  const activeModule = MODULES.find(m => m.id === activeModuleId) || MODULES[0];

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[var(--ts-bg)] text-[var(--ts-text-primary)] transition-colors duration-300">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-[var(--ts-bg-subtle)] border-r border-[var(--ts-border)] flex flex-col justify-between z-20 shadow-xl shrink-0">
        <div className="flex flex-col h-full overflow-hidden">
          {/* Header & Logo */}
          <div className="p-4 border-b border-[var(--ts-border)] flex items-center gap-3 shrink-0">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-black text-xl shadow-lg shadow-cyan-500/20">
              T
            </div>
            <div>
              <h1 className="font-extrabold text-base tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
                TechSpire HMS
              </h1>
              <p className="text-[10px] uppercase font-bold tracking-widest text-[var(--ts-text-muted)]">
                AI Hospital Suite
              </p>
            </div>
          </div>

          {/* Module Links List */}
          <nav className="p-3 space-y-1 overflow-y-auto flex-1">
            <div className="px-3 py-1 text-[10px] font-bold uppercase tracking-wider text-[var(--ts-text-muted)]">
              Core Applications
            </div>
            {MODULES.map(mod => {
              const Icon = mod.icon;
              const isActive = mod.id === activeModuleId;
              return (
                <button
                  key={mod.id}
                  onClick={() => navigate(mod.path)}
                  className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-medium text-xs transition-all duration-200 ${
                    isActive 
                      ? 'bg-gradient-to-r from-cyan-500/20 to-blue-600/20 text-cyan-400 border border-cyan-500/30 shadow-md shadow-cyan-500/10 font-bold' 
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

        {/* Footer / User Session & Controls */}
        <div className="p-4 border-t border-[var(--ts-border)] space-y-3 bg-[var(--ts-bg-floating)]/40 shrink-0">
          {/* User Profile info */}
          <div className="flex items-center justify-between bg-[var(--ts-card-bg)] p-2.5 rounded-xl border border-[var(--ts-border)]">
            <div className="flex items-center gap-2 overflow-hidden">
              <div className="w-7 h-7 rounded-lg bg-cyan-500/20 flex items-center justify-center text-cyan-400 font-bold shrink-0">
                <UserIcon className="w-4 h-4" />
              </div>
              <div className="truncate">
                <p className="text-xs font-bold text-[var(--ts-text-primary)] truncate">
                  {user?.full_name || user?.username || 'Administrator'}
                </p>
                <p className="text-[10px] text-[var(--ts-text-muted)] uppercase tracking-wider truncate">
                  {user?.role || 'Admin'}
                </p>
              </div>
            </div>
            <button
              onClick={logout}
              title="Logout"
              className="p-1.5 rounded-lg text-rose-400 hover:bg-rose-500/10 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>

          <div className="flex items-center justify-between px-1 text-xs">
            <span className="flex items-center gap-1.5 text-[var(--ts-text-secondary)] text-[11px]">
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              <span>Backend DB Status</span>
            </span>
            <span className="ts-badge ts-badge-success text-[10px]">{systemStatus}</span>
          </div>

          <button
            onClick={toggleTheme}
            className="w-full flex items-center justify-between px-3 py-2 rounded-lg bg-[var(--ts-bg-subtle)] border border-[var(--ts-border)] text-xs font-semibold text-[var(--ts-text-secondary)] hover:text-[var(--ts-text-primary)] transition-colors"
          >
            <div className="flex items-center gap-2">
              {theme === 'dark' ? <Moon className="w-4 h-4 text-cyan-400" /> : <Sun className="w-4 h-4 text-amber-400" />}
              <span>{theme === 'dark' ? 'Dark Mode' : 'Light Mode'}</span>
            </div>
            <span className="text-[10px] text-[var(--ts-text-muted)] uppercase">Toggle</span>
          </button>
        </div>
      </aside>

      {/* Main Content Viewport */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Header Bar */}
        <header className="h-16 px-6 border-b border-[var(--ts-border)] bg-[var(--ts-bg-subtle)]/80 backdrop-blur-md flex items-center justify-between z-10 shrink-0">
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-[var(--ts-text-muted)]">TechSpire HMS</span>
            <span className="text-[var(--ts-border)]">/</span>
            <span className="font-semibold text-sm text-[var(--ts-text-primary)]">
              {activeModule.name}
            </span>
            <span className="ts-badge ts-badge-cyan text-[10px]">Unified SPA</span>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-xs font-medium text-[var(--ts-text-secondary)] bg-[var(--ts-card-bg)] px-3 py-1.5 rounded-lg border border-[var(--ts-border)]">
              <ShieldCheck className="w-4 h-4 text-cyan-400" />
              <span>JWT Authenticated</span>
            </div>
          </div>
        </header>

        {/* View Content */}
        <main className="flex-1 overflow-auto p-6 bg-[var(--ts-bg)]">
          {children}
        </main>
      </div>
    </div>
  );
}
