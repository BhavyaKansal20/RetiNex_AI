import os
import pandas as pd

records = []

# ====================================
# UNIFIED DATASET
# ====================================

UNIFIED_ROOT = "dataset/dr_unified_v2/dr_unified_v2"

for split in ["train", "val", "test"]:

    split_path = os.path.join(UNIFIED_ROOT, split)

    for label in ["0", "1", "2", "3", "4"]:

        class_dir = os.path.join(split_path, label)

        if not os.path.exists(class_dir):
            continue

        for file in os.listdir(class_dir):

            if file.lower().endswith((".jpg", ".jpeg", ".png")):

                records.append({
                    "image_path": os.path.join(class_dir, file),
                    "label": int(label),
                    "source_dataset": "unified",
                    "split": split
                })

# ====================================
# IDRID DATASET
# ====================================

idrid_labels = pd.read_csv(
    "dataset/idrid/idrid_labels.csv"
)

for _, row in idrid_labels.iterrows():

    image_name = row["id_code"] + ".jpg"

    image_path = os.path.join(
        "dataset/idrid/Imagenes/Imagenes",
        image_name
    )

    if os.path.exists(image_path):

        records.append({
            "image_path": image_path,
            "label": int(row["diagnosis"]),
            "source_dataset": "idrid",
            "split": "train"
        })

# ====================================
# SAVE CSV
# ====================================

df = pd.DataFrame(records)

save_path = "metadata/retinex_master_metadata.csv"

df.to_csv(
    save_path,
    index=False
)

print("\nMetadata Created Successfully\n")

print(df.head())

print("\nTotal Images:", len(df))

print("\nClass Distribution:\n")

print(
    df["label"]
    .value_counts()
    .sort_index()
)