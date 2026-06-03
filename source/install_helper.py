"""Creates a Desktop shortcut for AutoWriter. Called by install.bat."""
import os, subprocess, sys

def main():
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    app_path     = os.path.join(script_dir, "autowriter.py")
    desktop      = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
    shortcut     = os.path.join(desktop, "AutoWriter.lnk")

    # Prefer pythonw.exe (no console window)
    py_dir  = os.path.dirname(sys.executable)
    pythonw = os.path.join(py_dir, "pythonw.exe")
    if not os.path.exists(pythonw):
        pythonw = "pythonw.exe"

    ps = f"""
$sh = New-Object -ComObject WScript.Shell
$s  = $sh.CreateShortcut("{shortcut}")
$s.TargetPath      = "{pythonw}"
$s.Arguments       = '"{app_path}"'
$s.WorkingDirectory= "{script_dir}"
$s.Description     = "AutoWriter - Human-like Typing Automation"
$s.Save()
"""
    r = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        print(f"  [OK] Desktop shortcut created.")
    else:
        # Fallback: drop a .bat launcher on the Desktop
        bat = os.path.join(desktop, "AutoWriter.bat")
        with open(bat, "w") as f:
            f.write(f'@echo off\nstart "" pythonw "{app_path}"\n')
        print(f"  [OK] Shortcut fallback: {bat}")

if __name__ == "__main__":
    main()
