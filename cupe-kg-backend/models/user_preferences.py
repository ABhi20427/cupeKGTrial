# models/user_preferences.py

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

class InterestType(Enum):
    HISTORICAL = "historical"
    RELIGIOUS = "religious"
    ARCHITECTURAL = "architectural"
    CULTURAL = "cultural"
    ARCHAEOLOGICAL = "archaeological"
    ROYAL_HERITAGE = "royal_heritage"
    ANCIENT_TEMPLES = "ancient_temples"
    FORTS_PALACES = "forts_palaces"
    UNESCO_SITES = "unesco_sites"

class TransportMode(Enum):
    CAR = "car"
    TRAIN = "train"
    BUS = "bus"
    FLIGHT = "flight"
    MIXED = "mixed"

@dataclass
class UserPreferences:
    # Core interests
    interests: List[InterestType]
    
    # Travel constraints
    max_travel_days: int
    budget_range: str  # "low", "medium", "high"
    transport_mode: TransportMode
    
    # Geographic preferences
    start_location: Optional[Dict[str, float]] = None  # {"lat": float, "lng": float}
    preferred_regions: List[str] = None  # ["south_india", "north_india", etc.]
    max_distance_km: Optional[int] = None
    
    # Historical preferences
    preferred_periods: List[str] = None  # ["mughal", "vijayanagara", "medieval", etc.]
    preferred_dynasties: List[str] = None
    
    # Experience preferences
    crowd_preference: str = "medium"  # "low", "medium", "high"
    accommodation_type: str = "medium"  # "budget", "medium", "luxury"
    cultural_activities: List[str] = None  # ["festivals", "local_food", "crafts", etc.]
    
    # Accessibility needs
    accessibility_required: bool = False
    physical_difficulty_preference: str = "medium"  # "easy", "medium", "difficult"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'interests': [interest.value if isinstance(interest, InterestType) else interest for interest in self.interests],
            'max_travel_days': self.max_travel_days,
            'budget_range': self.budget_range,
            'transport_mode': self.transport_mode.value if isinstance(self.transport_mode, TransportMode) else self.transport_mode,
            'start_location': self.start_location,
            'preferred_regions': self.preferred_regions or [],
            'max_distance_km': self.max_distance_km,
            'preferred_periods': self.preferred_periods or [],
            'preferred_dynasties': self.preferred_dynasties or [],
            'crowd_preference': self.crowd_preference,
            'accommodation_type': self.accommodation_type,
            'cultural_activities': self.cultural_activities or [],
            'accessibility_required': self.accessibility_required,
            'physical_difficulty_preference': self.physical_difficulty_preference
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        # Handle interests with safe error checking
        interests = []
        for interest in data.get('interests', []):
            if isinstance(interest, str):
                try:
                    interests.append(InterestType(interest))
                except ValueError:
                    print(f"Warning: Unknown interest type '{interest}' - skipping")
                    continue
            else:
                interests.append(interest)
        
        # Handle transport mode with fallback
        transport_mode = TransportMode.CAR
        transport_str = data.get('transport_mode', 'car')
        try:
            transport_mode = TransportMode(transport_str)
        except ValueError:
            print(f"Warning: Unknown transport mode '{transport_str}' - using default 'car'")
        
        return cls(
            interests=interests,
            max_travel_days=data.get('max_travel_days', 7),
            budget_range=data.get('budget_range', 'medium'),
            transport_mode=transport_mode,
            start_location=data.get('start_location'),
            preferred_regions=data.get('preferred_regions'),
            max_distance_km=data.get('max_distance_km'),
            preferred_periods=data.get('preferred_periods'),
            preferred_dynasties=data.get('preferred_dynasties'),
            crowd_preference=data.get('crowd_preference', 'medium'),
            accommodation_type=data.get('accommodation_type', 'medium'),
            cultural_activities=data.get('cultural_activities'),
            accessibility_required=data.get('accessibility_required', False),
            physical_difficulty_preference=data.get('physical_difficulty_preference', 'medium')
        )
