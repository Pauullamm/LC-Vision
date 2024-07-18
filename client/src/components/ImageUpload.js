// ImageUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import Loader from './Loader';

function ImageUpload() {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [resizedImage, setResizedImage] = useState(null);
  const [outputResponse, setOutputResponse] = useState("");
  const [uploadImage, setUploadImage] = useState(false)

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
    if (event.target.files && event.target.files[0]) {
      let file = event.target.files[0];
      let reader = new FileReader();
      reader.onload = (e) => {
        resizeImage(e.target.result);
      };
      reader.readAsDataURL(file);
    }

  };

  const resizeImage = (dataUrl) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const maxWidth = 200;
      const scaleSize = maxWidth / img.width;
      canvas.width = maxWidth;
      canvas.height = img.height * scaleSize;
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      const resizedDataUrl = canvas.toDataURL('image/jpeg')
      setResizedImage(resizedDataUrl);
    };
    img.onerror = () => {
      alert("Failed to load image. Please try a different file")
    };
    img.src = dataUrl;
  }

  const handleUpload = async () => {
    const formData = new FormData();
    if (!selectedFiles) {
      console.log("Please choose an image first");
      return
    };

    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('images', selectedFiles[i]);
    }
    setUploadImage(true)
    try {
      const port = "https://lc-vision.onrender.com/upload"//process.env.BE_EP
      const response = await axios.post(port, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      const ai_res = response.data.message.choices[0].message.content;
      setUploadImage(false);
      setOutputResponse(ai_res);
      
    } catch (error) {
      console.error('Error uploading images', error);
    }
  };

  return (
    <div class="flex flex-col">
      <h1 class="mt-5 text-gray-300 text-2xl font-bold">Select an image to upload</h1>

      <div class="flex justify-center">
        <div class="flex justify-center py-2 px-2 border-solid border-2 w-max h-max rounded-md mt-5">
          <div class="content-center">
            <input class="text-gray-300" type="file" multiple onChange={handleFileChange} />
          </div>
          <button class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center cursor-pointer" onClick={handleUpload}>Upload</button>
        </div>
        
      </div>
      <div class="flex justify-center">
        
        {resizedImage && <img src={resizedImage} alt="Selected" style={{ marginTop: '20px', maxWidth: '100%' }} />}
      </div>
      {uploadImage && <Loader />}
      |<div class="flex justify-center"><p class="w-1/2 text-gray-300">{outputResponse}</p></div>
      
    </div>
  );
}

export default ImageUpload;
