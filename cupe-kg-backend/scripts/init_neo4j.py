# scripts/init_neo4j.py
from neo4j import GraphDatabase
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def init_database():
    driver = GraphDatabase.driver(
        Config.NEO4J_URI, 
        auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
    )
    
    with driver.session() as session:
        # Clear existing data
        session.run("MATCH (n) DETACH DELETE n")
        
        # Load locations
        locations_dir = os.path.join('data', 'locations')
        location_files = [f for f in os.listdir(locations_dir) if f.endswith('.json')]
        
        for file_name in location_files:
            file_path = os.path.join(locations_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                location_data = json.load(f)
                
                
                # Create location node
                session.run("""
                    CREATE (l:Location {
                        id: $id,
                        name: $name,
                        description: $description,
                        category: $category,
                        history: $history,
                        period: $period,
                        dynasty: $dynasty,
                        lat: $lat,
                        lng: $lng,
                        tags: $tags
                    })
                """, 
                id=location_data['id'],
                name=location_data['name'],
                description=location_data['description'],
                category=location_data['category'],
                history=location_data['history'],
                period=location_data['period'],
                dynasty=location_data['dynasty'],
                lat=location_data['coordinates']['lat'],
                lng=location_data['coordinates']['lng'],
                tags=location_data['tags']
                )
                
                print(f"Created location node for {location_data['name']}")
        
        # Create relationships based on shared tags, periods, dynasties
        session.run("""
            MATCH (l1:Location), (l2:Location) 
            WHERE l1 <> l2
            WITH l1, l2, [x IN l1.tags WHERE x IN l2.tags] AS commonTags
            WHERE size(commonTags) > 0
            CREATE (l1)-[r:SHARES_THEME {theme: commonTags, strength: size(commonTags)}]->(l2)
        """)
        
        session.run("""
            MATCH (l1:Location), (l2:Location) 
            WHERE l1 <> l2 AND l1.dynasty = l2.dynasty
            CREATE (l1)-[r:SAME_DYNASTY {dynasty: l1.dynasty, strength: 3}]->(l2)
        """)
        
        print("Created relationships between locations")
    
    driver.close()
    print("Database initialization complete")

if __name__ == "__main__":
    init_database()