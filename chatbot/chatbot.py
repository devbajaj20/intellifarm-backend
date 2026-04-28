from chatbot.nlp_parser import parse_query
from engines.hybrid_crop_engine import crop_reply
from engines.fertilizer_engine import fertilizer_reply
from rag.rag_engine import ask_rag
from chatbot.memory import update_memory, get_memory, clear_memory


# -----------------------------------
# MAIN CHATBOT ENTRY
# -----------------------------------

def get_chat_response(user_message):
    msg = user_message.lower().strip()

    # -----------------------------------
    # RESET MEMORY
    # -----------------------------------
    if msg in ["reset", "clear memory", "forget details"]:
        clear_memory()
        return "I've cleared your saved farming details."

    # -----------------------------------
    # GREETING
    # -----------------------------------
    if msg in ["hi", "hello", "hey"]:
        return (
            "Hello 👋 I am IntelliFarm AI. "
            "Ask me about crops, fertilizer, disease, or farming guidance."
        )

    # -----------------------------------
    # PARSE USER QUERY
    # -----------------------------------
    parsed = parse_query(user_message)

    # -----------------------------------
    # STORE NEW MEMORY
    # -----------------------------------
    update_memory(parsed)

    # -----------------------------------
    # LOAD MEMORY
    # -----------------------------------
    memory = get_memory()

    # -----------------------------------
    # CHECK IF USER PROVIDED NUMERIC DATA
    # If yes, don't force old city memory
    # -----------------------------------
    has_numeric = any([
        parsed.get("temperature") is not None,
        parsed.get("humidity") is not None,
        parsed.get("rainfall") is not None,
        parsed.get("ph") is not None
    ])

    # -----------------------------------
    # MERGE MEMORY INTO MISSING FIELDS
    # -----------------------------------
    for key in ["city", "soil", "crop"]:
        if not parsed.get(key):

            # If numbers given, skip remembered city
            if key == "city" and has_numeric:
                continue

            if memory.get(key):
                parsed[key] = memory[key]

    # -----------------------------------
    # ROUTING BY INTENT
    # -----------------------------------
    intent = parsed["intent"]

    # Crop Recommendation
    if intent == "crop":
        return crop_reply(parsed)

    # Fertilizer Recommendation
    if intent == "fertilizer":
        return fertilizer_reply(parsed)

    # Advice / Knowledge Queries
    if intent == "advice":
        return ask_rag(user_message)

    # Disease Module
    if intent == "disease":
        return (
            "Disease detection module is being integrated. "
            "Soon you can upload leaf images for diagnosis."
        )

    # Default fallback = RAG
    return ask_rag(user_message)