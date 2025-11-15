# GUI Single-Click Launcher Setup

## Quick Start

### Option 1: Batch File (Easiest - Windows) ⭐ RECOMMENDED
Simply double-click `launch_gui.bat` to start the GUI immediately.

**Features:**
- Double-click to launch
- **Automatically installs Python if missing!**
- Automatically installs required packages (requests, colorama)
- Shows helpful error messages if something goes wrong
- Pauses on error so you can read the message
- No console window persists after launch

**What happens when you run it:**
1. Checks if Python is installed
2. If missing: Downloads and installs Python 3.11 automatically
3. Installs required packages (requests, colorama)
4. Launches the GUI
5. Ready to use!

### Option 2: Python Launcher
Double-click `gui_launcher.py` to start the GUI.

**Features:**
- Cross-platform (Windows, Mac, Linux)
- Clean error dialogs if something fails
- Note: Requires Python to be installed first

### Option 3: Create Desktop Shortcut (Windows)

To create a shortcut that you can place anywhere (including desktop):

1. **Right-click** on `launch_gui.bat`
2. Select **Send to** → **Desktop (create shortcut)**
3. A new shortcut appears on your desktop
4. You can rename it to just "MTG Rater" or similar
5. Right-click the shortcut and select **Properties** to change the icon

### Option 4: Compile to Standalone EXE (Advanced)

To create a standalone `.exe` that can run anywhere without Python installed:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Create the executable:
   ```bash
   pyinstaller gui_launcher.py --onefile --windowed --name "MTG_Rater" --icon icon.ico
   ```

3. The `.exe` will be in the `dist/` folder

**Note:** You'll need an `.ico` file for a custom icon. You can find free icon converters online.

## How They Work

- **launch_gui.bat**: Windows batch file that auto-installs Python if needed, then runs `gui.py`
- **gui_launcher.py**: Python script that launches the GUI, handles errors gracefully

## System Requirements

The batch file works on:
- ✅ Windows 10/11 with Python installed
- ✅ Windows 10/11 WITHOUT Python (will auto-install)
- ✅ Computers with internet access (for auto-installation)
- ✅ Administrator access recommended (for auto-installation)

## Troubleshooting

If you get an error when launching:

1. **"Failed to download Python"**: 
   - Check your internet connection
   - Try downloading Python manually from https://www.python.org/
   
2. **"Python still not found after installation"**: 
   - Restart your computer
   - Python needs environment variable refresh
   
3. **"Failed to launch GUI"**: 
   - Make sure `gui.py` is in the same folder as the launcher
   - Try running again (may need to wait for package installation)
   - Check that you have internet for package installation

## Recommended Setup

1. **Use `launch_gui.bat`** for any system - it handles everything automatically
2. **Optional: Create a desktop shortcut** for easy access from desktop
3. **Optional: Advanced users** can compile to `.exe` for portable distribution

## Advanced: Manual Python Installation

If auto-installation doesn't work, install Python manually:

1. Download from: https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Click "Install Now"
4. Restart your computer
5. Double-click `launch_gui.bat` again

