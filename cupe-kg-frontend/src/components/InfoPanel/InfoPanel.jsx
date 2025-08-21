import React, { useState, useEffect } from 'react';
import './InfoPanel.css';

const InfoPanel = ({ isOpen, isLoading, locationData, selectedLocation, onClose, onOpen, onCulturalIntelligence }) => {
  const [activeTab, setActiveTab] = useState('history');
  const [isVisible, setIsVisible] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [animationClass, setAnimationClass] = useState('');

  // Sync visibility state with isOpen prop
  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      // Add a small delay to trigger animation after component is mounted
      setTimeout(() => {
        setAnimationClass('animate-in');
      }, 50);
      onOpen?.(); // <-- Ensure callback is triggered when panel opens
    } else {
      // Set exit animation
      setAnimationClass('animate-out');
      // Delay hiding to allow for exit animation
      setTimeout(() => {
        setIsVisible(false);
        setAnimationClass('');
      }, 300);
    }
  }, [isOpen, onOpen]);

  // Reset image loaded state when location changes
  useEffect(() => {
    setImageLoaded(false);
  }, [selectedLocation]);

  // Reset to history tab when a new location is selected
  useEffect(() => {
    if (selectedLocation) {
      setActiveTab('history');
      onOpen?.();  // <-- ADD THIS when panel opens
    }
  }, [selectedLocation, onOpen]);

  if (!isVisible && !isOpen) {
    return null;
  }

  const handleTabChange = (tab) => {
    // Add tab change animation
    setAnimationClass('tab-change');
    setTimeout(() => {
      setActiveTab(tab);
      setAnimationClass('animate-in');
    }, 150);
  };

  const renderTabContent = () => {
    if (isLoading) {
      return (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading information...</p>
        </div>
      );
    }

    if (!locationData) {
      return null;
    }

    switch (activeTab) {
      case 'history':
        return (
          <div className={`tab-content ${animationClass}`}>
            <h3>Historical Significance</h3>
            <p>{locationData.history}</p>
            <div className="time-period">
              <h4>Time Period</h4>
              <div className="time-period-info">
                <span className="period">{locationData.period}</span>
                <span className="dynasty">{locationData.dynasty}</span>
              </div>
            </div>
          </div>
        );
      case 'culture':
        return (
          <div className={`tab-content ${animationClass}`}>
            <h3>Cultural Facts</h3>
            <ul className="culture-facts">
              {locationData.culturalFacts.map((fact, index) => (
                <li key={index} className={`stagger-delay-${index % 5 + 1}`}>{fact}</li>
              ))}
            </ul>
          </div>
        );
      case 'stories':
        return (
          <div className={`tab-content ${animationClass}`}>
            <h3>Legends & Stories</h3>
            <div className="story-container">
              {locationData.legends.map((legend, index) => (
                <div className={`story stagger-delay-${index + 1}`} key={index}>
                  <h4>{legend.title}</h4>
                  <p>{legend.description}</p>
                </div>
              ))}
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  const panelClasses = `info-panel ${isOpen ? 'open' : ''} ${animationClass}`;

  return (
    <div className={panelClasses} aria-hidden={!isOpen}>
      <div className="panel-header">
        {selectedLocation && (
          <>
            <div className="location-image-container">
              <img
                src={`/assets/images/${selectedLocation.id}.jpg`}
                alt={selectedLocation.name}
                className={`location-image ${imageLoaded ? 'loaded' : ''}`}
                onLoad={() => setImageLoaded(true)}
              />
              <div className="image-overlay"></div>
            </div>
            <h2 className="location-title">{selectedLocation.name}</h2>
          </>
        )}
        <button 
          className="close-button" 
          onClick={onClose}
          aria-label="Close information panel"
        >
          <span>×</span>
        </button>
      </div>

      <div className="panel-tabs">
        <button 
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => handleTabChange('history')}
          aria-pressed={activeTab === 'history'}
        >
          History
        </button>
        <button 
          className={`tab-button ${activeTab === 'culture' ? 'active' : ''}`}
          onClick={() => handleTabChange('culture')}
          aria-pressed={activeTab === 'culture'}
        >
          Culture
        </button>
        <button 
          className={`tab-button ${activeTab === 'stories' ? 'active' : ''}`}
          onClick={() => handleTabChange('stories')}
          aria-pressed={activeTab === 'stories'}
        >
          Stories
        </button>
      </div>

      <div className="panel-content">
        {renderTabContent()}
      </div>

      {locationData && (
        <div className="panel-footer">
          <div className="tags">
            {locationData.tags.map((tag, index) => (
              <span key={index} className="tag">{tag}</span>
            ))}
          </div>
          <div className="footer-buttons">
            <button className="explore-more-btn">
              Explore More
            </button>
            <button 
              className="ci-trigger-btn" 
              onClick={() => onCulturalIntelligence && onCulturalIntelligence()}
              title="Open Cultural Intelligence Analysis"
            >
              🧠 Cultural AI
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfoPanel;