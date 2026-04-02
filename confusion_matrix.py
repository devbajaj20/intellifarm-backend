import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# 1️⃣ Load dataset
# --------------------------------------------------
df = pd.read_csv("data/crop_dataset.csv")

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

for col in FEATURES:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=FEATURES)

# --------------------------------------------------
# 2️⃣ Categories
# --------------------------------------------------
categories = [
    "cereals",
    "vegetables",
    "fruits",
    "pulses",
    "cash",
    "oilseeds"
]

# Different colors for plots
colors = ["Blues", "Reds", "Greens", "Purples", "Oranges", "YlGnBu"]

# Create results folder
os.makedirs("results", exist_ok=True)

# --------------------------------------------------
# 3️⃣ Loop through categories
# --------------------------------------------------
for category, color in zip(categories, colors):

    data = df[df["crop_category"] == category]

    X = data[FEATURES]
    y = data["label"]

    if len(data) == 0:
        print(f"⚠️ No data for {category}")
        continue

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Load trained model
    with open(f"models/{category}_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Predictions
    y_pred = model.predict(X_test)

    # Labels
    labels = sorted(y.unique())

    cm = confusion_matrix(y_test, y_pred, labels=labels)

    # Accuracy
    accuracy = np.trace(cm) / np.sum(cm)

    # --------------------------------------------------
    # Plot confusion matrix
    # --------------------------------------------------
    plt.figure(figsize=(10,8))

    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=color,
        xticklabels=labels,
        yticklabels=labels,
        linewidths=0.5
    )

    plt.xlabel("Predicted Crop", fontsize=12)
    plt.ylabel("Actual Crop", fontsize=12)
    plt.title(f"Confusion Matrix - {category} (Accuracy = {accuracy:.2%})")

    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    plt.tight_layout()

    # Save figure
    plt.savefig(f"results/confusion_matrix_{category}.png", dpi=300)

    plt.close()

    print(f"✅ Saved confusion matrix for {category}")

print("\n🎉 All confusion matrices generated and saved in 'results/' folder")