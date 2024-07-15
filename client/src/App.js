import './App.css';
import ImageUpload from './components/ImageUpload';
import NavBar from './components/NavBar';

function App() {
  return (
    <div className="App">
      <NavBar />
      <h1 className="text-3xl font-bold underline"></h1>
      <ImageUpload />
    </div>
  );
}

export default App;
