import apiClient, { fetchStream } from './client';

export const chatbotApi = {
  getConversations: async (sessionId) => {
    const response = await apiClient.get('/chatbot/conversations', {
      params: { session_id: sessionId }
    });
    return response.data;
  },
  getConversationById: async (id) => {
    const response = await apiClient.get(`/chatbot/conversations/${id}`);
    return response.data;
  },
  createConversation: async (data) => {
    const response = await apiClient.post('/chatbot/conversations', data);
    return response.data;
  },
  streamChat: async (conversationId, message, onChunk, signal) => {
    return await fetchStream(
      '/chatbot/chat/stream',
      { conversation_id: conversationId, message },
      onChunk,
      signal
    );
  }
};

export default chatbotApi;
