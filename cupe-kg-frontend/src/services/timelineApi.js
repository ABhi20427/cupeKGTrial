// cupe-kg-frontend/src/services/timelineApi.js
// NEW FILE: Timeline-specific API service

class TimelineApiService {
  constructor() {
    // Get base URL from environment or default to current origin
    this.baseUrl = process.env.REACT_APP_API_URL || '';
    this.timeoutMs = 10000; // 10 second timeout
  }

  /**
   * Fetch timeline periods from backend API
   * @returns {Promise<Object>} Timeline periods data
   */
  async fetchTimelinePeriods() {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(`${this.baseUrl}/api/timeline/periods`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      if (!data.success) {
        throw new Error(data.error || 'Unknown API error');
      }

      return {
        periods: data.periods || [],
        totalPeriods: data.totalPeriods || 0,
        totalLocations: data.totalLocations || 0
      };

    } catch (error) {
      clearTimeout(timeoutId);
      
      if (error.name === 'AbortError') {
        throw new Error('Request timeout - server may be slow');
      }
      
      // Network or other errors
      if (!navigator.onLine) {
        throw new Error('No internet connection');
      }
      
      throw error;
    }
  }

  /**
   * Check timeline API health
   * @returns {Promise<Object>} Health status
   */
  async checkTimelineHealth() {
    try {
      const response = await fetch(`${this.baseUrl}/api/timeline/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Health check failed: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Timeline service unavailable: ${error.message}`);
    }
  }

  /**
   * Fetch locations for a specific period
   * @param {string} period - Period identifier
   * @returns {Promise<Array>} Locations for the period
   */
  async fetchLocationsByPeriod(period) {
    try {
      const response = await fetch(`${this.baseUrl}/api/locations/period/${encodeURIComponent(period)}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch locations for period: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      throw new Error(`Period locations unavailable: ${error.message}`);
    }
  }
}

// Create singleton instance
const timelineApiService = new TimelineApiService();

export default timelineApiService;