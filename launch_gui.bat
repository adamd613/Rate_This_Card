@echo off
REM MTG Draft Rater GUI - Single Click Launcher with Auto Python Installation
REM This batch file launches the GUI application and installs Python if needed

setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Python not found. Installing Python 3.11...
    echo.
    
    REM Download Python installer
    set "PYTHON_URL=https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    set "PYTHON_INSTALLER=%temp%\python-3.11.7-amd64.exe"
    
    echo Downloading Python from: !PYTHON_URL!
    powershell -Command "(New-Object Net.WebClient).DownloadFile('!PYTHON_URL!', '!PYTHON_INSTALLER!')"
    
    if not exist "!PYTHON_INSTALLER!" (
        echo.
        echo ERROR: Failed to download Python
        echo.
        echo Please download and install Python manually from: https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation
        echo.
        pause
        exit /b 1
    )
    
    echo Installing Python...
    REM Run installer with silent install and add to PATH
    "!PYTHON_INSTALLER!" /quiet InstallAllUsers=1 PrependPath=1
    
    if errorlevel 1 (
        echo.
        echo ERROR: Python installation failed
        echo.
        echo Please try manual installation from: https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH"
        echo.
        pause
        exit /b 1
    )
    
    echo Python installed successfully!
    echo.
    
    REM Clean up installer
    del "!PYTHON_INSTALLER!" 2>nul
    
    REM Refresh environment variables
    for /f "tokens=2*" %%A in ('reg query HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment /v PATH') do (
        set "PATH=%%B"
    )
)

REM Check if Python is now available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python still not found after installation
    echo Please restart your computer and try again
    echo.
    pause
    exit /b 1
)

REM Install required packages
echo Checking required packages...
python -m pip install -q requests colorama 2>nul

REM Launch the GUI
echo.
echo Starting MTG Draft Rater GUI...
echo.
python gui.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to launch GUI
    echo.
    echo Troubleshooting:
    echo - Make sure all Python files are in the same directory
    echo - Try running: python gui.py
    echo - Check internet connection for package installation
    echo.
    pause
    exit /b 1
)
