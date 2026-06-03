@echo off
setlocal
title AutoWriter  -  Build single EXE
color 0B

echo.
echo  ================================================
echo    AutoWriter  -  Building standalone EXE
echo  ================================================
echo.

:: Verify Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found. Please install Python 3.8+
    pause & exit /b 1
)

:: Generate icon
echo  [1/3]  Generating icon...
python generate_icon.py
if errorlevel 1 ( echo  [ERROR] Icon failed & pause & exit /b 1 )

:: Install / upgrade PyInstaller
echo  [2/3]  Installing PyInstaller...
pip install pyinstaller --quiet --disable-pip-version-check
if errorlevel 1 ( echo  [ERROR] pip failed & pause & exit /b 1 )

:: Build
echo  [3/3]  Bundling AutoWriter.exe  (takes ~60 sec) ...
echo.
if exist "dist\AutoWriter.exe" del /f /q "dist\AutoWriter.exe"
if exist "build\AutoWriter"    rmdir /s /q "build\AutoWriter"

pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=autowriter.ico ^
    --name=AutoWriter ^
    --collect-all customtkinter ^
    --hidden-import=pystray._win32 ^
    --hidden-import=PIL.IcoImagePlugin ^
    --add-data "autowriter.ico;." ^
    --noconfirm ^
    autowriter.py

if errorlevel 1 (
    echo.
    echo  [ERROR] Build failed. See output above.
    pause & exit /b 1
)

echo.
echo  ================================================
echo    Done!
echo    File:  dist\AutoWriter.exe
echo    Share this single file with anyone.
echo    No Python or libraries needed on their PC.
echo  ================================================
echo.
choice /c YN /M " Run AutoWriter.exe now to test?"
if not errorlevel 2 start "" "dist\AutoWriter.exe"
echo.
pause
