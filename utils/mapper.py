def map_user_inputs(data):
    level_map = {
        "low": 40,
        "medium": 90,
        "high": 140
    }

    ph_map = {
        "acidic": 5.5,
        "neutral": 7.0,
        "alkaline": 8.5
    }

    try:
        return [
            level_map[data["N"].lower()],
            level_map[data["P"].lower()],
            level_map[data["K"].lower()],
            float(data["temperature"]),
            float(data["humidity"]),
            ph_map[data["ph"].lower()],
            float(data["rainfall"])
        ]
    except KeyError as e:
        raise ValueError(f"Invalid input value: {e}")
