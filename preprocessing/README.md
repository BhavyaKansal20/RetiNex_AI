# Preprocessing Directory

## Purpose
Data preprocessing, augmentation, and feature engineering pipeline.

## Preprocessing Steps
1. **Image Resizing**: Standardize to model input size
2. **CLAHE**: Contrast Limited Adaptive Histogram Equalization
3. **Normalization**: Pixel value normalization
4. **Data Augmentation**: Rotation, flip, brightness adjustments

## Contents
- **clahe.py**: CLAHE implementation
- **augmentation.py**: Data augmentation strategies
- **data_loader.py**: Load and preprocess datasets
- **normalization.py**: Normalization techniques

## Class Imbalance Handling
- Weighted loss functions
- Oversampling/Undersampling
- SMOTE techniques (if needed)
