import React, { useState } from "react";
import {
  GoogleMap,
  LoadScript,
  Marker,
  Autocomplete,
  InfoWindow,
  Circle,
} from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "100vh",
};

const center = {
  lat: 37.7749, // San Francisco Latitude
  lng: -122.4194, // San Francisco Longitude
};

const MapComponent = () => {
  const [mapCenter, setMapCenter] = useState(center);
  const [autocomplete, setAutocomplete] = useState(null);
  const [safetyData, setSafetyData] = useState(null);
  const [selectedPlace, setSelectedPlace] = useState(null);
  const [loading, setLoading] = useState(false); // New loading state

  const onLoad = (autocompleteInstance) => {
    setAutocomplete(autocompleteInstance);
  };

  const onPlaceChanged = async () => {
    if (autocomplete !== null) {
      const place = autocomplete.getPlace();
      if (place.geometry) {
        const lat = place.geometry.location.lat();
        const lng = place.geometry.location.lng();
        setMapCenter({ lat, lng });

        setLoading(true); // Start loading
        try {
          // Fetch safety data from the backend
          const response = await fetch("http://localhost:5000/check_safety", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ location: place.formatted_address }),
          });
          const data = await response.json();
          setSafetyData(data);
          console.log(data);
        } catch (error) {
          console.error("Error fetching safety data:", error);
        } finally {
          setLoading(false); // Stop loading
        }
      }
    }
  };

  // Function to determine circle color based on safety score
  const getCircleColor = () => {
    if (!safetyData || !safetyData.safety_score) return "#FF0000"; // Default to red if no data
    const score = parseInt(safetyData.safety_score.split("/")[0]); // Extract numeric score
    if (score > 80) return "#00FF00"; // Green for score > 80
    if (score >= 60) return "#FFFF00"; // Yellow for score between 60 and 80
    return "#FF0000"; // Red for score < 60
  };

  return (
    <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY} libraries={["places"]}>
      <div
        className="absolute w-[100vw] top-20 flex justify-center z-10 p-4"
        style={{ marginBottom: "10px" }}
      >
        <Autocomplete onLoad={onLoad} onPlaceChanged={onPlaceChanged}>
          <input
            type="text"
            placeholder="Search for a location"
            className="w-[600px] h-[40px] p-2 rounded-3xl border border-gray-300 bg-white text-center shadow-lg"
          />
        </Autocomplete>
      </div>
      <GoogleMap mapContainerStyle={containerStyle} center={mapCenter} zoom={12}>
        {/* Marker for the searched location */}
        <Marker position={mapCenter} />

        {/* Conditionally render the Circle around the searched location */}
        {safetyData?.safety_score && (
          <Circle
            center={mapCenter}
            radius={3000} // 3km radius
            options={{
              strokeColor: getCircleColor(),
              strokeOpacity: 0.8,
              strokeWeight: 2,
              fillColor: getCircleColor(),
              fillOpacity: 0.2,
            }}
          />
        )}

        {/* Markers for nearby emergency locations */}
        {safetyData?.safety_info?.map((info, index) => {
          const [type, name, vicinity] = info.split(" - ");
          const latLng = { lat: mapCenter.lat + 0.01 * index, lng: mapCenter.lng + 0.01 * index }; // Mock lat/lng for demo
          return (
            <Marker
              key={index}
              position={latLng}
              onClick={() => setSelectedPlace({ type, name, vicinity })}
            />
          );
        })}

        {/* InfoWindow for selected place */}
        {selectedPlace && (
          <InfoWindow
            position={mapCenter}
            onCloseClick={() => setSelectedPlace(null)}
          >
            <div>
              <h3>{selectedPlace.type}</h3>
              <p>{selectedPlace.name}</p>
              <p>{selectedPlace.vicinity}</p>
            </div>
          </InfoWindow>
        )}
      </GoogleMap>

      {/* Loading indicator */}
      {loading && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-4 rounded-lg shadow-lg">
          <p>Loading...</p>
        </div>
      )}

      {/* Sidebar for safety details */}
      {safetyData && (
        <div className="absolute top-20 left-4 bg-white p-4 rounded-lg shadow-lg w-[300px]">
          <h2 className="text-lg font-bold">Safety Details</h2>
          <p><strong>Location:</strong> {safetyData.location}</p>
          <p><strong>Distance from Main Road:</strong> {safetyData.distance_from_main_road}</p>
          <p><strong>Crime Level:</strong> {safetyData.crime_level}</p>
          <p><strong>CCTV Count:</strong> {safetyData.cctv_count}</p>
          <p><strong>Street Lighting:</strong> {safetyData.street_lighting}</p>
          <p><strong>Safety Score:</strong> {safetyData.safety_score}</p>
        </div>
      )}
    </LoadScript>
  );
};

export default MapComponent;