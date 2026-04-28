from flask import Blueprint, request, jsonify
import pandas as pd

fert_bp = Blueprint("fert_bp", __name__)

try:
    df = pd.read_excel("data/fertilizer_calculation.xlsx")
except FileNotFoundError:
    raise RuntimeError("Fertilizer dataset not found at data/fertilizer_calculation.xlsx")


@fert_bp.route("/calculate-fertilizer", methods=["POST"])
def calculate_fertilizer():

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    required = ["crop", "area", "soil_n", "soil_p", "soil_k"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    try:
        crop    = str(data["crop"]).lower().strip()
        area    = float(data["area"])
        soil_n  = float(data["soil_n"])
        soil_p  = float(data["soil_p"])
        soil_k  = float(data["soil_k"])
    except (ValueError, TypeError):
        return jsonify({"error": "area, soil_n, soil_p, soil_k must be valid numbers"}), 400

    if area <= 0:
        return jsonify({"error": "area must be a positive number"}), 400

    matches = df[df["crop"].str.lower() == crop]
    if matches.empty:
        return jsonify({"error": f"Crop '{crop}' not found in dataset"}), 404

    row = matches.iloc[0]

    n_def = max(0, row["N_target"] - soil_n)
    p_def = max(0, row["P_target"] - soil_p)
    k_def = max(0, row["K_target"] - soil_k)

    urea = float(round((n_def / 0.46) * area, 2))
    dap  = float(round((p_def / 0.46) * area, 2))
    mop  = float(round((k_def / 0.60) * area, 2))

    return jsonify({
        "crop": crop,
        "area_ha": area,
        "urea_kg": urea,
        "dap_kg": dap,
        "mop_kg": mop,
        "organic_option": row["organic_option"],
        "split_schedule": row["split_schedule"],
        "ph_range": f"{row['ph_min']} – {row['ph_max']}",
        "preferred_soil": row["preferred_soil"]
    }), 200