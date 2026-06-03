@echo off
setlocal enabledelayedexpansion
title AutoWriter  -  Build Installer
mode con: cols=58 lines=32
color 0B

echo.
echo  ====================================================
echo    AutoWriter  Build System  v2.0
echo    Creates:  dist\AutoWriter_Setup_v2.0.exe
echo  ====================================================
echo.

:: ── Step 0: Verify Python ────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Install Python 3.8+ and
    echo          add it to PATH, then re-run this script.
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  [OK] %%v

:: ── Step 1: Generate icon ────────────────────────────────
echo.
echo  [1/4]  Generating autowriter.ico ...
pip install Pillow --quiet --disable-pip-version-check >nul 2>&1
python generate_icon.py
if errorlevel 1 (
    echo  [ERROR] Icon generation failed.
    pause & exit /b 1
)

:: ── Step 2: Install PyInstaller ──────────────────────────
echo.
echo  [2/4]  Installing PyInstaller (if not present) ...
pip install pyinstaller --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  [ERROR] Could not install PyInstaller.
    pause & exit /b 1
)
echo  [OK]   PyInstaller ready.

:: ── Step 3: Build AutoWriter.exe ────────────────────────
echo.
echo  [3/4]  Building AutoWriter.exe (this takes ~60 s) ...
echo.

:: Clean previous build artefacts
if exist "build\AutoWriter"    rmdir /s /q "build\AutoWriter"
if exist "dist\AutoWriter.exe" del /f /q   "dist\AutoWriter.exe"

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=autowriter.ico ^
    --name=AutoWriter ^
    --collect-data customtkinter ^
    --hidden-import=pystray._win32 ^
    --hidden-import=PIL.IcoImagePlugin ^
    --hidden-import=PIL.ImageDraw ^
    --add-data "autowriter.ico;." ^
    --noconfirm ^
    autowriter.py

if errorlevel 1 (
    echo.
    echo  [ERROR] PyInstaller build failed. See output above.
    pause & exit /b 1
)
echo.
echo  [OK]   dist\AutoWriter.exe created.

:: ── Step 4: Compile installer with Inno Setup ───────────
echo.
echo  [4/4]  Compiling installer ...

set "ISCC="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe"       set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"
if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    if "!ISCC!"=="" set "ISCC=C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    if "!ISCC!"=="" set "ISCC=C:\Program Files\Inno Setup 5\ISCC.exe"
)

if "!ISCC!"=="" (
    echo.
    echo  [!]  Inno Setup not found on this machine.
    echo.
    echo       AutoWriter.exe is already built at:
    echo         dist\AutoWriter.exe
    echo.
    echo       To create the full setup wizard installer:
    echo       1. Download Inno Setup (free) from:
    echo            https://jrsoftware.org/isinfo.php
    echo       2. Install it.
    echo       3. Re-run  build_installer.bat
    echo          — it will find Inno Setup automatically.
    echo.
    choice /c YN /M " Open the Inno Setup download page now?"
    if not errorlevel 2 start https://jrsoftware.org/isdl.php
    echo.
    pause
    exit /b 0
)

echo  Found: !ISCC!
"!ISCC!" installer.iss
if errorlevel 1 (
    echo.
    echo  [ERROR] Inno Setup compilation failed.
    pause & exit /b 1
)

:: ── Done ─────────────────────────────────────────────────
echo.
echo  ====================================================
echo    Build complete!
echo.
echo    Installer  →  dist\AutoWriter_Setup_v2.0.exe
echo    Standalone →  dist\AutoWriter.exe
echo.
echo    Share AutoWriter_Setup_v2.0.exe with anyone —
echo    no Python required on their machine.
echo  ====================================================
echo.
choice /c YN /M " Launch the installer now to test it?"
if not errorlevel 2 start "" "dist\AutoWriter_Setup_v2.0.exe"
echo.
pause
