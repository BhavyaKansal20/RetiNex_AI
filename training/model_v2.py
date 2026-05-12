import tensorflow as tf
from tensorflow.keras import layers, models

IMAGE_SIZE = 299
NUM_CLASSES = 5


def build_efficientnet_b3(freeze_base=True):
    """Enhanced EfficientNetV2-B3 model with deeper classification head."""
    base_model = tf.keras.applications.EfficientNetV2B3(
        include_top=False,
        weights="imagenet",
        input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3),
    )
    base_model.trainable = not freeze_base

    inputs = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

    model = models.Model(inputs, outputs, name="EfficientNetV2_B3_DR")
    return model


def build_ordinal_model(backbone="b0"):
    """Ordinal regression model: exploits DR severity ordering (0 < 1 < 2 < 3 < 4).

    Instead of 5-class softmax, uses 4 binary sigmoid outputs:
    P(class >= 1), P(class >= 2), P(class >= 3), P(class >= 4)

    Novel contribution for research paper.
    """
    if backbone == "b3":
        base_model = tf.keras.applications.EfficientNetV2B3(
            include_top=False, weights="imagenet", input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
        )
    else:
        base_model = tf.keras.applications.EfficientNetV2B0(
            include_top=False, weights="imagenet", input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
        )
    base_model.trainable = False

    inputs = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.3)(x)

    # 4 binary outputs for ordinal thresholds
    ordinal_outputs = layers.Dense(NUM_CLASSES - 1, activation="sigmoid", name="ordinal_output")(x)

    model = models.Model(inputs, ordinal_outputs, name="OrdinalDR")
    return model


def ordinal_to_class(ordinal_preds):
    """Convert ordinal predictions to class labels.

    Each sigmoid output represents P(class >= k).
    Class = sum of thresholds > 0.5
    """
    import numpy as np
    return np.sum(ordinal_preds > 0.5, axis=-1).astype(int)
