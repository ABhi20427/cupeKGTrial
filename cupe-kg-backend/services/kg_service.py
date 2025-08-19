# cupe-kg-backend/services/kg_service.py

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
        
        # Load data
        if self.use_placeholder:
            # Try to load from data module first, fallback to placeholder
            self.placeholder_locations = DataLoader.load_from_data_module()
            
            # Enrich with relationships for knowledge graph functionality
            DataLoader.enrich_with_relationships(self.placeholder_locations)
            
            logger.info(f"Loaded {len(self.placeholder_locations)} locations")
            
            # Log statistics
            stats = DataLoader.get_statistics(self.placeholder_locations)
            logger.info(f"Location statistics: {stats}")
    
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
                    RETURN l.id as id, l.name as name, l.description as description,
                           l.category as category, l.history as history, 
                           l.period as period, l.dynasty as dynasty,
                           l.lat as lat, l.lng as lng, l.tags as tags
                """)
                
                locations = []
                for record in result:
                    # Convert Neo4j record to Location object
                    location_data = {
                        'id': record['id'],
                        'name': record['name'],
                        'description': record['description'],
                        'category': record['category'],
                        'coordinates': {
                            'lat': record['lat'],
                            'lng': record['lng']
                        },
                        'history': record['history'] or '',
                        'period': record['period'] or '',
                        'dynasty': record['dynasty'] or '',
                        'tags': record['tags'] or []
                    }
                    
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
                
        except Exception as e:
            logger.error(f"Error fetching locations from Neo4j: {e}")
            logger.warning("Falling back to placeholder data")
            return list(self.placeholder_locations.values())
    
    def get_location_by_id(self, location_id: str) -> Optional[Location]:
        """Get a specific location by its ID"""
        if self.use_placeholder:
            return self.placeholder_locations.get(location_id)
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location {id: $id})
                    RETURN l
                """, id=location_id)
                
                record = result.single()
                if record:
                    node = record["l"]
                    location_data = dict(node.items())
                    # Convert Neo4j format to our format
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    return Location.from_dict(location_data)
                
                return None
                
        except Exception as e:
            logger.error(f"Error fetching location {location_id} from Neo4j: {e}")
            # Fallback to placeholder
            return self.placeholder_locations.get(location_id)
    
    def get_related_locations(self, location_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get locations related to the specified location"""
        if self.use_placeholder:
            location = self.placeholder_locations.get(location_id)
            if not location:
                return []
            
            # Get precomputed relationships
            related = getattr(location, '_related_locations', [])
            
            # Convert to the expected format
            result = []
            for rel in related[:limit]:
                related_location = self.placeholder_locations.get(rel['id'])
                if related_location:
                    result.append({
                        'location': related_location.to_dict(),
                        'relationship': rel['relationship_type'],
                        'strength': rel['similarity']
                    })
            
            return result
        
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
                    LIMIT $limit
                """, id=location_id, limit=limit)
                
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
                        'strength': record["strength"] or 1.0
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
            # Fallback to placeholder
            location = self.placeholder_locations.get(location_id)
            if location:
                related = getattr(location, '_related_locations', [])
                result = []
                for rel in related[:limit]:
                    related_location = self.placeholder_locations.get(rel['id'])
                    if related_location:
                        result.append({
                            'location': related_location.to_dict(),
                            'relationship': rel['relationship_type'],
                            'strength': rel['similarity']
                        })
                return result
            return []
    
    def get_locations_by_category(self, category: str) -> List[Location]:
        """Get all locations in a specific category"""
        if self.use_placeholder:
            return [loc for loc in self.placeholder_locations.values() 
                   if loc.category.lower() == category.lower()]
        
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
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
                
        except Exception as e:
            logger.error(f"Error fetching locations by category {category}: {e}")
            return [loc for loc in self.placeholder_locations.values() 
                   if loc.category.lower() == category.lower()]
    
    def get_locations_by_period(self, period: str) -> List[Location]:
        """Get locations from a specific historical period"""
        if self.use_placeholder:
            return [loc for loc in self.placeholder_locations.values() 
                   if period.lower() in loc.period.lower()]
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    WHERE toLower(l.period) CONTAINS toLower($period)
                    RETURN l
                """, period=period)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
                
        except Exception as e:
            logger.error(f"Error fetching locations by period {period}: {e}")
            return [loc for loc in self.placeholder_locations.values() 
                   if period.lower() in loc.period.lower()]
    
    def get_locations_by_dynasty(self, dynasty: str) -> List[Location]:
        """Get locations associated with a specific dynasty"""
        if self.use_placeholder:
            return [loc for loc in self.placeholder_locations.values() 
                   if dynasty.lower() in loc.dynasty.lower()]
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    WHERE toLower(l.dynasty) CONTAINS toLower($dynasty)
                    RETURN l
                """, dynasty=dynasty)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
                
        except Exception as e:
            logger.error(f"Error fetching locations by dynasty {dynasty}: {e}")
            return [loc for loc in self.placeholder_locations.values() 
                   if dynasty.lower() in loc.dynasty.lower()]
    
    def search_locations(self, query: str) -> List[Location]:
        """Search locations by text query"""
        if self.use_placeholder:
            query_lower = query.lower()
            results = []
            
            for location in self.placeholder_locations.values():
                # Search in multiple fields
                searchable_text = f"{location.name} {location.description} {location.history} {location.dynasty} {' '.join(location.tags)} {' '.join(location.cultural_facts)}"
                
                if query_lower in searchable_text.lower():
                    results.append(location)
            
            return results
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    WHERE toLower(l.name) CONTAINS toLower($query)
                       OR toLower(l.description) CONTAINS toLower($query)
                       OR toLower(l.history) CONTAINS toLower($query)
                       OR toLower(l.dynasty) CONTAINS toLower($query)
                       OR ANY(tag IN l.tags WHERE toLower(tag) CONTAINS toLower($query))
                    RETURN l
                """, query=query)
                
                locations = []
                for record in result:
                    node = record["l"]
                    location_data = dict(node.items())
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    location = Location.from_dict(location_data)
                    locations.append(location)
                
                return locations
                
        except Exception as e:
            logger.error(f"Error searching locations with query '{query}': {e}")
            # Fallback to placeholder search
            query_lower = query.lower()
            return [loc for loc in self.placeholder_locations.values() 
                   if query_lower in f"{loc.name} {loc.description} {loc.history}".lower()]
    
    def get_cultural_themes(self) -> List[str]:
        """Get all unique cultural themes/tags across all locations"""
        if self.use_placeholder:
            all_themes = set()
            for location in self.placeholder_locations.values():
                all_themes.update(location.tags)
                all_themes.update(location.get_cultural_themes())
            return sorted(list(all_themes))
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    UNWIND l.tags as tag
                    RETURN DISTINCT tag
                    ORDER BY tag
                """)
                
                themes = [record["tag"] for record in result]
                return themes
                
        except Exception as e:
            logger.error(f"Error fetching cultural themes: {e}")
            # Fallback
            all_themes = set()
            for location in self.placeholder_locations.values():
                all_themes.update(location.tags)
            return sorted(list(all_themes))
    
    def get_dynasties(self) -> List[str]:
        """Get all unique dynasties"""
        if self.use_placeholder:
            dynasties = set()
            for location in self.placeholder_locations.values():
                if location.dynasty:
                    dynasties.add(location.dynasty)
            return sorted(list(dynasties))
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l:Location)
                    WHERE l.dynasty IS NOT NULL AND l.dynasty <> ''
                    RETURN DISTINCT l.dynasty as dynasty
                    ORDER BY dynasty
                """)
                
                dynasties = [record["dynasty"] for record in result]
                return dynasties
                
        except Exception as e:
            logger.error(f"Error fetching dynasties: {e}")
            dynasties = set()
            for location in self.placeholder_locations.values():
                if location.dynasty:
                    dynasties.add(location.dynasty)
            return sorted(list(dynasties))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the knowledge graph"""
        if self.use_placeholder:
            return DataLoader.get_statistics(self.placeholder_locations)
        
        try:
            with self.driver.session() as session:
                # Get basic counts
                location_count = session.run("MATCH (l:Location) RETURN count(l) as count").single()["count"]
                
                # Get category distribution
                category_result = session.run("""
                    MATCH (l:Location)
                    RETURN l.category as category, count(*) as count
                    ORDER BY count DESC
                """)
                categories = {record["category"]: record["count"] for record in category_result}
                
                # Get dynasty distribution
                dynasty_result = session.run("""
                    MATCH (l:Location)
                    WHERE l.dynasty IS NOT NULL AND l.dynasty <> ''
                    RETURN l.dynasty as dynasty, count(*) as count
                    ORDER BY count DESC
                """)
                dynasties = {record["dynasty"]: record["count"] for record in dynasty_result}
                
                # Get relationship counts
                relationship_result = session.run("""
                    MATCH ()-[r]->()
                    RETURN TYPE(r) as relationship_type, count(r) as count
                """)
                relationships = {record["relationship_type"]: record["count"] for record in relationship_result}
                
                return {
                    'total_locations': location_count,
                    'categories': categories,
                    'dynasties': dynasties,
                    'relationships': relationships,
                    'data_source': 'neo4j'
                }
                
        except Exception as e:
            logger.error(f"Error fetching statistics from Neo4j: {e}")
            return DataLoader.get_statistics(self.placeholder_locations)