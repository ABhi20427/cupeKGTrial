# models/route.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RouteLocation:
    name: str
    coordinates: List[float]
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'coordinates': self.coordinates,
            'description': self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RouteLocation':
        return cls(
            name=data.get('name'),
            coordinates=data.get('coordinates', []),
            description=data.get('description', '')
        )

@dataclass
class Route:
    id: str
    name: str
    description: str
    color: str
    path: List[List[float]] = field(default_factory=list)
    locations: List[RouteLocation] = field(default_factory=list)
    dash_array: str = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'path': self.path,
            'locations': [loc.to_dict() for loc in self.locations],
            'dashArray': self.dash_array
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Route':
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description', ''),
            color=data.get('color', '#3f51b5'),
            path=data.get('path', []),
            locations=[RouteLocation.from_dict(loc) for loc in data.get('locations', [])],
            dash_array=data.get('dashArray')
        )