import React, { useState } from 'react';

const ImageUpload = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const handleImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      const reader = new FileReader();
      reader.onload = (e) => setSelectedImage(e.target.result);
      reader.readAsDataURL(event.target.files[0]);
      setIsUploading(true);
      setUploadMessage(''); // Clear previous messages
    }
  };

  const handleSubmit = async () => {
    if (!selectedImage) {
      setUploadMessage('Please select an image to upload');
      return;
    }

    setIsUploading(true);
    const port = process.env.BE_EP
    try {
      const response = await fetch(port, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: selectedImage }),
      });

      const data = await response.json();
      setUploadMessage(data.message); // Display success or error message
    } catch (error) {
      console.error('Error uploading image:', error);
      setUploadMessage('An error occurred during upload. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleImageChange} disabled={isUploading} />
      <button type="button" onClick={handleSubmit} disabled={isUploading}>
        {isUploading ? 'Uploading...' : 'Upload Image'}
      </button>
      {uploadMessage && <p>{uploadMessage}</p>}
    </div>
  );
};

export default ImageUpload;
