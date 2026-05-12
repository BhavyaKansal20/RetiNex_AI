import os
import cv2
import pandas as pd
from tqdm import tqdm
import numpy as np

# =========================================
# SETTINGS
# =========================================

IMAGE_SIZE = 299

APTOS_METADATA = "metadata/aptos_metadata.csv"
IDRID_METADATA = "metadata/idrid_metadata.csv"

# =========================================
# CLAHE FUNCTION
# =========================================

def apply_clahe(image):

    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=1.2,
        tileGridSize=(8, 8)
    )

    cl = clahe.apply(l)

    merged = cv2.merge((cl, a, b))

    enhanced = cv2.cvtColor(
        merged,
        cv2.COLOR_LAB2RGB
    )

    # Slight smoothing
    enhanced = cv2.GaussianBlur(
        enhanced,
        (3, 3),
        0
    )

    return enhanced

# =========================================
# IMAGE PREPROCESSING
# =========================================

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Threshold to isolate retina
    _, thresh = cv2.threshold(
        gray,
        10,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) > 0:

        largest = max(contours, key=cv2.contourArea)

        x, y, w, h = cv2.boundingRect(largest)
        margin = 20

        x = max(x - margin, 0)
        y = max(y - margin, 0)

        w = min(w + 2 * margin, image.shape[1] - x)
        h = min(h + 2 * margin, image.shape[0] - y)

        image = image[y:y+h, x:x+w]

    # Resize proportionally
    h, w, _ = image.shape

    scale = IMAGE_SIZE / max(h, w)

    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(
        image,
        (new_w, new_h)
    )

    # Create black canvas
    canvas = np.zeros(
        (IMAGE_SIZE, IMAGE_SIZE, 3),
        dtype=np.uint8
    )

    y_offset = (IMAGE_SIZE - new_h) // 2
    x_offset = (IMAGE_SIZE - new_w) // 2

    canvas[
        y_offset:y_offset + new_h,
        x_offset:x_offset + new_w
    ] = resized

    return canvas

# =========================================
# SAVE PROCESSED IMAGES
# =========================================

def process_dataset(metadata_path):

    df = pd.read_csv(metadata_path)

    for _, row in tqdm(df.iterrows(), total=len(df)):

        image_path = row["image_path"]

        dataset = row["dataset"]
        split = row["split"]

        processed_image = preprocess_image(image_path)

        if processed_image is None:
            continue

        filename = os.path.basename(image_path)

        save_dir = os.path.join(
            "processed",
            dataset,
            split
        )

        os.makedirs(save_dir, exist_ok=True)

        save_path = os.path.join(
            save_dir,
            filename
        )

        processed_image = cv2.cvtColor(
            processed_image,
            cv2.COLOR_RGB2BGR
        )

        cv2.imwrite(
            save_path,
            processed_image
        )

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    print("\nProcessing APTOS Dataset...\n")
    process_dataset(APTOS_METADATA)

    #print("\nProcessing IDRiD Dataset...\n")
    #process_dataset(IDRID_METADATA)

    print("\nPreprocessing Completed Successfully!")