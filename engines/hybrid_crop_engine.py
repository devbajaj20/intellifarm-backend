import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import pickle
from engines.weather_engine import get_weather

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv("data/crop_dataset.csv")

# Numeric columns (edit to match yours)
FEATURES = ["temperature", "humidity", "ph", "rainfall"]

# Keep usable rows
data = df.dropna(subset=FEATURES + ["label"]).copy()

X = data[FEATURES]
y = data["label"]

# -----------------------------------
# Similarity Model
# -----------------------------------
knn = NearestNeighbors(n_neighbors=10)
knn.fit(X)

# -----------------------------------
# Knowledge Rules
# -----------------------------------
CITY_RULES = {
    "chennai": ["groundnut", "millets", "maize", "rice", "banana"],
    "mumbai": ["rice", "vegetables", "maize"],
    "delhi": ["wheat", "mustard", "maize"]
}

# -----------------------------------
# PARTIAL INPUT ENGINE
# -----------------------------------
def recommend_partial(temp=None, humidity=None, ph=None, rainfall=None):
    query = {
        "temperature": temp if temp is not None else X["temperature"].mean(),
        "humidity": humidity if humidity is not None else X["humidity"].mean(),
        "ph": ph if ph is not None else X["ph"].mean(),
        "rainfall": rainfall if rainfall is not None else X["rainfall"].mean(),
    }

    q = np.array([[query["temperature"], query["humidity"], query["ph"], query["rainfall"]]])

    distances, indices = knn.kneighbors(q)

    crops = y.iloc[indices[0]].value_counts().head(3).index.tolist()

    return crops

# -----------------------------------
# FULL MODEL ENGINE
# -----------------------------------
def recommend_full(features):
    # load your trained model here
    with open("models/cereals_model.pkl", "rb") as f:
        model = pickle.load(f)

    pred = model.predict([features])[0]
    return [pred]

# -----------------------------------
# CITY KNOWLEDGE
# -----------------------------------
def recommend_city(city):
    return CITY_RULES.get(city.lower(), ["rice", "maize", "groundnut"])

# -----------------------------------
# MASTER ROUTER
# -----------------------------------
def recommend_crop(inputs):
    if "city" in inputs:
        return recommend_city(inputs["city"])

    full_keys = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

    if all(k in inputs for k in full_keys):
        return recommend_full([
            inputs["N"], inputs["P"], inputs["K"],
            inputs["temperature"], inputs["humidity"],
            inputs["ph"], inputs["rainfall"]
        ])

    return recommend_partial(
        temp=inputs.get("temperature"),
        humidity=inputs.get("humidity"),
        ph=inputs.get("ph"),
        rainfall=inputs.get("rainfall")
    )

def crop_reply(parsed):
    city = parsed.get("city")

    if city:
        weather = get_weather(city)

        if weather:
            parsed["temperature"] = weather["temperature"]
            parsed["humidity"] = weather["humidity"]
            parsed["rainfall"] = weather["rainfall"]

    crops = recommend_crop(parsed)

    if city:
        return f"Based on current weather in {city.title()}, suitable crops are: {', '.join(crops)}."

    return f"Suitable crops are: {', '.join(crops)}."