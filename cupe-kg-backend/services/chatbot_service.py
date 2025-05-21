# services/chatbot_service.py

import random
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
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
            # For a production system, you would use more sophisticated models
            # This is a simplified implementation
            self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
            self.model = AutoModelForQuestionAnswering.from_pretrained("distilbert-base-uncased-distilled-squad")
            
            # Initialize TF-IDF vectorizer for similarity matching
            self.vectorizer = TfidfVectorizer()
            
            # Prepare FAQ corpus
            self.faqs = self._prepare_faqs()
            self.faq_vectors = self.vectorizer.fit_transform([q for q, _ in self.faqs])
            
        except Exception as e:
            print(f"Error loading NLP models: {e}")
            # Fallback to rule-based approach if models can't be loaded
            self.tokenizer = None
            self.model = None
    
    def _prepare_faqs(self):
        """Prepare a corpus of FAQs for matching"""
        return [
            ("What is the best time to visit Taj Mahal?", 
             "The best time to visit the Taj Mahal is from October to March when the weather is pleasant and less humid. For the most magical experience, visit at sunrise when the marble takes on a soft pink glow, or at sunset when it appears golden. The monument is closed on Fridays for prayers at the mosque within the complex."),
            
            ("What is the best time to visit Hampi?", 
             "The best time to visit Hampi is from October to March when the weather is pleasant with temperatures between 15°C to 30°C. Avoid the summer months (April to June) when temperatures can soar above 40°C. The annual Hampi Festival in November is a great time to experience the local culture."),
            
            ("How do I reach Hampi?",
             "To reach Hampi, the nearest airport is in Ballari (Bellary) about 60 km away, or Hubli Airport (143 km). The closest major railway station is Hospet Junction (12 km), which has connections to Bangalore, Hyderabad, and Goa. From Hospet, you can take a local bus, auto-rickshaw, or taxi to Hampi."),
             
            ("What is the Buddhist Trail?",
             "The Buddhist Trail connects key sites of Buddhist heritage across northern India. Major stops include Bodh Gaya (where Buddha attained enlightenment), Sarnath (where he gave his first sermon), and Kushinagar (where he attained parinirvana). The route offers spiritual significance and architectural marvels spanning over 2,500 years of history."),
             
            ("Tell me about Delhi's monuments",
             "Delhi is home to numerous significant monuments, including three UNESCO World Heritage sites: the Qutub Minar, Red Fort, and Humayun's Tomb. Other notable monuments include India Gate, Jama Masjid, Lotus Temple, Akshardham Temple, and Jantar Mantar. These structures represent various architectural styles from different periods of India's history."),
             
            ("What dynasty built the Konark Sun Temple?",
             "The Konark Sun Temple was built by King Narasimhadeva I of the Eastern Ganga Dynasty in the 13th century (around 1250 CE). The Eastern Ganga Dynasty ruled the region of Kalinga (modern-day Odisha) from the 5th to the 15th century CE."),
            
            ("What is the significance of Khajuraho temples?",
             "The Khajuraho temples are renowned for their exquisite stone carvings depicting various aspects of human life, including spirituality, eroticism, and daily activities. Built by the Chandela dynasty between 950-1050 CE, they represent the culmination of North Indian temple architecture. While famous for their sensual sculptures, these only comprise about 10% of the total artwork, with the rest depicting religious themes, royal processions, and everyday life."),
            
            ("What is unique about Ajanta and Ellora Caves?",
             "Ajanta and Ellora Caves showcase unique ancient Indian rock-cut architecture. Ajanta's 30 Buddhist caves (2nd century BCE-6th century CE) feature stunning paintings depicting Buddha's life. Ellora's 34 caves (6th-11th century CE) represent religious harmony with Buddhist, Hindu, and Jain monuments. Most impressive is Ellora's Cave 16, the Kailasa Temple, carved from a single rock making it the world's largest monolithic structure."),
            
            ("Tell me about the Golden Temple.",
             "The Golden Temple (Harmandir Sahib) in Amritsar is Sikhism's holiest shrine. Built in 1604 by Guru Arjan Dev, it features a distinctive gold-plated upper portion (added by Maharaja Ranjit Singh in the early 19th century) surrounded by a sacred pool called Amrit Sarovar. It's known for its inclusive values, with four entrances symbolizing openness to all faiths and castes, and its community kitchen (langar) serving free meals to up to 100,000 visitors daily regardless of background."),
            
            ("What is the history of Qutub Minar?",
             "Qutub Minar was built beginning in 1192 by Qutub-ud-din Aibak, founder of the Delhi Sultanate, and later completed by his successor Iltutmish. Standing 73 meters tall, it's the world's tallest brick minaret. The tower marked the beginning of Islamic rule in India and was part of the Quwwat-ul-Islam mosque complex. Its construction used materials from 27 demolished Hindu and Jain temples, and it represents the earliest fusion of Islamic and Indian architectural styles."),
            
            ("What is the best way to plan a historical route in India?",
             "The best way to plan a historical route in India is to focus on a specific theme or region rather than trying to cover too much distance. Popular thematic routes include the Golden Triangle (Delhi-Agra-Jaipur), the Buddhist Circuit (Bodh Gaya-Sarnath-Kushinagar), Temple Routes of South India, or the Mughal Heritage Tour of North India. Consider the best season for travel, allow 2-3 days per major site, and plan for local transportation between locations. Our route planner can create a personalized itinerary based on your specific interests and time constraints.")
        ]
    
    def process_query(self, session_id, query, location_id=None):
        """
        Process a user query with context awareness
        
        Parameters:
        - session_id: Unique identifier for the conversation
        - query: The user's question
        - location_id: ID of the location currently being viewed (optional)
        
        Returns:
        - Response object with answer and suggested follow-ups
        """
        # Initialize conversation history if new session
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
            
        # Add the current query to history
        self.conversation_history[session_id].append({"role": "user", "text": query})
        
        # Get context for the question
        context = self._get_context(session_id, location_id)
        
        # Try to match with FAQ first
        faq_response = self._match_faq(query)
        if faq_response and faq_response['confidence'] > 0.8:
            # Use the FAQ response if high confidence match
            answer = faq_response['answer']
            confidence = faq_response['confidence']
        else:
            # Otherwise use intent detection and QA model
            intent = self._detect_intent(query)
            if intent:
                # Process specific intents
                response = self._handle_intent(intent, query, location_id, context)
                answer = response['answer']
                confidence = response['confidence']
            else:
                # General question answering using context
                response = self._answer_question(query, context)
                answer = response['answer']
                confidence = response['confidence']
        
        # Generate follow-up suggestions based on the conversation
        suggestions = self._generate_suggestions(query, answer, location_id)
        
        # Add response to conversation history
        self.conversation_history[session_id].append({"role": "assistant", "text": answer})
        
        # Return formatted response
        return {
            'answer': answer,
            'confidence': confidence,
            'followUpQuestions': suggestions
        }
        
    def _get_context(self, session_id, location_id=None):
        """Get relevant context for responding to the query"""
        context = ""
        
        # Add location-specific context if available
        if location_id:
            location = self.kg_service.get_location_by_id(location_id)
            if location:
                context += f"Name: {location.name}. Description: {location.description}. "
                context += f"History: {location.history}. Period: {location.period}. "
                context += f"Dynasty: {location.dynasty}. "
                
                # Add cultural facts
                if hasattr(location, 'cultural_facts') and location.cultural_facts:
                    context += "Cultural facts: " + " ".join(location.cultural_facts) + ". "
                
                # Add legends
                if hasattr(location, 'legends') and location.legends:
                    for legend in location.legends:
                        context += f"Legend - {legend['title']}: {legend['description']}. "
        
        # Add conversation history context (last 3 exchanges)
        if session_id in self.conversation_history:
            history = self.conversation_history[session_id][-6:]  # Last 3 exchanges (6 messages)
            for msg in history:
                context += f"{msg['role'].title()}: {msg['text']} "
        
        # Add general information about Indian heritage if context is limited
        if len(context) < 200:
            context += """
            India has a rich cultural heritage with numerous historical sites. 
            Some notable sites include the Taj Mahal in Agra, Hampi ruins in Karnataka,
            Konark Sun Temple in Odisha, the Red Fort in Delhi, Ajanta and Ellora Caves in Maharashtra,
            and Khajuraho Temples in Madhya Pradesh. 
            Indian history spans from ancient civilizations like the Indus Valley (3300-1300 BCE)
            through various empires including the Mauryan, Gupta, Delhi Sultanate, and Mughal periods. The country gained independence from British rule in 1947.
            The diverse geography, culture, religions, and architecture make India a rich tapestry
            of historical experiences for visitors to explore.
            """
            
        return context
        
    def _match_faq(self, query):
        """Match the query against FAQs using vector similarity"""
        if not self.faqs:
            return None
            
        # Transform the query using the same vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calculate similarity with all FAQs
        similarities = cosine_similarity(query_vector, self.faq_vectors).flatten()
        
        # Get the best match
        best_match_idx = similarities.argmax()
        confidence = similarities[best_match_idx]
        
        # Return if confidence is above threshold
        if confidence > 0.5:  # Adjust threshold as needed
            return {
                'answer': self.faqs[best_match_idx][1],
                'confidence': float(confidence)
            }
        
        return None
        
    def _detect_intent(self, query):
        """Detect the intent of the query using regex patterns"""
        # Simple intent detection using regular expressions
        # In a production system, use a more sophisticated approach
        intents = {
            'greeting': r'\b(hello|hi|hey|greetings|namaste)\b',
            'farewell': r'\b(bye|goodbye|see you|farewell)\b',
            'thanks': r'\b(thanks|thank you|appreciate)\b',
            'location_info': r'(tell me about|info on|information about|what is|where is) (.+)',
            'best_time': r'\b(best time|when to visit|visiting season|weather) (.+)\b',
            'how_to_reach': r'\b(how to reach|how to get to|directions to|travel to) (.+)\b',
            'historical_period': r'\b(history of|historical period|dynasty|king|ruler) (.+)\b',
            'route_suggestion': r'\b(route|itinerary|plan|travel plan|visit) (from|between|to) (.+)\b',
            'cultural_facts': r'\b(cultural facts|culture|tradition|art|cuisine) (.+)\b',
            'legend': r'\b(legend|story|myth|folklore|tale) (.+)\b',
            'compare': r'\b(compare|difference between|similarity between) (.+) and (.+)\b'
        }
        
        for intent, pattern in intents.items():
            if re.search(pattern, query.lower()):
                return intent
                
        return None
        
    def _handle_intent(self, intent, query, location_id, context):
        """Handle specific intents with appropriate responses"""
        if intent == 'greeting':
            return {
                'answer': "Namaste! I'm your CuPe-KG guide to India's cultural heritage. Ask me anything about historical sites, dynasties, art, or plan your travel route across India's rich tapestry of monuments and traditions.",
                'confidence': 0.95
            }
            
        elif intent == 'farewell':
            return {
                'answer': "Thank you for exploring India's rich heritage with CuPe-KG. May your journey through our cultural landscapes be fulfilling. Phir milenge (See you again)!",
                'confidence': 0.95
            }
            
        elif intent == 'thanks':
            return {
                'answer': "You're welcome! It's my pleasure to help you explore India's cultural heritage. Is there anything else you'd like to know about our historical treasures?",
                'confidence': 0.95
            }
            
        elif intent == 'location_info':
            # Extract location name from query
            match = re.search(r'(tell me about|info on|information about|what is|where is) (.+)', query.lower())
            if match:
                location_name = match.group(2).strip()
                return self._get_location_info(location_name, location_id)
                
        elif intent == 'best_time':
            # Extract location name from query
            match = re.search(r'\b(best time|when to visit|visiting season|weather) (.+)', query.lower())
            if match:
                location_name = match.group(2).strip()
                return self._get_best_time_to_visit(location_name)
                
        elif intent == 'how_to_reach':
            # Extract location name from query
            match = re.search(r'\b(how to reach|how to get to|directions to|travel to) (.+)', query.lower())
            if match:
                location_name = match.group(2).strip()
                return self._get_travel_directions(location_name)
                
        elif intent == 'historical_period':
            # Extract period from query
            match = re.search(r'\b(history of|historical period|dynasty|king|ruler) (.+)', query.lower())
            if match:
                subject = match.group(2).strip()
                return self._get_historical_info(subject)
        
        elif intent == 'cultural_facts':
            # Extract the subject
            match = re.search(r'\b(cultural facts|culture|tradition|art|cuisine) (.+)', query.lower())
            if match:
                subject = match.group(2).strip()
                return self._get_cultural_info(subject)
                
        elif intent == 'legend':
            # Extract the subject
            match = re.search(r'\b(legend|story|myth|folklore|tale) (.+)', query.lower())
            if match:
                subject = match.group(2).strip()
                return self._get_legend_info(subject)
                
        elif intent == 'route_suggestion':
            return self._suggest_route(query)
                
        # Fallback to general QA if no specific handler
        return self._answer_question(query, context)
        
    def _answer_question(self, question, context):
        """Answer a question based on provided context using NLP model"""
        if self.model and self.tokenizer:
            try:
                # Use the QA model to answer the question
                inputs = self.tokenizer(question, context, return_tensors="pt")
                outputs = self.model(**inputs)
                
                answer_start = torch.argmax(outputs.start_logits)
                answer_end = torch.argmax(outputs.end_logits) + 1
                
                answer = self.tokenizer.decode(inputs.input_ids[0][answer_start:answer_end])
                
                # Check if answer is meaningful
                if len(answer.strip()) < 3 or answer.strip() in [".", ",", "?", "!", ":"]:
                    return self._generate_fallback_response(question)
                    
                return {
                    'answer': answer,
                    'confidence': float(torch.max(outputs.start_logits).item() * torch.max(outputs.end_logits).item())
                }
                
            except Exception as e:
                print(f"Error in question answering: {e}")
                return self._generate_fallback_response(question)
        else:
            # Fallback to rule-based response if model not available
            return self._generate_fallback_response(question)
            
    def _generate_fallback_response(self, question):
        """Generate a fallback response when no good answer is found"""
        fallbacks = [
            "I'm not quite sure about that aspect of Indian heritage. Could you please rephrase or ask about a specific historical site, dynasty, or cultural tradition?",
            "That's an interesting question about Indian culture. Could you be more specific or ask about a particular historical site like the Taj Mahal, Ajanta Caves, or Khajuraho Temples?",
            "I don't have enough information to answer that question accurately. I'd be happy to tell you about major historical sites like the Taj Mahal, Hampi, Sanchi Stupa, or about dynastic periods like the Mughals or Mauryas.",
            "I'm still learning about India's vast cultural heritage. Could you ask me about specific monuments, historical periods, or perhaps you'd like recommendations for a cultural route?"
        ]
        
        return {
            'answer': random.choice(fallbacks),
            'confidence': 0.3
        }
        
    def _get_location_info(self, location_name, current_location_id=None):
        """Get information about a location"""
        # Try to find the location in our database
        all_locations = self.kg_service.get_all_locations()
        matching_location = None
        
        for location in all_locations:
            if location_name.lower() in location.name.lower() or location.name.lower() in location_name.lower():
                matching_location = location
                break
                
        # If a matching location was found
        if matching_location:
            # Create a rich, detailed response about the location
            response = (
                f"{matching_location.name} is {matching_location.description}. "
                f"It dates back to the {matching_location.period} during the {matching_location.dynasty}. "
                f"{matching_location.history} "
            )
            
            # Add a cultural fact if available
            if hasattr(matching_location, 'cultural_facts') and matching_location.cultural_facts:
                response += f"An interesting fact is that {random.choice(matching_location.cultural_facts)} "
                
            return {
                'answer': response,
                'confidence': 0.9
            }
        
        # If no matching location found
        return {
            'answer': f"I don't have specific information about {location_name} in my database. Would you like to know about other popular heritage sites in India like the Taj Mahal, Ajanta Caves, Khajuraho Temples, or Hampi?",
            'confidence': 0.3
        }
    
    def _get_best_time_to_visit(self, location_name):
        """Provide information about the best time to visit a location"""
        # This would ideally come from a database, but we'll use hardcoded responses for now
        best_times = {
            'taj mahal': "The best time to visit the Taj Mahal is from October to March when the weather is pleasant and less humid. For the most magical experience, visit at sunrise when the marble takes on a soft pink glow, or at sunset when it appears golden. The monument is closed on Fridays for prayers at the mosque within the complex.",
            'hampi': "The best time to visit Hampi is from October to March when the weather is pleasant with temperatures between 15°C to 30°C. Avoid the summer months (April to June) when temperatures can soar above 40°C. The annual Hampi Festival in November is a great time to experience the local culture.",
            'delhi': "The best time to visit Delhi is from October to March when the weather is cool and pleasant. Winter (December-January) can be chilly with temperatures dropping to 5-7°C. Avoid the summer months (April to June) when temperatures can reach 45°C, and the monsoon season (July to September) when humidity is high.",
            'konark': "The best time to visit Konark is from October to March when the weather is pleasant. The annual Konark Dance Festival in December is a special time to visit. Summers (April to June) can be extremely hot and humid with temperatures reaching 40°C, so it's best to avoid this season.",
            'khajuraho': "The ideal time to visit Khajuraho is from October to March when the weather is comfortable for exploring the temples. The Khajuraho Dance Festival in February/March is a special attraction. Summer (April to June) brings intense heat making extended exploration difficult.",
            'ajanta': "The best time to visit Ajanta Caves is from November to March when temperatures are moderate and comfortable for exploring. The caves are particularly beautiful during the monsoon (July-September) when the surrounding landscape is lush, but paths can be slippery.",
            'ellora': "Visit Ellora Caves between November and March for pleasant weather conducive to exploring. The site is open from sunrise to sunset, but early mornings offer better lighting for photography. Avoid summer (April-June) when temperatures can exceed 40°C making exploration of the unventilated caves uncomfortable.",
            'golden temple': "The Golden Temple can be visited year-round as it's open 24 hours. However, the most pleasant time is from October to March when the weather is mild. Visit during major Sikh festivals like Baisakhi (April), Guru Nanak Jayanti (November), or Diwali for an especially spiritual atmosphere, though expect crowds during these celebrations.",
            'sanchi stupa': "The best time to visit Sanchi Stupa is from October to March when the weather is cool and pleasant. The site is particularly beautiful during sunrise and sunset when the golden light enhances the ancient sandstone structures. Avoid summer months (April-June) when temperatures can exceed 40°C."
        }
        
        # Normalize the location name for matching
        normalized_location = location_name.lower()
        
        # Look for exact or partial matches
        for key, value in best_times.items():
            if key == normalized_location or key in normalized_location or normalized_location in key:
                return {
                    'answer': value,
                    'confidence': 0.9
                }
        
        # Default response if no match found
        return {
            'answer': f"For most historical sites in India, the best time to visit is during the winter months (October to March) when the weather is pleasant across most of the country. Most places experience hot summers (April to June) and monsoon rains (July to September). I don't have specific seasonal information for {location_name}, but following this general guideline would work well for most heritage sites.",
            'confidence': 0.6
        }
    
    def _get_travel_directions(self, location_name):
        """Provide information about how to reach a location"""
        # Again, this would ideally come from a database
        travel_info = {
            'taj mahal': "To reach the Taj Mahal in Agra, you can fly to Agra Airport with domestic connections, or more commonly to Delhi (230 km away) and then travel by road or train. The Gatimaan Express train from Delhi reaches Agra in about 100 minutes. Other options include numerous trains from major cities, luxury tourist buses, or private taxis. Within Agra, auto-rickshaws, cycle-rickshaws, and taxis can take you to the Taj Mahal's eastern gate entrance.",
            'hampi': "To reach Hampi, the nearest airport is in Ballari (Bellary) about 60 km away, or Hubli Airport (143 km). The closest major railway station is Hospet Junction (12 km), which has connections to Bangalore, Hyderabad, and Goa. From Hospet, you can take a local bus, auto-rickshaw, or taxi to Hampi. The UNESCO site is best explored on foot, by bicycle, or motorbike.",
            'delhi': "Delhi is easily accessible as it has an international airport (Indira Gandhi International Airport) with connections worldwide. The city is also well-connected by railways to all major Indian cities. Within Delhi, you can use the extensive Metro system, buses, auto-rickshaws, taxis, or ride-sharing services like Uber and Ola.",
            'konark': "To reach Konark, the nearest airport is Bhubaneswar (65 km) which has good connections to major Indian cities. The nearest railway station is at Puri (35 km). From either Bhubaneswar or Puri, you can hire a taxi or take a bus to Konark. The Odisha Tourism Development Corporation also operates special tours to Konark from both cities.",
            'khajuraho': "To reach Khajuraho, you can fly to Khajuraho Airport which has connections to Delhi and Varanasi. Alternatively, the nearest major railway station is Khajuraho Railway Station, connected to cities like Delhi, Varanasi, and Jhansi. From Jhansi, which is better connected by train, you can take a taxi (175 km). Regular buses also operate from Jhansi, Satna, and other nearby cities.",
            'ajanta': "To reach Ajanta Caves, fly to Aurangabad Airport (104 km) which has connections to major Indian cities. From Aurangabad, hire a taxi or join a tour to Ajanta. Alternatively, you can take a train to Jalgaon Junction (59 km from Ajanta) and then take a taxi. The Maharashtra Tourism Development Corporation operates buses from Aurangabad to Ajanta. The caves are closed on Mondays.",
            'ellora': "Ellora Caves are best reached via Aurangabad, which has an airport with connections to major Indian cities. From Aurangabad, Ellora is just 30 km away - take a taxi, join a tour, or use the daily MSRTC buses. If arriving by train, Aurangabad Railway Station has connections to Mumbai, Delhi, and other major cities. The caves are closed on Tuesdays.",
            'golden temple': "To reach the Golden Temple in Amritsar, fly to Sri Guru Ram Dass Jee International Airport with connections to major Indian cities and some international destinations. Alternatively, Amritsar is well-connected by train to Delhi, Mumbai, Kolkata, and other major cities. From the airport or railway station, taxis, auto-rickshaws, and cycle-rickshaws are available to reach the temple. The complex is pedestrian-only, and visitors must remove shoes and cover their heads before entering."
        }
        
        # Normalize the location name for matching
        normalized_location = location_name.lower()
        
        # Look for exact or partial matches
        for key, value in travel_info.items():
            if key == normalized_location or key in normalized_location or normalized_location in key:
                return {
                    'answer': value,
                    'confidence': 0.9
                }
        
        # Default response
        return {
            'answer': f"To reach most heritage sites in India, you would typically fly to the nearest major city and then use local transportation like trains, buses, or taxis to reach your destination. For specific directions to {location_name}, I recommend checking with Indian Railways (www.irctc.co.in) for train connections or with a travel agent who specializes in Indian tourism.",
            'confidence': 0.5
        }
    
    def _get_historical_info(self, subject):
        """Provide historical information about a subject"""
        # Sample historical information
        historical_info = {
            'vijayanagara empire': "The Vijayanagara Empire (1336-1646 CE) was one of the greatest Hindu empires in South India, known for its contributions to art, architecture, and culture. With its capital at Hampi, the empire reached its peak under King Krishnadevaraya (1509-1529). The ruins of Hampi showcase the empire's architectural magnificence with temples, royal complexes, and irrigation systems. The empire served as a bulwark against Islamic invasions from the north, preserving Hindu culture and traditions in southern India.",
            'mughal': "The Mughal Empire (1526-1857) was one of the most powerful Islamic dynasties in India, founded by Babur who defeated the Delhi Sultanate. It reached its zenith under Emperor Akbar through his policy of religious tolerance and administrative reforms. Shah Jahan's reign saw the construction of architectural marvels like the Taj Mahal, while Aurangzeb's religious orthodoxy and extensive conquests stretched imperial resources. Mughal architecture blends Persian, Turkish, and Indian styles, characterized by grand domes, minarets, and intricate decorations. The empire declined after Aurangzeb due to weak successors, regional revolts, and finally fell to British colonization.",
            'eastern ganga': "The Eastern Ganga Dynasty (8th-15th century CE) ruled the region of Kalinga (modern Odisha). They were great patrons of art and architecture, with their most famous contribution being the Konark Sun Temple built by King Narasimhadeva I. The dynasty's architectural style is known as Kalinga architecture, characterized by pyramidal roofs, elaborate carvings, and erotic sculptures. The dynasty supported both Hinduism and Jainism and maintained maritime trade links with Southeast Asia, spreading Indian cultural influence abroad.",
            'delhi sultanate': "The Delhi Sultanate (1206-1526) was a series of five Muslim dynasties that ruled northern India: the Mamluk, Khalji, Tughlaq, Sayyid, and Lodi dynasties. They introduced Indo-Islamic architecture, blending Indian and Persian styles. Notable monuments include the Qutub Minar, Alai Darwaza, and Quwwat-ul-Islam mosque. The Sultanate faced constant challenges from Mongol invasions and internal rebellions. Despite political instability, this period saw cultural synthesis between Islamic and Indian traditions in art, architecture, language, and governance.",
            'chandela': "The Chandela Dynasty (9th-13th century CE) ruled parts of Central India from their capital at Khajuraho. They are best known for building the magnificent temples of Khajuraho, renowned for their nagara-style architectural symbolism and intricate sculptures. The dynasty reached its peak under King Vidyadhara who successfully repelled attacks from Mahmud of Ghazni. The Chandelas were patrons of art, architecture, and literature during Medieval India, creating what is now considered one of India's greatest architectural treasures.",
            'satavahana': "The Satavahana Dynasty (230 BCE-220 CE) ruled the Deccan region of central India. They were important patrons of Buddhism and Hinduism, contributing significantly to cave architecture, as seen in the early Ajanta Caves. The Satavahanas promoted trade with the Roman Empire and facilitated cultural exchange. Under rulers like Gautamiputra Satakarni, they expanded their territory and revived Brahmanism after the decline of Mauryan influence. Their coins and inscriptions provide valuable historical evidence about this period.",
            'maurya': "The Maurya Empire (322-185 BCE) was one of ancient India's largest and most powerful empires, established by Chandragupta Maurya after overthrowing the Nanda Dynasty. It reached its greatest extent under Emperor Ashoka, who, after the bloody Kalinga War, embraced Buddhism and spread its teachings throughout Asia. The empire was known for its centralized administration, extensive trade networks, and remarkable architecture including monolithic pillars with edicts. Ashoka's pillars and rock edicts, like the one at Sanchi, represent some of the earliest stone structures and inscriptions in India.",
            'gupta': "The Gupta Empire (320-550 CE) is considered India's 'Golden Age,' marked by unprecedented achievements in science, mathematics, astronomy, literature, and art. Under rulers like Chandragupta I, Samudragupta, and Chandragupta II, the empire expanded through conquest and diplomatic marriages. This period saw the development of the decimal system, the concept of zero, the calculation of pi, and advancements in metallurgy. The arts flourished with Sanskrit literature reaching its peak, and Hindu temple architecture evolving into more sophisticated forms. The Gupta period represents classical Indian civilization at its height."
        }
        
        # Look for matches
        normalized_subject = subject.lower()
        for key, value in historical_info.items():
            if key in normalized_subject or normalized_subject in key:
                return {
                    'answer': value,
                    'confidence': 0.9
                }
        
        # If no match is found, try to match with location names
        all_locations = self.kg_service.get_all_locations()
        for location in all_locations:
            if subject.lower() in location.name.lower() or location.name.lower() in subject.lower():
                return {
                    'answer': f"{location.name} dates back to the {location.period} during the {location.dynasty}. {location.history}",
                    'confidence': 0.7
                }
        
        # Default response
        return {
            'answer': f"I don't have detailed historical information about '{subject}' in my database. I can tell you about major Indian dynasties like the Mauryas, Guptas, Delhi Sultanate, Mughals, Marathas, or Vijayanagara Empire if you're interested.",
            'confidence': 0.3
        }
    
    def _get_cultural_info(self, subject):
        """Provide cultural information about a subject"""
        cultural_info = {
            'taj mahal': "The Taj Mahal represents the pinnacle of Mughal cultural aesthetics, blending Persian, Islamic, and Indian architectural elements. Its white marble changes color throughout the day, reflecting India's poetic tradition of seeing beauty in transience. The monument is adorned with intricate pietra dura (stone inlay work) featuring botanical motifs and calligraphy of Quranic verses. The surrounding charbagh garden follows the Persian four-part design symbolizing paradise. Today, the Taj Mahal is not just a mausoleum but a cultural icon representing India's artistic achievement and eternal love.",
            'khajuraho': "The Khajuraho temples reflect medieval Indian society's holistic approach to spirituality, where human desires and divine aspirations weren't separate domains. The sculptures depict daily life, mythological scenes, and sensual themes in exquisite detail. The erotic sculptures, comprising only about 10% of the artwork, represent tantric traditions that view human sexuality as a path to spiritual transcendence. The temples feature classical Indian dance postures that influenced modern performance arts. Annual dance festivals held here celebrate this cultural continuity, connecting ancient temple art with living traditions.",
            'hampi': "Hampi's cultural landscape integrates natural rocky outcrops with human-made temples and civic structures, reflecting a unique adaptation to the environment. The site preserves elements of Vijayanagara court life, including public bathing areas, elephant stables, and musical pillars at Vittala Temple that demonstrate advanced acoustic engineering. Local traditions maintain connections to the Ramayana epic through sites associated with Hanuman and the monkey kingdom. Contemporary cultural life continues in the active Virupaksha Temple where rituals have been performed continually since the 7th century. The annual Hampi Utsav festival revives the artistic patronage once practiced by Vijayanagara kings.",
            'ajanta ellora': "Ajanta and Ellora caves represent a remarkable cultural synthesis across religious traditions. Ajanta's Buddhist paintings employ techniques like perspective and foreshortening that wouldn't appear in European art until much later. The artistic traditions documented in these caves influenced painting styles across Asia. Ellora demonstrates India's religious plurality with Hindu, Buddhist, and Jain monuments created side by side. The Kailasa Temple at Ellora represents ancient India's engineering prowess—carved from top to bottom out of a single rock, removing over 200,000 tons of stone. Local folk performances and craft traditions in the region still reference motifs and stories depicted in these ancient cave paintings and sculptures.",
            'indian cuisine': "Indian cuisine varies dramatically by region, with distinct flavor profiles developed through historical trade routes and cultural exchanges. Northern cuisine shows Persian and Central Asian influences with creamy gravies and tandoor cooking. Southern traditions feature rice, coconut, and tamarind with complex layering of spices. Eastern coastal cuisines emphasize seafood with mustard and chili, while western regions blend sweet, spicy, and sour elements. The principles of Ayurveda influence traditional Indian cooking, balancing six tastes (sweet, sour, salty, bitter, pungent, and astringent) for health. Religious traditions have shaped vegetarian cooking techniques that achieve rich flavors without meat, especially in temple cuisines across India.",
            'indian classical dance': "India's classical dance forms are living traditions with ancient roots, codified in the Natya Shastra text from around 200 BCE. Each dance form has regional associations: Bharatanatyam from Tamil Nadu, Kathakali from Kerala, Kathak from North India, Odissi from Odisha, Kuchipudi from Andhra Pradesh, Manipuri from the northeast, and Sattriya from Assam. These dances integrate intricate footwork, hand gestures (mudras), facial expressions (abhinaya), and rhythmic patterns. Originally performed in temples as spiritual offerings, these arts survived periods of decline by adapting to court patronage and modern stage performances. Today, classical dance practitioners balance traditional authenticity with contemporary innovation, making these ancient forms relevant to modern audiences."
        }
        
        # Look for matches
        normalized_subject = subject.lower()
        for key, value in cultural_info.items():
            if key in normalized_subject or normalized_subject in key:
                return {
                    'answer': value,
                    'confidence': 0.9
                }
                
        # If no match, return a general response
        return {
            'answer': f"India's cultural traditions span thousands of years with regional variations in art, architecture, cuisine, music, dance, and spiritual practices. The subcontinent has been a cultural crossroads, absorbing and transforming influences from Persia, Central Asia, Southeast Asia, and Europe while maintaining distinct indigenous traditions. I don't have specific information about {subject}, but I'd be happy to tell you about specific aspects of Indian cultural heritage like classical dance, temple architecture, or regional cuisines.",
            'confidence': 0.4
        }
    
    def _get_legend_info(self, subject):
        """Provide information about legends and stories"""
        # Try to match with a specific location first
        all_locations = self.kg_service.get_all_locations()
        for location in all_locations:
            if location.name.lower() in subject.lower() or subject.lower() in location.name.lower():
                if hasattr(location, 'legends') and location.legends:
                    # Pick a legend to share
                    legend = random.choice(location.legends)
                    return {
                        'answer': f"One fascinating legend associated with {location.name} is '{legend['title']}'. {legend['description']}",
                        'confidence': 0.9
                    }
        
        # If no location match or no legends available, provide some common legends
        common_legends = {
            'taj mahal': "The most famous legend of the Taj Mahal tells that Emperor Shah Jahan planned to build an identical Black Taj Mahal across the river, as a mausoleum for himself. This mirror image would have been constructed in black marble, connected by a bridge to the white Taj. Construction supposedly began but was halted when Shah Jahan was imprisoned by his son Aurangzeb. Archaeological excavations have found some structures that might support this theory, but many historians dismiss it as folklore rather than fact.",
            'khajuraho': "The most popular legend about Khajuraho involves Hemavati, daughter of a Brahmin priest. According to the story, she was bathing in a pond on a full moon night when the Moon God was so enchanted by her beauty that he descended to Earth in human form. Their union resulted in a son, Chandravarman, who became the founder of the Chandela dynasty. To absolve his mother from the sin of unwed motherhood, Chandravarman built the Khajuraho temples with sculptures celebrating all aspects of human life, including sensuality, suggesting that human desires are a natural part of divine creation.",
            'ellora kailasa': "Legend says that the architect of the Kailasa Temple at Ellora was given an impossible task: to complete this massive temple carved from a single rock within the king's lifetime. After meditation, the architect had a divine vision and realized he could carve from top to bottom instead of the conventional bottom-up approach. Working with thousands of laborers day and night, he removed over 200,000 tons of rock. When the king came to see the progress, he was astonished to find the entire temple already complete, as if by divine intervention.",
            'sanchi stupa': "A local legend tells that the great Emperor Ashoka fell ill and his wife promised to build 84,000 stupas if he recovered. When he did recover, Ashoka commissioned stupas across his empire to house Buddha's relics. The Great Stupa at Sanchi was supposedly built over a weekend by divine architects, explaining its perfect proportions. While historically inaccurate (the construction actually took years), this tale underscores the sacred significance of the monument and Ashoka's dedication to spreading Buddhism."
        }
        
        # Look for matches in common legends
        normalized_subject = subject.lower()
        for key, value in common_legends.items():
            if key in normalized_subject or normalized_subject in key:
                return {
                    'answer': value,
                    'confidence': 0.8
                }
        
        # Default response
        return {
            'answer': "Indian heritage sites are rich with legends and folklore that add cultural depth to their historical significance. These stories often blend historical facts with mythological elements, connecting monuments to divine interventions, cosmic events, or legendary rulers. While I don't have a specific legend about " + subject + ", I can share stories associated with famous sites like the Taj Mahal, Khajuraho Temples, or Hampi if you're interested.",
            'confidence': 0.5
        }
    
    def _suggest_route(self, query):
        """Suggest a travel route based on user query"""
        # Get all predefined routes
        all_routes = self.route_service.get_all_routes()
        
        # Look for keywords in the query that match route themes
        route_keywords = {
            'buddhist': ['buddhist', 'buddha', 'buddhism', 'spiritual', 'bodh gaya', 'sarnath'],
            'mughal': ['mughal', 'islamic', 'architecture', 'monuments', 'taj', 'agra', 'delhi'],
            'temple': ['temple','hindu', 'spiritual', 'architecture', 'konark', 'khajuraho', 'hampi']
        }
        
        matching_routes = []
        for route in all_routes:
            # Check if route name or description matches query
            if route.id in route_keywords and any(keyword in query.lower() for keyword in route_keywords[route.id]):
                matching_routes.append(route)
        
        if matching_routes:
            route = matching_routes[0]  # Take the first matching route for simplicity
            locations_str = ', '.join([loc.name for loc in route.locations])
            
            return {
                'answer': f"I recommend the {route.name} route which includes {locations_str}. This route will take you through {route.description}. The journey covers approximately {self._calculate_route_distance(route.path)} kilometers and would typically take about {self._estimate_route_duration(route.path)} days to complete while allowing time to explore each site.",
                'confidence': 0.9
            }
        
        # Check for specific interests or regions mentioned
        interest_keywords = {
            'architecture': "Based on your interest in architecture, I recommend the 'Architectural Marvels' route that includes the Taj Mahal in Agra, Khajuraho Temples in Madhya Pradesh, and Meenakshi Temple in Madurai. This showcases diverse architectural styles from Islamic to Hindu temple architecture across different periods.",
            'history': "For history enthusiasts, I recommend the 'Empires of India' route covering Delhi (multiple dynasties), Agra (Mughal glory), and Hampi (Vijayanagara ruins). This route traces the evolution of Indian political powers from medieval to colonial periods.",
            'spiritual': "For a spiritual journey, I suggest the 'Spiritual Confluence' route that includes Varanasi (Hinduism's holiest city), Bodh Gaya (Buddhism's birthplace), Amritsar (Golden Temple, Sikhism), and the Ajanta-Ellora caves (representing Buddhist, Hindu, and Jain traditions).",
            'nature': "If you're interested in combining heritage with natural beauty, the 'Heritage and Landscape' route covers Darjeeling (Himalayan tea plantations), Kaziranga National Park (wildlife), and the living root bridges of Meghalaya, along with the cultural sites of Kolkata.",
            'south india': "For exploring South India's heritage, the 'Southern Heritage Circuit' connects Chennai's temples, Mahabalipuram's shore temples, Thanjavur's Brihadeshwara Temple, and Madurai's Meenakshi Temple, highlighting Dravidian architecture and culture.",
            'rajasthan': "The 'Royal Rajasthan' route covers the magnificent forts and palaces of Jaipur, Jodhpur, Udaipur, and Jaisalmer, showcasing Rajput architecture and desert culture in India's most colorful state."
        }
        
        for keyword, response in interest_keywords.items():
            if keyword in query.lower():
                return {
                    'answer': response,
                    'confidence': 0.8
                }
        
        # If no predefined route matches, suggest creating a personalized route
        return {
            'answer': "I don't have a specific route that matches your query, but I can help create a personalized route based on your interests. Would you prefer exploring temple architecture, Mughal monuments, Buddhist sites, or perhaps focusing on a specific region of India? Popular themed routes include the Golden Triangle (Delhi-Agra-Jaipur), the Buddhist Circuit in North India, the Temple Trail in South India, or the Himalayan Heritage route in the north.",
            'confidence': 0.6
        }
    
    def _calculate_route_distance(self, path):
        """Calculate the approximate distance of a route in kilometers"""
        if not path or len(path) < 2:
            return 0
            
        total_distance = 0
        for i in range(len(path) - 1):
            # Simple distance calculation using Haversine formula
            lat1, lon1 = path[i]
            lat2, lon2 = path[i+1]
            
            # Convert latitude and longitude from degrees to radians
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            
            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
            c = 2 * np.arcsin(np.sqrt(a))
            r = 6371  # Radius of Earth in kilometers
            distance = c * r
            
            total_distance += distance
            
        return round(total_distance)
    
    def _estimate_route_duration(self, path):
        """Estimate the duration of a route in days based on distance and sites"""
        # A very simple estimation:
        # - Each 300 km of travel takes approximately 1 day
        # - Each major site requires about 1-2 days to explore properly
        
        distance = self._calculate_route_distance(path)
        travel_days = distance / 300  # Rough estimate of travel time
        
        # Estimate number of major sites as number of points in the path
        site_days = len(path) * 1.5  # Average 1.5 days per site
        
        # Total days needed
        total_days = travel_days + site_days
        
        return max(round(total_days), 7)  # Minimum 7 days for a cultural route
        
    def _generate_suggestions(self, query, answer, location_id):
        """Generate follow-up question suggestions based on the context"""
        # Default suggestions
        default_suggestions = [
            "Tell me about the Taj Mahal",
            "What is the Buddhist Trail route?",
            "What are the most important UNESCO sites in India?"
        ]
        
        # Location-specific suggestions
        location_suggestions = {
            'taj-mahal': [
                "What is the story behind the Taj Mahal?",
                "When is the best time to visit the Taj Mahal?",
                "What other monuments are near the Taj Mahal?"
            ],
            'hampi': [
                "What is the historical significance of Hampi?",
                "Tell me about the architecture of Hampi",
                "What legends are associated with Hampi?"
            ],
            'delhi': [
                "What are Delhi's top monuments?",
                "What's the best season to visit Delhi?",
                "Tell me about Delhi's cultural heritage"
            ],
            'konark': [
                "What is the significance of the Sun Temple?",
                "Tell me about the architectural style of Konark",
                "What are the best things to see at Konark?"
            ],
            'khajuraho': [
                "Tell me about the erotic sculptures at Khajuraho",
                "What is the history of the Chandela Dynasty?",
                "How many temples are there in Khajuraho?"
            ],
            'ajanta': [
                "What makes Ajanta Caves unique?",
                "Tell me about the paintings in Ajanta",
                "What's the difference between Ajanta and Ellora?"
            ],
            'ellora': [
                "Tell me about the Kailasa Temple at Ellora",
                "Which dynasties contributed to Ellora Caves?",
                "What religious traditions are represented at Ellora?"
            ]
        }
        
        # Route-specific suggestions
        if 'buddhist' in query.lower() or 'trail' in query.lower() or 'route' in query.lower():
            return [
                "How many days do I need for the Buddhist trail?",
                "Which is the best season for this route?",
                "What are the most important sites on this route?"
            ]
            
        # Use location-specific suggestions if available
        if location_id and location_id in location_suggestions:
            return location_suggestions[location_id]
            
        # Content-based suggestions based on the answer
        if 'best time' in answer.lower() or 'season' in answer.lower():
            return [
                "How do I reach this location?",
                "What are the must-see attractions there?",
                "Are there any local festivals I should know about?"
            ]
            
        if 'architecture' in answer.lower() or 'monument' in answer.lower():
            return [
                "Who built this monument?",
                "What architectural style is it?",
                "What other similar sites are there in India?"
            ]
            
        if 'dynasty' in answer.lower() or 'emperor' in answer.lower() or 'king' in answer.lower():
            return [
                "What other monuments did they build?",
                "What was their period of rule?",
                "What was their cultural contribution?"
            ]
            
        # Fallback to default suggestions
        return default_suggestions
    
    def get_recommendations(self, preferences):
        """
        Get personalized location recommendations based on user preferences
        
        Parameters:
        - preferences: Dict with keys like 'interests', 'preferred_regions', etc.
        
        Returns:
        - List of recommended locations with reasons
        """
        # Extract preferences
        interests = preferences.get('interests', [])
        preferred_regions = preferences.get('preferred_regions', [])
        historical_periods = preferences.get('historical_periods', [])
        
        # Get all locations
        all_locations = self.kg_service.get_all_locations()
        
        # Score locations based on preferences
        scored_locations = []
        for location in all_locations:
            score = 0
            reasons = []
            
            # Score based on interests
            for interest in interests:
                # Check if interest is in tags, category, or description
                interest_lower = interest.lower()
                if any(interest_lower in tag.lower() for tag in location.tags):
                    score += 3
                    reasons.append(f"Matches your interest in {interest}")
                if interest_lower in location.category.lower():
                    score += 2
                if interest_lower in location.description.lower():
                    score += 1
            
            # Score based on historical periods
            for period in historical_periods:
                if period.lower() in location.period.lower() or period.lower() in location.dynasty.lower():
                    score += 2
                    reasons.append(f"From your preferred {period} period")
            
            # Add a small random factor for variety
            score += random.uniform(0, 0.5)
            
            if score > 0:
                scored_locations.append((location, score, reasons))
        
        # Sort by score and take top 5
        scored_locations.sort(key=lambda x: x[1], reverse=True)
        top_recommendations = scored_locations[:5]
        
        # Format recommendations
        recommendations = []
        for location, score, reasons in top_recommendations:
            # If we have multiple reasons, just take the top two
            if len(reasons) > 2:
                reasons = reasons[:2]
            # If we have no specific reasons, add a generic one
            if not reasons:
                reasons = ["Aligns with your travel preferences"]
                
            recommendations.append({
                'id': location.id,
                'name': location.name,
                'description': location.description,
                'reasons': reasons
            })
        
        return recommendations
