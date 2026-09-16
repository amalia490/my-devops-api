import React from "react";
import { 
  ComposableMap, 
  Geographies, 
  Geography, 
  Marker, 
  ZoomableGroup, 
  Graticule, 
  Sphere 
} from "react-simple-maps";
import { PulsingMarker } from "./PulsingMarker";
import romaniaGeo from "../assets/romania-counties.json";

interface RomaniaMapProps {
  countiesData: any[]; 
}

export const RomaniaMap = ({ countiesData }: RomaniaMapProps) => {
  return (
    <div style={{ 
      width: "100%", 
      height: "700px", 
      backgroundColor: "transparent",
      borderRadius: "16px",
      overflow: "hidden",
      boxShadow: "0 0 40px rgba(79, 70, 229, 0.15)" 
    }}>
      <ComposableMap
        projection="geoOrthographic" 
        projectionConfig={{
          scale: 4500, 
          rotate: [-25, -46, 0] 
        }}
        width={800} 
        height={600}
        style={{ width: "100%", height: "100%" }}
      >
        <ZoomableGroup 
          center={[25, 46]} 
          minZoom={1} 
          maxZoom={6}
        >
          <Sphere 
            id="sphere"
            stroke="#1E1B4B" 
            strokeWidth={2} 
            fill="#06011A" 
          />
          
          <Graticule 
            stroke="#1E1B4B"    
            strokeWidth={1}    
            step={[2, 2]}       
          />

          <Geographies geography={romaniaGeo as any}>
            {({ geographies }) => (
              <>
                {geographies.map((geo) => (
                  <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    className="judet-interactiv"
                    onClick={() => {
                      console.log("Tot obiectul cu date:", geo.properties);
                    }}
                    
                    fill="#171038"
                    stroke="#4F46E5"
                    strokeWidth={0.8}
                    style={{ outline: "none" }} 
                  />
                ))}
              </>
            )}
          </Geographies>

          {countiesData.map((county) => (
            <Marker key={county.id} coordinates={[county.longitude, county.latitude]}>
              <PulsingMarker 
                  countyName={county.name} 
                  newsCount={county.newsCount} 
              />
            </Marker>
          ))}
        </ZoomableGroup>
      </ComposableMap>
    </div>
  );
};