import os
import pandas as pd

# =====================================
# PATHS
# =====================================

APTOS_DIR = "data/aptos"
IDRID_DIR = "data/idrid"

METADATA_DIR = "metadata"

os.makedirs(METADATA_DIR, exist_ok=True)

# =====================================
# APTOS METADATA
# =====================================

def create_aptos_metadata():

    all_dfs = []

    split_files = {
        "train": "train.csv",
        "val": "val.csv",
        "test": "test.csv"
    }

    for split, csv_file in split_files.items():

        csv_path = os.path.join(APTOS_DIR, csv_file)

        df = pd.read_csv(csv_path)

        image_folder = f"{split}_images"

        df["image_path"] = df["id_code"].apply(
            lambda x: os.path.join(
                APTOS_DIR,
                image_folder,
                f"{x}.png"
            )
        )

        df["split"] = split
        df["dataset"] = "aptos"

        all_dfs.append(df)

    aptos_df = pd.concat(all_dfs, ignore_index=True)

    save_path = os.path.join(
        METADATA_DIR,
        "aptos_metadata.csv"
    )

    aptos_df.to_csv(save_path, index=False)

    print("\nAPTOS Metadata Created")
    print(aptos_df.head())
    print(f"\nTotal Samples: {len(aptos_df)}")


# =====================================
# IDRID METADATA
# =====================================

def create_idrid_metadata():

    label_path = os.path.join(
        IDRID_DIR,
        "labels",
        "idrid_labels.csv"
    )

    df = pd.read_csv(label_path)

    # Remove junk columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    all_rows = []

    # =========================
    # TRAIN IMAGES
    # =========================

    for _, row in df.iterrows():

        train_path = os.path.join(
            IDRID_DIR,
            "train_images",
            f"{row['id_code']}.jpg"
        )

        if os.path.exists(train_path):

            temp = row.copy()

            temp["image_path"] = train_path
            temp["split"] = "train"
            temp["dataset"] = "idrid"

            all_rows.append(temp)

    # =========================
    # TEST IMAGES
    # =========================

    test_images = os.listdir(
        os.path.join(IDRID_DIR, "test_images")
    )

    for img_name in test_images:

        img_id = img_name.replace("test.jpg", "")

        matched = df[df["id_code"] == img_id]

        if len(matched) > 0:

            row = matched.iloc[0].copy()

            test_path = os.path.join(
                IDRID_DIR,
                "test_images",
                img_name
            )

            row["image_path"] = test_path
            row["split"] = "test"
            row["dataset"] = "idrid"

            all_rows.append(row)

    final_df = pd.DataFrame(all_rows)

    save_path = os.path.join(
        METADATA_DIR,
        "idrid_metadata.csv"
    )

    final_df.to_csv(save_path, index=False)

    print("\nIDRiD Metadata Created")
    print(final_df.head())
    print(f"\nTotal Samples: {len(final_df)}")


# =====================================
# RUN
# =====================================

if __name__ == "__main__":

    create_aptos_metadata()
    create_idrid_metadata()