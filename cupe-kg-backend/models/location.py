# cupe-kg-backend/models/location.py

"""
Location model for CuPe-KG project
Represents a cultural heritage location with all relevant information
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Legend:
    """Represents a legend or story associated with a location"""
    title: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'title': self.title,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Legend':
        return cls(
            title=data.get('title', ''),
            description=data.get('description', '')
        )

@dataclass
class Coordinates:
    """Represents geographical coordinates"""
    lat: float
    lng: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'lat': self.lat,
            'lng': self.lng
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Coordinates':
        return cls(
            lat=float(data.get('lat', 0.0)),
            lng=float(data.get('lng', 0.0))
        )

@dataclass
class Location:
    """
    Represents a cultural heritage location with comprehensive information
    """
    id: str
    name: str
    description: str
    category: str  # historical, religious, cultural, natural
    coordinates: Coordinates
    history: str = ""
    period: str = ""
    dynasty: str = ""
    cultural_facts: List[str] = field(default_factory=list)
    legends: List[Legend] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    # Optional fields for enhanced functionality
    images: List[str] = field(default_factory=list)
    best_time_to_visit: str = ""
    entry_fee: str = ""
    opening_hours: str = ""
    accessibility: str = ""
    nearby_attractions: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert location to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'coordinates': self.coordinates.to_dict(),
            'history': self.history,
            'period': self.period,
            'dynasty': self.dynasty,
            'culturalFacts': self.cultural_facts,  # Frontend expects camelCase
            'legends': [legend.to_dict() for legend in self.legends],
            'tags': self.tags,
            'images': self.images,
            'bestTimeToVisit': self.best_time_to_visit,
            'entryFee': self.entry_fee,
            'openingHours': self.opening_hours,
            'accessibility': self.accessibility,
            'nearbyAttractions': self.nearby_attractions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        """Create location from dictionary data"""
        # Handle coordinates
        coords_data = data.get('coordinates', {})
        if isinstance(coords_data, dict):
            coordinates = Coordinates.from_dict(coords_data)
        else:
            # Fallback for invalid coordinate data
            coordinates = Coordinates(lat=0.0, lng=0.0)
        
        # Handle legends
        legends_data = data.get('legends', [])
        legends = []
        for legend_data in legends_data:
            if isinstance(legend_data, dict):
                legends.append(Legend.from_dict(legend_data))
        
        # Handle cultural_facts (support both camelCase and snake_case)
        cultural_facts = (
            data.get('cultural_facts', []) or 
            data.get('culturalFacts', []) or 
            []
        )
        
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            description=data.get('description', ''),
            category=data.get('category', 'unknown'),
            coordinates=coordinates,
            history=data.get('history', ''),
            period=data.get('period', ''),
            dynasty=data.get('dynasty', ''),
            cultural_facts=cultural_facts,
            legends=legends,
            tags=data.get('tags', []),
            images=data.get('images', []),
            best_time_to_visit=data.get('best_time_to_visit', '') or data.get('bestTimeToVisit', ''),
            entry_fee=data.get('entry_fee', '') or data.get('entryFee', ''),
            opening_hours=data.get('opening_hours', '') or data.get('openingHours', ''),
            accessibility=data.get('accessibility', ''),
            nearby_attractions=data.get('nearby_attractions', []) or data.get('nearbyAttractions', [])
        )
    
    def get_cultural_themes(self) -> List[str]:
        """Extract cultural themes from tags and cultural facts"""
        themes = []
        
        # Add tags as themes
        themes.extend(self.tags)
        
        # Extract themes from cultural facts (basic keyword extraction)
        theme_keywords = [
            'architecture', 'temple', 'fort', 'palace', 'monument', 
            'UNESCO', 'heritage', 'dynasty', 'empire', 'art', 'sculpture',
            'religious', 'spiritual', 'pilgrimage', 'festival', 'tradition'
        ]
        
        for fact in self.cultural_facts:
            fact_lower = fact.lower()
            for keyword in theme_keywords:
                if keyword in fact_lower and keyword not in themes:
                    themes.append(keyword)
        
        return themes
    
    def calculate_similarity(self, other: 'Location') -> float:
        """Calculate similarity score with another location (0-1)"""
        if not isinstance(other, Location):
            return 0.0
        
        score = 0.0
        total_factors = 0
        
        # Category similarity
        if self.category == other.category:
            score += 0.3
        total_factors += 0.3
        
        # Dynasty similarity
        if self.dynasty and other.dynasty and self.dynasty == other.dynasty:
            score += 0.25
        total_factors += 0.25
        
        # Tag similarity
        common_tags = set(self.tags) & set(other.tags)
        if self.tags and other.tags:
            tag_similarity = len(common_tags) / max(len(self.tags), len(other.tags))
            score += tag_similarity * 0.25
        total_factors += 0.25
        
        # Period similarity (simplified)
        if self.period and other.period:
            # Very basic period matching - can be enhanced
            if any(word in self.period.lower() for word in other.period.lower().split()):
                score += 0.2
        total_factors += 0.2
        
        return score / total_factors if total_factors > 0 else 0.0
    
    def get_summary(self, max_length: int = 200) -> str:
        """Get a short summary of the location"""
        summary = self.description
        
        if len(summary) > max_length:
            # Truncate at word boundary
            summary = summary[:max_length].rsplit(' ', 1)[0] + '...'
        
        return summary
    
    def __str__(self) -> str:
        return f"Location(id='{self.id}', name='{self.name}', category='{self.category}')"
    
    def __repr__(self) -> str:
        return self.__str__()
    