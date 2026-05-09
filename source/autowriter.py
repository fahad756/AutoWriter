import tkinter as tk
from tkinter import scrolledtext
import pyautogui, time, threading

pyautogui.FAILSAFE = True
stop_flag = False

root = tk.Tk()
root.title("AutoWriter")
root.geometry("620x520")

text_area = scrolledtext.ScrolledText(root, height=11, font=("Segoe UI", 11))
text_area.pack(fill="both", expand=True, padx=20, pady=(20, 10))

status_var = tk.StringVar(value="Ready")
tk.Label(root, textvariable=status_var, fg="gray").pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

def run_typing(text, cd):
    global stop_flag
    for i in range(cd, 0, -1):
        if stop_flag:
            status_var.set("Stopped.")
            return
        status_var.set(f"Switch to browser and click target... {i}")
        time.sleep(1)
    status_var.set("Typing...")
    for char in text:
        if stop_flag:
            break
        if char == "\n":
            pyautogui.press("enter")
        else:
            pyautogui.write(char, interval=0)
        time.sleep(0.07)
    status_var.set("Stopped." if stop_flag else "Done!")
    start_btn.config(state="normal")
    stop_btn.config(state="disabled")

def start():
    global stop_flag
    text = text_area.get("1.0", "end-1c")
    if not text.strip():
        return
    stop_flag = False
    start_btn.config(state="disabled")
    stop_btn.config(state="normal")
    threading.Thread(target=run_typing, args=(text, 5), daemon=True).start()

def stop():
    global stop_flag
    stop_flag = True

start_btn = tk.Button(btn_frame, text="Start Typing", command=start,
                      font=("Segoe UI", 12), padx=20, pady=8,
                      bg="#2980b9", fg="white", relief="flat")
start_btn.pack(side="left", padx=5)

stop_btn = tk.Button(btn_frame, text="Stop", command=stop,
                     font=("Segoe UI", 12), padx=20, pady=8,
                     bg="#c0392b", fg="white", relief="flat", state="disabled")
stop_btn.pack(side="left", padx=5)

root.mainloop()
