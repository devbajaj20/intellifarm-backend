from flask import Blueprint, request, jsonify
from chatbot.chatbot import get_chat_response

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400

        reply = get_chat_response(message)

        return jsonify({
            "success": True,
            "user": message,
            "reply": reply
        }), 200

    except Exception as e:
        print("Chat Route Error:", e)

        return jsonify({
            "success": False,
            "error": "Unable to process request"
        }), 500