import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useMapContext } from '../../context/MapContext';
import { askChatbot } from '../../services/api';
import MessageGroup from './MessageGroup';
import './ChatInterface.css';
import './MessageGroup.css';

const ChatInterface = ({ isPanelOpen }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: '🙏 Namaste! I\'m your CuPe-KG cultural heritage guide. Discover India\'s rich history, explore magnificent monuments, and plan unforgettable heritage journeys.',
      timestamp: new Date(),
      status: 'delivered',
      confidence: 0.95
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  
  const mapContext = useMapContext();
  const selectedLocation = mapContext?.selectedLocation;

  // Initialize session ID
  useEffect(() => {
    if (!sessionId) {
      setSessionId(Date.now().toString() + Math.random().toString(36));
    }
  }, []);

  const suggestions = [
    "🏛️ Tell me about the history of Hampi",
    "🌅 What's the best time to visit Delhi?", 
    "🧘 Show me the Buddhist trail route",
    "🎨 What dynasty built the Konark Sun Temple?",
    "🗺️ Suggest a 7-day cultural heritage tour"
  ];

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      scrollToBottom();
    }, 100);
    
    return () => clearTimeout(timer);
  }, [messages, scrollToBottom]);

  useEffect(() => {
    // Add contextual message when location changes
    if (selectedLocation && sessionId) {
      const locationMessage = {
        id: Date.now(),
        type: 'bot',
        text: `✨ I see you're exploring ${selectedLocation.name}! This ${selectedLocation.category} site has fascinating stories to tell. What would you like to discover?`,
        timestamp: new Date(),
        confidence: 0.9,
        suggestions: [
          `📚 Tell me about ${selectedLocation.name}'s history`,
          `🕐 Best time to visit ${selectedLocation.name}`,
          `🎭 Cultural significance of ${selectedLocation.name}`,
          `🚗 How to reach ${selectedLocation.name}`
        ]
      };
      
      setMessages(prev => [...prev, locationMessage]);
      setShowSuggestions(false);
    }
  }, [selectedLocation, sessionId, scrollToBottom]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      const timeoutId = setTimeout(() => {
        inputRef.current?.focus();
      }, 400);
      return () => clearTimeout(timeoutId);
    }
  };

const handleInputChange = (e) => {
  const value = e.target.value;
  setInputValue(value);
  
  // Auto-resize textarea with bounds checking
  const textarea = e.target;
  textarea.style.height = '40px'; // Reset to minimum height
  const scrollHeight = Math.min(textarea.scrollHeight, 120);
  textarea.style.height = scrollHeight + 'px';
};

const handleKeyDown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (inputValue.trim()) {
      sendMessage();
    }
  }
};

const handleSuggestionClick = (suggestion) => {
  // Remove emoji from suggestion for cleaner input
  const cleanSuggestion = suggestion.replace(/^[^\w\s]+\s*/, '');
  setInputValue(cleanSuggestion);
  sendMessage(cleanSuggestion);
};

const sendMessage = async (text = inputValue) => {
  if (!text.trim() || !sessionId) return;
  
  // Add user message with enhanced styling
  const userMessage = {
    id: Date.now(),
    type: 'user',
    text: text,
    timestamp: new Date(),
    status: 'delivered'
  };
  
  // Clear input immediately and reset height
  setInputValue('');
  if (inputRef.current) {
    inputRef.current.style.height = '40px';
  }
  
  // Add user message to state
  setMessages(prev => [...prev, userMessage]);
  setShowSuggestions(false);
  setIsTyping(true);
  
  try {
    // Real API call to backend
    const response = await askChatbot(text, sessionId, selectedLocation?.id);
    
    // Create enhanced bot response
    const botMessage = {
      id: Date.now() + 1,
      type: 'bot',
      text: response.answer || "I'm sorry, I couldn't process your request.",
      timestamp: new Date(),
      confidence: response.confidence || 0.7,
      suggestions: response.followUpQuestions || []
    };
    
    // Add bot message to state
    setMessages(prev => [...prev, botMessage]);
    
  } catch (error) {
    console.error('Error getting chatbot response:', error);
    
    // Enhanced error message
    const errorMessage = {
      id: Date.now() + 1,
      type: 'bot',
      text: "🔄 I apologize, but I'm experiencing some technical difficulties. Please try asking about a specific heritage site or check your connection.",
      timestamp: new Date(),
      confidence: 0.3,
      suggestions: [
        "Tell me about the Taj Mahal",
        "What is the Golden Triangle route?",
        "Show me Buddhist heritage sites"
      ]
    };
    
    setMessages(prev => [...prev, errorMessage]);
  } finally {
    // Always reset typing state
    setIsTyping(false);
  }
};

  return (
    <div className={`chat-widget ${isPanelOpen ? 'panel-open' : ''}`}>
      {/* Glassmorphism Floating Action Button */}
      <button 
        className={`chat-toggle ${isOpen ? 'open' : ''}`} 
        onClick={toggleChat}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
          </svg>
        )}
      </button>
      
      {/* Glassmorphism Chat Container */}
      <div className={`chat-container ${isOpen ? 'open' : ''}`}>
        {/* Glass Header */}
        <div className="chat-header">
          <div className="chat-title">
            <svg viewBox="0 0 24 24" width="20" height="20" className="chat-icon">
              <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span>CuPe-KG Heritage Guide</span>
          </div>
        </div>
        
        {/* Messages Area */}
        <div className="chat-messages">
          <MessageGroup
            messages={messages}
            onSuggestionClick={handleSuggestionClick}
          />
          
          {/* Enhanced Typing Indicator */}
          {isTyping && (
            <div className="message bot-message typing">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          
          {/* Initial Suggestions with Glass Effect */}
          {showSuggestions && (
            <div className="initial-suggestions">
              <p>🌟 Explore India's incredible heritage with me:</p>
              <div className="suggestion-buttons">
                {suggestions.map((suggestion, index) => (
                  <button 
                    key={index}
                    className="suggestion-button"
                    onClick={() => handleSuggestionClick(suggestion)}
                    style={{ animationDelay: `${index * 0.1}s` }}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {/* Glass Input Area */}
        <div className="chat-input-container">
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder="Ask about India's heritage, monuments, or travel plans..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows="1"
            style={{ height: '40px' }}
          />
          <button 
            className="send-button" 
            onClick={() => sendMessage()}
            disabled={!inputValue.trim()}
            aria-label="Send message"
          >
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;