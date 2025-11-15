#!/usr/bin/env python
"""
MTG Draft Rater - GUI Quick Start
Run this script to start the graphical interface
"""

import sys
import subprocess
from pathlib import Path


def main():
    """Quick start the GUI"""
    print("=" * 60)
    print("MTG DRAFT RATER - GUI LAUNCHER")
    print("=" * 60)
    print("\nStarting graphical interface...\n")
    
    # Try to import and run GUI
    try:
        from gui import main as gui_main
        print("✓ GUI module loaded successfully")
        print("\nLaunching window...\n")
        gui_main()
    except ImportError as e:
        print(f"✗ Error: Could not import GUI module: {e}")
        print("\nThis might happen if:")
        print("  • tkinter is not installed")
        print("  • Python installation is incomplete")
        print("\nSolutions:")
        print("  • Windows: tkinter usually included, try reinstalling Python")
        print("  • Linux: Run 'sudo apt-get install python3-tk'")
        print("  • Mac: Reinstall Python from python.org")
        print("\nAlternatively, use the CLI:")
        print("  python main.py")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error starting GUI: {e}")
        print("\nTry the CLI instead:")
        print("  python main.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
