import React, { useState } from 'react';
import axios from 'axios';
import '../../App.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleFileRemove = () => {
    setFile(null);
  };

  const handleFileUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/uploadfile/', formData);
      console.log(response.data)
    } catch (error) {
    }
  };

  return (
    <div className='file-uploader'>
      <label htmlFor="file-upload" className="custom-file-upload">
        Select File
      </label>
      <input id="file-upload" type="file" onChange={handleFileChange} />

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
    </div>
  );
};

export default FileUpload;
