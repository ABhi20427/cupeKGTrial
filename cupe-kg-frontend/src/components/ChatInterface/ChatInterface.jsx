import React, { useState, useEffect, useRef } from 'react';
import { useMapContext } from '../../context/MapContext';
import MessageGroup from './MessageGroup';
import './ChatInterface.css';
import './MessageGroup.css';

const ChatInterface = () => {
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
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  
  const mapContext = useMapContext();
  const selectedLocation = mapContext?.selectedLocation;
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  useEffect(() => {
    // Check if either location or route is selected
    const panelShouldBeOpen = Boolean(selectedLocation || mapContext?.selectedRoute);
    // Add a small delay to match the panel animation
    let timeoutId;
    if (panelShouldBeOpen) {
      timeoutId = setTimeout(() => setIsPanelOpen(true), 50);
    } else {
      timeoutId = setTimeout(() => setIsPanelOpen(false), 300);
    }
    // Cleanup timeout on unmount or when dependencies change
    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [selectedLocation, mapContext?.selectedRoute]);

  const suggestions = [
    "Tell me about the history of Hampi",
    "What is the best time to visit Delhi?",
    "Show me the Buddhist trail route",
    "What dynasty built the Konark Sun Temple?",
    "Suggest a 7-day cultural tour"
  ];

  useEffect(() => {
    // Scroll to bottom when messages change
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add a context-aware message when location changes
    if (selectedLocation) {
      const locationMessage = {
        id: Date.now(),
        type: 'bot',
        text: `I see you're exploring ${selectedLocation.name}. Would you like to know more about its history or cultural significance?`,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, locationMessage]);
      setShowSuggestions(false);
    }
  }, [selectedLocation]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    // Focus input when opening
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

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const sendMessage = async (text = inputValue) => {
    if (!text.trim()) return;
    
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
      // This would be an actual API call in production
      // For now, simulate a response
      // const response = await fetch('/api/chatbot/ask', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ question: text, locationId: selectedLocation?.id })
      // });
      // const data = await response.json();
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Simulated responses
      let responseText = '';
      let followUpSuggestions = [];
      
      if (text.toLowerCase().includes('hampi')) {
        responseText = "Hampi was the capital of the Vijayanagara Empire (1336-1646 CE), once one of the richest cities in the world. The ruins showcase stunning temple architecture, with highlights including the Virupaksha Temple and stone chariot at Vittala Temple. UNESCO recognized it as a World Heritage site due to its historical and architectural significance.";
        followUpSuggestions = ["How do I reach Hampi?", "Best time to visit Hampi", "What are the must-see spots in Hampi?"];
      } 
      else if (text.toLowerCase().includes('delhi')) {
        responseText = "Delhi has been continuously inhabited since the 6th century BCE and served as a capital for numerous empires. It hosts three UNESCO World Heritage sites: Qutub Minar, Red Fort, and Humayun's Tomb. The city's culture blends multiple influences including Persian, Turkish, and indigenous Indian traditions, reflecting its complex history.";
        followUpSuggestions = ["What are Delhi's top monuments?", "Best season to visit Delhi", "Tell me about Delhi's cuisine"];
      }
      else if (text.toLowerCase().includes('buddhist') || text.toLowerCase().includes('trail') || text.toLowerCase().includes('route')) {
        responseText = "The Buddhist Trail connects key sites of Buddhist heritage across northern India. Major stops include Bodh Gaya (where Buddha attained enlightenment), Sarnath (where he gave his first sermon), and Kushinagar (where he attained parinirvana). The route offers spiritual significance and architectural marvels spanning over 2,500 years of history.";
        followUpSuggestions = ["How many days for the Buddhist trail?", "Best season for this route", "Most important sites on this route"];
      }
      else {
        responseText = "I'd be happy to help you explore India's rich cultural heritage. You can ask about specific historical sites like Hampi or Delhi, learn about different historical periods and dynasties, or explore themed routes like the Buddhist Trail, Temple Route, or Mughal Architecture tour.";
        followUpSuggestions = suggestions;
      }
      
      // Add bot response
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: responseText,
        timestamp: new Date(),
        suggestions: followUpSuggestions
      };
      
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
      
    } catch (error) {
      console.error("Error sending message:", error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        text: "I'm sorry, I couldn't process your request. Please try again later.",
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={`chat-wrapper${isPanelOpen ? ' panel-open' : ''}`}>
      <button 
        className={`chat-toggle ${isOpen ? 'open' : ''}`} 
        onClick={toggleChat}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
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