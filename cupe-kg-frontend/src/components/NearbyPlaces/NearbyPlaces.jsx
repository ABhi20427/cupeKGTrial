// src/components/NearbyPlaces/NearbyPlaces.jsx

import React, { useState, useEffect } from 'react';
import './NearbyPlaces.css';

const NearbyPlaces = ({ currentLocation, userInterests, onLocationSelect, isVisible }) => {
  const [nearbyPlaces, setNearbyPlaces] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [radius, setRadius] = useState(50);
  const [selectedInterests, setSelectedInterests] = useState(userInterests || []);

  useEffect(() => {
    if (isVisible && currentLocation) {
      fetchNearbyPlaces();
    }
  }, [isVisible, currentLocation, radius, selectedInterests]);

  const fetchNearbyPlaces = async () => {
    if (!currentLocation) return;

    setIsLoading(true);
    try {
      const interestsParam = selectedInterests.length > 0 
        ? `&interests=${selectedInterests.join(',')}`
        : '';
      
      const response = await fetch(
        `/api/nearby-places?lat=${currentLocation.lat}&lng=${currentLocation.lng}&radius=${radius}${interestsParam}`
      );
      
      if (response.ok) {
        const data = await response.json();
        setNearbyPlaces(data.nearby_places);
      } else {
        console.error('Failed to fetch nearby places');
      }
    } catch (error) {
      console.error('Error fetching nearby places:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInterestToggle = (interest) => {
    setSelectedInterests(prev => 
      prev.includes(interest)
        ? prev.filter(i => i !== interest)
        : [...prev, interest]
    );
  };

  const handleLocationClick = (place) => {
    onLocationSelect(place.location);
  };

  const getDistanceColor = (distance) => {
    if (distance < 20) return '#10b981'; // Green
    if (distance < 40) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getInterestMatchBadge = (score) => {
    if (score > 0.8) return { text: 'Perfect Match', color: '#10b981' };
    if (score > 0.6) return { text: 'Great Match', color: '#3b82f6' };
    if (score > 0.4) return { text: 'Good Match', color: '#f59e0b' };
    return { text: 'Partial Match', color: '#6b7280' };
  };

  const availableInterests = [
    'historical', 'religious', 'architectural', 'cultural', 
    'archaeological', 'royal_heritage', 'ancient_temples', 
    'forts_palaces', 'unesco_sites'
  ];

  if (!isVisible) return null;

  return (
    <div className="nearby-places-panel">
      <div className="panel-header">
        <h3>🎯 Nearby Historical Places</h3>
        <div className="location-info">
          📍 {currentLocation ? 
            `${currentLocation.lat.toFixed(3)}, ${currentLocation.lng.toFixed(3)}` : 
            'No location set'}
        </div>
      </div>

      <div className="filters-section">
        <div className="radius-control">
          <label>Search Radius: {radius} km</label>
          <input
            type="range"
            min="10"
            max="200"
            step="10"
            value={radius}
            onChange={(e) => setRadius(parseInt(e.target.value))}
            className="radius-slider"
          />
        </div>

        <div className="interests-filter">
          <label>Filter by Interests:</label>
          <div className="interests-chips">
            {availableInterests.map(interest => (
              <button
                key={interest}
                className={`interest-chip ${selectedInterests.includes(interest) ? 'selected' : ''}`}
                onClick={() => handleInterestToggle(interest)}
              >
                {interest.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="places-list">
        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Discovering nearby places...</p>
          </div>
        )}

        {!isLoading && nearbyPlaces.length === 0 && currentLocation && (
          <div className="empty-state">
            <div className="empty-icon">🏛️</div>
            <p>No historical places found within {radius}km</p>
            <small>Try increasing the search radius or adjusting your interests</small>
          </div>
        )}

        {!isLoading && nearbyPlaces.map((place, index) => {
          const matchBadge = getInterestMatchBadge(place.interest_match);
          
          return (
            <div 
              key={index} 
              className="place-card"
              onClick={() => handleLocationClick(place)}
            >
              <div className="place-header">
                <h4>{place.location.name}</h4>
                <div className="place-badges">
                  <span 
                    className="distance-badge"
                    style={{ backgroundColor: getDistanceColor(place.distance_km) }}
                  >
                    {place.distance_km} km
                  </span>
                  {selectedInterests.length > 0 && (
                    <span 
                      className="match-badge"
                      style={{ backgroundColor: matchBadge.color }}
                    >
                      {matchBadge.text}
                    </span>
                  )}
                </div>
              </div>

              <p className="place-description">
                {place.location.description?.length > 120 
                  ? `${place.location.description.substring(0, 120)}...`
                  : place.location.description}
              </p>

              <div className="place-details">
                {place.location.period && (
                  <div className="detail-item">
                    <span className="detail-label">Period:</span>
                    <span className="detail-value">{place.location.period}</span>
                  </div>
                )}
                {place.location.dynasty && (
                  <div className="detail-item">
                    <span className="detail-label">Dynasty:</span>
                    <span className="detail-value">{place.location.dynasty}</span>
                  </div>
                )}
                {place.location.category && (
                  <div className="detail-item">
                    <span className="detail-label">Type:</span>
                    <span className="detail-value">{place.location.category}</span>
                  </div>
                )}
              </div>

              {place.location.tags && place.location.tags.length > 0 && (
                <div className="place-tags">
                  {place.location.tags.slice(0, 3).map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                  ))}
                  {place.location.tags.length > 3 && (
                    <span className="tag more">+{place.location.tags.length - 3}</span>
                  )}
                </div>
              )}

              <div className="place-actions">
                <button className="view-details-btn">
                  View Details
                </button>
                <button className="add-to-route-btn">
                  Add to Route
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {nearbyPlaces.length > 0 && (
        <div className="panel-footer">
          <p>Found {nearbyPlaces.length} places within {radius}km</p>
          <button className="create-route-from-nearby" onClick={() => {
            // Create route from selected nearby places
            const routeData = {
              interests: selectedInterests,
              max_travel_days: Math.ceil(nearbyPlaces.length / 3),
              start_location: currentLocation,
              max_distance_km: radius
            };
            // Trigger route creation with these places
          }}>
            Create Route from These Places
          </button>
        </div>
      )}
    </div>
  );
};

export default NearbyPlaces;