// components/LocationMarker/LocationMarker.jsx
import React, { useEffect, useState } from 'react';
import { Marker, Tooltip } from 'react-leaflet';
import L from 'leaflet';
import './LocationMarker.css';

// Fix for default marker icon in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

const LocationMarker = ({ location, isSelected, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);
  const [markerRef, setMarkerRef] = useState(null);

  // Create custom icon based on location category and state
  const getCustomIcon = () => {
    const size = isSelected ? 48 : isHovered ? 40 : 32;
    
    // Define colors for different categories
    const colors = {
      historical: '#E91E63',  // Pink
      cultural: '#4CAF50',    // Green
      religious: '#FFC107',   // Amber
      default: '#2196F3'      // Blue
    };
    
    const color = colors[location.category] || colors.default;
    
    return L.divIcon({
      className: `custom-marker ${isSelected ? 'selected' : ''} ${isHovered ? 'hovered' : ''}`,
      html: `
        <div class="marker-container" style="width: ${size}px; height: ${size}px;">
          <svg viewBox="0 0 24 24" width="${size}" height="${size}">
            <path fill="${color}" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
          </svg>
          ${isSelected || isHovered ? `<div class="marker-pulse" style="border-color: ${color}"></div>` : ''}
        </div>
      `,
      iconSize: [size, size],
      iconAnchor: [size/2, size],
    });
  };
  
  useEffect(() => {
    // Apply animations when selection state changes
    if (markerRef) {
      if (isSelected) {
        markerRef._icon.classList.add('bounce-animation');
        setTimeout(() => {
          if (markerRef._icon) {
            markerRef._icon.classList.remove('bounce-animation');
          }
        }, 1000);
      }
    }
  }, [isSelected, markerRef]);

  const handleMarkerClick = () => {
    // Make sure this function is called and passing the location
    console.log("Marker clicked:", location.name);
    onClick(location);
  };

  return (
    <Marker
      position={[location.coordinates.lat, location.coordinates.lng]}
      icon={getCustomIcon()}
      eventHandlers={{
        click: handleMarkerClick,
        mouseover: () => setIsHovered(true),
        mouseout: () => setIsHovered(false),
      }}
      ref={(ref) => setMarkerRef(ref)}
    >
      <Tooltip 
        direction="top" 
        offset={[0, -20]} 
        opacity={0.9}
        permanent={isSelected || isHovered}
        className={`location-tooltip ${isSelected ? 'selected' : ''}`}
      >
        <div className="tooltip-content">
          <span className="location-name">{location.name}</span>
          {isSelected && <span className="location-hint">Click for details</span>}
        </div>
      </Tooltip>
    </Marker>
  );
};

export default LocationMarker;