import tensorflow as tf
import pandas as pd

# =========================================
# SETTINGS
# =========================================

IMAGE_SIZE = 299
BATCH_SIZE = 16
NUM_CLASSES = 5

# =========================================
# LOAD METADATA
# =========================================

df = pd.read_csv(
    "metadata/aptos_metadata.csv"
)

# =========================================
# SPLITS
# =========================================

train_df = df[df["split"] == "train"]
val_df = df[df["split"] == "val"]

# =========================================
# EFFICIENTNET PREPROCESSING
# =========================================

preprocess_input = tf.keras.applications.efficientnet_v2.preprocess_input

# =========================================
# IMAGE LOADER
# =========================================

def load_image(image_path, label):

    image = tf.io.read_file(image_path)

    image = tf.image.decode_png(
        image,
        channels=3
    )

    image = tf.image.resize(
        image,
        [IMAGE_SIZE, IMAGE_SIZE]
    )

    image = tf.cast(
        image,
        tf.float32
    )

    image = preprocess_input(image)

    label = tf.one_hot(
        label,
        depth=NUM_CLASSES
    )

    return image, label

# =========================================
# CREATE DATASET
# =========================================

def create_dataset(dataframe, training=False):

    dataset = tf.data.Dataset.from_tensor_slices(
        (
            dataframe["image_path"].values,
            dataframe["diagnosis"].values
        )
    )

    dataset = dataset.map(
        load_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    if training:

        dataset = dataset.shuffle(
            buffer_size=1000
        )

    dataset = dataset.repeat()

    dataset = dataset.batch(
        BATCH_SIZE
    )

    dataset = dataset.prefetch(
        tf.data.AUTOTUNE
    )

    return dataset

# =========================================
# DATASETS
# =========================================

train_dataset = create_dataset(
    train_df,
    training=True
)

val_dataset = create_dataset(
    val_df
)

# =========================================
# TRAINING STEPS
# =========================================

TRAIN_STEPS = len(train_df) // BATCH_SIZE

VAL_STEPS = len(val_df) // BATCH_SIZE

# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    print("\nTrain Samples:")
    print(len(train_df))

    print("\nValidation Samples:")
    print(len(val_df))

    print("\nTrain Steps:")
    print(TRAIN_STEPS)

    print("\nValidation Steps:")
    print(VAL_STEPS)

    for images, labels in train_dataset.take(1):

        print("\nImage Batch Shape:")
        print(images.shape)

        print("\nLabel Batch Shape:")
        print(labels.shape)