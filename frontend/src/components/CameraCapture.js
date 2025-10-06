import React, { useRef, useState, useEffect } from 'react';
import { Camera, X, RotateCw, CheckCircle } from 'lucide-react';
import './CameraCapture.css';

function CameraCapture({ onCapture, onClose }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [stream, setStream] = useState(null);
  const [error, setError] = useState('');
  const [facingMode, setFacingMode] = useState('environment'); // 'user' for front, 'environment' for back
  const [capturedImage, setCapturedImage] = useState(null);
  const [capturedFile, setCapturedFile] = useState(null);

  useEffect(() => {
    startCamera();
    return () => {
      stopCamera();
    };
  }, [facingMode]);

  const startCamera = async () => {
    try {
      setError('');
      
      // Stop existing stream
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }

      // Request camera access
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: facingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });

      setStream(mediaStream);
      
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error('Camera error:', err);
      setError('Unable to access camera. Please check permissions.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) {
      console.error('Video or canvas ref not available');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    // Set canvas size to video size
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Draw video frame to canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert to blob
    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
        const imageUrl = URL.createObjectURL(blob);
        console.log('Photo captured:', file.size, 'bytes');
        setCapturedImage(imageUrl);
        setCapturedFile(file); // Store the file
        
        // Stop camera after capture
        stopCamera();
      } else {
        console.error('Failed to create blob from canvas');
      }
    }, 'image/jpeg', 0.95);
  };

  const retakePhoto = () => {
    setCapturedImage(null);
    setCapturedFile(null);
    startCamera();
  };

  const confirmPhoto = () => {
    if (!capturedFile || !capturedImage) {
      console.error('No captured file or image');
      setError('Failed to process captured image. Please try again.');
      return;
    }

    console.log('Confirming photo:', capturedFile.name, capturedFile.size);
    // Send the captured file and image URL to parent
    onCapture(capturedFile, capturedImage);
    handleClose();
  };

  const switchCamera = () => {
    setFacingMode(prev => prev === 'user' ? 'environment' : 'user');
  };

  const handleClose = () => {
    stopCamera();
    onClose();
  };

  return (
    <div className="camera-modal">
      <div className="camera-container">
        <div className="camera-header">
          <h2>📸 Scan Food with Camera</h2>
          <button onClick={handleClose} className="close-camera-btn">
            <X size={24} />
          </button>
        </div>

        {error && (
          <div className="camera-error">
            <p>{error}</p>
            <button onClick={startCamera} className="btn btn-secondary">
              Try Again
            </button>
          </div>
        )}

        <div className="camera-view">
          {!capturedImage ? (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="camera-video"
              />
              <canvas ref={canvasRef} style={{ display: 'none' }} />
              
              <div className="camera-overlay">
                <div className="camera-frame">
                  <div className="corner top-left"></div>
                  <div className="corner top-right"></div>
                  <div className="corner bottom-left"></div>
                  <div className="corner bottom-right"></div>
                </div>
                <p className="camera-hint">Position food within the frame</p>
              </div>
            </>
          ) : (
            <div className="captured-preview">
              <img src={capturedImage} alt="Captured" className="preview-image" />
            </div>
          )}
        </div>

        <div className="camera-controls">
          {!capturedImage ? (
            <>
              <button onClick={switchCamera} className="btn btn-secondary camera-control-btn">
                <RotateCw size={20} />
                <span>Flip</span>
              </button>
              
              <button onClick={capturePhoto} className="btn btn-primary capture-btn">
                <Camera size={32} />
              </button>
              
              <div className="camera-control-btn"></div> {/* Spacer */}
            </>
          ) : (
            <>
              <button onClick={retakePhoto} className="btn btn-secondary">
                <RotateCw size={20} />
                Retake
              </button>
              
              <button onClick={confirmPhoto} className="btn btn-success">
                <CheckCircle size={20} />
                Use Photo
              </button>
            </>
          )}
        </div>

        <div className="camera-tips">
          <p>💡 Tips for best results:</p>
          <ul>
            <li>Ensure good lighting</li>
            <li>Center the food in frame</li>
            <li>Avoid shadows and glare</li>
            <li>Hold camera steady</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default CameraCapture;
