import pandas as pd

MASTER_CSV = "metadata/retinex_master_metadata.csv"
OUTPUT_CSV = "metadata/retinex_balanced_v1.csv"

TARGETS = {
    0: 15000,
    1: 12000,
    2: 12000,
    3: 12000,
    4: 12000
}

df = pd.read_csv(MASTER_CSV)

balanced_parts = []

for label, target in TARGETS.items():

    class_df = df[df["label"] == label]

    current_count = len(class_df)

    print(
        f"\nClass {label}: "
        f"{current_count} images"
    )

    if current_count >= target:

        sampled = class_df.sample(
            n=target,
            random_state=42
        )

    else:

        sampled = class_df.sample(
            n=target,
            replace=True,
            random_state=42
        )

    balanced_parts.append(sampled)

balanced_df = pd.concat(
    balanced_parts,
    ignore_index=True
)

balanced_df = balanced_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

balanced_df.to_csv(
    OUTPUT_CSV,
    index=False
)

print("\nBalanced Dataset Created!")

print("\nFinal Distribution:\n")

print(
    balanced_df["label"]
    .value_counts()
    .sort_index()
)

print(
    f"\nTotal Images: "
    f"{len(balanced_df)}"
)