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
                from neo4j import GraphDatabase
                from config import Config
                
                self.driver = GraphDatabase.driver(
                    Config.NEO4J_URI, 
                    auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
                )
                logger.info("Connected to Neo4j database")
            except Exception as e:
                logger.error(f"Failed to connect to Neo4j: {e}")
                logger.warning("Falling back to placeholder data")
                self.use_placeholder = True
        
        if self.use_placeholder:
            self.placeholder_locations = DataLoader.load_from_data_module()
            DataLoader.enrich_with_relationships(self.placeholder_locations)
            logger.info(f"Loaded {len(self.placeholder_locations)} locations")
            stats = DataLoader.get_statistics(self.placeholder_locations)
            logger.info(f"Location statistics: {stats}")
    
    def close(self):
        if not self.use_placeholder and hasattr(self, 'driver'):
            self.driver.close()
    
    def get_all_locations(self) -> List[Location]:
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
                    if 'lat' in location_data and 'lng' in location_data:
                        location_data['coordinates'] = {
                            'lat': location_data.pop('lat'),
                            'lng': location_data.pop('lng')
                        }
                    return Location.from_dict(location_data)
                return None
        except Exception as e:
            logger.error(f"Error fetching location {location_id} from Neo4j: {e}")
            return self.placeholder_locations.get(location_id)

    def get_related_locations(self, location_id, max_results=5):
        if self.use_placeholder:
            try:
                current_location = self.placeholder_locations.get(location_id)
                if not current_location:
                    return []
                
                related = []
                for loc_id, location in self.placeholder_locations.items():
                    if loc_id != location_id:
                        similarity_score = 0
                        if (hasattr(current_location, 'dynasty') and hasattr(location, 'dynasty') and
                            current_location.dynasty == location.dynasty):
                            similarity_score += 3
                        if (hasattr(current_location, 'period') and hasattr(location, 'period') and
                            current_location.period == location.period):
                            similarity_score += 2
                        if (hasattr(current_location, 'category') and hasattr(location, 'category') and
                            current_location.category == location.category):
                            similarity_score += 1
                        
                        if similarity_score > 0:
                            related.append({
                                'location': location.to_dict(),
                                'similarity_score': similarity_score
                            })
                
                related.sort(key=lambda x: x['similarity_score'], reverse=True)
                return [item['location'] for item in related[:max_results]]
            except Exception as e:
                logger.error(f"Error getting related locations: {e}")
                return []
        
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (l1:Location {id: $location_id})
                    MATCH (l2:Location)
                    WHERE l1 <> l2 AND (
                        l1.dynasty = l2.dynasty OR 
                        l1.period = l2.period OR 
                        l1.category = l2.category
                    )
                    RETURN l2, 
                    CASE 
                        WHEN l1.dynasty = l2.dynasty THEN 3
                        WHEN l1.period = l2.period THEN 2  
                        WHEN l1.category = l2.category THEN 1
                        ELSE 0
                    END as similarity
                    ORDER BY similarity DESC
                    LIMIT $max_results
                """, location_id=location_id, max_results=max_results)
                
                related_locations = []
                for record in result:
                    location_data = record["l2"]
                    location = Location(
                        id=location_data["id"],
                        name=location_data["name"],
                        description=location_data.get("description", ""),
                        category=location_data.get("category", ""),
                        coordinates={"lat": location_data.get("lat"), "lng": location_data.get("lng")},
                        history=location_data.get("history", ""),
                        period=location_data.get("period", ""),
                        dynasty=location_data.get("dynasty", "")
                    )
                    related_locations.append(location.to_dict())
                
                return related_locations
        except Exception as e:
            logger.error(f"Error querying related locations from Neo4j: {e}")
            return []

    def get_locations_by_category(self, category: str) -> List[Location]:
        if self.use_placeholder:
            return [
                loc for loc in self.placeholder_locations.values()
                if hasattr(loc, 'category') and loc.category and category.lower() in loc.category.lower()
            ]
        
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
            return [
                loc for loc in self.placeholder_locations.values()
                if hasattr(loc, 'category') and loc.category and category.lower() in loc.category.lower()
            ]

    def get_locations_by_period(self, period: str) -> List[Location]:
        if self.use_placeholder:
            filtered_locations = []
            for location in self.placeholder_locations.values():
                if hasattr(location, 'period') and location.period and period.lower() in location.period.lower():
                    filtered_locations.append(location)
            return filtered_locations
        
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
            logger.error(f"Error getting locations by period: {e}")
            return []

    def get_locations_by_dynasty(self, dynasty: str) -> List[Location]:
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
        if self.use_placeholder:
            query_lower = query.lower()
            results = []
            for location in self.placeholder_locations.values():
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
            query_lower = query.lower()
            return [loc for loc in self.placeholder_locations.values() 
                   if query_lower in f"{loc.name} {loc.description} {loc.history}".lower()]

    def get_cultural_themes(self) -> List[str]:
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
            all_themes = set()
            for location in self.placeholder_locations.values():
                all_themes.update(location.tags)
            return sorted(list(all_themes))

    def get_dynasties(self) -> List[str]:
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
        if self.use_placeholder:
            return DataLoader.get_statistics(self.placeholder_locations)
        
        try:
            with self.driver.session() as session:
                location_count = session.run("MATCH (l:Location) RETURN count(l) as count").single()["count"]
                category_result = session.run("""
                    MATCH (l:Location)
                    RETURN l.category as category, count(*) as count
                    ORDER BY count DESC
                """)
                categories = {record["category"]: record["count"] for record in category_result}
                
                dynasty_result = session.run("""
                    MATCH (l:Location)
                    WHERE l.dynasty IS NOT NULL AND l.dynasty <> ''
                    RETURN l.dynasty as dynasty, count(*) as count
                    ORDER BY count DESC
                """)
                dynasties = {record["dynasty"]: record["count"] for record in dynasty_result}
                
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
