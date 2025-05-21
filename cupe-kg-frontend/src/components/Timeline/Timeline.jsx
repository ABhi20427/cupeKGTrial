// components/Timeline/Timeline.jsx

import React, { useState, useEffect } from 'react';
import { useMapContext } from '../../context/MapContext';
import './Timeline.css';

const Timeline = () => {
  const { locations, selectLocation } = useMapContext();
  const [periods, setPeriods] = useState([]);
  const [activePeriod, setActivePeriod] = useState(null);
  const [isExpanded, setIsExpanded] = useState(true); // Changed to true to start expanded

  useEffect(() => {
    // Extract unique periods from locations and sort them chronologically
    const extractPeriods = () => {
      const uniquePeriods = new Set();
      
      locations.forEach(location => {
        if (location.period) {
          uniquePeriods.add(location.period);
        }
      });
      
      // Convert to array and sort (custom sorting function for historical periods)
      const periodArray = Array.from(uniquePeriods).sort((a, b) => {
        // Extract starting years
        const getStartYear = (period) => {
          const match = period.match(/^(\d+)/);
          if (match) return parseInt(match[1]);
          
          // Handle BCE/CE notation
          if (period.includes('BCE')) return -parseInt(period.match(/(\d+)/)[0]);
          
          // For periods like "6th century BCE"
          if (period.toLowerCase().includes('century bce')) {
            const century = parseInt(period.match(/(\d+)/)[0]);
            return -(century * 100);
          }
          
          // For periods like "5th century CE"
          if (period.toLowerCase().includes('century ce') || period.toLowerCase().includes('century')) {
            const century = parseInt(period.match(/(\d+)/)[0]);
            return century * 100;
          }
          
          return 0; // Default for periods that can't be parsed
        };
        
        return getStartYear(a) - getStartYear(b);
      });
      
      return periodArray;
    };
    
    setPeriods(extractPeriods());

    // Debug: Log the periods
    console.log("Timeline periods:", extractPeriods());
  }, [locations]);

  // Get locations for a specific period
  const getLocationsForPeriod = (period) => {
    return locations.filter(location => location.period === period);
  };

  // Handle period selection
  const handlePeriodClick = (period) => {
    setActivePeriod(period === activePeriod ? null : period);
  };

  // Handle location selection within a period
  const handleLocationClick = (location) => {
    selectLocation(location);
  };

  // Toggle expanded state of timeline
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`timeline-container ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="timeline-header" onClick={toggleExpand}>
        <h3>Time-Based Exploration</h3>
        <button className="expand-button">
          {isExpanded ? '−' : '+'}
        </button>
      </div>
      
      {isExpanded && (
        <div className="timeline-content">
          <div className="timeline">
            {periods.map((period, index) => (
              <div 
                key={index} 
                className={`timeline-period ${activePeriod === period ? 'active' : ''}`}
                onClick={() => handlePeriodClick(period)}
              >
                <div className="period-marker"></div>
                <div className="period-label">{period}</div>
              </div>
            ))}
          </div>
          
          {activePeriod && (
            <div className="period-locations">
              <h4>Locations from {activePeriod}</h4>
              <ul>
                {getLocationsForPeriod(activePeriod).map(location => (
                  <li 
                    key={location.id}
                    onClick={() => handleLocationClick(location)}
                    className="location-item"
                  >
                    <span className="location-name">{location.name}</span>
                    <span className="location-dynasty">{location.dynasty}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Timeline;