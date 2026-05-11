import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# =========================
# PATHS
# =========================

BASE_DIR = "data/idrid"

TRAIN_DIR = os.path.join(BASE_DIR, "train_images")
TEST_DIR = os.path.join(BASE_DIR, "test_images")
LABEL_PATH = os.path.join(BASE_DIR, "labels", "idrid_labels.csv")

# =========================
# LOAD LABELS
# =========================

df = pd.read_csv(LABEL_PATH)

print("\nDataset Labels Preview:\n")
print(df.head())

# =========================
# IMAGE COUNTS
# =========================

train_images = os.listdir(TRAIN_DIR)
test_images = os.listdir(TEST_DIR)

print(f"\nTrain Images: {len(train_images)}")
print(f"Test Images: {len(test_images)}")

# =========================
# SHOW SAMPLE IMAGES
# =========================

sample_images = train_images[:6]

plt.figure(figsize=(15, 8))

for i, img_name in enumerate(sample_images):
    img_path = os.path.join(TRAIN_DIR, img_name)

    img = Image.open(img_path)

    plt.subplot(2, 3, i + 1)
    plt.imshow(img)
    plt.title(img_name)
    plt.axis("off")

plt.tight_layout()
plt.show()

# =========================
# CHECK CORRUPTED IMAGES
# =========================

corrupted = []

for img_name in train_images:
    try:
        img_path = os.path.join(TRAIN_DIR, img_name)
        img = Image.open(img_path)
        img.verify()
    except:
        corrupted.append(img_name)

print(f"\nCorrupted Images Found: {len(corrupted)}")

if len(corrupted) > 0:
    print(corrupted)