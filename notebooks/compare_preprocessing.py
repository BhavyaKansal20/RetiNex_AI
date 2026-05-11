import cv2
import matplotlib.pyplot as plt

# =====================================
# IMAGE PATHS
# =====================================

RAW_IMAGE = "data/aptos/train_images/1ae8c165fd53.png"

PROCESSED_IMAGE = "processed/aptos/train/1ae8c165fd53.png"

# =====================================
# LOAD IMAGES
# =====================================

raw = cv2.imread(RAW_IMAGE)
processed = cv2.imread(PROCESSED_IMAGE)

raw = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

# =====================================
# DISPLAY
# =====================================

plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(raw)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(processed)
plt.title("Processed Image (CLAHE)")
plt.axis("off")

plt.tight_layout()
plt.show()