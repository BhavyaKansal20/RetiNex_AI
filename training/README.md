# Training Directory

## Purpose
Model training pipeline with logging, evaluation, and checkpoint management.

## Contents
- **train.py**: Main training script
- **callbacks.py**: TensorFlow callbacks (EarlyStopping, ModelCheckpoint)
- **loss_functions.py**: Custom loss functions for class imbalance
- **metrics.py**: Evaluation metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
- **cross_validation.py**: Cross-dataset evaluation

## Training Features
- Early stopping with patience
- Mixed precision training
- Automatic checkpoint saving
- Training history logging
- Tensorboard integration (optional)

## Evaluation Metrics
- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix
- ROC-AUC
- Per-class metrics
