# Historical Images for Timeline Feature

This directory contains historical visualizations and reconstructions of heritage sites in their prime cultural periods.

## Directory Structure

```
historical/
├── {location-id}-{era}-prime.jpg          # Primary historical image
├── {location-id}-historical.jpg           # General historical image
├── {location-id}-prime.jpg               # Prime period image
├── {era}-architecture.jpg                # Era-specific architecture
├── {dynasty-name}.jpg                    # Dynasty-specific images
└── default-historical.jpg                # Default fallback
```

## Image Naming Convention

### Location-specific images:
- `hampi-ce-prime.jpg` - Hampi during CE era prime
- `taj-mahal-historical.jpg` - Taj Mahal historical view
- `khajuraho-prime.jpg` - Khajuraho in its prime

### Era-specific images:
- `ce-architecture.jpg` - Common Era architecture
- `bce-architecture.jpg` - Before Common Era architecture

### Dynasty-specific images:
- `mughal-empire.jpg` - Mughal dynasty style
- `vijayanagara-empire.jpg` - Vijayanagara empire style
- `chola-dynasty.jpg` - Chola dynasty style

## Image Requirements

- **Format**: JPG, PNG, or WebP
- **Resolution**: Minimum 1200x800px for best quality
- **Aspect Ratio**: 3:2 or 16:9 preferred
- **Content**: Historical reconstructions, archaeological evidence, or period artwork

## Image Sources

Consider using:
1. Archaeological reconstructions
2. Historical paintings and artwork
3. Digital reconstructions by historians
4. Period drawings and sketches
5. Virtual reality reconstructions

## Fallback System

The system will try images in this order:
1. `{location-id}-{era}-prime.jpg`
2. `{location-id}-historical.jpg`
3. `{location-id}-prime.jpg`
4. `{era}-architecture.jpg`
5. `{dynasty-name}.jpg`
6. `default-historical.jpg`

## Creating Historical Content

To add historical visualizations:
1. Research the location's prime cultural period
2. Find or create appropriate historical images
3. Name the files according to the convention
4. Place them in this directory
5. Test the timeline feature to verify loading

## Example Locations

Priority locations for historical images:
- **Hampi** (Vijayanagara Empire, 1336-1646 CE)
- **Taj Mahal** (Mughal Empire, 1632-1653 CE)
- **Khajuraho** (Chandela Dynasty, 950-1050 CE)
- **Ajanta Caves** (Satavahana/Vakataka, 2nd century BCE - 6th century CE)
- **Golden Temple** (Sikh Gurus, 1577-1604 CE)

This feature creates an immersive experience showing how heritage sites looked during their peak cultural periods!