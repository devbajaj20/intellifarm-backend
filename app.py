from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os
from utils.mapper import map_user_inputs
from chatbot.routes import chatbot_bp
from services.llm_service import ask_llm
from dotenv import load_dotenv
from fertilizer_calculator import fert_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(chatbot_bp)
app.register_blueprint(fert_bp)
# --------------------------------------------------
# 1️⃣ Load dataset ONCE
# --------------------------------------------------
DATASET_PATH = "data/crop_dataset.csv"

if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError("❌ data/crop_dataset.csv not found")

DATASET = pd.read_csv(DATASET_PATH)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# --------------------------------------------------
# Fertilizer model path
# --------------------------------------------------

# --------------------------------------------------
# Fertilizer models + encoders
# --------------------------------------------------

FERT_MODEL_PATH = os.path.join(BASE_DIR, "models", "fertilizer_model.pkl")
SOIL_ENCODER_PATH = os.path.join(BASE_DIR, "models", "soil_encoder.pkl")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "models", "crop_encoder.pkl")
FERT_ENCODER_PATH = os.path.join(BASE_DIR, "models", "fert_encoder.pkl")
N_ENCODER_PATH = os.path.join(BASE_DIR, "models", "n_encoder.pkl")
P_ENCODER_PATH = os.path.join(BASE_DIR, "models", "p_encoder.pkl")
K_ENCODER_PATH = os.path.join(BASE_DIR, "models", "k_encoder.pkl")

with open(FERT_MODEL_PATH, "rb") as f:
    fertilizer_model = pickle.load(f)

with open(SOIL_ENCODER_PATH, "rb") as f:
    soil_encoder = pickle.load(f)

with open(CROP_ENCODER_PATH, "rb") as f:
    crop_encoder = pickle.load(f)

with open(FERT_ENCODER_PATH, "rb") as f:
    fert_encoder = pickle.load(f)

with open(N_ENCODER_PATH, "rb") as f:
    n_encoder = pickle.load(f)

with open(P_ENCODER_PATH, "rb") as f:
    p_encoder = pickle.load(f)

with open(K_ENCODER_PATH, "rb") as f:
    k_encoder = pickle.load(f)

# --------------------------------------------------
# 2️⃣ Model paths
# --------------------------------------------------
MODEL_PATHS = {
    "cereals": os.path.join(BASE_DIR, "models", "cereals_model.pkl"),
    "pulses": os.path.join(BASE_DIR, "models", "pulses_model.pkl"),
    "oilseeds": os.path.join(BASE_DIR, "models", "oilseeds_model.pkl"),
    "fruits": os.path.join(BASE_DIR, "models", "fruits_model.pkl"),
    "vegetables": os.path.join(BASE_DIR, "models", "vegetables_model.pkl"),
    "cash": os.path.join(BASE_DIR, "models", "cash_model.pkl")
}

# --------------------------------------------------
# 3️⃣ REAL-WORLD Soil Advisory Logic
# --------------------------------------------------
def soil_status(user_soil, crop):
    rows = DATASET[DATASET["label"] == crop]

    # Safety: crop not found
    if rows.empty:
        return "Conditionally Suitable"

    row = rows.iloc[0]

    soil1 = str(row["soil_type_1"]).lower()
    soil2 = str(row["soil_type_2"]).lower()

    # Missing soil info → manageable
    if soil1 == "unknown" and soil2 == "unknown":
        return "Suitable"

    user_words = set(user_soil.lower().split())
    soil_words = set(soil1.split()) | set(soil2.split())

    # Partial match → Suitable
    if len(user_words & soil_words) > 0:
        return "Suitable"

    # Real-life case → advisory, not rejection
    return "Conditionally Suitable"

def call_llm(prompt: str) -> str:
    try:
        return ask_llm(
            messages=[
                {
                    "role": "system",
                    "content": "You are an agricultural expert helping farmers make crop decisions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temp=0.6,
            tokens=120
        )

    except Exception as e:
        print("LLM Error:", e)
        return (
            "This crop suits your soil and climate conditions well. "
            "With proper irrigation and nutrient management, it can give good yield."
        )
    
def detect_deficiency(n, p, k):

    if n == "low":
        return "Nitrogen deficiency"
    if p == "low":
        return "Phosphorus deficiency"
    if k == "low":
        return "Potassium deficiency"

    return "Balanced nutrients"

def explain_fertilizer(crop, n_level, p_level, k_level, fertilizer):

    prompt = f"""
You are an agricultural expert.

Explain why the fertilizer {fertilizer} is recommended.

Crop: {crop}
Nitrogen level: {n_level}
Phosphorus level: {p_level}
Potassium level: {k_level}

Give:
1. Reason
2. Recommended dosage per acre
3. Practical farmer advice

Keep response short.
"""

    try:
        return ask_llm(
            messages=[
                {"role": "user", "content": prompt}
            ],
            tokens=120
        )

    except Exception as e:
        print("Fertilizer LLM Error:", e)
        return "Recommended fertilizer based on soil nutrient balance."
# --------------------------------------------------
# 4️⃣ Health check
# --------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "IntelliFarm Crop Recommendation API is running"
    })


@app.route("/explain-crop", methods=["POST"])
def explain_crop():
    data = request.json

    prompt = f"""
You are an agricultural expert AI.

Explain in simple farmer-friendly language:
Why is the crop "{data['crop']}" recommended?

Details:
- Soil type: {data['soil']}
- Nitrogen: {data['N']}
- Phosphorus: {data['P']}
- Potassium: {data['K']}
- Temperature: {data['temperature']}°C
- Humidity: {data['humidity']}%
- Rainfall: {data['rainfall']} mm
- Confidence score: {data['confidence']}%

Keep it short, practical, and helpful.
"""

    explanation = call_llm(prompt)  # OpenAI / Azure / Local LLM

    return jsonify({
        "explanation": explanation
    })


# --------------------------------------------------
# 5️⃣ Recommendation API
# --------------------------------------------------
@app.route("/recommend-crop", methods=["POST"])
def recommend_crop():
    try:
        data = request.get_json()

        category = data["category"].lower()
        user_soil = data["soil_type"].lower()

        if category not in MODEL_PATHS:
            return jsonify({"error": "Invalid crop category"}), 400

        # Map inputs
        features = map_user_inputs(data)

        model_path = MODEL_PATHS[category]
        if not os.path.exists(model_path):
            return jsonify({"error": "Model not found"}), 500

        with open(model_path, "rb") as f:
            model = pickle.load(f)

        # Predict
        probs = model.predict_proba([features])[0]
        classes = model.classes_

        top3_idx = np.argsort(probs)[-3:][::-1]

        recommendations = []
        for i in top3_idx:
            crop = classes[i]
            recommendations.append({
                "crop": crop,
                "confidence": round(probs[i] * 100, 2),
                "soil_status": soil_status(user_soil, crop)
            })

        return jsonify({
            "category": category,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({
            "error": "Invalid input data",
            "details": str(e)
        }), 400

# --------------------------------------------------
# METADATA API (FOR FLUTTER – FUTURE PROOF)
# --------------------------------------------------
@app.route("/metadata", methods=["GET"])
def metadata():
    return jsonify({
        "categories": list(MODEL_PATHS.keys()),
        "nutrient_levels": ["low", "medium", "high"],
        "ph_levels": ["acidic", "neutral", "alkaline"],
        "soil_types": sorted(
            set(
                DATASET["soil_type_1"].dropna().tolist() +
                DATASET["soil_type_2"].dropna().tolist()
            )
        )
    })

# --------------------------------------------------
# Fertilizer Recommendation API
# --------------------------------------------------

@app.route("/recommend-fertilizer", methods=["POST"])
def recommend_fertilizer():

    try:

        data = request.get_json()

        print("Incoming fertilizer payload:", data)

        # --------------------------------------------------
        # Encode categorical inputs
        # --------------------------------------------------

        soil = soil_encoder.transform([data["soil_type"].lower()])[0]
        crop = crop_encoder.transform([data["crop"].lower()])[0]

        n_level = n_encoder.transform([data["N_level"].lower()])[0]
        p_level = p_encoder.transform([data["P_level"].lower()])[0]
        k_level = k_encoder.transform([data["K_level"].lower()])[0]

        # --------------------------------------------------
        # Prepare feature vector
        # --------------------------------------------------

        features = np.array([[

            soil,
            crop,
            n_level,
            p_level,
            k_level,

            float(data["temperature"]),
            float(data["humidity"]),
            float(data["ph"]),
            float(data["rainfall"])

        ]])

        # --------------------------------------------------
        # Predict probabilities
        # --------------------------------------------------

        probs = fertilizer_model.predict_proba(features)[0]
        classes = fertilizer_model.classes_

        # Get top 3 fertilizers
        top3_idx = np.argsort(probs)[-3:][::-1]

        recommendations = []

        for i in top3_idx:

            fertilizer_name = fert_encoder.inverse_transform([classes[i]])[0]

            recommendations.append({
                "fertilizer": fertilizer_name,
                "confidence": round(probs[i] * 100, 2)
            })

        # --------------------------------------------------
        # Detect nutrient deficiency
        # --------------------------------------------------

        deficiency = detect_deficiency(
            data["N_level"],
            data["P_level"],
            data["K_level"]
        )

        # --------------------------------------------------
        # AI explanation (for best fertilizer)
        # --------------------------------------------------

        explanation = explain_fertilizer(
            data["crop"],
            data["N_level"],
            data["P_level"],
            data["K_level"],
            recommendations[0]["fertilizer"]
        )

        # --------------------------------------------------
        # Return response
        # --------------------------------------------------

        return jsonify({

            "nutrient_status": deficiency,
            "recommendations": recommendations,
            "explanation": explanation

        })

    except Exception as e:

        print("Fertilizer API error:", e)

        return jsonify({
            "error": "Invalid fertilizer input",
            "details": str(e)
        }), 400
# --------------------------------------------------
# 6️⃣ Run server
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)