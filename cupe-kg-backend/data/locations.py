# data/locations.py

def get_expanded_locations():
    """Return an expanded set of historical locations in India"""
    return [
        {
            "id": "taj-mahal",
            "name": "Taj Mahal",
            "description": "An ivory-white marble mausoleum on the south bank of the Yamuna river",
            "coordinates": {"lat": 27.1751, "lng": 78.0421},
            "category": "cultural",
            "history": "The Taj Mahal was commissioned in 1632 by the Mughal emperor Shah Jahan to house the tomb of his favorite wife, Mumtaz Mahal. Construction was completed in 1643, employing thousands of artisans and craftsmen. The Taj Mahal exemplifies the refinement of Mughal architecture, combining elements from Islamic, Persian, Ottoman Turkish and Indian architectural styles.",
            "period": "1632 CE - 1643 CE",
            
            "dynasty": "Mughal Empire",
            "culturalFacts": [
                "The Taj Mahal is considered one of the most perfect architectural monuments in the world.",
                "The main chamber houses the false sarcophagi of Mumtaz Mahal and Shah Jahan; the actual graves are at a lower level.",
                "The monument changes its color tones throughout the day, appearing pinkish in the morning, white in the evening, and golden in the moonlight.",
                "The four minarets surrounding the Taj Mahal were constructed slightly away from the main structure to protect it in case they collapsed.",
                "The Taj Mahal complex includes a mosque and a guest house, as well as ornamental gardens with reflecting pools."
            ],
            "legends": [
                {
                    "title": "The Black Taj Mahal",
                    "description": "Legend says Shah Jahan planned to build an identical mausoleum in black marble for himself on the opposite bank of the Yamuna river, connected by a bridge. This 'Black Taj' was never completed as he was imprisoned by his son Aurangzeb."
                },
                {
                    "title": "The Craftsmen's Hands",
                    "description": "According to local lore, Shah Jahan ordered the hands of the main craftsmen to be cut off after the Taj Mahal was completed so they could never build anything as magnificent again. However, historians consider this to be a myth without historical basis."
                }
            ],
            "tags": ["UNESCO Heritage", "Mausoleum", "Mughal", "Architecture", "Marble"]
        },
        {
            "id": "hampi",
            "name": "Hampi",
            "description": "Ancient city in Karnataka that was once the capital of the Vijayanagara Empire",
            "coordinates": {"lat": 15.3350, "lng": 76.4600},
            "category": "historical",
            "history": "Hampi was the capital of the Vijayanagara Empire in the 14th century and one of the richest and largest cities in the world during its prime. The architectural ruins at Hampi represent an excellent example of Hindu urban architecture and engineering. The city was sacked by invading Deccan Sultanate armies in 1565, after which it fell into ruin and was largely abandoned.",
            "period": "1336 CE - 1646 CE",
            "dynasty": "Vijayanagara Empire",
            "culturalFacts": [
                "Hampi is a UNESCO World Heritage Site known for its stunning ruins and boulder-strewn landscape.",
                "The Virupaksha Temple in Hampi continues to be an active place of worship, with rituals dating back to the 7th century CE.",
                "The city's architectural style combines elements from various South Indian dynasties, including Chalukyas, Hoysalas, and Kakatiyas.",
                "The famous stone chariot at the Vittala Temple is carved from a single block of granite and features musical pillars that produce different musical notes when tapped.",
                "Annual Hampi Utsav (festival) celebrates the rich cultural heritage with music, dance, and cultural performances."
            ],
            "legends": [
                {
                    "title": "The Story of Pampa and Shiva",
                    "description": "According to Hindu mythology, Pampa (the old name for the Tungabhadra River) was the daughter of Brahma who performed penance to marry Lord Shiva. Impressed by her devotion, Shiva agreed to marry her, and their union is believed to have taken place in Hampi. This is why the region was historically called 'Pampa-kshetra' (Pampa's place)."
                },
                {
                    "title": "Kishkindha Kingdom",
                    "description": "Hampi is believed to be the ancient Kishkindha, the monkey kingdom mentioned in the Hindu epic Ramayana. According to the epic, Lord Rama and his brother Lakshmana met Hanuman here while searching for Sita. Numerous hills and caves in the region are associated with tales from the Ramayana."
                }
            ],
            "tags": ["UNESCO Heritage", "Architecture", "Hindu", "Historical Kingdom", "Ruins"]
        },
        {
            "id": "khajuraho",
            "name": "Khajuraho Temples",
            "description": "Medieval Hindu and Jain temples famous for their nagara-style architectural symbolism and erotic sculptures",
            "coordinates": {"lat": 24.8318, "lng": 79.9199},
            "category": "religious",
            "history": "The Khajuraho temples were built between 950 and 1050 CE by the Chandela dynasty. Originally there were over 85 temples, but only about 25 have survived the ravages of time. After the decline of the Chandela empire, the temples were abandoned and reclaimed by the jungle until their rediscovery in the 1830s by British surveyor T.S. Burt.",
            "period": "950 CE - 1050 CE",
            "dynasty": "Chandela Dynasty",
            "culturalFacts": [
                "The temples are renowned for their intricate and often erotic sculptures that cover the exterior walls.",
                "The site is a UNESCO World Heritage Site and considered one of the 'seven wonders of India'.",
                "The temples represent a unique blend of architecture and sculpture, with some reaching heights of 35 meters.",
                "Despite common perceptions, only about 10% of the sculptures are erotic in nature; most depict everyday life and divine beings.",
                "The temples are divided into three geographical groups: Western, Eastern, and Southern."
            ],
            "legends": [
                {
                    "title": "Hemvati and the Moon God",
                    "description": "According to legend, Hemvati, daughter of a priest, was bathing in a pond when the Moon god was so enchanted by her beauty that he descended to earth in human form. From their union was born Chandravarman, founder of the Chandela dynasty. To absolve her son of the sin of illegitimate birth, Hemvati prayed to the gods, who instructed Chandravarman to build the temples with sculptures celebrating human passions without shame or guilt."
                },
                {
                    "title": "The Hidden Temples",
                    "description": "Local folklore claims that the temples were deliberately hidden deep in the forest to protect them from destruction during Islamic invasions. The dense jungle kept them concealed for centuries, preserving them from potential destruction."
                }
            ],
            "tags": ["UNESCO Heritage", "Hindu Temples", "Jain Temples", "Sculpture", "Medieval"]
        },
        {
            "id": "ajanta",
            "name": "Ajanta Caves",
            "description": "Buddhist cave monuments dating from the 2nd century BCE to about 480 CE",
            "coordinates": {"lat": 20.5523, "lng": 75.7033},
            "category": "religious",
            "history": "The Ajanta Caves constitute ancient monasteries and worship halls of different Buddhist traditions, carved into a 250-foot wall of rock. The caves were built in two phases, the first from the 2nd century BCE to the 1st century CE, and the second several centuries later. They were abandoned around 480 CE and forgotten until their accidental rediscovery in 1819 by a British officer during a tiger hunt.",
            "period": "2nd century BCE - 5th century CE",
            "dynasty": "Satavahana and Vakataka",
            "culturalFacts": [
                "The Ajanta Caves are a UNESCO World Heritage Site and contain some of the finest surviving examples of ancient Indian art.",
                "The caves include paintings and sculptures considered to be masterpieces of Buddhist religious art.",
                "The complex comprises 30 rock-cut cave monuments which are a mix of viharas (monasteries) and chaityas (worship halls).",
                "The paintings in the caves are executed on a ground of mud-plaster using the tempera technique.",
                "Themes of the paintings include the Jataka tales (stories of the Buddha's previous lives) and various Buddhist traditions."
            ],
            "legends": [
                {
                    "title": "The Hidden Buddha",
                    "description": "Local legend speaks of a hidden, unfinished cave that contains a massive Buddha statue that was abandoned when the caves were deserted. It is said that this cave has magical properties and only reveals itself to the truly enlightened."
                },
                {
                    "title": "The Eternal Flames",
                    "description": "According to folklore, ancient lamps in some of the deeper recesses of the caves were found still burning when they were rediscovered in the 19th century, despite being abandoned for over 1,000 years. While historically implausible, this legend speaks to the mysterious nature of the caves."
                }
            ],
            "tags": ["UNESCO Heritage", "Buddhist", "Cave Paintings", "Rock-Cut Architecture", "Ancient Art"]
        },
        {
            "id": "ellora",
            "name": "Ellora Caves",
            "description": "Rock-cut cave temples with monuments and artwork of Buddhism, Hinduism and Jainism from 600-1000 CE",
            "coordinates": {"lat": 20.0258, "lng": 75.1790},
            "category": "religious",
            "history": "The Ellora Caves are a complex of 34 rock-cut caves representing three different faiths: Buddhism, Hinduism, and Jainism. They were built between the 6th and 10th centuries CE under the patronage of various dynasties, particularly the Rashtrakuta rulers. The most remarkable of these is the Kailasa Temple (Cave 16), which is the largest monolithic structure in the world, carved from a single rock.",
            "period": "600 CE - 1000 CE",
            "dynasty": "Rashtrakuta Dynasty",
            "culturalFacts": [
                "The Ellora Caves demonstrate the religious harmony that existed in ancient India with Buddhist, Hindu, and Jain monuments side by side.",
                "The Kailasa Temple is twice the size of the Parthenon in Athens and took over 100 years to complete.",
                "The caves feature intricate sculptures and elaborate architectural details carved out of the volcanic basaltic rock.",
                "The site covers an area of 2 km and features over 100 caves, though only 34 are open to the public.",
                "The engineering techniques used to create these caves remain a subject of fascination for architects and historians."
            ],
            "legends": [
                {
                    "title": "The Divine Architect",
                    "description": "Legend has it that the architect of the Kailasa Temple, after being asked to complete this impossible task, first meditated for days and then had a divine vision of how to carve the temple from top to bottom, rather than the conventional bottom-up approach."
                },
                {
                    "title": "The Ten Avatars",
                    "description": "Local tradition claims that the ten avatars of Lord Vishnu carved in Cave 15 come to life on full moon nights and perform their cosmic duties, bringing blessings to those who witness this divine spectacle."
                }
            ],
            "tags": ["UNESCO Heritage", "Hindu Temples", "Buddhist Caves", "Jain Monuments", "Rock-Cut Architecture"]
        },
        {
            "id": "golden-temple",
            "name": "Golden Temple (Harmandir Sahib)",
            "description": "The holiest gurdwara and most important pilgrimage site of Sikhism",
            "coordinates": {"lat": 31.6200, "lng": 74.8765},
            "category": "religious",
            "history": "The Golden Temple was designed by Guru Arjan, the fifth Sikh Guru, and its foundation stone was laid by the Muslim Sufi saint Mian Mir in 1589. The temple was completed in 1604, and the Guru Granth Sahib, the Sikh holy book, was installed inside the same year. The temple was rebuilt several times after being destroyed by Afghan invaders. Its distinctive gold plating was added in the early 19th century by Maharaja Ranjit Singh.",
            "period": "1589 CE - 1604 CE (Original construction)",
            "dynasty": "Sikh Gurus (Later renovated under Sikh Empire)",
            "culturalFacts": [
                "The Golden Temple sits in the center of a sacred pool called the Amrit Sarovar (Pool of Nectar), which gives Amritsar its name.",
                "The temple has four entrances in four directions, symbolizing that people from all walks of life and all religions are welcome.",
                "The langar (community kitchen) at the Golden Temple serves free meals to up to 100,000 people every day, regardless of religion, caste, or background.",
                "The architecture blends Hindu and Islamic styles, representing the Sikh philosophy of unity and equality.",
                "The original copy of the Guru Granth Sahib is kept in the temple during the day and ceremonially returned to the Akal Takht at night."
            ],
            "legends": [
                {
                    "title": "The Healing Waters",
                    "description": "Legend says that the sacred pool surrounding the temple has healing properties, and many pilgrims take a dip in its waters believing it will cure their ailments and wash away their sins."
                },
                {
                    "title": "The Miracle of Light",
                    "description": "According to traditional accounts, when Maharaja Ranjit Singh donated the gold to cover the temple, a divine light was seen hovering over the shrine, confirming the sacred nature of this act of devotion."
                }
            ],
            "tags": ["Sikhism", "Gurdwara", "Golden Architecture", "Pilgrimage", "Religious Center"]
        },
        {
            "id": "goa-churches",
            "name": "Churches and Convents of Goa",
            "description": "A group of Catholic religious monuments built during Portuguese colonial rule",
            "coordinates": {"lat": 15.5005, "lng": 73.9154},
            "category": "religious",
            "history": "The churches and convents of Old Goa were built after the Portuguese conquest of Goa in 1510. The most significant construction began in the mid-16th century and continued until the 18th century. These monuments represent the evangelization of Asia and showcase the fusion of European architectural styles with local Indian traditions. After the decline of Old Goa in the 18th century due to epidemics, many of these structures fell into disrepair but were later restored.",
            "period": "16th century CE - 18th century CE",
            "dynasty": "Portuguese Colonial Rule",
            "culturalFacts": [
                "The Basilica of Bom Jesus, completed in 1605, houses the mortal remains of St. Francis Xavier, a revered missionary.",
                "The Sé Cathedral is the largest church in Asia and took 80 years to build.",
                "These monuments blend Portuguese Gothic, Renaissance, Baroque, and Mannerist styles with local Indian decorative elements.",
                "The Church of St. Francis of Assisi features an ornate gilded interior that exemplifies the wealth of Portuguese colonial art.",
                "Every ten years, the body of St. Francis Xavier is displayed for public veneration, attracting pilgrims from around the world."
            ],
            "legends": [
                {
                    "title": "The Incorrupt Saint",
                    "description": "Legend holds that the body of St. Francis Xavier has remained miraculously preserved for over 450 years without any embalming, considered a divine sign of his sainthood."
                },
                {
                    "title": "The Bell of Awakening",
                    "description": "Local lore claims that the Golden Bell that once hung in the Augustinian Church (now in ruins) could be heard throughout Goa, and had the power to ward off evil spirits and natural disasters."
                }
            ],
            "tags": ["UNESCO Heritage", "Colonial Architecture", "Catholic", "Portuguese", "Baroque"]
        },
        {
            "id": "qutub-minar",
            "name": "Qutub Minar",
            "description": "A 73-meter minaret built in the early 13th century and the tallest brick minaret in the world",
            "coordinates": {"lat": 28.5244, "lng": 77.1855},
            "category": "historical",
            "history": "The Qutub Minar was initiated by Qutub-ud-din Aibak, the first ruler of the Delhi Sultanate, around 1192 CE, but was completed by his successor, Iltutmish. Later, Firoz Shah Tughlaq and Sikandar Lodi also made additions to the structure. The tower was built as a victory monument and also as a minaret for the muezzin to call the faithful to prayer at the adjacent Quwwat-ul-Islam Mosque, the first mosque built in Delhi after the Islamic conquest.",
            "period": "1192 CE - 1220 CE (with later additions)",
            "dynasty": "Delhi Sultanate (Mamluk Dynasty)",
            "culturalFacts": [
                "The Qutub Minar features intricate carvings with verses from the Quran and elaborate geometric patterns.",
                "The minaret's construction used materials from 27 Hindu and Jain temples that were demolished by the Islamic invaders.",
                "The Iron Pillar in the Qutub complex has stood for over 1,600 years without rusting, demonstrating the advanced metallurgical skills of ancient Indian craftsmen.",
                "The tower has five distinct stories, each with a projecting balcony encircling the tower, and the lower three stories are made of red sandstone while the upper two are of marble and sandstone.",
                "The complex reflects the beginning of Indo-Islamic architecture, showcasing the fusion of Indian and Islamic styles."
            ],
            "legends": [
                {
                    "title": "The Wish-Fulfilling Pillar",
                    "description": "Legend says that if you can stand with your back to the Iron Pillar and encircle it with your arms, your wish will be granted. The pillar is believed to bring good fortune to those who can successfully perform this ritual."
                },
                {
                    "title": "The Unfinished Tower",
                    "description": "Local folklore suggests that the original plan was to build seven stories, but the construction was stopped at five because of an ominous astrological prediction related to the king's death once the tower was completed."
                }
            ],
            "tags": ["UNESCO Heritage", "Minaret", "Delhi Sultanate", "Islamic Architecture", "Medieval"]
        },
        {
            "id": "sanchi-stupa",
            "name": "Sanchi Stupa",
            "description": "One of the oldest stone structures in India and an important Buddhist monument",
            "coordinates": {"lat": 23.4794, "lng": 77.7375},
            "category": "religious",
            "history": "The Great Stupa at Sanchi was originally commissioned by Emperor Ashoka the Great in the 3rd century BCE to house the relics of Buddha. It was expanded in the 1st century BCE with the addition of four intricately carved gateways (toranas). Following the decline of Buddhism in India, the site was abandoned and fell into disrepair, only to be rediscovered in 1818 by a British officer. Major restoration work was undertaken in the 19th and early 20th centuries.",
            "period": "3rd century BCE (with later additions)",
            "dynasty": "Mauryan Empire (Later enhanced during Satavahana period)",
            "culturalFacts": [
                "The stupa's hemispherical dome represents the dome of heaven enclosing the earth.",
                "The four ornate gateways depict scenes from Buddha's life and previous incarnations (Jataka tales), created without actually showing Buddha in human form.",
                "The Ashoka Pillar at Sanchi, with its four lions (which became India's national emblem), is a prime example of Mauryan art.",
                "The monument showcases the transition from wooden to stone architecture in ancient India.",
                "The carvings on the toranas represent one of the finest examples of early Buddhist art and narrative sculpture."
            ],
            "legends": [
                {
                    "title": "The Buddha's Relics",
                    "description": "According to tradition, Emperor Ashoka distributed Buddha's relics among 84,000 stupas that he had built across his empire. The Sanchi Stupa is believed to contain a portion of these sacred relics."
                },
                {
                    "title": "The Guardian Spirits",
                    "description": "Local folklore suggests that the site is protected by guardian spirits who appear to sincere devotees in times of danger. During the full moon nights, it is said that these spirits circumambulate the stupa, blessing those who visit with pure intentions."
                }
            ],
            "tags": ["UNESCO Heritage", "Buddhist", "Stupa", "Ashoka", "Ancient Architecture"]
        },
        

        {
            "id": "jaipur",
            "name": "Jaipur",
            "description": "The Pink City, capital of Rajasthan known for its royal palaces and forts",
            "coordinates": {"lat": 26.9124, "lng": 75.7873},
            "category": "historical",
            "history": "Founded in 1727 by Maharaja Sawai Jai Singh II, Jaipur was one of the earliest planned cities of modern India. The city was painted pink in 1876 to welcome the Prince of Wales (later King Edward VII) and has maintained this distinctive color ever since. It represents the pinnacle of Rajput architecture and urban planning.",
            "period": "1727 CE - Present",
            "dynasty": "Kachwaha Rajputs",
            "culturalFacts": [
                "UNESCO World Heritage Site since 2019",
                "Part of India's Golden Triangle tourist circuit",
                "Home to Hawa Mahal (Palace of Winds) with 953 windows",
                "Features the world's largest stone sundial at Jantar Mantar",
                "Known for traditional crafts like blue pottery and jewelry"
            ],
            "legends": [
                {
                    "title": "The Pink City Legend",
                    "description": "Legend says the city was painted pink overnight by thousands of workers before the Prince of Wales' visit, as pink represents hospitality in Rajput culture. The color has been maintained by law ever since."
                }
            ],
            "tags": ["UNESCO Heritage", "Pink City", "Rajput", "Royal Architecture", "Golden Triangle"]
        },

        {
            "id": "bodh-gaya",
            "name": "Bodh Gaya",
            "description": "The holiest site in Buddhism where Prince Siddhartha attained enlightenment",
            "coordinates": {"lat": 24.6959, "lng": 84.9920},
            "category": "religious",
            "history": "Bodh Gaya is where Prince Siddhartha meditated under a Bodhi tree and attained enlightenment, becoming the Buddha around 528 BCE. The Mahabodhi Temple, built in the 5th-6th century CE, marks this sacred spot. The site has been a pilgrimage destination for Buddhists worldwide for over 2,500 years.",
            "period": "6th century BCE (enlightenment), 5th-6th century CE (temple)",
            "dynasty": "Various Buddhist kingdoms",
            "culturalFacts": [
                "UNESCO World Heritage Site since 2002",
                "The Bodhi Tree here is said to be a direct descendant of the original",
                "Features temples and monasteries from many Buddhist countries",
                "The Mahabodhi Temple is the oldest brick temple in India",
                "Attracts pilgrims from Tibet, Sri Lanka, Myanmar, Thailand, and Japan"
            ],
            "legends": [
                {
                    "title": "The Bodhi Tree Miracle",
                    "description": "Legend states that when the Buddha achieved enlightenment, the earth trembled, flowers rained from the sky, and the Bodhi tree's leaves shimmered with golden light."
                }
            ],
            "tags": ["UNESCO Heritage", "Buddhism", "Enlightenment", "Mahabodhi Temple", "Pilgrimage"]
        },

        {
            "id": "varanasi",
            "name": "Varanasi",
            "description": "One of the world's oldest living cities and holiest place in Hinduism",
            "coordinates": {"lat": 25.3176, "lng": 82.9739},
            "category": "religious",
            "history": "Varanasi, also known as Kashi or Benares, is one of the oldest continuously inhabited cities in the world, with settlements dating back to the 11th century BCE. It has been a major center of learning, spirituality, and culture for over 3,000 years. Mark Twain called it 'older than history, older than tradition, older even than legend.'",
            "period": "11th century BCE - Present",
            "dynasty": "Various Hindu kingdoms, Mughal Empire, British Raj",
            "culturalFacts": [
                "Over 80 ghats (stone steps) along the Ganges River",
                "Home to Banaras Hindu University, one of Asia's largest universities",
                "Famous for Banarasi silk sarees and classical music",
                "Over 2,000 temples in the city",
                "Birthplace of the tabla musical instrument"
            ],
            "legends": [
                {
                    "title": "The City of Shiva",
                    "description": "Hindu mythology states that Varanasi stands on the trident of Lord Shiva, making it the spiritual capital of Hinduism where dying here ensures liberation from the cycle of rebirth."
                }
            ],
            "tags": ["Ancient City", "Hinduism", "Ganges", "Spiritual Capital", "Classical Music"]
        },

        {
            "id": "madurai",
            "name": "Madurai",
            "description": "Ancient city famous for the magnificent Meenakshi Amman Temple",
            "coordinates": {"lat": 9.9252, "lng": 78.1198},
            "category": "religious",
            "history": "Madurai is one of Tamil Nadu's oldest cities, mentioned in ancient Tamil literature dating back to the 3rd century BCE. It was the capital of the Pandya Kingdom and later ruled by various dynasties. The city is famous for the Meenakshi Amman Temple, rebuilt in the 17th century during the Nayak period.",
            "period": "3rd century BCE - Present",
            "dynasty": "Pandya Kingdom, Nayak Dynasty",
            "culturalFacts": [
                "Known as the 'Temple City' and 'Athens of the East'",
                "The Meenakshi Temple has 14 gopurams (towers), the tallest being 52 meters",
                "Ancient center of Tamil literature and culture",
                "Famous for its night-blooming jasmine flowers",
                "Traditional center for classical dance and music"
            ],
            "legends": [
                {
                    "title": "The Fish-Eyed Goddess",
                    "description": "Legend tells of Princess Meenakshi, born with three breasts, who would lose the third when she met her future husband. She met Lord Shiva and became the presiding deity of the magnificent temple."
                }
            ],
            "tags": ["Temple City", "Dravidian Architecture", "Tamil Culture", "Meenakshi Temple", "Pandya Kingdom"]
        },

        {
            "id": "amritsar",
            "name": "Amritsar",
            "description": "Holy city of Sikhism, home to the Golden Temple",
            "coordinates": {"lat": 31.6340, "lng": 74.8723},
            "category": "religious",
            "history": "Amritsar was founded in 1577 by the fourth Sikh Guru, Ram Das. The Golden Temple (Harmandir Sahib) was built by the fifth Guru, Arjan Dev, in 1604. The city has been central to Sikh history and is the spiritual and cultural center of the Sikh community worldwide.",
            "period": "1577 CE - Present",
            "dynasty": "Sikh Gurus, Sikh Empire",
            "culturalFacts": [
                "The Golden Temple serves free meals to 100,000+ visitors daily",
                "The temple is surrounded by the sacred Amrit Sarovar (Pool of Nectar)",
                "Features the world's largest community kitchen (langar)",
                "The temple has four entrances, symbolizing openness to all religions",
                "Made famous globally through its inclusive philosophy"
            ],
            "legends": [
                {
                    "title": "The Pool of Immortality",
                    "description": "Legend states that the sacred pool around the Golden Temple has healing powers, and bathing in its waters can cure diseases and purify the soul."
                }
            ],
            "tags": ["Golden Temple", "Sikhism", "Community Kitchen", "Religious Harmony", "Sikh Heritage"]
        },
        # Add these to your locations array in locations.py

        {
            "id": "konark",
            "name": "Konark",
            "description": "Home to the magnificent Sun Temple, a masterpiece of Kalinga architecture",
            "coordinates": {"lat": 19.8876, "lng": 86.0945},
            "category": "religious",
            "history": "Konark is famous for its 13th-century Sun Temple, built by King Narasimhadeva I of the Eastern Ganga Dynasty. The temple was designed in the form of a colossal chariot with twelve pairs of elaborately carved wheels, pulled by seven horses. Though partly in ruins today, it remains a testament to the architectural brilliance and artistic mastery of ancient Odisha.",
            "period": "1238 CE - 1250 CE",
            "dynasty": "Eastern Ganga Dynasty",
            "culturalFacts": [
                "The Konark Sun Temple is a UNESCO World Heritage Site renowned for its architectural grandeur and precision.",
                "The temple's twelve pairs of wheels function as sundials that can accurately tell the time through their shadow positions.",
                "The intricate stone carvings depict various aspects of life, including erotic sculptures, mythological figures, and daily activities.",
                "The temple was once used as a navigational landmark by European sailors, who called it the 'Black Pagoda'.",
                "The main sanctum was once topped by a massive magnet that could suspend iron in mid-air."
            ],
            "legends": [
                {
                    "title": "The Architect's Sacrifice",
                    "description": "Legend tells of the chief architect's son who completed the temple by sacrificing his life, jumping from the top to save his father's honor when the construction faced impossible challenges."
                }
            ],
            "tags": ["Sun Temple", "UNESCO", "Kalinga architecture", "Eastern Ganga", "Surya", "religious"]
        },

        {
            "id": "udaipur", 
            "name": "Udaipur",
            "description": "The City of Lakes, known for its romantic palaces and stunning lake views",
            "coordinates": {"lat": 24.5854, "lng": 73.7125},
            "category": "historical",
            "history": "Founded in 1559 by Maharana Udai Singh II, Udaipur became the capital of the erstwhile kingdom of Mewar. Known as the 'Venice of the East', the city is famous for its artificial lakes, palaces, and romantic setting. The city palace complex overlooks Lake Pichola and is one of the largest palace complexes in the world.",
            "period": "1559 CE - Present",
            "dynasty": "Mewar Kingdom (Sisodia Rajputs)",
            "culturalFacts": [
                "Often called the 'Most Romantic City in India'",
                "Features interconnected lakes created by Maharana Udai Singh",
                "The City Palace is built on a hilltop and offers panoramic views",
                "Famous for miniature paintings and traditional Rajasthani crafts",
                "Popular filming location for many Bollywood movies"
            ],
            "legends": [
                {
                    "title": "The Sage's Blessing",
                    "description": "Legend says that a sage blessed Maharana Udai Singh, telling him to build his capital where he met the sage. This spot became Udaipur, and the blessing ensured the city would never face water scarcity despite being in a desert state."
                }
            ],
            "tags": ["City of Lakes", "Romantic", "Mewar", "Palaces", "Rajput Heritage"]
        },

        {
            "id": "mahabalipuram",
            "name": "Mahabalipuram", 
            "description": "Ancient port city famous for its stone temples and rock-cut sculptures",
            "coordinates": {"lat": 12.6269, "lng": 80.1927},
            "category": "historical",
            "history": "Mahabalipuram, also known as Mamallapuram, was a major port city of the Pallava kingdom during the 7th and 8th centuries CE. The town is famous for its stone temples and sculptures created during the reign of Narasimhavarman I. It served as an important center for art, culture, and maritime trade.",
            "period": "7th-8th century CE",
            "dynasty": "Pallava Dynasty",
            "culturalFacts": [
                "UNESCO World Heritage Site since 1984",
                "Famous for the Shore Temple, one of the oldest stone temples in South India",
                "Home to Arjuna's Penance, the world's largest bas-relief",
                "Features the Five Rathas (chariot-shaped temples) carved from single rocks",
                "Annual Mamallapuram Dance Festival showcases classical Indian dance"
            ],
            "legends": [
                {
                    "title": "The Seven Pagodas",
                    "description": "Local legend speaks of seven magnificent temples that once stood by the shore. Six were submerged by the sea due to their extraordinary beauty, which made the gods jealous. Only the Shore Temple remains visible."
                }
            ],
            "tags": ["UNESCO Heritage", "Shore Temple", "Pallava", "Rock-Cut Art", "Coastal Heritage"]
        },
        # Add these 4 new locations to your locations array in locations.py

{
    "id": "mysore-palace",
    "name": "Mysore Palace", 
    "description": "Magnificent Indo-Saracenic palace, seat of the Wodeyar dynasty and architectural marvel",
    "coordinates": {"lat": 12.3051, "lng": 76.6551},
    "category": "historical",
    "history": "The Mysore Palace is the official residence of the Wodeyars, the former royal family of Mysore. The current structure was built between 1897-1912 after the old palace was destroyed by fire. It represents the grandeur of the Kingdom of Mysore and showcases Indo-Saracenic architecture with Hindu, Muslim, Rajput, and Gothic styles blended together.",
    "period": "1912 CE (current structure, dynasty from 1399 CE)",
    "dynasty": "Kingdom of Mysore (Wodeyar Dynasty)",
    "cultural_facts": [
        "One of the largest palaces in India with Indo-Saracenic architecture",
        "Famous for its spectacular Dussehra celebrations and illumination with 97,000 light bulbs",
        "Houses a magnificent Durbar Hall with stained glass ceiling and golden throne",
        "The palace served as the seat of power for the Wodeyar dynasty for over 600 years",
        "Features a unique blend of Hindu, Islamic, Rajput, and Gothic architectural elements"
    ],
    "legends": [
        {
            "title": "The Golden Throne of Tipu Sultan",
            "description": "Legend says the famous golden throne (Chinnada Simhasana) was originally owned by Tipu Sultan and later acquired by the Wodeyars. It's displayed only during Dussehra celebrations, and local belief holds that the throne brings prosperity to the kingdom."
        },
        {
            "title": "The Curse of the Demon Mahishasura", 
            "description": "According to Hindu mythology, the city gets its name from the demon Mahishasura who was killed by Goddess Chamundeshwari on Chamundi Hill. The palace is said to be built on blessed land where good always triumphs over evil."
        }
    ],
    "tags": ["Royal Palace", "Indo-Saracenic", "Wodeyar Dynasty", "Dussehra", "Karnataka Heritage"]
},

{
    "id": "belur-halebidu",
    "name": "Belur and Halebidu",
    "description": "Twin temple complexes showcasing the pinnacle of Hoysala architecture and craftsmanship",
    "coordinates": {"lat": 13.1624, "lng": 75.8648}, # Belur coordinates (Halebidu is nearby)
    "category": "religious", 
    "history": "Belur and Halebidu were the sequential capitals of the Hoysala Empire during 10th-14th centuries. These temple complexes represent the zenith of Hoysala architecture. Belur's Chennakeshava Temple was built by King Vishnuvardhana in 1117 CE, while Halebidu's Hoysaleswara Temple was constructed during the reign of King Vishnuvardhana and his successors. The intricate stone carvings are considered among the finest examples of Indian temple architecture.",
    "period": "1117 CE - 1268 CE",
    "dynasty": "Hoysala Empire",
    "cultural_facts": [
        "Belur's Chennakeshava Temple took 103 years to complete and showcases unparalleled stone sculpture artistry",
        "Halebidu's Hoysaleswara Temple features over 240 wall sculptures and intricate friezes depicting Hindu mythology",
        "The temples are carved from chloritic schist (soapstone), allowing for extremely detailed sculptural work",
        "Features dancing figures of apsaras, musicians, and scenes from Hindu epics carved with jewel-like precision", 
        "UNESCO World Heritage Site candidate representing the height of South Indian temple architecture"
    ],
    "legends": [
        {
            "title": "The Dancing Queen Shantala",
            "description": "Queen Shantala Devi, wife of King Vishnuvardhana, was a renowned dancer. Legend says that many of the beautiful dancing figures carved on the temple walls are modeled after her graceful movements and expressions."
        },
        {
            "title": "The Unfinished Masterpiece",
            "description": "Local legend claims that the Halebidu temple was left intentionally unfinished because the sculptors feared that completing such divine beauty would invite the jealousy of the gods themselves."
        }
    ],
    "tags": ["Hoysala Architecture", "Temple Complex", "Stone Carving", "UNESCO Candidate", "Karnataka Heritage"]
},

{
    "id": "rishikesh",
    "name": "Rishikesh",
    "description": "The Yoga Capital of the World, sacred city on the banks of the Ganges in the Himalayan foothills", 
    "coordinates": {"lat": 30.0869, "lng": 78.2676},
    "category": "religious",
    "history": "Rishikesh is an ancient sacred city mentioned in Hindu scriptures including the Ramayana. It gained international fame in the 1960s when The Beatles stayed here to learn Transcendental Meditation. The city is dotted with numerous ashrams, temples, and yoga centers. It serves as the gateway to the Char Dham pilgrimage and is considered one of the holiest places in Hinduism for meditation and spiritual learning.",
    "period": "Ancient (mentioned in Ramayana) - Present",
    "dynasty": "Various Hindu Traditions and Spiritual Lineages",
    "cultural_facts": [
        "Known as the 'Yoga Capital of the World' with hundreds of yoga schools and ashrams",
        "The Beatles stayed at Maharishi Mahesh Yogi's ashram here in 1968, now called 'Beatles Ashram'",
        "Features iconic suspension bridges like Lakshman Jhula and Ram Jhula across the Ganges",
        "Home to the International Yoga Festival attracting practitioners from around the globe",
        "Gateway to the Char Dham pilgrimage (Kedarnath, Badrinath, Gangotri, Yamunotri)"
    ],
    "legends": [
        {
            "title": "Lakshman's Penance Bridge",
            "description": "Legend says that Lakshman, brother of Lord Rama, performed penance at this spot and crossed the river on a jute rope bridge. The famous Lakshman Jhula suspension bridge is built at this mythological crossing point."
        },
        {
            "title": "The Sage Raibhya's Meditation",
            "description": "According to ancient texts, the sage Raibhya performed severe austerities here, and Lord Vishnu appeared before him as 'Hrishikesh' (Lord of the Senses), giving the city its name."
        }
    ],
    "tags": ["Yoga Capital", "Spiritual Tourism", "Beatles Ashram", "Ganges", "Himalayan Heritage"]
},

{
    "id": "sanchi-stupa",
    "name": "Sanchi Stupa", 
    "description": "The oldest Buddhist monument in India and finest example of early Buddhist art and architecture",
    "coordinates": {"lat": 23.4795, "lng": 77.7395},
    "category": "religious",
    "history": "Sanchi is home to the oldest surviving Buddhist monuments in India, dating from the 3rd century BCE to the 12th century CE. The Great Stupa was originally commissioned by Emperor Ashoka in the 3rd century BCE and later enlarged. The site contains relics of Buddha's disciples and represents the evolution of Buddhist architecture over nearly 1,500 years. It's one of the most important Buddhist pilgrimage sites and a UNESCO World Heritage Site.",
    "period": "3rd century BCE - 12th century CE", 
    "dynasty": "Mauryan Empire (Emperor Ashoka) and later dynasties",
    "cultural_facts": [
        "The Great Stupa is one of the oldest stone structures in India and a UNESCO World Heritage Site",
        "Features four beautifully carved toranas (gateways) depicting Jataka tales and Buddha's life",
        "Contains relics of Buddha's chief disciples Sariputra and Maudgalyayana", 
        "Represents the purest form of early Buddhist architecture without any human representation of Buddha",
        "The site showcases the evolution of Buddhist art from symbolic representation to figurative sculpture"
    ],
    "legends": [
        {
            "title": "Ashoka's Divine Vision",
            "description": "Legend says Emperor Ashoka chose this site after having a divine vision where Buddha appeared and blessed this hill as a place where his teachings would be preserved for future generations."
        },
        {
            "title": "The Speaking Stupas",
            "description": "Local folklore believes that on full moon nights, the ancient stupas 'speak' to each other, sharing the wisdom of Buddha's teachings with anyone pure of heart who listens carefully."
        }
    ],
    "tags": ["Buddhist Heritage", "Emperor Ashoka", "UNESCO World Heritage", "Ancient Stupa", "Mauryan Architecture"]
},

{
    "id": "thanjavur",
    "name": "Thanjavur",
    "description": "Home to the magnificent Brihadeeswarar Temple and the historic Thanjavur Palace",
    "coordinates": {"lat": 10.7870, "lng": 79.1378},
    "category": "historical",
    "history": "Thanjavur served as the capital of the great Chola Empire from the 9th to 13th centuries. The city reached its zenith under Raja Raja Chola I, who built the magnificent Brihadeeswarar Temple in 1010 CE. Later, it became the capital of the Maratha kingdom of Thanjavur under the Bhonsle dynasty. The Thanjavur Palace complex was built by the Nayak and Maratha rulers.",
    "period": "9th century CE - Present",
    "dynasty": "Chola Empire, Nayak Dynasty, Maratha Kingdom",
    "culturalFacts": [
        "The Brihadeeswarar Temple is a UNESCO World Heritage Site and masterpiece of Dravidian architecture",
        "Known as the 'Rice Bowl of Tamil Nadu' due to its fertile agricultural lands",
        "Famous for Thanjavur paintings, a classical South Indian art form with rich colors and gold foil",
        "The temple's vimana (tower) is 216 feet tall and was the tallest structure in the world when built",
        "Thanjavur dolls (dancing dolls) are a unique craft tradition of the region"
    ],
    "legends": [
        {
            "title": "The Shadow-less Temple",
            "description": "Legend says that the Brihadeeswarar Temple's towering vimana is designed so perfectly that it casts no shadow on the ground at noon, demonstrating the architectural genius of ancient Tamil builders."
        },
        {
            "title": "The Flying Kite Stone",
            "description": "Local folklore tells that the 80-ton capstone on top of the temple was lifted using a massive earthen ramp and a giant kite, showcasing the ingenuity of Chola engineering."
        }
    ],
    "tags": ["Chola Empire", "Brihadeeswarar Temple", "UNESCO Heritage", "Dravidian Architecture", "Thanjavur Palace"]
},

{
    "id": "kanchipuram",
    "name": "Kanchipuram",
    "description": "A historic pilgrimage city famous for its ancient temples and silk sarees",
    "coordinates": {"lat": 12.8342, "lng": 79.7036},
    "category": "religious",
    "history": "Kanchipuram, known as the 'City of Thousand Temples', served as the capital of the Pallava dynasty from the 4th to 9th centuries CE. It was an important center of learning and pilgrimage, mentioned in ancient Tamil literature. The city houses numerous ancient temples dedicated to both Vishnu and Shiva, making it one of the seven sacred cities (Sapta Puri) in Hinduism.",
    "period": "4th century CE - Present",
    "dynasty": "Pallava Dynasty, Chola Empire, Vijayanagara Empire",
    "culturalFacts": [
        "One of the seven sacred cities (Sapta Puri) in Hinduism for attaining moksha",
        "Famous worldwide for Kanchipuram silk sarees, handwoven with pure mulberry silk",
        "The Ekambareswarar Temple has a 1000-year-old mango tree with four branches bearing different varieties of mangoes",
        "Kailasanathar Temple is one of the earliest structural temples in South India",
        "Former center of Buddhist learning with ancient monasteries and universities"
    ],
    "legends": [
        {
            "title": "The Four-Fruited Mango Tree",
            "description": "Legend says the ancient mango tree in Ekambareswarar Temple represents the four Vedas, with each branch bearing different varieties of mangoes, blessed by Goddess Parvati herself."
        },
        {
            "title": "The Golden City of Learning",
            "description": "Ancient texts describe Kanchipuram as a golden city where scholars from across India came to debate philosophy, and the city's temples served as universities for various branches of knowledge."
        }
    ],
    "tags": ["Pallava Dynasty", "Temple City", "Sapta Puri", "Silk Sarees", "Pilgrimage Center"]
},

{
    "id": "chidambaram",
    "name": "Chidambaram",
    "description": "A significant pilgrimage town famous for the Nataraja Temple and cosmic dance of Shiva",
    "coordinates": {"lat": 11.3988, "lng": 79.6947},
    "category": "religious",
    "history": "Chidambaram is an ancient temple town that has been a major pilgrimage center for over 2,000 years. The famous Nataraja Temple, dedicated to Lord Shiva as the cosmic dancer, was patronized by the Chola kings. The temple represents the cosmic dance of creation, preservation, and destruction. The town has been ruled by various dynasties including Pallavas, Cholas, and Vijayanagara Empire.",
    "period": "Ancient times - Present",
    "dynasty": "Pallava Dynasty, Chola Empire, Vijayanagara Empire",
    "culturalFacts": [
        "The Nataraja Temple is famous for its representation of Shiva's cosmic dance (Ananda Tandava)",
        "The temple's Chit Sabha (consciousness hall) represents the space element (akasha)",
        "Home to one of the Pancha Bhoota Sthalams representing the element of space/ether",
        "The temple has 21,600 gold tiles on its roof representing the number of breaths a human takes per day",
        "Center for classical Tamil poetry and Bharatanatyam dance traditions"
    ],
    "legends": [
        {
            "title": "The Cosmic Dance Hall",
            "description": "Legend states that Lord Shiva performs his eternal dance in the golden hall (Pon Ambalam) of Chidambaram, and those with divine vision can witness this cosmic performance that sustains the universe."
        },
        {
            "title": "The Secret of the Empty Space",
            "description": "The temple's inner sanctum contains empty space representing the formless nature of the divine, and it's said that true devotees can perceive the invisible dance of Nataraja in this sacred void."
        }
    ],
    "tags": ["Nataraja Temple", "Cosmic Dance", "Pancha Bhoota Sthalam", "Chola Patronage", "Spiritual Center"]
},

{
    "id": "thiruvannamalai",
    "name": "Thiruvannamalai",
    "description": "Sacred pilgrimage town known for the Arunachala Temple and spiritual significance",
    "coordinates": {"lat": 12.2253, "lng": 79.0747},
    "category": "religious",
    "history": "Thiruvannamalai is built around the sacred Arunachala Hill, considered to be a manifestation of Lord Shiva himself. The town has been a major pilgrimage center for centuries, with the Annamalaiyar Temple dating back to the 9th century. It gained further spiritual significance as the residence of sage Ramana Maharshi in the 20th century, attracting spiritual seekers from around the world.",
    "period": "9th century CE - Present",
    "dynasty": "Chola Empire, Vijayanagara Empire, Maratha Kingdom",
    "culturalFacts": [
        "The Arunachala Hill is considered one of the holiest mountains in South India",
        "Famous for the Karthigai Deepam festival when a huge fire is lit on the hill top",
        "Home to Ramana Maharshi's ashram, attracting spiritual seekers worldwide",
        "The Annamalaiyar Temple is one of the largest temples in Tamil Nadu",
        "Girivalam (circumambulation of the hill) is performed by thousands of devotees"
    ],
    "legends": [
        {
            "title": "The Fire Lingam of Arunachala",
            "description": "Legend says that when Brahma and Vishnu argued about their supremacy, Shiva appeared as an infinite column of fire. Arunachala Hill is believed to be the physical manifestation of this divine fire lingam."
        },
        {
            "title": "The Self-Manifested Temple",
            "description": "According to tradition, the Annamalaiyar Temple was not built by human hands but manifested spontaneously around the sacred hill, with each stone placed by divine will rather than human effort."
        }
    ],
    "tags": ["Arunachala Temple", "Sacred Hill", "Ramana Maharshi", "Karthigai Deepam", "Spiritual Tourism"]
},

{
    "id": "puri",
    "name": "Puri",
    "description": "Sacred coastal city famous for the Jagannath Temple and annual Rath Yatra festival",
    "coordinates": {"lat": 19.8135, "lng": 85.8312},
    "category": "religious",
    "history": "Puri is one of the four sacred dhams (pilgrimage sites) in Hinduism and home to the famous Jagannath Temple, built in the 12th century by King Anantavarman Chodaganga Deva of the Eastern Ganga Dynasty. The city has been a major pilgrimage center for centuries, with the annual Rath Yatra (chariot festival) attracting millions of devotees. The temple's unique tradition includes serving prasad (blessed food) to thousands daily.",
    "period": "12th century CE - Present",
    "dynasty": "Eastern Ganga Dynasty, Gajapati Dynasty",
    "culturalFacts": [
        "One of the Char Dham pilgrimage sites in Hinduism",
        "The Rath Yatra festival features three massive wooden chariots carrying the deities through the streets",
        "The Jagannath Temple serves Mahaprasad to over 100,000 pilgrims daily",
        "The temple flag atop the dome always flies in the opposite direction of the wind",
        "Puri beach is one of the most sacred beaches in Hinduism for performing last rites"
    ],
    "legends": [
        {
            "title": "The Incomplete Idols",
            "description": "Legend says that Lord Jagannath, his brother Balabhadra, and sister Subhadra were carved by divine architect Vishwakarma in secrecy. King Indradyumna opened the door prematurely, and the idols remained incomplete with no hands or legs, but the Lord blessed them to be worshipped in this form forever."
        },
        {
            "title": "The Sacred Kitchen Miracle",
            "description": "The temple kitchen is said to have a miraculous pot system where seven pots are stacked on a wood fire, but the top pot cooks first. Devotees believe this defies natural laws and is a divine blessing of Lord Jagannath."
        }
    ],
    "tags": ["Jagannath Temple", "Rath Yatra", "Char Dham", "Pilgrimage", "Odisha Heritage"]
},

{
    "id": "sundarbans",
    "name": "Sundarbans",
    "description": "Largest mangrove delta and UNESCO World Heritage Site, home to the Royal Bengal Tiger",
    "coordinates": {"lat": 21.9497, "lng": 89.1833},
    "category": "natural",
    "history": "The Sundarbans is the world's largest tidal mangrove forest, formed by the confluence of the Ganges, Brahmaputra, and Meghna rivers. The name 'Sundarbans' means 'beautiful forest' in Bengali. It has been inhabited for centuries with ancient references in Mughal records. The region was declared a UNESCO World Heritage Site in 1987 and is crucial for ecological balance and biodiversity.",
    "period": "Ancient times - Present",
    "dynasty": "Mughal Empire, British Colonial Rule, Modern India",
    "culturalFacts": [
        "UNESCO World Heritage Site and largest mangrove ecosystem in the world",
        "Home to approximately 400 Royal Bengal Tigers adapted to swim in saline water",
        "The region contains 102 islands with unique estuarine mangrove forests",
        "Important habitat for endangered species like Irrawaddy dolphins and saltwater crocodiles",
        "Local communities worship Bonbibi, the forest goddess who protects people from tigers"
    ],
    "legends": [
        {
            "title": "Bonbibi - The Forest Guardian",
            "description": "Local legend tells of Bonbibi, a forest goddess who protects honey collectors and woodcutters from tiger attacks. Both Hindus and Muslims worship her, making offerings before entering the forest for protection."
        },
        {
            "title": "Dakshin Ray - The Tiger Spirit",
            "description": "Folklore speaks of Dakshin Ray, a powerful spirit who appears as a tiger and rules the southern forests. He must be appeased with prayers and offerings, or he sends his tiger minions to punish those who disrespect the forest."
        }
    ],
    "tags": ["UNESCO Heritage", "Mangrove Forest", "Bengal Tiger", "Biodiversity", "Natural Wonder"]
},

{
    "id": "victoria-memorial",
    "name": "Victoria Memorial",
    "description": "Magnificent white marble monument built during British colonial era, now a museum",
    "coordinates": {"lat": 22.5448, "lng": 88.3426},
    "category": "historical",
    "history": "The Victoria Memorial was built between 1906 and 1921 to commemorate Queen Victoria's 25-year reign over India. Designed by British architect William Emerson, it combines British and Mughal architectural elements. After India's independence in 1947, it was converted into a museum showcasing the colonial history and Indian art. The memorial sits in 64 acres of landscaped gardens.",
    "period": "1906 CE - 1921 CE",
    "dynasty": "British Colonial Rule",
    "culturalFacts": [
        "Built with white Makrana marble from Rajasthan, the same material used for the Taj Mahal",
        "The bronze Angel of Victory statue atop the dome rotates with the wind",
        "Houses 25 galleries displaying paintings, manuscripts, and artifacts from British India",
        "The gardens feature numerous statues including Queen Victoria, Lord Curzon, and other colonial figures",
        "Popular cultural venue hosting light and sound shows depicting Kolkata's history"
    ],
    "legends": [
        {
            "title": "The Rotating Angel",
            "description": "The 16-foot bronze Angel of Victory crowning the memorial is designed to rotate with wind direction. Legend says it points toward prosperity when facing east and warns of challenges when turning west."
        },
        {
            "title": "The Midnight Procession",
            "description": "Local lore speaks of ghostly colonial-era processions seen in the memorial gardens on foggy winter nights, with sounds of horse carriages and British military bands echoing through the mist."
        }
    ],
    "tags": ["Colonial Architecture", "British Raj", "Marble Monument", "Museum", "Kolkata Heritage"]
},

{
    "id": "nalanda",
    "name": "Nalanda",
    "description": "Ancient Buddhist university and monastic complex, one of the world's first residential universities",
    "coordinates": {"lat": 25.1358, "lng": 85.4438},
    "category": "educational",
    "history": "Nalanda was an ancient center of higher learning in Bihar from the 5th century CE to 1200 CE. At its peak, it housed over 10,000 students and 2,000 teachers from across Asia, teaching subjects including Buddhist philosophy, logic, grammar, medicine, and mathematics. The university was destroyed by invader Bakhtiyar Khilji in 1193 CE. The ruins were excavated in the 19th century and designated a UNESCO World Heritage Site in 2016.",
    "period": "5th century CE - 12th century CE",
    "dynasty": "Gupta Empire, Pala Empire",
    "culturalFacts": [
        "UNESCO World Heritage Site since 2016 as an archaeological site of Nalanda Mahavihara",
        "Had a nine-story library called Dharmaganja with millions of manuscripts",
        "Attracted scholars from China, Korea, Japan, Tibet, Mongolia, Turkey, Sri Lanka, and Southeast Asia",
        "Chinese scholar Xuanzang studied here in the 7th century and documented its grandeur",
        "Covered an area of 14 hectares with lecture halls, meditation halls, and temples"
    ],
    "legends": [
        {
            "title": "The Three Libraries of Knowledge",
            "description": "Legend tells of three great libraries - Ratnasagara (Sea of Jewels), Ratnodadhi (Ocean of Jewels), and Ratnaranjaka (Delight of Jewels). When invaders set them on fire, the libraries burned for three months, showing the vastness of knowledge stored there."
        },
        {
            "title": "The Debate That Shook Mountains",
            "description": "According to tradition, the philosophical debates at Nalanda were so intense and profound that the nearby mountains would tremble, and divine beings would descend from heaven to listen to the discourse of learned masters."
        }
    ],
    "tags": ["UNESCO Heritage", "Ancient University", "Buddhist Learning", "Archaeological Site", "Bihar Heritage"]
},

{
    "id": "patna-golghar",
    "name": "Patna Golghar",
    "description": "Historic beehive-shaped granary built by the British to prevent famine",
    "coordinates": {"lat": 25.6171, "lng": 85.1392},
    "category": "historical",
    "history": "The Golghar (Round House) was constructed in 1786 by Captain John Garstin of the British East India Company to store grain as a safeguard against famine. The construction was prompted by the devastating famine of 1770 that killed millions. The massive granary, with its unique architecture and spiral staircase, was designed to store 140,000 tons of grain but was never used for its intended purpose.",
    "period": "1786 CE",
    "dynasty": "British East India Company",
    "culturalFacts": [
        "Built in the aftermath of the Great Bengal Famine of 1770",
        "Features a unique pillar-less structure with 145 steps spiraling to the top",
        "Offers panoramic views of Patna city and the Ganges River from the summit",
        "The doors were designed to open inward, preventing the structure from being filled to capacity",
        "Symbol of British engineering prowess and colonial administrative foresight"
    ],
    "legends": [
        {
            "title": "The Architectural Flaw",
            "description": "Legend says the architect designed the doors to open inward, meaning once filled with grain, the doors couldn't be opened. This ironic design flaw meant the granary remained empty, and the architect never received his full payment."
        },
        {
            "title": "The Curse of Abundance",
            "description": "Local folklore claims that the Golghar was cursed never to be filled because it was built from the suffering of famine victims. Any attempt to store grain would result in it mysteriously disappearing overnight."
        }
    ],
    "tags": ["British Architecture", "Colonial Heritage", "Granary", "Patna Landmark", "Historical Monument"]
},

{
    "id": "badami",
    "name": "Badami",
    "description": "Ancient capital of Chalukya dynasty famous for rock-cut cave temples",
    "coordinates": {"lat": 15.9149, "lng": 75.6765},
    "category": "religious",
    "history": "Badami served as the capital of the Early Chalukya dynasty from 540 CE to 757 CE. The town is famous for its four rock-cut cave temples carved into sandstone cliffs, built in the 6th century CE. These caves showcase Hindu, Jain, and possibly Buddhist influences. The Chalukyas later moved their capital, but Badami remained an important religious and cultural center.",
    "period": "6th century CE - 8th century CE",
    "dynasty": "Chalukya Dynasty",
    "culturalFacts": [
        "Features four cave temples carved into red sandstone cliffs overlooking Agastya Lake",
        "Cave 1 is dedicated to Shiva, Cave 2 and 3 to Vishnu, and Cave 4 to Jain Tirthankaras",
        "Cave 3 contains the largest cave temple with intricate carvings of Vishnu avatars",
        "The caves showcase the evolution of Indian rock-cut architecture",
        "Ancient inscriptions in Sanskrit and Kannada provide historical records of the Chalukya period"
    ],
    "legends": [
        {
            "title": "The Demon Slayer's Refuge",
            "description": "Legend says these caves were created by divine architect Vishwakarma for the Chalukya kings who slayed demons terrorizing the region. The caves were blessed to provide protection and spiritual power to righteous rulers."
        },
        {
            "title": "The Musical Pillars Secret",
            "description": "Local folklore speaks of hidden musical pillars within the caves that produce different classical ragas when struck in specific sequences, revealing the location of ancient Chalukya treasures."
        }
    ],
    "tags": ["Chalukya Dynasty", "Cave Temples", "Rock-cut Architecture", "Karnataka Heritage", "Ancient Capital"]
},

{
    "id": "pattadakal",
    "name": "Pattadakal",
    "description": "UNESCO World Heritage temple complex showcasing Chalukyan architectural synthesis",
    "coordinates": {"lat": 15.9477, "lng": 75.8165},
    "category": "religious",
    "history": "Pattadakal was the ceremonial capital of the Chalukya dynasty where kings were crowned. The site contains a group of 9 Hindu temples and a Jain sanctuary built in the 7th and 8th centuries CE. The temples represent the culmination of early Chalukyan architecture, blending the Nagara (North Indian) and Dravidian (South Indian) styles. UNESCO designated it a World Heritage Site in 1987.",
    "period": "7th-8th century CE",
    "dynasty": "Chalukya Dynasty",
    "culturalFacts": [
        "UNESCO World Heritage Site showcasing harmonious blend of northern and southern temple architecture",
        "The Virupaksha Temple was built by Queen Lokamahadevi to commemorate her husband's victory",
        "Contains inscriptions in Sanskrit, Kannada, and other languages documenting Chalukyan history",
        "Features exquisite sculptures depicting scenes from Ramayana, Mahabharata, and Puranas",
        "Represents the experimental phase that influenced later South Indian temple architecture"
    ],
    "legends": [
        {
            "title": "The Queen's Divine Dream",
            "description": "Legend says Queen Lokamahadevi had a divine vision where Lord Shiva instructed her to build a temple blending northern and southern styles to symbolize the unity of India. The Virupaksha Temple was the result of this divine command."
        },
        {
            "title": "The Coronation Sanctity",
            "description": "According to tradition, Chalukya princes who were crowned at Pattadakal gained divine blessings for just rule. Any king crowned elsewhere was said to face rebellions and misfortune, making Pattadakal essential for legitimate succession."
        }
    ],
    "tags": ["UNESCO Heritage", "Chalukya Architecture", "Temple Complex", "Karnataka Heritage", "Architectural Synthesis"]
},

{
    "id": "warangal-fort",
    "name": "Warangal Fort",
    "description": "Magnificent ruins of Kakatiya dynasty capital with iconic stone gateways",
    "coordinates": {"lat": 17.9784, "lng": 79.6005},
    "category": "historical",
    "history": "Warangal Fort was the capital of the Kakatiya dynasty from 12th to 14th century CE. Built by King Ganapati Deva and his daughter Queen Rudrama Devi, the fort showcases advanced engineering with concentric layers of defense. The most iconic structure is the Warangal Gate (Kakatiya Kala Thoranam), which has become the emblem of Telangana. The fort was later conquered by the Delhi Sultanate in 1323 CE.",
    "period": "12th-14th century CE",
    "dynasty": "Kakatiya Dynasty",
    "culturalFacts": [
        "The four ornamental gates (Thoranams) are architectural marvels and symbol of Telangana state",
        "Built using massive granite blocks fitted together without mortar using interlocking joints",
        "Features a 1000-pillared temple (Rudreshwara Temple) nearby, a Kakatiya masterpiece",
        "Advanced water management system with lakes and canals supported the kingdom",
        "Queen Rudrama Devi was one of the few female rulers in medieval India who fortified this capital"
    ],
    "legends": [
        {
            "title": "The Warrior Queen's Throne",
            "description": "Legend tells that Queen Rudrama Devi, one of India's few female rulers, held court in the fort dressed as a male warrior. Her throne had a secret mechanism that would detect deception, causing disloyal ministers to fall through a trapdoor."
        },
        {
            "title": "The Kohinoor Diamond Mystery",
            "description": "Local folklore claims that the famous Kohinoor diamond was mined from the Kollur mine near Warangal and was part of the Kakatiya treasury before being looted by Alauddin Khilji's forces during the conquest of the fort."
        }
    ],
    "tags": ["Kakatiya Dynasty", "Fort Architecture", "Telangana Heritage", "Medieval India", "Queen Rudrama Devi"]
},

{
    "id": "rameshwaram",
    "name": "Rameshwaram",
    "description": "Sacred island pilgrimage town with historic Ramanathaswamy Temple and Pamban Bridge",
    "coordinates": {"lat": 9.2876, "lng": 79.3129},
    "category": "religious",
    "history": "Rameshwaram is one of the holiest places in Hinduism, believed to be where Lord Rama built a bridge to Lanka and worshipped Lord Shiva to absolve sins after defeating Ravana. The Ramanathaswamy Temple was built in the 12th century and expanded over centuries. The island is connected to mainland India by the historic Pamban Bridge, built in 1914. It's one of the Char Dham pilgrimage sites.",
    "period": "12th century CE - Present (Temple), Ancient (Mythological)",
    "dynasty": "Pandya Dynasty, Setupati Kings",
    "culturalFacts": [
        "One of the Char Dham pilgrimage sites and one of the 12 Jyotirlinga temples",
        "The temple corridor is the longest in India at 1,220 meters with ornate pillars",
        "Features 22 sacred wells (theerthams) where pilgrims bathe before worship",
        "Pamban Bridge was India's first sea bridge and an engineering marvel of its time",
        "Dr. APJ Abdul Kalam was born here and his memorial attracts visitors worldwide"
    ],
    "legends": [
        {
            "title": "Ram Setu - The Divine Bridge",
            "description": "According to the Ramayana, Lord Rama and his vanara (monkey) army built a bridge of floating stones from Rameshwaram to Lanka. The remnants of this mythical bridge, called Adam's Bridge, can still be seen connecting India and Sri Lanka."
        },
        {
            "title": "The Two Lingams",
            "description": "Legend says Sita created a sand lingam for Rama to worship before Hanuman could bring one from Kashi. When Hanuman arrived with the Kashi lingam, both were installed in the temple. The sand lingam is worshipped first, honoring Sita's devotion."
        }
    ],
    "tags": ["Char Dham", "Jyotirlinga", "Ramayana", "Pamban Bridge", "Island Pilgrimage"]
},

{
    "id": "tirupati",
    "name": "Tirupati",
    "description": "Home to Venkateswara Temple, the world's richest and most visited religious site",
    "coordinates": {"lat": 13.6288, "lng": 79.4192},
    "category": "religious",
    "history": "Tirupati is home to the ancient Sri Venkateswara Temple located on Tirumala hills. The temple has been mentioned in ancient Tamil literature dating back to 300 CE, but the current structure was built during the Pallava period (9th century CE) and expanded by various dynasties. The temple receives the highest donations of any religious institution in the world and is visited by 50,000-100,000 pilgrims daily.",
    "period": "9th century CE - Present (Ancient references from 300 CE)",
    "dynasty": "Pallava Dynasty, Chola Empire, Vijayanagara Empire",
    "culturalFacts": [
        "The world's richest temple with annual donations exceeding billions of dollars",
        "Receives 50,000-100,000 pilgrims daily, making it the most visited religious site globally",
        "Famous for the tradition of devotees offering their hair as a sacrifice (tonsuring)",
        "The temple's main deity is adorned with jewels worth billions, including the famous Kiritam (crown)",
        "Tirumala Tirupati Devasthanams manages the temple and runs massive charitable operations"
    ],
    "legends": [
        {
            "title": "Venkateswara's Debt to Kubera",
            "description": "Legend says Lord Venkateswara borrowed money from Kubera (god of wealth) to finance his wedding to Goddess Padmavati. Devotees donate money to help the Lord repay this divine debt, which is why the temple receives such enormous wealth."
        },
        {
            "title": "The Self-Manifested Idol",
            "description": "According to tradition, the main idol of Lord Venkateswara is Swayambhu (self-manifested) and not carved by human hands. The deity's eyes are covered with a white mark because it's believed the Lord's direct gaze is too powerful for mortals to bear."
        }
    ],
    "tags": ["Venkateswara Temple", "Richest Temple", "Pilgrimage", "Hair Offering", "Andhra Pradesh Heritage"]
},

{
    "id": "lepakshi",
    "name": "Lepakshi",
    "description": "Historic temple town famous for the hanging pillar and Veerabhadra Temple",
    "coordinates": {"lat": 13.8283, "lng": 77.6037},
    "category": "religious",
    "history": "Lepakshi is famous for the Veerabhadra Temple built in the 16th century during the Vijayanagara Empire by brothers Viranna and Virupanna, who were governors under King Achyuta Deva Raya. The temple is renowned for its architectural marvels, exquisite frescoes, and the mysterious hanging pillar. The town's name comes from the legend of Jatayu from the Ramayana.",
    "period": "16th century CE",
    "dynasty": "Vijayanagara Empire",
    "culturalFacts": [
        "Famous for the hanging pillar that doesn't touch the ground, with a gap visible when paper is passed underneath",
        "Features India's largest monolithic Nandi bull statue, carved from a single granite block",
        "Temple ceilings have magnificent frescoes depicting scenes from Ramayana, Mahabharata, and Puranas",
        "The temple showcases the pinnacle of Vijayanagara architectural and artistic achievement",
        "Contains intricate carvings with over 70 pillars, each uniquely designed"
    ],
    "legends": [
        {
            "title": "Jatayu's Last Words - 'Le Pakshi'",
            "description": "Legend says that when Ravana abducted Sita, the divine eagle Jatayu fought him but was mortally wounded. He fell at this spot, and when Rama found him, he said 'Le Pakshi' (Rise, bird in Telugu), giving the town its name. A rock formation here is believed to be Jatayu's fallen body."
        },
        {
            "title": "The Hanging Pillar Miracle",
            "description": "According to local lore, a British engineer tried to move the hanging pillar to understand its construction secret. The moment he attempted to shift it, the entire temple structure began to shake. He immediately stopped, and the pillar remains mysteriously suspended to this day."
        }
    ],
    "tags": ["Vijayanagara Empire", "Hanging Pillar", "Veerabhadra Temple", "Monolithic Nandi", "Andhra Pradesh Heritage"]
}


    ]