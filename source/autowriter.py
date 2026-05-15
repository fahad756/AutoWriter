import customtkinter as ctk
import tkinter as tk
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
        self.root.geometry("700x560")
        self.root.minsize(600, 480)
        self.stop_flag = False
        self._ph = True
        self._build()
        self.root.mainloop()

    def _build(self):
        ctk.CTkLabel(self.root, text="AutoWriter",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(18, 4))

        ec = ctk.CTkFrame(self.root)
        ec.pack(fill="both", expand=True, padx=22, pady=10)
        ec.grid_columnconfigure(0, weight=1)
        ec.grid_rowconfigure(1, weight=1)

        # Formatting toolbar
        tb = ctk.CTkFrame(ec, height=40, fg_color="#141922")
        tb.grid(row=0, column=0, columnspan=2, sticky="ew")
        tb.grid_propagate(False)
        tbl = ctk.CTkFrame(tb, fg_color="transparent")
        tbl.pack(side="left", padx=8, pady=6)
        for lbl, tag in [("B", "bold"), ("I", "italic"), ("U", "underline"),
                         ("H1", "h1"), ("H2", "h2")]:
            ctk.CTkButton(tbl, text=lbl, width=32, height=26,
                          font=ctk.CTkFont(size=11, weight="bold"),
                          fg_color="#1e2533", hover_color="#2e3d5c", corner_radius=5,
                          command=lambda t=tag: self._fmt(t)).pack(side="left", padx=2)
        ctk.CTkLabel(tbl, text="|", text_color="#333",
                     font=ctk.CTkFont(size=16)).pack(side="left", padx=5)
        for lbl, ev in [("Undo", "<<Undo>>"), ("Redo", "<<Redo>>")]:
            ctk.CTkButton(tbl, text=lbl, width=42, height=26,
                          font=ctk.CTkFont(size=10), fg_color="#1e2533",
                          hover_color="#2e3d5c", corner_radius=5,
                          command=lambda e=ev: self.editor.event_generate(e)
                          ).pack(side="left", padx=2)
        self.char_lbl = ctk.CTkLabel(tb, text="0 chars",
                                     font=ctk.CTkFont(size=10), text_color="#444")
        self.char_lbl.pack(side="right", padx=12)

        self.editor = tk.Text(ec, bg="#0a1020", fg="#c4cce0",
                              insertbackground="#4f8ef7", font=("Segoe UI", 12),
                              relief="flat", wrap="word", padx=14, pady=10, undo=True)
        self.editor.grid(row=1, column=0, sticky="nsew")
        self.editor.tag_configure("bold",      font=("Segoe UI", 12, "bold"))
        self.editor.tag_configure("italic",    font=("Segoe UI", 12, "italic"))
        self.editor.tag_configure("underline", underline=True)
        self.editor.tag_configure("h1",        font=("Segoe UI", 20, "bold"), spacing1=8)
        self.editor.tag_configure("h2",        font=("Segoe UI", 15, "bold"), spacing1=4)
        self.editor.tag_configure("ph",        foreground="#2a3050")
        self.editor.insert("1.0", "Type or paste your text here...")
        self.editor.tag_add("ph", "1.0", "end")
        self.editor.bind("<FocusIn>", self._clr)
        self.editor.bind("<KeyRelease>",
                         lambda e: self.char_lbl.configure(
                             text=f"{len(self.editor.get('1.0','end-1c'))} chars"))
        vsb = ctk.CTkScrollbar(ec, command=self.editor.yview)
        vsb.grid(row=1, column=1, sticky="ns")
        self.editor.configure(yscrollcommand=vsb.set)

        row = ctk.CTkFrame(self.root, fg_color="transparent")
        row.pack(fill="x", padx=22, pady=(4, 8))
        ctk.CTkLabel(row, text="Speed:").pack(side="left")
        self.spd = ctk.StringVar(value="Medium")
        ctk.CTkOptionMenu(row, values=list(SPEEDS),
                          variable=self.spd, width=130).pack(side="left", padx=8)
        ctk.CTkLabel(row, text="Countdown:").pack(side="left", padx=(16, 0))
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
        self.sv = ctk.StringVar(value="Ready — paste text above, then click Start Typing")
        ctk.CTkLabel(self.root, textvariable=self.sv, text_color="gray",
                     font=ctk.CTkFont(size=10)).pack(pady=(0, 12))

    def _clr(self, _=None):
        if self._ph:
            self.editor.delete("1.0", "end")
            self.editor.tag_remove("ph", "1.0", "end")
            self._ph = False

    def _fmt(self, tag):
        try:
            s, e = self.editor.index("sel.first"), self.editor.index("sel.last")
            if tag in self.editor.tag_names(s):
                self.editor.tag_remove(tag, s, e)
            else:
                self.editor.tag_add(tag, s, e)
        except tk.TclError:
            pass

    def _start(self):
        if self._ph:
            return
        text = self.editor.get("1.0", "end-1c")
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
            self.root.after(0, lambda i=i: self.sv.set(
                f"Switch to browser and click target field... {i}"))
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
                d = random.uniform(mn, mx)
                if char in ".!?":
                    d = max(d, random.uniform(0.22, 0.55))
                elif char in ",;:":
                    d = max(d, random.uniform(0.12, 0.28))
                time.sleep(d)
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
