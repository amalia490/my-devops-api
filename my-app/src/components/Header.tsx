interface HeaderProps{
    status: 'operational' | 'issues' | 'down'
}

export function Header({status}: HeaderProps){
    let bannerColor = '';
    let mesaj = '';
    if (status === 'operational'){
        bannerColor = '#10B981'; 
        mesaj = 'Toate sistemele sunt operationale';
    } else if (status === 'issues'){
        bannerColor = '#FBBF24'; 
        mesaj = 'Probleme de performanta detectate';
    } else if (status === 'down'){
        bannerColor = '#EF4444'; 
        mesaj = 'Sistemul este in prezent indisponibil';
    }
    return (
    <header style={{ marginBottom: '30px', fontFamily: 'sans-serif' }}>
      <h1 style={{ fontSize: '2rem', color: '#333' }}>Status Platforma DevOps</h1>
      
      <div style={{
        backgroundColor: bannerColor,
        color: 'white',
        padding: '15px 20px',
        borderRadius: '8px',
        fontSize: '1.2rem',
        fontWeight: 'bold',
        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
        transition: 'background-color 0.3s ease' 
      }}>
        {mesaj}
      </div>
    </header>
  );
}