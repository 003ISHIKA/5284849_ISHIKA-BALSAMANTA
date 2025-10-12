"""
Script to download and organize skin cancer dataset
This will help you get started quickly!
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import shutil

def create_folder_structure():
    """Create necessary folders for the project"""
    
    folders = [
        'dataset/train',
        'dataset/validation',
        'dataset/test',
        'models',
        'test_images'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Created: {folder}")
    
    print("\n✅ Folder structure created successfully!")
    print("\nYour project structure:")
    print("""
    skin_cancer_detection/
    ├── dataset/
    │   ├── train/
    │   ├── validation/
    │   └── test/
    ├── models/
    └── test_images/
    """)

def organize_ham10000_dataset(csv_path, images_folder):
    """
    Organize HAM10000 dataset into train/val/test folders
    
    Args:
        csv_path: Path to HAM10000_metadata.csv
        images_folder: Path to folder containing all images
    """
    
    print("\n📁 Organizing HAM10000 dataset...")
    
    # Read metadata
    df = pd.read_csv(csv_path)
    print(f"Total images: {len(df)}")
    
    # Map diagnosis codes to full names
    dx_mapping = {
        'akiec': 'actinic_keratoses',
        'bcc': 'basal_cell_carcinoma',
        'bkl': 'benign_keratosis',
        'df': 'dermatofibroma',
        'mel': 'melanoma',
        'nv': 'melanocytic_nevi',
        'vasc': 'vascular_lesions'
    }
    
    # Create class folders
    for split in ['train', 'validation', 'test']:
        for class_name in dx_mapping.values():
            os.makedirs(f'dataset/{split}/{class_name}', exist_ok=True)
    
    # Split data: 70% train, 15% validation, 15% test
    from sklearn.model_selection import train_test_split
    
    train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df['dx'])
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['dx'])
    
    print(f"\nTrain samples: {len(train_df)}")
    print(f"Validation samples: {len(val_df)}")
    print(f"Test samples: {len(test_df)}")
    
    # Copy images to respective folders
    def copy_images(dataframe, split):
        print(f"\n📋 Copying {split} images...")
        for idx, row in dataframe.iterrows():
            image_id = row['image_id']
            diagnosis = dx_mapping[row['dx']]
            
            # Try both .jpg extensions
            src_path = None
            for ext in ['.jpg', '.JPG']:
                potential_path = os.path.join(images_folder, image_id + ext)
                if os.path.exists(potential_path):
                    src_path = potential_path
                    break
            
            if src_path:
                dst_path = f'dataset/{split}/{diagnosis}/{image_id}.jpg'
                shutil.copy2(src_path, dst_path)
                
                if (idx + 1) % 1000 == 0:
                    print(f"  Processed {idx + 1}/{len(dataframe)} images...")
            else:
                print(f"  Warning: Image not found - {image_id}")
        
        print(f"✅ {split.capitalize()} images copied!")
    
    copy_images(train_df, 'train')
    copy_images(val_df, 'validation')
    copy_images(test_df, 'test')
    
    # Print class distribution
    print("\n📊 Class Distribution:")
    print("\nTraining Set:")
    print(train_df['dx'].value_counts())
    
    print("\n✅ Dataset organization complete!")
    print("\nYou can now run the training script!")

def check_dataset_ready():
    """Check if dataset is properly organized"""
    
    print("\n🔍 Checking dataset...")
    
    required_classes = [
        'actinic_keratoses',
        'basal_cell_carcinoma',
        'benign_keratosis',
        'dermatofibroma',
        'melanoma',
        'melanocytic_nevi',
        'vascular_lesions'
    ]
    
    issues = []
    
    for split in ['train', 'validation']:
        split_path = f'dataset/{split}'
        if not os.path.exists(split_path):
            issues.append(f"Missing folder: {split_path}")
            continue
        
        for class_name in required_classes:
            class_path = f'{split_path}/{class_name}'
            if not os.path.exists(class_path):
                issues.append(f"Missing class folder: {class_path}")
            else:
                image_count = len([f for f in os.listdir(class_path) 
                                 if f.endswith(('.jpg', '.jpeg', '.png'))])
                print(f"✓ {split}/{class_name}: {image_count} images")
                
                if image_count == 0:
                    issues.append(f"No images in: {class_path}")
    
    if issues:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\n✅ Dataset is ready for training!")
        return True

def download_sample_images():
    """
    Download a few sample images for testing
    This is useful if you want to test the system before full training
    """
    print("\n📥 Downloading sample images...")
    print("Note: You'll need to manually download these from:")
    print("https://www.isic-archive.com/")
    print("\nOr use the HAM10000 dataset from Kaggle.")
    print("\nFor quick testing, you can use any skin lesion images from Google Images")
    print("and place them in the 'test_images' folder.")

# ============================================
# MAIN MENU
# ============================================

def main():
    print("="*60)
    print("  SKIN CANCER DETECTION - DATASET SETUP")
    print("="*60)
    
    while True:
        print("\n\nWhat would you like to do?")
        print("1. Create folder structure")
        print("2. Organize HAM10000 dataset (if you have it)")
        print("3. Check if dataset is ready")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            create_folder_structure()
            
        elif choice == '2':
            csv_path = input("\nEnter path to HAM10000_metadata.csv: ").strip()
            images_folder = input("Enter path to images folder: ").strip()
            
            if os.path.exists(csv_path) and os.path.exists(images_folder):
                organize_ham10000_dataset(csv_path, images_folder)
            else:
                print("❌ Invalid paths! Please check and try again.")
                
        elif choice == '3':
            check_dataset_ready()
            
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please enter 1-4.")

if __name__ == "__main__":
    main() 