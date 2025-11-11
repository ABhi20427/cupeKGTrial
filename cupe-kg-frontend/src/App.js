// cupe-kg-frontend/src/App.js
// FIXED VERSION - Replace your entire App.js with this

import React, { useState, useEffect } from 'react';
import Map from './components/Map/Map';
import Header from './components/Header/Header';
import InfoPanel from './components/InfoPanel/InfoPanel';
import ChatInterface from './components/ChatInterface/ChatInterface';
import Timeline from './components/Timeline/Timeline';
import GraphVisualization from './components/GraphVisualization/GraphVisualization';
import RoutePreferences from './components/RoutePreferences/RoutePreferences';
import NearbyPlaces from './components/NearbyPlaces/NearbyPlaces';
import CulturalIntelligence from './components/CulturalIntelligence/CulturalIntelligence';
import HistoricalView from './components/HistoricalView/HistoricalView';
import { MapProvider, useMapContext } from './context/MapContext';
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary';
import { searchLocations } from './services/api';
import './components/ChatInterface/ChatInterface.css';
import './components/ChatInterface/MessageGroup.css';
import './styles/variables.css';
import './styles/animations.css';

function AppContent() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [theme, setTheme] = useState('light');
  const [isPanelOpen, setIsPanelOpen] = useState(false);
  const [showTimeline, setShowTimeline] = useState(true);
  const [showGraph, setShowGraph] = useState(false);
  const [showRoutePreferences, setShowRoutePreferences] = useState(false);
  const [showNearbyPlaces, setShowNearbyPlaces] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [userInterests, setUserInterests] = useState([]);

  // Cultural Intelligence states
  const [showCulturalIntelligence, setShowCulturalIntelligence] = useState(false);
  const [selectedLocationForCI, setSelectedLocationForCI] = useState(null);
  const [currentRouteForCI, setCurrentRouteForCI] = useState(null);

  // Historical View states
  const [showHistoricalView, setShowHistoricalView] = useState(false);
  const [historicalLocation, setHistoricalLocation] = useState(null);
  const [historicalContext, setHistoricalContext] = useState(null);

  // Get data from MapContext - THIS FIXES THE LOCATIONS ERROR
  const { 
    selectRoute, 
    selectLocation, // Add selectLocation function
    locations,     // This was missing - get locations from context
    routes,        // This was missing - get routes from context
    selectedRoute, // Get current route
    selectedLocation 
  } = useMapContext();

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
        },
        (error) => {
          console.log('Geolocation error:', error);
        }
      );
    }
  }, []);

  // Make data globally available for enhanced route planner
  useEffect(() => {
    if (locations && routes) {
      window.allLocations = locations;
      window.allRoutes = routes;
      window.handleLocationSelected = handleLocationSelected;
      
      return () => {
        delete window.allLocations;
        delete window.allRoutes;
        delete window.handleLocationSelected;
      };
    }
  }, [locations, routes]);

  // Update current route for Cultural Intelligence
  useEffect(() => {
    setCurrentRouteForCI(selectedRoute);
  }, [selectedRoute]);

  const handleSearch = async (query) => {
    if (!query || !query.trim()) {
      setSearchQuery('');
      setSearchResults([]);
      return;
    }

    setSearchQuery(query);
    setIsSearching(true);
    
    try {
      console.log('Searching for:', query);
      const results = await searchLocations(query.trim());
      setSearchResults(results);
      
      // If we have results, show the first result on the map
      if (results.length > 0) {
        const firstResult = results[0];
        // Use MapContext to select the location
        const contextLocation = locations.find(loc => loc.id === firstResult.id);
        if (contextLocation) {
          selectLocation(contextLocation);
        }
      }
      
      console.log('Search completed. Found:', results.length, 'results');
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    document.body.className = theme === 'light' ? 'dark-theme' : 'light-theme';
  };


  const handleGraphNodeClick = (location) => {
    console.log('Graph node clicked:', location);
  };

  const toggleGraphVisualization = () => {
    setShowGraph(!showGraph);
  };

  const openRoutePreferences = () => {
    setShowRoutePreferences(true);
  };

  const closeRoutePreferences = () => {
    setShowRoutePreferences(false);
  };

  const handleRouteCreated = (responseData) => {
    console.log('New personalized route created:', responseData);
    
    const route = responseData;
    
    console.log('Route ID:', route?.id);
    console.log('Route name:', route?.name);
    console.log('Route path:', route?.path);
    console.log('Route locations:', route?.locations);
    console.log('Route color:', route?.color);
    
    selectRoute(route);
    console.log('selectRoute called with:', route);
    
    // Close route preferences after creating route
    setShowRoutePreferences(false);
  };

  const toggleNearbyPlaces = () => {
    setShowNearbyPlaces(!showNearbyPlaces);
  };

  const handleNearbyLocationSelect = (location) => {
    console.log('Nearby location selected:', location);
  };

  // Cultural Intelligence handlers
  const handleLocationSelected = (location) => {
    setSelectedLocationForCI(location);
    setShowCulturalIntelligence(true);
  };

  const handleCulturalInsightClose = () => {
    setShowCulturalIntelligence(false);
    setSelectedLocationForCI(null);
  };

  const handleRecommendSimilar = (connection) => {
    console.log('Recommend similar sites:', connection);
    // Here you could create a new route based on the connection
    // or highlight similar sites on the map
  };

  // Cultural Intelligence handlers
  const handleCulturalIntelligenceToggle = (location = null) => {
    if (location || selectedLocation) {
      const locationToUse = location || selectedLocation;
      setSelectedLocationForCI(locationToUse);
      setCurrentRouteForCI(selectedRoute);
      setShowCulturalIntelligence(true);
    } else {
      // No location selected, use a default or show message
      const defaultLocation = {
        id: 'default',
        name: 'Heritage Site Explorer',
        dynasty: 'Various Dynasties',
        period: 'Ancient to Modern',
        category: 'Cultural Heritage',
        description: 'Explore the rich cultural heritage and historical significance of India\'s monuments, temples, and archaeological sites.',
        tags: ['Heritage', 'Culture', 'History']
      };
      setSelectedLocationForCI(defaultLocation);
      setCurrentRouteForCI(selectedRoute);
      setShowCulturalIntelligence(true);
    }
  };

  // Timeline Historical View handlers
  const handleTimelineLocationSelect = (location, viewMode = 'modern', context = null) => {
    if (viewMode === 'historical' && location && context) {
      setHistoricalLocation(location);
      setHistoricalContext(context);
      setShowHistoricalView(true);
      // Also select the location on the map
      selectLocation(location);
      setIsPanelOpen(true);
    } else if (viewMode === 'modern') {
      setShowHistoricalView(false);
      setHistoricalLocation(null);
      setHistoricalContext(null);
    }
  };

  const handleHistoricalViewClose = () => {
    setShowHistoricalView(false);
    setHistoricalLocation(null);
    setHistoricalContext(null);
  };

  return (
    <div className={`app ${theme}-theme`}>
      <Header 
        onSearch={handleSearch} 
        onThemeToggle={toggleTheme}
        theme={theme}
        onToggleGraph={toggleGraphVisualization}
        showGraph={showGraph}
        onOpenRoutePreferences={openRoutePreferences}
        onToggleNearbyPlaces={toggleNearbyPlaces}
        showNearbyPlaces={showNearbyPlaces}
        userLocation={userLocation}
        onCulturalIntelligenceToggle={handleCulturalIntelligenceToggle}
        isSearching={isSearching}
        searchResults={searchResults}
      />
      
      <Map searchQuery={searchQuery} />
      
      <InfoPanel 
        onOpen={() => setIsPanelOpen(true)}
        onClose={() => setIsPanelOpen(false)}
      />
      
      <ErrorBoundary>
        <ChatInterface isPanelOpen={isPanelOpen} />
      </ErrorBoundary>
      
      <Timeline 
        isVisible={showTimeline}
        onLocationSelect={handleTimelineLocationSelect}
      />
      
      <GraphVisualization
        isVisible={showGraph}
        onNodeClick={handleGraphNodeClick}
        onClose={() => setShowGraph(false)}
      />

      <RoutePreferences
        isVisible={showRoutePreferences}
        onCreateRoute={handleRouteCreated}
        onClose={closeRoutePreferences}
      />

      <NearbyPlaces
        isVisible={showNearbyPlaces}
        currentLocation={userLocation}
        userInterests={userInterests}
        onLocationSelect={handleNearbyLocationSelect}
      />

      {showCulturalIntelligence && (
        <CulturalIntelligence
          selectedLocation={selectedLocationForCI}
          currentRoute={currentRouteForCI}
          isVisible={showCulturalIntelligence}
          onClose={handleCulturalInsightClose}
          onRecommendSimilar={handleRecommendSimilar}
        />
      )}

      <HistoricalView
        location={historicalLocation}
        historicalContext={historicalContext}
        isVisible={showHistoricalView}
        onClose={handleHistoricalViewClose}
      />
    </div>
  );
}

function App() {
  return (
    <MapProvider>
      <AppContent />
    </MapProvider>
  );
}

export default App;