import React, {useState} from 'react';
import axios from 'axios';
import '../../App.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [predicts, setPredicts] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileRemove = () => {
    setFile(null);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    setError(null)

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://goliaf-team.ru:8000/uploadfile/', formData);
      if (response.data?.error) {
        setError(response.data.error)
      }

      setPredicts(response?.data || [])
    } catch (error) {
      setError(error.message)
    }


    setIsLoading(false)
    setFile(null)
  };

  if (isLoading) return (
    <div>Loading...</div>
  )

  return (
    <div className='file-uploader'>
      <label htmlFor="file-upload" className="custom-file-upload">
        Excel файл
      </label>
      <input id="file-upload" type="file" onChange={handleFileChange}/>

      {file && (
        <div>
          <span>{file.name}</span>
          <span style={{
            display: "inline-block",
            marginLeft: "10px",
            marginTop: "10px",
            marginBottom: "10px",
            cursor: "pointer",
            border: "1px solid black",
            borderRadius: "50px",
            width: "22px",
            height: "22px",
            backgroundColor: "#ff8888",
          }} onClick={handleFileRemove}>x</span>
        </div>
      )}

      <button className={`${!file && "button__disabled"}`} onClick={handleFileUpload}>Рассчитать срок</button>
      {
        error && <div style={{color: "red", paddingTop: "20px"}}>{error}</div>
      }

      {
        predicts ? predicts?.map((predict, index) => {
          return (
            <div key={index}>
              <p>Название задачи: {predict.name}</p>
              <p>Дата начала: {predict.task_start_date}</p>
              <p>Дата окончания: {predict.predict}</p>
            </div>
          )
        }) : <></>
      }

    </div>
  );
};

export default FileUpload;
