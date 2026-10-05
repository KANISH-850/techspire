import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import chatbotApi from '../api/chatbot';
import { 
  Bot, Send, Plus, MessageSquare, Compass, Activity, 
  Sparkles, Shield, User, Paperclip
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function Chatbot() {
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);

  const [sessionId] = useState(() => {
    let sid = localStorage.getItem('anon_session_id');
    if (!sid) {
      sid = crypto.randomUUID();
      localStorage.setItem('anon_session_id', sid);
    }
    return sid;
  });

  const [conversationId, setConversationId] = useState(() => localStorage.getItem('anon_conversation_id') || null);
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const suggestions = [
    "Open CEO Dashboard",
    "Show patient Emily Chen's records",
    "Open Predictive Analytics",
    "Open AI Report Builder",
    "What medicine stock is low?"
  ];

  const fetchConversations = async () => {
    try {
      const data = await chatbotApi.getConversations(sessionId);
      setConversations(data || []);
    } catch (e) {
      console.error("Failed to fetch conversations", e);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, [sessionId]);

  useEffect(() => {
    const initConversation = async () => {
      try {
        if (conversationId) {
          const data = await chatbotApi.getConversationById(conversationId);
          if (data && data.messages && data.messages.length > 0) {
            setMessages(data.messages);
            return;
          }
        }

        const newConv = await chatbotApi.createConversation({
          title: 'New Consultation',
          status: 'active',
          session_id: sessionId
        });
        
        setConversationId(newConv.id);
        localStorage.setItem('anon_conversation_id', newConv.id);
        fetchConversations();

        setMessages([
          {
            id: 'system-1',
            role: 'assistant',
            content: "Hello! I am **TechSpire AI**, your unified hospital clinical & executive assistant. Ask me about patient records, bed occupancy, inventory alerts, or type *'Open Dashboard'*.",
            timestamp: new Date().toISOString()
          }
        ]);
      } catch (error) {
        console.error("Failed to initialize conversation", error);
        setMessages([
          {
            id: 'error-1',
            role: 'assistant',
            content: "⚠️ Unable to connect to hospital Chatbot engine. Ensure FastAPI backend is running.",
            timestamp: new Date().toISOString()
          }
        ]);
      }
    };

    initConversation();
  }, [conversationId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !conversationId) return;

    const userText = inputValue.trim();
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userText,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    const assistantMessageId = Date.now().toString() + "-ai";
    setMessages(prev => [...prev, {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      timestamp: new Date().toISOString()
    }]);

    try {
      await chatbotApi.streamChat(
        conversationId,
        userText,
        (chunk) => {
          setMessages(prev => 
            prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: msg.content + chunk } 
                : msg
            )
          );
        }
      );
      fetchConversations();
    } catch (error) {
      console.error("Failed to stream response", error);
      setMessages(prev => 
        prev.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, content: msg.content + "\n\n*(Connection interrupted or streaming timeout)*" } 
            : msg
        )
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    localStorage.removeItem('anon_conversation_id');
    setConversationId(null);
    setMessages([]);
  };

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
      case '/': 
      case '/dashboard': return 'CEO Executive AI Dashboard';
      case '/predictive':
      case '/predictive-analytics': return 'Predictive AI Analytics';
      case '/reports': return 'AI Report Builder';
      case '/procurement': return 'AI Procurement & Inventory';
      case '/patients': return 'Patients Registry';
      case '/appointments': return 'Appointments';
      case '/admissions': return 'Admissions';
      case '/beds': return 'Bed Management';
      default: return 'Module';
    }
  };

  return (
    <div className="flex h-[calc(100vh-7rem)] max-w-[1600px] mx-auto bg-[var(--ts-card-bg)] border border-[var(--ts-border)] rounded-2xl overflow-hidden shadow-2xl">
      {/* Sidebar - Saved Conversations */}
      <aside className="w-64 bg-[var(--ts-bg-subtle)] border-r border-[var(--ts-border)] flex flex-col justify-between p-4 shrink-0">
        <div className="space-y-4 flex-1 overflow-hidden flex flex-col">
          <button
            onClick={handleNewChat}
            className="w-full ts-btn-primary justify-center text-xs py-2.5 rounded-xl shadow-md"
          >
            <Plus className="w-4 h-4" /> New Consultation
          </button>

          <div className="flex-1 overflow-y-auto space-y-1 pr-1">
            <div className="px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-[var(--ts-text-muted)]">
              Consultation History
            </div>
            {conversations.map((c) => {
              const isActive = c.id === conversationId;
              return (
                <button
                  key={c.id}
                  onClick={() => {
                    setConversationId(c.id);
                    localStorage.setItem('anon_conversation_id', c.id);
                  }}
                  className={`w-full text-left px-3 py-2 rounded-xl text-xs flex items-center gap-2 transition-all ${
                    isActive
                      ? 'bg-cyan-500/20 text-cyan-400 font-bold border border-cyan-500/30'
                      : 'text-[var(--ts-text-secondary)] hover:bg-[var(--ts-card-hover)]'
                  }`}
                >
                  <MessageSquare className="w-3.5 h-3.5 shrink-0 text-cyan-400" />
                  <span className="truncate">{c.title || 'Consultation'}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="pt-3 border-t border-[var(--ts-border)] text-[10px] text-[var(--ts-text-muted)] flex items-center gap-2">
          <Shield className="w-3.5 h-3.5 text-cyan-400" />
          <span>LLM Engine: Qwen3:4B / ChromaDB RAG</span>
        </div>
      </aside>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col h-full bg-[var(--ts-bg)]">
        {/* Messages Feed */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            const navRoute = getNavRoute(msg.content);
            const cleanText = getCleanContent(msg.content);

            return (
              <div
                key={msg.id || idx}
                className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : ''}`}
              >
                <div className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold ${
                  isUser 
                    ? 'bg-gradient-to-tr from-cyan-500 to-blue-600 text-white' 
                    : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                }`}>
                  {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                <div className={`p-4 rounded-2xl text-xs leading-relaxed space-y-2 max-w-2xl ${
                  isUser
                    ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white font-medium rounded-tr-none'
                    : 'bg-[var(--ts-card-bg)] border border-[var(--ts-border)] text-[var(--ts-text-primary)] rounded-tl-none shadow-md'
                }`}>
                  <ReactMarkdown>{cleanText}</ReactMarkdown>

                  {navRoute && (
                    <div className="pt-2 border-t border-[var(--ts-border)]">
                      <button
                        onClick={() => navigate(navRoute)}
                        className="px-3.5 py-1.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold rounded-xl text-xs flex items-center gap-2 shadow-md hover:opacity-90 transition-opacity"
                      >
                        <Compass className="w-3.5 h-3.5" /> Navigate to {getModuleName(navRoute)} &rarr;
                      </button>
                    </div>
                  )}
                </div>
              </div>
            );
          })}

          {isLoading && (
            <div className="flex gap-3 max-w-3xl">
              <div className="w-8 h-8 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 animate-spin" />
              </div>
              <div className="p-4 rounded-2xl bg-[var(--ts-card-bg)] border border-[var(--ts-border)] text-xs text-[var(--ts-text-muted)] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" />
                <span>Thinking & Retrieving Context...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-[var(--ts-border)] bg-[var(--ts-bg-subtle)] space-y-3">
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            {suggestions.map((s, i) => (
              <button
                key={i}
                onClick={() => setInputValue(s)}
                className="px-3 py-1 bg-[var(--ts-card-bg)] border border-[var(--ts-border)] hover:border-cyan-500/50 rounded-full text-[11px] text-[var(--ts-text-secondary)] hover:text-cyan-400 transition-colors whitespace-nowrap"
              >
                {s}
              </button>
            ))}
          </div>

          <form onSubmit={handleSend} className="flex items-center gap-2">
            <input
              type="text"
              placeholder="Ask a clinical question, query patients, or type 'Open Dashboard'..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              disabled={isLoading || !conversationId}
              className="flex-1 bg-[var(--ts-card-bg)] border border-[var(--ts-border)] focus:border-cyan-500 text-xs text-[var(--ts-text-primary)] px-4 py-3 rounded-xl focus:outline-none transition-colors"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading || !conversationId}
              className="ts-btn-primary px-4 py-3 rounded-xl"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
