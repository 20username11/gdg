import React, { useState } from "react";
import {
  GoogleMap,
  Polyline,
  Marker,
  Autocomplete,
  useJsApiLoader,
} from "@react-google-maps/api";

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

    try {
      const response = await fetch(
        "https://40c4-103-97-165-190.ngrok-free.app/get_safe_routes",
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
        return;
      }

      const data = await response.json();
      console.log("Routes:", data.routes); // Debugging: Log the routes
      setRoutes(data.routes); // Update the routes state with the response
    } catch (error) {
      console.error("Error fetching routes:", error);
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
        <h2 className="flex justify-center  text-lg font-bold mb-2">Find Route</h2>
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
      <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={8}>
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
              {route.safe_places.map(([name, location], idx) => (
                <Marker
                  key={idx}
                  position={location}
                  label={name}
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
