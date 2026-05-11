
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil
import os

# ======================================
# LOAD CSV
# ======================================

df = pd.read_csv("data/aptos/train.csv")

# ======================================
# STRATIFIED SPLIT
# ======================================

train_df, val_df = train_test_split(

    df,

    test_size=0.15,

    stratify=df["diagnosis"],

    random_state=42
)

# ======================================
# SAVE CSV FILES
# ======================================

train_df.to_csv(
    "data/aptos/train_split.csv",
    index=False
)

val_df.to_csv(
    "data/aptos/val.csv",
    index=False
)

# ======================================
# CREATE VAL FOLDER
# ======================================

os.makedirs(
    "data/aptos/val_images",
    exist_ok=True
)

# ======================================
# MOVE VALIDATION IMAGES
# ======================================

for image_id in val_df["id_code"]:

    src = f"data/aptos/train_images/{image_id}.png"

    dst = f"data/aptos/val_images/{image_id}.png"

    if os.path.exists(src):

        shutil.move(src, dst)

print("\nValidation Split Created Successfully!")
