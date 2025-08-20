// cupe-kg-frontend/src/utils/routePlanner.js
// Create this new file for enhanced route planning

export class EnhancedRoutePlanner {
  constructor(locations, routes) {
    this.locations = locations;
    this.routes = routes;
  }

  // Main function to create personalized routes
  createPersonalizedRoute(preferences) {
    const {
      interests = [],
      maxDays = 7,
      budget = 'medium',
      season = 'winter',
      startLocation = 'delhi',
      transportMode = 'mixed',
      crowdPreference = 'medium'
    } = preferences;

    // Step 1: Filter locations by interests
    const candidateLocations = this.filterLocationsByInterests(interests);
    
    // Step 2: Apply seasonal and budget filters
    const filteredLocations = this.applyFilters(candidateLocations, { season, budget, crowdPreference });
    
    // Step 3: Create optimized path
    const optimizedPath = this.optimizePath(filteredLocations, startLocation, maxDays);
    
    // Step 4: Add transportation and cultural context
    const enhancedRoute = this.enhanceRouteWithContext(optimizedPath, transportMode, budget);
    
    return enhancedRoute;
  }

  // Filter locations based on user interests
  filterLocationsByInterests(interests) {
    if (!interests || interests.length === 0) {
      return this.locations;
    }

    return this.locations.filter(location => {
      const locationTags = location.tags || [];
      const locationCategory = location.category || '';
      
      return interests.some(interest => {
        switch (interest.toLowerCase()) {
          case 'religious':
          case 'spiritual':
            return locationCategory === 'religious' || 
                   locationTags.some(tag => tag.toLowerCase().includes('temple') || 
                                          tag.toLowerCase().includes('buddhist') ||
                                          tag.toLowerCase().includes('hindu'));
          
          case 'historical':
          case 'heritage':
            return locationCategory === 'historical' || 
                   locationTags.some(tag => tag.toLowerCase().includes('unesco') ||
                                          tag.toLowerCase().includes('heritage'));
          
          case 'architecture':
          case 'architectural':
            return locationTags.some(tag => tag.toLowerCase().includes('architecture') ||
                                          tag.toLowerCase().includes('palace') ||
                                          tag.toLowerCase().includes('fort'));
          
          case 'cultural':
            return locationCategory === 'cultural' ||
                   locationTags.some(tag => tag.toLowerCase().includes('cultural'));
          
          case 'royal':
          case 'palace':
            return locationTags.some(tag => tag.toLowerCase().includes('royal') ||
                                          tag.toLowerCase().includes('palace') ||
                                          tag.toLowerCase().includes('rajput'));
          
          default:
            return locationTags.some(tag => 
              tag.toLowerCase().includes(interest.toLowerCase()));
        }
      });
    });
  }

  // Apply various filters (seasonal, budget, crowd preference)
  applyFilters(locations, filters) {
    let filtered = [...locations];

    // Seasonal filter
    if (filters.season) {
      filtered = this.applySeasonalFilter(filtered, filters.season);
    }

    // Budget filter (affects location selection)
    if (filters.budget === 'low') {
      // Prefer locations with lower entry fees or free access
      filtered = filtered.filter(loc => 
        !loc.tags?.includes('Luxury') && 
        loc.category !== 'luxury'
      );
    }

    // Crowd preference filter
    if (filters.crowdPreference === 'low') {
      // Avoid very popular tourist spots during peak times
      filtered = filtered.filter(loc => 
        !loc.tags?.includes('Golden Triangle') ||
        filters.season === 'monsoon' // Off-season
      );
    }

    return filtered;
  }

  // Apply seasonal recommendations
  applySeasonalFilter(locations, season) {
    const seasonalPreferences = {
      'winter': { // Oct-Mar
        preferred: ['delhi', 'jaipur', 'udaipur', 'taj-mahal', 'khajuraho', 'konark'],
        avoid: [] // Most places good in winter
      },
      'summer': { // Apr-Jun
        preferred: ['amritsar', 'delhi'], // Northern hill stations better
        avoid: ['jaipur', 'udaipur'] // Too hot in Rajasthan
      },
      'monsoon': { // Jul-Sep
        preferred: ['ajanta', 'ellora', 'mahabalipuram'],
        avoid: ['amritsar'] // Heavy rains in Punjab
      }
    };

    const seasonData = seasonalPreferences[season] || seasonalPreferences['winter'];
    
    // Boost preferred locations, but don't completely exclude others
    return locations.map(location => ({
      ...location,
      seasonalBoost: seasonData.preferred.includes(location.id) ? 1.5 : 
                    seasonData.avoid.includes(location.id) ? 0.5 : 1.0
    })).sort((a, b) => (b.seasonalBoost || 1) - (a.seasonalBoost || 1));
  }

  // Optimize path between locations
  optimizePath(locations, startLocationId, maxDays) {
    if (locations.length === 0) return null;

    // Find start location
    const startLoc = locations.find(loc => loc.id === startLocationId) || locations[0];
    
    // Calculate maximum locations based on days (roughly 1.5-2 days per location)
    const maxLocations = Math.min(Math.floor(maxDays / 1.5), locations.length);
    
    // Simple greedy algorithm for path optimization
    let path = [startLoc];
    let remaining = locations.filter(loc => loc.id !== startLoc.id);
    
    while (path.length < maxLocations && remaining.length > 0) {
      const currentLoc = path[path.length - 1];
      
      // Find nearest location (simplified distance calculation)
      const nearest = remaining.reduce((nearest, loc) => {
        const currentDistance = this.calculateDistance(currentLoc.coordinates, loc.coordinates);
        const nearestDistance = nearest ? this.calculateDistance(currentLoc.coordinates, nearest.coordinates) : Infinity;
        
        return currentDistance < nearestDistance ? loc : nearest;
      }, null);
      
      if (nearest) {
        path.push(nearest);
        remaining = remaining.filter(loc => loc.id !== nearest.id);
      }
    }
    
    return path;
  }

  // Calculate distance between two coordinates (simplified)
  calculateDistance(coord1, coord2) {
    const lat1 = coord1.lat || coord1[0];
    const lng1 = coord1.lng || coord1[1];
    const lat2 = coord2.lat || coord2[0];
    const lng2 = coord2.lng || coord2[1];
    
    // Simple Euclidean distance (for basic optimization)
    return Math.sqrt(Math.pow(lat2 - lat1, 2) + Math.pow(lng2 - lng1, 2));
  }

  // Enhance route with transportation and cultural context
  enhanceRouteWithContext(path, transportMode, budget) {
    if (!path || path.length === 0) return null;

    const route = {
      id: `personalized-${Date.now()}`,
      name: 'Your Personalized Route',
      description: `Custom route with ${path.length} destinations tailored to your preferences`,
      color: '#2196F3',
      path: path.map(loc => [loc.coordinates.lat || loc.coordinates[0], loc.coordinates.lng || loc.coordinates[1]]),
      locations: path.map(loc => ({
        name: loc.name,
        coordinates: [loc.coordinates.lat || loc.coordinates[0], loc.coordinates.lng || loc.coordinates[1]],
        description: loc.description
      })),
      // Enhanced details
      estimatedDays: Math.ceil(path.length * 1.5),
      transportationMode: transportMode,
      budgetCategory: budget,
      detailedItinerary: this.createDetailedItinerary(path, transportMode, budget)
    };

    return route;
  }

  // Create detailed day-by-day itinerary
  createDetailedItinerary(path, transportMode, budget) {
    const itinerary = [];
    let currentDay = 1;

    for (let i = 0; i < path.length; i++) {
      const location = path[i];
      const nextLocation = path[i + 1];

      // Add location visit days
      const daysAtLocation = this.calculateDaysAtLocation(location);
      
      for (let day = 0; day < daysAtLocation; day++) {
        itinerary.push({
          day: currentDay + day,
          location: location.name,
          type: 'exploration',
          description: day === 0 ? 
            `Arrive and explore ${location.name}. ${location.description}` :
            `Continue exploring ${location.name}. Visit additional sites and local attractions.`,
          highlights: this.getLocationHighlights(location),
          estimatedCost: this.estimateDailyCost(location, budget)
        });
      }
      
      currentDay += daysAtLocation;

      // Add travel day if there's a next location
      if (nextLocation) {
        const travelInfo = this.getTravelInfo(location, nextLocation, transportMode);
        itinerary.push({
          day: currentDay,
          location: `${location.name} to ${nextLocation.name}`,
          type: 'travel',
          description: `Travel from ${location.name} to ${nextLocation.name}`,
          travelDetails: travelInfo,
          estimatedCost: travelInfo.cost
        });
        currentDay++;
      }
    }

    return itinerary;
  }

  // Calculate recommended days at each location
  calculateDaysAtLocation(location) {
    const locationDays = {
      'taj-mahal': 1,
      'delhi': 2,
      'jaipur': 2,
      'udaipur': 2,
      'varanasi': 2,
      'hampi': 2,
      'khajuraho': 1,
      'konark': 1,
      'ajanta': 1,
      'ellora': 1,
      'bodh-gaya': 1,
      'amritsar': 1,
      'madurai': 1,
      'mahabalipuram': 1
    };

    return locationDays[location.id] || 1;
  }

  // Get main highlights for each location
  getLocationHighlights(location) {
    const highlights = {
      'taj-mahal': ['Taj Mahal at sunrise', 'Agra Fort', 'Mehtab Bagh gardens'],
      'delhi': ['Red Fort', 'India Gate', 'Qutub Minar', 'Humayun\'s Tomb', 'Jama Masjid'],
      'jaipur': ['Hawa Mahal', 'City Palace', 'Amber Fort', 'Jantar Mantar'],
      'udaipur': ['City Palace', 'Lake Pichola boat ride', 'Jag Mandir', 'Saheliyon ki Bari'],
      'varanasi': ['Ganga Aarti ceremony', 'Boat ride at sunrise', 'Sarnath', 'Banaras Hindu University'],
      'hampi': ['Virupaksha Temple', 'Vittala Temple complex', 'Stone Chariot', 'Lotus Mahal'],
      'khajuraho': ['Western Group temples', 'Kandariya Mahadeva', 'Light and Sound show'],
      'konark': ['Sun Temple', 'Archaeological Museum', 'Chandrabhaga Beach'],
      'ajanta': ['Cave paintings', 'Cave 1 and 2 (finest paintings)', 'Viewpoint'],
      'ellora': ['Kailasa Temple (Cave 16)', 'Buddhist caves (1-12)', 'Jain caves (30-34)'],
      'bodh-gaya': ['Mahabodhi Temple', 'Bodhi Tree', 'International monasteries'],
      'amritsar': ['Golden Temple', 'Jallianwala Bagh', 'Wagah Border ceremony'],
      'madurai': ['Meenakshi Temple', 'Thirumalai Nayak Palace', 'Gandhi Memorial Museum'],
      'mahabalipuram': ['Shore Temple', 'Five Rathas', 'Arjuna\'s Penance', 'Beach']
    };

    return highlights[location.id] || ['Main attractions', 'Local culture', 'Photography'];
  }

  // Estimate daily cost based on budget category
  estimateDailyCost(location, budget) {
    const baseCosts = {
      'low': { accommodation: 1000, food: 800, local: 500 },
      'medium': { accommodation: 3000, food: 1500, local: 1000 },
      'high': { accommodation: 8000, food: 3000, local: 2000 }
    };

    const costs = baseCosts[budget] || baseCosts['medium'];
    const total = costs.accommodation + costs.food + costs.local;

    return {
      accommodation: costs.accommodation,
      food: costs.food,
      localTransport: costs.local,
      total: total,
      currency: 'INR'
    };
  }

  // Get travel information between locations
  getTravelInfo(fromLocation, toLocation, transportMode) {
    const distance = this.calculateDistance(fromLocation.coordinates, toLocation.coordinates) * 111; // Convert to rough km
    
    const travelOptions = {
      'flight': {
        duration: '2-3 hours',
        cost: Math.min(8000, distance * 2), // ₹2 per km, max ₹8000
        description: 'Fastest option, suitable for long distances'
      },
      'train': {
        duration: `${Math.ceil(distance / 60)} hours`, // Assume 60 km/h average
        cost: distance * 0.5, // ₹0.5 per km
        description: 'Comfortable and scenic, good for medium distances'
      },
      'bus': {
        duration: `${Math.ceil(distance / 40)} hours`, // Assume 40 km/h average
        cost: distance * 0.3, // ₹0.3 per km
        description: 'Most economical, good for shorter distances'
      },
      'car': {
        duration: `${Math.ceil(distance / 50)} hours`, // Assume 50 km/h average
        cost: distance * 8, // ₹8 per km (fuel + driver)
        description: 'Flexible timing, good for sightseeing en route'
      }
    };

    let selectedMode = transportMode;
    if (transportMode === 'mixed') {
      // Auto-select based on distance
      if (distance > 800) selectedMode = 'flight';
      else if (distance > 300) selectedMode = 'train';
      else selectedMode = 'car';
    }

    const travelDetails = travelOptions[selectedMode] || travelOptions['train'];
    
    return {
      mode: selectedMode,
      distance: Math.round(distance),
      duration: travelDetails.duration,
      cost: Math.round(travelDetails.cost),
      description: travelDetails.description,
      alternatives: transportMode === 'mixed' ? travelOptions : null
    };
  }

  // Get seasonal recommendations
  getSeasonalRecommendations(season) {
    const recommendations = {
      'winter': {
        bestFor: 'Most pleasant weather across India',
        clothing: 'Light woolens, comfortable walking shoes',
        specialEvents: 'Delhi Winter festivals, Rajasthan cultural events'
      },
      'summer': {
        bestFor: 'Hill stations and northern regions',
        clothing: 'Light cotton clothes, sun protection',
        specialEvents: 'Summer festivals in hill stations'
      },
      'monsoon': {
        bestFor: 'Cave exploration, cultural sites',
        clothing: 'Waterproof gear, quick-dry clothes',
        specialEvents: 'Monsoon festivals, lush green landscapes'
      }
    };

    return recommendations[season] || recommendations['winter'];
  }
}

// Usage example:
// const planner = new EnhancedRoutePlanner(locations, routes);
// const personalizedRoute = planner.createPersonalizedRoute({
//   interests: ['religious', 'historical'],
//   maxDays: 10,
//   budget: 'medium',
//   season: 'winter',
//   startLocation: 'delhi',
//   transportMode: 'mixed'
// });