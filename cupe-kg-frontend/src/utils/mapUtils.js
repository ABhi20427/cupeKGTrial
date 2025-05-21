/**
 * Utility functions for map operations in CuPe-KG application
 */

/**
 * Calculate distance between two points using the Haversine formula
 * @param {Array} point1 - [lat, lng] array for first point
 * @param {Array} point2 - [lat, lng] array for second point
 * @returns {Number} - Distance in kilometers
 */
export const calculateDistance = (point1, point2) => {
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
  
  /**
   * Calculate total distance of a route path
   * @param {Array} path - Array of [lat, lng] points
   * @returns {Number} - Total distance in kilometers
   */
  export const calculateTotalDistance = (path) => {
    let totalDistance = 0;
    
    for (let i = 0; i < path.length - 1; i++) {
      totalDistance += calculateDistance(path[i], path[i + 1]);
    }
    
    return totalDistance;
  };
  
  /**
   * Format distance for display
   * @param {Number} distance - Distance in kilometers
   * @returns {String} - Formatted distance string
   */
  export const formatDistance = (distance) => {
    if (distance < 1) {
      return `${Math.round(distance * 1000)} m`;
    }
    return `${Math.round(distance * 10) / 10} km`;
  };
  
  /**
   * Get the center point of a path
   * @param {Array} path - Array of [lat, lng] points
   * @returns {Array} - Center point as [lat, lng]
   */
  export const getPathCenter = (path) => {
    if (!path || path.length === 0) {
      return [0, 0];
    }
    
    let sumLat = 0;
    let sumLng = 0;
    
    for (const point of path) {
      sumLat += point[0];
      sumLng += point[1];
    }
    
    return [sumLat / path.length, sumLng / path.length];
  };
  
  /**
   * Get the bounds of a path
   * @param {Array} path - Array of [lat, lng] points
   * @returns {Object} - Bounds as { north, south, east, west }
   */
  export const getPathBounds = (path) => {
    if (!path || path.length === 0) {
      return { north: 0, south: 0, east: 0, west: 0 };
    }
    
    let north = path[0][0];
    let south = path[0][0];
    let east = path[0][1];
    let west = path[0][1];
    
    for (const point of path) {
      if (point[0] > north) north = point[0];
      if (point[0] < south) south = point[0];
      if (point[1] > east) east = point[1];
      if (point[1] < west) west = point[1];
    }
    
    return { north, south, east, west };
  };
  
  /**
   * Get a point at a specific percentage along a path
   * @param {Array} path - Array of [lat, lng] points
   * @param {Number} percentage - Percentage along the path (0-1)
   * @returns {Array} - Point at the given percentage as [lat, lng]
   */
  export const getPointAtPercentage = (path, percentage) => {
    if (!path || path.length < 2 || percentage < 0 || percentage > 1) {
      return null;
    }
    
    const totalDistance = calculateTotalDistance(path);
    const targetDistance = totalDistance * percentage;
    
    let coveredDistance = 0;
    
    for (let i = 0; i < path.length - 1; i++) {
      const segmentDistance = calculateDistance(path[i], path[i + 1]);
      
      if (coveredDistance + segmentDistance >= targetDistance) {
        // We found the segment where the point should be
        const remainingDistance = targetDistance - coveredDistance;
        const segmentProgress = remainingDistance / segmentDistance;
        
        // Interpolate position
        const lat = path[i][0] + (path[i + 1][0] - path[i][0]) * segmentProgress;
        const lng = path[i][1] + (path[i + 1][1] - path[i][1]) * segmentProgress;
        
        return [lat, lng];
      }
      
      coveredDistance += segmentDistance;
    }
    
    return path[path.length - 1]; // Return the last point if percentage is 1
  };
  
  /**
   * Create a smooth path by adding intermediate points
   * @param {Array} path - Array of [lat, lng] points
   * @param {Number} segments - Number of segments to divide each line into
   * @returns {Array} - Smoothed path with intermediate points
   */
  export const createSmoothPath = (path, segments = 5) => {
    if (!path || path.length < 2 || segments < 2) {
      return path;
    }
    
    const smoothedPath = [];
    
    for (let i = 0; i < path.length - 1; i++) {
      smoothedPath.push(path[i]);
      
      const [startLat, startLng] = path[i];
      const [endLat, endLng] = path[i + 1];
      
      for (let j = 1; j < segments; j++) {
        const progress = j / segments;
        const lat = startLat + (endLat - startLat) * progress;
        const lng = startLng + (endLng - startLng) * progress;
        
        smoothedPath.push([lat, lng]);
      }
    }
    
    smoothedPath.push(path[path.length - 1]);
    
    return smoothedPath;
  };