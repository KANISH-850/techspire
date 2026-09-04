import React from 'react';
import { LayoutDashboard, MessageSquare, Pill, Calendar, FileText, History, Activity, Plus } from 'lucide-react';
import './App.css';

export default function Sidebar({ onNewChat, conversations = [], activeConversationId, onSelectConversation }) {
  // Group conversations
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);

  const grouped = {
    today: [],
    yesterday: [],
    older: []
  };

  conversations.forEach(conv => {
    const convDate = new Date(conv.updated_at);
    convDate.setHours(0, 0, 0, 0);
    
    if (convDate.getTime() === today.getTime()) {
      grouped.today.push(conv);
    } else if (convDate.getTime() === yesterday.getTime()) {
      grouped.yesterday.push(conv);
    } else {
      grouped.older.push(conv);
    }
  });

  const renderGroup = (title, group) => {
    if (group.length === 0) return null;
    return (
      <div className="nav-section" key={title}>
        <h3 className="section-title">{title}</h3>
        <nav className="nav-menu recent-topics">
          {group.map(conv => (
            <a 
              key={conv.id} 
              href="#" 
              className={`nav-item small ${activeConversationId === conv.id ? 'active' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                onSelectConversation?.(conv.id);
              }}
            >
              <History size={16} />
              {conv.title || 'New Consultation'}
            </a>
          ))}
        </nav>
      </div>
    );
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo-icon">
          <Activity size={24} color="white" />
        </div>
        <h2 className="logo-text">HealthSync AI</h2>
      </div>

      <div className="user-profile-card">
        <img 
          src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex" 
          alt="Anonymous User" 
          className="user-avatar" 
        />
        <div className="user-info">
          <div className="user-name">Guest User</div>
          <div className="user-id">Status: Anonymous</div>
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
        
        <button 
          className="btn-primary w-full justify-center" 
          style={{ marginTop: '16px' }}
          onClick={(e) => { e.preventDefault(); onNewChat?.(); }}
        >
          <Plus size={18} />
          New Chat
        </button>
      </div>

      <div className="sidebar-history-container">
        {renderGroup('TODAY', grouped.today)}
        {renderGroup('YESTERDAY', grouped.yesterday)}
        {renderGroup('OLDER', grouped.older)}
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
