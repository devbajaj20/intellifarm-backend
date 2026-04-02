from flask import Blueprint,request,jsonify

from fertilizer_module.fertilizer_predict import predict_fertilizer
from fertilizer_module.fertilizer_explanation import explain_fertilizer

fertilizer_bp = Blueprint("fertilizer",__name__)

@fertilizer_bp.route("/fertilizer-predict",methods=["POST"])
def fertilizer_predict():

    data = request.json

    fertilizer = predict_fertilizer(data)

    reason = explain_fertilizer(
        data["N"],
        data["P"],
        data["K"],
        fertilizer
    )

    return jsonify({

        "recommended_fertilizer":fertilizer,
        "reason":reason

    })