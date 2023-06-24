import InputForm from "./components/Main/Main";
import FileUploader from "./components/FileUploader/FileUploader";
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="container">
        <InputForm/>
        <FileUploader/>
      </div>

    </div>
  );
}

export default App;
