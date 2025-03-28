// filepath: c:\Users\devan\Documents\coding\projects\gdg\Frontend\src\components\Map\Map.jsx
import React, { useState } from "react";
import { GoogleMap, LoadScript, Marker, Autocomplete } from "@react-google-maps/api";

const containerStyle = {
    width: "100%",
    height: "500px",
};

const center = {
    lat: 37.7749, // San Francisco Latitude
    lng: -122.4194, // San Francisco Longitude
};

const MapComponent = () => {
    const [mapCenter, setMapCenter] = useState(center);
    const [autocomplete, setAutocomplete] = useState(null);

    const onLoad = (autocompleteInstance) => {
        setAutocomplete(autocompleteInstance);
    };

    const onPlaceChanged = () => {
        if (autocomplete !== null) {
            const place = autocomplete.getPlace();
            if (place.geometry) {
                setMapCenter({
                    lat: place.geometry.location.lat(),
                    lng: place.geometry.location.lng(),
                });
            }
        }
    };

    return (
        <LoadScript googleMapsApiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY} libraries={["places"]}>
            <div style={{ marginBottom: "10px" }}>
                <Autocomplete onLoad={onLoad} onPlaceChanged={onPlaceChanged}>
                    <input
                        type="text"
                        placeholder="Search for a location"
                        style={{
                            width: "300px",
                            height: "40px",
                            padding: "10px",
                            borderRadius: "5px",
                            border: "1px solid #ccc",
                        }}
                    />
                </Autocomplete>
            </div>
            <GoogleMap mapContainerStyle={containerStyle} center={mapCenter} zoom={12}>
                <Marker position={mapCenter} />
            </GoogleMap>
        </LoadScript>
    );
};

export default MapComponent;