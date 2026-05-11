import tensorflow as tf

from training.model import build_model

from training.create_datasets import (
    train_dataset,
    val_dataset,
    TRAIN_STEPS,
    VAL_STEPS
)

# =========================================
# BUILD MODEL
# =========================================

model = build_model()

# =========================================
# COMPILE MODEL
# =========================================

model.compile(

    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-4
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

        monitor="val_loss",

        patience=5,

        restore_best_weights=True
    ),

    tf.keras.callbacks.ReduceLROnPlateau(

        monitor="val_loss",

        factor=0.2,

        patience=2,

        verbose=1
    ),

    tf.keras.callbacks.ModelCheckpoint(

        filepath="models/best_model.keras",

        monitor="val_loss",

        save_best_only=True,

        verbose=1
    )
]

# =========================================
# TRAIN MODEL
# =========================================

history = model.fit(

    train_dataset,

    validation_data=val_dataset,

    epochs=15,

    steps_per_epoch=TRAIN_STEPS,

    validation_steps=VAL_STEPS,

    callbacks=callbacks
)

# =========================================
# SAVE FINAL MODEL
# =========================================

model.save(
    "models/final_model.keras"
)

print("\nTraining Completed Successfully!")