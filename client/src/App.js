//routing
import { Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import NavBar from './components/NavBar'
import AboutPage from './pages/AboutPage';
import PillAnimation from './components/PillAnimation';

function App() {
  return (
    <div>
      <NavBar />
      <Routes>
        <Route path='/' exact element={<HomePage />} />
        <Route path='/about' element={<AboutPage />}/>
      </Routes>
      <PillAnimation />
    </div>
  );
}

export default App;
