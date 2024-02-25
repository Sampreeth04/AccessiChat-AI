import React, { useState, useRef, useMemo, useCallback } from "react";
import usePlacesAutocomplete, {
  getGeocode,
  getLatLng,
} from "use-places-autocomplete";
import {
  GoogleMap,
  useLoadScript,
  MarkerF,
  Circle,
  DirectionsRenderer,
} from "@react-google-maps/api";

export function Places({ setOffice }) {
  const {
    ready,
    value,
    setValue,
    suggestions: { status, data },
    clearSuggestions,
  } = usePlacesAutocomplete();

  const handleSelect = async (val) => {
    setValue(val, false);
    clearSuggestions();

    const results = await getGeocode({ address: val });
    const { lat, lng } = await getLatLng(results[0]);
    setOffice({ lat, lng });
  };
}

export function Distance({ leg }) {
  if (!leg.distance || !leg.duration) return null;

  return (
    <div>
      <p>
        This hospital is <span className="highlight">{leg.distance.text}</span>{" "}
        away from your home. That would take{" "}
        <span className="highlight">{leg.duration.text}</span> each direction.
      </p>
    </div>
  );
}
const libraries = ["places"];
const mapContainerStyle = {
  width: "100vw",
  height: "100vh",
};
const center = {
  lat: 43.07213891862731, // default latitude
  lng: -89.40643786738592, // default longitude
};
const hospital1 = {
  lat: 43.065212,
  lng: -89.401584,
};
const hospital2 = {
  lat: 43.065933,
  lng: -89.399383,
};
const hospital3 = {
  lat: 43.059338,
  lng: -89.401429,
};
const hospital4 = {
  lat: 43.074248,
  lng: -89.431126,
};
const hospital5 = {
  lat: 43.076585,
  lng: -89.431847,
};
const hospital6 = {
  lat: 43.133732,
  lng: -89.398569,
};
const hospital7 = {
  lat: 43.019153,
  lng: -89.525006,
};
const hospital8 = {
  lat: 43.153039,
  lng: -89.296703,
};
const hospital9 = {
  lat: 42.920225,
  lng: -89.210744,
};
const hospital10 = {
  lat: 43.282854,
  lng: -89.720065,
};

const Map = () => {
  const [office, setOffice] = useState();
  const [directions, setDirections] = useState();
  const mapRef = useRef();
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: "AIzaSyD6UweKilcNOrzqS5XjFffg7stPOd0atNs",
    libraries,
  });
  const center = useMemo(
    () => ({ lat: 43.07213891862731, lng: -89.40643786738592 }),
    []
  );
  const options = useMemo(
    () => ({
      mapId: "9b9970c6c984ad16",
      disableDefaultUI: false,
      clickableIcons: false,
    }),
    []
  );
  const onLoad = useCallback((map) => (mapRef.current = map), []);

  if (loadError) {
    return <div>Error loading maps</div>;
  }

  if (!isLoaded) {
    return <div>Loading maps</div>;
  }
  const defaultOptions = {
    strokeOpacity: 0.5,
    strokeWeight: 2,
    clickable: false,
    draggable: false,
    editable: false,
    visible: true,
  };
  const closeOptions = {
    ...defaultOptions,
    zIndex: 3,
    fillOpacity: 0.05,
    strokeColor: "#8BC34A",
    fillColor: "#8BC34A",
  };
  const middleOptions = {
    ...defaultOptions,
    zIndex: 2,
    fillOpacity: 0.05,
    strokeColor: "#FBC02D",
    fillColor: "#FBC02D",
  };
  const farOptions = {
    ...defaultOptions,
    zIndex: 1,
    fillOpacity: 0.05,
    strokeColor: "#FF5252",
    fillColor: "#FF5252",
  };
  return (
    <div className="map">
      <GoogleMap
        mapContainerClassName="map-container"
        mapContainerStyle={mapContainerStyle}
        zoom={10}
        center={center}
        onLoad={onLoad}
        options={options}
      >
        {directions && (
          <DirectionsRenderer
            directions={directions}
            options={{
              polylineOptions: {
                zIndex: 50,
                strokeColor: "#1976D2",
                strokeWeight: 5,
              },
            }}
          />
        )}

        <MarkerF
          position={center}
          icon="https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png"
        />
        <MarkerF position={hospital1} />
        <MarkerF position={hospital2} />
        <MarkerF position={hospital3} />
        <MarkerF position={hospital4} />
        <MarkerF position={hospital5} />
        <MarkerF position={hospital6} />
        <MarkerF position={hospital7} />
        <MarkerF position={hospital8} />
        <MarkerF position={hospital9} />
        <MarkerF position={hospital10} />

        <Circle center={center} radius={15000} options={closeOptions} />
        <Circle center={center} radius={30000} options={middleOptions} />
        <Circle center={center} radius={45000} options={farOptions} />
      </GoogleMap>
    </div>
  );
};

export default Map;
