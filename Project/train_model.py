"""
Skin Cancer Detection using Deep Learning
This script trains a CNN model to classify skin lesions
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import os

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

class SkinCancerDetector:
    def __init__(self, img_size=(224, 224), num_classes=7):
        """
        Initialize the skin cancer detector
        
        Args:
            img_size: Input image size (height, width)
            num_classes: Number of skin cancer types to classify
        """
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.history = None
        
    def create_model(self, use_pretrained=True):
        """
        Create the CNN model
        
        Args:
            use_pretrained: If True, use transfer learning with MobileNetV2
        """
        if use_pretrained:
            # Transfer Learning with MobileNetV2
            base_model = MobileNetV2(
                input_shape=(*self.img_size, 3),
                include_top=False,
                weights='imagenet'
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Add custom classification head
            self.model = models.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.Dropout(0.3),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(self.num_classes, activation='softmax')
            ])
        else:
            # Simple CNN from scratch
            self.model = models.Sequential([
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.img_size, 3)),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(128, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(self.num_classes, activation='softmax')
            ])
        
        # Compile model
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("Model created successfully!")
        self.model.summary()
        
    def prepare_data(self, train_dir, val_dir, batch_size=32):
        """
        Prepare data generators with augmentation
        
        Args:
            train_dir: Path to training data directory
            val_dir: Path to validation data directory
            batch_size: Batch size for training
        """
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create generators
        self.train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=True
        )
        
        self.val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
        print(f"Training samples: {self.train_generator.samples}")
        print(f"Validation samples: {self.val_generator.samples}")
        print(f"Classes: {list(self.train_generator.class_indices.keys())}")
        
        return self.train_generator, self.val_generator
    
    def train(self, epochs=20, save_path='skin_cancer_model.h5'):
        """
        Train the model
        
        Args:
            epochs: Number of training epochs
            save_path: Path to save the best model
        """
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                save_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train model
        self.history = self.model.fit(
            self.train_generator,
            validation_data=self.val_generator,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        
        print(f"\nTraining completed! Best model saved to {save_path}")
        return self.history
    
    def plot_training_history(self):
        """Plot training and validation accuracy/loss"""
        if self.history is None:
            print("No training history available!")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Accuracy plot
        ax1.plot(self.history.history['accuracy'], label='Train Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Val Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.history.history['loss'], label='Train Loss')
        ax2.plot(self.history.history['val_loss'], label='Val Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Training history plot saved as 'training_history.png'")
    
    def evaluate(self, test_dir):
        """Evaluate model on test data"""
        test_datagen = ImageDataGenerator(rescale=1./255)
        test_generator = test_datagen.flow_from_directory(
            test_dir,
            target_size=self.img_size,
            batch_size=32,
            class_mode='categorical',
            shuffle=False
        )
        
        loss, accuracy = self.model.evaluate(test_generator)
        print(f"\nTest Accuracy: {accuracy*100:.2f}%")
        print(f"Test Loss: {loss:.4f}")
        
        return loss, accuracy


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = SkinCancerDetector(img_size=(224, 224), num_classes=7)
    
    # Create model (using transfer learning for better results)
    detector.create_model(use_pretrained=True)
    
    # Prepare data (update these paths to your dataset location)
    train_dir = 'dataset/train'
    val_dir = 'dataset/validation'
    
    detector.prepare_data(train_dir, val_dir, batch_size=32)
    
    # Train model
    detector.train(epochs=20, save_path='best_skin_cancer_model.h5')
    
    # Plot training history
    detector.plot_training_history()
    
    # Evaluate on test set (if available)
    # test_dir = 'dataset/test'
    # detector.evaluate(test_dir)