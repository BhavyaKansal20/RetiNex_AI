import pandas as pd
import os

# =====================================
# LOAD METADATA
# =====================================

df = pd.read_csv(
    "metadata/aptos_metadata.csv"
)

# =====================================
# UPDATE PATHS
# =====================================

def convert_path(row):

    split = row["split"]

    filename = os.path.basename(
        row["image_path"]
    )

    return os.path.join(
        "processed",
        "aptos",
        split,
        filename
    )

df["image_path"] = df.apply(
    convert_path,
    axis=1
)

# =====================================
# SAVE
# =====================================

df.to_csv(
    "metadata/aptos_metadata.csv",
    index=False
)

print("\nMetadata paths updated!")
print(df.head())