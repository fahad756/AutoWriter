
# Rhythm modes — Natural / Burst / Fatigue / Steady
# Controls how inter-key delay varies across the text

# Typo simulation: ~2.5% chance of adjacent-key mispress + self-correct
ADJACENT = {'a':'sq','b':'vn','c':'xv','d':'sf','e':'wr','f':'dg',
            'g':'fh','h':'gj','i':'uo','j':'hk','k':'jl','l':'k',
            'm':'n','n':'bm','o':'ip','p':'o','q':'wa','r':'et',
            's':'ad','t':'ry','u':'yi','v':'cb','w':'qe','x':'zc','y':'tu','z':'x'}


# Win32 SendInput — low-level keyboard injection for anti-detection mode
import ctypes
from ctypes import wintypes, Structure, Union, POINTER, c_ulong

PUL = POINTER(c_ulong)

class _KbdInput(Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD),
                ("dwExtraInfo", PUL)]

class _IUnion(Union):
    _fields_ = [("ki", _KbdInput)]

class _Input(Structure):
    _fields_ = [("type", wintypes.DWORD), ("ii", _IUnion)]

def _send_unicode(char: str) -> None:
    extra = c_ulong(0)
    code  = ord(char)
    for flags in (0x0004, 0x0004 | 0x0002):
        ki  = _KbdInput(0, code, flags, 0, ctypes.pointer(extra))
        inp = _Input(1, _IUnion(ki=ki))
        ctypes.windll.user32.SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

# Mouse micro-jitter every 15-28 keystrokes + random thinking pauses
# Both only active when undetect mode is enabled

# WPM target slider: when > 0, overrides speed preset
# Formula: char_delay = 60.0 / (wpm * 5)

import pystray
from PIL import Image, ImageDraw

# System tray: closing window hides app; right-click tray to quit

# Load autowriter.ico for window titlebar and tray icon
# Added top navigation bar with brand label and Tray button

# Refactored settings panel into 3 cards:
#   Typing | Anti-Detection | Timing

# Added CTkProgressBar that fills as text is typed

# v2.0 — all features integrated, UI polished, ready for release
