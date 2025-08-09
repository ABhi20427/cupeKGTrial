import React, { createContext, useState, useContext, useEffect } from 'react';
// eslint-disable-next-line no-unused-vars
import { fetchPlaceData, fetchRoutes, fetchLocations } from '../services/api';
import { placeholderData } from '../data/placeholderData';
import { routes as routesData } from '../data/routes';

// Create the context
const MapContext = createContext();

// Custom hook to use the map context
export const useMapContext = () => useContext(MapContext);

// Provider component
export const MapProvider = ({ children }) => {
  // State for locations and routes
  const [locations, setLocations] = useState([]);
  const [routes, setRoutes] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(null);
  const [selectedRoute, setSelectedRoute] = useState(null);
  const [locationData, setLocationData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mapInstance, setMapInstance] = useState(null);

  // Initial data loading
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        // In a real application, uncomment these lines to fetch from API
        // const locationsData = await fetchLocations();
        // const routesData = await fetchRoutes();
        
        // For now, use placeholder data
        const locationsData = [
          { 
            id: 'hampi', 
            name: 'Hampi', 
            coordinates: { lat: 15.3350, lng: 76.4600 },
            category: 'historical' 
          },
          { 
            id: 'delhi', 
            name: 'Delhi', 
            coordinates: { lat: 28.7041, lng: 77.1025 },
            category: 'cultural'  
          },
          { 
            id: 'konark', 
            name: 'Konark', 
            coordinates: { lat: 19.8876, lng: 86.0945 },
            category: 'religious'  
          }
        ];
        
        setLocations(locationsData);
        setRoutes(routesData);
      } catch (err) {
        setError('Failed to load initial data');
        console.error('Error loading initial data:', err);
      }
    };
    
    loadInitialData();
  }, []);

  // Function to handle location selection
  const selectLocation = async (location) => {
    setIsLoading(true);
    setSelectedLocation(location);
    
    try {
      // In a real application, uncomment to fetch from API
      // const data = await fetchPlaceData(location.id);
      
      // For now, use placeholder data with a simulated delay
      setTimeout(() => {
        setLocationData(placeholderData[location.id]);
        setIsLoading(false);
      }, 500);
    } catch (err) {
      setError('Failed to load location data');
      console.error('Error fetching location data:', err);
      setIsLoading(false);
    }
  };

  // Function to select a route
  const selectRoute = (routeId) => {
    const route = routes.find(r => r.id === routeId);
    setSelectedRoute(route);
  };

  // Function to clear selections
  const clearSelections = () => {
    setSelectedLocation(null);
    setSelectedRoute(null);
    setLocationData(null);
  };

  // Function to pan map to a location
  const panToLocation = (location) => {
    if (mapInstance && location) {
      mapInstance.flyTo(
        [location.coordinates.lat, location.coordinates.lng],
        10,
        {
          animate: true,
          duration: 1.5
        }
      );
    }
  };

  // Function to reset map view
  const resetMapView = () => {
    if (mapInstance) {
      const INDIA_CENTER = [20.5937, 78.9629];
      const DEFAULT_ZOOM = 5;
      
      mapInstance.flyTo(
        INDIA_CENTER,
        DEFAULT_ZOOM,
        {
          animate: true,
          duration: 1.5
        }
      );
      
      clearSelections();
    }
  };

  // Create the value object
  const contextValue = {
    locations,
    routes,
    selectedLocation,
    selectedRoute,
    locationData,
    isLoading,
    error,
    mapInstance,
    setMapInstance,
    selectLocation,
    selectRoute,
    clearSelections,
    panToLocation,
    resetMapView
  };

  return (
    <MapContext.Provider value={contextValue}>
      {children}
    </MapContext.Provider>
  );
};

export default MapContext;