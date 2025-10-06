import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # MongoDB
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/NutriScan')
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_HOURS = 24
    
    # Flask
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = FLASK_ENV == 'development'
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # ML Model
    MODEL_PATH = 'ml_models/food_classifier.h5'
    MODEL_LABELS_PATH = 'ml_models/food_labels.txt'
    
    # Health scoring thresholds
    HEALTHY_THRESHOLDS = {
        'calories': 400,
        'sugar': 15,
        'fat': 10,
        'sodium': 500
    }
    
    MODERATE_THRESHOLDS = {
        'calories': 600,
        'sugar': 25,
        'fat': 20,
        'sodium': 1000
    }
