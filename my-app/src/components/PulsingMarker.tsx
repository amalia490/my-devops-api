import React from 'react';
import { Marker } from "react-simple-maps"; // Dacă folosești librăria

export const PulsingMarker = ({ countyName, newsCount, coordinates } : {countyName: string, newsCount: number, coordinates ?: [number, number]}) => {
  if (newsCount === 0) return null;
  const baseRadius = 4 + (newsCount * 1.5); 
  
  return (
    <g onClick={() => alert(`Ai dat click pe ${countyName}!`)} style={{ cursor: 'pointer' }}>
      <circle 
        r={baseRadius} 
        fill="none" 
        stroke="red" 
        strokeWidth="2"
      >
        <animate 
          attributeName="r" 
          begin="0s" 
          dur="1.5s" 
          values={`${baseRadius}; ${baseRadius * 3}`} 
          calcMode="spline" 
          keyTimes="0; 1" 
          keySplines="0.165, 0.84, 0.44, 1" 
          repeatCount="indefinite" 
        />
        <animate 
          attributeName="opacity" 
          begin="0s" 
          dur="1.5s" 
          values="1; 0" 
          calcMode="spline" 
          keyTimes="0; 1" 
          keySplines="0.3, 0.61, 0.355, 1" 
          repeatCount="indefinite" 
        />
      </circle>

      <circle 
        r={baseRadius} 
        fill="red" 
      />
      
    </g>
    // </Marker>
  );
};