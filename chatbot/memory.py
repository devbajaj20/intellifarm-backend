# Simple in-memory session store

USER_MEMORY = {
    "city": None,
    "soil": None,
    "crop": None
}


def update_memory(parsed):
    for key in ["city", "soil", "crop"]:
        if parsed.get(key):
            USER_MEMORY[key] = parsed[key]


def get_memory():
    return USER_MEMORY.copy()


def clear_memory():
    USER_MEMORY["city"] = None
    USER_MEMORY["soil"] = None
    USER_MEMORY["crop"] = None