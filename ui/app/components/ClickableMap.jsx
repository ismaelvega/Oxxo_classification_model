"use client";
import React, { useState } from 'react';

import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';

const mapContainerStyle = {
  width: '100%',
  height: '400px'
};

// initial center of the map
const defaultCenter = {
  lat: 37.7749,
  lng: -122.4194
};

function ClickableMap({ onCoordinatesChange }) { // Accept onCoordinatesChange as a prop
  const [coords, setCoords] = useState({ lat: null, lng: null });

  const handleMapClick = event => {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    const newCoords = { lat, lng };
    setCoords(newCoords);
    if (onCoordinatesChange) { // If the callback is provided
      onCoordinatesChange(newCoords); // Call it with the new coordinates
    }
  };

  return (
    <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}>
      <GoogleMap
        mapContainerStyle={mapContainerStyle}
        center={defaultCenter}
        zoom={10}
        onClick={handleMapClick}
      >
        {coords.lat && (
          <Marker position={coords} />
        )}
      </GoogleMap>

      {coords.lat && (
        <div style={{ marginTop: 8 }}>
          <strong>Clicked Coordinates:</strong><br/>
          Latitude: {coords.lat.toFixed(6)}<br/>
          Longitude: {coords.lng.toFixed(6)}
        </div>
      )}
    </LoadScript>
  );
}

export default ClickableMap;
