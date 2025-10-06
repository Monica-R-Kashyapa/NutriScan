import React from 'react';
import './LoadingAnimation.css';

function LoadingAnimation({ message = 'Loading...' }) {
  return (
    <div className="loading-container">
      <div className="loading-spinner-wrapper">
        <div className="loading-spinner">
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-ring"></div>
          <div className="spinner-food-icon">🍎</div>
        </div>
      </div>
      <p className="loading-message">{message}</p>
    </div>
  );
}

export default LoadingAnimation;
