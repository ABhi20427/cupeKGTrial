export const routes = [
  // ENHANCED EXISTING ROUTE 1 - Buddhist Trail (now with actual markers)
  {
    id: 'buddhist',
    name: 'Buddhist Trail',
    description: 'Follow the footsteps of Buddha and explore key sites of Buddhist heritage',
    color: '#FF5722',
    path: [
      [28.7041, 77.1025], // Delhi
      [25.3176, 82.9739], // Varanasi
      [24.6959, 84.9920], // Bodh Gaya (now has marker data)
      [25.2048, 85.8910], // Nalanda
      [20.5523, 75.7033], // Ajanta Caves (now connected)
    ],
    locations: [
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Starting point with Buddhist monuments like Ashokan pillars'
      },
      { 
        name: 'Varanasi', 
        coordinates: [25.3176, 82.9739],
        description: 'Ancient spiritual city where Buddha gave his first sermon'
      },
      { 
        name: 'Bodh Gaya', 
        coordinates: [24.6959, 84.9920],
        description: 'Sacred site where Buddha attained enlightenment under the Bodhi Tree'
      },
      { 
        name: 'Ajanta Caves', 
        coordinates: [20.5523, 75.7033],
        description: 'Buddhist cave monuments with ancient paintings and sculptures'
      }
    ]
  },

  // ENHANCED EXISTING ROUTE 2 - Mughal Architecture (now with Jaipur marker)
  {
    id: 'mughal',
    name: 'Mughal Architecture',
    description: 'Discover the grandeur of Mughal architectural marvels across Northern India',
    color: '#4CAF50',
    dashArray: '5, 10',
    path: [
      [28.7041, 77.1025], // Delhi
      [27.1751, 78.0421], // Taj Mahal (Agra)
      [26.9124, 75.7873], // Jaipur (now has marker data)
      [25.3176, 82.9739], // Varanasi
    ],
    locations: [
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Home to Red Fort, Jama Masjid, and Humayun\'s Tomb'
      },
      { 
        name: 'Taj Mahal', 
        coordinates: [27.1751, 78.0421],
        description: 'Location of the iconic Taj Mahal and Agra Fort'
      },
      { 
        name: 'Jaipur', 
        coordinates: [26.9124, 75.7873],
        description: 'The Pink City with Hawa Mahal and City Palace'
      },
      { 
        name: 'Varanasi', 
        coordinates: [25.3176, 82.9739],
        description: 'Ancient city with Mughal influence and Ganga Aarti'
      }
    ]
  },

  // ENHANCED EXISTING ROUTE 3 - Temple Route (now with Madurai marker)
  {
    id: 'temple',
    name: 'Temple Route',
    description: 'Experience the rich diversity of ancient temple architecture and spirituality',
    color: '#9C27B0',
    path: [
      [19.8876, 86.0945], // Konark
      [20.0258, 75.1790], // Ellora Caves
      [20.5523, 75.7033], // Ajanta Caves
      [24.8318, 79.9199], // Khajuraho
      [15.3350, 76.4600], // Hampi
      [9.9252, 78.1198],  // Madurai (now has marker data)
    ],
    locations: [
      { 
        name: 'Konark', 
        coordinates: [19.8876, 86.0945],
        description: 'Famous Sun Temple designed as a massive chariot'
      },
      { 
        name: 'Ellora Caves', 
        coordinates: [20.0258, 75.1790],
        description: 'Multi-religious rock-cut temples including Kailasa Temple'
      },
      { 
        name: 'Khajuraho', 
        coordinates: [24.8318, 79.9199],
        description: 'Medieval temples with intricate sculptures'
      },
      { 
        name: 'Hampi', 
        coordinates: [15.3350, 76.4600],
        description: 'Ruins of Vijayanagara with numerous temples'
      },
      { 
        name: 'Madurai', 
        coordinates: [9.9252, 78.1198],
        description: 'Home to the magnificent Meenakshi Amman Temple'
      }
    ]
  },

  // NEW ROUTE 4 - Rajasthan Royal Route
  {
    id: 'rajasthan-royal',
    name: 'Rajasthan Royal Route',
    description: 'Explore the majestic palaces, forts, and royal heritage of Rajasthan',
    color: '#E91E63',
    path: [
      [28.7041, 77.1025], // Delhi (starting point)
      [26.9124, 75.7873], // Jaipur
      [24.5854, 73.7125], // Udaipur
    ],
    locations: [
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Gateway to Rajasthan with Red Fort and India Gate'
      },
      { 
        name: 'Jaipur', 
        coordinates: [26.9124, 75.7873],
        description: 'The Pink City with Hawa Mahal and Amber Fort'
      },
      { 
        name: 'Udaipur', 
        coordinates: [24.5854, 73.7125],
        description: 'City of Lakes with romantic palaces and stunning views'
      }
    ]
  },

  // NEW ROUTE 5 - Spiritual Confluence Route
  {
    id: 'spiritual-confluence',
    name: 'Spiritual Confluence',
    description: 'Journey through India\'s diverse spiritual traditions and sacred sites',
    color: '#FF9800',
    dashArray: '10, 5',
    path: [
      [31.6340, 74.8723], // Amritsar (Sikhism)
      [28.7041, 77.1025], // Delhi
      [25.3176, 82.9739], // Varanasi (Hinduism)
      [24.6959, 84.9920], // Bodh Gaya (Buddhism)
      [20.5523, 75.7033], // Ajanta Caves (Buddhism)
    ],
    locations: [
      { 
        name: 'Amritsar', 
        coordinates: [31.6340, 74.8723],
        description: 'Golden Temple - holiest shrine of Sikhism'
      },
      { 
        name: 'Delhi', 
        coordinates: [28.7041, 77.1025],
        description: 'Multi-religious heritage with Jama Masjid and temples'
      },
      { 
        name: 'Varanasi', 
        coordinates: [25.3176, 82.9739],
        description: 'Spiritual capital of Hinduism on the banks of Ganges'
      },
      { 
        name: 'Bodh Gaya', 
        coordinates: [24.6959, 84.9920],
        description: 'Where Buddha attained enlightenment'
      },
      { 
        name: 'Ajanta Caves', 
        coordinates: [20.5523, 75.7033],
        description: 'Ancient Buddhist monasteries and art'
      }
    ]
  },

  // NEW ROUTE 6 - Heritage Coast Route
  {
    id: 'heritage-coast',
    name: 'Heritage Coast',
    description: 'Discover India\'s coastal heritage and maritime history',
    color: '#00BCD4',
    path: [
      [19.8876, 86.0945], // Konark (eastern coast)
      [12.6269, 80.1927], // Mahabalipuram (southern coast)
    ],
    locations: [
      { 
        name: 'Konark', 
        coordinates: [19.8876, 86.0945],
        description: 'Sun Temple on the eastern coast of India'
      },
      { 
        name: 'Mahabalipuram', 
        coordinates: [12.6269, 80.1927],
        description: 'Ancient port city with stone temples by the sea'
      }
    ]
  },
  // Add these new routes to your routes array in routes.js

  {
    id: 'karnataka-heritage',
    name: 'Karnataka Heritage Circuit',
    description: 'Explore the rich architectural heritage of Karnataka from Vijayanagara to Hoysala dynasties',
    color: '#8BC34A',
    path: [
      [15.3350, 76.4600], // Hampi
      [12.3051, 76.6551], // Mysore Palace  
      [13.1624, 75.8648], // Belur-Halebidu
    ],
    locations: [
      { 
        name: 'Hampi', 
        coordinates: [15.3350, 76.4600],
        description: 'Ruins of the magnificent Vijayanagara Empire'
      },
      { 
        name: 'Mysore Palace', 
        coordinates: [12.3051, 76.6551],
        description: 'Indo-Saracenic palace of the Wodeyar dynasty'
      },
      { 
        name: 'Belur and Halebidu', 
        coordinates: [13.1624, 75.8648],
        description: 'Masterpieces of Hoysala temple architecture'
      }
    ]
  },

  // NEW ROUTE - Spiritual Himalayan Trail  
  {
    id: 'spiritual-himalayan',
    name: 'Spiritual Himalayan Trail',
    description: 'Journey through sacred sites from the Ganges plains to Himalayan foothills',
    color: '#00BCD4',
    path: [
      [25.3176, 82.9739], // Varanasi
      [30.0869, 78.2676], // Rishikesh
      [24.6959, 84.9920], // Bodh Gaya
    ],
    locations: [
      { 
        name: 'Varanasi', 
        coordinates: [25.3176, 82.9739],
        description: 'Ancient spiritual capital on the banks of Ganges'
      },
      { 
        name: 'Rishikesh', 
        coordinates: [30.0869, 78.2676],
        description: 'Yoga capital of the world in Himalayan foothills'
      },
      { 
        name: 'Bodh Gaya', 
        coordinates: [24.6959, 84.9920],
        description: 'Sacred site of Buddha\'s enlightenment'
      }
    ]
  },

  // ENHANCED ROUTE - Complete Buddhist Heritage Circuit
  {
    id: 'complete-buddhist',
    name: 'Complete Buddhist Heritage Circuit', 
    description: 'Comprehensive journey through India\'s most significant Buddhist sites',
    color: '#FF9800',
    path: [
      [24.6959, 84.9920], // Bodh Gaya
      [23.4795, 77.7395], // Sanchi Stupa
      [20.5523, 75.7033], // Ajanta Caves
      [20.0258, 75.1790], // Ellora Caves
    ],
    locations: [
      { 
        name: 'Bodh Gaya', 
        coordinates: [24.6959, 84.9920],
        description: 'Where Buddha attained enlightenment'
      },
      { 
        name: 'Sanchi Stupa', 
        coordinates: [23.4795, 77.7395],
        description: 'Oldest Buddhist monuments built by Emperor Ashoka'
      },
      { 
        name: 'Ajanta Caves', 
        coordinates: [20.5523, 75.7033],
        description: 'Ancient Buddhist cave paintings and sculptures'
      },
      { 
        name: 'Ellora Caves', 
        coordinates: [20.0258, 75.1790],
        description: 'Multi-religious rock-cut temples including Buddhist caves'
      }
    ]
  }
  ];