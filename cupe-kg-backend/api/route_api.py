# api/route_api.py
from flask import Blueprint, jsonify, request
from services.route_service import RouteService
from models.route import Route, RouteLocation

route_bp = Blueprint('routes', __name__, url_prefix='/api/routes')
route_service = RouteService()

def register_route_routes(app):
    app.register_blueprint(route_bp)

@route_bp.route('/', methods=['GET'])
def get_all_routes():
    routes = route_service.get_all_routes()
    return jsonify([route.to_dict() for route in routes])

@route_bp.route('/<route_id>', methods=['GET'])
def get_route(route_id):
    route = route_service.get_route_by_id(route_id)
    if not route:
        return jsonify({'error': 'Route not found'}), 404
    
    return jsonify(route.to_dict())

@route_bp.route('/theme/<theme>', methods=['GET'])
def get_routes_by_theme(theme):
    routes = route_service.get_routes_by_theme(theme)
    return jsonify([route.to_dict() for route in routes])

@route_bp.route('/personalized', methods=['POST'])
def create_personalized_route():
    """Create a personalized route based on preferences"""
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    preferences = request.json
    required_fields = ['interests', 'startLocation', 'endLocation', 'maxDays']
    
    # Check for required fields
    for field in required_fields:
        if field not in preferences:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        route = route_service.create_personalized_route(preferences)
        return jsonify(route.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@route_bp.route('/nearby-attractions', methods=['GET'])
def get_nearby_attractions():
    """Get attractions near a specific location"""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    if not lat or not lng:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    
    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return jsonify({'error': 'Invalid latitude or longitude'}), 400
    
    # This would use a more sophisticated algorithm to find nearby attractions
    # For now, we'll return a placeholder
    return jsonify([
        {
            'id': 'nearby1',
            'name': 'Nearby Attraction 1',
            'description': 'A nearby attraction',
            'distance': 5.2,  # km
            'coordinates': {'lat': lat + 0.05, 'lng': lng + 0.05}
        },
        {
            'id': 'nearby2',
            'name': 'Nearby Attraction 2',
            'description': 'Another nearby attraction',
            'distance': 8.7,  # km
            'coordinates': {'lat': lat - 0.08, 'lng': lng - 0.03}
        }
    ])