from training.utils import get_class_weights

import pandas as pd
import matplotlib.pyplot as plt

# ======================================
# LOAD METADATA
# ======================================

df = pd.read_csv("metadata/aptos_metadata.csv")

print("\nDataset Preview:\n")
print(df.head())

# ======================================
# CLASS DISTRIBUTION
# ======================================

class_counts = df["diagnosis"].value_counts().sort_index()

print("\nClass Distribution:\n")
print(class_counts)

# ======================================
# PLOT
# ======================================

plt.figure(figsize=(8, 5))

class_counts.plot(kind="bar")

plt.title("APTOS DR Class Distribution")
plt.xlabel("Diagnosis Class")
plt.ylabel("Number of Images")

plt.xticks(rotation=0)

# ======================================
# CLASS PERCENTAGES
# ======================================

percentages = (
    class_counts / len(df)
) * 100

print("\nClass Percentages:\n")
print(percentages.round(2))

# ======================================
# CLASS WEIGHTS
# ======================================

class_weights = get_class_weights(
    df["diagnosis"]
)

print("\nClass Weights:\n")

for cls, weight in class_weights.items():
    print(f"Class {cls}: {weight:.4f}")

# SHOW PLOT LAST
plt.show()