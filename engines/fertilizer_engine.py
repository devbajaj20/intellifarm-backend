import requests
from rag.rag_engine import ask_rag

BASE_URL = "http://127.0.0.1:10000"

# -----------------------------------
# VALID DATASET VALUES
# -----------------------------------

CROP_MAP = {
    "rice": "rice",
    "maize": "maize",
    "cotton": "cotton",
    "groundnut": "groundnut",
    "wheat": "wheat",
    "banana": "banana",
    "tomato": "tomato",
    "potato": "potato",
    "onion": "onion"
}

SOIL_MAP = {
    "loamy": "loamy soil",
    "loam": "loamy soil",
    "black": "black soil",
    "sandy": "sandy loam",
    "sand": "sandy loam",
    "clay": "clay loam",
    "alluvial": "alluvial soil",
    "laterite": "laterite soil"
}


# -----------------------------------
# EXTRACT WORD FROM QUERY
# -----------------------------------

def extract_from_map(msg, mapping):
    for key in mapping:
        if key in msg:
            return mapping[key]
    return None


# -----------------------------------
# MAIN FERTILIZER REPLY
# -----------------------------------

def fertilizer_reply(parsed):
    msg = msg.lower()

    # -----------------------------------
    # HOW / WHY / WHEN QUESTIONS -> RAG
    # -----------------------------------
    if any(x in msg for x in [
        "how", "why", "when",
        "apply", "use", "dosage"
    ]):
        return ask_rag(msg)

    # -----------------------------------
    # EXTRACT CROP + SOIL
    # -----------------------------------
    crop = extract_from_map(msg, CROP_MAP) or "rice"
    soil = extract_from_map(msg, SOIL_MAP) or "loamy soil"

    # -----------------------------------
    # Nutrient levels
    # -----------------------------------
    n = "low" if "low nitrogen" in msg else "medium"
    p = "low" if "low phosphorus" in msg else "medium"
    k = "low" if "low potassium" in msg else "medium"

    payload = {
        "soil_type": soil,
        "crop": crop,
        "N_level": n,
        "P_level": p,
        "K_level": k,
        "temperature": 30,
        "humidity": 70,
        "ph": 6.5,
        "rainfall": 110
    }

    try:
        res = requests.post(
            f"{BASE_URL}/recommend-fertilizer",
            json=payload,
            timeout=5
        )

        data = res.json()

        if "recommendations" in data:
            top = data["recommendations"][0]

            return (
                f"For {crop} in {soil}, recommended fertilizer is "
                f"{top['fertilizer']} "
                f"with {top['confidence']}% confidence."
            )

        return "Unable to get fertilizer recommendation."

    except Exception as e:
        print("Fertilizer Engine Error:", e)

        return (
            f"For {crop}, apply balanced NPK fertilizer "
            f"after soil testing."
        )