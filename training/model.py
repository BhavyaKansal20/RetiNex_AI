import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models

# =========================================
# SETTINGS
# =========================================

IMAGE_SIZE = 300
NUM_CLASSES = 5

# =========================================
# BUILD MODEL
# =========================================

def build_model():

    base_model = tf.keras.applications.EfficientNetV2B3(
        include_top=False,
        weights="imagenet",
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
    )

    # Freeze backbone initially
    base_model.trainable = False

    inputs = layers.Input(
        shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
    )

    x = base_model(
        inputs,
        training=False
    )

    x = layers.GlobalAveragePooling2D()(x)

    x = layers.Dropout(0.3)(x)

    outputs = layers.Dense(
        NUM_CLASSES,
        activation="softmax"
    )(x)

    model = models.Model(
        inputs,
        outputs
    )

    return model