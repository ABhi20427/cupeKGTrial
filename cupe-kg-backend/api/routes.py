# api/routes.py
from flask import Blueprint, jsonify, request, current_app
from services.kg_service import KnowledgeGraphService
from services.route_service import RouteService
from api.chatbot_api import register_chatbot_routes
from models.user import UserPreferences

# Flag to check if UserPreferences class is available
HAS_USER_PREFERENCES = True

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Initialize services
kg_service = KnowledgeGraphService()
route_service = RouteService()

def register_routes(app):
    app.register_blueprint(api_bp)
    register_chatbot_routes(app)

# Location endpoints
@api_bp.route('/locations', methods=['GET'])
def get_locations():
    locations = kg_service.get_all_locations()
    return jsonify([location.to_dict() for location in locations])

@api_bp.route('/place-info', methods=['GET'])
def get_place_info():
    location_name = request.args.get('name')
    if not location_name:
        return jsonify({'error': 'No location name provided'}), 400
    
    location = kg_service.get_location_by_id(location_name)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
@api_bp.route('/place-info', methods=['GET'])
def get_place_info():
    location_name = request.args.get('name')
    if not location_name:
        return jsonify({'error': 'No location name provided'}), 400
    
    location = kg_service.get_location_by_id(location_name)
    if not location:
        return jsonify({'error': 'Location not found'}), 404
    
    # Get related locations for this location
    related = kg_service.get_related_locations(location_name)
    
    # Combine all data
    response = location.to_dict()
    response['relatedLocations'] = related
    
    return jsonify(response)

@api_bp.route('/locations/period/<period>', methods=['GET'])
def get_locations_by_period(period):
    locations = kg_service.get_locations_by_period(period)
    return jsonify([location.to_dict() for location in locations])

@api_bp.route('/locations/category/<category>', methods=['GET'])
def get_locations_by_category(category):
    """Get locations filtered by category (historical, religious, cultural)"""
    all_locations = kg_service.get_all_locations()
    filtered = [loc for loc in all_locations if loc.category == category]
    return jsonify([location.to_dict() for location in filtered])

# Search endpoint with more detailed implementation
@api_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    
    # Simple search implementation
    all_locations = kg_service.get_all_locations()
    results = []
    
    for location in all_locations:
        # Search in name, description, history
        search_text = f"{location.name} {location.description} {location.history} {location.dynasty}".lower()
        
        # Add cultural facts and tags to search text
        for fact in location.cultural_facts:
            search_text += " " + fact.lower()
        for tag in location.tags:
            search_text += " " + tag.lower()
        
        # Check if query is in search text
        if query.lower() in search_text:
            results.append(location.to_dict())
    
    return jsonify(results)

# Advanced search with more complex filtering
@api_bp.route('/advanced-search', methods=['POST'])
def advanced_search():
    if not request.json:
        return jsonify({'error': 'No search criteria provided'}), 400
    
    criteria = request.json
    all_locations = kg_service.get_all_locations()
    results = all_locations
    
    # Apply filters
    if 'category' in criteria and criteria['category']:
        results = [loc for loc in results if loc.category == criteria['category']]
    
    if 'period' in criteria and criteria['period']:
        results = [loc for loc in results if criteria['period'] in loc.period]
    
    if 'dynasty' in criteria and criteria['dynasty']:
        results = [loc for loc in results if criteria['dynasty'] in loc.dynasty]
    
    if 'tags' in criteria and criteria['tags']:
        # Filter locations that contain ANY of the specified tags
        tag_results = []
        for loc in results:
            for tag in criteria['tags']:
                if tag in loc.tags:
                    tag_results.append(loc)
                    break
        results = tag_results
    
    if 'query' in criteria and criteria['query']:
        # Text search similar to simple search
        query = criteria['query'].lower()
        query_results = []
        
        for location in results:
            search_text = f"{location.name} {location.description} {location.history}".lower()
            if query in search_text:
                query_results.append(location)
        
        results = query_results
    
    return jsonify([location.to_dict() for location in results])

# Advanced personalized route creation
@api_bp.route('/personalized-route-advanced', methods=['POST'])
def create_advanced_personalized_route():
    """Create an advanced personalized route with enhanced preferences"""
    try:
        if not request.json:
            return jsonify({'error': 'No preferences provided'}), 400
        
        preferences_data = request.json
        current_app.logger.info(f"Received advanced route preferences: {preferences_data}")
        
        # Convert to UserPreferences object
        try:
            if HAS_USER_PREFERENCES:
                user_prefs = UserPreferences(**preferences_data)
            else:
                # Fallback for basic dict handling
                user_prefs = type('UserPreferences', (), preferences_data)()
                
        except Exception as e:
            current_app.logger.error(f"Error creating UserPreferences object: {e}")
            return jsonify({'error': f'Invalid preferences format: {str(e)}'}), 400
        
        # Create the route
        try:
            route = route_service.create_personalized_route_with_preferences(user_prefs)
            
            if not route:
                raise ValueError("Route service returned None")
                
            if not route.locations or len(route.locations) == 0:
                raise ValueError("No locations in generated route")
            
        except ValueError as ve:
            current_app.logger.error(f"ValueError creating advanced route: {ve}")
            
            # Try with relaxed preferences
            current_app.logger.info("Trying with relaxed preferences...")
            
            # Create relaxed preferences
            relaxed_prefs_data = preferences_data.copy()
            relaxed_prefs_data['preferred_dynasties'] = []  # Clear dynasty filter
            relaxed_prefs_data['preferred_periods'] = []    # Clear period filter
            relaxed_prefs_data['max_distance_km'] = 2000    # Increase distance
            
            if HAS_USER_PREFERENCES:
                relaxed_prefs = UserPreferences(**relaxed_prefs_data)
            else:
                relaxed_prefs = type('UserPreferences', (), relaxed_prefs_data)()
            
            try:
                route = route_service.create_personalized_route_with_preferences(relaxed_prefs)
                current_app.logger.info("Successfully created route with relaxed preferences")
            except Exception as relaxed_error:
                current_app.logger.error(f"Even relaxed preferences failed: {relaxed_error}")
                return jsonify({
                    'error': 'No suitable locations found for your preferences',
                    'suggestion': 'Try selecting broader interests or increasing your travel distance',
                    'debug_info': {
                        'original_error': str(ve),
                        'relaxed_error': str(relaxed_error),
                        'received_preferences': preferences_data
                    }
                }), 400
        
        # Convert route to API response format
        response_data = {
            'id': route.id,
            'name': route.name,
            'description': route.description,
            'color': route.color,
            'path': route.path,
            'locations': [
                {
                    'name': loc.name,
                    'coordinates': loc.coordinates,
                    'description': loc.description
                } for loc in route.locations
            ],
            'total_days': len(route.locations) * 2,  # Estimate 2 days per location
            'total_cost': 15000 * len(route.locations),  # Estimate cost
            'optimization_metrics': {
                'total_locations': len(route.locations),
                'estimated_distance': sum([100] * (len(route.locations) - 1)) if len(route.locations) > 1 else 0
            }
        }
        
        current_app.logger.info(f"Successfully created advanced route with {len(route.locations)} locations")
        return jsonify(response_data), 200
        
    except Exception as e:
        current_app.logger.error(f"Unexpected error in advanced route creation: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': 'Internal server error while creating route',
            'message': str(e),
            'suggestion': 'Please try again with different preferences'
        }), 500


# Debug endpoint for location data
@api_bp.route('/debug/locations', methods=['GET'])
def debug_locations():
    """Debug endpoint to check location data"""
    try:
        all_locations = kg_service.get_all_locations()
        
        location_summary = []
        for loc in all_locations[:10]:  # Show first 10 locations
            location_summary.append({
                'name': loc.name,
                'category': getattr(loc, 'category', 'N/A'),
                'dynasty': getattr(loc, 'dynasty', 'N/A'),
                'tags': getattr(loc, 'tags', []),
                'has_coordinates': hasattr(loc, 'coordinates') and loc.coordinates is not None
            })
        
        return jsonify({
            'total_locations': len(all_locations),
            'sample_locations': location_summary,
            'available_categories': list(set([getattr(loc, 'category', 'unknown') for loc in all_locations])),
            'available_dynasties': list(set([getattr(loc, 'dynasty', 'unknown') for loc in all_locations])),
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500