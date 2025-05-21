# app.py

import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from services.kg_service import KnowledgeGraphService
from services.route_service import RouteService
from services.chatbot_service import ChatbotService
import uuid
import os
import logging

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
CORS(app)  # Enable CORS for all routes

# Initialize services with proper error handling
try:
    # Check if we should use placeholder data
    use_placeholder = os.environ.get('USE_PLACEHOLDER', 'true').lower() == 'true'
    logger.info(f"Initializing services with use_placeholder={use_placeholder}")
    
    kg_service = KnowledgeGraphService(use_placeholder=use_placeholder)
    route_service = RouteService(kg_service)
    chatbot_service = ChatbotService(kg_service, route_service)
    
    logger.info("Services initialized successfully")
except Exception as e:
    logger.error(f"Error initializing services: {e}")
    raise

# Session management (simplified; use a proper session management in production)
active_sessions = {}

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'service': 'cupe-kg-backend',
        'timestamp': datetime.datetime.now().isoformat()
    })

# Location Endpoints
@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all available locations"""
    try:
        locations = kg_service.get_all_locations()
        return jsonify([loc.to_dict() for loc in locations])
    except Exception as e:
        logger.error(f"Error fetching locations: {e}")
        return jsonify({'error': 'Failed to fetch locations'}), 500

@app.route('/api/place-info', methods=['GET'])
def get_place_info():
    """Get detailed info about a specific location"""
    location_name = request.args.get('name')
    if not location_name:
        return jsonify({'error': 'No location name provided'}), 400
    
    try:
        location = kg_service.get_location_by_id(location_name)
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        # Get related locations
        related = kg_service.get_related_locations(location_name)
        
        # Combine location data with related locations
        response = location.to_dict()
        response['relatedLocations'] = related
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error fetching place info for {location_name}: {e}")
        return jsonify({'error': 'Failed to fetch place information'}), 500

@app.route('/api/locations/period/<period>', methods=['GET'])
def get_locations_by_period(period):
    """Get locations from a specific historical period"""
    try:
        locations = kg_service.get_locations_by_period(period)
        return jsonify([loc.to_dict() for loc in locations])
    except Exception as e:
        logger.error(f"Error fetching locations by period {period}: {e}")
        return jsonify({'error': 'Failed to fetch locations by period'}), 500

@app.route('/api/locations/category/<category>', methods=['GET'])
def get_locations_by_category(category):
    """Get locations filtered by category"""
    try:
        locations = kg_service.get_locations_by_category(category)
        return jsonify([location.to_dict() for location in locations])
    except Exception as e:
        logger.error(f"Error fetching locations by category {category}: {e}")
        return jsonify({'error': 'Failed to fetch locations by category'}), 500

@app.route('/api/related-locations/<location_id>', methods=['GET'])
def get_related_locations(location_id):
    """Get locations related to a specific location"""
    try:
        related = kg_service.get_related_locations(location_id)
        return jsonify(related)
    except Exception as e:
        logger.error(f"Error fetching related locations for {location_id}: {e}")
        return jsonify({'error': 'Failed to fetch related locations'}), 500

# Route Endpoints
@app.route('/api/routes', methods=['GET'])
def get_routes():
    """Get all predefined routes"""
    try:
        routes = route_service.get_all_routes()
        return jsonify([route.to_dict() for route in routes])
    except Exception as e:
        logger.error(f"Error fetching routes: {e}")
        return jsonify({'error': 'Failed to fetch routes'}), 500

@app.route('/api/routes/<route_id>', methods=['GET'])
def get_route(route_id):
    """Get a specific route by ID"""
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
    """Get routes matching a specific theme"""
    try:
        routes = route_service.get_routes_by_theme(theme)
        return jsonify([route.to_dict() for route in routes])
    except Exception as e:
        logger.error(f"Error fetching routes by theme {theme}: {e}")
        return jsonify({'error': 'Failed to fetch routes by theme'}), 500

@app.route('/api/personalized-route', methods=['POST'])
def create_personalized_route():
    """Create a personalized route based on preferences"""
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    preferences = request.json
    required_fields = ['interests', 'startLocation', 'maxDays']
    
    # Check for required fields
    for field in required_fields:
        if field not in preferences:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        route = route_service.create_personalized_route(preferences)
        return jsonify(route.to_dict())
    except Exception as e:
        logger.error(f"Error creating personalized route: {e}")
        return jsonify({'error': str(e)}), 500

# Search Endpoints
@app.route('/api/search', methods=['GET'])
def search():
    """Basic search for locations by keyword"""
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
    """Advanced search with multiple criteria"""
    if not request.json:
        return jsonify({'error': 'No search criteria provided'}), 400
    
    try:
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
                if hasattr(loc, 'tags'):
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
    except Exception as e:
        logger.error(f"Error in advanced search: {e}")
        return jsonify({'error': 'Advanced search operation failed'}), 500

# Chatbot Endpoints
@app.route('/api/chatbot/ask', methods=['POST'])
def ask_question():
    """Answer a question from the chatbot"""
    if not request.json or 'question' not in request.json:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        question = request.json['question']
        location_id = request.json.get('locationId')
        
        # Get or create session ID
        session_id = request.json.get('sessionId')
        if not session_id:
            session_id = str(uuid.uuid4())
            active_sessions[session_id] = {'created_at': datetime.datetime.now()}
        
        # Process the query
        result = chatbot_service.process_query(session_id, question, location_id)
        
        # Add session ID to response
        result['sessionId'] = session_id
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing chatbot query: {e}")
        return jsonify({
            'error': 'Failed to process your question', 
            'sessionId': session_id if 'session_id' in locals() else str(uuid.uuid4())
        }), 500

@app.route('/api/chatbot/recommend', methods=['POST'])
def get_recommendations():
    """Get personalized location recommendations"""
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    try:
        preferences = request.json
        recommendations = chatbot_service.get_recommendations(preferences)
        
        return jsonify(recommendations)
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        return jsonify({'error': 'Failed to generate recommendations'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    # Print startup message
    logger.info(f"Starting CuPe-KG backend on port {port}, debug={debug}")
    
    # Run the Flask app
    app.run(debug=debug, host='0.0.0.0', port=port)