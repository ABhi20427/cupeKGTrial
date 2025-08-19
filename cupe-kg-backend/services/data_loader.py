# cupe-kg-backend/services/data_loader.py

"""
Data loading service for CuPe-KG
Handles loading and processing of cultural heritage data
"""

import logging
from typing import Dict, List, Any
from models.location import Location, Legend, Coordinates

logger = logging.getLogger(__name__)

class DataLoader:
    """Service for loading and managing cultural heritage data"""
    
    @staticmethod
    def load_placeholder_locations() -> Dict[str, Location]:
        """
        Load comprehensive placeholder location data
        This includes rich cultural information for testing
        """
        locations_data = [
            {
                "id": "hampi",
                "name": "Hampi",
                "description": "Ancient capital of the mighty Vijayanagara Empire, showcasing breathtaking temple architecture",
                "category": "historical",
                "coordinates": {"lat": 15.3350, "lng": 76.4600},
                "history": "Hampi was the capital of the Vijayanagara Empire from 1336 to 1646 CE, one of the greatest empires in South Indian history. At its peak, it was one of the largest and richest cities in the world, with a population of over 500,000. The city was a major trading center, dealing in spices, textiles, and precious stones.",
                "period": "1336 CE - 1646 CE",
                "dynasty": "Vijayanagara Empire",
                "cultural_facts": [
                    "UNESCO World Heritage Site since 1986",
                    "Contains over 1,600 surviving monuments",
                    "Famous for the iconic Stone Chariot at Vittala Temple",
                    "Unique fusion of Hindu and Islamic architectural styles",
                    "Home to the world's largest medieval-era stone structures"
                ],
                "legends": [
                    {
                        "title": "The Monkey Kingdom of Kishkindha",
                        "description": "According to the Ramayana, Hampi is believed to be the legendary Kishkindha, the kingdom of the monkey warriors. It was here that Lord Rama met Hanuman and Sugriva."
                    }
                ],
                "tags": ["UNESCO", "Vijayanagara", "temples", "heritage", "ruins", "Ramayana"],
                "best_time_to_visit": "October to March",
                "opening_hours": "Sunrise to Sunset",
                "entry_fee": "₹30 for Indians, ₹500 for foreigners"
            },
            {
                "id": "delhi",
                "name": "Delhi",
                "description": "Historic capital city representing layers of Indian civilization",
                "category": "cultural",
                "coordinates": {"lat": 28.7041, "lng": 77.1025},
                "history": "Delhi has been continuously inhabited since the 6th century BCE and has served as the capital for numerous empires. The city has witnessed the rise and fall of many dynasties including the Delhi Sultanate, Mughals, and British Raj.",
                "period": "6th century BCE - Present",
                "dynasty": "Multiple (Mughal, Delhi Sultanate, British, Modern India)",
                "cultural_facts": [
                    "Contains three UNESCO World Heritage Sites",
                    "Capital of seven different cities throughout history",
                    "Home to India's largest mosque, Jama Masjid",
                    "Birthplace of Urdu poetry and Hindustani classical music",
                    "Cultural melting pot of North Indian traditions"
                ],
                "legends": [
                    {
                        "title": "The Pandava Connection",
                        "description": "According to the Mahabharata, Delhi was originally called Indraprastha, the magnificent capital built by the Pandava brothers."
                    }
                ],
                "tags": ["capital", "Mughal", "Delhi Sultanate", "UNESCO", "multicultural", "Mahabharata"],
                "best_time_to_visit": "October to March",
                "opening_hours": "Varies by monument",
                "entry_fee": "Varies by monument"
            },
            {
                "id": "konark",
                "name": "Konark Sun Temple",
                "description": "Magnificent 13th-century temple designed as a colossal chariot of the Sun God",
                "category": "religious",
                "coordinates": {"lat": 19.8876, "lng": 86.0945},
                "history": "The Konark Sun Temple was built in the 13th century by King Narasimhadeva I of the Eastern Ganga Dynasty. It was designed as a massive chariot of Surya, the Sun God, with 24 intricately carved wheels and seven horses.",
                "period": "13th century CE",
                "dynasty": "Eastern Ganga Dynasty",
                "cultural_facts": [
                    "UNESCO World Heritage Site since 1984",
                    "Designed as Sun God's chariot with 24 wheels and 7 horses",
                    "Wheels function as accurate sundials",
                    "Famous for intricate erotic sculptures",
                    "Showcases Kalinga school of architecture at its pinnacle"
                ],
                "legends": [
                    {
                        "title": "Samba's Divine Cure",
                        "description": "Legend says Prince Samba, son of Lord Krishna, was cursed with leprosy. Following sage advice, he meditated here worshipping Surya for 12 years and was cured."
                    }
                ],
                "tags": ["Sun Temple", "UNESCO", "Kalinga architecture", "Eastern Ganga", "Surya", "religious"],
                "best_time_to_visit": "October to March",
                "opening_hours": "6:00 AM to 8:00 PM",
                "entry_fee": "₹25 for Indians, ₹300 for foreigners"
            },
            {
                "id": "taj_mahal",
                "name": "Taj Mahal",
                "description": "Iconic marble mausoleum, symbol of eternal love and pinnacle of Mughal architecture",
                "category": "historical",
                "coordinates": {"lat": 27.1751, "lng": 78.0421},
                "history": "The Taj Mahal was built by Mughal Emperor Shah Jahan in memory of his beloved wife Mumtaz Mahal, who died in childbirth in 1631. Construction began in 1632 and was completed in 1653.",
                "period": "1632 CE - 1653 CE",
                "dynasty": "Mughal Empire (Shah Jahan)",
                "cultural_facts": [
                    "UNESCO World Heritage Site since 1983",
                    "One of the New Seven Wonders of the World",
                    "Built with white Makrana marble that changes color throughout the day",
                    "Represents perfect symmetry in Islamic architecture",
                    "Symbol of India globally and masterpiece of world heritage"
                ],
                "legends": [
                    {
                        "title": "The Eternal Love Story",
                        "description": "Shah Jahan promised Mumtaz Mahal on her deathbed that he would build her the most beautiful tomb ever created. Legend says he planned to build a black marble mausoleum for himself across the river."
                    }
                ],
                "tags": ["UNESCO", "Mughal", "Shah Jahan", "mausoleum", "marble", "wonder", "love"],
                "best_time_to_visit": "October to March, sunrise and sunset",
                "opening_hours": "6:00 AM to 6:30 PM (Closed on Fridays)",
                "entry_fee": "₹50 for Indians, ₹1100 for foreigners"
            },
            {
                "id": "khajuraho",
                "name": "Khajuraho Group of Monuments",
                "description": "Spectacular medieval Hindu and Jain temples famous for intricate sculptures",
                "category": "religious",
                "coordinates": {"lat": 24.8318, "lng": 79.9199},
                "history": "The Khajuraho temples were built between 950 and 1050 CE by the Chandela dynasty rulers. Originally, there were over 85 temples, of which only 25 survive today.",
                "period": "950 CE - 1050 CE",
                "dynasty": "Chandela Dynasty",
                "cultural_facts": [
                    "UNESCO World Heritage Site since 1986",
                    "Represents the golden age of medieval Indian temple architecture",
                    "Famous for erotic sculptures representing tantric philosophy",
                    "Built without any mortar using precisely fitted sandstone blocks",
                    "Hosts annual Khajuraho Dance Festival"
                ],
                "legends": [
                    {
                        "title": "The Moon God's Love",
                        "description": "Legend tells of Hemavati, a beautiful priest's daughter who was seduced by the Moon God. Their son Chandravarman founded the Chandela dynasty."
                    }
                ],
                "tags": ["UNESCO", "Chandela", "temples", "sculpture", "medieval", "tantric", "dance"],
                "best_time_to_visit": "October to March",
                "opening_hours": "Sunrise to Sunset",
                "entry_fee": "₹30 for Indians, ₵500 for foreigners"
            }
        ]
        
        locations = {}
        for loc_data in locations_data:
            try:
                location = Location.from_dict(loc_data)
                locations[location.id] = location
                logger.info(f"Loaded location: {location.name}")
            except Exception as e:
                logger.error(f"Error creating location from data: {e}")
                continue
        
        logger.info(f"Successfully loaded {len(locations)} placeholder locations")
        return locations
    
    @staticmethod 
    def validate_location_data(location_data: Dict[str, Any]) -> bool:
        """
        Validate that location data has required fields
        """
        required_fields = ['id', 'name', 'description', 'category', 'coordinates']
        
        for field in required_fields:
            if field not in location_data:
                logger.warning(f"Location data missing required field: {field}")
                return False
        
        # Validate coordinates structure
        coords = location_data.get('coordinates', {})
        if not isinstance(coords, dict) or 'lat' not in coords or 'lng' not in coords:
            logger.warning("Invalid coordinates structure")
            return False
        
        # Validate coordinate values
        try:
            lat = float(coords['lat'])
            lng = float(coords['lng'])
            if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
                logger.warning("Coordinates out of valid range")
                return False
        except (ValueError, TypeError):
            logger.warning("Invalid coordinate values")
            return False
        
        return True
    
    @staticmethod
    def load_from_data_module() -> Dict[str, Location]:
        """
        Try to load from the data module first, fallback to placeholder if failed
        """
        try:
            # Try to import the data module
            from data.locations import get_expanded_locations
            location_data_list = get_expanded_locations()
            
            locations = {}
            for loc_data in location_data_list:
                if DataLoader.validate_location_data(loc_data):
                    try:
                        location = Location.from_dict(loc_data)
                        locations[location.id] = location
                    except Exception as e:
                        logger.error(f"Error creating location {loc_data.get('id', 'unknown')}: {e}")
                        continue
                else:
                    logger.warning(f"Invalid location data for {loc_data.get('id', 'unknown')}")
            
            if locations:
                logger.info(f"Successfully loaded {len(locations)} locations from data module")
                return locations
            else:
                logger.warning("No valid locations found in data module, using placeholder")
                return DataLoader.load_placeholder_locations()
                
        except ImportError as e:
            logger.info(f"Could not import data module: {e}. Using placeholder data.")
            return DataLoader.load_placeholder_locations()
        except Exception as e:
            logger.error(f"Error loading from data module: {e}. Using placeholder data.")
            return DataLoader.load_placeholder_locations()
    
    @staticmethod
    def enrich_with_relationships(locations: Dict[str, Location]) -> None:
        """
        Add relationship information between locations for knowledge graph
        """
        for location_id, location in locations.items():
            related_locations = []
            
            for other_id, other_location in locations.items():
                if other_id != location_id:
                    similarity = location.calculate_similarity(other_location)
                    if similarity > 0.3:  # Threshold for meaningful relationship
                        related_locations.append({
                            'id': other_id,
                            'name': other_location.name,
                            'similarity': similarity,
                            'relationship_type': DataLoader._determine_relationship_type(location, other_location)
                        })
            
            # Sort by similarity and keep top relationships
            related_locations.sort(key=lambda x: x['similarity'], reverse=True)
            
            # Store as a private attribute (you might want to add this to the Location model)
            setattr(location, '_related_locations', related_locations[:5])
    
    @staticmethod
    def _determine_relationship_type(loc1: Location, loc2: Location) -> str:
        """Determine the type of relationship between two locations"""
        if loc1.dynasty == loc2.dynasty and loc1.dynasty:
            return "same_dynasty"
        elif loc1.category == loc2.category:
            return "same_category"
        elif set(loc1.tags) & set(loc2.tags):
            return "shared_themes"
        else:
            return "general"
    
    @staticmethod
    def get_statistics(locations: Dict[str, Location]) -> Dict[str, Any]:
        """Get statistics about loaded locations"""
        if not locations:
            return {}
        
        categories = {}
        dynasties = {}
        periods = {}
        total_cultural_facts = 0
        total_legends = 0
        
        for location in locations.values():
            # Category stats
            categories[location.category] = categories.get(location.category, 0) + 1
            
            # Dynasty stats
            if location.dynasty:
                dynasties[location.dynasty] = dynasties.get(location.dynasty, 0) + 1
            
            # Period stats (simplified)
            if location.period:
                period_key = location.period.split(' - ')[0]  # Take start period
                periods[period_key] = periods.get(period_key, 0) + 1
            
            # Content stats
            total_cultural_facts += len(location.cultural_facts)
            total_legends += len(location.legends)
        
        return {
            'total_locations': len(locations),
            'categories': categories,
            'dynasties': dynasties,
            'periods': periods,
            'total_cultural_facts': total_cultural_facts,
            'total_legends': total_legends,
            'avg_cultural_facts_per_location': total_cultural_facts / len(locations),
            'avg_legends_per_location': total_legends / len(locations)
        }