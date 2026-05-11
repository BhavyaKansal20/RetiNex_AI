from sklearn.utils.class_weight import compute_class_weight
import numpy as np

# =========================================
# COMPUTE CLASS WEIGHTS
# =========================================

def get_class_weights(labels):

    classes = np.unique(labels)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=labels
    )

    class_weights = dict(
        zip(classes, weights)
    )

    return class_weights