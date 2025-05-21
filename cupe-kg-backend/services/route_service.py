# services/route_service.py

import numpy as np
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
import random
from models.route import Route, RouteLocation

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
        
    def create_personalized_route(self, preferences):
        """
        Create a personalized route based on user preferences using
        sophisticated algorithms to find optimal paths.
        
        Parameters:
        - preferences: dict with keys:
            - interests: list of interests
            - startLocation:starting point ID
            - endLocation: ending point ID (optional)
            - maxDays: maximum duration in days
            - mustVisit: list of location IDs that must be included (optional)
            
        Returns:
        - A Route object with optimized path
        """
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
        path = [[loc.coordinates['lat'], loc.coordinates['lng']] for loc in optimal_route]
        
        # Create RouteLocation objects
        route_locations = []
        for location in optimal_route:
            route_locations.append(RouteLocation(
                name=location.name,
                coordinates=[location.coordinates['lat'], location.coordinates['lng']],
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
            for interest in interests:
                interest_lower = interest.lower()
                for tag in location.tags:
                    if interest_lower in tag.lower():
                        score += 2
                        break
            
            # Score based on category
            for interest in interests:
                if interest.lower() in location.category.lower():
                    score += 2
                    break
                    
            # Score based on dynasty/period match
            for interest in interests:
                if (interest.lower() in location.dynasty.lower() or 
                    interest.lower() in location.period.lower()):
                    score += 1.5
                    break
                    
            # Score based on description and history (text matching)
            text = f"{location.description} {location.history}"
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
            if any('unesco' in tag.lower() for tag in location.tags):
                score += 3
                
            # Score based on interest match
            for interest in interests:
                interest_lower = interest.lower()
                # Check tags
                if any(interest_lower in tag.lower() for tag in location.tags):
                    score += 2
                
                # Check category, dynasty, description
                if interest_lower in location.category.lower():
                    score += 1.5
                if interest_lower in location.dynasty.lower():
                    score += 1
                if interest_lower in location.description.lower():
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
            coords[i, 0] = loc.coordinates['lat']
            coords[i, 1] = loc.coordinates['lng']
            
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
        """Get a appropriate color based on interests"""
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
            interest_lower = interest.lower()
            for key, color in interest_colors.items():
                if key in interest_lower or interest_lower in key:
                    return color
                    
        # Default color if no match found
        return '#3f51b5'  # Indigo blue