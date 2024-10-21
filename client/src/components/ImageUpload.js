// ImageUpload.js
import React, { useState } from 'react';
import axios from 'axios';
import Loader from './Loader';
import { useSelector } from 'react-redux';
import ErrorAlert from './ErrorAlert';
import ChatDisplay from './ChatDisplay';
import { GoTrash } from "react-icons/go";


function ImageUpload() {
  const [selectedFiles, setSelectedFiles] = useState(null);
  const [resizedImage, setResizedImage] = useState(null);
  const [outputResponse, setOutputResponse] = useState(["", ""]);
  const [uploadImage, setUploadImage] = useState(false)
  const inputValue = useSelector((state) => state.input.inputValue);
  const [tooltipVisible, setTooltipVisible] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });
  const [errorMessage, setErrorMessage] = useState(null);
  
  const sessionID = useSelector((state) => state.session.sessionID); // get session id as state from navbar
  const handleMouseOver = (event) => {
    if (!inputValue.trim()) {
      setTooltipPosition({ x: event.clientX, y: event.clientY });
      setTooltipVisible(true);
    }
  };

  const handleMouseOut = () => {
    setTooltipVisible(false);
  };

  const clearOutput = () => {
    setOutputResponse(["", ""]);
  };

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
      setErrorMessage("Please choose an image first");
      return
    };

    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append('images', selectedFiles[i]);
      formData.append('sessionID', sessionID);
    }
    setUploadImage(true); //start loading animation
    
    try {
      const port = process.env.REACT_APP_IMG_ENDPOINT //make sure .env is same level as package.json
      const response = await axios.post(port, formData);
      const ai_res = response.data.message.choices[0].message.content;
      setUploadImage(false); //stop loading animation as successful
      setOutputResponse([ai_res, response.data.interpretation]);
      
    } catch (error) {
      console.error('Error uploading images', error);
      setUploadImage(false); //stop loading animation as failed
      setErrorMessage(error.message);
    }
  };

  return (
    <div className="flex flex-col md:min-w-sm items-center">
      <h1 className="mt-5 text-gray-300 text-2xl font-bold text-center">1. Enter your OpenAI API key</h1>
      <h1 className="mt-5 text-gray-300 text-2xl font-bold text-center">2. Select an image to upload</h1>
      <div className="flex justify-center">
        <div className="flex justify-center py-2 px-2 border-solid border-2 w-max h-max rounded-md mt-5">
          <div className="content-center">
            <input className="text-gray-300" type="file" multiple onChange={handleFileChange} />
          </div>
          <button className="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center" 
          style={{ cursor: inputValue.trim() ? 'pointer' : 'not-allowed' }} 
          disabled={!inputValue.trim()} 
          onClick={handleUpload}
          onMouseOver={handleMouseOver}
          onMouseOut={handleMouseOut}
          >Upload</button>

          {tooltipVisible && (
        <div 
          style={{ 
            position: 'absolute', 
            left: `${tooltipPosition.x}px`, 
            top: `${tooltipPosition.y}px`,
            backgroundColor: 'black',
            color: 'white',
            padding: '5px',
            borderRadius: '3px',
            pointerEvents: 'none'
          }}
        >
          Please add your API key first!
        </div>
      )}
        </div>
        
      </div>
      <div className="flex justify-center">
        
        {resizedImage && <img src={resizedImage} alt="Selected" style={{ marginTop: '20px', maxWidth: '100%' }} />}
      </div>
      {}
      {uploadImage && <Loader />}      
        <div className="
          flex 
          flex-col 
          items-center 
          justify-evenly 
          text-center 
          border-solid
          border-2 
          border-gray-300 
          p-5 
          rounded-lg 
          shadow-lg 
          w-full 
          max-w-3xl 
          my-5">
          <div className='flex justify-evenly w-full'>
            <ChatDisplay displayTitle={'AI Description'} outputResponse={outputResponse[0]}/>
            <ChatDisplay displayTitle={'AI Interpretation'} outputResponse={outputResponse[1]}/>
          </div>
          <div className='flex justify-center'>
            <button 
              className="clear-butt mt-4 bg-gray-500 text-white py-2 px-4 rounded items-center text-sm flex"  // Added 'flex' here
              onClick={clearOutput}
            >
              <span className="flex items-center"> {/* This ensures text and icon are aligned */}
                Clear Output <GoTrash className="ml-2" /> {/* Added margin-left for spacing */}
              </span>
            </button>
          </div>


        </div>

      {errorMessage ? <ErrorAlert alertText={errorMessage} /> : null}
    </div>
  );
}

export default ImageUpload;
