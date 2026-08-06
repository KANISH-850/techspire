import React from 'react';
import { LayoutDashboard, MessageSquare, Pill, Calendar, FileText, History, Activity } from 'lucide-react';
import './App.css';

export default function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-icon">
          <Activity size={24} color="#003380" />
        </div>
        <h2 className="logo-text">HealthSync AI</h2>
      </div>

      <div className="user-profile-card">
        <img 
          src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex" 
          alt="Alex Johnson" 
          className="user-avatar" 
        />
        <div className="user-info">
          <div className="user-name">Alex Johnson</div>
          <div className="user-id">Patient ID: #8821</div>
        </div>
      </div>

      <div className="nav-section">
        <h3 className="section-title">MAIN</h3>
        <nav className="nav-menu">
          <a href="#" className="nav-item active">
            <MessageSquare size={18} />
            Messages
          </a>
        </nav>
      </div>

      <div className="nav-section">
        <h3 className="section-title">RECENT TOPICS</h3>
        <nav className="nav-menu recent-topics">
          <a href="#" className="nav-item small">
            <History size={16} />
            Migraine Symptoms
          </a>
          <a href="#" className="nav-item small">
            <History size={16} />
            Lisinopril Refill Request
          </a>
          <a href="#" className="nav-item small">
            <History size={16} />
            Lab Results: Blood Panel
          </a>
        </nav>
      </div>

      <div className="sidebar-footer">
        <button className="btn-primary w-full justify-center">
          <Calendar size={18} />
          Book Appointment
        </button>
      </div>
    </div>
  );
}
