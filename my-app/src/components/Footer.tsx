interface FooterProps {
  lastUpdated: string;
}

export function Footer({ lastUpdated }: FooterProps) {
  return (
    <footer style={{
      marginTop: '50px',
      paddingTop: '20px',
      borderTop: '1px solid #E5E7EB', 
      display: 'flex',
      justifyContent: 'space-between', 
      alignItems: 'center',
      color: '#6B7280', 
      fontSize: '0.875rem',
      fontFamily: 'sans-serif'
    }}>
      <div>
        <span>Platforma monitorizata activ</span>
      </div>

      <div>
        <span>Ultima actualizare: <strong>{lastUpdated}</strong></span>
      </div>
    </footer>
  );
}