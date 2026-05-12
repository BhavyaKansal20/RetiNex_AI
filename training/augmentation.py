import tensorflow as tf

IMAGE_SIZE = 299


def apply_augmentation(image, label):
    """Standard augmentation pipeline for retinal images."""
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_flip_up_down(image)
    image = tf.image.random_brightness(image, max_delta=0.15)
    image = tf.image.random_contrast(image, lower=0.85, upper=1.15)
    image = tf.image.random_saturation(image, lower=0.85, upper=1.15)

    # Random rotation (0, 90, 180, 270 degrees)
    k = tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.int32)
    image = tf.image.rot90(image, k=k)

    image = tf.clip_by_value(image, 0.0, 255.0)
    return image, label


def mixup(images, labels, alpha=0.2):
    """MixUp augmentation: linear interpolation of image pairs.

    Reference: Zhang et al., "mixup: Beyond Empirical Risk Minimization", ICLR 2018
    """
    batch_size = tf.shape(images)[0]
    lam = tf.random.uniform(shape=[batch_size, 1, 1, 1], minval=0.0, maxval=alpha)
    indices = tf.random.shuffle(tf.range(batch_size))
    shuffled_images = tf.gather(images, indices)
    shuffled_labels = tf.gather(labels, indices)
    mixed_images = lam * images + (1.0 - lam) * shuffled_images
    lam_labels = tf.reshape(lam, [batch_size, 1])
    mixed_labels = lam_labels * tf.cast(labels, tf.float32) + (1.0 - lam_labels) * tf.cast(shuffled_labels, tf.float32)
    return mixed_images, mixed_labels


def cutmix(images, labels, alpha=1.0):
    """CutMix augmentation: replace a rectangular region with another sample.

    Reference: Yun et al., "CutMix: Regularization Strategy to Train Strong Classifiers", ICCV 2019
    """
    batch_size = tf.shape(images)[0]
    lam = tf.random.uniform(shape=[], minval=0.0, maxval=1.0)

    cut_ratio = tf.sqrt(1.0 - lam)
    cut_h = tf.cast(tf.cast(IMAGE_SIZE, tf.float32) * cut_ratio, tf.int32)
    cut_w = tf.cast(tf.cast(IMAGE_SIZE, tf.float32) * cut_ratio, tf.int32)

    cx = tf.random.uniform(shape=[], minval=0, maxval=IMAGE_SIZE, dtype=tf.int32)
    cy = tf.random.uniform(shape=[], minval=0, maxval=IMAGE_SIZE, dtype=tf.int32)

    x1 = tf.clip_by_value(cx - cut_w // 2, 0, IMAGE_SIZE)
    y1 = tf.clip_by_value(cy - cut_h // 2, 0, IMAGE_SIZE)
    x2 = tf.clip_by_value(cx + cut_w // 2, 0, IMAGE_SIZE)
    y2 = tf.clip_by_value(cy + cut_h // 2, 0, IMAGE_SIZE)

    indices = tf.random.shuffle(tf.range(batch_size))
    shuffled_images = tf.gather(images, indices)
    shuffled_labels = tf.gather(labels, indices)

    # Build mask
    mask = tf.ones_like(images)
    padding = [[0, 0], [y1, IMAGE_SIZE - y2], [x1, IMAGE_SIZE - x2], [0, 0]]
    cutout = tf.zeros([batch_size, y2 - y1, x2 - x1, 3])
    padded_cutout = tf.pad(cutout, padding, constant_values=1.0)
    mask = padded_cutout

    mixed = images * mask + shuffled_images * (1.0 - mask)
    area = tf.cast((x2 - x1) * (y2 - y1), tf.float32) / tf.cast(IMAGE_SIZE * IMAGE_SIZE, tf.float32)
    mixed_labels = (1.0 - area) * tf.cast(labels, tf.float32) + area * tf.cast(shuffled_labels, tf.float32)

    return mixed, mixed_labels
