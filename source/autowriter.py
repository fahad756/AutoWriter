import customtkinter as ctk
import pyautogui, time, random, threading

pyautogui.FAILSAFE = True
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SPEEDS = {
    "Slow": (0.12, 0.28), "Medium": (0.05, 0.15),
    "Fast": (0.02, 0.08), "Very Fast": (0.008, 0.03),
}

class AutoWriterApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("AutoWriter")
        self.root.geometry("660x520")
        self.stop_flag = False
        self._build()
        self.root.mainloop()

    def _build(self):
        ctk.CTkLabel(self.root, text="AutoWriter",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(18, 4))
        card = ctk.CTkFrame(self.root)
        card.pack(fill="both", expand=True, padx=22, pady=10)
        ctk.CTkLabel(card, text="Text to type",
                     font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=14, pady=(10, 4))
        self.tb = ctk.CTkTextbox(card, font=ctk.CTkFont(size=12), wrap="word")
        self.tb.pack(fill="both", expand=True, padx=14, pady=(0, 12))

        row = ctk.CTkFrame(self.root, fg_color="transparent")
        row.pack(fill="x", padx=22, pady=(0, 8))
        ctk.CTkLabel(row, text="Speed:").pack(side="left")
        self.spd = ctk.StringVar(value="Medium")
        ctk.CTkOptionMenu(row, values=list(SPEEDS),
                          variable=self.spd, width=130).pack(side="left", padx=8)
        ctk.CTkLabel(row, text="Countdown (sec):").pack(side="left", padx=(16, 0))
        self.cd = ctk.DoubleVar(value=5)
        ctk.CTkSlider(row, from_=3, to=15, number_of_steps=12,
                      variable=self.cd, width=110).pack(side="left", padx=8)

        bf = ctk.CTkFrame(self.root, fg_color="transparent")
        bf.pack(fill="x", padx=22, pady=(0, 8))
        bf.grid_columnconfigure((0, 1), weight=1)
        self.sb = ctk.CTkButton(bf, text="Start Typing", height=44,
                                font=ctk.CTkFont(size=13, weight="bold"),
                                command=self._start)
        self.sb.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        self.xb = ctk.CTkButton(bf, text="Stop", height=44,
                                font=ctk.CTkFont(size=13, weight="bold"),
                                fg_color="#aa1f1f", hover_color="#801818",
                                state="disabled", command=self._stop)
        self.xb.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        self.sv = ctk.StringVar(value="Ready — enter text and click Start Typing")
        ctk.CTkLabel(self.root, textvariable=self.sv, text_color="gray",
                     font=ctk.CTkFont(size=10)).pack(pady=(0, 12))

    def _start(self):
        text = self.tb.get("1.0", "end-1c")
        if not text.strip():
            return
        self.stop_flag = False
        self.sb.configure(state="disabled")
        self.xb.configure(state="normal")
        threading.Thread(target=self._run,
                         args=(text, int(self.cd.get())), daemon=True).start()

    def _run(self, text, cd):
        for i in range(cd, 0, -1):
            if self.stop_flag:
                self._done(True)
                return
            self.root.after(0, lambda i=i: self.sv.set(f"Switch to browser... {i}"))
            time.sleep(1)
        self.root.after(0, lambda: self.sv.set("Typing..."))
        mn, mx = SPEEDS[self.spd.get()]
        for char in text:
            if self.stop_flag:
                break
            if char == "\n":
                pyautogui.press("enter")
                time.sleep(0.28)
            else:
                try:
                    pyautogui.write(char, interval=0)
                except Exception:
                    pass
                time.sleep(random.uniform(mn, mx))
        self._done(self.stop_flag)

    def _done(self, stopped):
        self.stop_flag = False
        self.root.after(0, lambda: self.sv.set("Stopped." if stopped else "Done!"))
        self.root.after(0, lambda: self.sb.configure(state="normal"))
        self.root.after(0, lambda: self.xb.configure(state="disabled"))

    def _stop(self):
        self.stop_flag = True

if __name__ == "__main__":
    AutoWriterApp()
