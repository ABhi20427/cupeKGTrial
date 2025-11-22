// src/components/Header/Header.jsx (Updated with Route Planner Buttons)

import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from '../LanguageSwitcher/LanguageSwitcher';
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
  const { t } = useTranslation();
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
    <>
      <header className="top-nav">
        <div className="nav-left">
          <div className="logo">{t('header.title')}</div>
          <span className="logo-subtitle">{t('header.subtitle')}</span>
        </div>

        <div className="nav-center">
          <form className="search-form" onSubmit={handleSearchSubmit}>
            <input
              type="text"
              className="search-input"
              placeholder={t('header.search.placeholder')}
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
        </div>

        <div className="nav-right">
          <button
            className="btn-primary"
            onClick={onOpenRoutePreferences}
            title={t('header.buttons.createRoute')}
          >
            <svg viewBox="0 0 24 24" width="18" height="18">
              <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"/>
            </svg>
            <span>Create Route</span>
          </button>

          <button
            className={`btn-ghost ${showNearbyPlaces ? 'active' : ''}`}
            onClick={onToggleNearbyPlaces}
            title={t('header.buttons.nearby')}
            disabled={!userLocation}
          >
            <span>Nearby</span>
          </button>

          <button
            className="btn-ghost-alt"
            onClick={onCulturalIntelligenceToggle}
            title={t('header.buttons.culturalAI')}
          >
            <span>Cultural AI</span>
          </button>

          <div className="nav-divider"></div>

          <LanguageSwitcher />

          <button
            className="theme-toggle"
            onClick={onThemeToggle}
            aria-label={t('header.buttons.themeToggle', { mode: theme === 'light' ? 'dark' : 'light' })}
          >
            {theme === 'light' ? '☾' : '☀'}
          </button>

          <button className="menu-toggle" onClick={toggleMenu}>
            <span className="menu-icon"></span>
          </button>
        </div>
      </header>

      <nav className={`nav-menu ${isMenuOpen ? 'open' : ''}`}>
        <button onClick={() => window.location.href = '/'} className="nav-link active">{t('header.nav.home')}</button>
        <button onClick={() => window.location.href = '/explore'} className="nav-link">{t('header.nav.explore')}</button>
        <button onClick={() => window.location.href = '/routes'} className="nav-link">{t('header.nav.routes')}</button>
        <button onClick={() => window.location.href = '/about'} className="nav-link">{t('header.nav.about')}</button>
        <button onClick={handleContactClick} className="nav-link">{t('header.nav.contact')}</button>
      </nav>

      {/* Contact Popup */}
      {showContactPopup && (
        <div className="contact-popup-overlay" onClick={closeContactPopup}>
          <div className="contact-popup" onClick={(e) => e.stopPropagation()}>
            <div className="contact-popup-header">
              <h3>{t('header.contact.title')}</h3>
              <button className="close-popup-btn" onClick={closeContactPopup}>×</button>
            </div>
            <div className="contact-popup-content">
              <p>{t('header.contact.message')}</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Header;