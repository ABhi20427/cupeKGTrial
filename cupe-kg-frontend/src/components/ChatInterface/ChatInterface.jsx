import React, { useState, useEffect, useRef } from 'react';
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
      text: 'Hello! I\'m your CuPe-KG guide. Ask me anything about Indian heritage sites, historical periods, or travel routes.',
      timestamp: new Date(),
      status: 'delivered'
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
    "Tell me about the history of Hampi",
    "What is the best time to visit Delhi?", 
    "Show me the Buddhist trail route",
    "What dynasty built the Konark Sun Temple?",
    "Suggest a 7-day cultural tour"
  ];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add contextual message when location changes
    if (selectedLocation && sessionId) {
      const locationMessage = {
        id: Date.now(),
        type: 'bot',
        text: `I see you're exploring ${selectedLocation.name}. Would you like to know more about its history, cultural significance, or visiting information?`,
        timestamp: new Date(),
        suggestions: [
          `Tell me about ${selectedLocation.name}'s history`,
          `Best time to visit ${selectedLocation.name}`,
          `Cultural significance of ${selectedLocation.name}`,
          `How to reach ${selectedLocation.name}`
        ]
      };
      
      setMessages(prev => [...prev, locationMessage]);
      setShowSuggestions(false);
    }
  }, [selectedLocation, sessionId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      const timeoutId = setTimeout(() => {
        inputRef.current?.focus();
      }, 300);
      return () => clearTimeout(timeoutId);
    }
  };

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const sendMessage = async (text = inputValue) => {
    if (!text.trim() || !sessionId) return;
    
    // Add user message
    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: text,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setShowSuggestions(false);
    setIsTyping(true);
    
    try {
      // **REAL API CALL** - This connects to your backend!
      const response = await askChatbot(text, sessionId, selectedLocation?.id);
      
      // Create bot response message
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: response.answer,
        timestamp: new Date(),
        confidence: response.confidence,
        suggestions: response.followUpQuestions || []
      };
      
      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      console.error('Error getting chatbot response:', error);
      
      // Fallback response on error
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: "I'm sorry, I'm having trouble processing your request right now. Please try asking about a specific heritage site or historical period.",
        timestamp: new Date(),
        suggestions: suggestions.slice(0, 3)
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className={`chat-widget ${isPanelOpen ? 'panel-open' : ''}`}>
      <button className={`chat-toggle ${isOpen ? 'open' : ''}`} onClick={toggleChat}>
        {isOpen ? (
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/>
          </svg>
        )}
      </button>
      
      <div className={`chat-container ${isOpen ? 'open' : ''}`}>
        <div className="chat-header">
          <div className="chat-title">
            <svg viewBox="0 0 24 24" width="20" height="20" className="chat-icon">
              <path fill="currentColor" d="M12 1c-6.1 0-11 4.9-11 11s4.9 11 11 11 11-4.9 11-11-4.9-11-11-11zM12 21c-5 0-9-4-9-9s4-9 9-9 9 4 9 9-4 9-9 9zM12 7c-2.2 0-4 1.8-4 4s1.8 4 4 4 4-1.8 4-4-1.8-4-4-4zM12 13c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2z"/>
            </svg>
            <span>CuPe-KG Assistant</span>
          </div>
        </div>
        
        <div className="chat-messages">
          <MessageGroup
            messages={messages}
            onSuggestionClick={handleSuggestionClick}
          />
          
          {isTyping && (
            <div className="message bot-message typing">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          
          {showSuggestions && (
            <div className="initial-suggestions">
              <p>Here are some things you can ask:</p>
              <div className="suggestion-buttons">
                {suggestions.map((suggestion, index) => (
                  <button 
                    key={index}
                    className="suggestion-button"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-container">
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder="Ask about Indian heritage..."
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows="1"
          />
          <button 
            className="send-button" 
            onClick={() => sendMessage()}
            disabled={!inputValue.trim()}
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