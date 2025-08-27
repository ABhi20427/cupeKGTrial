# services/chatbot_service.py

import random
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ChatbotService:
    def __init__(self, kg_service, route_service):
        self.kg_service = kg_service
        self.route_service = route_service
        self.conversation_history = {}  # Store conversation history by session
        self.load_models()
        
    def load_models(self):
        """Load NLP models for question answering and intent detection"""
        try:
            # Initialize TF-IDF vectorizer for similarity matching
            self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
            
            # Prepare FAQ corpus
            self.faqs = self._prepare_faqs()
            if self.faqs:
                self.faq_vectors = self.vectorizer.fit_transform([q for q, _ in self.faqs])
            else:
                self.faq_vectors = None
                
            print("Chatbot models loaded successfully")
            
        except Exception as e:
            print(f"Error loading NLP models: {e}")
            self.vectorizer = None
            self.faq_vectors = None
    
    def _prepare_faqs(self):
        """Prepare a comprehensive corpus of FAQs for matching"""
        return [
            # Taj Mahal FAQs
            ("What is the best time to visit Taj Mahal", 
             "The best time to visit the Taj Mahal is from October to March when the weather is pleasant. For the most magical experience, visit at sunrise when the marble takes on a soft pink glow, or at sunset when it appears golden. The monument is closed on Fridays."),
            
            ("How to reach Taj Mahal", 
             "The Taj Mahal is located in Agra, Uttar Pradesh. The nearest airport is Agra Airport (12 km away). By train, Agra Cantt and Agra Fort stations are well-connected. From Delhi, you can take the Yamuna Expressway (3-4 hours by road) or the high-speed trains like Gatimaan Express."),
            
            ("History of Taj Mahal", 
             "The Taj Mahal was built by Mughal Emperor Shah Jahan between 1632-1653 as a mausoleum for his beloved wife Mumtaz Mahal. It's considered the finest example of Mughal architecture, combining elements from Islamic, Persian, Ottoman Turkish and Indian architectural styles."),
            
            # Hampi FAQs
            ("What is the best time to visit Hampi", 
             "The best time to visit Hampi is from October to March when the weather is pleasant with temperatures between 15°C to 30°C. Avoid summer months (April-June) when temperatures soar above 40°C. The annual Hampi Festival in November is ideal for experiencing local culture."),
            
            ("How do I reach Hampi", 
             "To reach Hampi, the nearest airport is Ballari (60 km) or Hubli Airport (143 km). The closest railway station is Hospet Junction (12 km) with connections to Bangalore, Hyderabad, and Goa. From Hospet, take local buses, auto-rickshaws, or taxis to Hampi."),
             
            ("History of Hampi", 
             "Hampi was the capital of the Vijayanagara Empire (1336-1646 CE), once one of the richest cities in the world. The ruins showcase stunning temple architecture including the Virupaksha Temple and stone chariot at Vittala Temple. UNESCO recognized it as a World Heritage site in 1986."),
            
            ("What are the must see spots in Hampi", 
             "Must-see spots in Hampi include the Virupaksha Temple (still active), Vittala Temple with its famous stone chariot, Lotus Mahal, Elephant Stables, Hemakuta Hill for sunset views, and the Royal Enclosure with Mahanavami Dibba platform."),
             
            # General India Tourism
            ("What is the Buddhist Trail", 
             "The Buddhist Trail connects key sites of Buddhist heritage across northern India, including Bodh Gaya (where Buddha attained enlightenment), Sarnath (first sermon), Kushinagar (Buddha's death), Lumbini (birthplace), Rajgir, and Nalanda. This circuit traces the life and teachings of Buddha."),
            
            ("Best time to visit India", 
             "The best time to visit India varies by region. Generally, October to March is ideal for most of India with pleasant weather. Hill stations are best in summer (April-June). Avoid monsoon season (July-September) except for Kerala where it's beautiful. Winter (December-February) is perfect for most heritage sites."),
            
            ("Golden Triangle route", 
             "The Golden Triangle is India's most popular tourist circuit covering Delhi (capital with Mughal and British heritage), Agra (home to Taj Mahal), and Jaipur (Pink City with Rajput palaces). This route offers a perfect introduction to India's history, architecture, and culture in 5-7 days."),
            
            # Specific Dynasties and Periods
            ("Mughal architecture", 
             "Mughal architecture (1526-1857) blends Islamic, Persian, Turkish, and Indian styles. Key features include large bulbous domes, slender minarets, pointed arches, and extensive use of red sandstone and white marble. Famous examples include Taj Mahal, Red Fort, and Humayun's Tomb."),
            
            ("Vijayanagara Empire", 
             "The Vijayanagara Empire (1336-1646) was a South Indian empire with its capital at Hampi. Known for its military prowess, trade networks, and architectural achievements, it was one of the most powerful empires in Indian history before falling to the Deccan Sultanates."),
            
            ("Chola dynasty temples", 
             "The Chola dynasty (9th-13th centuries) built magnificent temples featuring towering gopurams (gateway towers), intricate bronze sculptures, and sophisticated hydraulic systems. UNESCO World Heritage Chola temples include Brihadeshwara Temple in Thanjavur and temples at Darasuram and Gangaikonda Cholapuram."),
            
            # Travel Planning
            ("How to plan historical route in India", 
             "To plan a historical route in India: 1) Choose a theme (Mughal heritage, temple architecture, Buddhist sites). 2) Select a region to minimize travel time. 3) Allow 2-3 days per major site. 4) Consider seasonal weather. 5) Book accommodations in advance. 6) Hire local guides for deeper insights. Popular themes include Golden Triangle, Buddhist Circuit, and Temple Trails of South India."),
        ]
    
    def process_query(self, query, location_id=None, session_id=None):
        """
        Process a user query with enhanced context awareness
        
        Parameters:
        - query: The user's question
        - location_id: ID of the location currently being viewed (optional)
        - session_id: Unique identifier for the conversation (optional)
        
        Returns:
        - Response object with answer and suggested follow-ups
        """
        if not session_id:
            session_id = f"session_{random.randint(1000, 9999)}"
            
        # Initialize conversation history if new session
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
            
        # Add the current query to history
        self.conversation_history[session_id].append({"role": "user", "text": query})
        
        # Get context for the question
        context = self._get_context(session_id, location_id)
        
        # Process the query through multiple strategies
        response = self._process_query_intelligently(query, context, location_id)
        
        # Generate follow-up suggestions based on the conversation
        suggestions = self._generate_dynamic_suggestions(query, response['answer'], location_id)
        
        # Add response to conversation history
        self.conversation_history[session_id].append({"role": "assistant", "text": response['answer']})
        
        # Return formatted response
        return {
            'answer': response['answer'],
            'confidence': response.get('confidence', 0.7),
            'followUpQuestions': suggestions
        }
    
    def _process_query_intelligently(self, query, context, location_id):
        """Intelligently process query using multiple strategies"""
        
        # Strategy 1: Try FAQ matching first
        faq_response = self._match_faq(query)
        if faq_response and faq_response['confidence'] > 0.6:
            return faq_response
            
        # Strategy 2: Intent-based processing
        intent = self._detect_intent(query)
        if intent:
            return self._handle_intent(intent, query, location_id, context)
            
        # Strategy 3: Location-specific information
        if location_id:
            location_response = self._get_location_specific_info(query, location_id)
            if location_response['confidence'] > 0.5:
                return location_response
                
        # Strategy 4: Keyword-based matching with knowledge graph
        kg_response = self._search_knowledge_graph(query)
        if kg_response['confidence'] > 0.5:
            return kg_response
            
        # Strategy 5: Fallback response
        return self._generate_contextual_fallback(query, context)
    
    def _get_context(self, session_id, location_id=None):
        """Get relevant context for responding to the query"""
        context = ""
        
        # Add location-specific context if available
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                context += f"Current location: {location.name}. "
                context += f"Description: {location.description}. "
                context += f"Historical period: {location.period}. "
                context += f"Dynasty: {location.dynasty}. "
                context += f"History: {location.history}. "
                
                # Add cultural facts if available
                if hasattr(location, 'cultural_facts') and location.cultural_facts:
                    context += "Cultural facts: " + " ".join(location.cultural_facts[:2]) + ". "
        
        # Add conversation history context (last 4 exchanges)
        if session_id in self.conversation_history:
            history = self.conversation_history[session_id][-8:]  # Last 4 exchanges
            for msg in history:
                context += f"{msg['role'].title()}: {msg['text']} "
        
        return context
        
    def _match_faq(self, query):
        """Enhanced FAQ matching with better similarity scoring"""
        if not self.faqs or not self.vectorizer or self.faq_vectors is None:
            return None
            
        try:
            # Transform the query using the same vectorizer
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarity with all FAQs
            similarities = cosine_similarity(query_vector, self.faq_vectors).flatten()
            
            # Get the best match
            best_match_idx = similarities.argmax()
            confidence = float(similarities[best_match_idx])
            
            # Return if confidence is above threshold
            if confidence > 0.3:  # Lowered threshold for better matching
                return {
                    'answer': self.faqs[best_match_idx][1],
                    'confidence': confidence
                }
        except Exception as e:
            print(f"Error in FAQ matching: {e}")
            
        return None
    
    def _detect_intent(self, query):
        """Enhanced intent detection using regex patterns"""
        intents = {
            'greeting': r'\b(hello|hi|hey|greetings|namaste|good\s+(morning|afternoon|evening))\b',
            'farewell': r'\b(bye|goodbye|see you|farewell|thanks|thank you)\b',
            'location_info': r'\b(tell me about|info about|information about|what is|describe|explain)\s+(.+)',
            'best_time': r'\b(best time|when to visit|visiting season|weather|climate)\b',
            'how_to_reach': r'\b(how to reach|how to get to|directions to|travel to|route to)\b',
            'history': r'\b(history|historical|heritage|past|ancient|built by|founded by)\b',
            'architecture': r'\b(architecture|architectural|design|style|built|construction)\b',
            'culture': r'\b(culture|cultural|tradition|festival|art|customs)\b',
            'route_planning': r'\b(route|itinerary|plan|trip|tour|visit|travel plan)\b',
            'must_see': r'\b(must see|must visit|top attractions|highlights|famous|popular)\b',
            'dynasty': r'\b(dynasty|empire|ruler|king|emperor|sultan)\b'
        }
        
        query_lower = query.lower()
        detected_intents = []
        
        for intent, pattern in intents.items():
            if re.search(pattern, query_lower):
                detected_intents.append(intent)
                
        # Return the most specific intent or the first one found
        return detected_intents[0] if detected_intents else None
    
    def _handle_intent(self, intent, query, location_id, context):
        """Handle specific intents with appropriate responses"""
        
        if intent == 'greeting':
            return {
                'answer': "Namaste! I'm your CuPe-KG cultural heritage guide. I can help you explore India's rich history, plan heritage routes, and discover fascinating stories about our monuments and traditions. What would you like to know?",
                'confidence': 0.9
            }
            
        elif intent == 'farewell':
            return {
                'answer': "Thank you for exploring India's cultural heritage with me! Have a wonderful journey through our incredible history and traditions. Namaste! 🙏",
                'confidence': 0.9
            }
            
        elif intent in ['location_info', 'history', 'architecture', 'culture']:
            # Extract location name from query
            location_name = self._extract_location_name(query)
            if location_name:
                return self._get_location_info(location_name, location_id)
            elif location_id:
                # Use current location
                location = self.kg_service.get_location_by_id(location_id)
                return self._get_location_info(location.name if location else "", location_id)
                
        elif intent == 'best_time':
            location_name = self._extract_location_name(query)
            return self._get_best_time_info(location_name or "India")
            
        elif intent == 'how_to_reach':
            location_name = self._extract_location_name(query)
            return self._get_travel_info(location_name)
            
        elif intent == 'route_planning':
            return self._suggest_routes(query)
            
        elif intent == 'must_see':
            location_name = self._extract_location_name(query)
            return self._get_must_see_attractions(location_name)
            
        elif intent == 'dynasty':
            dynasty_name = self._extract_dynasty_name(query)
            return self._get_dynasty_info(dynasty_name)
        
        # Fallback to general processing
        return self._search_knowledge_graph(query)
    
    def _extract_location_name(self, query):
        """Extract location names from the query"""
        # Common location patterns
        location_patterns = [
            r'(?:about|of|in|visit|reach|to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:temple|fort|palace|mahal|heritage)',
            r'(Taj\s+Mahal|Red\s+Fort|Golden\s+Temple|Hampi|Khajuraho|Ajanta|Ellora|Konark|Sanchi|Bodh\s+Gaya)',
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_dynasty_name(self, query):
        """Extract dynasty names from the query"""
        dynasties = ['Mughal', 'Chola', 'Vijayanagara', 'Mauryan', 'Gupta', 'Delhi Sultanate', 'Maratha', 'Rajput']
        for dynasty in dynasties:
            if dynasty.lower() in query.lower():
                return dynasty
        return None
    
    def _search_knowledge_graph(self, query):
        """Search the knowledge graph for relevant information"""
        try:
            # Get all locations from knowledge graph
            all_locations = self.kg_service.get_all_locations()
            
            query_lower = query.lower()
            best_matches = []
            
            for location in all_locations:
                score = 0
                search_text = f"{location.name} {location.description} {location.history} {location.dynasty} {location.period}".lower()
                
                # Add cultural facts and tags to search text
                if hasattr(location, 'cultural_facts'):
                    search_text += " " + " ".join(location.cultural_facts).lower()
                if hasattr(location, 'tags'):
                    search_text += " " + " ".join(location.tags).lower()
                
                # Calculate relevance score
                query_words = query_lower.split()
                for word in query_words:
                    if len(word) > 2:  # Ignore short words
                        if word in search_text:
                            score += search_text.count(word)
                
                if score > 0:
                    best_matches.append((location, score))
            
            # Sort by relevance score
            best_matches.sort(key=lambda x: x[1], reverse=True)
            
            if best_matches:
                location, score = best_matches[0]
                
                # Create rich response
                response = f"{location.name} is a {location.category} site from the {location.period} period. "
                response += f"{location.description} "
                
                if location.dynasty and location.dynasty != "Unknown":
                    response += f"It was built during the {location.dynasty} era. "
                
                if hasattr(location, 'cultural_facts') and location.cultural_facts:
                    response += f"Cultural insight: {random.choice(location.cultural_facts)} "
                
                return {
                    'answer': response.strip(),
                    'confidence': min(0.8, score / 10)  # Normalize confidence
                }
        
        except Exception as e:
            print(f"Error searching knowledge graph: {e}")
        
        return {'answer': '', 'confidence': 0.0}
    
    def _generate_dynamic_suggestions(self, query, answer, location_id):
        """Generate dynamic follow-up suggestions based on context"""
        suggestions = []
        
        # Location-specific suggestions
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                suggestions.extend([
                    f"Best time to visit {location.name}",
                    f"How to reach {location.name}",
                    f"Cultural significance of {location.name}",
                    f"Architecture of {location.name}"
                ])
        
        # Query-based suggestions
        query_lower = query.lower()
        
        if 'history' in query_lower or 'historical' in query_lower:
            suggestions.extend([
                "Tell me about Mughal architecture",
                "What is the Vijayanagara Empire?",
                "Show me Buddhist heritage sites"
            ])
        
        elif 'time' in query_lower or 'visit' in query_lower:
            suggestions.extend([
                "Best time to visit Rajasthan",
                "Weather in Kerala",
                "Festival seasons in India"
            ])
        
        elif 'route' in query_lower or 'plan' in query_lower:
            suggestions.extend([
                "Golden Triangle route",
                "Buddhist circuit plan",
                "South India temple trail"
            ])
        
        elif 'temple' in query_lower:
            suggestions.extend([
                "Chola dynasty temples",
                "Cave temples of India",
                "Temple architecture styles"
            ])
        
        # Default suggestions if none generated
        if not suggestions:
            suggestions = [
                "Tell me about the Taj Mahal",
                "Plan a heritage route",
                "Buddhist trail in India",
                "Mughal monuments"
            ]
        
        return suggestions[:4]  # Return max 4 suggestions
    
    def _get_location_info(self, location_name, location_id=None):
        """Get comprehensive information about a location"""
        try:
            # Try to find the location in our database
            all_locations = self.kg_service.get_all_locations()
            matching_location = None
            
            for location in all_locations:
                if (location_name.lower() in location.name.lower() or 
                    location.name.lower() in location_name.lower()):
                    matching_location = location
                    break
            
            if matching_location:
                # Create rich, detailed response
                response = f"{matching_location.name} is {matching_location.description} "
                
                if matching_location.period and matching_location.period != "Unknown":
                    response += f"Dating back to the {matching_location.period}, "
                
                if matching_location.dynasty and matching_location.dynasty != "Unknown":
                    response += f"it was built during the {matching_location.dynasty} period. "
                
                if matching_location.history:
                    response += f"{matching_location.history} "
                
                # Add cultural facts
                if hasattr(matching_location, 'cultural_facts') and matching_location.cultural_facts:
                    response += f"Cultural insight: {random.choice(matching_location.cultural_facts)} "
                
                return {
                    'answer': response.strip(),
                    'confidence': 0.9
                }
            
            # If no exact match, provide general guidance
            return {
                'answer': f"I don't have specific information about {location_name} in my database. However, I can help you explore other famous heritage sites like the Taj Mahal, Hampi ruins, Khajuraho temples, or Ajanta caves. What type of heritage site interests you most?",
                'confidence': 0.4
            }
        
        except Exception as e:
            print(f"Error getting location info: {e}")
            return self._generate_contextual_fallback(location_name, "")
    
    def _get_best_time_info(self, location_name):
        """Provide best time to visit information"""
        # Predefined best time information for major destinations
        best_times = {
            'taj mahal': "October to March is ideal for visiting the Taj Mahal. Early morning (sunrise) or late afternoon provides the best lighting and fewer crowds.",
            'hampi': "October to March offers pleasant weather (15-30°C). The Hampi Festival in November is particularly special.",
            'rajasthan': "October to March is perfect for Rajasthan. Avoid summer months when temperatures exceed 45°C.",
            'kerala': "October to March for general tourism. June to September (monsoon) is beautiful but wet.",
            'delhi': "October to March has pleasant weather. Avoid May-June (extreme heat) and July-September (monsoon).",
            'goa': "November to February is peak season with perfect weather and minimal rainfall.",
            'india': "Generally, October to March is ideal for most of India, with cool and dry weather perfect for sightseeing."
        }
        
        location_lower = location_name.lower()
        for key, info in best_times.items():
            if key in location_lower or location_lower in key:
                return {
                    'answer': info,
                    'confidence': 0.8
                }
        
        return {
            'answer': f"For most heritage sites in India including {location_name}, October to March is generally the best time to visit with pleasant weather and clear skies. Avoid extreme summer (April-June) and heavy monsoon (July-September) unless you're visiting hill stations.",
            'confidence': 0.6
        }
    
    def _get_travel_info(self, location_name):
        """Provide travel information for reaching destinations"""
        if not location_name:
            return {
                'answer': "Please specify the destination you'd like to reach, and I'll provide detailed travel information including flights, trains, and road routes.",
                'confidence': 0.3
            }
        
        # You could enhance this with actual route data from your knowledge graph
        return {
            'answer': f"To reach {location_name}, I'd recommend checking the nearest airport, railway station, and road connections. Most major heritage sites in India are well-connected by rail and road. Would you like me to suggest a complete travel itinerary including {location_name}?",
            'confidence': 0.6
        }
    
    def _suggest_routes(self, query):
        """Suggest heritage routes based on query"""
        route_keywords = {
            'golden triangle': "The Golden Triangle (Delhi-Agra-Jaipur) covers India's most iconic monuments including Red Fort, Taj Mahal, and Hawa Mahal. Perfect 5-7 day introduction to Indian heritage.",
            'buddhist': "The Buddhist Circuit includes Bodh Gaya (enlightenment), Sarnath (first sermon), Kushinagar (death), and Rajgir (monsoon retreats). Traces Buddha's life journey.",
            'south india': "South India Temple Trail covers Mahabalipuram's shore temples, Thanjavur's Brihadeshwara Temple, Madurai's Meenakshi Temple, and Hampi's Vijayanagara ruins.",
            'rajasthan': "Rajasthan Heritage Circuit: Jaipur (Pink City), Udaipur (Lake City), Jodhpur (Blue City), and Jaisalmer (Golden City) - showcasing Rajput grandeur.",
            'mughal': "Mughal Heritage Route: Delhi (Red Fort, Humayun's Tomb), Agra (Taj Mahal, Fatehpur Sikri), and extending to Lahore's Mughal monuments."
        }
        
        query_lower = query.lower()
        for keyword, description in route_keywords.items():
            if keyword in query_lower:
                return {
                    'answer': description,
                    'confidence': 0.8
                }
        
        return {
            'answer': "I can help you plan various heritage routes! Popular options include the Golden Triangle (Delhi-Agra-Jaipur), Buddhist Circuit, South India Temple Trail, or Rajasthan's Royal Circuit. What type of heritage interests you most - Mughal architecture, ancient temples, Buddhist sites, or royal palaces?",
            'confidence': 0.7
        }
    
    def _get_must_see_attractions(self, location_name):
        """Get must-see attractions for a location"""
        attractions = {
            'hampi': "Must-see in Hampi: Virupaksha Temple (active worship), Vittala Temple with stone chariot, Lotus Mahal, Elephant Stables, Hemakuta Hill for sunset, and Royal Enclosure.",
            'delhi': "Delhi highlights: Red Fort, India Gate, Humayun's Tomb, Qutub Minar, Lotus Temple, Akshardham, and bustling Chandni Chowk market.",
            'agra': "Agra essentials: Taj Mahal (sunrise/sunset), Agra Fort, Fatehpur Sikri, and Mehtab Bagh for Taj views across Yamuna river.",
            'jaipur': "Jaipur must-sees: Amber Fort, City Palace, Hawa Mahal, Jantar Mantar observatory, and vibrant local bazaars."
        }
        
        if location_name:
            location_lower = location_name.lower()
            for key, info in attractions.items():
                if key in location_lower:
                    return {
                        'answer': info,
                        'confidence': 0.8
                    }
        
        return {
            'answer': f"I'd love to suggest must-see attractions for {location_name}! Could you be more specific about the destination? I have detailed information about major heritage sites across India.",
            'confidence': 0.5
        }
    
    def _get_dynasty_info(self, dynasty_name):
        """Provide information about historical dynasties"""
        dynasties = {
            'mughal': "The Mughal Empire (1526-1857) created iconic monuments like the Taj Mahal, Red Fort, and Fatehpur Sikri. Known for Indo-Islamic architecture blending Persian, Turkish, and Indian styles.",
            'vijayanagara': "The Vijayanagara Empire (1336-1646) with capital at Hampi was South India's most powerful kingdom. Famous for massive temple complexes and sophisticated urban planning.",
            'chola': "The Chola Dynasty (9th-13th centuries) built magnificent temples with towering gopurams. UNESCO World Heritage Chola temples showcase Dravidian architecture at its peak.",
            'mauryan': "The Mauryan Empire (322-185 BCE) under Ashoka spread Buddhism across India. Famous for rock edicts, stupas at Sanchi, and the lion capital (India's national emblem)."
        }
        
        if dynasty_name:
            dynasty_lower = dynasty_name.lower()
            for key, info in dynasties.items():
                if key in dynasty_lower:
                    return {
                        'answer': info,
                        'confidence': 0.8
                    }
        
        return {
            'answer': "India has been ruled by many great dynasties including the Mauryans, Guptas, Cholas, Delhi Sultanates, Mughals, and Marathas. Each left distinctive architectural and cultural legacies. Which dynasty interests you most?",
            'confidence': 0.6
        }
    
    def _generate_contextual_fallback(self, query, context):
        """Generate contextual fallback responses"""
        fallbacks = [
            "I'm still learning about India's vast cultural heritage. Could you ask me about specific monuments like the Taj Mahal, Hampi ruins, or Khajuraho temples?",
            "That's an interesting question! I specialize in Indian heritage sites, historical periods, and cultural routes. Try asking about a specific monument, dynasty, or region.",
            "I'd love to help you explore Indian culture! Could you be more specific - are you interested in temple architecture, Mughal monuments, Buddhist sites, or travel planning?",
            "While I'm still expanding my knowledge, I can definitely help with major heritage sites, historical periods, and travel routes across India. What aspect interests you most?"
        ]
        
        return {
            'answer': random.choice(fallbacks),
            'confidence': 0.3
        }
    
    def get_recommendations(self, preferences):
        """Generate personalized recommendations based on user preferences"""
        try:
            # This would use your route service and user preferences
            # For now, providing a structured response
            return {
                'recommendations': [
                    {
                        'name': 'Golden Triangle',
                        'description': 'Classic Delhi-Agra-Jaipur circuit',
                        'duration': '5-7 days',
                        'highlights': ['Taj Mahal', 'Red Fort', 'Hawa Mahal']
                    }
                ],
                'message': 'Based on your preferences, here are some curated heritage routes!'
            }
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return {
                'recommendations': [],
                'message': 'I can help you plan heritage routes! What type of sites interest you most?'
            }# services/chatbot_service.py - COMPLETE IMPLEMENTATION

import re
import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class ChatbotService:
    def __init__(self, kg_service, route_service):
        self.kg_service = kg_service
        self.route_service = route_service
        self.conversation_history = {}
        
        # Initialize FAQ database
        self.faq_database = self._initialize_faq()
        
        # Initialize intent patterns
        self.intent_patterns = self._initialize_intent_patterns()
    
    def _initialize_faq(self):
        """Initialize FAQ database with common tourism questions"""
        return {
            "what is the best time to visit": {
                "answer": "The best time to visit most heritage sites in India is from October to March when the weather is pleasant. However, specific recommendations vary by region.",
                "confidence": 0.8
            },
            "how to reach": {
                "answer": "Most heritage sites are well-connected by road, rail, and air. I can help you plan specific routes based on your starting location.",
                "confidence": 0.8
            },
            "entry fee": {
                "answer": "Entry fees vary by site. UNESCO World Heritage sites typically charge ₹30-40 for Indians and $10-15 for foreign tourists. Some sites offer combined tickets.",
                "confidence": 0.7
            },
            "opening hours": {
                "answer": "Most heritage sites are open from sunrise to sunset (approximately 6 AM to 6 PM). Some sites like the Taj Mahal have special timings and are closed on Fridays.",
                "confidence": 0.8
            },
            "photography": {
                "answer": "Photography is generally allowed in most heritage sites, but there may be restrictions in certain areas. Video cameras might require additional fees.",
                "confidence": 0.7
            }
        }
    
    def _initialize_intent_patterns(self):
        """Initialize intent recognition patterns"""
        return {
            "history": r"\b(history|historical|ancient|dynasty|built|constructed|when|period|era)\b",
            "travel": r"\b(visit|travel|trip|journey|route|how to reach|transportation)\b", 
            "information": r"\b(tell me|about|what is|describe|information|details)\b",
            "recommendation": r"\b(recommend|suggest|best|top|popular|famous)\b",
            "timing": r"\b(time|when|hours|open|close|timing|schedule)\b",
            "cost": r"\b(cost|price|fee|ticket|entry|expensive|budget)\b",
            "location": r"\b(where|location|address|find|situated|located)\b"
        }
    
    def process_query(self, query, location_id=None, session_id=None):
        """Main method to process user queries"""
        try:
            # Initialize session if not exists
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            # Add user query to history
            self.conversation_history[session_id].append({"role": "user", "text": query})
            
            # Get context for the response
            context = self._get_context(session_id, location_id)
            
            # Process the query intelligently
            response = self._process_query_intelligently(query, context, location_id)
            
            # Generate follow-up suggestions
            suggestions = self._generate_dynamic_suggestions(query, response['answer'], location_id)
            
            # Add response to history
            self.conversation_history[session_id].append({"role": "assistant", "text": response['answer']})
            
            return {
                'answer': response['answer'],
                'confidence': response.get('confidence', 0.7),
                'followUpQuestions': suggestions
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'answer': "I apologize, but I'm experiencing some technical difficulties. Please try asking about a specific heritage site.",
                'confidence': 0.3,
                'followUpQuestions': [
                    "Tell me about the Taj Mahal",
                    "What is the Golden Triangle route?",
                    "Show me Buddhist heritage sites"
                ]
            }
    
    def _process_query_intelligently(self, query, context, location_id):
        """Intelligently process query using multiple strategies"""
        
        # Strategy 1: Try FAQ matching first
        faq_response = self._match_faq(query)
        if faq_response and faq_response['confidence'] > 0.6:
            return faq_response
            
        # Strategy 2: Intent-based processing
        intent = self._detect_intent(query)
        if intent:
            return self._handle_intent(intent, query, location_id, context)
            
        # Strategy 3: Location-specific information
        if location_id:
            location_response = self._get_location_specific_info(query, location_id)
            if location_response['confidence'] > 0.5:
                return location_response
                
        # Strategy 4: Keyword-based matching with knowledge graph
        kg_response = self._search_knowledge_graph(query)
        if kg_response['confidence'] > 0.5:
            return kg_response
            
        # Strategy 5: Fallback response
        return self._generate_contextual_fallback(query, context)
    
    def _match_faq(self, query):
        """Match query against FAQ database"""
        query_lower = query.lower()
        best_match = None
        highest_score = 0
        
        for faq_key, faq_data in self.faq_database.items():
            # Simple keyword matching
            keywords = faq_key.split()
            score = sum(1 for keyword in keywords if keyword in query_lower) / len(keywords)
            
            if score > highest_score and score > 0.5:
                highest_score = score
                best_match = faq_data
        
        if best_match:
            return {
                "answer": best_match["answer"],
                "confidence": best_match["confidence"] * highest_score
            }
        
        return None
    
    def _detect_intent(self, query):
        """Detect user intent from query"""
        query_lower = query.lower()
        
        for intent, pattern in self.intent_patterns.items():
            if re.search(pattern, query_lower, re.IGNORECASE):
                return intent
        
        return None
    
    def _handle_intent(self, intent, query, location_id, context):
        """Handle different intents"""
        try:
            if intent == "history":
                return self._handle_history_intent(query, location_id)
            elif intent == "travel":
                return self._handle_travel_intent(query, location_id)
            elif intent == "information":
                return self._handle_information_intent(query, location_id)
            elif intent == "recommendation":
                return self._handle_recommendation_intent(query, location_id)
            elif intent == "timing":
                return self._handle_timing_intent(query, location_id)
            elif intent == "cost":
                return self._handle_cost_intent(query, location_id)
            elif intent == "location":
                return self._handle_location_intent(query, location_id)
            else:
                return self._generate_generic_response(query)
        except Exception as e:
            logger.error(f"Error handling intent {intent}: {e}")
            return self._generate_generic_response(query)
    
    def _handle_history_intent(self, query, location_id):
        """Handle history-related queries"""
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                response = f"📜 {location.name} has a fascinating history! "
                if location.history:
                    response += location.history
                if location.period:
                    response += f" It belongs to the {location.period} period"
                if location.dynasty:
                    response += f" and was built during the {location.dynasty} dynasty."
                
                return {"answer": response, "confidence": 0.9}
        
        # Generic history response
        return {
            "answer": "India has a rich cultural heritage spanning thousands of years, from ancient Indus Valley civilization to the Mughal Empire and colonial period. Which specific period or location interests you?",
            "confidence": 0.7
        }
    
    def _handle_travel_intent(self, query, location_id):
        """Handle travel-related queries"""
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                response = f"🚗 To visit {location.name}: "
                response += f"It's located in {location.state}, India. "
                response += "The best way to reach depends on your starting point. I can help you plan a detailed route if you share your location."
                
                return {"answer": response, "confidence": 0.8}
        
        return {
            "answer": "I can help you plan your heritage journey! India's heritage sites are well-connected by various means of transport. Which destination interests you?",
            "confidence": 0.7
        }
    
    def _handle_information_intent(self, query, location_id):
        """Handle information requests"""
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                response = f"ℹ️ About {location.name}: "
                response += location.description
                if hasattr(location, 'cultural_facts') and location.cultural_facts:
                    response += f" Cultural significance: {' '.join(location.cultural_facts[:2])}"
                
                return {"answer": response, "confidence": 0.9}
        
        return {
            "answer": "I'd be happy to share information about India's heritage sites! Which specific location or aspect interests you?",
            "confidence": 0.7
        }
    
    def _handle_recommendation_intent(self, query, location_id):
        """Handle recommendation requests"""
        locations = self.kg_service.get_all_locations()
        if locations:
            # Get top 3 popular locations
            top_locations = locations[:3]
            response = "🌟 Here are some must-visit heritage sites:\n\n"
            for loc in top_locations:
                response += f"• **{loc.name}** - {loc.description[:100]}...\n"
            
            return {"answer": response, "confidence": 0.8}
        
        return {
            "answer": "I recommend exploring the Golden Triangle (Delhi-Agra-Jaipur), the Buddhist Circuit, or South India's temple architecture. What type of experience interests you?",
            "confidence": 0.7
        }
    
    def _handle_timing_intent(self, query, location_id):
        """Handle timing-related queries"""
        generic_timing = "Most heritage sites are open from sunrise to sunset (6 AM - 6 PM). Some sites like the Taj Mahal have special timings and weekly closures."
        
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                response = f"⏰ {location.name} timing: {generic_timing}"
                return {"answer": response, "confidence": 0.7}
        
        return {"answer": f"⏰ {generic_timing}", "confidence": 0.7}
    
    def _handle_cost_intent(self, query, location_id):
        """Handle cost-related queries"""
        generic_cost = "Entry fees typically range from ₹25-40 for Indians and $10-15 for foreign tourists. UNESCO World Heritage sites may have higher fees."
        
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                response = f"💰 {location.name} fees: {generic_cost}"
                return {"answer": response, "confidence": 0.7}
        
        return {"answer": f"💰 {generic_cost}", "confidence": 0.7}
    
    def _handle_location_intent(self, query, location_id):
        """Handle location-related queries"""
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                coords = location.coordinates
                response = f"📍 {location.name} is located in {location.state}, India"
                if coords and isinstance(coords, dict):
                    response += f" at coordinates ({coords.get('lat', 'N/A')}, {coords.get('lng', 'N/A')})"
                
                return {"answer": response, "confidence": 0.9}
        
        return {
            "answer": "India's heritage sites are spread across the country. Which specific location are you looking for?",
            "confidence": 0.6
        }
    
    def _get_location_specific_info(self, query, location_id):
        """Get location-specific information"""
        try:
            location = self.kg_service.get_location_by_id(location_id)
            if not location:
                return {"answer": "Location information not available.", "confidence": 0.3}
            
            # Build comprehensive response about the location
            response_parts = []
            
            # Basic info
            response_parts.append(f"🏛️ **{location.name}**")
            response_parts.append(location.description)
            
            # Historical context
            if location.period:
                response_parts.append(f"📅 Period: {location.period}")
            
            if location.dynasty:
                response_parts.append(f"👑 Dynasty: {location.dynasty}")
            
            # Cultural facts
            if hasattr(location, 'cultural_facts') and location.cultural_facts:
                response_parts.append("🎭 Cultural Facts:")
                for fact in location.cultural_facts[:2]:
                    response_parts.append(f"• {fact}")
            
            response = "\n\n".join(response_parts)
            
            return {"answer": response, "confidence": 0.8}
            
        except Exception as e:
            logger.error(f"Error getting location info: {e}")
            return {"answer": "Unable to retrieve location information.", "confidence": 0.3}
    
    def _search_knowledge_graph(self, query):
        """Search knowledge graph for relevant information"""
        try:
            # Extract potential location names from query
            locations = self.kg_service.get_all_locations()
            
            query_lower = query.lower()
            matching_locations = []
            
            for location in locations:
                # Better matching logic - check if query words appear in location name or description
                location_text = f"{location.name.lower()} {location.description.lower()}"
                query_words = query_lower.split()
                
                # Score based matching - higher score for exact name matches
                score = 0
                for word in query_words:
                    if len(word) > 2:  # Skip short words
                        if word in location.name.lower():
                            score += 10  # Higher weight for name matches
                        elif word in location.description.lower():
                            score += 1
                        elif hasattr(location, 'tags') and any(word in tag.lower() for tag in location.tags):
                            score += 5  # Medium weight for tag matches
                
                if score > 0:
                    matching_locations.append((location, score))
            
            if matching_locations:
                # Sort by score and return the best matching location
                matching_locations.sort(key=lambda x: x[1], reverse=True)
                best_match, best_score = matching_locations[0]
                
                response = f"🔍 Found information about {best_match.name}: {best_match.description}"
                
                # Add dynasty and period information if available
                if hasattr(best_match, 'dynasty') and best_match.dynasty:
                    response += f" Built during the {best_match.dynasty} period"
                    if hasattr(best_match, 'period') and best_match.period:
                        response += f" ({best_match.period})"
                    response += "."
                
                confidence = min(0.9, 0.4 + (best_score * 0.05))  # Scale confidence based on score
                return {"answer": response, "confidence": confidence}
            
            return {"answer": "No specific matches found in knowledge base.", "confidence": 0.4}
            
        except Exception as e:
            logger.error(f"Error searching knowledge graph: {e}")
            return {"answer": "Search functionality temporarily unavailable.", "confidence": 0.3}
    
    def _generate_dynamic_suggestions(self, query, response, location_id):
        """Generate context-aware follow-up suggestions"""
        suggestions = []
        
        query_lower = query.lower()
        
        # Try to extract location from the response if not provided as location_id
        found_location = None
        if "Found information about" in response:
            # Extract location name from response
            import re
            match = re.search(r'Found information about ([^:]+):', response)
            if match:
                location_name = match.group(1).strip()
                # Find this location in our knowledge base
                all_locations = self.kg_service.get_all_locations()
                for loc in all_locations:
                    if loc.name.lower() == location_name.lower():
                        found_location = loc
                        break
        
        # Generate location-specific suggestions
        if found_location:
            suggestions.extend([
                f"Best time to visit {found_location.name}",
                f"How to reach {found_location.name}",
                f"History of {found_location.name}",
                f"Architecture of {found_location.name}"
            ])
            
            # Add dynasty-specific suggestions
            if hasattr(found_location, 'dynasty') and found_location.dynasty:
                suggestions.append(f"Show me other {found_location.dynasty} sites")
                
            # Add category-specific suggestions  
            if hasattr(found_location, 'category') and found_location.category:
                suggestions.append(f"Show me other {found_location.category} sites")
        
        # Query-based suggestions
        elif any(word in query_lower for word in ['buddhist', 'buddha']):
            suggestions.extend([
                "Tell me about Bodh Gaya",
                "Show me Ajanta Caves",
                "Buddhist circuit route",
                "History of Buddhism in India"
            ])
        
        elif any(word in query_lower for word in ['golden triangle']):
            suggestions.extend([
                "Tell me about Delhi monuments",
                "History of Agra",
                "Jaipur palaces and forts", 
                "Plan Golden Triangle itinerary"
            ])
            
        elif any(word in query_lower for word in ['south india', 'southern']):
            suggestions.extend([
                "Tell me about Hampi",
                "Madurai temple architecture",
                "Kerala heritage sites",
                "Dravidian architecture"
            ])
        
        # Default suggestions if none generated
        if not suggestions:
            suggestions = [
                "Tell me about the Taj Mahal",
                "Show me Buddhist heritage sites", 
                "What is the Golden Triangle route?",
                "Recommend sites in South India"
            ]
        
        return suggestions[:4]  # Return max 4 suggestions
    
    def _generate_contextual_fallback(self, query, context):
        """Generate contextual fallback response"""
        fallback_responses = [
            "I'd love to help you explore India's rich heritage! Could you be more specific about what you'd like to know?",
            "India has thousands of heritage sites with fascinating stories. What particular aspect interests you?",
            "I can help you with information about historical sites, travel planning, cultural facts, and more. What would you like to explore?",
            "That's an interesting question! Let me help you discover India's cultural treasures. Which region or time period interests you most?"
        ]
        
        return {
            "answer": random.choice(fallback_responses),
            "confidence": 0.5
        }
    
    def _generate_generic_response(self, query):
        """Generate a generic helpful response"""
        return {
            "answer": "I'm here to help you explore India's incredible cultural heritage! Feel free to ask about specific sites, historical periods, travel routes, or cultural facts.",
            "confidence": 0.6
        }
    
    def _get_context(self, session_id, location_id=None):
        """Get relevant context for responding to the query"""
        context = ""
        
        # Add location-specific context if available
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                context += f"Current location: {location.name}. "
                context += f"Description: {location.description}. "
                if location.period:
                    context += f"Historical period: {location.period}. "
                if location.dynasty:
                    context += f"Dynasty: {location.dynasty}. "
                if location.history:
                    context += f"History: {location.history[:200]}... "
        
        # Add conversation history context
        if session_id in self.conversation_history:
            recent_messages = self.conversation_history[session_id][-4:]  # Last 4 messages
            for msg in recent_messages:
                context += f"{msg['role']}: {msg['text'][:100]}... "
        
        return context
    
    def get_recommendations(self, preferences):
        """Generate personalized recommendations based on user preferences"""
        try:
            # Use the route service to generate personalized routes
            route = self.route_service.create_personalized_route_with_preferences(preferences)
            
            recommendations = {
                "recommended_locations": [],
                "suggested_routes": [route.to_dict()] if route else [],
                "cultural_insights": []
            }
            
            # Add location recommendations
            locations = self.kg_service.get_all_locations()
            
            # Simple filtering based on interests
            interests = preferences.get('interests', [])
            if interests:
                filtered_locations = []
                for location in locations[:10]:  # Limit to first 10
                    if any(interest.lower() in location.category.lower() 
                          for interest in interests if hasattr(location, 'category')):
                        filtered_locations.append(location.to_dict())
                
                recommendations["recommended_locations"] = filtered_locations
            else:
                recommendations["recommended_locations"] = [loc.to_dict() for loc in locations[:5]]
            
            # Add cultural insights
            recommendations["cultural_insights"] = [
                "Consider visiting during festival seasons for authentic cultural experiences",
                "Many heritage sites offer guided tours that provide deeper historical context",
                "Local cuisine near heritage sites often reflects historical influences"
            ]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {
                "recommended_locations": [],
                "suggested_routes": [],
                "cultural_insights": ["I apologize, but I'm having trouble generating personalized recommendations right now."],
                "error": str(e)
            }