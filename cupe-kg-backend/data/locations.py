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
        }
    ]