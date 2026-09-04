import React, { useState, useEffect } from 'react';
import ChatArea from '../ChatArea';
import Sidebar from '../Sidebar';
import '../App.css';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Main Chat Interface
function Chatbot() {
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

  const fetchConversations = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/chatbot/conversations?session_id=${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setConversations(data);
      }
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
          // Fetch existing conversation
          const res = await fetch(`${API_BASE_URL}/chatbot/conversations/${conversationId}`);
          if (res.ok) {
            const data = await res.json();
            if (data.messages && data.messages.length > 0) {
              setMessages(data.messages);
            } else {
              setMessages([{
                id: 'system-1',
                role: 'assistant',
                content: "Good morning! I'm your HealthSync AI assistant. How can I help you manage your health today?",
                timestamp: new Date().toISOString()
              }]);
            }
            return;
          }
          // If not found, fall through to create a new one
        }

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);
        
        const res = await fetch(`${API_BASE_URL}/chatbot/conversations`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ title: 'New Consultation', status: 'active', session_id: sessionId }),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!res.ok) {
          throw new Error('Failed to create conversation');
        }
        
        const data = await res.json();
        setConversationId(data.id);
        localStorage.setItem('anon_conversation_id', data.id);
        fetchConversations(); // refresh list
        
        setMessages([
          {
            id: 'system-1',
            role: 'assistant',
            content: "Good morning! I'm your HealthSync AI assistant. How can I help you manage your health today?",
            timestamp: new Date().toISOString()
          }
        ]);
      } catch (error) {
        console.error("Failed to initialize conversation", error);
        setConversationId('fallback-offline-id'); 
        setMessages([
          {
            id: 'error-1',
            role: 'error',
            content: 'Unable to connect to the hospital backend. Ensure backend is running.',
            timestamp: new Date().toISOString()
          }
        ]);
      }
    };
    
    initConversation();
  }, [conversationId]); // If conversationId gets cleared, it will create a new one

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading || !conversationId) return;

    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 seconds for AI stream

      const res = await fetch(`${API_BASE_URL}/chatbot/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: userMessage.content
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!res.ok) {
        throw new Error('Network response was not ok');
      }
      
      // Handle the streaming response
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let done = false;
      
      const assistantMessageId = Date.now().toString() + "-ai";
      setMessages(prev => [...prev, {
        id: assistantMessageId,
        role: 'assistant',
        content: '',
        timestamp: new Date().toISOString()
      }]);

      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          setMessages(prev => 
            prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: msg.content + chunk } 
                : msg
            )
          );
        }
      }
      
      fetchConversations(); // Update list in case title was updated

    } catch (error) {
      console.error("Failed to send message", error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'error',
        content: "Sorry, I'm having trouble connecting to the server. Or AI quota exceeded.",
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };
  const handleNewChat = () => {
    localStorage.removeItem('anon_conversation_id');
    setConversationId(null);
    setMessages([]);
  };

  const handleSelectConversation = (id) => {
    setConversationId(id);
    localStorage.setItem('anon_conversation_id', id);
  };

  return (
    <div className="app-layout">
      <Sidebar 
        onNewChat={handleNewChat} 
        conversations={conversations} 
        activeConversationId={conversationId}
        onSelectConversation={handleSelectConversation}
      />
      <ChatArea 
        messages={messages}
        inputValue={inputValue}
        setInputValue={setInputValue}
        handleSend={handleSend}
        isLoading={isLoading}
        conversationId={conversationId}
      />
    </div>
  );
}

export default Chatbot;
