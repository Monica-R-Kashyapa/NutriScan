# ML Models Directory

## Food Classifier Model

This directory should contain the trained food classification model.

### Model File
- `food_classifier.h5` - Pre-trained Keras/TensorFlow model for food recognition

### Getting a Pre-trained Model

You have several options:

#### Option 1: Use Food-101 Dataset Model
Download a pre-trained model from:
- https://www.kaggle.com/models
- https://github.com/stratospark/food-101-keras

#### Option 2: Train Your Own Model
```python
# Example training script
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# Load base model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Add custom layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(30, activation='softmax')(x)  # 30 food classes

model = Model(inputs=base_model.input, outputs=predictions)

# Compile and train
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# model.fit(train_data, epochs=10)

# Save model
model.save('food_classifier.h5')
```

#### Option 3: Use Fallback Mode (Current)
The application currently runs in fallback mode, which uses a simple prediction system based on filename matching and random selection from the labels list. This is sufficient for development and testing.

### Model Requirements
- Input: 224x224 RGB images
- Output: Softmax probabilities for 30 food classes
- Format: Keras/TensorFlow .h5 file

### Labels
The `food_labels.txt` file contains the list of food categories the model can recognize. Update this file if you train a model with different categories.
