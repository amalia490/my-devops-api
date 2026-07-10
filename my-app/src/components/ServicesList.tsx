import { StatusBadge } from './StatusBadge';
export interface Service {
  id: number;
  name: string;
  status: 'operational' | 'degraded' | 'outage';
}

interface ServicesListProps {
  services: Service[];
}

export function ServicesList({ services }: ServicesListProps) {
  const getStatusBadge = (status: Service['status']) => {
    return <StatusBadge status={status} />;
  };

  return (
    <div style={{ marginBottom: '40px', fontFamily: 'sans-serif' }}>
      <h2 style={{ color: '#333', borderBottom: '2px solid #E5E7EB', paddingBottom: '10px', marginBottom: '20px' }}>
        Status Servicii
      </h2>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {services.map((service) => (
          <div 
            key={service.id}
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '16px 20px',
              backgroundColor: '#F9FAFB', 
              border: '1px solid #E5E7EB',
              borderRadius: '8px',
              boxShadow: '0 1px 2px rgba(0,0,0,0.05)'
            }}
          >
            <span style={{ fontSize: '1.1rem', fontWeight: '500', color: '#111827' }}>
              {service.name}
            </span>
            
            {getStatusBadge(service.status)}
          </div>
        ))}
      </div>
    </div>
  );
}