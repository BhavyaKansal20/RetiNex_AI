import tensorflow as tf


class FocalLoss(tf.keras.losses.Loss):
    """Focal Loss for handling class imbalance in DR classification.

    Reduces the loss contribution from easy examples and focuses on hard ones.
    Especially useful for DR where No_DR and Mild classes dominate.

    Reference: Lin et al., "Focal Loss for Dense Object Detection", ICCV 2017
    """

    def __init__(self, gamma=2.0, alpha=None, num_classes=5, **kwargs):
        super().__init__(**kwargs)
        self.gamma = gamma
        if alpha is None:
            self.alpha = tf.ones(num_classes) / num_classes
        else:
            self.alpha = tf.constant(alpha, dtype=tf.float32)

    def call(self, y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = y_true * tf.pow(1.0 - y_pred, self.gamma)
        focal = self.alpha * weight * cross_entropy
        return tf.reduce_sum(focal, axis=-1)

    def get_config(self):
        config = super().get_config()
        config.update({"gamma": self.gamma, "alpha": self.alpha.numpy().tolist()})
        return config


class SeverityAwareFocalLoss(tf.keras.losses.Loss):
    """Severity-Aware Focal Loss: custom gamma per class based on DR severity ordinality.

    Higher severity classes get lower gamma (less focus reduction) to ensure the model
    doesn't under-predict dangerous conditions.

    Novel contribution for research paper.
    """

    def __init__(self, gammas=None, alpha=None, num_classes=5, **kwargs):
        super().__init__(**kwargs)
        if gammas is None:
            # Lower gamma for higher severity = more focus on severe cases
            self.gammas = tf.constant([3.0, 2.5, 2.0, 1.5, 1.0], dtype=tf.float32)
        else:
            self.gammas = tf.constant(gammas, dtype=tf.float32)
        if alpha is None:
            self.alpha = tf.ones(num_classes) / num_classes
        else:
            self.alpha = tf.constant(alpha, dtype=tf.float32)

    def call(self, y_true, y_pred):
        y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)
        cross_entropy = -y_true * tf.math.log(y_pred)
        weight = y_true * tf.pow(1.0 - y_pred, self.gammas)
        focal = self.alpha * weight * cross_entropy
        return tf.reduce_sum(focal, axis=-1)

    def get_config(self):
        config = super().get_config()
        config.update({
            "gammas": self.gammas.numpy().tolist(),
            "alpha": self.alpha.numpy().tolist(),
        })
        return config
