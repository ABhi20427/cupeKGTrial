// src/components/RoutePreferences/RoutePreferences.jsx

import React, { useState, useEffect } from 'react';
import './RoutePreferences.css';

const RoutePreferences = ({ onCreateRoute, onClose, isVisible }) => {
  const [preferences, setPreferences] = useState({
    interests: [],
    max_travel_days: 7,
    budget_range: 'medium',
    transport_mode: 'car',
    start_location: null,
    preferred_regions: [],
    max_distance_km: 500,
    preferred_periods: [],
    preferred_dynasties: [],
    crowd_preference: 'medium',
    accommodation_type: 'medium',
    cultural_activities: [],
    accessibility_required: false,
    physical_difficulty_preference: 'medium'
  });

  const [suggestions, setSuggestions] = useState({
    available_interests: [],
    available_periods: [],
    available_dynasties: [],
    available_categories: []
  });
  const [currentLocation, setCurrentLocation] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isVisible) {
      fetchSuggestions();
      getUserLocation();
    }
  }, [isVisible]);

  const fetchSuggestions = async () => {
    try {
      const response = await fetch('/api/preference-suggestions');
      if (response.ok) {
        const data = await response.json();
        console.log('Suggestions received:', data); // Debug log
        setSuggestions(data);
      } else {
        console.error('Failed to fetch suggestions');
        // Fallback data
        setSuggestions({
          available_interests: ['historical', 'religious', 'architectural', 'cultural'],
          available_periods: ['Ancient', 'Medieval', 'Mughal', 'Colonial', 'Modern'],
          available_dynasties: ['Mughal Empire', 'Vijayanagara Empire', 'Mauryan Empire', 'Gupta Empire'],
          available_categories: ['historical', 'religious', 'cultural']
        });
      }
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      // Fallback data
      setSuggestions({
        available_interests: ['historical', 'religious', 'architectural', 'cultural'],
        available_periods: ['Ancient', 'Medieval', 'Mughal', 'Colonial', 'Modern'],
        available_dynasties: ['Mughal Empire', 'Vijayanagara Empire', 'Mauryan Empire', 'Gupta Empire'],
        available_categories: ['historical', 'religious', 'cultural']
      });
    }
  };

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setCurrentLocation(location);
          setPreferences(prev => ({
            ...prev,
            start_location: location
          }));
        },
        (error) => {
          console.log('Geolocation error:', error);
        }
      );
    }
  };

  const handleInterestToggle = (interest) => {
    setPreferences(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const handleMultiSelectToggle = (field, value) => {
    console.log(`Toggling ${field} with value:`, value); // Debug log
    setPreferences(prev => {
      const currentArray = prev[field] || [];
      const newArray = currentArray.includes(value)
        ? currentArray.filter(item => item !== value)
        : [...currentArray, value];

      console.log(`Updated ${field}:`, newArray); // Debug log

      return {
        ...prev,
        [field]: newArray
      };
    });
  };

  const handleInputChange = (field, value) => {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSubmit = async () => {
    if (preferences.interests.length === 0) {
      alert('Please select at least one interest');
      return;
    }

    console.log('Submitting preferences:', preferences); // Debug log

    setIsLoading(true);
    try {
      const response = await fetch('/api/personalized-route-advanced', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(preferences)
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Route created:', data); // Debug log
        onCreateRoute(data.route);
        onClose();
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error creating route:', error);
      alert('Failed to create personalized route');
    } finally {
      setIsLoading(false);
    }
  };

  const interestDisplayNames = {
    'historical': 'Historical Sites',
    'religious': 'Religious Places',
    'architectural': 'Architecture',
    'cultural': 'Cultural Heritage',
    'archaeological': 'Archaeological Sites',
    'royal_heritage': 'Royal Heritage',
    'ancient_temples': 'Ancient Temples',
    'forts_palaces': 'Forts & Palaces',
    'unesco_sites': 'UNESCO Sites'
  };

  if (!isVisible) return null;

  return (
    <div className="route-preferences-overlay">
      <div className="route-preferences-modal">
        <div className="preferences-header">
          <h2>Create Your Personalized Route</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="preferences-content">
          {/* Interests Section */}
          <div className="preference-section">
            <h3>What interests you? <span className="required">*</span></h3>
            <div className="interests-grid">
              {suggestions.available_interests?.map(interest => (
                <button
                  key={interest}
                  className={`interest-btn ${preferences.interests.includes(interest) ? 'selected' : ''}`}
                  onClick={() => handleInterestToggle(interest)}
                >
                  {interestDisplayNames[interest] || interest}
                </button>
              ))}
            </div>
          </div>

          {/* Travel Duration */}
          <div className="preference-section">
            <h3>Travel Duration</h3>
            <div className="input-group">
              <label>Maximum travel days:</label>
              <input
                type="number"
                min="1"
                max="30"
                value={preferences.max_travel_days}
                onChange={(e) => handleInputChange('max_travel_days', parseInt(e.target.value))}
              />
            </div>
          </div>

          {/* Budget & Transport */}
          <div className="preference-section">
            <div className="two-column">
              <div className="input-group">
                <label>Budget Range:</label>
                <select
                  value={preferences.budget_range}
                  onChange={(e) => handleInputChange('budget_range', e.target.value)}
                >
                  <option value="low">Budget-friendly</option>
                  <option value="medium">Moderate</option>
                  <option value="high">Luxury</option>
                </select>
              </div>
              <div className="input-group">
                <label>Transport Mode:</label>
                <select
                  value={preferences.transport_mode}
                  onChange={(e) => handleInputChange('transport_mode', e.target.value)}
                >
                  <option value="car">Car</option>
                  <option value="train">Train</option>
                  <option value="bus">Bus</option>
                  <option value="flight">Flight</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
            </div>
          </div>

          {/* Historical Preferences - Safe Rendering */}
          <div className="preference-section">
            <h3>Historical Preferences</h3>
            <div className="two-column">
              <div className="input-group">
                <label>Preferred Periods:</label>
                <div className="multi-select">
                  {suggestions.available_periods && suggestions.available_periods.length > 0 ? (
                    suggestions.available_periods.slice(0, 8).map(period => (
                      <label key={period} className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={preferences.preferred_periods.includes(period)}
                          onChange={() => handleMultiSelectToggle('preferred_periods', period)}
                        />
                        {period}
                      </label>
                    ))
                  ) : (
                    <div className="no-data">No historical periods available</div>
                  )}
                </div>
              </div>
              <div className="input-group">
                <label>Preferred Dynasties:</label>
                <div className="multi-select">
                  {suggestions.available_dynasties && suggestions.available_dynasties.length > 0 ? (
                    suggestions.available_dynasties.slice(0, 8).map(dynasty => (
                      <label key={dynasty} className="checkbox-label">
                        <input
                          type="checkbox"
                          checked={preferences.preferred_dynasties.includes(dynasty)}
                          onChange={() => handleMultiSelectToggle('preferred_dynasties', dynasty)}
                        />
                        {dynasty}
                      </label>
                    ))
                  ) : (
                    <div className="no-data">No dynasties available</div>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Distance & Location */}
          <div className="preference-section">
            <h3>Location Preferences</h3>
            <div className="input-group">
              <label>Maximum distance from start (km):</label>
              <input
                type="number"
                min="50"
                max="2000"
                step="50"
                value={preferences.max_distance_km}
                onChange={(e) => handleInputChange('max_distance_km', parseInt(e.target.value))}
              />
            </div>
            {currentLocation && (
              <div className="location-info">
                <p>📍 Using your current location as starting point</p>
                <small>Lat: {currentLocation.lat.toFixed(4)}, Lng: {currentLocation.lng.toFixed(4)}</small>
              </div>
            )}
          </div>

          {/* Experience Preferences */}
          <div className="preference-section">
            <h3>Experience Preferences</h3>
            <div className="three-column">
              <div className="input-group">
                <label>Crowd Level:</label>
                <select
                  value={preferences.crowd_preference}
                  onChange={(e) => handleInputChange('crowd_preference', e.target.value)}
                >
                  <option value="low">Peaceful</option>
                  <option value="medium">Moderate</option>
                  <option value="high">Bustling</option>
                </select>
              </div>
              <div className="input-group">
                <label>Accommodation:</label>
                <select
                  value={preferences.accommodation_type}
                  onChange={(e) => handleInputChange('accommodation_type', e.target.value)}
                >
                  <option value="budget">Budget</option>
                  <option value="medium">Comfortable</option>
                  <option value="luxury">Luxury</option>
                </select>
              </div>
              <div className="input-group">
                <label>Physical Difficulty:</label>
                <select
                  value={preferences.physical_difficulty_preference}
                  onChange={(e) => handleInputChange('physical_difficulty_preference', e.target.value)}
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Moderate</option>
                  <option value="difficult">Challenging</option>
                </select>
              </div>
            </div>
          </div>

          {/* Accessibility */}
          <div className="preference-section">
            <div className="input-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.accessibility_required}
                  onChange={(e) => handleInputChange('accessibility_required', e.target.checked)}
                />
                Accessibility features required
              </label>
            </div>
          </div>

          {/* Cultural Activities */}
          <div className="preference-section">
            <h3>Cultural Activities (Optional)</h3>
            <div className="activities-grid">
              {['festivals', 'local_food', 'crafts', 'music', 'dance', 'markets'].map(activity => (
                <button
                  key={activity}
                  className={`activity-btn ${preferences.cultural_activities.includes(activity) ? 'selected' : ''}`}
                  onClick={() => handleMultiSelectToggle('cultural_activities', activity)}
                >
                  {activity.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Debug Info (can remove in production) */}
          <div className="preference-section" style={{fontSize: '12px', color: '#666'}}>
            <details>
              <summary>Debug Info (Click to expand)</summary>
              <pre>{JSON.stringify({
                'Selected Periods': preferences.preferred_periods,
                'Selected Dynasties': preferences.preferred_dynasties,
                'Available Periods': suggestions.available_periods,
                'Available Dynasties': suggestions.available_dynasties
              }, null, 2)}</pre>
            </details>
          </div>
        </div>

        <div className="preferences-footer">
          <button className="cancel-btn" onClick={onClose}>Cancel</button>
          <button 
            className="create-route-btn" 
            onClick={handleSubmit}
            disabled={isLoading || preferences.interests.length === 0}
          >
            {isLoading ? 'Creating Route...' : 'Create My Route'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default RoutePreferences;
