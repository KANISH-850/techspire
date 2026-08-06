import React, { useRef, useEffect } from 'react';
import { Search, MoreVertical, Paperclip, Send, Bot } from 'lucide-react';
import './App.css';

import ReactMarkdown from 'react-markdown';

export default function ChatArea({ 
  messages, 
  inputValue, 
  setInputValue, 
  handleSend, 
  isLoading, 
  conversationId 
}) {
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const formatTime = (isoString) => {
    try {
      return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch(e) {
      return '';
    }
  };

  const suggestions = [
    "Book Appointment",
    "Ask about symptoms",
    "Refill Prescription",
    "View Lab Results"
  ];

  return (
    <div className="chat-area">
      <header className="chat-header">
        <div className="bot-avatar">
          <Bot size={24} color="#003380" />
        </div>
        <div className="header-info">
          <h1>MediChat Assistant</h1>
          <div className="status">
            <div className="status-dot"></div>
            Online and ready to help
          </div>
        </div>
        <div className="header-actions">
          <button className="icon-btn"><Search size={20} /></button>
          <button className="icon-btn"><MoreVertical size={20} /></button>
        </div>
      </header>

      <main className="message-list">
        {messages.length > 0 && (
          <div className="date-separator">
            <span>Today, 9:41 AM</span>
          </div>
        )}
        
        {messages.map((msg, idx) => (
          <div key={msg.id || idx} className={`message-wrapper ${msg.role === 'error' ? 'error' : msg.role}`}>
            {msg.role !== 'user' && (
              <div className="msg-avatar">
                <Bot size={16} color="#003380" />
              </div>
            )}
            <div className="message-bubble">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
            {/* The screenshot doesn't show timestamps on every bubble, but we can keep them hidden or minimal if desired. For now, removing to match screenshot exactly. */}
          </div>
        ))}
        
        {isLoading && (
          <div className="message-wrapper assistant">
            <div className="msg-avatar">
              <Bot size={16} color="#003380" />
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
            placeholder="Type your message here..."
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
          MediChat provides information, not medical advice. For emergencies, dial 911.
        </div>
      </div>
    </div>
  );
}
