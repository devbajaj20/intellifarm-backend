import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier

# --------------------------------------------------
# 1️⃣ Load dataset
# --------------------------------------------------
df = pd.read_csv("data/crop_dataset.csv")

FEATURES = ["N","P","K","temperature","humidity","ph","rainfall"]

for col in FEATURES:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=FEATURES)

# --------------------------------------------------
# 2️⃣ Crop Categories
# --------------------------------------------------
categories = ["cereals","pulses","oilseeds","fruits","vegetables","cash"]

accuracy_list = []
precision_list = []
recall_list = []
f1_list = []

# --------------------------------------------------
# 3️⃣ Train + Evaluate models
# --------------------------------------------------
for cat in categories:

    data = df[df["crop_category"] == cat]

    X = data[FEATURES]
    y = data["label"]

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Store metrics
    accuracy_list.append(accuracy_score(y_test, y_pred))
    precision_list.append(precision_score(y_test, y_pred, average="weighted"))
    recall_list.append(recall_score(y_test, y_pred, average="weighted"))
    f1_list.append(f1_score(y_test, y_pred, average="weighted"))

# --------------------------------------------------
# 4️⃣ Print Metrics Table
# --------------------------------------------------
results_df = pd.DataFrame({
    "Category": categories,
    "Accuracy": accuracy_list,
    "Precision": precision_list,
    "Recall": recall_list,
    "F1 Score": f1_list
})

results_df = results_df.round(4)

print("\n================ Crop Recommendation Model Performance ================\n")
print(results_df.to_string(index=False))

# --------------------------------------------------
# 5️⃣ Graph 1: Precision Recall F1
# --------------------------------------------------
metrics_df = pd.DataFrame({
    "Category": categories,
    "Precision": precision_list,
    "Recall": recall_list,
    "F1 Score": f1_list
})

metrics_df = metrics_df.set_index("Category")

metrics_df.plot(
    kind="bar",
    figsize=(10,6),
    color=["#a5d6a7", "#66bb6a", "#1b5e20"]
)

plt.title("Model Performance by Crop Category")
plt.ylabel("Score")
plt.ylim(0.5,1.0)
plt.xticks(rotation=0)
plt.tight_layout()

plt.show()

# --------------------------------------------------
# 6️⃣ Graph 2: Accuracy
# --------------------------------------------------
plt.figure(figsize=(8,5))

sns.barplot(
    x=categories,
    y=accuracy_list,
    palette="Greens"
)

plt.title("Accuracy for Each Crop Category Model")
plt.ylabel("Accuracy")
plt.ylim(0.5,1.0)

plt.tight_layout()
plt.show()