import React, { useEffect, useState } from 'react';

const ChatDisplay = ({ displayTitle, outputResponse }) => {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    const textToDisplay = outputResponse;

    let index = 0;

    const interval = setInterval(() => {
      if (index < textToDisplay.length) {
        setDisplayedText((prev) => prev + textToDisplay[index]);
        index++;
      } else {
        clearInterval(interval);
      }
    }, 20); // Adjust the interval for speed (100ms in this example)

    return () => clearInterval(interval); // Cleanup on unmount
  }, [outputResponse]);

  // Split the displayed text into lines and render with <br /> for line breaks
  const lines = displayedText.split('---').map((line, idx) => (
    <React.Fragment key={idx}>
      {line.trim()}
      <br />
    </React.Fragment>
  ));

  return (
    <div className='mx-5 text-center w-full'>
      <h4 className="text-gray-300 text-xl font-bold">{displayTitle}</h4>
      {lines}
    </div>
  );
};

export default ChatDisplay;
