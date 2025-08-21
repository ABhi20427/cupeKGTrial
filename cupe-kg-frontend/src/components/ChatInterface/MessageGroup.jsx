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

  return (
    <div className="message-group">
      {messages.map((message) => (
        <div key={message.id} className={`message ${message.type}-message`}>
          <div className="message-content">
            <p>{message.text}</p>
            
            {/* Show confidence for bot messages if available */}
            {message.type === 'bot' && message.confidence && (
              <div className="message-confidence">
                <span className={`confidence-indicator ${
                  message.confidence > 0.7 ? 'high' : 
                  message.confidence > 0.4 ? 'medium' : 'low'
                }`}>
                  {message.confidence > 0.7 ? '●' : message.confidence > 0.4 ? '◐' : '○'}
                </span>
              </div>
            )}
          </div>
          
          <div className="message-timestamp">
            {formatTimestamp(message.timestamp)}
          </div>
          
          {/* Dynamic suggestions for bot messages */}
          {message.type === 'bot' && message.suggestions && message.suggestions.length > 0 && (
            <div className="message-suggestions">
              {message.suggestions.map((suggestion, index) => (
                <button 
                  key={index}
                  className="suggestion-button"
                  onClick={() => onSuggestionClick(suggestion)}
                >
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