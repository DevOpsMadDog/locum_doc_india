"use client";

import { GoogleMap, Marker, useJsApiLoader } from "@react-google-maps/api";

const containerStyle = {
  width: "100%",
  height: "100vh",
};

const chennaiCenter = { lat: 13.0827, lng: 80.2707 };

export default function LiveMap({ doctorLocation }) {
  const { isLoaded } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || "",
  });

  if (!isLoaded) {
    return <div style={{ padding: 24 }}>Loading map...</div>;
  }

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={chennaiCenter} zoom={12}>
      {doctorLocation && <Marker position={doctorLocation} />}
    </GoogleMap>
  );
}
