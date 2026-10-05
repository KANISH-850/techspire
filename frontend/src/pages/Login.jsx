import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import { ShieldCheck, Activity, Key, User, AlertCircle } from 'lucide-react';

export default function Login() {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('admin123');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim() || !password.trim()) return;

    try {
      setLoading(true);
      setError(null);
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      console.error("Login failed:", err);
      setError(err.response?.data?.detail || "Invalid credentials or backend unavailable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen items-center justify-center bg-[#0b1120] text-slate-100 p-4 font-sans">
      <div className="w-full max-w-md bg-[#1e293b]/90 border border-slate-700/60 backdrop-blur-xl p-8 rounded-2xl shadow-2xl space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-cyan-500 via-blue-600 to-indigo-600 flex items-center justify-center text-white font-black text-2xl mx-auto shadow-lg shadow-cyan-500/30">
            T
          </div>
          <h1 className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent">
            TechSpire HMS
          </h1>
          <p className="text-xs uppercase tracking-widest text-slate-400 font-semibold">
            Unified AI Healthcare System
          </p>
        </div>

        {error && (
          <div className="bg-rose-500/10 border border-rose-500/30 p-3 rounded-xl flex items-center gap-3 text-rose-400 text-xs font-medium">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Username
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="w-full bg-[#0f172a] border border-slate-700 focus:border-cyan-500 rounded-xl pl-9 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition-colors"
                placeholder="Enter username..."
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Key className="w-4 h-4 text-slate-400 absolute left-3 top-3.5" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full bg-[#0f172a] border border-slate-700 focus:border-cyan-500 rounded-xl pl-9 pr-4 py-2.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition-colors"
                placeholder="Enter password..."
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-cyan-500 via-blue-600 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold py-3 rounded-xl text-sm shadow-lg shadow-cyan-500/25 transition-all flex items-center justify-center gap-2"
          >
            {loading ? (
              <Activity className="w-4 h-4 animate-spin" />
            ) : (
              <ShieldCheck className="w-4 h-4" />
            )}
            <span>{loading ? 'Authenticating...' : 'Sign In to Portal'}</span>
          </button>
        </form>

        <div className="border-t border-slate-800 pt-4 text-center">
          <p className="text-[11px] text-slate-400">
            Default credentials: <span className="font-mono text-cyan-400 font-bold">admin</span> / <span className="font-mono text-cyan-400 font-bold">admin123</span>
          </p>
        </div>
      </div>
    </div>
  );
}
