# services/data_loader.py
import json
import os
from models.location import Location
from models.route import Route, RouteLocation

class DataLoader:
    @staticmethod
    def load_placeholder_locations():
        """Load the placeholder location data used in the frontend"""
        locations = {}
        
        # Hampi
        hampi = Location(
            id="hampi",
            name="Hampi",
            description="Ancient city in Karnataka that was once the capital of the Vijayanagara Empire",
            coordinates={"lat": 15.3350, "lng": 76.4600},
            category="historical",
            history="Hampi was the capital of the Vijayanagara Empire in the 14th century and one of the richest and largest cities in the world during its prime. The architectural ruins at Hampi represent an excellent example of Hindu urban architecture and engineering. The city was sacked by invading Deccan Sultanate armies in 1565, after which it fell into ruin and was largely abandoned.",
            period="1336 CE - 1646 CE",
            dynasty="Vijayanagara Empire",
            cultural_facts=[
                "Hampi is a UNESCO World Heritage Site known for its stunning ruins and boulder-strewn landscape.",
                "The Virupaksha Temple in Hampi continues to be an active place of worship, with rituals dating back to the 7th century CE.",
                "The city's architectural style combines elements from various South Indian dynasties, including Chalukyas, Hoysalas, and Kakatiyas.",
                "The famous stone chariot at the Vittala Temple is carved from a single block of granite and features musical pillars that produce different musical notes when tapped.",
                "Annual Hampi Utsav (festival) celebrates the rich cultural heritage with music, dance, and cultural performances."
            ],
            legends=[
                {
                    "title": "The Story of Pampa and Shiva",
                    "description": "According to Hindu mythology, Pampa (the old name for the Tungabhadra River) was the daughter of Brahma who performed penance to marry Lord Shiva. Impressed by her devotion, Shiva agreed to marry her, and their union is believed to have taken place in Hampi. This is why the region was historically called 'Pampa-kshetra' (Pampa's place)."
                },
                {
                    "title": "Kishkindha Kingdom",
                    "description": "Hampi is believed to be the ancient Kishkindha, the monkey kingdom mentioned in the Hindu epic Ramayana. According to the epic, Lord Rama and his brother Lakshmana met Hanuman here while searching for Sita. Numerous hills and caves in the region are associated with tales from the Ramayana."
                }
            ],
            tags=["UNESCO Heritage", "Architecture", "Hindu", "Historical Kingdom", "Ruins"]
        )
        locations["hampi"] = hampi
        
        # Delhi
        delhi = Location(
            id="delhi",
            name="Delhi",
            description="Historic capital city that showcases India's rich cultural and architectural heritage",
            coordinates={"lat": 28.7041, "lng": 77.1025},
            category="cultural",
            history="Delhi has been continuously inhabited since the 6th century BCE and has served as the capital of various empires throughout Indian history. It has been built, destroyed, and rebuilt many times. From the Delhi Sultanate to the Mughal Empire and later the British colonial period, each ruler left their architectural and cultural mark on the city. Modern Delhi became the capital of independent India in 1947.",
            period="6th century BCE - Present",
            dynasty="Multiple (Delhi Sultanate, Mughal Empire, British Raj, etc.)",
            cultural_facts=[
                "Delhi has been the capital of at least seven different empires throughout history, earning it the nickname \"City of Cities.\"",
                "The city hosts three UNESCO World Heritage sites: Qutub Minar, Red Fort, and Humayun's Tomb.",
                "Delhi's cuisine reflects its multicultural heritage, with Mughlai food, Punjabi delicacies, and street food like chaat and kebabs.",
                "The city is divided into Old Delhi (historic center with narrow lanes and heritage sites) and New Delhi (the planned capital built during British rule).",
                "Delhi's culture blends Persian, Turkish, Arabic, and indigenous Indian traditions due to centuries of diverse rule."
            ],
            legends=[
                {
                    "title": "The Legend of Prithviraj Chauhan",
                    "description": "The last Hindu king to rule Delhi, Prithviraj Chauhan, is celebrated in folklore and epic poems. Legend says that even after being blinded and captured by Muhammad Ghori, he could shoot an arrow guided only by sound. He killed Ghori in an archery contest before being executed himself."
                },
                {
                    "title": "The Curse of Djinns at Feroz Shah Kotla",
                    "description": "The ruins of Feroz Shah Kotla fort are believed to be inhabited by djinns (supernatural beings in Islamic mythology). People still visit every Thursday to light candles and write letters to the djinns, asking for wishes to be fulfilled and problems to be solved."
                }
            ],
            tags=["Capital City", "Mughal Architecture", "Colonial Heritage", "UNESCO Sites", "Multicultural"]
        )
        locations["delhi"] = delhi
        
        # Konark
        konark = Location(
            id="konark",
            name="Konark",
            description="Home to the magnificent Sun Temple, a masterpiece of Kalinga architecture",
            coordinates={"lat": 19.8876, "lng": 86.0945},
            category="religious",
            history="Konark is famous for its 13th-century Sun Temple, built by King Narasimhadeva I of the Eastern Ganga Dynasty. The temple was designed in the form of a colossal chariot with twelve pairs of elaborately carved wheels, pulled by seven horses. Though partly in ruins today, it remains a testament to the architectural brilliance and artistic mastery of ancient Odisha. The temple was once used as an important navigational landmark by European sailors, who referred to it as the \"Black Pagoda.\"",
            period="1238 CE - 1250 CE",
            dynasty="Eastern Ganga Dynasty",
            cultural_facts=[
                "The Konark Sun Temple is a UNESCO World Heritage Site renowned for its architectural grandeur and precision.",
                "The temple's twelve pairs of wheels function as sundials that can accurately tell the time through their shadow positions.",
                "The walls are adorned with intricate carvings depicting daily life, mythological narratives, and famously, erotic sculptures inspired by the Kama Sutra.",
                "The annual Konark Dance Festival celebrates classical Indian dance forms against the backdrop of the illuminated temple.",
                "The name \"Konark\" derives from the Sanskrit words \"Kona\" (corner) and \"Arka\" (sun), as the temple is dedicated to the sun god Surya."
            ],
            legends=[
                {
                    "title": "The Magnetic Dome",
                    "description": "Legend says that the temple originally had a massive magnetic dome that caused ships passing through the Bay of Bengal to be drawn toward the shore, disrupting their navigation systems. European sailors reportedly removed the dome to protect their shipping routes."
                },
                {
                    "title": "The Architect's Sacrifice",
                    "description": "According to local folklore, the chief architect of the temple, Bisu Maharana, faced a deadly challenge. The king had demanded the temple be completed in twelve years. When it appeared the deadline would be missed, Bisu's twelve-year-old son, Dharmapada, arrived and miraculously completed the unfinished work overnight. When the architects discovered this, the boy jumped into the sea to save his father and colleagues from the king's wrath, sacrificing himself."
                }
            ],
            tags=["Sun Temple", "UNESCO Heritage", "Sculpture", "Ancient Architecture", "Hindu"]
        )
        locations["konark"] = konark
        
        return locations
    
    @staticmethod
    def load_placeholder_routes():
        """Load the placeholder route data used in the frontend"""
        routes = []
        
        # Buddhist Trail
        buddhist_trail = Route(
            id="buddhist",
            name="Buddhist Trail",
            description="Follow the footsteps of Buddha and explore key sites of Buddhist heritage",
            color="#FF5722",
            path=[
                [28.7041, 77.1025],  # Delhi
                [27.5006, 77.6714],  # Mathura
                [25.3176, 82.9739],  # Varanasi
                [24.6959, 84.9920],  # Bodh Gaya
                [25.2048, 85.8910],  # Nalanda
                [25.5941, 85.1376],  # Patna (Pataliputra)
                [24.1913, 88.2683]   # Rajgir
            ],
            locations=[
                RouteLocation(
                    name="Delhi",
                    coordinates=[28.7041, 77.1025],
                    description="Starting point with Buddhist monuments like Ashokan pillars"
                ),
                RouteLocation(
                    name="Bodh Gaya",
                    coordinates=[24.6959, 84.9920],
                    description="Where Buddha attained enlightenment under the Bodhi Tree"
                ),
                RouteLocation(
                    name="Nalanda",
                    coordinates=[25.2048, 85.8910],
                    description="Ancient Buddhist university and center of learning"
                )
            ]
        )
        routes.append(buddhist_trail)
        
        # Mughal Architecture route
        mughal_route = Route(
            id="mughal",
            name="Mughal Architecture",
            description="Discover the grandeur of Mughal architectural marvels across Northern India",
            color="#4CAF50",
            dash_array="5, 10",
            path=[
                [28.7041, 77.1025],  # Delhi
                [27.1767, 78.0081],  # Agra
                [26.9124, 75.7873],  # Jaipur
                [26.2124, 78.1772],  # Gwalior
                [25.3176, 82.9739],  # Varanasi
                [26.8467, 80.9462]   # Lucknow
            ],
            locations=[
                RouteLocation(
                    name="Delhi",
                    coordinates=[28.7041, 77.1025],
                    description="Home to Red Fort, Jama Masjid, and Humayun's Tomb"
                ),
                RouteLocation(
                    name="Agra",
                    coordinates=[27.1767, 78.0081],
                    description="Location of the iconic Taj Mahal and Agra Fort"
                ),
                RouteLocation(
                    name="Fatehpur Sikri",
                    coordinates=[27.0940, 77.6700],
                    description="Abandoned Mughal capital city with well-preserved architecture"
                )
            ]
        )
        routes.append(mughal_route)
        
        # Temple Route
        temple_route = Route(
            id="temple",
            name="Temple Route",
            description="Experience the rich diversity of ancient temple architecture and spirituality",
            color="#9C27B0",
            path=[
                [19.8876, 86.0945],  # Konark
                [19.8135, 85.8312],  # Puri
                [20.2399, 85.8320],  # Bhubaneswar
                [15.3350, 76.4600],  # Hampi
                [13.0827, 75.2579],  # Belur
                [10.9435, 79.8380],  # Thanjavur
                [9.9195, 78.1193]    # Madurai
            ],
            locations=[
                RouteLocation(
                    name="Konark",
                    coordinates=[19.8876, 86.0945],
                    description="Famous for the Sun Temple, an architectural marvel"
                ),
                RouteLocation(
                    name="Hampi",
                    coordinates=[15.3350, 76.4600],
                    description="Ruins of Vijayanagara with numerous temples"
                ),
                RouteLocation(
                    name="Madurai",
                    coordinates=[9.9195, 78.1193],
                    description="Home to the magnificent Meenakshi Amman Temple"
                )
            ]
        )
        routes.append(temple_route)
        
        return routes