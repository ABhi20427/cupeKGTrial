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

    let periods = [];
    const rangeMatch = periodString.match(dateRangeRegex);

    if (rangeMatch) {
      const [_, start, end] = rangeMatch;
      periods.push({
        start: parseInt(start),
        end: parseInt(end),
        original: periodString
      });
    } else {
      const singleMatch = periodString.match(singleDateRegex);
      if (singleMatch) {
        const [_, year] = singleMatch;
        const yearNum = parseInt(year);
        periods.push({
          start: yearNum,
          end: yearNum,
          original: periodString
        });
      }
    }

    return periods;
  }, []);

  const processLocationsIntoTimeline = useCallback((locations) => {
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

    return Array.from(periodMap.values())
      .sort((a, b) => a.start - b.start)
      .map(period => ({
        ...period,
        dynasties: Array.from(period.dynasties)
      }));
  }, [extractPeriodInfo]);

  // Process locations into timeline periods
  useEffect(() => {
    if (locations.length > 0) {
      const periods = processLocationsIntoTimeline(locations);
      setTimelinePeriods(periods);
    }
  }, [locations, processLocationsIntoTimeline]);

  const handlePeriodClick = useCallback((period) => {
    setSelectedPeriod(selectedPeriod === period ? null : period);
  }, [selectedPeriod]);

  const handleLocationClick = useCallback((location) => {
    selectLocation(location);
    if (onLocationSelect) {
      onLocationSelect(location);
    }
  }, [selectLocation, onLocationSelect]);

  const toggleExpansion = useCallback(() => {
    setIsExpanded(!isExpanded);
  }, [isExpanded]);

  if (!isVisible || timelinePeriods.length === 0) {
    return null;
  }

  return (
    <div className={`timeline-container ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="timeline-header" onClick={toggleExpansion}>
        <h3>Historical Timeline</h3>
        <span className={`expand-icon ${isExpanded ? 'expanded' : ''}`}>
          {isExpanded ? '▼' : '▲'}
        </span>
      </div>

      {isExpanded && (
        <div className="timeline-content">
          <div className="timeline-periods">
            {timelinePeriods.map((period, index) => (
              <div 
                key={`${period.start}-${period.end}`}
                className={`timeline-period ${selectedPeriod === period ? 'selected' : ''}`}
                onClick={() => handlePeriodClick(period)}
              >
                <div className="period-header">
                  <span className="period-date">
                    {period.start === period.end 
                      ? `${period.start} CE`
                      : `${period.start} CE - ${period.end} CE`
                    }
                  </span>
                  <span className="location-count">
                    {period.locations.length} location{period.locations.length !== 1 ? 's' : ''}
                  </span>
                </div>

                {selectedPeriod === period && (
                  <div className="period-details">
                    {period.dynasties.length > 0 && (
                      <div className="period-dynasties">
                        <h4>Dynasties:</h4>
                        <ul>
                          {period.dynasties.map(dynasty => (
                            <li key={dynasty}>{dynasty}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                    
                    <div className="period-locations">
                      <h4>Locations:</h4>
                      <ul>
                        {period.locations.map(location => (
                          <li 
                            key={location.id}
                            className={`location-item ${selectedLocation?.id === location.id ? 'selected' : ''}`}
                            onClick={(e) => {
                              e.stopPropagation();
                              handleLocationClick(location);
                            }}
                          >
                            {location.name}
                            <span className="location-category">{location.category}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Timeline;
