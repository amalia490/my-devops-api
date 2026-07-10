import './App.css'
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { IncidentCard} from './components/IncidentCard';
import type { IncidentCardProps } from './components/IncidentCard';
import { IncidentsHistoric } from './components/IncidentsHistoric';
import { ServicesList} from './components/ServicesList';
import type { Service } from './components/ServicesList';
import { ApolloClient, HttpLink, InMemoryCache, gql } from "@apollo/client";
import { ApolloProvider } from "@apollo/client/react";

function App() {
  const timpulCurent = new Date().toLocaleTimeString('ro-RO');
  const client = new ApolloClient({
  link: new HttpLink({ uri: "https://flyby-router-demo.herokuapp.com/" }),
  cache: new InMemoryCache(),
  });
  const mockedServices: Service[] = [
    { id: 1, name: "API Autentificare", status: "operational" },
    { id: 2, name: "Baza de Date Principală", status: "operational" },
    { id: 3, name: "Procesare Plăți", status: "degraded" },
    { id: 4, name: "Aplicație Frontend", status: "operational" }
  ];
  const dateDeLaBackend: IncidentCardProps[] = [
    {
      id: 1,
      titlu: "Picaj temporar Frontend",
      descriere: "Aplicația web nu a putut fi accesată timp de 5 minute din cauza unei configurări greșite la serverul de DNS.",
      rezolvat: true,
      serviceName: "Serviciul Web", 
      data: "9 Iulie 2026, 09:12 EEST"
    },
    {
      id: 2,
      titlu: "Eroare la procesarea imaginilor",
      descriere: "Serviciul S3 a refuzat conexiunile pentru scurt timp. S-a făcut rollback la versiunea anterioară.",
      rezolvat: false,
      serviceName: "Serviciul de Stocare",
      data: "7 Iulie 2026, 14:30 EEST"
    },
    {
      id: 3,
      titlu: "Latență pe API-ul de Plăți",
      descriere: "Timp de răspuns ridicat din cauza unor indexuri lipsă în baza de date SQLModel.",
      rezolvat: true,
      serviceName: "Serviciul de Plăți",
      data: "2 Iulie 2026, 11:05 EEST"
    }
  ];

  const isOutage = mockedServices.some(s => s.status === 'outage');
  const isDegraded = mockedServices.some(s => s.status === 'degraded');
  const headerStatus = isOutage ? 'down' : (isDegraded ? 'issues' : 'operational');

  return (
    <div style={{maxWidth: '800px', margin: '0 auto', padding: '20px', minHeight: '100vh', display: 'flex', flexDirection: 'column'}}>
      
      <Header status={headerStatus} />

      <main style={{ flex: 1 }}>
        <h2 style={{ fontFamily: 'sans-serif', color: '#333', borderBottom: '2px solid #E5E7EB', paddingBottom: '10px' }}>
          Incidente Raportate
        </h2>

        <IncidentCard 
          titlu="Latență crescută pe API-ul de Plăți"
          descriere="Investigăm o problemă care cauzează un timp de răspuns ridicat pentru procesarea plăților. Baza de date este stabilă, dar nodurile de worker sunt suprasolicitate."
          rezolvat={false}
          serviceName="Serviciul de Plăți"
          data="10 Iulie 2026, 18:45 EEST"
        />

        <IncidentCard 
          titlu="Picaj temporar Frontend"
          descriere="Aplicația web nu a putut fi accesată timp de 5 minute din cauza unei configurări greșite la serverul de DNS. Problema a fost identificată și remediată."
          rezolvat={true}
          serviceName="Serviciul Web"
          data="9 Iulie 2026, 09:12 EEST"
        />
        <ServicesList services={mockedServices} />
        <IncidentsHistoric incidente={dateDeLaBackend} />
      </main>

      <Footer lastUpdated={timpulCurent} />
      
    </div>
  );
}

export default App
