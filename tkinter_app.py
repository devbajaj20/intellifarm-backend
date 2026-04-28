import tkinter as tk
from tkinter import scrolledtext
import requests

API_URL = "http://127.0.0.1:10000/chat"   # Flask backend


def send_message():
    user_msg = entry_box.get().strip()

    if not user_msg:
        return

    chat_area.insert(tk.END, f"You: {user_msg}\n")
    entry_box.delete(0, tk.END)

    try:
        response = requests.post(
            API_URL,
            json={"message": user_msg}
        )

        data = response.json()

        bot_reply = data.get("reply", "No reply")

    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    chat_area.insert(tk.END, f"IntelliFarm AI: {bot_reply}\n\n")
    chat_area.see(tk.END)


# Main Window
root = tk.Tk()
root.title("IntelliFarm Chatbot Test")
root.geometry("700x550")
root.config(bg="#e8f5e9")

# Heading
title = tk.Label(
    root,
    text="🌱 IntelliFarm AI Assistant",
    font=("Arial", 18, "bold"),
    bg="#2e7d32",
    fg="white",
    pady=10
)
title.pack(fill="x")

# Chat Area
chat_area = scrolledtext.ScrolledText(
    root,
    wrap=tk.WORD,
    font=("Arial", 12),
    height=25
)
chat_area.pack(padx=10, pady=10, fill="both", expand=True)

# Input Frame
bottom_frame = tk.Frame(root, bg="#e8f5e9")
bottom_frame.pack(fill="x", padx=10, pady=10)

entry_box = tk.Entry(
    bottom_frame,
    font=("Arial", 12)
)
entry_box.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=8)

send_btn = tk.Button(
    bottom_frame,
    text="Send",
    font=("Arial", 12, "bold"),
    bg="#43a047",
    fg="white",
    padx=20,
    command=send_message
)
send_btn.pack(side="right")

entry_box.bind("<Return>", lambda event: send_message())

root.mainloop()