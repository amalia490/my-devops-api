export type ServiceStatus = 'operational' | 'degraded' | 'outage';

interface StatusBadgeProps {
  status: ServiceStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  let culoare = '';
  let text = '';
  let iconita = '';

  switch (status) {
    case 'operational':
      culoare = '#10B981';
      text = 'Operațional';
      iconita = '🟢';
      break;
    case 'degraded':
      culoare = '#F59E0B'; 
      text = 'Performanță Scăzută';
      iconita = '🟡';
      break;
    case 'outage':
      culoare = '#EF4444';
      text = 'Picat';
      iconita = '🔴';
      break;
  }

  return (
    <span style={{ 
      color: culoare, 
      fontWeight: 'bold', 
      display: 'flex', 
      alignItems: 'center', 
      gap: '6px' 
    }}>
      {iconita} {text}
    </span>
  );
}