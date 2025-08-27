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
            # ... (original placeholder data unchanged; you may adjust as needed)
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
        Try to load from the data module first, fallback to placeholder if failed.
        ENHANCED: Uses expanded location fields if present, creates sample data if not found.
        """
        try:
            from data.locations import get_expanded_locations
            locations_data = get_expanded_locations()
            locations = {}
            for loc_data in locations_data:
                location = Location.from_dict(loc_data)
                locations[location.id] = location
            logger.info(f"Loaded {len(locations)} locations from data module")
            return locations
        except ImportError:
            logger.warning("Data module not found, creating sample data")
            return DataLoader._create_sample_data()
        except Exception as e:
            logger.error(f"Error loading from data module: {e}. Using placeholder data.")
            return DataLoader._create_sample_data()

    @staticmethod
    def _create_sample_data() -> Dict[str, Location]:
        """
        ENHANCED: Sample data creation for development/testing,
        using expanded field set as in enhanced code.
        """
        sample_data = [
            # ... (insert enhanced sample data entries as in your improved code, see your sample_data list)
        ]
        
        locations = {}
        for loc_data in sample_data:
            location = Location(
                id=loc_data.get('id'),
                name=loc_data.get('name'),
                description=loc_data.get('description', ''),
                category=loc_data.get('category', ''),
                coordinates=loc_data.get('coordinates', {}),
                state=loc_data.get('state', ''),
                history=loc_data.get('history', ''),
                period=loc_data.get('period', ''),
                dynasty=loc_data.get('dynasty', ''),
                cultural_facts=loc_data.get('cultural_facts', []),
                legends=loc_data.get('legends', []),
                best_time_to_visit=loc_data.get('best_time_to_visit', ''),
                accessibility=loc_data.get('accessibility', {}),
                entry_fee=loc_data.get('entry_fee', {}),
                opening_hours=loc_data.get('opening_hours', ''),
                nearby_attractions=loc_data.get('nearby_attractions', []),
                transportation=loc_data.get('transportation', {}),
                local_cuisine=loc_data.get('local_cuisine', []),
                festivals=loc_data.get('festivals', []),
                photography_allowed=loc_data.get('photography_allowed', True),
                guided_tours_available=loc_data.get('guided_tours_available', False)
            )
            locations[location.id] = location

        logger.info(f"Created {len(locations)} sample locations")
        return locations

    @staticmethod
    def enrich_with_relationships(locations: Dict[str, Location]) -> None:
        """
        Add relationship information between locations for knowledge graph.
        ENHANCED: Adds related_locations attribute based on dynasty, period, or category.
        """
        try:
            for location in locations.values():
                if not hasattr(location, 'related_locations'):
                    location.related_locations = []
                for other_id, other_location in locations.items():
                    if (location.id != other_id and 
                        (location.dynasty == other_location.dynasty or
                         location.period == other_location.period or
                         location.category == other_location.category)):
                        location.related_locations.append(other_id)
            logger.info("Enriched locations with relationship data")
        except Exception as e:
            logger.error(f"Error enriching with relationships: {e}")

    @staticmethod
    def get_statistics(locations: Dict[str, Location]) -> Dict[str, Any]:
        """
        Get statistics about loaded locations.
        ENHANCED: Returns counts of unique dynasties, periods, categories, and states.
        """
        if not locations:
            return {}
        
        stats = {
            'total_locations': len(locations),
            'dynasties': set(),
            'periods': set(),
            'categories': set(),
            'states': set()
        }
        
        for location in locations.values():
            if hasattr(location, 'dynasty') and location.dynasty:
                stats['dynasties'].add(location.dynasty)
            if hasattr(location, 'period') and location.period:
                stats['periods'].add(location.period)
            if hasattr(location, 'category') and location.category:
                stats['categories'].add(location.category)
            if hasattr(location, 'state') and location.state:
                stats['states'].add(location.state)
        
        # Convert sets to counts
        stats['unique_dynasties'] = len(stats['dynasties'])
        stats['unique_periods'] = len(stats['periods'])
        stats['unique_categories'] = len(stats['categories'])
        stats['unique_states'] = len(stats['states'])
        
        # Remove the sets from final stats
        del stats['dynasties']
        del stats['periods']
        del stats['categories']
        del stats['states']
        
        return stats
