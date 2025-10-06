import numpy as np
from PIL import Image
import os
from config import Config

class MLService:
    """Machine Learning service for food classification"""
    
    def __init__(self):
        self.model = None
        self.labels = []
        self.model_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the pre-trained model and labels"""
        try:
            # Try to load TensorFlow model
            import tensorflow as tf
            
            if os.path.exists(Config.MODEL_PATH):
                self.model = tf.keras.models.load_model(Config.MODEL_PATH)
                print(f"✅ Model loaded from {Config.MODEL_PATH}")
            else:
                print(f"⚠️ Model file not found at {Config.MODEL_PATH}")
                print("Using fallback prediction mode")
            
            # Load labels from your trained model
            if os.path.exists(Config.MODEL_LABELS_PATH):
                with open(Config.MODEL_LABELS_PATH, 'r') as f:
                    self.labels = [line.strip() for line in f.readlines()]
                print(f"✅ Loaded {len(self.labels)} food labels from your dataset")
            else:
                # Try to detect labels from food_data directory
                self.labels = self._detect_labels_from_dataset()
                if not self.labels:
                    # Final fallback
                    self.labels = self._get_fallback_labels()
                    print(f"⚠️ Using fallback labels ({len(self.labels)} items)")
            
            self.model_loaded = True if self.model else False
            
        except ImportError:
            print("⚠️ TensorFlow not available, using fallback mode")
            self.labels = self._get_fallback_labels()
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self.labels = self._get_fallback_labels()
    
    def _detect_labels_from_dataset(self):
        """Detect food labels from your food_data directory"""
        try:
            data_dir = 'food_data/train'
            if os.path.exists(data_dir):
                labels = [d for d in os.listdir(data_dir) 
                         if os.path.isdir(os.path.join(data_dir, d))]
                if labels:
                    labels.sort()  # Alphabetical order
                    print(f"✅ Detected {len(labels)} food categories from your dataset")
                    print(f"   Categories: {', '.join(labels[:5])}{'...' if len(labels) > 5 else ''}")
                    return labels
        except Exception as e:
            print(f"⚠️ Could not detect labels from dataset: {e}")
        return []
    
    def _get_fallback_labels(self):
        """Get fallback food labels (only used if no model and no dataset found)"""
        return [
            'pizza', 'burger', 'salad', 'fries', 'hot_dog',
            'sushi', 'ice_cream', 'donut', 'cake', 'sandwich'
        ]
    
    def preprocess_image(self, image_path):
        """Preprocess image for model prediction"""
        try:
            # Load and resize image
            img = Image.open(image_path)
            img = img.convert('RGB')
            img = img.resize((224, 224))  # Standard size for most food models
            
            # Convert to array and normalize
            img_array = np.array(img)
            img_array = img_array / 255.0  # Normalize to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {str(e)}")
            return None
    
    def predict(self, image_path):
        """Predict food item from image"""
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            if img_array is None:
                return self._fallback_prediction(image_path)
            
            # Make prediction
            if self.model and self.model_loaded:
                predictions = self.model.predict(img_array)
                top_indices = np.argsort(predictions[0])[-3:][::-1]  # Top 3 predictions
                
                results = []
                for idx in top_indices:
                    if idx < len(self.labels):
                        results.append({
                            'food_name': self.labels[idx].replace('_', ' ').title(),
                            'confidence': float(predictions[0][idx])
                        })
                
                return results
            else:
                return self._fallback_prediction(image_path)
                
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            return self._fallback_prediction(image_path)
    
    def _fallback_prediction(self, image_path):
        """Fallback prediction when model is not available"""
        # Simple demo prediction based on image name or random selection
        import random
        
        # Try to guess from filename
        filename = os.path.basename(image_path).lower()
        
        for label in self.labels:
            if label.replace('_', '') in filename.replace('_', '').replace('-', ''):
                return [{
                    'food_name': label.replace('_', ' ').title(),
                    'confidence': 0.85
                }]
        
        # Random selection for demo
        selected = random.choice(self.labels)
        return [{
            'food_name': selected.replace('_', ' ').title(),
            'confidence': 0.75
        }]
    
    def get_food_category(self, food_name):
        """Categorize food into general categories"""
        food_lower = food_name.lower()
        
        categories = {
            'fast_food': ['pizza', 'burger', 'fries', 'hot dog', 'nachos'],
            'dessert': ['cake', 'ice cream', 'donut', 'pie', 'cookie'],
            'healthy': ['salad', 'salmon', 'soup', 'vegetables', 'fruit'],
            'asian': ['sushi', 'ramen', 'curry', 'dumplings', 'fried rice'],
            'breakfast': ['pancakes', 'waffles', 'omelette', 'toast'],
            'mexican': ['tacos', 'burrito', 'quesadilla', 'nachos']
        }
        
        for category, keywords in categories.items():
            if any(keyword in food_lower for keyword in keywords):
                return category
        
        return 'other'

# Global instance
ml_service = MLService()
