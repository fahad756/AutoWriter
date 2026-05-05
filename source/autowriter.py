import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("AutoWriter")
root.geometry("600x450")

tk.Label(root, text="AutoWriter", font=("Segoe UI", 18, "bold")).pack(pady=20)
tk.Label(root, text="Text to type:").pack(anchor="w", padx=20)

text_area = scrolledtext.ScrolledText(root, height=14, font=("Segoe UI", 11))
text_area.pack(fill="both", expand=True, padx=20, pady=(5, 20))

root.mainloop()
