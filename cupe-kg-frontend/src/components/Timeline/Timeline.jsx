// cupe-kg-frontend/src/components/Timeline/Timeline.jsx
// FINAL VERSION with Complete API Integration

import React, { useState, useEffect, useCallback } from 'react';
import { useTranslation } from 'react-i18next';
import { useMapContext } from '../../context/MapContext';
import timelineApiService from '../../services/timelineApi';
import { useTranslatedText } from '../../utils/translationHelper';
import './Timeline.css';

// Helper component to translate text items
const TranslatedText = ({ text }) => {
  const { translatedText } = useTranslatedText(text || '');
  return <>{translatedText}</>;
};

const Timeline = ({ isVisible, onLocationSelect }) => {
  const { t } = useTranslation();
  const { locations, selectLocation, selectedLocation } = useMapContext();
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [timelinePeriods, setTimelinePeriods] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dataSource, setDataSource] = useState('none');
  const [apiHealth, setApiHealth] = useState(null);

  // Fetch timeline data from backend API
  const fetchTimelineFromAPI = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      console.log('Timeline: Attempting to fetch from API...');
      
      // First check API health
      try {
        const health = await timelineApiService.checkTimelineHealth();
        setApiHealth(health);
        console.log('Timeline API Health:', health);
      } catch (healthError) {
        console.warn('Timeline API health check failed:', healthError.message);
      }
      
      // Fetch timeline data
      const data = await timelineApiService.fetchTimelinePeriods();
      
      if (data.periods && data.periods.length > 0) {
        setTimelinePeriods(data.periods);
        setDataSource('backend');
        console.log(`Timeline: Successfully loaded ${data.totalPeriods} periods from backend API`);
        console.log('Timeline data:', data);
      } else {
        throw new Error('No timeline periods received from API');
      }
      
    } catch (error) {
      console.error('Timeline API Error:', error);
      setError(error.message);
      
      // Fallback to frontend processing
      console.log('Timeline: Falling back to frontend data processing');
      if (locations && locations.length > 0) {
        const periods = processLocationsIntoTimeline(locations);
        setTimelinePeriods(periods);
        setDataSource('frontend-fallback');
      } else {
        setDataSource('no-data');
      }
    } finally {
      setIsLoading(false);
    }
  }, [locations]);

  // Process locations into timeline periods (fallback method)
  const processLocationsIntoTimeline = useCallback((locations) => {
    if (!locations || !Array.isArray(locations)) {
      console.warn('Timeline: Invalid locations data for processing');
      return [];
    }

    const periodMap = new Map();
    
    locations.forEach(location => {
      if (!location || !location.period) return;
      
      try {
        // Extract period information
        const periodInfo = extractPeriodInfo(location.period);
        
        periodInfo.forEach(period => {
          const key = period.label;
          if (!periodMap.has(key)) {
            periodMap.set(key, {
              ...period,
              locations: []
            });
          }
          periodMap.get(key).locations.push(location);
        });
      } catch (err) {
        console.warn(`Timeline: Error processing location ${location.name}:`, err);
      }
    });
    
    // Convert to array and sort by start year
    const periodsArray = Array.from(periodMap.values());
    periodsArray.sort((a, b) => a.startYear - b.startYear);
    
    console.log(`Timeline: Processed ${periodsArray.length} periods from ${locations.length} locations`);
    return periodsArray;
  }, []);

  const extractPeriodInfo = (periodString) => {
    const periods = [];
    
    if (!periodString || typeof periodString !== 'string') {
      return periods;
    }
    
    // Handle different period formats with more robust patterns
    const patterns = [
      // "1336 CE - 1646 CE"
      {
        regex: /(\d{1,4})\s*CE\s*-\s*(\d{1,4})\s*CE/i,
        handler: (match) => ({
          startYear: parseInt(match[1]),
          endYear: parseInt(match[2]),
          label: `${match[1]} CE - ${match[2]} CE`,
          era: 'CE'
        })
      },
      // "13th century CE"
      {
        regex: /(\d{1,2})(?:st|nd|rd|th)\s*century\s*CE/i,
        handler: (match) => {
          const century = parseInt(match[1]);
          const startYear = (century - 1) * 100 + 1;
          const endYear = century * 100;
          return {
            startYear,
            endYear,
            label: `${century}${getOrdinalSuffix(century)} Century CE`,
            era: 'CE'
          };
        }
      },
      // "950 CE - 1050 CE" (range without second CE)
      {
        regex: /(\d{1,4})\s*-\s*(\d{1,4})\s*CE/i,
        handler: (match) => ({
          startYear: parseInt(match[1]),
          endYear: parseInt(match[2]),
          label: `${match[1]} - ${match[2]} CE`,
          era: 'CE'
        })
      },
      // Single year "1632 CE"
      {
        regex: /(\d{1,4})\s*CE/i,
        handler: (match) => ({
          startYear: parseInt(match[1]),
          endYear: parseInt(match[1]) + 50, // Approximate 50-year span
          label: `${match[1]} CE`,
          era: 'CE'
        })
      },
      // "2nd century BCE"
      {
        regex: /(\d{1,2})(?:st|nd|rd|th)\s*century\s*BCE/i,
        handler: (match) => {
          const century = parseInt(match[1]);
          return {
            startYear: -(century * 100),
            endYear: -((century - 1) * 100 + 1),
            label: `${century}${getOrdinalSuffix(century)} Century BCE`,
            era: 'BCE'
          };
        }
      },
      // Complex periods like "3rd century BCE (with later additions)"
      {
        regex: /(\d{1,2})(?:st|nd|rd|th)\s*century\s*BCE.*$/i,
        handler: (match) => {
          const century = parseInt(match[1]);
          return {
            startYear: -(century * 100),
            endYear: -((century - 1) * 100 + 1),
            label: `${century}${getOrdinalSuffix(century)} Century BCE`,
            era: 'BCE'
          };
        }
      }
    ];
    
    for (const pattern of patterns) {
      const match = periodString.match(pattern.regex);
      if (match) {
        try {
          periods.push(pattern.handler(match));
          break;
        } catch (err) {
          console.warn(`Error parsing period "${periodString}":`, err);
          continue;
        }
      }
    }
    
    // Fallback: create a general period
    if (periods.length === 0) {
      periods.push({
        startYear: 1000, // Default
        endYear: 2000,
        label: periodString.trim(),
        era: 'Unknown'
      });
    }
    
    return periods;
  };

  // Helper function for ordinal suffixes
  const getOrdinalSuffix = (num) => {
    const remainder = num % 10;
    const hundredRemainder = num % 100;
    
    if (hundredRemainder >= 11 && hundredRemainder <= 13) {
      return 'th';
    }
    
    switch (remainder) {
      case 1: return 'st';
      case 2: return 'nd';
      case 3: return 'rd';
      default: return 'th';
    }
  };

  // Main effect: Load timeline data when component becomes visible
  useEffect(() => {
    if (isVisible && timelinePeriods.length === 0) {
      fetchTimelineFromAPI();
    }
  }, [isVisible, fetchTimelineFromAPI, timelinePeriods.length]);

  // Fallback effect: Use local data if API fails and locations are available
  useEffect(() => {
    if (locations && locations.length > 0 && timelinePeriods.length === 0 && !isLoading && dataSource === 'no-data') {
      console.log('Timeline: Using local locations data as final fallback');
      const periods = processLocationsIntoTimeline(locations);
      if (periods.length > 0) {
        setTimelinePeriods(periods);
        setDataSource('frontend');
      }
    }
  }, [locations, timelinePeriods.length, isLoading, dataSource, processLocationsIntoTimeline]);

  const handlePeriodClick = (period) => {
    if (selectedPeriod?.label === period.label) {
      setSelectedPeriod(null);
      // Reset to modern view
      if (onLocationSelect) {
        onLocationSelect(null, 'modern');
      }
    } else {
      setSelectedPeriod(period);
      // Trigger historical visualization mode
      if (onLocationSelect) {
        onLocationSelect(period.locations[0] || null, 'historical', {
          period: period,
          era: period.era,
          timeframe: period.label
        });
      }
    }
  };

  const handleLocationClick = (location) => {
    selectLocation(location);
    if (onLocationSelect) {
      // Pass historical context when clicking from timeline
      onLocationSelect(location, 'historical', {
        period: selectedPeriod,
        era: selectedPeriod?.era,
        timeframe: selectedPeriod?.label,
        dynasty: location.dynasty
      });
    }
  };

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  // Retry loading from API
  const retryApiLoad = () => {
    setError(null);
    setTimelinePeriods([]);
    setDataSource('none');
    fetchTimelineFromAPI();
  };

  const getEraColor = (era) => {
    const colors = {
      'CE': '#3f51b5',
      'BCE': '#e91e63',
      'Unknown': '#757575'
    };
    return colors[era] || colors['Unknown'];
  };

  const getDynastyColor = (dynasty) => {
    if (!dynasty) return '#757575';
    
    const colors = {
      'Mughal Empire': '#ff9800',
      'Vijayanagara Empire': '#4caf50',
      'Chandela Dynasty': '#9c27b0',
      'Eastern Ganga Dynasty': '#f44336',
      'Satavahana and Vakataka': '#00bcd4',
      'Rashtrakuta Dynasty': '#795548',
      'Delhi Sultanate': '#607d8b',
      'Sikh Gurus': '#9c27b0',
      'Portuguese Colonial': '#ff5722',
      'Mauryan Empire': '#3f51b5'
    };
    
    // Find matching dynasty
    for (const [key, color] of Object.entries(colors)) {
      if (dynasty.includes(key)) {
        return color;
      }
    }
    return '#757575';
  };

  if (!isVisible) return null;

  return (
    <div className={`timeline-container ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="timeline-header" onClick={toggleExpanded}>
        <h3>{t('timeline.title', 'Historical Timeline')}</h3>
        <div className="timeline-status">
          {dataSource === 'backend' && <span className="data-source-indicator api" title="Data from backend API">API</span>}
          {dataSource === 'frontend' && <span className="data-source-indicator local" title="Data processed locally">LOCAL</span>}
          {dataSource === 'frontend-fallback' && <span className="data-source-indicator fallback" title="Fallback to local processing">FALLBACK</span>}
          {apiHealth && (
            <span className="api-health-indicator" title={`${apiHealth.locationsWithPeriods}/${apiHealth.totalLocations} locations have period data`}>
              {apiHealth.locationsWithPeriods}/{apiHealth.totalLocations}
            </span>
          )}
        </div>
        <button className="expand-button" />
      </div>
      
      {isExpanded && (
        <div className="timeline-content">
          {/* Loading State */}
          {isLoading && (
            <div className="timeline-loading">
              <div className="loading-spinner"></div>
              <p>{t('timeline.loading', 'Loading timeline data from server...')}</p>
            </div>
          )}

          {/* Error State with Retry */}
          {error && !isLoading && timelinePeriods.length === 0 && (
            <div className="timeline-error">
              <div className="error-message">
                <p>{t('timeline.error', 'Failed to load timeline data')}</p>
                <small>{error}</small>
              </div>
              <button onClick={retryApiLoad} className="retry-button">
                {t('timeline.retry', 'Retry API Connection')}
              </button>
            </div>
          )}

          {/* Timeline Periods */}
          {!isLoading && timelinePeriods.length > 0 && (
            <>
              <div className="timeline-periods">
                {timelinePeriods.map((period, index) => (
                  <div 
                    key={`${period.label}-${index}`}
                    className={`timeline-period ${selectedPeriod?.label === period.label ? 'active' : ''}`}
                    onClick={() => handlePeriodClick(period)}
                  >
                    <div 
                      className="period-marker"
                      style={{ backgroundColor: getEraColor(period.era) }}
                    />
                    
                    <div className="period-info">
                      <div className="period-label">
                        {period.label}
                      </div>
                      <div className="period-meta">
                        {period.locations?.length || 0} location{(period.locations?.length || 0) !== 1 ? 's' : ''}
                        {period.era !== 'Unknown' && (
                          <span className="era-indicator"> • {period.era}</span>
                        )}
                      </div>
                    </div>
                    
                    {selectedPeriod?.label === period.label && period.locations && (
                      <div className="period-locations">
                        <h4>{t('timeline.heritageSites', 'Heritage Sites from this Period')}</h4>
                        <ul>
                          {period.locations.map((location, locIndex) => (
                            <li
                              key={location.id || `${location.name}-${locIndex}`}
                              className={`location-item ${selectedLocation?.id === location.id ? 'selected' : ''}`}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleLocationClick(location);
                              }}
                            >
                              <div className="location-info">
                                <div className="location-name">
                                  <TranslatedText text={location.name} />
                                </div>
                                {location.dynasty && (
                                  <div className="location-dynasty">
                                    <TranslatedText text={location.dynasty} />
                                  </div>
                                )}
                                {location.category && (
                                  <div className="location-category">
                                    <TranslatedText text={location.category} />
                                  </div>
                                )}
                              </div>
                              <div 
                                className="dynasty-indicator"
                                style={{ backgroundColor: getDynastyColor(location.dynasty) }}
                                title={location.dynasty || 'Unknown dynasty'}
                              />
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
              
              {/* Data source info */}
              {(error || dataSource === 'frontend-fallback') && (
                <div className="timeline-info">
                  <small>
                    {dataSource === 'frontend-fallback' && '⚠️ Using fallback data processing'}
                    {error && !timelinePeriods.length && '❌ Server connection failed'}
                  </small>
                </div>
              )}
            </>
          )}

          {/* Empty State */}
          {!isLoading && timelinePeriods.length === 0 && !error && (
            <div className="timeline-empty">
              <div className="timeline-empty-icon">📅</div>
              <div className="timeline-empty-text">
                No timeline data available
              </div>
              <button onClick={retryApiLoad} className="retry-button">
                Try Loading Again
              </button>
            </div>
          )}
          
          {/* Legend */}
          {timelinePeriods.length > 0 && (
            <div className="timeline-legend">
              <h4>Era Legend</h4>
              <div className="legend-items">
                <div className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: '#3f51b5' }}></div>
                  <span>Common Era (CE)</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color" style={{ backgroundColor: '#e91e63' }}></div>
                  <span>Before Common Era (BCE)</span>
                </div>
                {timelinePeriods.some(p => p.era === 'Unknown') && (
                  <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: '#757575' }}></div>
                    <span>Unknown Period</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Timeline;