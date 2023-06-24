import React, {useState} from 'react';
import axios from 'axios';

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState('');

  const onChange = (e) => {
    setFile(e.target.files[0]);
    setFilename(e.target.files[0].name);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post('API_URL', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    console.log(response.data);
  };

  return (
    <form onSubmit={onSubmit}>
      <br/>
      <div>
        <input type="file" onChange={onChange} />
      </div>
      <br/>
      <div>
        <button type="submit">Upload</button>
      </div>
    </form>
  );
};

export default FileUploader;