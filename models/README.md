# Models Directory

## Purpose
Store trained model checkpoints, architectures, and model-related utilities.

## Contents
- **model_architecture.py**: EfficientNetV2 and alternative model definitions
- **saved_models/**: Trained model checkpoints (.h5, .keras files)
- **model_utils.py**: Helper functions for model loading/saving

## Model Variants
- Primary: EfficientNetV2B0, EfficientNetV2B3
- Experimental: Vision Transformer (ViT), ConvNeXtTiny

## Training Strategy
- Transfer learning from ImageNet weights
- Early stopping with checkpoint saving
- Best model selection based on validation metrics
