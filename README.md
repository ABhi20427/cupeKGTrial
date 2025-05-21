# CuPe-KG: Cultural Perspective-Based Knowledge Graph for Tourism Resources

## Project Overview

CuPe-KG is an interactive web application that visualizes cultural and historical sites across India through an engaging map interface. The application leverages a knowledge graph backend to present rich information about various locations, their historical significance, cultural facts, and associated legends or stories.

### Key Features

- **Interactive India Map:** Displays markers for significant locations like Hampi, Delhi, and Konark
- **Detailed Information Panels:** When a location is selected, displays comprehensive information including:
  - Historical significance 
  - Cultural facts
  - Legends and stories
  - Period/dynasty information
- **Cultural Route Visualizations:** Animated travel routes connecting locations based on themes (Buddhist Trail, Mughal Architecture, Temple Route)
- **Modern UI/UX:** Smooth animations, transitions, and an intuitive interface for seamless exploration
- **API Integration:** Backend connectivity to fetch detailed location data

## Project Structure

```
cupe-kg-frontend/
├── public/
│   ├── index.html
│   ├── favicon.ico
│   └── assets/
│       ├── markers/
│       └── images/
├── src/
│   ├── App.js
│   ├── index.js
│   ├── components/
│   │   ├── Map/
│   │   ├── LocationMarker/
│   │   ├── RouteVisualizer/
│   │   ├── InfoPanel/
│   │   ├── Timeline/
│   │   └── Header/
│   ├── services/
│   │   └── api.js
│   ├── context/
│   │   └── MapContext.js
│   ├── data/
│   │   ├── placeholderData.js
│   │   └── routes.js
│   ├── styles/
│   │   ├── variables.css
│   │   └── animations.css
│   └── utils/
│       └── mapUtils.js
└── package.json
```

## Technology Stack

- **Frontend Framework:** React.js
- **Map Library:** Leaflet.js
- **State Management:** React Context API
- **HTTP Client:** Fetch API
- **Styling:** CSS with custom animations and transitions
- **API Integration:** RESTful API endpoints

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cupe-kg-frontend.git
   cd cupe-kg-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Start the development server:
   ```bash
   npm start
   # or
   yarn start
   ```

4. Open [http://localhost:3000](http://localhost:3000) to view the application in your browser.

## API Integration

The frontend is designed to connect with a Flask/Django backend via these endpoints:

- `/api/place-info?name={placeName}` - Get detailed information about a specific place
- `/api/routes` - Get all available cultural routes
- `/api/locations` - Get all tourist locations
- `/api/search?q={query}` - Search for locations by keywords
- `/api/perspective?place={placeName}&type={perspectiveType}` - Get cultural perspective data

## Location Data Structure

Each location contains the following information:

```javascript
{
  id: 'location-id',
  name: 'Location Name',
  description: 'Brief description',
  history: 'Detailed history text...',
  period: 'Time period (e.g., 1336 CE - 1646 CE)',
  dynasty: 'Associated dynasty/empire',
  culturalFacts: [
    'Cultural fact 1',
    'Cultural fact 2',
    // ...
  ],
  legends: [
    {
      title: 'Legend Title',
      description: 'Legend description text...'
    },
    // ...
  ],
  tags: ['Tag1', 'Tag2', 'Tag3']
}
```

## Route Data Structure

Each route is defined as:

```javascript
{
  id: 'route-id',
  name: 'Route Name',
  description: 'Route description',
  color: '#HexColor',
  path: [
    [lat1, lng1],
    [lat2, lng2],
    // ...
  ],
  locations: [
    {
      name: 'Location Name',
      coordinates: [lat, lng],
      description: 'Brief description'
    },
    // ...
  ]
}
```

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/my-new-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project was created as part of a college assignment
- Map data provided by OpenStreetMap
- Cultural and historical information sourced from various public domain resources