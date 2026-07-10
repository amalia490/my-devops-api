export interface IncidentCardProps{
    id?: number; 
    titlu: string;
    descriere: string;
    rezolvat: boolean;
    serviceName: string;
    data: string;
}

export function IncidentCard({titlu, descriere, rezolvat, serviceName, data} : IncidentCardProps){
    const culoareBadge = rezolvat ? 'green' : '#F59E0B';
    const fundalCard = rezolvat ? '#F9FAFB' : '#FFFBEB';

    return (
    <div style={{
      border: `1px solid ${rezolvat ? '#E5E7EB' : '#FDE68A'}`,
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '20px',
      backgroundColor: fundalCard,
      fontFamily: 'sans-serif',
      boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
    }}>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
            <h3 style={{ margin: 0, color: '#111827', fontSize: '1.25rem' }}>{titlu}</h3>
            <span style={{backgroundColor: culoareBadge, color: 'white', padding: '4px 12px', borderRadius: '20px', fontSize: '0.75rem', fontWeight: 'bold', textTransform: 'uppercase'}}>
            {rezolvat ? 'Rezolvat' : 'In curs de rezolvare'}
            </span>
        </div>
        <p style={{ margin: '0 0 10px 0', color: '#4B5563', fontWeight: 'bold' }}>
            Serviciul din care face parte: {serviceName}
        </p>
        <p style={{ margin: '0 0 15px 0', color: '#4B5563', lineHeight: '1.5' }}>
            Descriere: {descriere}
        </p>
        <div style={{ fontSize: '0.875rem', color: '#6B7280' }}>
        🗓️ Raportat: {data}
        </div>
    </div>
    );
}