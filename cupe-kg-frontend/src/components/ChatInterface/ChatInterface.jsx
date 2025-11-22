import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useMapContext } from '../../context/MapContext';
import { askChatbot } from '../../services/api';
import { translateText } from '../../utils/translationHelper';
import MessageGroup from './MessageGroup';
import './ChatInterface.css';
import './MessageGroup.css';

const ChatInterface = ({ isPanelOpen }) => {
  const { t, i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      text: t('chat.welcome'),
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
  const chatMessagesRef = useRef(null); // NEW: Direct reference to chat messages container
  const shouldScrollToBottom = useRef(true); // NEW: Control when to scroll
  
  const mapContext = useMapContext();
  const selectedLocation = mapContext?.selectedLocation;

  // Initialize session ID
  useEffect(() => {
    if (!sessionId) {
      setSessionId(Date.now().toString() + Math.random().toString(36));
    }
  }, [sessionId]);

  const suggestions = [
    t('chat.suggestions.hampi'),
    t('chat.suggestions.delhi'),
    t('chat.suggestions.buddhist'),
    t('chat.suggestions.konark'),
    t('chat.suggestions.tour')
  ];

  // IMPROVED: More reliable scroll to bottom function
  const scrollToBottom = useCallback(() => {
    if (!shouldScrollToBottom.current) return;
    
    // Multiple fallback methods to ensure scrolling works
    const scrollToEnd = () => {
      // Method 1: Use messagesEndRef if available
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'end',
          inline: 'nearest' 
        });
      }
      
      // Method 2: Direct scroll on chat container
      if (chatMessagesRef.current) {
        chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
      }
    };

    // Execute scroll after DOM update
    requestAnimationFrame(() => {
      setTimeout(scrollToEnd, 10); // Small delay for DOM rendering
    });
  }, []);

  // FIXED: Better scroll effect with proper dependencies
  useEffect(() => {
    // Only auto-scroll when messages change OR typing state changes
    scrollToBottom();
  }, [messages.length, isTyping, scrollToBottom]); // Changed from [messages] to [messages.length]

  // NEW: Scroll when chat opens
  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        shouldScrollToBottom.current = true;
        scrollToBottom();
      }, 300); // Wait for opening animation
    }
  }, [isOpen, scrollToBottom]);

  // Check if user is near bottom to decide whether to auto-scroll
  const handleScroll = useCallback(() => {
    if (chatMessagesRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = chatMessagesRef.current;
      const isNearBottom = scrollTop + clientHeight >= scrollHeight - 50; // 50px threshold
      shouldScrollToBottom.current = isNearBottom;
    }
  }, []);

  useEffect(() => {
    // Add contextual message when location changes
    if (selectedLocation && sessionId) {
      shouldScrollToBottom.current = true; // Always scroll for new contextual messages
      const locationMessage = {
        id: Date.now(),
        type: 'bot',
        text: `✨ I see you're exploring ${selectedLocation.name}! This ${selectedLocation.category} site has fascinating stories to tell. What would you like to know about it?`,
        timestamp: new Date(),
        confidence: 0.9,
        suggestions: [
          `Tell me about ${selectedLocation.name}'s history`,
          `What makes ${selectedLocation.name} special?`,
          "Show me nearby heritage sites",
          "Plan a visit to this location"
        ]
      };
      
      setMessages(prev => [...prev, locationMessage]);
    }
  }, [selectedLocation, sessionId]);

  const toggleChat = useCallback(() => {
    setIsOpen(!isOpen);
    if (!isOpen) {
      // When opening, ensure we scroll to bottom and focus input
      setTimeout(() => {
        shouldScrollToBottom.current = true;
        scrollToBottom();
        inputRef.current?.focus();
      }, 350);
    }
  }, [isOpen, scrollToBottom]);

  const handleInputChange = useCallback((e) => {
    setInputValue(e.target.value);
    
    // Auto-resize textarea
    if (e.target.scrollHeight <= 120) {
      e.target.style.height = 'auto';
      e.target.style.height = e.target.scrollHeight + 'px';
    }
  }, []);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim()) {
        sendMessage();
      }
    }
  }, [inputValue]);

  const handleSuggestionClick = useCallback((suggestion) => {
    shouldScrollToBottom.current = true; // Always scroll for suggestions
    setInputValue(suggestion);
    setShowSuggestions(false);
    
    // Auto-send suggestion or just populate input
    setTimeout(() => {
      sendMessage(suggestion);
    }, 100);
  }, []);

// ONLY CHANGE THIS SECTION IN YOUR EXISTING ChatInterface.jsx

  const sendMessage = useCallback(async (messageText = null) => {
    const textToSend = messageText || inputValue.trim();
    if (!textToSend) return;

    shouldScrollToBottom.current = true; // Always scroll for new user messages
    
    // Create user message
    const userMessage = {
      id: Date.now(),
      type: 'user', 
      text: textToSend,
      timestamp: new Date(),
      status: 'sending'
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    setShowSuggestions(false);

    // Reset textarea height
    if (inputRef.current) {
      inputRef.current.style.height = '40px';
    }

    try {
      // Update user message status
      setMessages(prev => 
        prev.map(msg => 
          msg.id === userMessage.id 
            ? { ...msg, status: 'delivered' }
            : msg
        )
      );

      // Get bot response
      const response = await askChatbot(textToSend, sessionId, selectedLocation);

      // Translate bot response if not in English
      let botText = response.answer || "I apologize, but I'm having trouble understanding that. Could you please rephrase your question about India's cultural heritage?";
      if (i18n.language !== 'en') {
        botText = await translateText(botText, i18n.language, 'en');
      }

      // FIXED: Use 'answer' instead of 'response' field
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: botText,
        timestamp: new Date(),
        confidence: response.confidence || 0.7,
        suggestions: response.followUpQuestions || []
      };

      setMessages(prev => [...prev, botMessage]);
      
    } catch (error) {
      console.error('Error getting chatbot response:', error);
      
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
      setIsTyping(false);
    }
  }, [inputValue, sessionId, selectedLocation]);

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
        
        {/* Messages Area - FIXED with proper ref and scroll handling */}
        <div 
          className="chat-messages" 
          ref={chatMessagesRef}
          onScroll={handleScroll}
        >
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
          
          {/* FIXED: Scroll anchor element */}
          <div 
            ref={messagesEndRef} 
            style={{ 
              height: '1px', 
              width: '100%', 
              paddingBottom: '8px' 
            }} 
          />
        </div>
        
        {/* Enhanced Glass Input Area */}
        <div className={`chat-input-container ${isTyping ? 'sending' : ''}`}>
          <textarea
            ref={inputRef}
            className="chat-input"
            placeholder={t('chat.placeholder')}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            rows="1"
            style={{ height: '40px' }}
            maxLength={500}
            aria-label="Chat input"
          />
          
          {/* Optional Character Counter */}
          {inputValue.length > 400 && (
            <div className="input-counter">
              {inputValue.length}/500
            </div>
          )}
          
          {/* Optional Voice Input Button (for future enhancement) 
          <button 
            className="voice-button"
            onClick={() => {}}
            aria-label="Voice input"
            style={{ display: 'none' }}
          >
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
              <path fill="currentColor" d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
            </svg>
          </button>
          */}
          
          {/* Enhanced Send Button */}
          <button 
            className="send-button" 
            onClick={() => sendMessage()}
            disabled={!inputValue.trim() || isTyping}
            aria-label={isTyping ? "Sending message..." : "Send message"}
          >
            {isTyping ? (
              // Loading spinner when sending
              <svg viewBox="0 0 24 24" width="20" height="20" className="spinner">
                <path fill="currentColor" d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z"/>
              </svg>
            ) : (
              // Send arrow icon
              <svg viewBox="0 0 24 24" width="20" height="20">
                <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;