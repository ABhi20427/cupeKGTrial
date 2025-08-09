import React from 'react';
import { format } from 'date-fns';
import './MessageGroup.css';

const MessageGroup = ({ messages, handleSuggestionClick }) => {
  const formatTime = (date) => {
    return format(new Date(date), 'h:mm a');
  };

  return (
    <div className="message-groups">
      {messages.map((message) => (
        <div 
          key={message.id}
          className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
        >
          <div className="message-content">
            <p>{message.text}</p>
            {message.suggestions && message.suggestions.length > 0 && (
              <div className="message-suggestions">
                {message.suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    className="suggestion-button"
                    onClick={() => handleSuggestionClick(suggestion)}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>
          <div className="message-timestamp">
            {formatTime(message.timestamp)}
          </div>
        </div>
      ))}
    </div>
  );
};

export default MessageGroup;
