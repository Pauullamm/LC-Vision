// ImageUpload.js
import React, { useState } from 'react';
import axios from 'axios';

function ImageUpload() {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [base64Images, setBase64Images] = useState([]);

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('images', selectedFiles[i]);
    }

    try {
      const port = process.env.BE_EP
      const response = await axios.post(`${port}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Response:', response);
      setBase64Images(response.data.base64_images);
    } catch (error) {
      console.error('Error uploading images', error);
    }
  };

  return (
    <div>
      <h1>Image Upload</h1>
      <input type="file" multiple onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {base64Images.length > 0 && (
        <div>
          <h2>Base64 Images</h2>
          {base64Images.map((base64, index) => (
            <img key={index} src={`data:image/jpeg;base64,${base64}`} alt={`Uploaded ${index}`} />
          ))}
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
