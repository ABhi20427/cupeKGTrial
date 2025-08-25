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
}
        
        
    ]