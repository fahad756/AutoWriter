import tkinter as tk
from tkinter import scrolledtext
import pyautogui, time, threading

pyautogui.FAILSAFE = True

def do_type():
    text = text_area.get("1.0", "end-1c")
    for char in text:
        if char == "\n":
            pyautogui.press("enter")
        else:
            pyautogui.write(char, interval=0)
        time.sleep(0.07)

root = tk.Tk()
root.title("AutoWriter")
root.geometry("600x480")

text_area = scrolledtext.ScrolledText(root, height=12, font=("Segoe UI", 11))
text_area.pack(fill="both", expand=True, padx=20, pady=20)

tk.Button(
    root, text="Start Typing",
    command=lambda: threading.Thread(target=do_type, daemon=True).start(),
    font=("Segoe UI", 12), padx=20, pady=8,
    bg="#2980b9", fg="white", relief="flat"
).pack(pady=10)

root.mainloop()
