@echo off
REM MTG Draft Rater GUI - Single Click Launcher
REM This batch file launches the GUI application directly

cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo During installation, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

REM Launch the GUI
echo Starting MTG Draft Rater GUI...
python gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch GUI
    echo.
    echo Troubleshooting:
    echo - Make sure all Python files are in the same directory
    echo - Check that requirements are installed: pip install -r requirements.txt
    echo - Try running: python gui.py
    echo.
    pause
    exit /b 1
)
