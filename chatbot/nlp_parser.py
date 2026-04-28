import re
from rapidfuzz import process, fuzz

# -----------------------------------
# Vocabulary
# -----------------------------------

CROPS = [
    "rice",
    "maize",
    "cotton",
    "groundnut",
    "wheat",
    "banana",
    "tomato",
    "potato",
    "onion",
    "millets"
]

SOILS = [
    "red soil",
    "black soil",
    "loamy soil",
    "clay loam",
    "sandy loam",
    "alluvial soil",
    "laterite soil"
]

CITIES = [
    "chennai",
    "mumbai",
    "delhi",
    "bangalore",
    "hyderabad",
    "kolkata",
    "pune",
    "coimbatore"
]

ALL_WORDS = CROPS + SOILS + CITIES + [
    "crop",
    "fertilizer",
    "nitrogen",
    "phosphorus",
    "potassium",
    "weather",
    "disease",
    "leaf",
    "spots",
    "yellow",
    "grow",
    "plant",
    "sow"
]

# -----------------------------------
# Normalize
# -----------------------------------

def normalize(text):
    return text.lower().strip()


# -----------------------------------
# Tokenize
# -----------------------------------

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


# -----------------------------------
# Spelling Correction
# -----------------------------------

def correct_token(word):
    match = process.extractOne(word, ALL_WORDS, scorer=fuzz.ratio)

    if match and match[1] >= 80:
        return match[0]

    return word


# -----------------------------------
# Entity Extraction
# -----------------------------------

def extract_crop(msg):
    for crop in CROPS:
        if crop in msg:
            return crop
    return None


def extract_soil(msg):
    # Exact phrase first
    for soil in SOILS:
        if soil in msg:
            return soil

    # Smart fallback words
    if "red" in msg:
        return "red soil"

    if "black" in msg:
        return "black soil"

    if "loamy" in msg or "loam" in msg:
        return "loamy soil"

    if "sandy" in msg:
        return "sandy loam"

    if "clay" in msg:
        return "clay loam"

    if "alluvial" in msg:
        return "alluvial soil"

    if "laterite" in msg:
        return "laterite soil"

    return None


def extract_city(msg):
    for city in CITIES:
        if city in msg:
            return city
    return None


# -----------------------------------
# Nutrient Parsing
# -----------------------------------

def extract_nutrients(msg):
    result = {
        "N_level": "medium",
        "P_level": "medium",
        "K_level": "medium"
    }

    # Nitrogen
    if "low nitrogen" in msg:
        result["N_level"] = "low"
    elif "high nitrogen" in msg:
        result["N_level"] = "high"

    # Phosphorus
    if "low phosphorus" in msg:
        result["P_level"] = "low"
    elif "high phosphorus" in msg:
        result["P_level"] = "high"

    # Potassium
    if "low potassium" in msg:
        result["K_level"] = "low"
    elif "high potassium" in msg:
        result["K_level"] = "high"

    return result


# -----------------------------------
# Numeric Extraction
# -----------------------------------

def extract_temperature(msg):
    match = re.search(r"(temp|temperature)\s*(is|=)?\s*(\d+)", msg)
    return float(match.group(3)) if match else None


def extract_humidity(msg):
    match = re.search(r"(humidity)\s*(is|=)?\s*(\d+)", msg)
    return float(match.group(3)) if match else None


def extract_rainfall(msg):
    match = re.search(r"(rainfall|rain)\s*(is|=)?\s*(\d+)", msg)
    return float(match.group(3)) if match else None


def extract_ph(msg):
    match = re.search(r"(ph)\s*(is|=)?\s*(\d+(\.\d+)?)", msg)
    return float(match.group(3)) if match else None


# -----------------------------------
# Intent Detection
# -----------------------------------

def detect_intent(msg):
    msg = msg.lower()

    # Advice / Explanation
    if any(x in msg for x in [
        "how", "why", "when",
        "apply", "use", "dosage"
    ]):
        return "advice"

    # Disease
    if any(x in msg for x in [
        "leaf", "spots", "yellow",
        "curling", "disease"
    ]):
        return "disease"

    # Fertilizer
    if any(x in msg for x in [
        "fertilizer",
        "urea",
        "dap",
        "mop",
        "nitrogen",
        "phosphorus",
        "potassium",
        "npk"
    ]):
        return "fertilizer"

    # Crop
    if any(x in msg for x in [
        "crop",
        "grow",
        "plant",
        "sow",
        "cultivate",
        "best crop",
        "best for",
        "suitable",
        "farming"
    ]):
        return "crop"

    # Smart fallback:
    # city / soil / weather numbers usually means crop query
    if extract_city(msg) or extract_soil(msg):
        return "crop"

    if (
        extract_temperature(msg) is not None or
        extract_humidity(msg) is not None or
        extract_rainfall(msg) is not None
    ):
        return "crop"

    return "general"


# -----------------------------------
# Main Parser
# -----------------------------------

def parse_query(user_message):
    msg = normalize(user_message)

    # Tokenize + spelling correction
    tokens = tokenize(msg)
    corrected_tokens = [correct_token(t) for t in tokens]

    # Corrected sentence
    token_msg = " ".join(corrected_tokens)

    data = {
        "intent": detect_intent(token_msg),

        # Use corrected text for words
        "crop": extract_crop(token_msg),
        "soil": extract_soil(token_msg),
        "city": extract_city(token_msg),

        # Use raw text for numbers
        "temperature": extract_temperature(msg),
        "humidity": extract_humidity(msg),
        "rainfall": extract_rainfall(msg),
        "ph": extract_ph(msg)
    }

    data.update(extract_nutrients(token_msg))

    return data