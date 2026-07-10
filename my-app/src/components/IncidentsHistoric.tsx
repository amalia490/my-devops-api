import { IncidentCard} from './IncidentCard';
import type { IncidentCardProps } from './IncidentCard';

interface IncidentsHistoricProps {
  incidente: IncidentCardProps[];
}

export function IncidentsHistoric({ incidente }: IncidentsHistoricProps) {
  if (incidente.length === 0) {
    return (
      <div style={{ marginTop: '40px', fontFamily: 'sans-serif' }}>
        <h3 style={{ color: '#4B5563', borderBottom: '1px solid #E5E7EB', paddingBottom: '10px' }}>Istoric Incidente</h3>
        <p style={{ color: '#6B7280' }}>Nu s-au raportat incidente recente. Totul functioneaza perfect!</p>
      </div>
    );
  }
  return (
    <div style={{ marginTop: '40px', fontFamily: 'sans-serif' }}>
      <h3 style={{ color: '#4B5563', borderBottom: '1px solid #E5E7EB', paddingBottom: '10px', marginBottom: '20px' }}>
        Istoric Incidente
      </h3>

      {incidente.map((incident) => (
        <IncidentCard
          key={incident.id} 
          titlu={incident.titlu}
          descriere={incident.descriere}
          rezolvat={incident.rezolvat}
          serviceName={incident.serviceName}
          data={incident.data}
        />
      ))}
    </div>
  );
}