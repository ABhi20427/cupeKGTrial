// src/services/api.js

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

console.log('API_BASE configured as:', API_BASE);

// Location Services
export const fetchLocations = async () => {
  try {
    const response = await fetch(`${API_BASE}/locations`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Fetched locations:', data.length);
    return data;
  } catch (error) {
    console.error('Error fetching locations:', error);
    throw error;
  }
};

export const fetchPlaceData = async (locationId) => {
  try {
    const response = await fetch(`${API_BASE}/place-info?name=${encodeURIComponent(locationId)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Fetched place data for:', locationId, data);
    return data;
  } catch (error) {
    console.error('Error fetching place data:', error);
    throw error;
  }
};

export const fetchRoutes = async () => {
  try {
    const response = await fetch(`${API_BASE}/routes`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Fetched routes:', data.length);
    return data;
  } catch (error) {
    console.error('Error fetching routes:', error);
    throw error;
  }
};

// Search Services
export const searchLocations = async (query) => {
  try {
    const response = await fetch(`${API_BASE}/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('Search results for:', query, data.length);
    return data;
  } catch (error) {
    console.error('Error searching locations:', error);
    throw error;
  }
};

// Chatbot Services
export const askChatbot = async (question, sessionId, locationId = null) => {
  try {
    const response = await fetch(`${API_BASE}/chatbot/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        question,
        sessionId,
        locationId
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Chatbot response:', data);
    return data;
  } catch (error) {
    console.error('Error asking chatbot:', error);
    throw error;
  }
};

export const getChatbotRecommendations = async (preferences) => {
  try {
    const response = await fetch(`${API_BASE}/chatbot/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(preferences)
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('Chatbot recommendations:', data);
    return data;
  } catch (error) {
    console.error('Error getting recommendations:', error);
    throw error;
  }
};

// Cultural perspective endpoint (if implemented later)
export const fetchPerspective = async (placeName, perspectiveType) => {
  try {
    const response = await fetch(`${API_BASE}/perspective?place=${encodeURIComponent(placeName)}&type=${encodeURIComponent(perspectiveType)}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching perspective:', error);
    throw error;
  }
};

// Utility function to check API health
export const checkAPIHealth = async () => {
  try {
    const response = await fetch(`${API_BASE}/health`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log('API Health:', data);
    return data;
  } catch (error) {
    console.error('API health check failed:', error);
    throw error;
  }
};

// Advanced search with filters
export const advancedSearch = async (filters) => {
  try {
    const queryParams = new URLSearchParams();
    
    if (filters.query) queryParams.append('q', filters.query);
    if (filters.category) queryParams.append('category', filters.category);
    if (filters.dynasty) queryParams.append('dynasty', filters.dynasty);
    if (filters.period) queryParams.append('period', filters.period);
    
    const response = await fetch(`${API_BASE}/search/advanced?${queryParams}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error in advanced search:', error);
    throw error;
  }
};

// No need to re-export API_BASE as it's already exported through const declaration