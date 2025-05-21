# api/routes.py
from flask import Blueprint, jsonify, request
from services.kg_service import KnowledgeGraphService
from services.route_service import RouteService
from api.chatbot_api import register_chatbot_routes

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