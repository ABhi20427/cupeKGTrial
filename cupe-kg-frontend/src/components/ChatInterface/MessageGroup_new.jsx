import React from 'react';
import './MessageGroup.css';

const MessageGroup = ({ messages, onSuggestionClick }) => {
  const formatTimestamp = (timestamp) => {
    const now = new Date();
    const messageTime = new Date(timestamp);
    const diffInMinutes = Math.floor((now - messageTime) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    
    return messageTime.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getConfidenceLevel = (confidence) => {
    if (confidence > 0.7) return 'high';
    if (confidence > 0.4) return 'medium';
    return 'low';
  };

  const getConfidenceIcon = (confidence) => {
    if (confidence > 0.7) return '●';
    if (confidence > 0.4) return '◐';
    return '○';
  };

  return (
    <div className="message-group">
      {messages.map((message, index) => (
        <div 
          key={message.id} 
          className={`message ${message.type}-message ${
            message.confidence && getConfidenceLevel(message.confidence) === 'high' ? 'high-confidence' : ''
          }`}
          style={{ 
            animationDelay: `${index * 0.1}s`,
            '--message-index': index 
          }}
        >
          <div className="message-content">
            <p>{message.text}</p>
            
            {/* Enhanced Confidence Indicator */}
            {message.type === 'bot' && message.confidence && (
              <div className="message-confidence">
                <span className={`confidence-indicator ${getConfidenceLevel(message.confidence)}`}>
                  {getConfidenceIcon(message.confidence)}
                </span>
                <span className="confidence-text">
                  {Math.round(message.confidence * 100)}%
                </span>
              </div>
            )}
          </div>
          
          {/* Elegant Timestamp */}
          <div className="message-timestamp">
            {formatTimestamp(message.timestamp)}
            {message.type === 'user' && (
              <span className="message-status">
                {message.status === 'delivered' ? '✓' : '⏳'}
              </span>
            )}
          </div>
          
          {/* Dynamic Floating Suggestions */}
          {message.type === 'bot' && message.suggestions && message.suggestions.length > 0 && (
            <div className="message-suggestions">
              {message.suggestions.map((suggestion, suggestionIndex) => (
                <button 
                  key={suggestionIndex}
                  className="suggestion-button"
                  onClick={() => onSuggestionClick(suggestion)}
                  style={{ 
                    animationDelay: `${(index * 0.1) + (suggestionIndex * 0.05)}s` 
                  }}
                >
                  <span className="suggestion-icon">💫</span>
                  {suggestion}
                </button>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageGroup;