import React, { useState, useRef } from "react";
import {
  GoogleMap,
  Polyline,
  Marker,
  Autocomplete,
  useJsApiLoader,
} from "@react-google-maps/api";
import Loader from "../common/Loader";

const containerStyle = {
  width: "100%",
  height: "100vh",
};

const center = {
  lat: 19.076, // Mumbai Latitude
  lng: 72.8777, // Mumbai Longitude
};

const FindRoute = () => {
  const [routes, setRoutes] = useState(null);
  const [from, setFrom] = useState(""); // State for "From" location
  const [to, setTo] = useState(""); // State for "To" location
  const [fromAutocomplete, setFromAutocomplete] = useState(null); // Autocomplete instance for "From"
  const [toAutocomplete, setToAutocomplete] = useState(null); // Autocomplete instance for "To"
  const [loading, setLoading] = useState(false); // Loading state
  const mapRef = useRef(null); // Reference to the Google Map instance

  // Use useJsApiLoader to load the Google Maps API
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
    libraries: ["places", "geometry"],
  });

  const fetchRoutes = async () => {
    if (!from || !to) {
      alert("Please enter both 'From' and 'To' locations.");
      return;
    }

    setLoading(true); // Start loading

    try {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/get_safe_routes`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ start: from, destination: to }), // Send start and destination
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Error:", errorData);
        alert(`Error: ${errorData.error}`);
        setLoading(false); // Stop loading
        return;
      }

      const data = await response.json();
      console.log("Routes:", data.routes); // Debugging: Log the routes
      setRoutes(data.routes); // Update the routes state with the response

      // Move the map to the "From" location
      if (mapRef.current && fromAutocomplete) {
        const place = fromAutocomplete.getPlace();
        if (place && place.geometry) {
          const { lat, lng } = place.geometry.location;
          mapRef.current.panTo({ lat: lat(), lng: lng() });
        }
      }
    } catch (error) {
      console.error("Error fetching routes:", error);
    } finally {
      setLoading(false); // Stop loading
    }
  };

  const handleFromPlaceChanged = () => {
    if (fromAutocomplete) {
      const place = fromAutocomplete.getPlace();
      if (place && place.formatted_address) {
        setFrom(place.formatted_address);
      }
    }
  };

  const handleToPlaceChanged = () => {
    if (toAutocomplete) {
      const place = toAutocomplete.getPlace();
      if (place && place.formatted_address) {
        setTo(place.formatted_address);
      }
    }
  };

  if (!isLoaded) {
    return <div>Loading...</div>; // Show a loading indicator until the API is loaded
  }

  return (
    <div>
      {/* Input fields for "From" and "To" locations */}
      <div className="absolute top-[15vh] left-4 z-10 bg-white p-4 rounded-lg shadow-xl">
        <h2 className="flex justify-center text-lg font-bold mb-2">Find Route</h2>
        <Autocomplete
          onLoad={(autocomplete) => setFromAutocomplete(autocomplete)}
          onPlaceChanged={handleFromPlaceChanged}
        >
          <input
            type="text"
            placeholder="From"
            value={from}
            onChange={(e) => setFrom(e.target.value)}
            className="w-full mb-2 p-2 border border-gray-300 rounded"
          />
        </Autocomplete>
        <Autocomplete
          onLoad={(autocomplete) => setToAutocomplete(autocomplete)}
          onPlaceChanged={handleToPlaceChanged}
        >
          <input
            type="text"
            placeholder="To"
            value={to}
            onChange={(e) => setTo(e.target.value)}
            className="w-full mb-2 p-2 border border-gray-300 rounded"
          />
        </Autocomplete>
        <button
          onClick={fetchRoutes}
          className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
        >
          Find Route
        </button>
      </div>

      {/* Google Map */}
      <GoogleMap
        mapContainerStyle={containerStyle}
        center={center}
        zoom={8}
        onLoad={(map) => (mapRef.current = map)} // Save the map instance
      >
        {/* Show loading overlay */}
        {loading && (
          <div className="absolute top-0 left-0 w-full h-full flex items-center justify-center bg-white z-50">
                    <Loader />
          </div>
        )}

        {/* Render routes */}
        {routes?.map((route, index) => {
          // Assign colors based on the index of the route
          const colors = ["#00FF00", "#FFFF00", "#FF0000"]; // Green, Yellow, Red
          const strokeColor = colors[index % colors.length]; // Cycle through colors if more than 3 routes

          return (
            <React.Fragment key={index}>
              {/* Render the polyline for the route */}
              <Polyline
                path={window.google.maps.geometry.encoding.decodePath(
                  route.polyline
                )} // Use window.google
                options={{
                  strokeColor, // Assign color based on index
                  strokeOpacity: 0.8,
                  strokeWeight: 4,
                }}
              />

              {/* Render markers for safe places */}
              {route.safe_places.map(([, location], idx) => (
                <Marker
                  key={idx}
                  position={location}
                  icon="https://maps.google.com/mapfiles/ms/icons/police.png"
                />
              ))}
            </React.Fragment>
          );
        })}
      </GoogleMap>
    </div>
  );
};

export default FindRoute;