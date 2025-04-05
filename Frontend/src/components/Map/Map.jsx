import React, { useState } from "react";
import {
  GoogleMap,
  LoadScript,
  Marker,
  Autocomplete,
  InfoWindow,
  Circle,
} from "@react-google-maps/api";
import Loader from "../common/Loader";
import hospitalMarker from "../../assets/icons/hospital.png";

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
      console.log(place);
      if (place.geometry) {
        const lat = place.geometry.location.lat();
        const lng = place.geometry.location.lng();
        setMapCenter({ lat, lng });

        setLoading(true); // Start loading
        try {
          // Fetch safety data from the backend
          const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/check_safety`, {
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

    // Ensure safety_score is a string before splitting
    const scoreString = String(safetyData.safety_score);
    const score = parseInt(scoreString.split("/")[0]); // Extract numeric score

    if (score > 80) return "#00FF00"; // Green for score > 80
    if (score >= 60) return "#FFFF00"; // Yellow for score between 60 and 80
    return "#FF0000"; // Red for score < 60
  };

  return (
    <LoadScript
      googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}
      libraries={["places"]}
    >
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
      {loading ? (
        <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center bg-white z-50">
          <Loader />
        </div>
      ) : (
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={mapCenter}
          zoom={12}
          options={{
            mapTypeControl: false, // Disable Map and Satellite view
          }}
        >
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
          {safetyData?.safety_locations?.map((location, index) => {
            const icon =
              location.type === "hospital"
                ? hospitalMarker
                : location.type === "police"
                ? "https://maps.google.com/mapfiles/ms/icons/police.png"
                : "https://maps.google.com/mapfiles/ms/icons/red-dot.png";

            return (
              <Marker
                key={index}
                position={{ lat: location.lat, lng: location.lng }}
                icon={icon}
                onClick={() =>
                  setSelectedPlace({
                    type: location.type,
                    name: location.name,
                    vicinity: location.vicinity,
                  })
                }
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
      )}
      // Sidebar for safety details
      {safetyData && (
        <div className="absolute top-20 left-4 bg-white p-4 rounded-lg shadow-lg w-[300px]">
          <h2 className="text-lg font-bold">Safety Details</h2>
          <p>
            <strong>Location:</strong> {safetyData.location}
          </p>
          <p>
            <strong>Distance from Main Road:</strong>{" "}
            {safetyData.distance_from_main_road}
          </p>
          <p>
            <strong>Crime Level:</strong> {safetyData.crime_level}
          </p>
          <p>
            <strong>CCTV Count:</strong> {safetyData.cctv_count}
          </p>
          <p>
            <strong>Street Lighting:</strong> {safetyData.street_lighting}
          </p>
          <p>
            <strong>Summary:</strong>{" "}
            {safetyData.ai_response.replace(
              /```json\n|\n ```| "response"/g,
              ""
            )}
          </p>
          <p>
            <strong>Safety Score:</strong> {safetyData.safety_score}
          </p>
        </div>
      )}
    </LoadScript>
  );
};

export default MapComponent;
