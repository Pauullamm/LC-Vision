import React from 'react';
import Lottie from 'react-lottie';
import * as animationData from '../assets/animation.json'

const PillAnimation = () => {
  const defaultOptions = {
    loop: true,
    autoplay: true, 
    animationData: animationData,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice'
    }
  };
  return (
    <div className='animation-background'>
      <div className='animation-container'>
        <Lottie 
          options={defaultOptions}
        />
      </div>
    </div>
  );
};

export default PillAnimation;
