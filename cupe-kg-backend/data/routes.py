# data/routes.py

"""
This module contains predefined cultural routes data.
Each route is a dictionary containing:
- name: Name of the route
- description: Description of the route
- locations: List of locations in the route, each with:
  - name: Location name
  - coordinates: [latitude, longitude]
  - description: Location description
"""

routes = [
    {
        "id": "temple-route-1",
        "name": "Ancient Temples Route",
        "description": "A journey through India's most significant temple sites",
        "color": "#3f51b5",  # Material UI primary blue
        "path": [],  # Will be computed by the service
        "dashArray": None,
        "locations": [
            {
                "name": "Hampi",
                "coordinates": [15.3350, 76.4600],
                "description": "Ancient temple complex in Karnataka"
            }
            # Add more locations as needed
        ]
    }
    # Add more routes as needed
]
