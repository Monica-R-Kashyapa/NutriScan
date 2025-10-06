"""
Quick Training Script - Uses transfer learning for fast training
Works with your custom food_data dataset
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers

# Configuration
IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 5  # Quick training
DATA_DIR = 'food_data'  # Your custom dataset directory

def create_simple_model(num_classes):
    """
    Create a simple transfer learning model
    """
    print("🏗️  Creating model with transfer learning...")
    
    # Use MobileNetV2 pre-trained on ImageNet
    base_model = MobileNetV2(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom head
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.2),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_quick():
    """
    Quick training with your custom food_data dataset
    """
    print("=" * 60)
    print("🚀 Quick Training Mode - Using Your Custom Dataset")
    print("=" * 60)
    
    # Check for data
    if not os.path.exists(f'{DATA_DIR}/train'):
        print(f"\n❌ Dataset not found at '{DATA_DIR}/train'!")
        print("\n📁 Expected structure:")
        print(f"   {DATA_DIR}/")
        print("     train/")
        print("       [your_food_category_1]/")
        print("         image1.jpg")
        print("         image2.jpg")
        print("       [your_food_category_2]/")
        print("         image1.jpg")
        print("     validation/")
        print("       [your_food_category_1]/")
        print("         image1.jpg")
        print("       [your_food_category_2]/")
        print("         image1.jpg")
        print(f"\n💡 Make sure your images are in '{DATA_DIR}/' folder!")
        return
    
    # Create data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    print("\n📁 Loading your dataset...")
    train_gen = train_datagen.flow_from_directory(
        f'{DATA_DIR}/train',
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    val_gen = val_datagen.flow_from_directory(
        f'{DATA_DIR}/validation',
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    num_classes = len(train_gen.class_indices)
    class_names = list(train_gen.class_indices.keys())
    
    print(f"\n✅ Dataset loaded:")
    print(f"   Classes: {num_classes}")
    print(f"   Class names: {class_names}")
    print(f"   Training samples: {train_gen.samples}")
    print(f"   Validation samples: {val_gen.samples}")
    
    # Build model
    model = create_simple_model(num_classes)
    print("\n✅ Model created!")
    
    # Train
    print(f"\n🚀 Training for {EPOCHS} epochs...")
    print("   (This should take 5-10 minutes)")
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=EPOCHS,
        verbose=1
    )
    
    # Save model
    os.makedirs('ml_models', exist_ok=True)
    model.save('ml_models/food_classifier.h5')
    print("\n✅ Model saved: ml_models/food_classifier.h5")
    
    # Save labels
    with open('ml_models/food_labels.txt', 'w') as f:
        for label in class_names:
            f.write(f"{label}\n")
    print("✅ Labels saved: ml_models/food_labels.txt")
    
    # Final accuracy
    val_loss, val_acc = model.evaluate(val_gen, verbose=0)
    print(f"\n📊 Final Validation Accuracy: {val_acc*100:.2f}%")
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print("=" * 60)
    print("\n💡 Next steps:")
    print("1. Restart the backend server")
    print("2. The app will use your trained model")
    print("3. Test with real food images!")
    
    if val_acc < 0.7:
        print("\n⚠️  Accuracy is low. To improve:")
        print("   - Add more training images (50-100 per category)")
        print("   - Train for more epochs (10-20)")
        print("   - Add more diverse images")

if __name__ == "__main__":
    train_quick()
