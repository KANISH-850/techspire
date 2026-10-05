import React, { useRef, useEffect } from 'react';
import { Paperclip, Send, Bot, Compass } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import './App.css';

export default function ChatArea({ 
  messages, 
  inputValue, 
  setInputValue, 
  handleSend, 
  isLoading, 
  conversationId 
}) {
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const suggestions = [
    "Open Dashboard",
    "Open Predictive Analytics",
    "Open Reports",
    "Open Procurement",
    "What is the status of patient Emily Chen?"
  ];

  // Helper to extract navigation route if present
  const getNavRoute = (content) => {
    if (!content) return null;
    const match = content.match(/\[NAVIGATE:(.*?)\]/);
    return match ? match[1] : null;
  };

  const getCleanContent = (content) => {
    if (!content) return '';
    return content.replace(/\[NAVIGATE:.*?\]/g, '').trim();
  };

  const getModuleName = (route) => {
    switch (route) {
      case '/': return 'CEO Executive AI Dashboard';
      case '/predictive-analytics': return 'Predictive AI Analytics';
      case '/reports': return 'AI Report Builder';
      case '/procurement': return 'AI Procurement & Inventory';
      case '/chatbot': return 'AI Chatbot';
      default: return 'Module';
    }
  };

  return (
    <div className="chat-area">
      <main className="message-list">
        {messages.length > 0 && (
          <div className="date-separator">
            <span>Today's Consultation Thread</span>
          </div>
        )}
        
        {messages.map((msg, idx) => {
          const navRoute = getNavRoute(msg.content);
          const cleanText = getCleanContent(msg.content);

          return (
            <div key={msg.id || idx} className={`message-wrapper ${msg.role === 'error' ? 'error' : msg.role}`}>
              {msg.role !== 'user' && (
                <div className="msg-avatar">
                  <Bot size={20} color="#0EA5E9" />
                </div>
              )}
              <div className="message-bubble flex flex-col gap-2">
                <ReactMarkdown>{cleanText}</ReactMarkdown>
                
                {navRoute && (
                  <div className="mt-2 pt-2 border-t border-slate-200">
                    <button
                      onClick={() => navigate(navRoute)}
                      className="px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold rounded-xl text-xs flex items-center gap-2 shadow-md hover:opacity-90 transition-opacity"
                    >
                      <Compass className="w-4 h-4" /> Open {getModuleName(navRoute)} &rarr;
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
        
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="msg-avatar">
              <Bot size={20} color="#0EA5E9" />
            </div>
            <div className="message-bubble">
              <div className="typing-indicator">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      <div className="input-container">
        <div className="suggestion-chips">
          {suggestions.map((s, i) => (
            <button 
              key={i} 
              className="chip"
              onClick={() => {
                setInputValue(s);
              }}
            >
              {s}
            </button>
          ))}
        </div>

        <form onSubmit={handleSend} className="input-form">
          <button type="button" className="icon-btn attachment-btn">
            <Paperclip size={20} />
          </button>
          
          <input
            type="text"
            className="chat-input"
            placeholder="Ask a medical question, patient query, or say 'Open Dashboard'..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            disabled={isLoading || !conversationId}
            autoFocus
          />
          
          <button 
            type="submit" 
            className="send-button"
            disabled={!inputValue.trim() || isLoading || !conversationId}
          >
            <Send size={20} />
          </button>
        </form>
        
        <div className="footer-disclaimer">
          HealthSync AI Assistant provides administrative & clinical information. For medical emergencies, contact emergency staff.
        </div>
      </div>
    </div>
  );
}
