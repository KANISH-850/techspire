import React, { useState, useEffect } from 'react';
import Sidebar from './Sidebar';
import ChatArea from './ChatArea';
import './App.css';

const API_BASE_URL = 'http://localhost:8000/api/v1';
const MOCK_USER_ID = "user-demo-123";

function App() {
  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const initAuthAndConversation = async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 3000);
        
        const res = await fetch(`${API_BASE_URL}/chatbot/conversations`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ title: 'New Consultation', status: 'active' }),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!res.ok) throw new Error('Failed to create conversation');
        const data = await res.json();
        setConversationId(data.id);
        
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
    initAuthAndConversation();
  }, []);

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

      if (!res.ok) throw new Error('Network response was not ok');
      
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

  return (
    <div className="app-layout">
      <Sidebar />
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

export default App;
