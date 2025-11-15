#!/usr/bin/env python
"""
Quick start guide for the MTG Draft Rater
Run this to get started with the application
"""

import subprocess
import sys
import os

def main():
    print("=" * 60)
    print("MTG DRAFT DECK RATING ENGINE - QUICK START")
    print("=" * 60)
    
    print("""
This application helps you draft the perfect MTG deck by:

1. Fetching real card data from Scryfall API
2. Analyzing your current deck composition
3. Rating all remaining cards 1-10 based on synergies
4. Providing recommendations in real-time

WHAT YOU'LL NEED:
- Python 3.8 or higher
- Internet connection (first load of each set)
- About 30 seconds for initial set data fetch

HOW TO USE:
1. Run: python main.py
2. Select a set you're drafting (e.g., "MOM" for March of the Machine)
3. Add cards as you pick them during draft
4. Get card ratings and recommendations
5. Build your optimal 40-card deck

QUICK DEMO:
""")
    
    response = input("Would you like to try a quick demo? (y/n): ").strip().lower()
    
    if response == 'y':
        print("\nLaunching MTG Draft Rater...")
        print("-" * 60)
        try:
            subprocess.run([sys.executable, "main.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        except KeyboardInterrupt:
            print("\n\nDemo ended.")
    else:
        print("\nTo start the application, run:")
        print("  python main.py")
        print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
