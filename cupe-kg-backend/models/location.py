# models/location.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Location:
    id: str
    name: str
    description: str
    coordinates: Dict[str, float]
    category: str
    history: str
    period: str
    dynasty: str
    cultural_facts: List[str] = field(default_factory=list)
    legends: List[Dict[str, str]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'coordinates': self.coordinates,
            'category': self.category,
            'history': self.history,
            'period': self.period,
            'dynasty': self.dynasty,
            'culturalFacts': self.cultural_facts,
            'legends': self.legends,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            coordinates=data.get('coordinates', {}),
            category=data.get('category'),
            history=data.get('history', ''),
            period=data.get('period', ''),
            dynasty=data.get('dynasty', ''),
            cultural_facts=data.get('culturalFacts', []),
            legends=data.get('legends', []),
            tags=data.get('tags', [])
        )