// cupe-kg-frontend/src/utils/enhancedRoutePlanner.js
// FIXED VERSION - Replace your entire enhancedRoutePlanner.js with this

export class UltraAccurateRoutePlanner {
  constructor(locations, routes) {
    this.locations = locations || [];
    this.routes = routes || [];
    
    // Real distance matrix (in km) between major Indian cities
    this.realDistanceMatrix = {
      'delhi': {
        'jaipur': 280, 'agra': 233, 'varanasi': 821, 'amritsar': 460,
        'hampi': 1483, 'udaipur': 421, 'khajuraho': 620, 'bodh-gaya': 1105
      },
      'jaipur': {
        'delhi': 280, 'udaipur': 393, 'taj-mahal': 240, 'ajanta': 739
      },
      'taj-mahal': {
        'delhi': 233, 'jaipur': 240, 'khajuraho': 295, 'varanasi': 605
      },
      'varanasi': {
        'delhi': 821, 'bodh-gaya': 250, 'khajuraho': 298, 'kolkata': 679,
        'agra': 605
      },
      'bodh-gaya': {
        'varanasi': 250, 'delhi': 1105, 'kolkata': 495, 'patna': 135
      },
      'hampi': {
        'delhi': 1483, 'madurai': 440
      },
      'madurai': {
        'hampi': 440, 'chennai': 462, 'bangalore': 460, 'kochi': 257
      },
      'amritsar': {
        'delhi': 460, 'chandigarh': 230, 'shimla': 350
      },
      'udaipur': {
        'jaipur': 393, 'delhi': 421, 'mumbai': 734, 'ajanta': 451
      },
      'konark': {
        'bhubaneswar': 65, 'kolkata': 380, 'delhi': 1108
      },
      'ajanta': {
        'ellora': 95, 'mumbai': 440, 'pune': 240, 'udaipur': 451
      },
      'ellora': {
        'ajanta': 95, 'mumbai': 380, 'pune': 220
      }
    };

    // Transportation costs (INR per km)
    this.transportationCosts = {
      'flight': 3.5,
      'train': 0.75,
      'bus': 0.45,
      'car': 12
    };

    // Accommodation costs by city (per night)
    this.accommodationCosts = {
      'delhi': { low: 1200, medium: 3500, high: 8500 },
      'jaipur': { low: 800, medium: 2500, high: 6500 },
      'taj-mahal': { low: 900, medium: 2800, high: 7000 },
      'varanasi': { low: 600, medium: 1800, high: 4500 },
      'amritsar': { low: 700, medium: 2000, high: 5000 },
      'udaipur': { low: 1000, medium: 3200, high: 8000 },
      'hampi': { low: 500, medium: 1500, high: 3500 },
      'madurai': { low: 600, medium: 1800, high: 4000 },
      'bodh-gaya': { low: 400, medium: 1200, high: 2800 },
      'konark': { low: 600, medium: 1600, high: 3500 },
      'mahabalipuram': { low: 800, medium: 2200, high: 5500 },
      'ajanta': { low: 600, medium: 1600, high: 3800 },
      'ellora': { low: 600, medium: 1600, high: 3800 },
      'khajuraho': { low: 700, medium: 2000, high: 4500 }
    };

    // Weather and seasonal data
    this.seasonalData = {
      'winter': {
        months: ['Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar'],
        bestRegions: ['north', 'central', 'west', 'south'],
        temperature: { min: 10, max: 25 },
        rainfall: 'minimal'
      },
      'summer': {
        months: ['Apr', 'May', 'Jun'],
        bestRegions: ['hills', 'north-east'],
        avoidRegions: ['rajasthan', 'central'],
        temperature: { min: 25, max: 45 },
        rainfall: 'none'
      },
      'monsoon': {
        months: ['Jul', 'Aug', 'Sep'],
        bestRegions: ['western-ghats', 'caves'],
        temperature: { min: 20, max: 30 },
        rainfall: 'heavy'
      }
    };
  }

  // Main route creation function
  createUltraAccurateRoute(preferences) {
    console.log('Creating ultra-accurate route with preferences:', preferences);
    
    const {
      interests = [],
      max_travel_days = 7,
      budget_range = 'medium',
      preferred_season = 'winter',
      start_location = null,
      transport_mode = 'car'
    } = preferences;

    // Step 1: Filter locations by interests
    const candidateLocations = this.filterLocationsByInterests(interests);
    console.log('Candidate locations found:', candidateLocations.length);
    
    if (candidateLocations.length === 0) {
      throw new Error('No locations found matching your interests');
    }

    // Step 2: Create optimized path
    const optimizedPath = this.optimizePath(candidateLocations, start_location, max_travel_days);
    console.log('Optimized path created:', optimizedPath.length, 'locations');
    
    if (optimizedPath.length === 0) {
      throw new Error('Could not create an optimized path with your preferences');
    }

    // Step 3: Generate detailed itinerary
    const detailedItinerary = this.createDetailedItinerary(optimizedPath, transport_mode, budget_range);
    
    return detailedItinerary;
  }

  // Filter locations based on interests
  filterLocationsByInterests(interests) {
    if (!interests || interests.length === 0) {
      return this.locations.slice(0, 8); // Return first 8 locations as default
    }

    const filteredLocations = this.locations.filter(location => {
      const locationTags = location.tags || [];
      const locationCategory = location.category || '';
      const locationDescription = location.description || '';
      
      return interests.some(interest => {
        return locationTags.some(tag => tag.toLowerCase().includes(interest.toLowerCase())) ||
               locationCategory.toLowerCase().includes(interest.toLowerCase()) ||
               locationDescription.toLowerCase().includes(interest.toLowerCase());
      });
    });

    // If filtered results are too few, add some popular destinations
    if (filteredLocations.length < 3) {
      const popularDestinations = this.locations.filter(loc => 
        ['taj-mahal', 'delhi', 'jaipur', 'varanasi', 'hampi'].includes(loc.id)
      );
      return [...filteredLocations, ...popularDestinations].slice(0, 8);
    }

    return filteredLocations.slice(0, 10);
  }

  // Optimize path based on distance and travel time
  optimizePath(locations, startLocation, maxDays) {
    if (!locations || locations.length === 0) {
      return [];
    }

    // Limit locations based on travel days (roughly 1-2 locations per day)
    const maxLocations = Math.min(locations.length, Math.ceil(maxDays / 1.5));
    const limitedLocations = locations.slice(0, maxLocations);
    
    if (limitedLocations.length <= 1) {
      return limitedLocations;
    }

    // Simple nearest neighbor optimization
    const optimizedPath = [];
    const remainingLocations = [...limitedLocations];
    
    // Start with location closest to start point or first location
    let currentLocation;
    if (startLocation) {
      currentLocation = this.findNearestLocation(remainingLocations, startLocation);
    } else {
      currentLocation = remainingLocations[0];
    }
    
    optimizedPath.push(currentLocation);
    const currentIndex = remainingLocations.indexOf(currentLocation);
    remainingLocations.splice(currentIndex, 1);

    // Add nearest neighbors
    while (remainingLocations.length > 0 && optimizedPath.length < maxLocations) {
      const currentCoords = this.getLocationCoordinates(currentLocation);
      let nearestLocation = null;
      let shortestDistance = Infinity;

      remainingLocations.forEach(loc => {
        const locCoords = this.getLocationCoordinates(loc);
        const distance = this.calculateHaversineDistance(currentCoords, locCoords);
        
        if (distance < shortestDistance) {
          shortestDistance = distance;
          nearestLocation = loc;
        }
      });

      if (nearestLocation) {
        optimizedPath.push(nearestLocation);
        currentLocation = nearestLocation;
        const nearestIndex = remainingLocations.indexOf(nearestLocation);
        remainingLocations.splice(nearestIndex, 1);
      } else {
        break;
      }
    }

    return optimizedPath;
  }

  // Find nearest location to a given point
  findNearestLocation(locations, point) {
    let nearest = locations[0];
    let shortestDistance = Infinity;

    locations.forEach(location => {
      const locCoords = this.getLocationCoordinates(location);
      const distance = this.calculateHaversineDistance(point, locCoords);
      
      if (distance < shortestDistance) {
        shortestDistance = distance;
        nearest = location;
      }
    });

    return nearest;
  }

  // Get coordinates from location object
  getLocationCoordinates(location) {
    if (location.coordinates) {
      if (typeof location.coordinates === 'object' && location.coordinates.lat) {
        return { lat: location.coordinates.lat, lng: location.coordinates.lng };
      } else if (Array.isArray(location.coordinates)) {
        return { lat: location.coordinates[0], lng: location.coordinates[1] };
      }
    }
    
    // Fallback coordinates if not available
    return { lat: 28.6139, lng: 77.2090 }; // Delhi coordinates as fallback
  }

  // Calculate Haversine distance
  calculateHaversineDistance(coord1, coord2) {
    const R = 6371; // Earth's radius in km
    const lat1 = coord1.lat || coord1[0] || 0;
    const lng1 = coord1.lng || coord1[1] || 0;
    const lat2 = coord2.lat || coord2[0] || 0;
    const lng2 = coord2.lng || coord2[1] || 0;
    
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return Math.round(R * c);
  }

  // Create detailed itinerary
  createDetailedItinerary(path, transportMode, budget) {
    const itinerary = [];
    let currentDay = 1;
    let totalCost = 0;
    
    for (let i = 0; i < path.length; i++) {
      const location = path[i];
      const nextLocation = path[i + 1];
      
      // Location exploration days - THIS IS THE MISSING METHOD
      const daysAtLocation = this.getOptimalDaysAtLocation(location);
      const dailyCost = this.getAccommodationCost(location.id || location.name, budget) + 
                       this.getFoodCost(budget) + 
                       this.getLocalTransportCost();
      
      for (let day = 0; day < daysAtLocation; day++) {
        const dayActivity = this.generateDayActivity(location, day, budget);
        itinerary.push({
          day: currentDay + day,
          location: location.name,
          type: 'exploration',
          description: dayActivity.description,
          highlights: dayActivity.highlights,
          costs: {
            accommodation: this.getAccommodationCost(location.id || location.name, budget),
            food: this.getFoodCost(budget),
            localTransport: this.getLocalTransportCost(),
            attractions: dayActivity.attractionCosts,
            total: dailyCost + dayActivity.attractionCosts
          },
          culturalInsights: this.getCulturalInsights(location),
          practicalTips: this.getPracticalTips(location)
        });
        totalCost += dailyCost + dayActivity.attractionCosts;
      }
      
      currentDay += daysAtLocation;
      
      // Travel day
      if (nextLocation) {
        const travelDetails = this.getAccurateTravelDetails(location, nextLocation, transportMode);
        itinerary.push({
          day: currentDay,
          location: `${location.name} to ${nextLocation.name}`,
          type: 'travel',
          description: `Travel from ${location.name} to ${nextLocation.name} via ${travelDetails.mode}`,
          travelDetails: travelDetails,
          costs: {
            transport: travelDetails.cost,
            food: travelDetails.mealCost || 0,
            total: travelDetails.cost + (travelDetails.mealCost || 0)
          }
        });
        totalCost += travelDetails.cost + (travelDetails.mealCost || 0);
        currentDay++;
      }
    }
    
    return {
      id: `ultra-accurate-${Date.now()}`,
      name: 'Your Culturally Intelligent Route',
      description: `Scientifically optimized ${path.length}-destination route with cultural depth`,
      color: '#2196F3',
      path: path.map(loc => {
        const coords = this.getLocationCoordinates(loc);
        return [coords.lat, coords.lng];
      }),
      locations: path.map(loc => {
        const coords = this.getLocationCoordinates(loc);
        return {
          name: loc.name,
          coordinates: [coords.lat, coords.lng],
          description: loc.description || 'Cultural heritage site'
        };
      }),
      detailedItinerary: itinerary,
      totalCost: Math.round(totalCost),
      totalDays: currentDay - 1,
      culturalThemes: this.extractCulturalThemes(path),
      optimizationMetrics: {
        totalDistance: this.calculateTotalDistance(path),
        culturalDiversity: this.calculateCulturalDiversity(path),
        costEfficiency: this.calculateCostEfficiency(totalCost, path.length)
      }
    };
  }

  // THE MISSING METHOD - Calculate optimal days at each location
  getOptimalDaysAtLocation(location) {
    // Default to 2 days, but adjust based on location importance and attractions
    const locationName = location.name?.toLowerCase() || '';
    
    // Major destinations that need more time
    const majorDestinations = ['delhi', 'rajasthan', 'taj mahal', 'varanasi', 'hampi'];
    if (majorDestinations.some(dest => locationName.includes(dest))) {
      return 3;
    }
    
    // UNESCO sites or complex sites
    const complexSites = ['ajanta', 'ellora', 'khajuraho', 'konark'];
    if (complexSites.some(site => locationName.includes(site))) {
      return 2;
    }
    
    // Default for most locations
    return 2;
  }

  // Helper methods for accurate cost calculation
  getAccommodationCost(locationId, budget) {
    const normalizedId = locationId?.toLowerCase().replace(/\s+/g, '-') || 'default';
    const costs = this.accommodationCosts[normalizedId] || { low: 800, medium: 2500, high: 6000 };
    return costs[budget] || costs.medium;
  }

  getFoodCost(budget) {
    const foodCosts = { low: 800, medium: 1500, high: 3000 };
    return foodCosts[budget] || foodCosts.medium;
  }

  getLocalTransportCost() {
    return 500; // Average local transport per day
  }

  // Generate detailed day activities
  generateDayActivity(location, dayNumber, budget) {
    const attractions = this.getLocationAttractions(location.id || location.name);
    const selectedAttractions = attractions.slice(dayNumber * 2, (dayNumber + 1) * 2);
    
    return {
      description: `Day ${dayNumber + 1} in ${location.name}: ${selectedAttractions.map(a => a.name).join(', ')}`,
      highlights: selectedAttractions,
      attractionCosts: selectedAttractions.reduce((sum, attr) => sum + (attr.entryCost || 0), 0)
    };
  }

  // Get location-specific attractions with costs
  getLocationAttractions(locationId) {
    const attractions = {
      'delhi': [
        { name: 'Red Fort', entryCost: 35, time: '3 hours' },
        { name: 'India Gate', entryCost: 0, time: '1 hour' },
        { name: 'Qutub Minar', entryCost: 30, time: '2 hours' },
        { name: 'Lotus Temple', entryCost: 0, time: '1 hour' }
      ],
      'taj-mahal': [
        { name: 'Taj Mahal', entryCost: 50, time: '4 hours' },
        { name: 'Agra Fort', entryCost: 40, time: '3 hours' },
        { name: 'Mehtab Bagh', entryCost: 25, time: '2 hours' }
      ],
      'jaipur': [
        { name: 'Amber Fort', entryCost: 25, time: '4 hours' },
        { name: 'City Palace', entryCost: 30, time: '3 hours' },
        { name: 'Hawa Mahal', entryCost: 15, time: '1 hour' }
      ]
    };

    const normalizedId = locationId?.toLowerCase().replace(/\s+/g, '-') || 'default';
    return attractions[normalizedId] || [
      { name: 'Main Attraction', entryCost: 25, time: '3 hours' },
      { name: 'Local Temple', entryCost: 10, time: '2 hours' },
      { name: 'Cultural Site', entryCost: 20, time: '2 hours' }
    ];
  }

  // Get accurate travel details between locations
  getAccurateTravelDetails(from, to, mode) {
    const fromCoords = this.getLocationCoordinates(from);
    const toCoords = this.getLocationCoordinates(to);
    const distance = this.calculateHaversineDistance(fromCoords, toCoords);
    
    const transportMode = mode || 'car';
    const costPerKm = this.transportationCosts[transportMode] || this.transportationCosts.car;
    const baseCost = distance * costPerKm;
    
    // Calculate travel time based on mode
    const speeds = { car: 60, train: 80, bus: 50, flight: 500 }; // km/h
    const speed = speeds[transportMode] || speeds.car;
    const travelTimeHours = Math.ceil(distance / speed);
    
    return {
      mode: transportMode,
      distance: distance,
      duration: `${travelTimeHours} hours`,
      cost: Math.round(baseCost),
      mealCost: travelTimeHours > 4 ? 300 : 0
    };
  }

  // Get cultural insights for location
  getCulturalInsights(location) {
    return [
      `Rich cultural heritage dating back centuries`,
      `Architectural significance in ${location.dynasty || 'regional'} style`,
      `Important pilgrimage and tourism destination`
    ];
  }

  // Get practical tips
  getPracticalTips(location) {
    return [
      'Best visited early morning or late afternoon',
      'Respect local customs and dress codes',
      'Hire local guides for deeper insights',
      'Carry water and comfortable walking shoes'
    ];
  }

  // Extract cultural themes from path
  extractCulturalThemes(path) {
    const themes = new Set();
    path.forEach(location => {
      if (location.dynasty) themes.add(location.dynasty);
      if (location.category) themes.add(location.category);
      if (location.tags) location.tags.forEach(tag => themes.add(tag));
    });
    return Array.from(themes);
  }

  // Calculate total distance
  calculateTotalDistance(path) {
    let totalDistance = 0;
    for (let i = 0; i < path.length - 1; i++) {
      const current = this.getLocationCoordinates(path[i]);
      const next = this.getLocationCoordinates(path[i + 1]);
      totalDistance += this.calculateHaversineDistance(current, next);
    }
    return totalDistance;
  }

  // Calculate cultural diversity score
  calculateCulturalDiversity(path) {
    const themes = this.extractCulturalThemes(path);
    return Math.min(themes.length * 10, 100); // Max 100%
  }

  // Calculate cost efficiency
  calculateCostEfficiency(totalCost, numLocations) {
    const costPerLocation = totalCost / numLocations;
    return costPerLocation < 5000 ? 'High' : costPerLocation < 8000 ? 'Medium' : 'Low';
  }
}