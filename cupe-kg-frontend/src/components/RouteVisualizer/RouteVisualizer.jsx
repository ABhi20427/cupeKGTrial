import React, { useEffect, useState } from 'react';
import { Polyline, Circle } from 'react-leaflet';
import './RouteVisualizer.css';

const RouteVisualizer = ({ route }) => {
  const [animationProgress, setAnimationProgress] = useState(0);
  const [isAnimating, setIsAnimating] = useState(true);
  
  useEffect(() => {
    // Reset animation when route changes
    setAnimationProgress(0);
    setIsAnimating(true);
    
    let startTime = null;
    const animationDuration = 2000; // 2 seconds for full animation
    
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const elapsed = timestamp - startTime;
      const progress = Math.min(elapsed / animationDuration, 1);
      
      setAnimationProgress(progress);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        setIsAnimating(false);
      }
    };
    
    const animationFrame = requestAnimationFrame(animate);
    
    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [route]);
  
  // Get the portion of the route path that should be visible based on animation progress
  const getVisiblePath = () => {
    if (!route || !route.path || route.path.length < 2) return [];
    
    if (animationProgress >= 1) return route.path;
    
    const totalSegments = route.path.length - 1;
    const segmentsToShow = Math.ceil(totalSegments * animationProgress);
    
    return route.path.slice(0, segmentsToShow + 1);
  };
  
  // Get the position for the "travel dot" that moves along the route
  const getTravelDotPosition = () => {
    if (!route || !route.path || route.path.length < 2) return null;
    
    if (animationProgress >= 1) return route.path[route.path.length - 1];
    
    const totalDistance = calculateTotalDistance(route.path);
    const targetDistance = totalDistance * animationProgress;
    
    let coveredDistance = 0;
    
    for (let i = 0; i < route.path.length - 1; i++) {
      const segmentDistance = calculateDistance(route.path[i], route.path[i + 1]);
      
      if (coveredDistance + segmentDistance >= targetDistance) {
        // We found the segment where the dot should be
        const remainingDistance = targetDistance - coveredDistance;
        const segmentProgress = remainingDistance / segmentDistance;
        
        // Interpolate position
        const lat = route.path[i][0] + (route.path[i + 1][0] - route.path[i][0]) * segmentProgress;
        const lng = route.path[i][1] + (route.path[i + 1][1] - route.path[i][1]) * segmentProgress;
        
        return [lat, lng];
      }
      
      coveredDistance += segmentDistance;
    }
    
    return route.path[route.path.length - 1];
  };
  
  // Calculate distance between two points using the Haversine formula
  const calculateDistance = (point1, point2) => {
    const [lat1, lon1] = point1;
    const [lat2, lon2] = point2;
    
    const R = 6371; // Earth radius in km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
      Math.sin(dLon/2) * Math.sin(dLon/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c;
    
    return distance;
  };
  
  // Calculate total distance of the route
  const calculateTotalDistance = (path) => {
    let totalDistance = 0;
    
    for (let i = 0; i < path.length - 1; i++) {
      totalDistance += calculateDistance(path[i], path[i + 1]);
    }
    
    return totalDistance;
  };
  
  if (!route || !route.path || route.path.length < 2) return null;
  
  const visiblePath = getVisiblePath();
  const travelDotPosition = getTravelDotPosition();
  
  // Define Polyline style
  const polylineOptions = {
    color: route.color || '#3f51b5',
    weight: 4,
    opacity: 0.8,
    lineJoin: 'round',
    dashArray: route.dashArray || null,
    className: 'route-path'
  };
  
  // Define location dots style
  const stationCircleOptions = {
    radius: 6,
    fillColor: '#fff',
    color: route.color || '#3f51b5',
    weight: 2,
    opacity: 1,
    fillOpacity: 1
  };
  
  // Define travel dot style
  const travelDotOptions = {
    radius: 8,
    fillColor: route.color || '#3f51b5',
    color: '#fff',
    weight: 2,
    opacity: 1,
    fillOpacity: 1,
    className: isAnimating ? 'travel-dot pulsing' : 'travel-dot'
  };
  
  return (
    <>
      {/* The route path */}
      <Polyline positions={visiblePath} {...polylineOptions} />
      
      {/* Location dots along the route */}
      {route.locations && route.locations.map((location, index) => (
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