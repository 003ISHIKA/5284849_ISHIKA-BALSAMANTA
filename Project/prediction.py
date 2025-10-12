"""
Skin Cancer Detection - Prediction Script
Load trained model and make predictions on new images
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

class SkinCancerPredictor:
    def __init__(self, model_path, img_size=(224, 224)):
        """
        Initialize predictor with trained model
        
        Args:
            model_path: Path to saved model (.h5 file)
            img_size: Image size expected by model
        """
        self.model = keras.models.load_model(model_path)
        self.img_size = img_size
        
        # Skin cancer class names (update based on your dataset)
        self.class_names = [
            'Actinic keratoses',
            'Basal cell carcinoma',
            'Benign keratosis',
            'Dermatofibroma',
            'Melanoma',
            'Melanocytic nevi',
            'Vascular lesions'
        ]
        
        print(f"Model loaded successfully from {model_path}")
    
    def preprocess_image(self, image_path):
        """
        Preprocess image for prediction
        
        Args:
            image_path: Path to image file
        
        Returns:
            Preprocessed image array
        """
        # Load image
        img = Image.open(image_path).convert('RGB')
        
        # Resize
        img = img.resize(self.img_size)
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array, img
    
    def predict(self, image_path, show_image=True):
        """
        Make prediction on single image
        
        Args:
            image_path: Path to image file
            show_image: Whether to display the image with prediction
        
        Returns:
            Dictionary with prediction results
        """
        # Preprocess image
        img_array, original_img = self.preprocess_image(image_path)
        
        # Make prediction
        predictions = self.model.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx] * 100
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3_predictions = [
            {
                'class': self.class_names[idx],
                'confidence': predictions[0][idx] * 100
            }
            for idx in top_3_idx
        ]
        
        result = {
            'predicted_class': self.class_names[predicted_class_idx],
            'confidence': confidence,
            'top_3': top_3_predictions,
            'all_probabilities': {
                self.class_names[i]: predictions[0][i] * 100 
                for i in range(len(self.class_names))
            }
        }
        
        # Display results
        if show_image:
            self.visualize_prediction(original_img, result)
        
        return result
    
    def visualize_prediction(self, image, result):
        """Display image with prediction results"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Show image
        ax1.imshow(image)
        ax1.axis('off')
        ax1.set_title(f"Predicted: {result['predicted_class']}\nConfidence: {result['confidence']:.2f}%", 
                     fontsize=12, fontweight='bold')
        
        # Show probability distribution
        classes = list(result['all_probabilities'].keys())
        probabilities = list(result['all_probabilities'].values())
        colors = ['red' if p == max(probabilities) else 'skyblue' for p in probabilities]
        
        ax2.barh(classes, probabilities, color=colors)
        ax2.set_xlabel('Confidence (%)', fontsize=11)
        ax2.set_title('Class Probabilities', fontsize=12, fontweight='bold')
        ax2.set_xlim([0, 100])
        
        # Add percentage labels
        for i, (cls, prob) in enumerate(zip(classes, probabilities)):
            ax2.text(prob + 1, i, f'{prob:.1f}%', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.show()
    
    def predict_batch(self, image_folder):
        """
        Make predictions on all images in a folder
        
        Args:
            image_folder: Path to folder containing images
        
        Returns:
            List of prediction results
        """
        results = []
        image_files = [f for f in os.listdir(image_folder) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"\nProcessing {len(image_files)} images...")
        
        for img_file in image_files:
            img_path = os.path.join(image_folder, img_file)
            try:
                result = self.predict(img_path, show_image=False)
                result['filename'] = img_file
                results.append(result)
                print(f"✓ {img_file}: {result['predicted_class']} ({result['confidence']:.2f}%)")
            except Exception as e:
                print(f"✗ Error processing {img_file}: {str(e)}")
        
        return results
    
    def get_risk_assessment(self, predicted_class):
        """
        Get risk assessment for predicted class
        
        Args:
            predicted_class: Name of predicted class
        
        Returns:
            Risk level and recommendation
        """
        high_risk = ['Melanoma', 'Basal cell carcinoma']
        moderate_risk = ['Actinic keratoses', 'Dermatofibroma']
        low_risk = ['Benign keratosis', 'Melanocytic nevi', 'Vascular lesions']
        
        if predicted_class in high_risk:
            return {
                'risk_level': 'HIGH',
                'recommendation': 'Please consult a dermatologist immediately for proper diagnosis and treatment.'
            }
        elif predicted_class in moderate_risk:
            return {
                'risk_level': 'MODERATE',
                'recommendation': 'Schedule an appointment with a dermatologist for evaluation.'
            }
        else:
            return {
                'risk_level': 'LOW',
                'recommendation': 'Monitor the lesion and consult a doctor if you notice any changes.'
            }


# Example usage
if __name__ == "__main__":
    # Initialize predictor
    predictor = SkinCancerPredictor(
        model_path='best_skin_cancer_model.h5',
        img_size=(224, 224)
    )
    
    # Single image prediction
    print("\n=== Single Image Prediction ===")
    image_path = 'test_image.jpg'  # Update with your image path
    
    if os.path.exists(image_path):
        result = predictor.predict(image_path)
        
        print(f"\nPrediction: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        
        print("\nTop 3 Predictions:")
        for i, pred in enumerate(result['top_3'], 1):
            print(f"{i}. {pred['class']}: {pred['confidence']:.2f}%")
        
        # Get risk assessment
        risk = predictor.get_risk_assessment(result['predicted_class'])
        print(f"\nRisk Level: {risk['risk_level']}")
        print(f"Recommendation: {risk['recommendation']}")
    else:
        print(f"Image not found: {image_path}")
    
    # Batch prediction
    # test_folder = 'test_images'
    # if os.path.exists(test_folder):
    #     results = predictor.predict_batch(test_folder)