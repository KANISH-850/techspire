import React, { useRef, useEffect } from 'react';
import { Paperclip, Send, Bot } from 'lucide-react';
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

  const suggestions = [
    "Book Appointment",
    "Ask about symptoms",
    "Refill Prescription",
    "View Lab Results"
  ];

  return (
    <div className="chat-area">
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
                <Bot size={20} color="#0EA5E9" />
              </div>
            )}
            <div className="message-bubble">
              <ReactMarkdown>{msg.content}</ReactMarkdown>
            </div>
          </div>
        ))}
        
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
