import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import LocationMarker from '../LocationMarker/LocationMarker';
import InfoPanel from '../InfoPanel/InfoPanel';
import RouteVisualizer from '../RouteVisualizer/RouteVisualizer';
import { useMapContext, MapProvider } from '../../context/MapContext';
import './Map.css';

// Set India's coordinates and default zoom level
const INDIA_CENTER = [20.5937, 78.9629];
const DEFAULT_ZOOM = 5;

// AnimatedPane handles smooth transitions when changing map view
const AnimatedPane = () => {
  const map = useMap();
  const { selectedLocation, mapInstance, setMapInstance } = useMapContext();
  
  useEffect(() => {
    // Store map instance in context
    if (map && !mapInstance) {
      setMapInstance(map);
    }
  }, [map, mapInstance, setMapInstance]);
  
  useEffect(() => {
    if (selectedLocation) {
      map.flyTo(
        [selectedLocation.coordinates.lat, selectedLocation.coordinates.lng], 
        10, 
        { 
          animate: true, 
          duration: 1.5 
        }
      );
    }
  }, [selectedLocation, map]);

  return null;
};

const MapContent = () => {
  const { 
    locations, 
    selectedLocation, 
    locationData, 
    isLoading, 
    selectLocation, 
    selectedRoute,
    selectRoute,
    clearSelections,
    resetMapView
  } = useMapContext();
  
  const [isPanelOpen, setIsPanelOpen] = useState(false);

  useEffect(() => {
    setIsPanelOpen(!!locationData);
  }, [locationData]);

  const handleLocationClick = (location) => {
    selectLocation(location);
    // Cultural Intelligence can be opened manually via the button in InfoPanel or Header
  };


  const closePanel = () => {
    setIsPanelOpen(false);
    // Add a slight delay before resetting data
    setTimeout(() => {
      clearSelections();
    }, 300);
  };

  return (
    <div className="map-container">
      <MapContainer
        center={INDIA_CENTER}
        zoom={DEFAULT_ZOOM}
        className="map"
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        />
        
        {locations.map(location => (
          <LocationMarker
            key={location.id}
            location={location}
            isSelected={selectedLocation?.id === location.id}
            onClick={() => handleLocationClick(location)}
          />
        ))}
        
        {selectedRoute && <RouteVisualizer route={selectedRoute} />}
        <AnimatedPane />
      </MapContainer>

      <div className="map-controls">
        <button className="control-btn home-btn" onClick={resetMapView}>
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
        </button>
      </div>

      <InfoPanel 
        isOpen={isPanelOpen}
        isLoading={isLoading}
        locationData={locationData}
        selectedLocation={selectedLocation}
        onClose={closePanel}
      />
    </div>
  );
};

// In your Map.jsx file, find the Map component at the bottom and replace it with this:

const Map = () => {
  // Remove the MapProvider wrapper - use the existing context from App.js
  return <MapContent />;
};

export default Map;