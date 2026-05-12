
import os
import pandas as pd

# =====================================
# PATHS
# =====================================

APTOS_DIR = "data/aptos"

METADATA_DIR = "metadata"

os.makedirs(METADATA_DIR, exist_ok=True)

# =====================================
# CREATE APTOS METADATA
# =====================================

def create_aptos_metadata():

    all_dfs = []

    split_files = {
    "train": "train.csv",
    "val": "val.csv",
    "test": "test.csv"
    }

    for split, csv_file in split_files.items():

        csv_path = os.path.join(
            APTOS_DIR,
            csv_file
        )

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

    aptos_df = pd.concat(
        all_dfs,
        ignore_index=True
    )

    save_path = os.path.join(
        METADATA_DIR,
        "aptos_metadata.csv"
    )

    aptos_df.to_csv(
        save_path,
        index=False
    )

    print("\nAPTOS Metadata Created")
    print(aptos_df.head())
    print(f"\nTotal Samples: {len(aptos_df)}")


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    create_aptos_metadata()
