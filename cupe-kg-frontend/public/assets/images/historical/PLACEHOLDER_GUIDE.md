# Historical Images Placeholder Guide

## 📁 Directory: `/public/assets/images/historical/`

All the placeholder files have been created for you! Simply replace these placeholder files with actual historical photos of the monuments in their prime era.

## 🏛️ **Primary Historical Images** (Replace these with main historical photos):

### Major Monuments
- `taj-mahal-mughal-prime.jpg` - Taj Mahal in Mughal prime era
- `red-fort-mughal-prime.jpg` - Red Fort in Mughal prime era  
- `qutub-minar-sultanate-prime.jpg` - Qutub Minar in Sultanate era
- `india-gate-british-prime.jpg` - India Gate in British era
- `hampi-vijayanagara-prime.jpg` - Hampi in Vijayanagara prime era
- `mysore-palace-wodeyar-prime.jpg` - Mysore Palace in Wodeyar era
- `golconda-qutbshahi-prime.jpg` - Golconda Fort in Qutb Shahi era

### Temples & Religious Sites
- `meenakshi-temple-pandyan-prime.jpg` - Meenakshi Temple in Pandyan era
- `somnath-chalukya-prime.jpg` - Somnath Temple in Chalukya era
- `dwarkadhish-ancient-prime.jpg` - Dwarkadhish Temple in ancient era
- `golden-temple-sikh-prime.jpg` - Golden Temple in Sikh empire era
- `lotus-temple-modern-prime.jpg` - Lotus Temple in modern era
- `birla-mandir-modern-prime.jpg` - Birla Mandir in modern era
- `sanchi-stupa-mauryan-prime.jpg` - Sanchi Stupa in Mauryan era
- `khajuraho-chandela-prime.jpg` - Khajuraho in Chandela era
- `konark-ganga-prime.jpg` - Konark Sun Temple in Eastern Ganga era

### Cave Complexes
- `ajanta-gupta-prime.jpg` - Ajanta Caves in Gupta period
- `ellora-rashtrakuta-prime.jpg` - Ellora Caves in Rashtrakuta period

### Cities & Regions  
- `agra-mughal-prime.jpg` - Agra in Mughal era
- `delhi-sultanate-prime.jpg` - Delhi in Sultanate era
- `madurai-pandyan-prime.jpg` - Madurai in Pandyan era
- `amritsar-sikh-prime.jpg` - Amritsar in Sikh era
- `kanyakumari-ancient-prime.jpg` - Kanyakumari in ancient era

## 🎨 **Generic Era Images** (Optional - for fallbacks):
- `ancient-architecture.jpg` - Generic ancient Indian architecture
- `medieval-architecture.jpg` - Generic medieval architecture  
- `mughal-architecture.jpg` - Generic Mughal architecture
- `modern-architecture.jpg` - Generic modern architecture

## 📝 **Image Requirements:**
- **Format:** JPG preferred (PNG also works)
- **Size:** Minimum 800x600px, recommended 1200x800px or higher
- **Quality:** High resolution for best viewing experience
- **Content:** Show the monument/site in its historical prime with:
  - Complete/restored architecture
  - Period-appropriate surroundings
  - Cultural/religious activities if possible
  - Vibrant colors and life

## 🔄 **How to Replace:**
1. Find the placeholder file you want to replace
2. Delete the placeholder file
3. Add your historical photo with the exact same filename
4. The HistoricalView component will automatically display your image!

## 🆘 **Fallback System:**
If primary image isn't found, the system tries:
1. `{location}-historical.jpg`
2. `{location}-prime.jpg`  
3. `{era}-architecture.jpg`
4. `generic-{dynasty}.jpg`
5. `default-historical.svg` (provided)