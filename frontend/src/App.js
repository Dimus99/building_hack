import InputForm from "./components/Main/Main";
import './App.css';
import FileUpload from "./components/FileUploader/FileUploader";
import {useState} from "react";

function App() {

  const [isUploadFileView, setIsUploadFileView] = useState(false);

  return (
    <div className="App">
      <div className='tabs'>
          <div className={`tab ${!isUploadFileView ? 'tab__active' : ''}`} onClick={() => setIsUploadFileView(false)}>
            Ручной ввод
          </div>
          <div className={`tab ${isUploadFileView ? 'tab__active' : ''}`} onClick={() => setIsUploadFileView(true)}>
            Загрузка Excel файла
          </div>
        </div>
      <div className="container">


        {
          isUploadFileView ? <FileUpload/> : <InputForm/>
        }
      </div>

    </div>
  );
}

export default App;
