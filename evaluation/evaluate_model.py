import sys
import os

sys.path.append(
    os.path.abspath(".")
)

import tensorflow as tf
import pandas as pd
import numpy as np

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt

from training.create_datasets import (
    val_dataset,
    VAL_STEPS
)

# =========================================
# LOAD MODEL
# =========================================

model = tf.keras.models.load_model(
    "models/best_model.keras"
)

# =========================================
# GET PREDICTIONS
# =========================================

y_true = []
y_pred = []

print("\nGenerating Predictions...\n")

for images, labels in val_dataset.take(VAL_STEPS):

    predictions = model.predict(
        images,
        verbose=0
    )

    predicted_classes = np.argmax(
        predictions,
        axis=1
    )

    true_classes = np.argmax(
        labels.numpy(),
        axis=1
    )

    y_true.extend(true_classes)
    y_pred.extend(predicted_classes)

# =========================================
# CLASSIFICATION REPORT
# =========================================

print("\nClassification Report:\n")

report = classification_report(

    y_true,

    y_pred,

    target_names=[
        "No_DR",
        "Mild",
        "Moderate",
        "Severe",
        "Proliferative_DR"
    ]
)

print(report)

# =========================================
# CONFUSION MATRIX
# =========================================

cm = confusion_matrix(
    y_true,
    y_pred
)

# =========================================
# PLOT
# =========================================

fig, ax = plt.subplots(
    figsize=(10, 10)
)

disp = ConfusionMatrixDisplay(

    confusion_matrix=cm,

    display_labels=[
        "No_DR",
        "Mild",
        "Moderate",
        "Severe",
        "Proliferative"
    ]
)

disp.plot(
    cmap="Blues",
    ax=ax
)

plt.title(
    "RetiNexAI Confusion Matrix"
)

plt.savefig(
    "confusion_matrix.png"
)

plt.show()

print("\nConfusion Matrix Saved!")