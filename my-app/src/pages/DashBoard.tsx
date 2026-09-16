import React from 'react';
import { useQuery } from '@apollo/client/react';
import { GET_MAP_DATA } from '../components/types';
import { RomaniaMap } from '../components/Romania';
// import { NewsDashboard } from '../components/NewsDashboard';

export function DashBoard() {
  const { loading, error, data } = useQuery(GET_MAP_DATA, {
    pollInterval: 60000 
  });

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundColor: '#0B0024' }}>
        <h2 style={{ color: '#818CF8' }}>Se aduc ultimele știri... 📡</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ textAlign: 'center', padding: '50px', color: '#EF4444', backgroundColor: '#0B0024', height: '100vh' }}>
        <h2>Eroare de conexiune la serverul de știri!</h2>
        <p>{error.message}</p>
      </div>
    );
  }

  const countiesData = data?.Counties || [];

  return (
    <div style={{ width: '100%', minHeight: '100vh', backgroundColor: '#0B0024', padding: '20px' }}>
      <RomaniaMap countiesData={countiesData} />
    </div>
  );
}