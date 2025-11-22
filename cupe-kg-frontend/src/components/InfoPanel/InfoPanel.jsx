// Update your InfoPanel.jsx with this enhanced image handling

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useTranslatedText } from '../../utils/translationHelper';
import { useMapContext } from '../../context/MapContext';
import './InfoPanel.css';

// Helper component to translate text items
const TranslatedText = ({ text }) => {
  const { translatedText } = useTranslatedText(text || '');
  return <>{translatedText}</>;
};

const InfoPanel = ({ onClose, onOpen, onCulturalIntelligence, onExploreRoute }) => {
  // Get data from MapContext
  const { selectedLocation, locationData, isLoading, clearSelections } = useMapContext();
  const isOpen = !!selectedLocation;
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState('history');
  const [isVisible, setIsVisible] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [imageSrc, setImageSrc] = useState('');
  const [animationClass, setAnimationClass] = useState('');

  // Translate location data fields
  const { translatedText: translatedName } = useTranslatedText(selectedLocation?.name || '');
  const { translatedText: translatedHistory } = useTranslatedText(locationData?.history || '');
  const { translatedText: translatedPeriod } = useTranslatedText(locationData?.period || '');
  const { translatedText: translatedDynasty } = useTranslatedText(locationData?.dynasty || '');

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

  const handleClose = (e) => {
    console.log('Close button clicked!');
    // Prevent event from bubbling up
    e.preventDefault();
    e.stopPropagation();
    // Blur the button to remove focus before closing
    e.currentTarget.blur();
    // Clear the selected location to close the panel
    clearSelections();
    // Call onClose callback if provided
    if (onClose) {
      onClose();
    }
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
            <h3>{t('infoPanel.tabs.history')}</h3>
            <p>{translatedHistory}</p>
            <div className="time-period">
              <h4>Time Period</h4>
              <div className="time-period-info">
                <span className="period">{translatedPeriod}</span>
                <span className="dynasty">{translatedDynasty}</span>
              </div>
            </div>
          </div>
        );
      case 'culture':
        return (
          <div className={`tab-content ${animationClass}`}>
            <h3>{t('infoPanel.tabs.culture')}</h3>
            <ul className="culture-facts">
              {locationData.culturalFacts.map((fact, index) => (
                <li key={index} className={`stagger-delay-${index % 5 + 1}`}>
                  <TranslatedText text={fact} />
                </li>
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
                  <h4><TranslatedText text={legend.title} /></h4>
                  <p><TranslatedText text={legend.description} /></p>
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
    <div className={panelClasses} aria-hidden={!isVisible}>
      <div className="panel-header">
        <button
          className="close-button"
          onClick={handleClose}
          aria-label="Close information panel"
          style={{ zIndex: 999 }}
        >
          ×
        </button>
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
            </div>
            <div className="info-header-content">
              <span className="badge">{selectedLocation.category || 'Heritage Site'}</span>
              <h2 className="location-title">{translatedName}</h2>
              <p className="info-sub">
                {selectedLocation.state || 'India'} · {selectedLocation.description?.substring(0, 40) || 'Cultural Heritage Site'}
              </p>
              <div className="info-chips">
                {(locationData?.tags || selectedLocation.tags || ['Heritage', 'Culture', 'History']).slice(0, 3).map((tag, index) => (
                  <span key={index} className="chip">{tag}</span>
                ))}
              </div>
            </div>
          </>
        )}
      </div>

      <div className="panel-tabs">
        <button
          className={`tab-button ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => handleTabChange('history')}
          aria-pressed={activeTab === 'history'}
        >
          {t('infoPanel.tabs.history')}
        </button>
        <button
          className={`tab-button ${activeTab === 'culture' ? 'active' : ''}`}
          onClick={() => handleTabChange('culture')}
          aria-pressed={activeTab === 'culture'}
        >
          {t('infoPanel.tabs.culture')}
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
          <div className="footer-buttons">
            <button
              className="explore-more-btn"
              onClick={() => onExploreRoute && onExploreRoute(selectedLocation)}
              title="Create a route including this location"
            >
              Explore Route
            </button>
            <button
              className="ci-trigger-btn"
              onClick={() => onCulturalIntelligence && onCulturalIntelligence()}
              title="Open Cultural Intelligence Analysis"
            >
              🧠 Ask Cultural AI
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfoPanel;