import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.kg_service import KnowledgeGraphService
from services.route_service import RouteService
from services.chatbot_service import ChatbotService
import uuid
import os
import logging

# Try to import advanced preference models
try:
    from models.user_preferences import UserPreferences
    # from models.interest_type import InterestType
    HAS_USER_PREFERENCES = True
except ImportError:
    print("UserPreferences or InterestType not found. Using fallback.")
    HAS_USER_PREFERENCES = False
    class InterestType:
        HISTORICAL = "historical"
        RELIGIOUS = "religious"
        ARCHITECTURAL = "architectural"
        CULTURAL = "cultural"
        ARCHAEOLOGICAL = "archaeological"
        ROYAL_HERITAGE = "royal_heritage"
        ANCIENT_TEMPLES = "ancient_temples"
        FORTS_PALACES = "forts_palaces"
        UNESCO_SITES = "unesco_sites"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize services
try:
    use_placeholder = os.environ.get('USE_PLACEHOLDER', 'true').lower() == 'true'
    logger.info(f"Initializing services with use_placeholder={use_placeholder}")
    kg_service = KnowledgeGraphService(use_placeholder=use_placeholder)
    route_service = RouteService(kg_service)
    chatbot_service = ChatbotService(kg_service, route_service)
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    raise

active_sessions = {}

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'cupe-kg-backend',
        'timestamp': datetime.datetime.now().isoformat()
    })

# ------------------ Location Endpoints ------------------
@app.route('/api/locations', methods=['GET'])
def get_locations():
    try:
        locations = kg_service.get_all_locations()
        return jsonify([loc.to_dict() for loc in locations])
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        return jsonify({'error': 'Failed to fetch locations'}), 500

@app.route('/api/place-info', methods=['GET'])
def get_place_info():
    location_name = request.args.get('name')
    if not location_name:
        return jsonify({'error': 'No location name provided'}), 400
    try:
        location = kg_service.get_location_by_id(location_name)
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        related = kg_service.get_related_locations(location_name)
        response = location.to_dict()
        response['relatedLocations'] = related
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error fetching place info for {location_name}: {e}")
        return jsonify({'error': 'Failed to fetch place information'}), 500

@app.route('/api/locations/period/<period>', methods=['GET'])
def get_locations_by_period(period):
    try:
        locations = kg_service.get_locations_by_period(period)
        return jsonify([loc.to_dict() for loc in locations])
    except Exception as e:
        logger.error(f"Error fetching locations by period {period}: {e}")
        return jsonify({'error': 'Failed to fetch locations by period'}), 500

@app.route('/api/locations/category/<category>', methods=['GET'])
def get_locations_by_category(category):
    try:
        locations = kg_service.get_locations_by_category(category)
        return jsonify([location.to_dict() for location in locations])
    except Exception as e:
        logger.error(f"Error fetching locations by category {category}: {e}")
        return jsonify({'error': 'Failed to fetch locations by category'}), 500

@app.route('/api/related-locations/<location_id>', methods=['GET'])
def get_related_locations(location_id):
    try:
        related = kg_service.get_related_locations(location_id)
        return jsonify(related)
    except Exception as e:
        logger.error(f"Error fetching related locations for {location_id}: {e}")
        return jsonify({'error': 'Failed to fetch related locations'}), 500

# ------------------ Route Endpoints ------------------
@app.route('/api/routes', methods=['GET'])
def get_routes():
    try:
        routes = route_service.get_all_routes()
        return jsonify([route.to_dict() for route in routes])
    except Exception as e:
        logger.error(f"Error fetching routes: {e}")
        return jsonify({'error': 'Failed to fetch routes'}), 500

@app.route('/api/routes/<route_id>', methods=['GET'])
def get_route(route_id):
    try:
        route = route_service.get_route_by_id(route_id)
        if not route:
            return jsonify({'error': 'Route not found'}), 404
        return jsonify(route.to_dict())
    except Exception as e:
        logger.error(f"Error fetching route {route_id}: {e}")
        return jsonify({'error': 'Failed to fetch route'}), 500

@app.route('/api/routes/theme/<theme>', methods=['GET'])
def get_routes_by_theme(theme):
    try:
        routes = route_service.get_routes_by_theme(theme)
        return jsonify([route.to_dict() for route in routes])
    except Exception as e:
        logger.error(f"Error fetching routes by theme {theme}: {e}")
        return jsonify({'error': 'Failed to fetch routes by theme'}), 500

@app.route('/api/personalized-route', methods=['POST'])
def create_personalized_route():
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    preferences = request.json
    required_fields = ['interests', 'startLocation', 'maxDays']
    for field in required_fields:
        if field not in preferences:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    try:
        route = route_service.create_personalized_route(preferences)
        return jsonify(route.to_dict())
    except Exception as e:
        logger.error(f"Error creating personalized route: {e}")
        return jsonify({'error': str(e)}), 500

# ------------------ Improved: Personalized Route Advanced ------------------
@app.route('/api/personalized-route-advanced', methods=['POST'])
def create_personalized_route_advanced():
    """Create a personalized route based on detailed user preferences"""
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    try:
        logger.info(f"Received advanced route preferences: {request.json}")
        
        # Use the enhanced route service method directly
        route = route_service.create_personalized_route_with_preferences(request.json)
        
        response_data = {
            'route': route.to_dict(),
            'preferences_applied': request.json,
            'total_locations': len(route.locations),
            'estimated_duration_days': request.json.get('max_travel_days', 7)
        }
        
        logger.info(f"Advanced route created successfully with {len(route.locations)} locations")
        return jsonify(response_data)
    
    except ValueError as e:
        logger.error(f"ValueError creating advanced route: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error creating advanced route: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to create personalized route'}), 500

@app.route('/api/nearby-places', methods=['GET'])
def get_nearby_places():
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius_km = int(request.args.get('radius', 50))
        interests = request.args.get('interests', '').split(',') if request.args.get('interests') else []
        location = {'lat': lat, 'lng': lng}
        interest_list = [i.strip() for i in interests if i.strip()]
        nearby_places = route_service.get_nearby_historical_places(location, radius_km, interest_list)
        return jsonify({
            'location': location,
            'radius_km': radius_km,
            'interests': interest_list,
            'nearby_places': nearby_places,
            'total_found': len(nearby_places)
        })
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid parameters provided'}), 400
    except Exception as e:
        logger.error(f"Error fetching nearby places: {e}")
        return jsonify({'error': 'Failed to fetch nearby places'}), 500

# ------------------ Improved: Preference Suggestions ------------------
@app.route('/api/preference-suggestions', methods=['GET'])
def get_preference_suggestions():
    """Get suggestions for user preferences based on available data"""
    try:
        all_locations = kg_service.get_all_locations()
        
        # Extract available periods
        periods = set()
        dynasties = set()
        categories = set()
        
        for location in all_locations:
            if hasattr(location, 'period') and location.period:
                periods.add(location.period)
            if hasattr(location, 'dynasty') and location.dynasty:
                dynasties.add(location.dynasty)
            if hasattr(location, 'category') and location.category:
                categories.add(location.category)
        
        # Fixed interests list (simplified, no dependency on enum fallback)
        available_interests = [
            'historical', 'religious', 'architectural', 'cultural',
            'archaeological', 'royal_heritage', 'ancient_temples', 
            'forts_palaces', 'unesco_sites'
        ]
        
        suggestions = {
            'available_interests': available_interests,
            'available_periods': sorted(list(periods)),
            'available_dynasties': sorted(list(dynasties)),
            'available_categories': sorted(list(categories)),
            'transport_modes': ['car', 'train', 'bus', 'flight', 'mixed'],
            'budget_ranges': ['low', 'medium', 'high'],
            'crowd_preferences': ['low', 'medium', 'high'],
            'difficulty_levels': ['easy', 'medium', 'difficult']
        }
        
        logger.info(f"Preference suggestions: {len(periods)} periods, {len(dynasties)} dynasties")
        return jsonify(suggestions)
    
    except Exception as e:
        logger.error(f"Error fetching preference suggestions: {e}")
        return jsonify({'error': 'Failed to fetch suggestions'}), 500
# Add this debug endpoint to your app_backend.py

@app.route('/api/debug-locations', methods=['POST'])
def debug_locations():
    """Debug endpoint to see what locations match preferences"""
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    try:
        preferences = request.json
        all_locations = kg_service.get_all_locations()
        
        debug_info = {
            'total_locations': len(all_locations),
            'preferences_received': preferences,
            'location_details': []
        }
        
        # Check each location against preferences
        for location in all_locations:
            location_info = {
                'name': location.name,
                'category': getattr(location, 'category', 'N/A'),
                'dynasty': getattr(location, 'dynasty', 'N/A'), 
                'period': getattr(location, 'period', 'N/A'),
                'tags': getattr(location, 'tags', []),
                'description': getattr(location, 'description', 'N/A')[:100] + '...',
                'matches_interests': False,
                'matches_periods': False,
                'matches_dynasties': False
            }
            
            # Check interest matches
            for interest in preferences.get('interests', []):
                interest_lower = interest.lower()
                location_tags = [tag.lower() for tag in getattr(location, 'tags', [])]
                location_category = getattr(location, 'category', '').lower()
                location_description = getattr(location, 'description', '').lower()
                
                if (interest_lower in location_tags or 
                    interest_lower in location_category or 
                    interest_lower in location_description):
                    location_info['matches_interests'] = True
                    break
            
            # Check period matches
            location_period = getattr(location, 'period', '').lower()
            for period in preferences.get('preferred_periods', []):
                if period.lower() in location_period:
                    location_info['matches_periods'] = True
                    break
            
            # Check dynasty matches
            location_dynasty = getattr(location, 'dynasty', '').lower()
            for dynasty in preferences.get('preferred_dynasties', []):
                if dynasty.lower() in location_dynasty:
                    location_info['matches_dynasties'] = True
                    break
            
            debug_info['location_details'].append(location_info)
        
        return jsonify(debug_info)
    
    except Exception as e:
        logger.error(f"Debug error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/route-optimization', methods=['POST'])
def optimize_existing_route():
    if not request.json:
        return jsonify({'error': 'No optimization parameters provided'}), 400
    try:
        route_id = request.json.get('route_id')
        optimization_params = request.json.get('optimization_params', {})
        if not route_id:
            return jsonify({'error': 'Route ID is required'}), 400
        existing_route = route_service.get_route_by_id(route_id)
        if not existing_route:
            return jsonify({'error': 'Route not found'}), 404
        optimized_route = route_service.optimize_route(existing_route, optimization_params)
        return jsonify({
            'original_route': existing_route.to_dict(),
            'optimized_route': optimized_route.to_dict(),
            'optimization_applied': optimization_params
        })
    except Exception as e:
        logger.error(f"Error optimizing route: {e}")
        return jsonify({'error': 'Failed to optimize route'}), 500

# ------------------ Search Endpoints ------------------
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400
    try:
        results = kg_service.search_locations(query)
        return jsonify([location.to_dict() for location in results])
    except Exception as e:
        logger.error(f"Error searching locations with query '{query}': {e}")
        return jsonify({'error': 'Search operation failed'}), 500

@app.route('/api/advanced-search', methods=['POST'])
def advanced_search():
    if not request.json:
        return jsonify({'error': 'No search criteria provided'}), 400
    try:
        criteria = request.json
        all_locations = kg_service.get_all_locations()
        results = all_locations
        if 'category' in criteria and criteria['category']:
            results = [loc for loc in results if loc.category == criteria['category']]
        if 'period' in criteria and criteria['period']:
            results = [loc for loc in results if criteria['period'] in loc.period]
        if 'dynasty' in criteria and criteria['dynasty']:
            results = [loc for loc in results if criteria['dynasty'] in loc.dynasty]
        if 'tags' in criteria and criteria['tags']:
            results = [loc for loc in results if any(tag in getattr(loc, 'tags', []) for tag in criteria['tags'])]
        if 'query' in criteria and criteria['query']:
            query = criteria['query'].lower()
            results = [loc for loc in results if query in f"{loc.name} {loc.description} {loc.history}".lower()]
        return jsonify([location.to_dict() for location in results])
    except Exception as e:
        logger.error(f"Error in advanced search: {e}")
        return jsonify({'error': 'Advanced search operation failed'}), 500

# ------------------ Chatbot Endpoints ------------------
@app.route('/api/chatbot/ask', methods=['POST'])
def chatbot_ask():
    try:
        if not request.json or 'question' not in request.json:
            return jsonify({
                'error': 'No question provided',
                'answer': 'Please provide a question to get started.',
                'confidence': 0.1,
                'followUpQuestions': []
            }), 400
        
        question = request.json['question']
        session_id = request.json.get('sessionId', str(uuid.uuid4()))
        location_id = request.json.get('locationId')
        
        logger.info(f"Processing chatbot query: '{question}' for session: {session_id}")
        
        # Process the query using the chatbot service
        result = chatbot_service.process_query(
            query=question,
            location_id=location_id,
            session_id=session_id
        )
        
        # Ensure required fields are present
        if not isinstance(result, dict):
            result = {'answer': str(result)}
            
        result.setdefault('answer', 'I apologize, but I could not process your request.')
        result.setdefault('confidence', 0.5)
        result.setdefault('followUpQuestions', [])
        result['sessionId'] = session_id
        
        logger.info(f"Chatbot response: confidence={result.get('confidence', 'N/A')}")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error processing chatbot query: {e}", exc_info=True)
        return jsonify({
            'error': 'Failed to process query',
            'answer': "I'm having trouble processing your request. Please try asking about a specific heritage site or historical period.",
            'confidence': 0.3,
            'followUpQuestions': [
                "Tell me about the Taj Mahal",
                "What is the Golden Triangle route?",
                "Show me Buddhist heritage sites"
            ],
            'sessionId': request.json.get('sessionId', str(uuid.uuid4()))
        }), 500

@app.route('/api/chatbot/recommend', methods=['POST'])
def get_recommendations():
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    try:
        preferences = request.json
        recommendations = chatbot_service.get_recommendations(preferences)
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Failed to generate recommendations'}), 500

@app.route('/api/debug/test-distance', methods=['GET'])
def debug_test_distance():
    try:
        # Test coordinates - Bangalore to Mysore
        bangalore = {'lat': 12.9716, 'lng': 77.5946}
        
        # Get Mysore location from your data
        all_locations = kg_service.get_all_locations()
        mysore_location = None
        
        for loc in all_locations:
            if 'mysore' in loc.name.lower():
                mysore_location = loc
                break
        
        if not mysore_location:
            return jsonify({'error': 'Mysore not found in locations'})
        
        # Calculate distance using route service
        distance = route_service._calculate_distance(bangalore, mysore_location)
        
        return jsonify({
            'bangalore': bangalore,
            'mysore_name': mysore_location.name,
            'mysore_coordinates': mysore_location.coordinates,
            'mysore_coordinates_type': str(type(mysore_location.coordinates)),
            'calculated_distance': distance
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'traceback': str(e.__traceback__)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    logger.info(f"Starting CuPe-KG backend on port {port}, debug={debug}")
    print(f"User Preferences Model Available: {HAS_USER_PREFERENCES}")
    app.run(debug=debug, host='0.0.0.0', port=port)
