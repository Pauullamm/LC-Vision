import './App.css';
import ImageUpload from './components/ImageUpload';
import NavBar from './components/NavBar';
import Loader from './components/Loader';

function App() {
  return (
    <div className="App">
      <NavBar />
      
      <ImageUpload />
      <Loader />
    </div>
  );
}

export default App;
