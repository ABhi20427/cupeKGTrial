// Update your InfoPanel.jsx with this enhanced image handling

import React, { useState, useEffect } from 'react';
import './InfoPanel.css';

const InfoPanel = ({ isOpen, isLoading, locationData, selectedLocation, onClose, onOpen, onCulturalIntelligence }) => {
  const [activeTab, setActiveTab] = useState('history');
  const [isVisible, setIsVisible] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [imageSrc, setImageSrc] = useState('');
  const [animationClass, setAnimationClass] = useState('');

  // Enhanced image handling
  useEffect(() => {
    if (selectedLocation) {
      setImageLoaded(false);
      setImageError(false);
      
      // Try multiple image sources in order of preference
      const imagePaths = [
        `/assets/images/${selectedLocation.id}.jpg`,
        `/assets/images/${selectedLocation.id}.jpeg`,
        `/assets/images/${selectedLocation.name.toLowerCase().replace(/\s+/g, '-')}.jpg`,
        `/assets/images/placeholder.jpg`
      ];
      
      setImageSrc(imagePaths[0]); // Start with first option
    }
  }, [selectedLocation]);

  const handleImageError = () => {
    if (!imageError) {
      setImageError(true);
      
      // Try fallback images in order
      const fallbackPaths = [
        `/assets/images/${selectedLocation?.name.toLowerCase().replace(/\s+/g, '-')}.jpg`,
        `/assets/images/placeholder.jpg`,
        `/assets/images/default-heritage-site.jpg`,
        'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDQwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSI0MDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjZjVmNWY1Ii8+CjxwYXRoIGQ9Ik0xMDAgODBMMTUwIDEyMEwyMDAgODBMMzAwIDEyMFYxNjBIMTAwVjgwWiIgZmlsbD0iIzNmNTFiNSIvPgo8dGV4dCB4PSIyMDAiIHk9IjEwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzY2NiIgZm9udC1mYW1pbHk9InNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiPkhlcml0YWdlIFNpdGU8L3RleHQ+Cjwvc3ZnPg==' // SVG placeholder as last resort
      ];
      
      // Try next fallback
      if (fallbackPaths.length > 0) {
        setImageSrc(fallbackPaths[0]);
      }
    }
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
    setImageError(false);
  };

  // Sync visibility state with isOpen prop
  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      setTimeout(() => {
        setAnimationClass('animate-in');
      }, 50);
      onOpen?.();
    } else {
      setAnimationClass('animate-out');
      setTimeout(() => {
        setIsVisible(false);
        setAnimationClass('');
      }, 300);
    }
  }, [isOpen, onOpen]);

  // Reset to history tab when a new location is selected
  useEffect(() => {
    if (selectedLocation) {
      setActiveTab('history');
      onOpen?.();
    }
  }, [selectedLocation, onOpen]);

  if (!isVisible && !isOpen) {
    return null;
  }

  const handleTabChange = (tab) => {
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
                src={imageSrc}
                alt={selectedLocation.name}
                className={`location-image ${imageLoaded ? 'loaded' : ''} ${imageError ? 'error' : ''}`}
                onLoad={handleImageLoad}
                onError={handleImageError}
              />
              <div className="image-overlay"></div>
              {imageError && (
                <div className="image-error-overlay">
                  <div className="error-icon">🏛️</div>
                  <div className="error-text">Heritage Site</div>
                </div>
              )}
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