# api/chatbot_api.py (updated)
from flask import Blueprint, jsonify, request
from services.chatbot_service import ChatbotService
from services.kg_service import KnowledgeGraphService
from services.route_service import RouteService

# Create blueprint
chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize services
kg_service = KnowledgeGraphService()
route_service = RouteService()
chatbot_service = ChatbotService(kg_service, route_service)

def register_chatbot_routes(app):
    app.register_blueprint(chatbot_bp)

@chatbot_bp.route('/ask', methods=['POST'])
def ask_question():
    if not request.json or 'question' not in request.json:
        return jsonify({'error': 'No question provided'}), 400
    
    question = request.json['question']
    location_id = request.json.get('locationId')
    
    # Process the query using the chatbot service
    result = chatbot_service.process_query(question, location_id)
    
    return jsonify(result)

@chatbot_bp.route('/recommend', methods=['POST'])
def get_recommendations():
    if not request.json:
        return jsonify({'error': 'No preferences provided'}), 400
    
    preferences = request.json
    recommendations = chatbot_service.get_recommendations(preferences)
    
    return jsonify(recommendations)