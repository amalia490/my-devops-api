import './App.css'
import { DashBoard } from './pages/DashBoard';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { ChannelPage } from './pages/ChannelPage';
import { Header } from './components/Header';
import { Footer} from './components/Footer';

function App() {
  return (
    <BrowserRouter>
    <Header/>
      <Routes>
        <Route path="/" element={<DashBoard />} />
        <Route path="/canal/:idAndName" element={<ChannelPage />} />
      </Routes>
      <Footer lastUpdated= {new Date().toLocaleString('ro-RO')}/>
    </BrowserRouter>
  );
}

export default App
