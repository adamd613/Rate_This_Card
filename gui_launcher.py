#!/usr/bin/env python3
"""
MTG Draft Rater - GUI Launcher Executable
Standalone executable for launching the GUI without showing console window.
Can be compiled to .exe with PyInstaller: pyinstaller gui_launcher.py --onefile --windowed
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Launch the GUI application."""
    # Get the directory where this script is located
    app_dir = Path(__file__).parent.absolute()
    gui_file = app_dir / "gui.py"
    
    # Verify gui.py exists
    if not gui_file.exists():
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"gui.py not found in {app_dir}\n\n"
            "Make sure all files are in the same directory."
        )
        root.destroy()
        return 1
    
    # Launch GUI in a separate process
    try:
        subprocess.run(
            [sys.executable, str(gui_file)],
            cwd=str(app_dir),
            check=False
        )
        return 0
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Error",
            f"Failed to launch GUI:\n\n{str(e)}\n\n"
            "Make sure Python is correctly installed."
        )
        root.destroy()
        return 1

if __name__ == "__main__":
    sys.exit(main())
