"""
MTG Draft Rater - Unified Launcher
Choose between CLI and GUI interfaces
"""

import sys
import os
from pathlib import Path


def show_launcher_menu():
    """Display the launcher menu"""
    print("\n" + "=" * 60)
    print("MTG DRAFT DECK RATING ENGINE - LAUNCHER")
    print("=" * 60)
    print("\nChoose your interface:\n")
    print("1. GUI (Graphical Interface) - Recommended for most users")
    print("2. CLI (Command Line Interface) - Advanced/power users")
    print("3. Exit")
    print("\n" + "=" * 60)


def launch_gui():
    """Launch the GUI version"""
    print("\nStarting GUI...")
    try:
        from gui import main
        main()
    except ImportError as e:
        print(f"Error: Could not import GUI module: {e}")
        print("\nTroubleshooting:")
        print("- Ensure tkinter is installed (comes with Python)")
        print("- On Linux: sudo apt-get install python3-tk")
        print("- On Mac: tkinter should be included")
        print("- On Windows: tkinter is included with Python")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting GUI: {e}")
        sys.exit(1)


def launch_cli():
    """Launch the CLI version"""
    print("\nStarting CLI...")
    try:
        from main import MTGDraftRater
        app = MTGDraftRater()
        app.run()
    except Exception as e:
        print(f"Error starting CLI: {e}")
        sys.exit(1)


def main():
    """Main launcher"""
    while True:
        show_launcher_menu()
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            launch_gui()
            break
        elif choice == "2":
            launch_cli()
            break
        elif choice == "3":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
