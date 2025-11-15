# MTG Draft Deck Rating Engine

A comprehensive tool to craft the perfect MTG draft deck in real-time during drafting sessions. Choose between CLI or GUI interface.

## Quick Start

### 🚀 Easiest Way: Double-Click Launcher
Simply **double-click `launch_gui.bat`** to launch the GUI!
- Automatically installs Python if needed
- Installs required packages
- Single-click, no setup required

### Alternative: Command Line
```bash
python main.py           # CLI interface
python gui.py            # GUI interface
python launcher.py       # Choose interface (CLI or GUI)
```

## Features

### 🎯 Intelligent Card Rating System
- **Mana Curve Analysis**: Rates cards based on how they fit into your deck's mana curve
- **Color Synergy**: Analyzes color identity and penalizes off-color cards
- **Creature/Spell Balance**: Maintains optimal deck composition (~65% creatures in limited)
- **Synergy Detection**: Identifies keyword synergies, creature types, and theme synergies
- **Limited Format Power Level**: Evaluates cards specifically for limited draft gameplay
- **All Cards Rated**: Get ratings for every card in the set, including those in your deck
- **Real-Time Performance**: Optimized caching for fast rating updates

### 📊 Comprehensive Deck Analysis
- Mana curve visualization
- Color distribution tracking
- Detected themes and synergies
- Creature-to-spell ratio optimization
- Power/toughness analysis

### 💾 Deck Management
- Save and load draft decks
- Persistent card data caching (no internet needed after first load)
- Real-time deck statistics

### 🔍 Real MTG Data
- Integrates with **Scryfall API** for real card data
- Access to all official MTG sets
- Complete card information including:
  - Mana costs and CMC
  - Card types and subtypes
  - Oracle text and abilities
  - Power/toughness for creatures
  - Rarity information

### 🖥️ Dual Interface Options

#### GUI (Graphical User Interface)
- Visual card list with search functionality
- Color-coded ratings (Green 9-10, Blue 7-8, Orange 5-6, Red <4)
- Double-click cards to add to deck
- Real-time deck statistics dashboard
- Save/load decks with simple dialogs

#### CLI (Command Line Interface)
- Terminal-based interface with colored output
- Browse top 20 recommendations
- Full-featured deck management
- Good for server/remote use

## How to Use

### Installation (One-Time Setup)

If using the launcher `.bat` file, nothing needed! It handles everything.

Otherwise:
```bash
cd "Rate_This_Card"
pip install -r requirements.txt
```

### Running the GUI Application

#### Option 1: Double-Click Launcher (Recommended)
Simply double-click `launch_gui.bat` - that's it!

#### Option 2: Python Command
```bash
python gui.py
```

#### Option 3: Create Desktop Shortcut
Right-click `launch_gui.bat` → Send to → Desktop (create shortcut)

### Running the CLI Application

```bash
python main.py
```

### Workflow During Draft

#### GUI Workflow:
1. **Select a Set**: Choose which MTG set you're drafting from
   - Use the search box or dropdown menu
   - Click "Load Set" to fetch cards
   
2. **Build Your Deck**: Add cards as you draft
   - Type card name and click "Add" or press Enter
   - Or double-click cards from the "Cards in Set" list
   - View your deck on the left side

3. **Rate Cards**: Click "Rate Cards" to get recommendations
   - All cards get color-coded ratings
   - Highest-rated cards appear first
   - Search to filter the list
   - Double-click any card to add to deck

4. **Track Statistics**: Bottom panel shows real-time analysis
   - Deck size, creature count, mana curve
   - Color distribution
   - Detected synergies and themes

5. **Save/Load**: Buttons to persist your work
   - Save current deck at any time
   - Load previous drafts

#### CLI Workflow:
1. Select a set from the menu
2. Add cards using the command line
3. View ratings for recommendations
4. View statistics to monitor deck health
5. Save when finished

## Rating System

Cards are rated 1-10 based on:

### Mana Curve Fit (±2.0 points)
- Cards at needed mana costs get boosts
- Over-represented costs get penalties
- Targets: 2-3 one-mana, 3-4 two-mana, etc.

### Color Synergy (±1.5 points)
- Cards in your main colors get bonuses
- Off-color cards get penalties
- Colorless cards are flexible

### Deck Balance (±1.5 points)
- Prioritizes ~65% creatures, ~35% spells
- Adjusts based on current composition

### Synergies (0-3+ points)
- Keyword overlaps (flying, sacrifice, etc.)
- Creature type matches
- Theme synergies

### Limited Power Level (0-1.5 points)
- Removal spells rated highly
- Card draw is valuable
- Good stats-to-cost ratio rewarded

### Deck Completion (0-1 points)
- Bonus for cards when deck is under 40 cards
- Encourages filling your deck

## Caching & Performance

- **First load**: ~20-30 seconds to fetch set data from Scryfall
- **Subsequent loads**: Instant (cached locally)
- **Card ratings**: ~1-2 seconds (optimized with pre-computed caches)
- **Search**: Real-time, no delay

Cache files stored in `cache/` directory:
- Set data as JSON files (e.g., `MOM.json`)
- Decks as `.deck` files

## Troubleshooting

### Application won't start
- Ensure Python is installed: `python --version`
- Try the launcher `.bat` file - it handles Python auto-installation
- Check internet connection for first-time set loading

### Cards not showing up
- Make sure set loaded successfully (status message says "✓ Loaded N cards")
- Try searching by partial card name
- Check that you're in the correct set

### Ratings seem slow
- First rating takes 1-2 seconds (normal)
- Subsequent ratings use cached data and are faster
- Large sets (500+ cards) may take a moment

### Card not found when searching
- Try partial matching
- Check spelling
- Verify card is in the selected set

## Requirements

- Python 3.8+ (auto-installed by launcher if needed)
- Internet connection (first load per set)
- Windows/Mac/Linux with tkinter support

## Keyboard Shortcuts

### GUI
- **Enter**: Add card (when entry field focused)
- **Double-click**: Add card from list
- **Ctrl+C**: Quit application

### CLI
- Type commands directly in menu
- Type `done` to finish adding cards
- Type `exit` or `quit` to leave

## File Structure

```
Rate_This_Card/
├── gui.py                    # GUI application
├── main.py                   # CLI application
├── launcher.py               # Interface chooser
├── launch_gui.bat           # Single-click launcher
├── card_rating_engine.py    # Rating algorithm
├── scryfall_api.py          # Scryfall API integration
├── config.py                # Configuration
├── requirements.txt         # Python dependencies
└── cache/                   # Cached set data
```

## Tips for Best Results

1. **Add cards as you draft** - Keep updating for real-time recommendations
2. **Review top-rated cards** - Usually the best picks
3. **Check the synergies** - Look for themes in your deck
4. **Monitor deck health** - Use statistics to stay balanced
5. **Learn your set** - Most sets have 2-3 main archetypes

## Known Limitations

- Ratings optimized for Limited format
- Keyword-based synergies (not exhaustive)
- Cannot predict future picks or metagame shifts
- No support for custom card data (Scryfall only)

## Future Enhancements

Possible improvements:
- [ ] Machine learning model for better ratings
- [ ] Support for sealed format
- [ ] Curve optimization suggestions
- [ ] Card combo database
- [ ] Integration with draft tracking websites
- [ ] Export to MTG Arena/Cockatrice

## License

This tool uses data from Scryfall (https://scryfall.com/). See Scryfall's terms for usage rights.
