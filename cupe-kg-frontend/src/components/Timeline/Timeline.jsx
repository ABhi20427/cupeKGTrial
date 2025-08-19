// src/components/Timeline/Timeline.jsx

import React, { useState, useEffect, useCallback } from 'react';
import { useMapContext } from '../../context/MapContext';
import './Timeline.css';

const Timeline = ({ isVisible, onLocationSelect }) => {
  const { locations, selectLocation, selectedLocation } = useMapContext();
  const [selectedPeriod, setSelectedPeriod] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  const [timelinePeriods, setTimelinePeriods] = useState([]);

  const extractPeriodInfo = useCallback((periodString) => {
    // Regular expressions to match different date formats
    const dateRangeRegex = /(\d{1,4})\s*(?:BCE|CE)?\s*-\s*(\d{1,4})\s*(?:BCE|CE)?/i;
    const singleDateRegex = /(\d{1,4})\s*(?:BCE|CE)?/i;
    const centuryRegex = /(\d{1,2})(?:st|nd|rd|th)\s+century\s+(?:BCE|CE)?/i;

    let periods = [];
    
    // Try to match date range format
    const rangeMatch = periodString.match(dateRangeRegex);
    if (rangeMatch) {
      const [_, start, end] = rangeMatch;
      periods.push({
        start: parseInt(start),
        end: parseInt(end),
        label: periodString,
        type: 'range'
      });
      return periods;
    }

    // Try to match century format
    const centuryMatch = periodString.match(centuryRegex);
    if (centuryMatch) {
      const century = parseInt(centuryMatch[1]);
      const startYear = (century - 1) * 100;
      const endYear = century * 100;
      periods.push({
        start: startYear,
        end: endYear,
        label: periodString,
        type: 'century'
      });
      return periods;
    }

    // Try to match single date
    const singleMatch = periodString.match(singleDateRegex);
    if (singleMatch) {
      const year = parseInt(singleMatch[1]);
      periods.push({
        start: year,
        end: year,
        label: periodString,
        type: 'year'
      });
      return periods;
    }

    // Fallback for unparseable dates
    periods.push({
      start: 0,
      end: 0,
      label: periodString,
      type: 'unknown'
    });

    return periods;
  }, []);

  const processLocationsIntoTimeline = useCallback((locs) => {
    const periodMap = new Map();
    
    locations.forEach(location => {
      if (!location.period) return;
      
      const periodInfo = extractPeriodInfo(location.period);
      
      periodInfo.forEach(period => {
        const key = `${period.start}-${period.end}`;
        if (!periodMap.has(key)) {
          periodMap.set(key, {
            start: period.start,
            end: period.end,
            label: period.label,
            type: period.type,
            locations: [],
            dynasties: new Set()
          });
        }
        
        const periodData = periodMap.get(key);
        periodData.locations.push(location);
        if (location.dynasty) {
          periodData.dynasties.add(location.dynasty);
        }
      });
    });
    
    // Convert to array and sort by start year
    return Array.from(periodMap.values())
      .sort((a, b) => a.start - b.start)
      .map(period => ({
        ...period,
        dynasties: Array.from(period.dynasties)
      }));
  }, [extractPeriodInfo]);

  useEffect(() => {
    if (locations.length > 0) {
      const periods = processLocationsIntoTimeline(locations);
      setTimelinePeriods(periods);
    }
  }, [locations, processLocationsIntoTimeline]);

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