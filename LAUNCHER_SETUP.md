# GUI Single-Click Launcher Setup

## Quick Start

### Option 1: Batch File (Easiest - Windows)
Simply double-click `launch_gui.bat` to start the GUI immediately.

**Features:**
- Double-click to launch
- Shows error messages if something goes wrong
- Pauses on error so you can read the message
- No console window (runs in background)

### Option 2: Python Launcher
Double-click `gui_launcher.py` to start the GUI.

**Features:**
- Cross-platform (Windows, Mac, Linux)
- Clean error dialogs if something fails

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

- **launch_gui.bat**: Simple Windows batch file that checks Python is installed, then runs `gui.py`
- **gui_launcher.py**: Python script that launches the GUI, handles errors gracefully

## Troubleshooting

If you get an error when launching:

1. **"Python is not installed"**: Download Python from https://www.python.org/ and reinstall with "Add Python to PATH" checked
2. **"gui.py not found"**: Make sure `gui.py` is in the same folder as the launcher
3. **"Requirements not installed"**: Run this command:
   ```bash
   pip install requests colorama
   ```

## Recommended Setup

1. Use `launch_gui.bat` for immediate launching
2. Create a desktop shortcut to `launch_gui.bat` for easy access
3. Optional: Install PyInstaller and build `.exe` for portable distribution
