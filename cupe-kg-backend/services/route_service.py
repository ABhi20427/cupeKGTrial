# services/route_service.py (Complete Enhanced Version)

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
import random
import math
from typing import List, Dict, Any, Optional, Tuple
from models.route import Route, RouteLocation
from models.location import Location

# Import the new UserPreferences model if it exists, otherwise use basic dict
try:
    from models.user_preferences import UserPreferences, InterestType
    HAS_USER_PREFERENCES = True
except ImportError:
    HAS_USER_PREFERENCES = False
    print("UserPreferences model not found. Using basic preference handling.")

class RouteService:
    def __init__(self, kg_service):
        self.kg_service = kg_service
        self._initialize_predefined_routes()
        
    def _initialize_predefined_routes(self):
        """Initialize predefined cultural routes"""
        try:
            # Try to load routes from data module
            from data.routes import routes as routes_data
            self.predefined_routes = []
            
            for route_data in routes_data:
                # Convert location data to RouteLocation objects
                locations = [
                    RouteLocation(
                        name=loc['name'],
                        coordinates=loc['coordinates'],
                        description=loc['description']
                    ) for loc in route_data.get('locations', [])
                ]
                
                # Create Route object
                route = Route(
                    id=route_data['id'],
                    name=route_data['name'],
                    description=route_data['description'],
                    color=route_data.get('color', '#3f51b5'),
                    path=route_data.get('path', []),
                    locations=locations,
                    dash_array=route_data.get('dashArray')
                )
                
                self.predefined_routes.append(route)
                
        except (ImportError, AttributeError) as e:
            # Fall back to hardcoded routes if data module is unavailable
            print(f"Error loading routes: {e}")
            self.predefined_routes = self._create_hardcoded_routes()
    
    def _create_hardcoded_routes(self):
        """Create hardcoded routes as fallback"""
        routes = []
        
        # Buddhist Trail
        buddhist_trail = Route(
            id="buddhist",
            name="Buddhist Trail",
            description="Follow the footsteps of Buddha and explore key sites of Buddhist heritage",
            color="#FF5722",
            path=[
                [28.7041, 77.1025],  # Delhi
                [27.5006, 77.6714],  # Mathura
                [25.3176, 82.9739],  # Varanasi
                [24.6959, 84.9920],  # Bodh Gaya
                [25.2048, 85.8910],  # Nalanda
                [25.5941, 85.1376],  # Patna
                [24.1913, 88.2683]   # Rajgir
            ],
            locations=[
                RouteLocation(
                    name="Delhi",
                    coordinates=[28.7041, 77.1025],
                    description="Starting point with Buddhist monuments like Ashokan pillars"
                ),
                RouteLocation(
                    name="Bodh Gaya",
                    coordinates=[24.6959, 84.9920],
                    description="Where Buddha attained enlightenment under the Bodhi Tree"
                ),
                RouteLocation(
                    name="Nalanda",
                    coordinates=[25.2048, 85.8910],
                    description="Ancient Buddhist university and center of learning"
                )
            ]
        )
        routes.append(buddhist_trail)
        
        # Mughal Architecture route
        mughal_route = Route(
            id="mughal",
            name="Mughal Architecture",
            description="Discover the grandeur of Mughal architectural marvels across Northern India",
            color="#4CAF50",
            dash_array="5, 10",
            path=[
                [28.7041, 77.1025],  # Delhi
                [27.1767, 78.0081],  # Agra
                [26.9124, 75.7873],  # Jaipur
                [26.2124, 78.1772],  # Gwalior
                [25.3176, 82.9739],  # Varanasi
                [26.8467, 80.9462]   # Lucknow
            ],
            locations=[
                RouteLocation(
                    name="Delhi",
                    coordinates=[28.7041, 77.1025],
                    description="Home to Red Fort, Jama Masjid, and Humayun's Tomb"
                ),
                RouteLocation(
                    name="Agra",
                    coordinates=[27.1767, 78.0081],
                    description="Location of the iconic Taj Mahal and Agra Fort"
                ),
                RouteLocation(
                    name="Fatehpur Sikri",
                    coordinates=[27.0940, 77.6700],
                    description="Abandoned Mughal capital city with well-preserved architecture"
                )
            ]
        )
        routes.append(mughal_route)
        
        # Temple Route
        temple_route = Route(
            id="temple",
            name="Temple Route",
            description="Experience the rich diversity of ancient temple architecture and spirituality",
            color="#9C27B0",
            path=[
                [19.8876, 86.0945],  # Konark
                [19.8135, 85.8312],  # Puri
                [20.2399, 85.8320],  # Bhubaneswar
                [15.3350, 76.4600],  # Hampi
                [13.0827, 75.2579],  # Belur
                [10.9435, 79.8380],  # Thanjavur
                [9.9195, 78.1193]    # Madurai
            ],
            locations=[
                RouteLocation(
                    name="Konark",
                    coordinates=[19.8876, 86.0945],
                    description="Famous for the Sun Temple, an architectural marvel"
                ),
                RouteLocation(
                    name="Hampi",
                    coordinates=[15.3350, 76.4600],
                    description="Ruins of Vijayanagara with numerous temples"
                ),
                RouteLocation(
                    name="Madurai",
                    coordinates=[9.9195, 78.1193],
                    description="Home to the magnificent Meenakshi Amman Temple"
                )
            ]
        )
        routes.append(temple_route)
        
        return routes
        
    def get_all_routes(self):
        """Get all predefined routes"""
        return self.predefined_routes
    
    def get_route_by_id(self, route_id):
        """Get a specific route by ID"""
        for route in self.predefined_routes:
            if route.id == route_id:
                return route
        return None
    
    def get_routes_by_theme(self, theme):
        """Get routes matching a specific theme"""
        matching_routes = []
        theme_lower = theme.lower()
        
        for route in self.predefined_routes:
            if (theme_lower in route.id.lower() or 
                theme_lower in route.name.lower() or 
                theme_lower in route.description.lower()):
                matching_routes.append(route)
                
        return matching_routes

    # ===== NEW ENHANCED PREFERENCE-BASED ROUTING =====
    
    def create_personalized_route_with_preferences(self, preferences) -> Route:
        """Create a personalized route based on detailed user preferences"""
        
        # Handle both UserPreferences object and dict
        if HAS_USER_PREFERENCES and isinstance(preferences, UserPreferences):
            prefs = preferences
        else:
            # Convert dict to pseudo-UserPreferences for compatibility
            prefs = self._dict_to_preferences(preferences)
        
        # Step 1: Get all locations and filter by preferences
        all_locations = self.kg_service.get_all_locations()
        suitable_locations = self._filter_locations_by_preferences(all_locations, prefs)
        
        if not suitable_locations:
            raise ValueError("No suitable locations found for your preferences")
        
        # Step 2: Score and rank locations
        scored_locations = self._score_locations(suitable_locations, prefs)
        
        # Step 3: Create optimal route
        optimal_route = self._create_optimal_route(scored_locations, prefs)
        
        return optimal_route
    
    def _dict_to_preferences(self, preferences_dict):
        """Convert dict to preferences object for compatibility"""
        class SimplePreferences:
            def __init__(self, data):
                self.interests = data.get('interests', [])
                self.max_travel_days = data.get('max_travel_days', 7)
                self.budget_range = data.get('budget_range', 'medium')
                self.transport_mode = data.get('transport_mode', 'car')
                self.start_location = data.get('start_location')
                self.preferred_regions = data.get('preferred_regions', [])
                self.max_distance_km = data.get('max_distance_km', 500)
                self.preferred_periods = data.get('preferred_periods', [])
                self.preferred_dynasties = data.get('preferred_dynasties', [])
                self.crowd_preference = data.get('crowd_preference', 'medium')
                self.accommodation_type = data.get('accommodation_type', 'medium')
                self.cultural_activities = data.get('cultural_activities', [])
                self.accessibility_required = data.get('accessibility_required', False)
                self.physical_difficulty_preference = data.get('physical_difficulty_preference', 'medium')
            
            def to_dict(self):
                return {
                    'interests': self.interests,
                    'max_travel_days': self.max_travel_days,
                    'budget_range': self.budget_range,
                    'transport_mode': self.transport_mode,
                    'start_location': self.start_location,
                    'preferred_regions': self.preferred_regions,
                    'max_distance_km': self.max_distance_km,
                    'preferred_periods': self.preferred_periods,
                    'preferred_dynasties': self.preferred_dynasties,
                    'crowd_preference': self.crowd_preference,
                    'accommodation_type': self.accommodation_type,
                    'cultural_activities': self.cultural_activities,
                    'accessibility_required': self.accessibility_required,
                    'physical_difficulty_preference': self.physical_difficulty_preference
                }
        
        return SimplePreferences(preferences_dict)
    
    # Replace your _filter_locations_by_preferences method in route_service.py

# Replace this method in your route_service.py

    def _filter_locations_by_preferences(self, locations: List[Location], prefs) -> List[Location]:
        """Filter locations based on user preferences - COMPLETELY FIXED VERSION"""
        print(f"\n=== FILTERING {len(locations)} LOCATIONS ===")
        print(f"User interests: {prefs.interests}")
        
        filtered = []
        
        for location in locations:
            print(f"\n--- Checking {location.name} ---")
            
            # If no interests specified, include all locations
            if not prefs.interests:
                print(f"✅ No interests specified, including {location.name}")
                filtered.append(location)
                continue
            
            # Check if location matches any interest
            matches_interest = self._matches_interests(location, prefs.interests)
            
            if matches_interest:
                print(f"✅ Including {location.name} - matches interests")
                filtered.append(location)
            else:
                print(f"❌ Excluding {location.name} - no interest match")
        
        print(f"\n=== FILTERING COMPLETE ===")
        print(f"Filtered locations: {[loc.name for loc in filtered]}")
        print(f"Total: {len(filtered)} out of {len(locations)}")
        
        return filtered
    
    def _matches_interests(self, location: Location, interests) -> bool:
        """Check if location matches user interests - FIXED VERSION"""
        if not interests:
            return True

        print(f"Checking location: {location.name}")
        print(f"User interests: {interests}")

        # Get location data with better handling
        location_tags = [tag.lower().strip() for tag in getattr(location, 'tags', [])]
        location_category = getattr(location, 'category', '').lower().strip()
        location_description = getattr(location, 'description', '').lower().strip()
        location_name = getattr(location, 'name', '').lower().strip()
        location_dynasty = getattr(location, 'dynasty', '').lower().strip()

        print(f"Location category: '{location_category}'")
        print(f"Location tags: {location_tags}")
        print(f"Location dynasty: '{location_dynasty}'")

        for interest in interests:
            interest_lower = str(interest).lower().strip()
            print(f"Checking interest: '{interest_lower}'")

            # 1. EXACT category match
            if interest_lower == location_category:
                print(f"✅ EXACT category match: {interest_lower}")
                return True

            # 2. Category contains interest (partial match)
            if interest_lower in location_category or location_category in interest_lower:
                print(f"✅ Category partial match: {interest_lower} <-> {location_category}")
                return True

            # 3. Check tags (exact and partial)
            for tag in location_tags:
                if interest_lower == tag or interest_lower in tag or tag in interest_lower:
                    print(f"✅ Tag match: {interest_lower} <-> {tag}")
                    return True

            # 4. Check name (partial match)
            if interest_lower in location_name or location_name in interest_lower:
                print(f"✅ Name match: {interest_lower} <-> {location_name}")
                return True

            # 5. Check description (partial match)
            if interest_lower in location_description:
                print(f"✅ Description match: {interest_lower} in description")
                return True

            # 6. Dynasty match
            if interest_lower in location_dynasty or location_dynasty in interest_lower:
                print(f"✅ Dynasty match: {interest_lower} <-> {location_dynasty}")
                return True

            # 7. BROAD MATCHING - This is the key fix!
            broad_matches = {
                'historical': ['history', 'historic', 'heritage', 'ancient', 'medieval', 'monument', 'fort', 'palace', 'temple'],
                'religious': ['temple', 'mosque', 'church', 'spiritual', 'sacred', 'holy', 'pilgrimage', 'worship', 'deity'],
                'architectural': ['architecture', 'building', 'structure', 'design', 'construction', 'monument', 'palace', 'fort'],
                'cultural': ['culture', 'art', 'tradition', 'festival', 'heritage', 'custom', 'community'],
                'archaeological': ['archaeology', 'excavation', 'ruins', 'ancient', 'artifact', 'site'],
                'royal_heritage': ['royal', 'king', 'queen', 'emperor', 'palace', 'kingdom', 'dynasty', 'maharaja'],
                'ancient_temples': ['temple', 'ancient', 'deity', 'worship', 'shrine', 'sacred'],
                'forts_palaces': ['fort', 'palace', 'citadel', 'stronghold', 'castle', 'fortification'],
                'unesco_sites': ['unesco', 'world heritage', 'protected', 'international']
            }

            # Check broad matches
            if interest_lower in broad_matches:
                keywords = broad_matches[interest_lower]
                search_text = f"{location_name} {location_description} {location_category} {' '.join(location_tags)} {location_dynasty}"
                
                for keyword in keywords:
                    if keyword in search_text:
                        print(f"✅ BROAD match: {interest_lower} -> found '{keyword}' in location data")
                        return True

            # 8. Reverse broad matching - check if location keywords match interest categories
            for category, keywords in broad_matches.items():
                if category == interest_lower:
                    continue
                for keyword in keywords:
                    if (keyword in location_name or keyword in location_description or 
                        keyword in location_category or any(keyword in tag for tag in location_tags)):
                        if interest_lower in category or category in interest_lower:
                            print(f"✅ REVERSE broad match: found '{keyword}', matches {interest_lower}")
                            return True

        print(f"❌ No match found for location {location.name} with interests {interests}")
        return False
    
    def _get_interest_keywords(self, interest) -> List[str]:
        """Get keywords associated with each interest type - IMPROVED VERSION"""
        
        # Handle both string and enum interests
        if hasattr(interest, 'value'):
            interest_str = interest.value
        else:
            interest_str = str(interest)
        
        # More comprehensive keyword mapping
        keyword_map = {
            'historical': ["historical", "history", "heritage", "monument", "ancient", "medieval", "empire", "kingdom", "dynasty", "archaeological", "ruins"],
            'religious': ["religious", "temple", "church", "mosque", "gurdwara", "monastery", "shrine", "sacred", "holy", "pilgrimage", "spiritual", "buddhist", "hindu", "islamic", "christian", "sikh", "jain"],
            'architectural': ["architecture", "palace", "fort", "building", "construction", "minaret", "dome", "tower", "castle", "citadel"],
            'cultural': ["cultural", "traditional", "folk", "art", "craft", "festival", "dance", "music"],
            'archaeological': ["archaeological", "ruins", "excavation", "artifact", "ancient", "prehistoric"],
            'royal_heritage': ["royal", "king", "queen", "emperor", "empire", "dynasty", "palace", "court"],
            'ancient_temples': ["temple", "shrine", "ancient", "deity", "worship", "sacred", "religious"],
            'forts_palaces': ["fort", "palace", "castle", "citadel", "fortress", "royal"],
            'unesco_sites': ["unesco", "world heritage", "protected", "heritage"]
        }
        
        interest_lower = interest_str.lower()
        
        # Return keywords for the interest, or just the interest itself if not found
        return keyword_map.get(interest_lower, [interest_lower])
    
    def _matches_periods(self, location: Location, preferred_periods: List[str]) -> bool:
        """Check if location matches preferred historical periods"""
        location_period = getattr(location, 'period', '').lower() if hasattr(location, 'period') else ""
        
        for period in preferred_periods:
            if period.lower() in location_period:
                return True
        
        return False
    
    def _matches_dynasties(self, location: Location, preferred_dynasties: List[str]) -> bool:
        """Check if location matches preferred dynasties"""
        location_dynasty = getattr(location, 'dynasty', '').lower() if hasattr(location, 'dynasty') else ""
        
        for dynasty in preferred_dynasties:
            if dynasty.lower() in location_dynasty:
                return True
        
        return False
    
    def _matches_regions(self, location: Location, preferred_regions: List[str]) -> bool:
        """Check if location is in preferred regions"""
        # This would need to be implemented based on your regional classification
        # For now, returning True as placeholder
        return True
    
    def _calculate_distance(self, point1: Dict[str, float], point2) -> float:
        """Calculate distance between two points in kilometers"""
        # Handle different coordinate formats
        if isinstance(point2, dict):
            lat2, lon2 = point2.get('lat', 0), point2.get('lng', 0)
        elif hasattr(point2, 'coordinates'):
            coords = point2.coordinates
            if isinstance(coords, dict):
                lat2, lon2 = coords.get('lat', 0), coords.get('lng', 0)
            elif isinstance(coords, (list, tuple)) and len(coords) >= 2:
                lat2, lon2 = coords[0], coords[1]
            else:
                return float('inf')
        else:
            return float('inf')
            
        lat1, lon1 = point1['lat'], point1['lng']
        
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon/2) * math.sin(delta_lon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance
    
    def _score_locations(self, locations: List[Location], prefs) -> List[Tuple[Location, float]]:
        """Score locations based on preference alignment"""
        scored = []
        
        for location in locations:
            score = 0.0
            
            # Interest alignment score (40% weight)
            interest_score = self._calculate_interest_score(location, prefs.interests)
            score += interest_score * 0.4
            
            # Historical significance score (20% weight)
            historical_score = self._calculate_historical_score(location, prefs)
            score += historical_score * 0.2
            
            # Accessibility score (20% weight)
            accessibility_score = self._calculate_accessibility_score(location, prefs)
            score += accessibility_score * 0.2
            
            # Distance score (20% weight)
            distance_score = self._calculate_distance_score(location, prefs)
            score += distance_score * 0.2
            
            scored.append((location, score))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
    def _calculate_interest_score(self, location: Location, interests) -> float:
        """Calculate how well location matches interests (0-1 scale)"""
        if not interests:
            return 0.5
        
        matches = 0
        for interest in interests:
            if self._matches_interests(location, [interest]):
                matches += 1
        
        return min(matches / len(interests), 1.0)
    
    def _calculate_historical_score(self, location: Location, prefs) -> float:
        """Calculate historical significance score"""
        score = 0.5  # Base score
        
        # Bonus for preferred periods
        if prefs.preferred_periods and self._matches_periods(location, prefs.preferred_periods):
            score += 0.3
        
        # Bonus for preferred dynasties
        if prefs.preferred_dynasties and self._matches_dynasties(location, prefs.preferred_dynasties):
            score += 0.2
        
        return min(score, 1.0)
    
    def _calculate_accessibility_score(self, location: Location, prefs) -> float:
        """Calculate accessibility score based on preferences"""
        # This would be enhanced with real accessibility data
        base_score = 0.7
        
        if prefs.accessibility_required:
            # Check if location has accessibility features
            # For now, returning reduced score as placeholder
            return 0.3
        
        return base_score
    
    def _calculate_distance_score(self, location: Location, prefs) -> float:
        """Calculate distance score - closer locations get higher scores"""
        if not prefs.start_location:
            return 0.5
        
        distance = self._calculate_distance(prefs.start_location, location)
        max_preferred_distance = prefs.max_distance_km or 500
        
        # Score decreases with distance
        score = max(0, 1 - (distance / max_preferred_distance))
        return score
    
    def _create_optimal_route(self, scored_locations: List[Tuple[Location, float]], prefs) -> Route:
        """Create optimal route from scored locations"""
        
        # Select top locations based on travel days
        max_locations = min(prefs.max_travel_days * 2, len(scored_locations))  # 2 locations per day max
        selected_locations = scored_locations[:max_locations]
        
        if not selected_locations:
            raise ValueError("No locations selected for route")
        
        # Create route locations and path with robust coordinate extraction
        route_locations = []
        path = []  # This will store the coordinate path
        for location, score in selected_locations:
            coords = location.coordinates
            # FIXED: Proper coordinate extraction
            if hasattr(coords, 'lat') and hasattr(coords, 'lng'):
                # Coordinates object with lat/lng properties
                coord_list = [float(coords.lat), float(coords.lng)]
            elif isinstance(coords, dict):
                # Dictionary format
                coord_list = [float(coords.get('lat', 0)), float(coords.get('lng', 0))]
            elif isinstance(coords, (list, tuple)) and len(coords) >= 2:
                # Array format
                coord_list = [float(coords[0]), float(coords[1])]
            else:
                # Fallback - this should not happen if data is correct
                print(f"Warning: Could not extract coordinates for {location.name}: {coords}")
                coord_list = [0, 0]
            # Debug: Print actual coordinates being used
            print(f"Location {location.name}: coordinates {coords} -> path coordinate {coord_list}")
            # Add to path
            path.append(coord_list)
            # Create RouteLocation object
            route_location = RouteLocation(
                name=location.name,
                coordinates=coord_list,
                description=f"{getattr(location, 'description', '')[:100]}... (Score: {score:.2f})"
            )
            route_locations.append(route_location)
        # Optimize order based on geographical proximity
        optimized_locations = self._optimize_route_order(route_locations, prefs.start_location)
        # Create optimized path (reorder path to match optimized locations)
        optimized_path = []
        for loc in optimized_locations:
            if isinstance(loc.coordinates, (list, tuple)) and len(loc.coordinates) >= 2:
                optimized_path.append(loc.coordinates)
        # Debug: Print final path
        print(f"Final optimized path: {optimized_path}")
        # Create route object
        route = Route(
            id=f"personalized_{random.randint(1000, 9999)}",
            name=f"Personalized {'/'.join(str(i) for i in prefs.interests[:2])} Route",
            description=f"Custom route for {prefs.max_travel_days} days based on your preferences",
            color="#e91e63",  # Pink color for personalized routes
            path=optimized_path,  # Use optimized path
            locations=optimized_locations
        )
        return route
    
    def _optimize_route_order(self, locations: List[RouteLocation], start_point: Optional[Dict[str, float]]) -> List[RouteLocation]:
        """Optimize the order of locations to minimize travel distance"""
        if len(locations) <= 2:
            return locations
        
        # Create distance matrix
        n = len(locations)
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Handle coordinate format
                    coord_i = locations[i].coordinates
                    coord_j = locations[j].coordinates
                    
                    if isinstance(coord_i, (list, tuple)) and isinstance(coord_j, (list, tuple)):
                        point_i = {'lat': coord_i[0], 'lng': coord_i[1]}
                        point_j = {'lat': coord_j[0], 'lng': coord_j[1]}
                        dist = self._calculate_distance(point_i, point_j)
                        distances[i][j] = dist
        
        # Simple nearest neighbor heuristic
        visited = [False] * n
        route_order = []
        
        # Start from location closest to start_point if provided
        if start_point:
            start_idx = 0
            min_start_dist = float('inf')
            for i in range(n):
                coord = locations[i].coordinates
                if isinstance(coord, (list, tuple)) and len(coord) >= 2:
                    point = {'lat': coord[0], 'lng': coord[1]}
                    dist = self._calculate_distance(start_point, point)
                    if dist < min_start_dist:
                        min_start_dist = dist
                        start_idx = i
        else:
            start_idx = 0
        
        current = start_idx
        visited[current] = True
        route_order.append(current)
        
        while len(route_order) < n:
            next_idx = None
            min_dist = float('inf')
            
            for i in range(n):
                if not visited[i] and distances[current][i] < min_dist:
                    min_dist = distances[current][i]
                    next_idx = i
            
            if next_idx is not None:
                visited[next_idx] = True
                route_order.append(next_idx)
                current = next_idx
        
        return [locations[i] for i in route_order]
    
    def get_nearby_historical_places(self, location: Dict[str, float], radius_km: int = 50, 
                                   interests = None) -> List[Dict[str, Any]]:
        """Get nearby historical places based on location and interests"""
        all_locations = self.kg_service.get_all_locations()
        nearby = []
        
        for loc in all_locations:
            distance = self._calculate_distance(location, loc)
            
            if distance <= radius_km:
                # Check interest match if specified
                if interests and not self._matches_interests(loc, interests):
                    continue
                
                nearby.append({
                    'location': loc.to_dict(),
                    'distance_km': round(distance, 1),
                    'interest_match': self._calculate_interest_score(loc, interests or [])
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        return nearby

    # ===== EXISTING FUNCTIONALITY (PRESERVED) =====
        
    def create_personalized_route(self, preferences):
        """
        Create a personalized route based on user preferences using
        sophisticated algorithms to find optimal paths.
        
        Parameters:
        - preferences: dict with keys:
            - interests: list of interests
            - startLocation: starting point ID
            - endLocation: ending point ID (optional)
            - maxDays: maximum duration in days
            - mustVisit: list of location IDs that must be included (optional)
            
        Returns:
        - A Route object with optimized path
        """
        # Check if this is a new-style preferences call
        if ('max_travel_days' in preferences or 
            'start_location' in preferences or 
            HAS_USER_PREFERENCES and isinstance(preferences, UserPreferences)):
            return self.create_personalized_route_with_preferences(preferences)
            
        # Original functionality for backward compatibility
        # Extract preferences
        interests = preferences.get('interests', [])
        start_location_id = preferences.get('startLocation')
        end_location_id = preferences.get('endLocation')
        max_days = preferences.get('maxDays', 7)
        must_visit = preferences.get('mustVisit', [])
        
        # Get all locations
        all_locations = self.kg_service.get_all_locations()
        
        # Filter locations based on interests and must-visit locations
        candidate_locations = self._filter_locations_by_interests(all_locations, interests)
        
        # Ensure must-visit locations are included
        must_visit_locations = []
        for loc_id in must_visit:
            location = self.kg_service.get_location_by_id(loc_id)
            if location and location not in candidate_locations:
                must_visit_locations.append(location)
        
        candidate_locations.extend(must_visit_locations)
        
        # Find start and end locations if specified
        start_location = None
        end_location = None
        
        if start_location_id:
            start_location = self.kg_service.get_location_by_id(start_location_id)
            if start_location and start_location not in candidate_locations:
                candidate_locations.append(start_location)
                
        if end_location_id:
            end_location = self.kg_service.get_location_by_id(end_location_id)
            if end_location and end_location not in candidate_locations:
                candidate_locations.append(end_location)
        
        # Calculate travel time matrix between locations
        distances = self._calculate_travel_matrix(candidate_locations)
        
        # Determine how many locations can be realistically visited in the given time
        avg_visit_duration = 1.0  # Average days to visit a location
        avg_travel_time = 0.5  # Average days to travel between locations
        
        max_locations = int(max_days / (avg_visit_duration + avg_travel_time))
        max_locations = min(max(max_locations, 3), len(candidate_locations))  # At least 3, at most all candidates
        
        # If we have more candidates than we can visit, prioritize them
        if len(candidate_locations) > max_locations:
            priority_locations = self._prioritize_locations(candidate_locations, interests, must_visit, max_locations)
        else:
            priority_locations = candidate_locations
            
        # Make sure start and end locations are included if specified
        if start_location and start_location not in priority_locations:
            priority_locations.append(start_location)
        if end_location and end_location not in priority_locations:
            priority_locations.append(end_location)
            
        # Get optimal route through selected locations
        optimal_route = self._find_optimal_route(priority_locations, distances, start_location, end_location)
        
        # Create a Route object
        route_name = f"Personalized {', '.join(interests[:2])} Route"
        route_description = f"A customized route based on your interests in {', '.join(interests)}"
        route_color = self._get_theme_color(interests)
        
        # Create path from location coordinates
        path = []
        for loc in optimal_route:
            coords = loc.coordinates
            if isinstance(coords, dict):
                path.append([coords['lat'], coords['lng']])
            elif isinstance(coords, (list, tuple)):
                path.append(list(coords))
        
        # Create RouteLocation objects
        route_locations = []
        for location in optimal_route:
            coords = location.coordinates
            if isinstance(coords, dict):
                coord_list = [coords['lat'], coords['lng']]
            elif isinstance(coords, (list, tuple)):
                coord_list = list(coords)
            else:
                coord_list = [0, 0]
                
            route_locations.append(RouteLocation(
                name=location.name,
                coordinates=coord_list,
                description=location.description[:100] + '...' if len(location.description) > 100 else location.description
            ))
            
        # Create and return Route object
        personalized_route = Route(
            id="custom",
            name=route_name,
            description=route_description,
            color=route_color,
            path=path,
            locations=route_locations
        )
        
        return personalized_route

    def _filter_locations_by_interests(self, locations, interests):
        """Filter locations based on user interests with scoring"""
        if not interests:
            # If no interests provided, return a limited selection of diverse locations
            return random.sample(locations, min(8, len(locations)))
            
        scored_locations = []
        
        for location in locations:
            score = 0
            
            # Score based on tags matching interests
            location_tags = getattr(location, 'tags', [])
            for interest in interests:
                interest_lower = interest.lower()
                for tag in location_tags:
                    if interest_lower in tag.lower():
                        score += 2
                        break
            
            # Score based on category
            location_category = getattr(location, 'category', '')
            for interest in interests:
                if interest.lower() in location_category.lower():
                    score += 2
                    break
                    
            # Score based on dynasty/period match
            location_dynasty = getattr(location, 'dynasty', '')
            location_period = getattr(location, 'period', '')
            for interest in interests:
                if (interest.lower() in location_dynasty.lower() or 
                    interest.lower() in location_period.lower()):
                    score += 1.5
                    break
                    
            # Score based on description and history (text matching)
            location_description = getattr(location, 'description', '')
            location_history = getattr(location, 'history', '')
            text = f"{location_description} {location_history}"
            for interest in interests:
                if interest.lower() in text.lower():
                    score += 1
                    break
                    
            # Add a small random factor for diversity
            score += random.uniform(0, 0.5)
                
            if score > 0:
                scored_locations.append((location, score))
        
        # Sort by score and return top locations
        scored_locations.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 10 for route planning feasibility
        top_locations = [loc for loc, _ in scored_locations[:10]]
        
        return top_locations
    
    def _prioritize_locations(self, locations, interests, must_visit, max_count):
        """Prioritize locations based on significance and relevance to interests"""
        # Must-visit locations have highest priority
        must_visit_locations = [loc for loc in locations if loc.id in must_visit]
        remaining_slots = max_count - len(must_visit_locations)
        
        if remaining_slots <= 0:
            return must_visit_locations[:max_count]
            
        # Score remaining locations
        remaining_locations = [loc for loc in locations if loc.id not in must_visit]
        scored_locations = []
        
        for location in remaining_locations:
            score = 0
            
            # UNESCO sites get a significance boost
            location_tags = getattr(location, 'tags', [])
            if any('unesco' in tag.lower() for tag in location_tags):
                score += 3
                
            # Score based on interest match
            for interest in interests:
                interest_lower = interest.lower()
                # Check tags
                if any(interest_lower in tag.lower() for tag in location_tags):
                    score += 2
                
                # Check category, dynasty, description
                location_category = getattr(location, 'category', '')
                location_dynasty = getattr(location, 'dynasty', '')
                location_description = getattr(location, 'description', '')
                
                if interest_lower in location_category.lower():
                    score += 1.5
                if interest_lower in location_dynasty.lower():
                    score += 1
                if interest_lower in location_description.lower():
                    score += 0.5
            
            # Add a small random factor for diversity
            score += random.uniform(0, 0.5)
            scored_locations.append((location, score))
            
        # Sort by score
        scored_locations.sort(key=lambda x: x[1], reverse=True)
        top_remaining = [loc for loc, _ in scored_locations[:remaining_slots]]
        
        # Combine must-visit with top remaining
        prioritized = must_visit_locations + top_remaining
        return prioritized
    
    def _calculate_travel_matrix(self, locations):
        """Calculate travel time matrix between locations using Haversine distance"""
        if not locations:
            return np.array([])
            
        n = len(locations)
        coords = np.zeros((n, 2))
        
        for i, loc in enumerate(locations):
            location_coords = loc.coordinates
            if isinstance(location_coords, dict):
                coords[i, 0] = location_coords['lat']
                coords[i, 1] = location_coords['lng']
            elif isinstance(location_coords, (list, tuple)) and len(location_coords) >= 2:
                coords[i, 0] = location_coords[0]
                coords[i, 1] = location_coords[1]
            
        # Calculate pairwise distances
        distances = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    distances[i, j] = 0
                else:
                    # Haversine formula for distance between two points on a sphere
                    lat1, lon1 = coords[i]
                    lat2, lon2 = coords[j]
                    
                    # Convert to radians
                    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
                    
                    # Haversine formula
                    dlon = lon2 - lon1
                    dlat = lat2 - lat1
                    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
                    c = 2 * np.arcsin(np.sqrt(a))
                    r = 6371  # Radius of Earth in kilometers
                    distances[i, j] = c * r
                    
        return distances
    
    def _find_optimal_route(self, locations, distances, start_location=None, end_location=None):
        """Find optimal route through locations, respecting start and end constraints"""
        if len(locations) <= 2:
            return locations
            
        # If start and end are specified, solve an open TSP
        if start_location and end_location and start_location != end_location:
            return self._solve_open_tsp(locations, distances, start_location, end_location)
        
        # Otherwise solve a standard TSP with optional starting point
        start_idx = None
        if start_location:
            for i, loc in enumerate(locations):
                if loc.id == start_location.id:
                    start_idx = i
                    break
                    
        return self._solve_tsp(locations, distances, start_idx)
    
    def _solve_tsp(self, locations, distances, start_idx=None):
        """Solve a Traveling Salesperson Problem"""
        n = len(locations)
        if n <= 1:
            return locations
            
        # If start index is not specified, use a simple heuristic
        if start_idx is None:
            # Find the location that minimizes the sum of distances to all other locations
            total_distances = np.sum(distances, axis=1)
            start_idx = np.argmin(total_distances)
            
        # Greedy nearest neighbor algorithm
        unvisited = set(range(n))
        unvisited.remove(start_idx)
        path = [start_idx]
        
        while unvisited:
            last = path[-1]
            # Find closest unvisited location
            next_idx = min(unvisited, key=lambda i: distances[last, i])
            path.append(next_idx)
            unvisited.remove(next_idx)
            
        # Return locations in the computed path order
        return [locations[i] for i in path]
    
    def _solve_open_tsp(self, locations, distances, start_location, end_location):
        """Solve an open TSP with fixed start and end points"""
        n = len(locations)
        if n <= 2:
            return locations
            
        # Find indices of start and end locations
        start_idx = None
        end_idx = None
        
        for i, loc in enumerate(locations):
            if loc.id == start_location.id:
                start_idx = i
            if loc.id == end_location.id:
                end_idx = i
                
        if start_idx is None or end_idx is None:
            # Fall back to standard TSP if start or end not found
            return self._solve_tsp(locations, distances)
            
        # Handle special case: only start and end
        if n == 2:
            return [locations[start_idx], locations[end_idx]]
            
        # Solve with start and end fixed
        unvisited = set(range(n))
        unvisited.remove(start_idx)
        unvisited.remove(end_idx)
        
        path = [start_idx]
        
        # Greedily add each next closest location
        while unvisited:
            last = path[-1]
            next_idx = min(unvisited, key=lambda i: distances[last, i])
            path.append(next_idx)
            unvisited.remove(next_idx)
            
        # Add end location
        path.append(end_idx)
        
        # Return locations in the computed path order
        return [locations[i] for i in path]
    
    def _get_theme_color(self, interests):
        """Get an appropriate color based on interests"""
        # Map common interests to colors
        interest_colors = {
            'temple': '#9C27B0',  # Purple
            'religious': '#9C27B0',
            'buddhist': '#FF9800',  # Orange
            'hindu': '#9C27B0',
            'jain': '#9C27B0',
            'mughal': '#4CAF50',  # Green
            'islamic': '#4CAF50',
            'architecture': '#3F51B5',  # Indigo
            'heritage': '#3F51B5',
            'history': '#795548',  # Brown
            'ancient': '#795548',
            'medieval': '#795548',
            'nature': '#009688',  # Teal
            'beach': '#03A9F4',  # Light Blue
            'mountain': '#009688',
            'wildlife': '#8BC34A',  # Light Green
            'food': '#FF5722',  # Deep Orange
            'cuisine': '#FF5722',
            'art': '#E91E63',  # Pink
            'craft': '#E91E63',
            'sculpture': '#E91E63'
        }
        
        # Check if any interest matches our predefined themes
        for interest in interests:
            interest_lower = str(interest).lower()
            for key, color in interest_colors.items():
                if key in interest_lower or interest_lower in key:
                    return color
                    
        # Default color if no match found
        return '#3f51b5'  # Indigo blue
    
    def optimize_route(self, existing_route, optimization_params):
        """Optimize an existing route based on new parameters"""
        # This method can be implemented to modify existing routes
        # based on new constraints like time, budget, accessibility
        
        # For now, return the existing route
        # You can enhance this with actual optimization logic
        return existing_route