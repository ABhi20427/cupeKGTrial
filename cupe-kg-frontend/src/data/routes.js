/**
 * Routes data for CuPe-KG tourism application
 * Defines cultural and historical routes across India
 */

export const routes = [
  {
    id: 'buddhist',
    name: 'Buddhist Trail',
    description: 'Follow the footsteps of Buddha and explore key sites of Buddhist heritage',
    color: '#FF5722',
    // Path is defined as array of [lat, lng] coordinates
    path: [
      [28.7041, 77.1025], // Delhi
      [27.5006, 77.6714], // Mathura
      [25.3176, 82.9739], // Varanasi
      [24.6959, 84.9920], // Bodh Gaya
      [25.2048, 85.8910], // Nalanda
      [25.5941, 85.1376], // Patna (Pataliputra)
      [24.1913, 88.2683]  // Rajgir
    ],
    locations: [
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Starting point with Buddhist monuments like Ashokan pillars'
      },
      { 
        name: 'Bodh Gaya', 
        coordinates: [24.6959, 84.9920],
        description: 'Where Buddha attained enlightenment under the Bodhi Tree'
      },
      { 
        name: 'Nalanda', 
        coordinates: [25.2048, 85.8910],
        description: 'Ancient Buddhist university and center of learning'
      }
    ]
  },
  {
    id: 'mughal',
    name: 'Mughal Architecture',
    description: 'Discover the grandeur of Mughal architectural marvels across Northern India',
    color: '#4CAF50',
    dashArray: '5, 10',
    path: [
      [28.7041, 77.1025], // Delhi
      [27.1767, 78.0081], // Agra
      [26.9124, 75.7873], // Jaipur
      [26.2124, 78.1772], // Gwalior
      [25.3176, 82.9739], // Varanasi
      [26.8467, 80.9462]  // Lucknow
    ],
    locations: [
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Home to Red Fort, Jama Masjid, and Humayun\'s Tomb'
      },
      { 
        name: 'Agra', 
        coordinates: [27.1767, 78.0081],
        description: 'Location of the iconic Taj Mahal and Agra Fort'
      },
      { 
        name: 'Fatehpur Sikri', 
        coordinates: [27.0940, 77.6700],
        description: 'Abandoned Mughal capital city with well-preserved architecture'
      }
    ]
  },
  {
    id: 'temple',
    name: 'Temple Route',
    description: 'Experience the rich diversity of ancient temple architecture and spirituality',
    color: '#9C27B0',
    path: [
      [19.8876, 86.0945], // Konark
      [19.8135, 85.8312], // Puri
      [20.2399, 85.8320], // Bhubaneswar
      [15.3350, 76.4600], // Hampi
      [13.0827, 75.2579], // Belur
      [10.9435, 79.8380], // Thanjavur
      [9.9195, 78.1193]   // Madurai
    ],
    locations: [
      { 
        name: 'Konark', 
        coordinates: [19.8876, 86.0945],
        description: 'Famous for the Sun Temple, an architectural marvel'
      },
      { 
        name: 'Hampi', 
        coordinates: [15.3350, 76.4600],
        description: 'Ruins of Vijayanagara with numerous temples'
      },
      { 
        name: 'Madurai', 
        coordinates: [9.9195, 78.1193],
        description: 'Home to the magnificent Meenakshi Amman Temple'
      }
    ]
  }
];