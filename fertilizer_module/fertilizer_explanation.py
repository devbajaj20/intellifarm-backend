def explain_fertilizer(N,P,K,fertilizer):

    reasons = []

    if N < 40:
        reasons.append("Nitrogen level is low")

    if P < 40:
        reasons.append("Phosphorus level is low")

    if K < 40:
        reasons.append("Potassium level is low")

    info = {

        "Urea":"Urea supplies nitrogen for leaf growth",

        "DAP":"DAP improves root development",

        "MOP":"MOP provides potassium for strong crops",

        "17-17-17":"Balanced fertilizer for overall growth",

        "20-20":"Balanced fertilizer for healthy crops",

        "28-28":"High phosphorus fertilizer for root development"

    }

    return ", ".join(reasons) + ". " + info.get(fertilizer,"")