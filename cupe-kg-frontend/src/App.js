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
import { MapProvider, useMapContext } from './context/MapContext';
import './components/ChatInterface/ChatInterface.css';
import './components/ChatInterface/MessageGroup.css';
import './styles/variables.css';
import './styles/animations.css';

function AppContent() {
  const [searchQuery, setSearchQuery] = useState('');
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

  // Get data from MapContext - THIS FIXES THE LOCATIONS ERROR
  const { 
    selectRoute, 
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

  const handleSearch = (query) => {
    setSearchQuery(query);
    console.log('Searching for:', query);
  };

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
    document.body.className = theme === 'light' ? 'dark-theme' : 'light-theme';
  };

  const handleTimelineLocationSelect = (location) => {
    console.log('Timeline location selected:', location);
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
        tags: ['Heritage', 'Culture', 'History']
      };
      setSelectedLocationForCI(defaultLocation);
      setCurrentRouteForCI(selectedRoute);
      setShowCulturalIntelligence(true);
    }
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
      />
      
      <Map searchQuery={searchQuery} />
      
      <InfoPanel 
        onOpen={() => setIsPanelOpen(true)}
        onClose={() => setIsPanelOpen(false)}
      />
      
      <ChatInterface isPanelOpen={isPanelOpen} />
      
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