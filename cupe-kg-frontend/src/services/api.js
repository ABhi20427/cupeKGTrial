/**
 * API service for the CuPe-KG tourism application
 * Handles all data fetching from the backend
 */

// Base API URL - replace with your actual backend URL in production
const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Fetch information about a specific place
 * @param {string} placeId - ID of the place to fetch
 * @returns {Promise} - Promise containing place data
 */
export const fetchPlaceData = async (placeId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/place-info?name=${encodeURIComponent(placeId)}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching place data:', error);
    throw error;
  }
};

/**
 * Fetch all available cultural routes
 * @returns {Promise} - Promise containing routes data
 */
export const fetchRoutes = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/routes`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching routes:', error);
    throw error;
  }
};

/**
 * Fetch all tourist locations
 * @returns {Promise} - Promise containing locations data
 */
export const fetchLocations = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/locations`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching locations:', error);
    throw error;
  }
};

/**
 * Search for locations by keywords
 * @param {string} query - Search query
 * @returns {Promise} - Promise containing search results
 */
export const searchLocations = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error searching locations:', error);
    throw error;
  }
};

/**
 * Fetch cultural perspective data for visualization
 * @param {string} placeId - ID of the place
 * @param {string} perspectiveType - Type of perspective (e.g., 'religious', 'historical')
 * @returns {Promise} - Promise containing perspective data
 */
export const fetchCulturalPerspective = async (placeId, perspectiveType) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/perspective?place=${encodeURIComponent(placeId)}&type=${encodeURIComponent(perspectiveType)}`
    );
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching cultural perspective:', error);
    throw error;
  }
};