import { useQuery } from '@apollo/client/react';
import { GET_NEWS } from '../components/types';
import { NewsDashboard } from '../components/NewsDashboard';

export function DashBoard() {
  const { loading, error, data } = useQuery(GET_NEWS, {
    pollInterval: 60000 
  });

  if (loading) return <h2 style={{ textAlign: 'center', padding: '50px', color: '#1E3A8A' }}>Se aduc ultimele știri... 📡</h2>;
  
  if (error) return (
    <div style={{ textAlign: 'center', padding: '50px', color: '#DC2626' }}>
      <h2>Eroare de conexiune la serverul de știri!</h2>
      <p>{error.message}</p>
    </div>
  );

  const displayedSources = data?.NewsSources || [];

  return <NewsDashboard NewsSources={displayedSources} />;
}