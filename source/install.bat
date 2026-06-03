@echo off
setlocal enabledelayedexpansion
title AutoWriter Installer
mode con: cols=52 lines=26
color 0B

echo.
echo  ==========================================
echo    AutoWriter  ^|  Human-like Typing v2.0
echo  ==========================================
echo.

:: ── 1. Check Python ─────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [!] Python was not found on this machine.
    echo.
    echo  Please install Python 3.8+ from:
    echo    https://www.python.org/downloads/
    echo.
    echo  IMPORTANT: tick "Add Python to PATH"
    echo  during the Python installer.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do (
    echo  [OK] %%v detected.
)

:: ── 2. Upgrade pip silently ─────────────────────────
python -m pip install --upgrade pip --quiet --disable-pip-version-check >nul 2>&1

:: ── 3. Install packages ─────────────────────────────
echo.
echo  Installing packages (first run may take ~30s)...
pip install -r "%~dp0requirements.txt" --quiet --disable-pip-version-check
if errorlevel 1 (
    echo.
    echo  [!] Quiet install failed. Retrying with output...
    pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo.
        echo  [ERROR] Could not install packages.
        echo  Check your internet connection and try again.
        pause
        exit /b 1
    )
)
echo  [OK] All packages installed.

:: ── 4. Desktop shortcut ─────────────────────────────
echo.
echo  Creating Desktop shortcut...
python "%~dp0install_helper.py"

:: ── 5. Done ─────────────────────────────────────────
echo.
echo  ==========================================
echo    Installation complete!
echo.
echo    Find "AutoWriter" on your Desktop.
echo    Closing the app sends it to the tray.
echo    Emergency stop: move mouse to top-left.
echo  ==========================================
echo.
choice /c YN /M " Launch AutoWriter now? [Y/N]"
if errorlevel 2 goto done
echo.
echo  Starting AutoWriter...
start "" pythonw "%~dp0autowriter.py"
:done
echo.
pause
