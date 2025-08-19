// src/components/Timeline/Timeline.jsx

import React, { useState, useEffect } from 'react';
import { useMapContext } from '../../context/MapContext';
import './Timeline.css';

const Timeline = ({ isVisible, onLocationSelect }) => {
  const { locations, selectLocation, selectedLocation } = useMapContext();
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [timelinePeriods, setTimelinePeriods] = useState([]);

  // Process locations into timeline periods
  useEffect(() => {
    if (locations.length > 0) {
      const periods = processLocationsIntoTimeline(locations);
      setTimelinePeriods(periods);
    }
  }, [locations]);

  const processLocationsIntoTimeline = (locations) => {
    const periodMap = new Map();
    
    locations.forEach(location => {
      if (!location.period) return;
      
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
    });
    
    // Convert to array and sort by start year
    const periodsArray = Array.from(periodMap.values());
    periodsArray.sort((a, b) => a.startYear - b.startYear);
    
    return periodsArray;
  };

  const extractPeriodInfo = (periodString) => {
    const periods = [];
    
    // Handle different period formats
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
            label: `${match[1]}th Century CE`,
            era: 'CE'
          };
        }
      },
      // "950 CE - 1050 CE"
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
          endYear: parseInt(match[1]) + 50, // Approximate
          label: `${match[1]} CE`,
          era: 'CE'
        })
      }
    ];
    
    for (const pattern of patterns) {
      const match = periodString.match(pattern.regex);
      if (match) {
        periods.push(pattern.handler(match));
        break;
      }
    }
    
    // Fallback: create a general period
    if (periods.length === 0) {
      periods.push({
        startYear: 1000, // Default
        endYear: 2000,
        label: periodString,
        era: 'Unknown'
      });
    }
    
    return periods;
  };

  const handlePeriodClick = (period) => {
    if (selectedPeriod?.label === period.label) {
      setSelectedPeriod(null);
    } else {
      setSelectedPeriod(period);
    }
  };

  const handleLocationClick = (location) => {
    selectLocation(location);
    if (onLocationSelect) {
      onLocationSelect(location);
    }
  };

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
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
    const colors = {
      'Mughal Empire': '#ff9800',
      'Vijayanagara Empire': '#4caf50',
      'Chandela Dynasty': '#9c27b0',
      'Eastern Ganga Dynasty': '#f44336',
      'Satavahana and Vakataka': '#00bcd4',
      'Rashtrakuta Dynasty': '#795548',
      'Delhi Sultanate': '#607d8b'
    };
    
    // Find matching dynasty
    for (const [key, color] of Object.entries(colors)) {
      if (dynasty && dynasty.includes(key)) {
        return color;
      }
    }
    return '#757575';
  };

  if (!isVisible) return null;

  return (
    <div className={`timeline-container ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="timeline-header" onClick={toggleExpanded}>
        <h3>Historical Timeline</h3>
        <button className="expand-button" />
      </div>
      
      {isExpanded && (
        <div className="timeline-content">
          <div className="timeline-periods">
            {timelinePeriods.map((period, index) => (
              <div 
                key={period.label}
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
                    {period.locations.length} location{period.locations.length !== 1 ? 's' : ''}
                  </div>
                </div>
                
                {selectedPeriod?.label === period.label && (
                  <div className="period-locations">
                    <h4>Heritage Sites from this Period</h4>
                    <ul>
                      {period.locations.map((location) => (
                        <li
                          key={location.id}
                          className={`location-item ${selectedLocation?.id === location.id ? 'selected' : ''}`}
                          onClick={(e) => {
                            e.stopPropagation();
                            handleLocationClick(location);
                          }}
                        >
                          <div className="location-info">
                            <div className="location-name">{location.name}</div>
                            <div className="location-dynasty">
                              {location.dynasty}
                            </div>
                          </div>
                          <div 
                            className="dynasty-indicator"
                            style={{ backgroundColor: getDynastyColor(location.dynasty) }}
                          />
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {timelinePeriods.length === 0 && (
            <div className="no-timeline-data">
              <p>Loading timeline data...</p>
            </div>
          )}
          
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
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline;