// Replace your RouteVisualizer component with this fixed version

import React, { useState, useEffect } from 'react';
import { Polyline, Circle } from 'react-leaflet';

const RouteVisualizer = ({ route }) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [animationProgress, setAnimationProgress] = useState(0);

  // Helper function to safely extract coordinates
  const extractCoordinates = (coord) => {
    if (!coord) return null;
    
    // Handle different coordinate formats
    if (Array.isArray(coord) && coord.length >= 2) {
      // Ensure coordinates are numbers
      const lat = parseFloat(coord[0]);
      const lng = parseFloat(coord[1]);
      
      // Validate coordinates
      if (isNaN(lat) || isNaN(lng)) {
        console.warn('Invalid coordinates:', coord);
        return null;
      }
      
      return [lat, lng];
    }
    
    if (coord.lat !== undefined && coord.lng !== undefined) {
      const lat = parseFloat(coord.lat);
      const lng = parseFloat(coord.lng);
      
      if (isNaN(lat) || isNaN(lng)) {
        console.warn('Invalid coordinates:', coord);
        return null;
      }
      
      return [lat, lng];
    }
    
    console.warn('Unknown coordinate format:', coord);
    return null;
  };

  // Convert route path to valid coordinates
  const getValidPath = () => {
    if (!route || !route.path) {
      console.warn('Route or route.path is missing');
      return [];
    }
    
    const validPath = route.path
      .map(coord => extractCoordinates(coord))
      .filter(coord => coord !== null);
    
    console.log('Original path:', route.path);
    console.log('Valid path:', validPath);
    
    return validPath;
  };

  // Convert route locations to valid coordinates
  const getValidLocations = () => {
    if (!route || !route.locations) {
      console.warn('Route or route.locations is missing');
      return [];
    }
    
    const validLocations = route.locations
      .map(location => {
        const coords = extractCoordinates(location.coordinates);
        return coords ? { ...location, coordinates: coords } : null;
      })
      .filter(location => location !== null);
    
    console.log('Original locations:', route.locations);
    console.log('Valid locations:', validLocations);
    
    return validLocations;
  };

  // Animation effect
  useEffect(() => {
    if (!route) return;
    
    setIsAnimating(true);
    const duration = 3000; // 3 seconds
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      setAnimationProgress(progress);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setIsAnimating(false);
      }
    };
    
    animate();
  }, [route]);

  // Get visible path based on animation progress
  const getVisiblePath = () => {
    const fullPath = getValidPath();
    if (fullPath.length === 0) return [];
    
    if (!isAnimating) return fullPath;
    
    const visiblePointCount = Math.floor(fullPath.length * animationProgress);
    return fullPath.slice(0, Math.max(visiblePointCount, 1));
  };

  // Get travel dot position
  const getTravelDotPosition = () => {
    const fullPath = getValidPath();
    if (fullPath.length === 0 || !isAnimating) return null;
    
    const targetIndex = Math.floor((fullPath.length - 1) * animationProgress);
    return fullPath[targetIndex];
  };

  if (!route) {
    console.warn('RouteVisualizer: No route provided');
    return null;
  }

  const validPath = getValidPath();
  const validLocations = getValidLocations();
  
  if (validPath.length === 0) {
    console.error('RouteVisualizer: No valid path coordinates found');
    return null;
  }

  const visiblePath = getVisiblePath();
  const travelDotPosition = getTravelDotPosition();

  // Define styles
  const polylineOptions = {
    color: route.color || '#e91e63',
    weight: 4,
    opacity: 0.8,
    lineJoin: 'round',
    dashArray: route.dashArray || null,
    className: 'route-path'
  };

  const stationCircleOptions = {
    radius: 6,
    fillColor: '#fff',
    color: route.color || '#e91e63',
    weight: 2,
    opacity: 1,
    fillOpacity: 1
  };

  const travelDotOptions = {
    radius: 8,
    fillColor: route.color || '#e91e63',
    color: '#fff',
    weight: 2,
    opacity: 1,
    fillOpacity: 1,
    className: isAnimating ? 'travel-dot pulsing' : 'travel-dot'
  };

  console.log('RouteVisualizer rendering:', {
    routeName: route.name,
    pathLength: validPath.length,
    locationsLength: validLocations.length,
    isAnimating,
    animationProgress
  });

  return (
    <>
      {/* The route path */}
      <Polyline positions={visiblePath} {...polylineOptions} />
      
      {/* Location dots along the route */}
      {validLocations.map((location, index) => (
        <Circle 
          key={`station-${index}`}
          center={location.coordinates} 
          {...stationCircleOptions}
        />
      ))}
      
      {/* Moving travel dot */}
      {travelDotPosition && (
        <Circle 
          center={travelDotPosition} 
          {...travelDotOptions}
        />
      )}
    </>
  );
};

export default RouteVisualizer;