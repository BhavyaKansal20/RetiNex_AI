import tensorflow as tf
import pandas as pd

# =========================================
# SETTINGS
# =========================================

IMAGE_SIZE = 384
BATCH_SIZE = 16

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
test_df = df[df["split"] == "test"]

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
    ) / 255.0

    label = tf.one_hot(label, depth=5)

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
        dataset = dataset.shuffle(1000)

    dataset = dataset.batch(BATCH_SIZE)

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

test_dataset = create_dataset(
    test_df
)

# =========================================
# TEST PIPELINE
# =========================================

if __name__ == "__main__":

    print("\nTrain batches:")
    print(len(train_dataset))

    print("\nValidation batches:")
    print(len(val_dataset))

    print("\nTest batches:")
    print(len(test_dataset))

    for images, labels in train_dataset.take(1):

        print("\nImage Batch Shape:")
        print(images.shape)

        print("\nLabel Batch Shape:")
        print(labels.shape)