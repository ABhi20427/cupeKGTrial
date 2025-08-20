import React, { useState, useEffect } from 'react';
import Map from './components/Map/Map';
import Header from './components/Header/Header';
import InfoPanel from './components/InfoPanel/InfoPanel';
import ChatInterface from './components/ChatInterface/ChatInterface';
import Timeline from './components/Timeline/Timeline';
import GraphVisualization from './components/GraphVisualization/GraphVisualization';
import RoutePreferences from './components/RoutePreferences/RoutePreferences';
import NearbyPlaces from './components/NearbyPlaces/NearbyPlaces';
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

  const { selectRoute } = useMapContext();

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

// Replace the handleRouteCreated function in your App.js

  // Replace the handleRouteCreated function in your App.js

  // Replace the handleRouteCreated function in your App.js

const handleRouteCreated = (responseData) => {
  console.log('New personalized route created:', responseData);
  
  // The route object is passed directly
  const route = responseData;
  
  // Debug the route structure
  console.log('Route ID:', route?.id);
  console.log('Route name:', route?.name);
  console.log('Route path:', route?.path);
  console.log('Route locations:', route?.locations);
  console.log('Route color:', route?.color);
  
  // Select the route to display it on the map
  selectRoute(route);
  
  console.log('selectRoute called with:', route);
};

  const toggleNearbyPlaces = () => {
    setShowNearbyPlaces(!showNearbyPlaces);
  };

  const handleNearbyLocationSelect = (location) => {
    console.log('Nearby location selected:', location);
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
