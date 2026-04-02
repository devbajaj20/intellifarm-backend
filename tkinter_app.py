import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://127.0.0.1:5000/recommend-crop"

# -------------------------------------------------
# Fetch recommendation
# -------------------------------------------------
def get_recommendation():
    try:
        payload = {
            "category": category_var.get(),
            "N": n_var.get(),
            "P": p_var.get(),
            "K": k_var.get(),
            "temperature": float(temp_var.get()),
            "humidity": float(humidity_var.get()),
            "ph": ph_var.get(),
            "rainfall": float(rainfall_var.get()),
            "soil_type": soil_var.get()
        }

        response = requests.post(API_URL, json=payload)
        data = response.json()

        result_box.config(state="normal")
        result_box.delete("1.0", tk.END)

        for i, rec in enumerate(data["recommendations"], start=1):
            status = rec.get("soil_status", "Conditionally Suitable")

            result_box.insert(
                tk.END,
                f"[{i}]  CROP : {rec['crop'].upper()}\n"
                f"     CONFIDENCE : {rec['confidence']} %\n"
                f"     SOIL STATUS : {status}\n\n"
            )

        result_box.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# -------------------------------------------------
# Root Window (Desktop)
# -------------------------------------------------
root = tk.Tk()
root.title("IntelliFarm – AI Crop Recommendation System")
root.geometry("1250x750")
root.configure(bg="#000000")
root.minsize(1200, 700)

# -------------------------------------------------
# Style (Technical Dark Theme)
# -------------------------------------------------
style = ttk.Style()
style.theme_use("clam")

BG = "#000000"
CARD = "#0d0d0d"
TEXT = "#2e7d32"
ACCENT = "#4caf50"
BORDER = "#1b5e20"

style.configure(".", background=BG, foreground=TEXT)
style.configure("TFrame", background=BG)
style.configure("Card.TFrame", background=CARD, relief="solid", borderwidth=1)

style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 14))
style.configure("Header.TLabel", font=("Segoe UI", 28, "bold"), foreground=ACCENT)
style.configure("Sub.TLabel", font=("Segoe UI", 14), foreground="#81c784")
style.configure("Section.TLabel", font=("Segoe UI", 18, "bold"), foreground=ACCENT)

style.configure("TButton",
                font=("Segoe UI", 14, "bold"),
                background=ACCENT,
                foreground="black",
                padding=12)

style.map("TButton", background=[("active", "#66bb6a")])

style.configure("TCombobox",
                font=("Segoe UI", 14),
                fieldbackground=CARD,
                background=CARD,
                foreground=TEXT)

style.configure("TEntry",
                font=("Segoe UI", 14),
                fieldbackground=CARD,
                foreground=TEXT)

# -------------------------------------------------
# Scrollable Canvas (KEY PART)
# -------------------------------------------------
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Enable mouse wheel scrolling
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# -------------------------------------------------
# Main Centered Container
# -------------------------------------------------
main = ttk.Frame(scrollable_frame)
main.pack(expand=True, pady=30)

# Header
ttk.Label(main, text="INTELLIFARM", style="Header.TLabel").pack()
ttk.Label(main,
          text="AI-Driven Crop Recommendation Dashboard",
          style="Sub.TLabel").pack(pady=(5, 30))

# Content
content = ttk.Frame(main)
content.pack()

# -------------------------------------------------
# Input Card
# -------------------------------------------------
input_card = ttk.Frame(content, style="Card.TFrame", padding=30)
input_card.grid(row=0, column=0, padx=50, sticky="n")

ttk.Label(input_card, text="INPUT PARAMETERS", style="Section.TLabel").pack(pady=(0, 20))

def dropdown(label, var, values):
    ttk.Label(input_card, text=label).pack(anchor="w", pady=(10, 4))
    ttk.Combobox(input_card, textvariable=var,
                 values=values, state="readonly",
                 width=32).pack()

category_var = tk.StringVar(value="cereals")
n_var = tk.StringVar(value="medium")
p_var = tk.StringVar(value="medium")
k_var = tk.StringVar(value="medium")
ph_var = tk.StringVar(value="neutral")
soil_var = tk.StringVar(value="clay loam")

temp_var = tk.StringVar(value="28")
humidity_var = tk.StringVar(value="75")
rainfall_var = tk.StringVar(value="180")

dropdown("Crop Category", category_var,
         ["cereals", "pulses", "vegetables", "fruits", "oilseeds", "cash"])
dropdown("Nitrogen (N)", n_var, ["low", "medium", "high"])
dropdown("Phosphorus (P)", p_var, ["low", "medium", "high"])
dropdown("Potassium (K)", k_var, ["low", "medium", "high"])
dropdown("Soil pH", ph_var, ["acidic", "neutral", "alkaline"])
dropdown("Soil Type", soil_var,
         ["clay loam", "loamy", "sandy", "black soil", "alluvial soil"])

ttk.Label(input_card, text="Temperature (°C)").pack(anchor="w", pady=(10, 4))
ttk.Entry(input_card, textvariable=temp_var, width=34).pack()

ttk.Label(input_card, text="Humidity (%)").pack(anchor="w", pady=(10, 4))
ttk.Entry(input_card, textvariable=humidity_var, width=34).pack()

ttk.Label(input_card, text="Rainfall (mm)").pack(anchor="w", pady=(10, 4))
ttk.Entry(input_card, textvariable=rainfall_var, width=34).pack()

ttk.Button(input_card,
           text="RUN AI RECOMMENDATION",
           command=get_recommendation).pack(pady=25)

# -------------------------------------------------
# Output Card
# -------------------------------------------------
output_card = ttk.Frame(content, style="Card.TFrame", padding=30)
output_card.grid(row=0, column=1, padx=50, sticky="n")

ttk.Label(output_card, text="MODEL OUTPUT", style="Section.TLabel").pack(pady=(0, 20))

result_box = tk.Text(
    output_card,
    height=18,
    width=55,
    font=("Consolas", 14),
    bg="#000000",
    fg=TEXT,
    insertbackground=TEXT,
    state="disabled",
    relief="solid",
    borderwidth=1
)
result_box.pack()

# -------------------------------------------------
# Footer
# -------------------------------------------------
ttk.Label(main,
          text="IntelliFarm © 2026 | Machine Learning Based Decision Support System",
          font=("Segoe UI", 11),
          foreground="#66bb6a").pack(pady=30)

root.mainloop()
