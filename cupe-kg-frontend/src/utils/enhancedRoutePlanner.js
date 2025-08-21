// cupe-kg-frontend/src/utils/enhancedRoutePlanner.js
// Create this file in the correct location: src/utils/enhancedRoutePlanner.js

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
      budget_category = 'medium',
      preferred_season = 'winter',
      start_location = 'delhi',
      transport_modes = ['mixed']
    } = preferences;

    // Step 1: Filter locations by interests
    const candidateLocations = this.filterLocationsByInterests(interests);
    
    // Step 2: Create optimized path
    const optimizedPath = this.optimizePath(candidateLocations, start_location, max_travel_days);
    
    // Step 3: Generate detailed itinerary
    const detailedItinerary = this.createDetailedItinerary(optimizedPath, transport_modes[0], budget_category);
    
    return detailedItinerary;
  }

  // Filter locations based on interests
  filterLocationsByInterests(interests) {
    if (!interests || interests.length === 0) {
      return this.locations.slice(0, 8); // Return first 8 locations as default
    }

    return this.locations.filter(location => {
      const locationTags = location.tags || [];
      const locationCategory = location.category || '';
      
      return interests.some(interest => {
        switch (interest.toLowerCase()) {
          case 'religious':
          case 'spiritual':
            return locationCategory === 'religious' || 
                   locationTags.some(tag => 
                     ['temple', 'buddhist', 'hindu', 'sikh', 'religious'].includes(tag.toLowerCase())
                   );
          
          case 'historical':
          case 'heritage':
            return locationCategory === 'historical' || 
                   locationTags.some(tag => 
                     ['unesco', 'heritage', 'historical'].includes(tag.toLowerCase())
                   );
          
          case 'architectural':
          case 'architecture':
            return locationTags.some(tag => 
              ['architecture', 'palace', 'fort', 'mughal'].includes(tag.toLowerCase())
            );
          
          case 'cultural':
            return locationCategory === 'cultural';
          
          default:
            return locationTags.some(tag => 
              tag.toLowerCase().includes(interest.toLowerCase())
            ) || locationCategory.toLowerCase().includes(interest.toLowerCase());
        }
      });
    });
  }

  // Optimize path between locations
  optimizePath(locations, startLocationId, maxDays) {
    if (locations.length === 0) return [];
    
    // Find start location
    const startLoc = locations.find(loc => loc.id === startLocationId) || locations[0];
    
    // Calculate maximum locations (2 days per location average)
    const maxLocations = Math.min(Math.floor(maxDays / 2), locations.length, 5);
    
    if (maxLocations <= 1) return [startLoc];
    
    // Simple greedy algorithm for path optimization
    let optimizedPath = [startLoc];
    let remainingLocations = locations.filter(loc => loc.id !== startLoc.id);
    
    while (optimizedPath.length < maxLocations && remainingLocations.length > 0) {
      const currentLoc = optimizedPath[optimizedPath.length - 1];
      
      // Find nearest location
      let nearestLoc = null;
      let shortestDistance = Infinity;
      
      remainingLocations.forEach(loc => {
        const distance = this.getDistance(currentLoc.id, loc.id);
        if (distance < shortestDistance) {
          shortestDistance = distance;
          nearestLoc = loc;
        }
      });
      
      if (nearestLoc) {
        optimizedPath.push(nearestLoc);
        remainingLocations = remainingLocations.filter(loc => loc.id !== nearestLoc.id);
      } else {
        break;
      }
    }
    
    return optimizedPath;
  }

  // Get distance between two locations
  getDistance(loc1Id, loc2Id) {
    // Check real distance matrix first
    if (this.realDistanceMatrix[loc1Id] && this.realDistanceMatrix[loc1Id][loc2Id]) {
      return this.realDistanceMatrix[loc1Id][loc2Id];
    }
    if (this.realDistanceMatrix[loc2Id] && this.realDistanceMatrix[loc2Id][loc1Id]) {
      return this.realDistanceMatrix[loc2Id][loc1Id];
    }
    
    // Fallback to coordinate calculation
    const loc1 = this.locations.find(l => l.id === loc1Id);
    const loc2 = this.locations.find(l => l.id === loc2Id);
    
    if (!loc1 || !loc2) return 1000; // High penalty for unknown locations
    
    return this.calculateHaversineDistance(loc1.coordinates, loc2.coordinates);
  }

  // Calculate Haversine distance
  calculateHaversineDistance(coord1, coord2) {
    const R = 6371; // Earth's radius in km
    const lat1 = coord1.lat || coord1[0];
    const lng1 = coord1.lng || coord1[1];
    const lat2 = coord2.lat || coord2[0];
    const lng2 = coord2.lng || coord2[1];
    
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return Math.round(R * c);
  }

  // Check if locations are in different regions
  isDifferentRegion(loc1, loc2) {
    const regions = {
      'north': ['delhi', 'agra', 'jaipur', 'amritsar'],
      'west': ['udaipur', 'ajanta', 'ellora'],
      'central': ['khajuraho', 'bodh-gaya', 'varanasi'],
      'south': ['hampi', 'madurai', 'mahabalipuram'],
      'east': ['konark']
    };
    
    let loc1Region = null, loc2Region = null;
    
    Object.entries(regions).forEach(([region, cities]) => {
      if (cities.includes(loc1.id)) loc1Region = region;
      if (cities.includes(loc2.id)) loc2Region = region;
    });
    
    return loc1Region !== loc2Region;
  }

  // Create detailed itinerary
  createDetailedItinerary(path, transportMode, budget) {
    const itinerary = [];
    let currentDay = 1;
    let totalCost = 0;
    
    for (let i = 0; i < path.length; i++) {
      const location = path[i];
      const nextLocation = path[i + 1];
      
      // Location exploration days
      const daysAtLocation = this.getOptimalDaysAtLocation(location);
      const dailyCost = this.getAccommodationCost(location.id, budget) + 
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
            accommodation: this.getAccommodationCost(location.id, budget),
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
      path: path.map(loc => [loc.coordinates.lat, loc.coordinates.lng]),
      locations: path.map(loc => ({
        name: loc.name,
        coordinates: [loc.coordinates.lat, loc.coordinates.lng],
        description: loc.description
      })),
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

  // Helper methods for accurate cost calculation
  getAccommodationCost(locationId, budget) {
    const costs = this.accommodationCosts[locationId] || { low: 800, medium: 2500, high: 6000 };
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
    const attractions = this.getLocationAttractions(location.id);
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
        { name: 'Humayun\'s Tomb', entryCost: 30, time: '2 hours' }
      ],
      'jaipur': [
        { name: 'Hawa Mahal', entryCost: 50, time: '1 hour' },
        { name: 'City Palace', entryCost: 300, time: '3 hours' },
        { name: 'Amber Fort', entryCost: 200, time: '4 hours' },
        { name: 'Jantar Mantar', entryCost: 40, time: '1 hour' }
      ],
      'taj-mahal': [
        { name: 'Taj Mahal', entryCost: 1100, time: '4 hours' },
        { name: 'Agra Fort', entryCost: 650, time: '3 hours' },
        { name: 'Mehtab Bagh', entryCost: 300, time: '2 hours' }
      ]
      // Add more locations...
    };
    
    return attractions[locationId] || [
      { name: 'Main attraction', entryCost: 100, time: '3 hours' },
      { name: 'Secondary site', entryCost: 50, time: '2 hours' }
    ];
  }

  getTravelDetails(fromLoc, toLoc, transportMode) {
    const distance = this.getDistance(fromLoc.id, toLoc.id);
    
    let selectedMode = transportMode;
    if (transportMode === 'mixed') {
      if (distance > 800) selectedMode = 'flight';
      else if (distance > 400) selectedMode = 'train';
      else selectedMode = 'car';
    }
    
    const costPerKm = this.transportationCosts[selectedMode] || this.transportationCosts.train;
    const cost = Math.round(distance * costPerKm);
    
    let duration;
    switch (selectedMode) {
      case 'flight':
        duration = '3 hours';
        break;
      case 'train':
        duration = `${Math.ceil(distance / 60)} hours`;
        break;
      case 'bus':
        duration = `${Math.ceil(distance / 45)} hours`;
        break;
      case 'car':
        duration = `${Math.ceil(distance / 50)} hours`;
        break;
      default:
        duration = '6 hours';
    }
    
    return {
      mode: selectedMode,
      distance: distance,
      duration: duration,
      cost: Math.max(cost, 200), // Minimum cost
      description: `${distance}km via ${selectedMode}`
    };
  }

  calculateTotalDistance(path) {
    let total = 0;
    for (let i = 0; i < path.length - 1; i++) {
      total += this.getDistance(path[i].id, path[i + 1].id);
    }
    return total;
  }
}