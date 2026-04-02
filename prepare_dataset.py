import pandas as pd
import os

# --------------------------------------------------
# 0️⃣ Ensure output folder exists
# --------------------------------------------------
os.makedirs("data", exist_ok=True)

# --------------------------------------------------
# 1️⃣ Read ALL sheets from Excel
# --------------------------------------------------
sheets = pd.read_excel("crop_dataset.xlsx", sheet_name=None)

all_data = []

# --------------------------------------------------
# 2️⃣ Sheet name → category mapping
# --------------------------------------------------
SHEET_CATEGORY_MAP = {
    "cereals": "cereals",
    "pulses": "pulses",
    "oilseeds": "oilseeds",
    "fruits": "fruits",
    "vegetables": "vegetables",
    "commercial crops": "cash",
    "cash crops": "cash"
}

# --------------------------------------------------
# 3️⃣ Helper: detect soil-related columns dynamically
# --------------------------------------------------
def find_soil_columns(columns):
    soil_cols = []
    for col in columns:
        if "soil" in col.lower():
            soil_cols.append(col)
    return soil_cols

# --------------------------------------------------
# 4️⃣ Process each sheet
# --------------------------------------------------
for sheet_name, df in sheets.items():
    key = sheet_name.strip().lower()

    if key not in SHEET_CATEGORY_MAP:
        print(f"⚠️ Skipping sheet: {sheet_name}")
        continue

    # ---- Standardize column names ----
    df.rename(columns={
        "temperature(in degree celsius)": "temperature",
        "humidity(in percentage)": "humidity",
        "ph of soil": "ph",
        "rainfall( in mm )": "rainfall",
        "Label": "label"
    }, inplace=True)

    # ---- Clean crop labels ----
    df["label"] = df["label"].astype(str).str.lower().str.strip()

    # ---- Detect soil columns ----
    soil_cols = find_soil_columns(df.columns)

    if len(soil_cols) >= 2:
        df["soil_type_1"] = df[soil_cols[0]]
        df["soil_type_2"] = df[soil_cols[1]]
    elif len(soil_cols) == 1:
        df["soil_type_1"] = df[soil_cols[0]]
        df["soil_type_2"] = df[soil_cols[0]]
    else:
        df["soil_type_1"] = "unknown"
        df["soil_type_2"] = "unknown"

    # ---- Normalize soil values ----
    df["soil_type_1"] = (
        df["soil_type_1"]
        .astype(str)
        .str.lower()
        .str.strip()
        .replace("nan", "unknown")
    )

    df["soil_type_2"] = (
        df["soil_type_2"]
        .astype(str)
        .str.lower()
        .str.strip()
        .replace("nan", "unknown")
    )

    # ---- Assign category from sheet ----
    df["crop_category"] = SHEET_CATEGORY_MAP[key]

    # ---- Keep only required columns ----
    df = df[
        [
            "N", "P", "K",
            "temperature", "humidity", "ph", "rainfall",
            "label", "crop_category",
            "soil_type_1", "soil_type_2"
        ]
    ]

    all_data.append(df)

# --------------------------------------------------
# 5️⃣ Merge all sheets
# --------------------------------------------------
final_df = pd.concat(all_data, ignore_index=True)

# --------------------------------------------------
# 6️⃣ Final safety cleaning
# --------------------------------------------------
final_df["soil_type_1"] = final_df["soil_type_1"].fillna("unknown")
final_df["soil_type_2"] = final_df["soil_type_2"].fillna("unknown")

# Normalize extra spaces
final_df["soil_type_1"] = final_df["soil_type_1"].str.replace(r"\s+", " ", regex=True)
final_df["soil_type_2"] = final_df["soil_type_2"].str.replace(r"\s+", " ", regex=True)

# --------------------------------------------------
# 7️⃣ Save final dataset
# --------------------------------------------------
final_df.to_csv("data/crop_dataset.csv", index=False)

# --------------------------------------------------
# 8️⃣ Verification output
# --------------------------------------------------
print("✅ Dataset prepared successfully from ALL sheets!")
print(final_df["crop_category"].value_counts())

print("\nSoil column check:")
print(final_df[["soil_type_1", "soil_type_2"]].head())
