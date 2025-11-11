import React, { useState, useEffect } from 'react';
import './HistoricalView.css';

const HistoricalView = ({ location, historicalContext, isVisible, onClose }) => {
  const [currentImage, setCurrentImage] = useState('historical');
  const [imageLoaded, setImageLoaded] = useState(false);
  const [comparisonMode, setComparisonMode] = useState(false);

  useEffect(() => {
    setImageLoaded(false);
    setCurrentImage('historical');
  }, [location, historicalContext]);

  if (!isVisible || !location || !historicalContext) return null;

  const getHistoricalImagePath = () => {
    const basePath = '/assets/images/historical';
    const locationId = location.id || location.name.toLowerCase().replace(/\s+/g, '-');
    const era = historicalContext.era?.toLowerCase() || 'ancient';
    
    // Try different historical image paths
    const imagePaths = [
      `${basePath}/${locationId}-${era}-prime.jpg`,
      `${basePath}/${locationId}-historical.jpg`,
      `${basePath}/${locationId}-prime.jpg`,
      `${basePath}/${era}-architecture.jpg`,
      `${basePath}/generic-${historicalContext.dynasty?.toLowerCase().replace(/\s+/g, '-')}.jpg`,
      `${basePath}/default-historical.jpg`
    ];
    
    return imagePaths[0]; // Return primary path, with fallbacks handled in onError
  };

  const getModernImagePath = () => {
    return `/assets/images/${location.id || location.name.toLowerCase().replace(/\s+/g, '-')}.jpg`;
  };

  const getHistoricalDescription = () => {
    const { period, dynasty, era, timeframe } = historicalContext;
    
    return {
      title: `${location.name} in Its Prime (${timeframe})`,
      description: `During the ${dynasty || 'ancient period'}, ${location.name} was at the height of its cultural and architectural significance. This visualization shows how the site would have appeared during the ${era} period, complete with original structures, vibrant community life, and cultural activities.`,
      features: getHistoricalFeatures(),
      culturalLife: getHistoricalCulturalLife()
    };
  };

  const getHistoricalFeatures = () => {
    // Generate features based on location type and dynasty
    const baseFeatures = [
      "Complete architectural structures",
      "Active religious ceremonies",
      "Bustling marketplace activity",
      "Royal processions and festivals"
    ];

    // Add dynasty-specific features
    if (location.dynasty?.includes('Mughal')) {
      return [
        ...baseFeatures,
        "Ornate gardens with fountains",
        "Imperial court gatherings",
        "Intricate marble inlay work",
        "Persian-style architectural elements"
      ];
    } else if (location.dynasty?.includes('Vijayanagara')) {
      return [
        ...baseFeatures,
        "Grand temple complexes",
        "Stone chariot processions",
        "Hampi bazaar trading hub",
        "Royal elephant stables"
      ];
    } else if (location.dynasty?.includes('Chola')) {
      return [
        ...baseFeatures,
        "Towering temple gopurams",
        "Bronze sculpture workshops",
        "Classical dance performances",
        "Irrigation canal systems"
      ];
    }

    return baseFeatures;
  };

  const getHistoricalCulturalLife = () => {
    return [
      "Religious festivals and ceremonies",
      "Traditional arts and crafts",
      "Cultural performances and music",
      "Ancient trade and commerce",
      "Royal patronage of arts"
    ];
  };

  const historicalInfo = getHistoricalDescription();

  return (
    <div className={`historical-view ${isVisible ? 'visible' : ''}`}>
      <div className="historical-view-header">
        <button className="close-historical" onClick={onClose}>×</button>
        <div className="view-mode-toggle">
          <button 
            className={`mode-btn ${!comparisonMode ? 'active' : ''}`}
            onClick={() => setComparisonMode(false)}
          >
            Historical View
          </button>
          <button 
            className={`mode-btn ${comparisonMode ? 'active' : ''}`}
            onClick={() => setComparisonMode(true)}
          >
            Then vs Now
          </button>
        </div>
      </div>

      <div className="historical-content">
        <div className={`image-section ${comparisonMode ? 'comparison' : ''}`}>
          {!comparisonMode ? (
            <div className="historical-image-container">
              <img
                src={getHistoricalImagePath()}
                alt={`${location.name} in ${historicalContext.timeframe}`}
                className={`historical-image ${imageLoaded ? 'loaded' : ''}`}
                onLoad={() => setImageLoaded(true)}
                onError={(e) => {
                  // Fallback to default historical image
                  e.target.src = '/assets/images/historical/default-historical.jpg';
                }}
              />
              <div className="historical-overlay">
                <div className="time-period-badge">
                  {historicalContext.timeframe}
                </div>
                <div className="dynasty-badge">
                  {location.dynasty || 'Ancient Period'}
                </div>
              </div>
            </div>
          ) : (
            <div className="comparison-container">
              <div className="comparison-panel historical">
                <img
                  src={getHistoricalImagePath()}
                  alt={`${location.name} historical`}
                  className="comparison-image"
                  onError={(e) => {
                    e.target.src = '/assets/images/historical/default-historical.jpg';
                  }}
                />
                <div className="comparison-label historical">
                  Prime Era ({historicalContext.timeframe})
                </div>
              </div>
              <div className="comparison-panel modern">
                <img
                  src={getModernImagePath()}
                  alt={`${location.name} modern`}
                  className="comparison-image"
                  onError={(e) => {
                    e.target.src = '/assets/images/placeholder.jpg';
                  }}
                />
                <div className="comparison-label modern">Today</div>
              </div>
            </div>
          )}
        </div>

        <div className="historical-info">
          <h2>{historicalInfo.title}</h2>
          <p className="historical-description">{historicalInfo.description}</p>

          <div className="historical-features">
            <h3>Life in the Prime Era</h3>
            <div className="feature-grid">
              <div className="feature-category">
                <h4>Architectural Features</h4>
                <ul>
                  {historicalInfo.features.slice(0, 4).map((feature, index) => (
                    <li key={index}>{feature}</li>
                  ))}
                </ul>
              </div>
              <div className="feature-category">
                <h4>Cultural Life</h4>
                <ul>
                  {historicalInfo.culturalLife.map((activity, index) => (
                    <li key={index}>{activity}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>

          {location.history && (
            <div className="historical-context">
              <h3>Historical Context</h3>
              <p>{location.history}</p>
            </div>
          )}

          <div className="period-timeline">
            <h3>Era Timeline</h3>
            <div className="timeline-bar">
              <div className="timeline-marker" style={{
                left: '20%',
                backgroundColor: historicalContext.era === 'BCE' ? '#e91e63' : '#3f51b5'
              }}>
                <span className="marker-label">{historicalContext.timeframe}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoricalView;