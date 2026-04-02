import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score


# --------------------------------------------------
# 1️⃣ Load dataset
# --------------------------------------------------

df = pd.read_csv("data/fertilizer_dataset_full.csv")

print("Dataset loaded\n")
print(df.head())


# --------------------------------------------------
# 2️⃣ Encode categorical columns
# --------------------------------------------------

soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()
fert_encoder = LabelEncoder()

n_encoder = LabelEncoder()
p_encoder = LabelEncoder()
k_encoder = LabelEncoder()

df["soil_type"] = soil_encoder.fit_transform(df["soil_type"])
df["crop"] = crop_encoder.fit_transform(df["crop"])
df["fertilizer"] = fert_encoder.fit_transform(df["fertilizer"])

df["N_level"] = n_encoder.fit_transform(df["N_level"])
df["P_level"] = p_encoder.fit_transform(df["P_level"])
df["K_level"] = k_encoder.fit_transform(df["K_level"])


# --------------------------------------------------
# 3️⃣ Feature selection
# --------------------------------------------------

FEATURES = [
    "soil_type",
    "crop",
    "N_level",
    "P_level",
    "K_level",
    "temperature",
    "humidity",
    "ph",
    "rainfall",
]

X = df[FEATURES]
y = df["fertilizer"]


# --------------------------------------------------
# 4️⃣ Train Test Split (STRATIFIED)
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# --------------------------------------------------
# 5️⃣ Train model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# --------------------------------------------------
# 6️⃣ Predictions
# --------------------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n================ Model Performance ================\n")

print("Accuracy:", round(accuracy,4))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))


# --------------------------------------------------
# 7️⃣ Confusion matrix
# --------------------------------------------------

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(7,5))

sns.heatmap(
    cm,
    annot=True,
    cmap="Greens",
    fmt="d",
    xticklabels=fert_encoder.classes_,
    yticklabels=fert_encoder.classes_
)

plt.title("Fertilizer Prediction Confusion Matrix")

plt.xlabel("Predicted Fertilizer")
plt.ylabel("Actual Fertilizer")

plt.tight_layout()

plt.show()


# --------------------------------------------------
# 8️⃣ Save model + encoders
# --------------------------------------------------

pickle.dump(model, open("models/fertilizer_model.pkl", "wb"))

pickle.dump(soil_encoder, open("models/soil_encoder.pkl", "wb"))
pickle.dump(crop_encoder, open("models/crop_encoder.pkl", "wb"))
pickle.dump(fert_encoder, open("models/fert_encoder.pkl", "wb"))

pickle.dump(n_encoder, open("models/n_encoder.pkl", "wb"))
pickle.dump(p_encoder, open("models/p_encoder.pkl", "wb"))
pickle.dump(k_encoder, open("models/k_encoder.pkl", "wb"))

print("\nModel and encoders saved successfully")