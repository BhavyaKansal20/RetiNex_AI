import tensorflow as tf
import pandas as pd

from training.model import build_model
from training.create_datasets import (
    train_dataset,
    val_dataset,
    test_dataset
)

from training.utils import get_class_weights

# =========================================
# LOAD METADATA
# =========================================

df = pd.read_csv(
    "metadata/aptos_metadata.csv"
)

class_weights = get_class_weights(
    df["diagnosis"]
)

# =========================================
# BUILD MODEL
# =========================================

model = build_model()

# =========================================
# COMPILE
# =========================================

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-3
    ),

    loss="categorical_crossentropy",

    metrics=[
        "accuracy"
    ]
)

# =========================================
# CALLBACKS
# =========================================

callbacks = [

    tf.keras.callbacks.EarlyStopping(
        patience=5,
        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(
        factor=0.2,
        patience=2
    ),

    tf.keras.callbacks.ModelCheckpoint(
        "models/best_model.keras",
        save_best_only=True
    )
]

# =========================================
# TRAIN
# =========================================

history = model.fit(

    train_dataset,

    validation_data=val_dataset,

    epochs=15,

    class_weight=class_weights,

    callbacks=callbacks
)

# =========================================
# TEST EVALUATION
# =========================================

results = model.evaluate(
    test_dataset
)

print("\nTest Results:")
print(results)