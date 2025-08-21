// cupe-kg-frontend/src/components/CulturalIntelligence/CulturalIntelligence.jsx
// This will be the MAIN FEATURE that sets your project apart

import React, { useState, useEffect } from 'react';
import './CulturalIntelligence.css';

const CulturalIntelligence = ({ 
  selectedLocation, 
  currentRoute, 
  isVisible, 
  onClose,
  onRecommendSimilar 
}) => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('overview');
  const [connectionStrength, setConnectionStrength] = useState(0);

  useEffect(() => {
    if (selectedLocation && isVisible) {
      generateCulturalInsights(selectedLocation);
    }
  }, [selectedLocation, isVisible]);

  const generateCulturalInsights = async (location) => {
    setLoading(true);
    try {
      // Simulate AI-powered cultural analysis
      const culturalAnalysis = await analyzeCulturalContext(location);
      setInsights(culturalAnalysis);
      
      // Calculate cultural connection strength
      const strength = calculateCulturalConnections(location, currentRoute);
      setConnectionStrength(strength);
    } catch (error) {
      console.error('Error generating cultural insights:', error);
    } finally {
      setLoading(false);
    }
  };

  // AI-powered cultural context analysis
  const analyzeCulturalContext = async (location) => {
    // This simulates your BERT-based cultural analysis
    return new Promise((resolve) => {
      setTimeout(() => {
        const analysis = {
          // Historical Context Analysis
          historicalContext: {
            era: location.period,
            dynasty: location.dynasty,
            politicalContext: generatePoliticalContext(location),
            economicContext: generateEconomicContext(location),
            socialContext: generateSocialContext(location)
          },

          // Cultural Significance Analysis
          culturalSignificance: {
            architecturalStyle: analyzeArchitecturalStyle(location),
            artisticInfluences: analyzeArtisticInfluences(location),
            religiousSignificance: analyzeReligiousSignificance(location),
            culturalExchange: analyzeCulturalExchange(location)
          },

          // Modern Relevance
          modernRelevance: {
            preservation: analyzePreservationStatus(location),
            tourism: analyzeTourismImpact(location),
            education: analyzeEducationalValue(location),
            inspiration: analyzeModernInspiration(location)
          },

          // Interconnections with other sites
          culturalConnections: findCulturalConnections(location),

          // Storytelling elements
          narrativeElements: generateNarrativeElements(location),

          // Recommended exploration approach
          explorationGuide: generateExplorationGuide(location)
        };
        resolve(analysis);
      }, 1500);
    });
  };

  // Generate political context using cultural intelligence
  const generatePoliticalContext = (location) => {
    const politicalContexts = {
      'Mughal Empire': {
        powerStructure: 'Centralized imperial administration with Persian influences',
        keyFigures: ['Akbar', 'Shah Jahan', 'Aurangzeb'],
        policies: 'Religious tolerance under early Mughals, later orthodox policies',
        militaryStrategy: 'Composite bow cavalry, gunpowder technology, fortified cities'
      },
      'Vijayanagara Empire': {
        powerStructure: 'Decentralized feudal system with strong military organization',
        keyFigures: ['Harihara I', 'Bukka Raya', 'Krishna Deva Raya'],
        policies: 'Hindu revival, patronage of arts, trade promotion',
        militaryStrategy: 'Elephant cavalry, fortified capital, alliance systems'
      },
      'Chandela Dynasty': {
        powerStructure: 'Regional kingdom with temple-centered governance',
        keyFigures: ['Yashovarman', 'Dhanga', 'Vidyadhara'],
        policies: 'Temple patronage, tantric philosophy integration',
        militaryStrategy: 'Cavalry-based armies, hill fort defenses'
      },
      'Eastern Ganga Dynasty': {
        powerStructure: 'Maritime kingdom with strong naval power',
        keyFigures: ['Narasimhadeva I', 'Anangabhima Deva'],
        policies: 'Temple construction, maritime trade, Kalinga architecture',
        militaryStrategy: 'Naval supremacy, coastal fortifications'
      }
    };

    return politicalContexts[location.dynasty] || {
      powerStructure: 'Regional governance with local administrative systems',
      keyFigures: ['Local rulers and administrators'],
      policies: 'Cultural patronage and regional development',
      militaryStrategy: 'Adapted to local geographical advantages'
    };
  };

  // Generate economic context
  const generateEconomicContext = (location) => {
    const economicPatterns = {
      'delhi': {
        tradeRoutes: ['Grand Trunk Road', 'Central Asian routes', 'Deccan trade'],
        primaryCommodities: ['Textiles', 'Spices', 'Precious metals', 'Crafts'],
        economicRole: 'Imperial capital and trade hub',
        monetarySystem: 'Silver-based currency with gold reserves'
      },
      'hampi': {
        tradeRoutes: ['Arabian Sea ports', 'Deccan plateau', 'South Indian networks'],
        primaryCommodities: ['Diamonds', 'Spices', 'Textiles', 'Horses'],
        economicRole: 'International trading metropolis',
        monetarySystem: 'Gold pagodas and silver currency'
      },
      'taj-mahal': {
        tradeRoutes: ['Yamuna river trade', 'Agra-Delhi corridor'],
        primaryCommodities: ['Marble', 'Precious stones', 'Luxury goods'],
        economicRole: 'Imperial center and luxury production',
        monetarySystem: 'Mughal silver rupees'
      }
    };

    return economicPatterns[location.id] || {
      tradeRoutes: ['Regional trade networks'],
      primaryCommodities: ['Local specialties', 'Agricultural products'],
      economicRole: 'Regional economic center',
      monetarySystem: 'Local and regional currency systems'
    };
  };

  // Analyze architectural style with AI insight
  const analyzeArchitecturalStyle = (location) => {
    const architecturalAnalysis = {
      'taj-mahal': {
        primaryStyle: 'Indo-Islamic (Mughal)',
        keyFeatures: ['Onion dome', 'Minarets', 'Pietra dura inlay', 'Symmetrical gardens'],
        innovations: ['Perfect proportional harmony', 'Color-changing marble effect'],
        influences: ['Persian', 'Central Asian', 'Indian'],
        globalImpact: 'Inspired Islamic architecture worldwide'
      },
      'hampi': {
        primaryStyle: 'Vijayanagara Architecture',
        keyFeatures: ['Pillared halls', 'Gopurams', 'Mandapas', 'Stone chariot'],
        innovations: ['Musical pillars', 'Monolithic sculptures', 'Hydraulic systems'],
        influences: ['Chalukya', 'Hoysala', 'Kakatiya'],
        globalImpact: 'Influenced South Indian temple architecture'
      },
      'khajuraho': {
        primaryStyle: 'Nagara (North Indian temple)',
        keyFeatures: ['Shikhara towers', 'Sculptural panels', 'Erotic sculptures'],
        innovations: ['Integration of tantra philosophy', 'Architectural symbolism'],
        influences: ['Gupta', 'Post-Gupta traditions'],
        globalImpact: 'Influenced medieval Indian sculpture'
      }
    };

    return architecturalAnalysis[location.id] || {
      primaryStyle: 'Regional architectural tradition',
      keyFeatures: ['Local building techniques', 'Regional materials'],
      innovations: ['Adaptation to local climate', 'Cultural integration'],
      influences: ['Local traditions', 'Regional kingdoms'],
      globalImpact: 'Contributed to Indian architectural diversity'
    };
  };

  // Find cultural connections between locations
  const findCulturalConnections = (location) => {
    // This would use your knowledge graph to find connections
    const connections = [];
    
    // Dynasty connections
    const sameDynastyLocations = window.allLocations?.filter(loc => 
      loc.dynasty === location.dynasty && loc.id !== location.id
    ) || [];
    
    if (sameDynastyLocations.length > 0) {
      connections.push({
        type: 'dynasty',
        title: `${location.dynasty} Heritage Sites`,
        locations: sameDynastyLocations,
        description: `Other monuments built during the ${location.dynasty} period`,
        strength: 'high'
      });
    }

    // Architectural style connections
    const sameStyleLocations = findArchitecturalConnections(location);
    if (sameStyleLocations.length > 0) {
      connections.push({
        type: 'architectural',
        title: 'Similar Architectural Style',
        locations: sameStyleLocations,
        description: 'Sites sharing similar architectural elements and techniques',
        strength: 'medium'
      });
    }

    // Religious/Cultural theme connections
    const themeConnections = findThematicConnections(location);
    if (themeConnections.length > 0) {
      connections.push({
        type: 'thematic',
        title: 'Cultural Theme Connections',
        locations: themeConnections,
        description: 'Sites connected by religious or cultural themes',
        strength: 'medium'
      });
    }

    return connections;
  };

  // Generate narrative elements for storytelling
  const generateNarrativeElements = (location) => {
    return {
      openingHook: generateOpeningHook(location),
      keyStories: generateKeyStories(location),
      characterSpotlight: generateCharacterSpotlight(location),
      mysteryElements: generateMysteryElements(location),
      culturalLessons: generateCulturalLessons(location),
      modernConnections: generateModernConnections(location)
    };
  };

  const generateOpeningHook = (location) => {
    const hooks = {
      'taj-mahal': "Imagine a love so profound that it created one of the world's most beautiful buildings...",
      'hampi': "Step into the ruins of what was once the world's second-largest medieval city...",
      'khajuraho': "Discover temples where stone comes alive with a thousand stories...",
      'varanasi': "Enter a city older than Rome, where time seems to flow differently..."
    };
    
    return hooks[location.id] || `Journey into the heart of ${location.name}, where history whispers through ancient stones...`;
  };

  const generateKeyStories = (location) => {
    // Extract from location legends and add AI-generated context
    const stories = location.legends || [];
    return stories.map(legend => ({
      ...legend,
      historicalContext: generateHistoricalContext(legend),
      modernInterpretation: generateModernInterpretation(legend),
      culturalSignificance: generateCulturalSignificance(legend)
    }));
  };

  // Calculate cultural connection strength
  const calculateCulturalConnections = (location, route) => {
    if (!route || !route.locations) return 0;
    
    let strength = 0;
    
    route.locations.forEach(routeLoc => {
      // Dynasty connections
      if (routeLoc.dynasty === location.dynasty) strength += 30;
      
      // Period overlap
      if (periodsOverlap(routeLoc.period, location.period)) strength += 20;
      
      // Category similarity
      if (routeLoc.category === location.category) strength += 15;
      
      // Tag overlap
      const commonTags = (routeLoc.tags || []).filter(tag => 
        (location.tags || []).includes(tag)
      );
      strength += commonTags.length * 5;
    });
    
    return Math.min(strength, 100); // Cap at 100%
  };

  const periodsOverlap = (period1, period2) => {
    // Simple overlap detection - could be made more sophisticated
    if (!period1 || !period2) return false;
    return period1.includes('CE') && period2.includes('CE');
  };

  if (!isVisible) return null;

  return (
    <div className="cultural-intelligence-overlay">
      <div className="cultural-intelligence-panel">
        <div className="ci-header">
          <h2>Cultural Intelligence: {selectedLocation?.name}</h2>
          <div className="connection-strength">
            <span>Route Connection: </span>
            <div className="strength-bar">
              <div 
                className="strength-fill" 
                style={{ width: `${connectionStrength}%` }}
              ></div>
            </div>
            <span>{connectionStrength}%</span>
          </div>
          <button className="close-btn" onClick={onClose}>✕</button>
        </div>

        <div className="ci-tabs">
          <button 
            className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
          <button 
            className={`tab ${activeTab === 'context' ? 'active' : ''}`}
            onClick={() => setActiveTab('context')}
          >
            Historical Context
          </button>
          <button 
            className={`tab ${activeTab === 'connections' ? 'active' : ''}`}
            onClick={() => setActiveTab('connections')}
          >
            Cultural Connections
          </button>
          <button 
            className={`tab ${activeTab === 'stories' ? 'active' : ''}`}
            onClick={() => setActiveTab('stories')}
          >
            Stories & Legends
          </button>
          <button 
            className={`tab ${activeTab === 'guide' ? 'active' : ''}`}
            onClick={() => setActiveTab('guide')}
          >
            Exploration Guide
          </button>
        </div>

        <div className="ci-content">
          {loading ? (
            <div className="loading-state">
              <div className="ai-thinking">
                <div className="thinking-dots">
                  <span></span><span></span><span></span>
                </div>
                <p>AI analyzing cultural context...</p>
              </div>
            </div>
          ) : (
            <div className="content-sections">
              {activeTab === 'overview' && insights && (
                <OverviewSection insights={insights} location={selectedLocation} />
              )}
              {activeTab === 'context' && insights && (
                <ContextSection insights={insights.historicalContext} />
              )}
              {activeTab === 'connections' && insights && (
                <ConnectionsSection 
                  connections={insights.culturalConnections} 
                  onRecommendSimilar={onRecommendSimilar}
                />
              )}
              {activeTab === 'stories' && insights && (
                <StoriesSection narratives={insights.narrativeElements} />
              )}
              {activeTab === 'guide' && insights && (
                <GuideSection guide={insights.explorationGuide} />
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Component sections
const OverviewSection = ({ insights, location }) => (
  <div className="overview-section">
    <div className="significance-grid">
      <div className="significance-card">
        <h4>Architectural Significance</h4>
        <p>{insights.culturalSignificance.architecturalStyle.primaryStyle}</p>
        <ul>
          {insights.culturalSignificance.architecturalStyle.keyFeatures.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>
      </div>
      
      <div className="significance-card">
        <h4>Historical Importance</h4>
        <p><strong>Era:</strong> {insights.historicalContext.era}</p>
        <p><strong>Dynasty:</strong> {insights.historicalContext.dynasty}</p>
        <p>{insights.historicalContext.politicalContext.powerStructure}</p>
      </div>
      
      <div className="significance-card">
        <h4>Cultural Impact</h4>
        <p>{insights.culturalSignificance.artisticInfluences}</p>
        <div className="impact-metrics">
          <span className="metric">
            <strong>Preservation:</strong> {insights.modernRelevance.preservation}
          </span>
        </div>
      </div>
    </div>
    
    <div className="ai-insights">
      <h4>🤖 AI Cultural Analysis</h4>
      <div className="insight-cards">
        <div className="insight-card">
          <h5>Unique Features</h5>
          <p>AI has identified distinctive elements that set this site apart from others in the region.</p>
        </div>
        <div className="insight-card">
          <h5>Cultural Synthesis</h5>
          <p>This location represents a convergence of multiple cultural traditions and influences.</p>
        </div>
      </div>
    </div>
  </div>
);

const ContextSection = ({ insights }) => (
  <div className="context-section">
    <div className="context-timeline">
      <h4>Political Context</h4>
      <div className="context-details">
        <p><strong>Power Structure:</strong> {insights.powerStructure}</p>
        <p><strong>Key Figures:</strong> {insights.keyFigures.join(', ')}</p>
        <p><strong>Policies:</strong> {insights.policies}</p>
      </div>
    </div>
    
    <div className="economic-context">
      <h4>Economic Context</h4>
      <div className="economic-grid">
        <div className="economic-item">
          <h5>Trade Routes</h5>
          <ul>
            {insights.economicContext?.tradeRoutes?.map((route, index) => (
              <li key={index}>{route}</li>
            )) || []}
          </ul>
        </div>
        <div className="economic-item">
          <h5>Primary Commodities</h5>
          <ul>
            {insights.economicContext?.primaryCommodities?.map((commodity, index) => (
              <li key={index}>{commodity}</li>
            )) || []}
          </ul>
        </div>
      </div>
    </div>
  </div>
);

const ConnectionsSection = ({ connections, onRecommendSimilar }) => (
  <div className="connections-section">
    <h4>Cultural Network Analysis</h4>
    {connections.map((connection, index) => (
      <div key={index} className={`connection-group ${connection.strength}`}>
        <div className="connection-header">
          <h5>{connection.title}</h5>
          <span className={`strength-badge ${connection.strength}`}>
            {connection.strength} connection
          </span>
        </div>
        <p>{connection.description}</p>
        <div className="connected-locations">
          {connection.locations.map((loc, locIndex) => (
            <div key={locIndex} className="connected-location">
              <span className="location-name">{loc.name}</span>
              <span className="location-period">{loc.period}</span>
            </div>
          ))}
        </div>
        <button 
          className="explore-connection-btn"
          onClick={() => onRecommendSimilar(connection)}
        >
          Explore Similar Sites
        </button>
      </div>
    ))}
  </div>
);

const StoriesSection = ({ narratives }) => (
  <div className="stories-section">
    <div className="narrative-hook">
      <h4>Opening Story</h4>
      <p className="hook-text">{narratives.openingHook}</p>
    </div>
    
    <div className="key-stories">
      <h4>Legends & Stories</h4>
      {narratives.keyStories.map((story, index) => (
        <div key={index} className="story-card">
          <h5>{story.title}</h5>
          <p className="story-description">{story.description}</p>
          {story.historicalContext && (
            <div className="story-context">
              <h6>Historical Context</h6>
              <p>{story.historicalContext}</p>
            </div>
          )}
        </div>
      ))}
    </div>
  </div>
);

const GuideSection = ({ guide }) => (
  <div className="guide-section">
    <h4>AI-Recommended Exploration</h4>
    <div className="exploration-tips">
      <div className="tip-category">
        <h5>Best Photography Spots</h5>
        <ul>
          <li>Golden hour shots from the main entrance</li>
          <li>Architectural details during midday</li>
          <li>Panoramic views from elevated positions</li>
        </ul>
      </div>
      
      <div className="tip-category">
        <h5>Cultural Etiquette</h5>
        <ul>
          <li>Respect religious customs and traditions</li>
          <li>Dress appropriately for sacred spaces</li>
          <li>Follow photography restrictions</li>
        </ul>
      </div>
      
      <div className="tip-category">
        <h5>Hidden Gems</h5>
        <ul>
          <li>Lesser-known architectural details</li>
          <li>Local legends and stories</li>
          <li>Best times for fewer crowds</li>
        </ul>
      </div>
    </div>
  </div>
);

// Helper functions
const findArchitecturalConnections = (location) => {
  // This would analyze architectural similarities
  return [];
};

const findThematicConnections = (location) => {
  // This would find thematic connections
  return [];
};

const generateHistoricalContext = (legend) => {
  return "Historical records suggest this legend reflects the cultural values and beliefs of the period.";
};

const generateModernInterpretation = (legend) => {
  return "Modern scholars interpret this story as a metaphor for the artistic and spiritual aspirations of the era.";
};

const generateCulturalSignificance = (legend) => {
  return "This legend continues to influence local traditions and artistic expressions today.";
};

export default CulturalIntelligence;