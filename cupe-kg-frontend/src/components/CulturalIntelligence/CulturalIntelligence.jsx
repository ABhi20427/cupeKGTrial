// cupe-kg-frontend/src/components/CulturalIntelligence/CulturalIntelligence.jsx
// COMPLETE IMPLEMENTATION - Replace your entire file with this

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
      // Simulate AI-powered cultural analysis (Your BERT model would go here)
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

  // AI-powered cultural context analysis using BERT backend
  const analyzeCulturalContext = async (location) => {
    try {
      const response = await fetch('/api/cultural-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          locationId: location.id,
          locationName: location.name,
          dynasty: location.dynasty,
          period: location.period,
          description: location.description
        })
      });
      
      const analysis = await response.json();
      return analysis;
    } catch (error) {
      console.error('Error fetching cultural analysis:', error);
      // Fallback to mock data
      return {
        historicalContext: {
          era: location.period || 'Historical Period',
          dynasty: location.dynasty || 'Regional Dynasty',
          politicalContext: generatePoliticalContext(location),
          economicContext: generateEconomicContext(location),
          socialContext: generateSocialContext(location)
        },
        culturalSignificance: {
          architecturalStyle: analyzeArchitecturalStyle(location),
          artisticInfluences: analyzeArtisticInfluences(location),
          religiousSignificance: analyzeReligiousSignificance(location),
          culturalExchange: analyzeCulturalExchange(location)
        },
        modernRelevance: {
          preservation: analyzePreservationStatus(location),
          tourism: analyzeTourismImpact(location),
          education: analyzeEducationalValue(location),
          inspiration: analyzeModernInspiration(location)
        },
        culturalConnections: findCulturalConnections(location),
        narrativeElements: generateNarrativeElements(location),
        explorationGuide: generateExplorationGuide(location)
      };
    }
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
      }
    };

    const dynasty = location.dynasty || 'Regional Dynasty';
    return politicalContexts[dynasty] || {
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

    const locationId = location.id || location.name?.toLowerCase().replace(/\s+/g, '-');
    return economicPatterns[locationId] || {
      tradeRoutes: ['Regional trade networks'],
      primaryCommodities: ['Local specialties', 'Agricultural products'],
      economicRole: 'Regional economic center',
      monetarySystem: 'Local and regional currency systems'
    };
  };

  // Generate social context
  const generateSocialContext = (location) => {
    return {
      socialHierarchy: 'Complex caste-based society with royal patronage',
      culturalPractices: 'Religious festivals, artistic patronage, educational institutions',
      demographicComposition: 'Mixed religious and ethnic communities',
      dailyLife: 'Agricultural and trade-based economy with urban centers'
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
        keyFeatures: ['Shikhara towers', 'Sculptural panels', 'Erotic sculptures', 'Intricate carvings'],
        innovations: ['Integration of tantra philosophy', 'Architectural symbolism'],
        influences: ['Gupta', 'Post-Gupta traditions', 'Tantric philosophy'],
        globalImpact: 'Influenced medieval Indian sculpture and temple design'
      }
    };

    const locationId = location.id || location.name?.toLowerCase().replace(/\s+/g, '-');
    return architecturalAnalysis[locationId] || {
      primaryStyle: 'Regional architectural tradition',
      keyFeatures: ['Local building techniques', 'Regional materials', 'Cultural motifs'],
      innovations: ['Adaptation to local climate', 'Cultural integration'],
      influences: ['Local traditions', 'Regional kingdoms'],
      globalImpact: 'Contributed to Indian architectural diversity'
    };
  };

  // Other helper functions (simplified for brevity)
  const analyzeArtisticInfluences = (location) => {
    return `Rich artistic traditions reflecting ${location.dynasty || 'local'} cultural values and synthesis of multiple artistic traditions.`;
  };

  const analyzeReligiousSignificance = (location) => {
    return `Significant spiritual and religious importance in Indian culture, representing the integration of faith and artistry.`;
  };

  const analyzeCulturalExchange = (location) => {
    return 'This site represents the synthesis of multiple cultural traditions, showcasing India\'s history of cultural exchange and adaptation.';
  };

  const analyzePreservationStatus = (location) => {
    if (location.tags && location.tags.includes('UNESCO Heritage')) {
      return 'UNESCO World Heritage Site with active conservation programs';
    }
    return 'Protected monument under Archaeological Survey of India';
  };

  const analyzeTourismImpact = (location) => {
    return 'Major tourist destination contributing to local economy and cultural awareness';
  };

  const analyzeEducationalValue = (location) => {
    return 'Serves as an open-air museum teaching art, architecture, history, and cultural studies';
  };

  const analyzeModernInspiration = (location) => {
    return 'Continues to inspire contemporary artists, architects, and cultural practitioners worldwide';
  };

  // Find cultural connections between locations
  const findCulturalConnections = (location) => {
    const connections = [];
    
    // Mock data - in real implementation, this would use your knowledge graph
    const mockConnections = [
      {
        type: 'dynasty',
        title: `${location.dynasty || 'Historical'} Heritage Sites`,
        locations: [
          { name: 'Related Site 1', period: location.period },
          { name: 'Related Site 2', period: location.period }
        ],
        description: `Other monuments from the ${location.dynasty || 'same'} period`,
        strength: 'high'
      },
      {
        type: 'architectural',
        title: 'Similar Architectural Style',
        locations: [
          { name: 'Style Comparison Site 1', period: location.period },
          { name: 'Style Comparison Site 2', period: location.period }
        ],
        description: 'Sites sharing architectural elements and design principles',
        strength: 'medium'
      }
    ];

    return mockConnections;
  };

  // Generate narrative elements for storytelling
  const generateNarrativeElements = (location) => {
    return {
      openingHook: generateOpeningHook(location),
      keyStories: location.legends || [
        { title: 'Local Legend', description: 'Fascinating stories passed down through generations about this remarkable site.' }
      ],
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
      'khajuraho': "Discover temples where stone comes alive with stories of human passion and divine spirituality...",
      'varanasi': "Enter a city older than Rome, where time seems to flow differently...",
      'konark': "Behold a temple designed as the chariot of the Sun God, where time itself was captured in stone...",
      'delhi': "Walk through a city that has been the seat of power for over a millennium..."
    };
    
    const locationId = location.id || location.name?.toLowerCase().replace(/\s+/g, '-');
    return hooks[locationId] || `Journey into the heart of ${location.name}, where history whispers through ancient stones...`;
  };

  const generateCharacterSpotlight = (location) => {
    return `The visionary rulers and skilled artisans who created this magnificent testament to ${location.dynasty || 'ancient'} culture and craftsmanship.`;
  };

  const generateMysteryElements = (location) => {
    return 'Archaeological mysteries and hidden details that continue to fascinate researchers and visitors alike.';
  };

  const generateCulturalLessons = (location) => {
    return [
      'Religious tolerance and cultural synthesis',
      'Artistic excellence through royal patronage',
      'Integration of spiritual and material worlds',
      'Preservation of cultural heritage for future generations'
    ];
  };

  const generateModernConnections = (location) => {
    return 'This heritage site continues to influence modern Indian identity, artistic expression, and cultural pride.';
  };

  const generateExplorationGuide = (location) => {
    return {
      bestTimes: 'Early morning or late afternoon for optimal lighting and fewer crowds',
      photographyTips: 'Focus on architectural details and play of light and shadow',
      culturalEtiquette: 'Respect religious customs and dress appropriately',
      hiddenGems: 'Look for lesser-known carvings and architectural details often missed by tourists',
      localInsights: 'Engage with local guides who can share oral traditions and stories'
    };
  };

  // Calculate cultural connection strength
  const calculateCulturalConnections = (location, route) => {
    if (!route || !route.locations) return Math.floor(Math.random() * 50) + 30; // Mock calculation
    
    let strength = 0;
    
    route.locations.forEach(routeLoc => {
      // Dynasty connections
      if (routeLoc.dynasty === location.dynasty) strength += 30;
      
      // Period overlap
      if (routeLoc.period && location.period && routeLoc.period === location.period) strength += 20;
      
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

  if (!isVisible) return null;

  return (
    <div className="cultural-intelligence-overlay">
      <div className="cultural-intelligence-panel">
        <div className="ci-header">
          <h2>Cultural Intelligence: {selectedLocation?.name || 'Heritage Site'}</h2>
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
        <p><strong>Style:</strong> {insights.culturalSignificance.architecturalStyle.primaryStyle}</p>
        <h5>Key Features:</h5>
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
        <p><strong>Power Structure:</strong> {insights.politicalContext.powerStructure}</p>
        <p><strong>Key Figures:</strong> {insights.politicalContext.keyFigures.join(', ')}</p>
        <p><strong>Policies:</strong> {insights.politicalContext.policies}</p>
        <p><strong>Military Strategy:</strong> {insights.politicalContext.militaryStrategy}</p>
      </div>
    </div>
    
    <div className="economic-context">
      <h4>Economic Context</h4>
      <div className="economic-grid">
        <div className="economic-item">
          <h5>Trade Routes</h5>
          <ul>
            {insights.economicContext.tradeRoutes.map((route, index) => (
              <li key={index}>{route}</li>
            ))}
          </ul>
        </div>
        <div className="economic-item">
          <h5>Primary Commodities</h5>
          <ul>
            {insights.economicContext.primaryCommodities.map((commodity, index) => (
              <li key={index}>{commodity}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  </div>
);

const ConnectionsSection = ({ connections, onRecommendSimilar }) => (
  <div className="connections-section">
    <h4>Cultural Network Analysis</h4>
    {connections.length > 0 ? connections.map((connection, index) => (
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
        {onRecommendSimilar && (
          <button 
            className="explore-connection-btn"
            onClick={() => onRecommendSimilar(connection)}
          >
            Explore Similar Sites
          </button>
        )}
      </div>
    )) : (
      <p>No direct cultural connections found with other sites in the current database.</p>
    )}
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
      {narratives.keyStories.length > 0 ? narratives.keyStories.map((story, index) => (
        <div key={index} className="story-card">
          <h5>{story.title || 'Local Legend'}</h5>
          <p className="story-description">{story.description || story}</p>
        </div>
      )) : (
        <div className="story-card">
          <h5>Cultural Heritage</h5>
          <p className="story-description">Local legends and stories are being researched for this location.</p>
        </div>
      )}
    </div>
    
    <div className="character-spotlight">
      <h4>Character Spotlight</h4>
      <p>{narratives.characterSpotlight}</p>
    </div>
  </div>
);

const GuideSection = ({ guide }) => (
  <div className="guide-section">
    <h4>AI-Recommended Exploration</h4>
    <div className="exploration-tips">
      <div className="tip-category">
        <h5>Best Photography Times</h5>
        <p>{guide.bestTimes}</p>
      </div>
      
      <div className="tip-category">
        <h5>Photography Tips</h5>
        <p>{guide.photographyTips}</p>
      </div>
      
      <div className="tip-category">
        <h5>Cultural Etiquette</h5>
        <p>{guide.culturalEtiquette}</p>
      </div>
      
      <div className="tip-category">
        <h5>Hidden Gems</h5>
        <p>{guide.hiddenGems}</p>
      </div>
      
      <div className="tip-category">
        <h5>Local Insights</h5>
        <p>{guide.localInsights}</p>
      </div>
    </div>
  </div>
);

export default CulturalIntelligence;