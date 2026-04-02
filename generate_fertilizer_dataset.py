import pandas as pd
import random

# Load your crop recommendation dataset
crop_df = pd.read_csv("data/crop_dataset.csv")

# Unique crops with categories
crops = crop_df[["crop_category", "label", "soil_type_1"]].drop_duplicates()

# Nutrient levels farmers can choose
levels = ["low", "medium", "high"]

fertilizers = [
    "Urea",
    "DAP",
    "MOP",
    "NPK",
    "Compost",
    "Ammonium Sulfate"
]

rows = []

for _, row in crops.iterrows():
    for i in range(8):  # generate multiple rows per crop

        rows.append({
            "crop_category": row["crop_category"],
            "crop": row["label"],
            "soil_type": row["soil_type_1"],
            "N_level": random.choice(levels),
            "P_level": random.choice(levels),
            "K_level": random.choice(levels),
            "temperature": random.randint(20, 35),
            "humidity": random.randint(50, 90),
            "ph": round(random.uniform(5.5, 7.5), 1),
            "rainfall": random.randint(80, 250),
            "fertilizer": random.choice(fertilizers)
        })

fert_df = pd.DataFrame(rows)

fert_df.to_csv("data/fertilizer_dataset_full.csv", index=False)

print("✅ Fertilizer dataset generated successfully")
print("Rows:", len(fert_df))