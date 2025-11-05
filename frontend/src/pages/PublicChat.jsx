import React, { useState, useEffect, useRef } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { Send, Bot, User, Star } from 'lucide-react';
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL || ''
});
import { toast } from 'sonner';

const PublicChat = () => {
  const { chatbotId } = useParams();
  const [searchParams] = useSearchParams();
  const [chatbot, setChatbot] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [sessionId] = useState(() => `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`);
  const [conversationId, setConversationId] = useState(null);
  const [showRating, setShowRating] = useState(false);
  const [rating, setRating] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    loadChatbot();
  }, [chatbotId, searchParams.get('t')]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadChatbot = async () => {
    try {
      const response = await api.get(`/api/public/chatbot/${chatbotId}`);
      setChatbot(response.data);
      
      // Add welcome message
      setMessages([{
        role: 'assistant',
        content: response.data.welcome_message,
        timestamp: new Date()
      }]);
      
      // Notify parent iframe that loading is complete
      if (window.parent !== window) {
        window.parent.postMessage({ type: 'chatbot-loaded' }, '*');
      }
    } catch (error) {
      console.error('Error loading chatbot:', error);
      
      // Notify parent iframe of error
      if (window.parent !== window) {
        window.parent.postMessage({ 
          type: 'chatbot-error',
          error: error.response?.data?.detail || 'Failed to load chatbot'
        }, '*');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() || sending) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setSending(true);

    // Add user message to UI
    setMessages(prev => [...prev, {
      role: 'user',
      content: userMessage,
      timestamp: new Date()
    }]);

    try {
      const response = await api.post(`/api/public/chat/${chatbotId}`, {
        message: userMessage,
        session_id: sessionId
      });

      // Set conversation ID for rating
      if (!conversationId) {
        setConversationId(response.data.conversation_id);
      }

      // Add AI response to UI
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.data.message,
        timestamp: new Date()
      }]);

      // Show rating after 3 messages
      if (messages.filter(m => m.role === 'user').length >= 2) {
        setShowRating(true);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      console.error('Error details:', error.response?.data || error.message);
      
      // Add error message to chat
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        isError: true
      }]);
      
      toast.error(error.response?.data?.detail || 'Failed to send message');
    } finally {
      setSending(false);
    }
  };

  const handleRating = async (value) => {
    if (!conversationId) return;
    
    setRating(value);
    try {
      await api.post(`/api/analytics/rate/${conversationId}`, {
        rating: value
      });
      toast.success('Thank you for your feedback!');
      setTimeout(() => setShowRating(false), 2000);
    } catch (error) {
      console.error('Error submitting rating:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (!chatbot) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Chatbot Not Found</h2>
          <p className="text-gray-600">This chatbot is not publicly accessible or does not exist.</p>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="min-h-screen flex flex-col"
      style={{
        background: chatbot.widget_theme === 'dark' 
          ? 'linear-gradient(to bottom right, #1a1a2e, #16213e, #0f3460)'
          : 'linear-gradient(to bottom right, #faf5ff, #fce7f3, #e0e7ff)'
      }}
    >
      {/* Header */}
      <div 
        className="p-6 border-b shadow-md"
        style={{
          backgroundColor: chatbot.primary_color,
          color: 'white'
        }}
      >
        <div className="max-w-4xl mx-auto flex items-center space-x-4">
          {chatbot.logo_url ? (
            <img src={chatbot.logo_url} alt="Logo" className="h-10 w-10 rounded-full object-cover flex-shrink-0" />
          ) : (
            <Bot className="w-8 h-8 flex-shrink-0" />
          )}
          <div className="flex-1 min-w-0">
            <h1 className="text-2xl font-bold truncate">{chatbot.name}</h1>
            <p className="text-sm opacity-90">AI-Powered Assistant</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex items-start space-x-3 ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              {message.role === 'assistant' && (
                <div 
                  className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: chatbot.secondary_color }}
                >
                  {chatbot.avatar_url ? (
                    <img src={chatbot.avatar_url} alt="Bot" className="w-full h-full rounded-full object-cover" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>
              )}
              
              <div
                className={`max-w-xs md:max-w-2xl rounded-2xl p-4 shadow-md ${
                  message.role === 'user'
                    ? 'text-white'
                    : chatbot.widget_theme === 'dark'
                    ? 'bg-gray-800 text-white'
                    : 'bg-white text-gray-800'
                }`}
                style={
                  message.role === 'user'
                    ? { backgroundColor: chatbot.primary_color }
                    : {}
                }
              >
                <p className="whitespace-pre-wrap break-words text-sm">{message.content}</p>
              </div>

              {message.role === 'user' && (
                <div 
                  className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0"
                  style={{ backgroundColor: chatbot.secondary_color }}
                >
                  <User className="w-5 h-5 text-white" />
                </div>
              )}
            </div>
          ))}
          
          {sending && (
            <div className="flex items-start space-x-3">
              <div 
                className="w-8 h-8 rounded-full flex items-center justify-center"
                style={{ backgroundColor: chatbot.secondary_color }}
              >
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div className={`rounded-2xl p-4 ${
                chatbot.widget_theme === 'dark' ? 'bg-gray-800' : 'bg-white'
              }`}>
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Rating Widget */}
      {showRating && !rating && (
        <div className="max-w-4xl mx-auto px-4 mb-4">
          <div className="bg-white rounded-xl p-4 shadow-lg border-2 border-purple-200">
            <p className="text-sm text-gray-700 mb-2 text-center">How was your experience?</p>
            <div className="flex justify-center space-x-2">
              {[1, 2, 3, 4, 5].map((value) => (
                <button
                  key={value}
                  onClick={() => handleRating(value)}
                  className="p-1 hover:scale-110 transition-transform"
                >
                  <Star 
                    className="w-6 h-6 text-yellow-400 hover:fill-yellow-400"
                    fill="none"
                  />
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t bg-white/80 backdrop-blur-sm p-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSendMessage} className="flex items-center space-x-2">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-purple-500"
              disabled={sending}
            />
            <button
              type="submit"
              disabled={sending || !inputMessage.trim()}
              className="p-3 rounded-full text-white disabled:opacity-50 transition-all hover:scale-105"
              style={{ backgroundColor: chatbot.primary_color }}
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          
          {/* Branding Footer */}
          <div className="mt-3 text-center">
            <a 
              href="https://botsmith.ai" 
              target="_blank" 
              rel="noopener noreferrer" 
              className="inline-flex items-center gap-1 text-xs text-gray-400 hover:text-purple-600 transition-colors"
            >
              <span>Powered by</span>
              <span className="font-semibold" style={{ color: chatbot.primary_color }}>BotSmith</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PublicChat;
