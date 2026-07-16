import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Channel } from '../components/Channel'; 
import { useQuery } from '@apollo/client/react';
import { GET_CHANNEL_DETAILS } from '../components/types';

export const ChannelPage: React.FC = () => {
  const { idAndName } = useParams<{ idAndName: string }>();
  const channelIdString = idAndName?.split('-')[0];
  const channelId = channelIdString ? parseInt(channelIdString, 10) : 0;

  const { loading, error, data } = useQuery(GET_CHANNEL_DETAILS, {
    variables: { NewsSourceId: channelId },
    skip: !channelId, 
  });

  if (loading) return <h2 style={{ textAlign: 'center', padding: '50px' }}>Se încarcă detaliile canalului... ⏳</h2>;
  
  if (error) return (
    <div style={{ textAlign: 'center', padding: '50px', color: '#DC2626' }}>
      <h2>Eroare la încărcarea canalului!</h2>
      <p>{error.message}</p>
    </div>
  );

  const source = data?.NewsSourcesById;

  if (!source) return <h2 style={{ textAlign: 'center' }}>Canalul nu a fost găsit.</h2>;

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      <Link 
        to="/" 
        style={{ 
          display: 'inline-block', 
          marginBottom: '20px', 
          color: '#1E3A8A', 
          textDecoration: 'none', 
          fontWeight: 'bold',
          fontSize: '1.1rem'
        }}
      >
        ← Înapoi la Toate Canalele
      </Link>

      <Channel source={source} />
    </div>
  );
};