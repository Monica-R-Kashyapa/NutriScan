import React, { useState, useRef } from 'react';
import { Camera, Upload, X, CheckCircle, AlertCircle } from 'lucide-react';
import { foodAPI } from '../services/api';
import CameraCapture from '../components/CameraCapture';
import './Scanner.css';

function Scanner() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [showCamera, setShowCamera] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResult(null);
      setError('');
    }
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleScan = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setScanning(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('image', selectedFile);

      const response = await foodAPI.scanFood(formData);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to scan food. Please try again.');
    } finally {
      setScanning(false);
    }
  };

  const handleCameraCapture = (file, imageUrl) => {
    console.log('Camera capture received:', file?.name, file?.size);
    setSelectedFile(file);
    setPreview(imageUrl);
    setResult(null);
    setError('');
    setShowCamera(false);
  };

  const openCamera = () => {
    setShowCamera(true);
  };

  const closeCamera = () => {
    setShowCamera(false);
  };

  const getHealthBadge = (status) => {
    const badges = {
      healthy: { emoji: '✅', text: 'Healthy', class: 'healthy', icon: CheckCircle },
      moderate: { emoji: '⚠️', text: 'Moderately Healthy', class: 'moderate', icon: AlertCircle },
      unhealthy: { emoji: '❌', text: 'Unhealthy', class: 'unhealthy', icon: AlertCircle },
    };
    return badges[status] || badges.moderate;
  };

  return (
    <div className="scanner">
      <div className="container">
        <div className="scanner-header">
          <h1>🔍 Scan Your Food</h1>
          <p>Upload or capture a photo to analyze nutrition and health score</p>
        </div>

        <div className="scanner-grid">
          {/* Upload Section */}
          <div className="card upload-section">
            <h2>Upload or Capture Image</h2>
            
            {!preview ? (
              <>
                <div className="upload-area" onClick={() => fileInputRef.current?.click()}>
                  <Upload size={64} color="#d1d5db" />
                  <h3>Click to upload image</h3>
                  <p>Supports: JPG, PNG, JPEG, GIF, WEBP</p>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                  />
                </div>
                
                <div className="or-divider">
                  <span>OR</span>
                </div>
                
                <button onClick={openCamera} className="btn btn-primary btn-block camera-btn">
                  <Camera size={20} />
                  Use Camera
                </button>
              </>
            ) : (
              <div className="preview-area">
                <img src={preview} alt="Preview" className="preview-image" />
                <button onClick={handleClearFile} className="clear-btn">
                  <X size={20} />
                </button>
              </div>
            )}

            {error && (
              <div className="alert alert-error">
                <AlertCircle size={20} />
                {error}
              </div>
            )}

            <button
              onClick={handleScan}
              className="btn btn-primary btn-block"
              disabled={!selectedFile || scanning}
            >
              {scanning ? (
                <>
                  <div className="spinner-small"></div>
                  Analyzing...
                </>
              ) : (
                <>
                  <Camera size={20} />
                  Scan Food
                </>
              )}
            </button>
          </div>

          {/* Results Section */}
          <div className="card results-section">
            <h2>Analysis Results</h2>
            
            {!result ? (
              <div className="empty-results">
                <Upload size={64} color="#d1d5db" />
                <p>Upload and scan an image to see results</p>
              </div>
            ) : (
              <div className="results-content">
                {/* Food Name */}
                <div className="result-header">
                  <h3>{result.food_name}</h3>
                  <span className="confidence-badge">
                    {Math.round(result.confidence * 100)}% confident
                  </span>
                </div>

                {/* Health Score */}
                <div className="health-score-section">
                  <div className={`health-badge large ${getHealthBadge(result.health_score.status).class}`}>
                    <span className="badge-emoji">{getHealthBadge(result.health_score.status).emoji}</span>
                    <div>
                      <div className="badge-text">{getHealthBadge(result.health_score.status).text}</div>
                      <div className="badge-score">Score: {result.health_score.score}/100</div>
                    </div>
                  </div>
                </div>

                {/* Nutrition Facts */}
                <div className="nutrition-section">
                  <h4>Nutrition Facts</h4>
                  <div className="nutrition-grid">
                    <div className="nutrition-item">
                      <span className="nutrition-label">Calories</span>
                      <span className="nutrition-value">{result.nutrition.calories} kcal</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Protein</span>
                      <span className="nutrition-value">{result.nutrition.protein}g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Carbs</span>
                      <span className="nutrition-value">{result.nutrition.carbs}g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Fat</span>
                      <span className="nutrition-value">{result.nutrition.fat}g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Sugar</span>
                      <span className="nutrition-value">{result.nutrition.sugar}g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Fiber</span>
                      <span className="nutrition-value">{result.nutrition.fiber}g</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Sodium</span>
                      <span className="nutrition-value">{result.nutrition.sodium}mg</span>
                    </div>
                    <div className="nutrition-item">
                      <span className="nutrition-label">Serving</span>
                      <span className="nutrition-value">{result.nutrition.serving_size}</span>
                    </div>
                  </div>
                </div>

                {/* Reasons */}
                {result.health_score.reasons && result.health_score.reasons.length > 0 && (
                  <div className="reasons-section">
                    <h4>Analysis</h4>
                    <ul className="reasons-list">
                      {result.health_score.reasons.map((reason, index) => (
                        <li key={index}>{reason}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Recommendations */}
                {result.health_score.recommendations && result.health_score.recommendations.length > 0 && (
                  <div className="recommendations-section">
                    <h4>💡 Recommendations</h4>
                    <ul className="recommendations-list">
                      {result.health_score.recommendations.map((rec, index) => (
                        <li key={index}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Alternatives */}
                {result.alternatives && result.alternatives.length > 0 && (
                  <div className="alternatives-section">
                    <h4>🥗 Healthier Alternatives</h4>
                    <div className="alternatives-list">
                      {result.alternatives.map((alt, index) => (
                        <div key={index} className="alternative-item">
                          <CheckCircle size={16} color="#10b981" />
                          <span>{alt}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Camera Modal */}
      {showCamera && (
        <CameraCapture
          onCapture={handleCameraCapture}
          onClose={closeCamera}
        />
      )}
    </div>
  );
}

export default Scanner;
