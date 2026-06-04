import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("metadata/retinex_master_metadata.csv")

print("\nTotal Images:", len(df))

print("\nClass Distribution:\n")
print(df["label"].value_counts().sort_index())

plt.figure(figsize=(10,6))

df["label"].value_counts().sort_index().plot(
    kind="bar"
)

plt.title("RetiNex Dataset Class Distribution")

plt.xlabel("DR Grade")

plt.ylabel("Number of Images")

plt.tight_layout()

plt.savefig(
    "retinex_class_distribution.png"
)

plt.show()