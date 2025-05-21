# services/kg_service.py

import logging
from typing import List, Dict, Any, Optional
from models.location import Location
from services.data_loader import DataLoader

logger = logging.getLogger(__name__)

class KnowledgeGraphService:
    def __init__(self, use_placeholder=True):
        self.use_placeholder = use_placeholder
        
        if not use_placeholder:
            try:
                # Import Neo4j here to avoid errors if not installed
                from neo4j import GraphDatabase
                from config import Config
                
                # Connect to Neo4j
                self.driver = GraphDatabase.driver(
                    Config.NEO4J_URI, 
                    auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
                )
                logger.info("Connected to Neo4j database")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                logger.warning("Falling back to placeholder data")
                self.use_placeholder = True
        
        # Load placeholder data
        if self.use_placeholder:
            self.placeholder_locations = self._load_locations_from_data()
            logger.info(f"Loaded {len(self.placeholder_locations)} locations from placeholder data")
    
    def _load_locations_from_data(self):
        """Load location data from the data module"""
        locations = {}
        
        # Get expanded locations from data/locations.py
        try:
            from data.locations import get_expanded_locations
            location_data = get_expanded_locations()
            
            for loc_dict in location_data:
                location = Location.from_dict(loc_dict)
                locations[location.id] = location
                
        except (ImportError, AttributeError) as e:
            logger.error(f"Error loading expanded locations: {e}")
            # Fall back to basic placeholder data
            locations = DataLoader.load_placeholder_locations()
            
        return locations
    
    def close(self):
        """Close database connection if using Neo4j"""
        if not self.use_placeholder and hasattr(self, 'driver'):
            self.driver.close()
    
    def get_all_locations(self) -> List[Location]:
        """Get all available locations"""
        if self.use_placeholder:
            return list(self.placeholder_locations.values())
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    RETURN l
                """)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    # Convert Neo4j format to our model format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
        except Exception as e:
            logger.error(f"Error fetching locations from Neo4j: {e}")
            return list(self.placeholder_locations.values())
    
    def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """Get a specific location by ID"""
        if self.use_placeholder:
            return self.placeholder_locations.get(location_id)
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location {id: $id})
                    RETURN l
                """, id=location_id)
                
                record = result.single()
                if not record:
                    return None
                    
                node = record["l"]
                location_data = dict(node.items())
                # Convert Neo4j format to our model format
                if 'lat' in location_data and 'lng' in location_data:
                    location_data['coordinates'] = {
                        'lat': location_data.pop('lat'),
                        'lng': location_data.pop('lng')
                    }
                return Location.from_dict(location_data)
        except Exception as e:
            logger.error(f"Error fetching location {location_id} from Neo4j: {e}")
            return self.placeholder_locations.get(location_id)
    
    def get_locations_by_period(self, period: str) -> List[Location]:
        """Get locations from a specific historical period"""
        if self.use_placeholder:
            return [loc for loc in self.placeholder_locations.values() if period.lower() in loc.period.lower()]
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    WHERE l.period CONTAINS $period
                    RETURN l
                """, period=period)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    # Convert Neo4j format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
        except Exception as e:
            logger.error(f"Error fetching locations by period {period} from Neo4j: {e}")
            return [loc for loc in self.placeholder_locations.values() if period.lower() in loc.period.lower()]
    
    def get_locations_by_category(self, category: str) -> List[Location]:
        """Get locations of a specific category (historical, religious, cultural)"""
        if self.use_placeholder:
            return [loc for loc in self.placeholder_locations.values() if loc.category.lower() == category.lower()]
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location {category: $category})
                    RETURN l
                """, category=category)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    # Convert Neo4j format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
        except Exception as e:
            logger.error(f"Error fetching locations by category {category} from Neo4j: {e}")
            return [loc for loc in self.placeholder_locations.values() if loc.category.lower() == category.lower()]
    
    def get_related_locations(self, location_id: str) -> List[Dict[str, Any]]:
        """Get locations related to a specific location"""
        if self.use_placeholder:
            # For placeholder data, find locations with similar tags
            source_location = self.placeholder_locations.get(location_id)
            if not source_location:
                return []
            
            related = []
            for loc in self.placeholder_locations.values():
                if loc.id == location_id:
                    continue
                
                # Find common tags
                common_tags = [tag for tag in loc.tags if tag in source_location.tags]
                if common_tags:
                    related.append({
                        'location': loc.to_dict(),
                        'relationship': 'SHARES_THEME',
                        'commonTags': common_tags,
                        'strength': len(common_tags)
                    })
                
                # Check for same dynasty
                if loc.dynasty == source_location.dynasty:
                    related.append({
                        'location': loc.to_dict(),
                        'relationship': 'SAME_DYNASTY',
                        'dynasty': loc.dynasty,
                        'strength': 3
                    })
                
                # Check for same period
                if loc.period == source_location.period:
                    related.append({
                        'location': loc.to_dict(),
                        'relationship': 'SAME_PERIOD',
                        'period': loc.period,
                        'strength': 2
                    })
                
                # Check for same category
                if loc.category == source_location.category:
                    related.append({
                        'location': loc.to_dict(),
                        'relationship': 'SAME_CATEGORY',
                        'category': loc.category,
                        'strength': 1
                    })
            
            # Remove duplicates (prefer stronger relationships)
            seen_ids = set()
            unique_related = []
            for rel in sorted(related, key=lambda x: x['strength'], reverse=True):
                loc_id = rel['location']['id']
                if loc_id not in seen_ids:
                    seen_ids.add(loc_id)
                    unique_related.append(rel)
            
            return unique_related[:5]  # Return top 5 related locations
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l1:Location {id: $id})-[r]-(l2:Location)
                    RETURN l2 as location, TYPE(r) as relationship, r.strength as strength, 
                           CASE 
                             WHEN TYPE(r) = 'SHARES_THEME' THEN r.theme 
                             WHEN TYPE(r) = 'SAME_DYNASTY' THEN r.dynasty
                             ELSE NULL 
                           END as commonProperty
                    ORDER BY r.strength DESC
                """, id=location_id)
                
                related = []
                for record in result:
                    node = record["location"]
                    location_data = dict(node.items())
                    # Convert Neo4j format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    
                    relation_info = {
                        'location': location.to_dict(),
                        'relationship': record["relationship"],
                        'strength': record["strength"]
                    }
                    
                    # Add relationship-specific properties
                    common_property = record["commonProperty"]
                    if common_property:
                        if relation_info['relationship'] == 'SHARES_THEME':
                            relation_info['commonTags'] = common_property
                        elif relation_info['relationship'] == 'SAME_DYNASTY':
                            relation_info['dynasty'] = common_property
                    
                    related.append(relation_info)
                
                return related
        except Exception as e:
            logger.error(f"Error fetching related locations for {location_id} from Neo4j: {e}")
            # Fall back to placeholder implementation
            return self.get_related_locations(location_id)
    
    def search_locations(self, query: str) -> List[Location]:
        """Search for locations by keyword"""
        if self.use_placeholder:
            results = []
            query_lower = query.lower()
            
            for location in self.placeholder_locations.values():
                # Search in name, description, history
                search_text = f"{location.name} {location.description} {location.history} {location.dynasty}".lower()
                
                # Add cultural facts and tags to search text
                for fact in getattr(location, 'cultural_facts', []):
                    search_text += " " + fact.lower()
                for tag in getattr(location, 'tags', []):
                    search_text += " " + tag.lower()
                
                # Check if query is in search text
                if query_lower in search_text:
                    results.append(location)
            
            return results
        
        try:
            with self.driver.session() as session:
                # Customize this query based on your Neo4j schema
                result = session.run("""
                    MATCH (l:Location)
                    WHERE l.name CONTAINS $query OR 
                          l.description CONTAINS $query OR 
                          l.history CONTAINS $query OR 
                          l.dynasty CONTAINS $query OR
                          ANY(tag IN l.tags WHERE tag CONTAINS $query)
                    RETURN l
                """, query=query)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    # Convert Neo4j format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
        except Exception as e:
            logger.error(f"Error searching locations with query '{query}' in Neo4j: {e}")
            return self.search_locations(query)