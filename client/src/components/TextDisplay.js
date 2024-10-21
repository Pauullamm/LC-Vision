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
    }, 20);

    return () => clearInterval(interval);
  }, [outputResponse]);

  const lines = displayedText.split('---').map((line, idx) => (
    <React.Fragment key={idx}>
    <span style={{ color: 'white' }}>{line.trim()}</span>
      <br />
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
