// src/components/Header/Header.jsx (Updated with Route Planner Buttons)

import React, { useState, useEffect } from 'react';
import './Header.css';

const Header = ({ 
  onSearch, 
  onThemeToggle, 
  theme,
  onOpenRoutePreferences,
  onToggleNearbyPlaces,
  showNearbyPlaces,
  userLocation,
  onCulturalIntelligenceToggle,
  isSearching = false,
  searchResults = []
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showContactPopup, setShowContactPopup] = useState(false);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm);
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleContactClick = () => {
    setShowContactPopup(true);
    setIsMenuOpen(false); // Close mobile menu if open
  };

  const closeContactPopup = () => {
    setShowContactPopup(false);
  };

  // Handle Escape key to close popup
  useEffect(() => {
    const handleEscapeKey = (event) => {
      if (event.key === 'Escape' && showContactPopup) {
        closeContactPopup();
      }
    };

    document.addEventListener('keydown', handleEscapeKey);
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [showContactPopup]);

  return (
    <header className="app-header">
      <div className="header-container">
        <div className="logo-container">
          <h1 className="logo">CuPe-KG</h1>
          <span className="logo-subtitle">Cultural Perspectives Knowledge Graph</span>
        </div>

        <form className="search-form" onSubmit={handleSearchSubmit}>
          <input
            type="text"
            className="search-input"
            placeholder="Search for locations, routes, or cultural elements..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit" className={`search-button ${isSearching ? 'searching' : ''}`} disabled={isSearching}>
            {isSearching ? (
              <svg viewBox="0 0 24 24" className="search-icon spinning">
                <path d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z"/>
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" className="search-icon">
                <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
              </svg>
            )}
          </button>
        </form>

        <div className="header-controls">
          {/* NEW: Route Planner Button */}
          <button 
            className="control-button route-planner-btn"
            onClick={onOpenRoutePreferences}
            title="Create Personalized Route"
          >
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12 2L13.09 8.26L22 9L13.09 9.74L12 16L10.91 9.74L2 9L10.91 8.26L12 2M12 12L11.47 14.76L9 15L11.47 15.24L12 18L12.53 15.24L15 15L12.53 14.76L12 12Z"/>
            </svg>
            <span>Create Route</span>
          </button>

          {/* NEW: Nearby Places Button */}
          <button 
            className={`control-button nearby-btn ${showNearbyPlaces ? 'active' : ''}`}
            onClick={onToggleNearbyPlaces}
            title="Find Nearby Places"
            disabled={!userLocation}
          >
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z"/>
            </svg>
            <span>Nearby</span>
            {!userLocation && <span className="location-indicator">📍</span>}
          </button>

          {/* Cultural Intelligence Button */}
          <button 
            className="control-button cultural-ai-btn"
            onClick={onCulturalIntelligenceToggle}
            title="Cultural Intelligence Analysis"
          >
            <svg viewBox="0 0 24 24" width="20" height="20">
              <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/>
            </svg>
            <span>Cultural AI</span>
          </button>

          <button 
            className="theme-toggle" 
            onClick={onThemeToggle}
            aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? (
              <svg viewBox="0 0 24 24" className="moon-icon">
                <path d="M12,3c-4.97,0-9,4.03-9,9s4.03,9,9,9s9-4.03,9-9c0-0.46-0.04-0.92-0.1-1.36c-0.98,1.37-2.58,2.26-4.4,2.26 c-2.98,0-5.4-2.42-5.4-5.4c0-1.81,0.89-3.42,2.26-4.4C12.92,3.04,12.46,3,12,3L12,3z"/>
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" className="sun-icon">
                <path d="M12,7c-2.76,0-5,2.24-5,5s2.24,5,5,5s5-2.24,5-5S14.76,7,12,7L12,7z M2,13h2c0.55,0,1-0.45,1-1 s-0.45-1-1-1H2c-0.55,0-1,0.45-1,1S1.45,13,2,13z M20,13h2c0.55,0,1-0.45,1-1s-0.45-1-1-1h-2c-0.55,0-1,0.45-1,1 S19.45,13,20,13z M11,2v2c0,0.55,0.45,1,1,1s1-0.45,1-1V2c0-0.55-0.45-1-1-1S11,1.45,11,2z M11,20v2c0,0.55,0.45,1,1,1 s1-0.45,1-1v-2c0-0.55-0.45-1-1-1S11,19.45,11,20z M5.99,4.58c-0.39-0.39-1.03-0.39-1.41,0 c-0.39,0.39-0.39,1.03,0,1.41l1.06,1.06c0.39,0.39,1.03,0.39,1.41,0s0.39-1.03,0-1.41L5.99,4.58z M18.36,16.95 c-0.39-0.39-1.03-0.39-1.41,0c-0.39,0.39-0.39,1.03,0,1.41l1.06,1.06c0.39,0.39,1.03,0.39,1.41,0c0.39-0.39,0.39-1.03,0-1.41 L18.36,16.95z M19.42,5.99c0.39-0.39,0.39-1.03,0-1.41c-0.39-0.39-1.03-0.39-1.41,0l-1.06,1.06c-0.39,0.39-0.39,1.03,0,1.41 s1.03,0.39,1.41,0L19.42,5.99z M7.05,18.36c0.39-0.39,0.39-1.03,0-1.41c-0.39-0.39-1.03-0.39-1.41,0l-1.06,1.06 c-0.39,0.39-0.39,1.03,0,1.41s1.03,0.39,1.41,0L7.05,18.36z"/>
              </svg>
            )}
          </button>

          <button className="menu-toggle" onClick={toggleMenu}>
            <span className="menu-icon"></span>
          </button>
        </div>

        {/* NEW: Location Status */}
        {userLocation && (
          <div className="location-status">
            <span className="location-dot"></span>
            <small>Location detected</small>
          </div>
        )}
      </div>

      <nav className={`main-nav ${isMenuOpen ? 'open' : ''}`}>
        <ul className="nav-list">
          <li className="nav-item">
            <button onClick={() => window.location.href = '/'} className="nav-link active">Home</button>
          </li>
          <li className="nav-item">
            <button onClick={() => window.location.href = '/explore'} className="nav-link">Explore</button>
          </li>
          <li className="nav-item">
            <button onClick={() => window.location.href = '/routes'} className="nav-link">Routes</button>
          </li>
          <li className="nav-item">
            <button onClick={() => window.location.href = '/about'} className="nav-link">About</button>
          </li>
          <li className="nav-item">
            <button onClick={handleContactClick} className="nav-link">Contact</button>
          </li>
        </ul>
      </nav>
      
      {/* Contact Popup */}
      {showContactPopup && (
        <div className="contact-popup-overlay" onClick={closeContactPopup}>
          <div className="contact-popup" onClick={(e) => e.stopPropagation()}>
            <div className="contact-popup-header">
              <h3>Contact Us</h3>
              <button className="close-popup-btn" onClick={closeContactPopup}>×</button>
            </div>
            <div className="contact-popup-content">
              <p>I don't want you to contact us</p>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;