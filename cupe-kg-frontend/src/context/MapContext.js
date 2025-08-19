// src/context/MapContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { fetchPlaceData, fetchRoutes, fetchLocations, checkAPIHealth } from '../services/api';
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
  const [apiConnected, setApiConnected] = useState(false);

  // Initial data loading
  useEffect(() => {
    const loadInitialData = async () => {
      setIsLoading(true);
      setError(null);
      
      try {
        // First check if API is healthy
        console.log('Checking API health...');
        await checkAPIHealth();
        setApiConnected(true);
        console.log('API is healthy, loading data...');
        
        // Load locations from backend
        const locationsData = await fetchLocations();
        console.log('Received locations from backend:', locationsData);
        
        // Transform backend data to frontend format
        const transformedLocations = locationsData.map(location => ({
          id: location.id,
          name: location.name,
          coordinates: location.coordinates,
          category: location.category,
          description: location.description,
          dynasty: location.dynasty,
          period: location.period,
          tags: location.tags || []
        }));
        
        setLocations(transformedLocations);
        console.log('Transformed locations:', transformedLocations);
        
        // Try to load routes from backend, fallback to local data
        try {
          const routesData = await fetchRoutes();
          setRoutes(routesData);
          console.log('Loaded routes from backend:', routesData);
        } catch (routeError) {
          console.warn('Could not load routes from backend, using fallback data:', routeError);
          setRoutes(routesData); // Use local fallback data
        }
        
      } catch (err) {
        console.error('Error loading data from backend:', err);
        setError('Failed to connect to backend. Using fallback data.');
        setApiConnected(false);
        
        // Fallback to original placeholder data
        const fallbackLocations = [
          { 
            id: 'hampi', 
            name: 'Hampi', 
            coordinates: { lat: 15.3350, lng: 76.4600 },
            category: 'historical',
            description: 'Ancient capital of the Vijayanagara Empire'
          },
          { 
            id: 'delhi', 
            name: 'Delhi', 
            coordinates: { lat: 28.7041, lng: 77.1025 },
            category: 'cultural',
            description: 'Historic capital with layers of civilization'
          },
          { 
            id: 'konark', 
            name: 'Konark', 
            coordinates: { lat: 19.8876, lng: 86.0945 },
            category: 'religious',
            description: '13th-century Sun Temple designed as a chariot'
          }
        ];
        
        setLocations(fallbackLocations);
        setRoutes(routesData);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadInitialData();
  }, []);

  // Function to handle location selection
  const selectLocation = async (location) => {
    setIsLoading(true);
    setSelectedLocation(location);
    setError(null);
    
    try {
      if (apiConnected) {
        console.log('Fetching detailed data for location:', location.id);
        const data = await fetchPlaceData(location.id);
        console.log('Received detailed location data:', data);
        setLocationData(data);
      } else {
        // Fallback to basic location data
        console.log('API not connected, using basic location data');
        setLocationData({
          id: location.id,
          name: location.name,
          description: location.description,
          history: 'Detailed history will be available when connected to the backend.',
          culturalFacts: ['Rich cultural heritage site'],
          legends: [],
          tags: location.tags || []
        });
      }
    } catch (err) {
      console.error('Error fetching location data:', err);
      setError('Failed to load detailed location information');
      
      // Set basic fallback data
      setLocationData({
        id: location.id,
        name: location.name,
        description: location.description,
        history: 'Unable to load detailed information at this time.',
        culturalFacts: [],
        legends: [],
        tags: []
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle route selection
  const selectRoute = (route) => {
    setSelectedRoute(route);
    setSelectedLocation(null); // Clear location selection when route is selected
    setLocationData(null);
  };

  // Function to clear all selections
  const clearSelections = () => {
    setSelectedLocation(null);
    setSelectedRoute(null);
    setLocationData(null);
  };

  // Function to reset map view to India
  const resetMapView = () => {
    if (mapInstance) {
      mapInstance.setView([20.5937, 78.9629], 5); // India center coordinates
    }
    clearSelections();
  };

  // Function to search locations
  const searchLocations = (query) => {
    if (!query.trim()) return locations;
    
    const searchTerm = query.toLowerCase();
    return locations.filter(location => 
      location.name.toLowerCase().includes(searchTerm) ||
      location.description.toLowerCase().includes(searchTerm) ||
      location.category.toLowerCase().includes(searchTerm) ||
      (location.dynasty && location.dynasty.toLowerCase().includes(searchTerm)) ||
      (location.tags && location.tags.some(tag => tag.toLowerCase().includes(searchTerm)))
    );
  };

  // Function to filter locations by category
  const filterLocationsByCategory = (category) => {
    if (!category) return locations;
    return locations.filter(location => location.category === category);
  };

  // Function to get available categories
  const getCategories = () => {
    const categories = [...new Set(locations.map(loc => loc.category))];
    return categories.sort();
  };

  // Function to get available dynasties
  const getDynasties = () => {
    const dynasties = [...new Set(locations.map(loc => loc.dynasty).filter(Boolean))];
    return dynasties.sort();
  };

  // Function to refresh data from backend
  const refreshData = async () => {
    setIsLoading(true);
    try {
      await checkAPIHealth();
      const locationsData = await fetchLocations();
      const transformedLocations = locationsData.map(location => ({
        id: location.id,
        name: location.name,
        coordinates: location.coordinates,
        category: location.category,
        description: location.description,
        dynasty: location.dynasty,
        period: location.period,
        tags: location.tags || []
      }));
      setLocations(transformedLocations);
      setApiConnected(true);
      setError(null);
      console.log('Data refreshed successfully');
    } catch (err) {
      console.error('Error refreshing data:', err);
      setError('Failed to refresh data from backend');
    } finally {
      setIsLoading(false);
    }
  };

  const value = {
    // State
    locations,
    routes,
    selectedLocation,
    selectedRoute,
    locationData,
    isLoading,
    error,
    mapInstance,
    apiConnected,
    
    // Setters
    setMapInstance,
    
    // Actions
    selectLocation,
    selectRoute,
    clearSelections,
    resetMapView,
    searchLocations,
    filterLocationsByCategory,
    getCategories,
    getDynasties,
    refreshData
  };

  return (
    <MapContext.Provider value={value}>
      {children}
    </MapContext.Provider>
  );
};

export default MapContext;
