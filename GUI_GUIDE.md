# MTG Draft Rater - GUI User Guide

## 🚀 Getting Started with the GUI

The graphical interface provides a modern, user-friendly way to use the MTG Draft Rater. It's perfect for interactive drafting sessions!

### Starting the GUI

**Option 1: Direct Launch (Recommended)**
```bash
python gui.py
```

**Option 2: Use Launcher**
```bash
python launcher.py
# Then select option 1 (GUI)
```

## 📋 Interface Overview

The GUI is organized into 4 main sections:

```
┌─────────────────────────────────────────────────────────────┐
│  SET SELECTION (Top)                                        │
│  [Search] [Dropdown ▼] [Load Set]                           │
├──────────────────────────┬──────────────────────────────────┤
│                          │                                  │
│  YOUR DECK (Left)        │  RECOMMENDATIONS (Right)         │
│  Add Card: [____] [Add]  │  [Rate Cards Button]            │
│  [Card List]             │                                  │
│  ................        │  Recommendation Results:         │
│  ................        │  1. Card A (9.5/10)             │
│  ................        │  2. Card B (9.0/10)             │
│                          │  ................                │
│  [Remove] [Save] [Load]  │  Add card #: [__] [Add]        │
├──────────────────────────┴──────────────────────────────────┤
│  DECK ANALYSIS (Bottom)                                     │
│  Size: 5/40 | Creatures: 4 (80%) | Avg CMC: 2.3            │
│  Themes: White-Blue deck, Flying synergy                    │
└─────────────────────────────────────────────────────────────┘
```

## 🎮 How to Use

### Step 1: Load a Set

1. **Search for a set** (optional):
   - Type in the "Search Set" field
   - Example: "MOM" or "March"
   - The dropdown will filter automatically

2. **Select a set** from the dropdown:
   - Click the dropdown arrow
   - Choose from filtered results
   - Click "Load Set" button

3. **Wait for loading**:
   - First time: 20-30 seconds (fetches from Scryfall)
   - Subsequent loads: <1 second (uses cache)

### Step 2: Build Your Deck

1. **Add cards**:
   - Type card name in "Add Card" field
   - Press Enter or click "Add" button
   - Cards are fuzzy-matched (partial names work!)

2. **Remove cards**:
   - Select a card in the list
   - Click "Remove Selected"
   - Or clear all with "Clear All"

3. **Organize deck**:
   - Card list shows current deck
   - Numbers indicate pick order
   - Update live statistics on every change

### Step 3: Get Recommendations

1. **Rate cards**:
   - Click "Rate Cards" button
   - System analyzes your deck
   - Shows top 20 recommendations

2. **Understanding the ratings**:
   - **Green (9-10)**: Excellent - Take it!
   - **Blue (7-8)**: Good - Solid pick
   - **Orange (5-6)**: Okay - Fills a slot
   - **Red (<4)**: Weak - Consider passing

3. **Add recommended cards**:
   - Enter number (e.g., "1" for top pick)
   - Click "Add" to add to deck
   - Or manually search and add

### Step 4: Monitor Your Deck

The **Deck Analysis** section shows:
- **Deck Size**: Current/40 cards
- **Creatures**: Count and percentage
- **Spells**: Non-creature spell count
- **Average CMC**: Mana curve health
- **Colors**: Your deck's color identity
- **Themes**: Detected synergies (flying, tokens, etc.)

## 📊 Interface Features

### Set Selection Panel
- **Search Box**: Filter sets by name or code
- **Dropdown**: Browse and select from available sets
- **Load Button**: Fetch and load selected set
- **Status**: Shows current operation or loaded set info

### Deck Management Panel
- **Add Card Input**: Type card names (fuzzy matching)
- **Card List**: View all selected cards with numbers
- **Remove Selected**: Remove highlighted card
- **Clear All**: Empty entire deck
- **Save Deck**: Persist deck to file
- **Load Deck**: Restore saved deck
- **Deck Counter**: Shows current size

### Recommendations Panel
- **Rate Cards Button**: Analyze and rate all remaining cards
- **Results Display**: Color-coded card ratings with explanations
- **Manual Selection**: Add specific recommendation by number
- **Scroll Support**: Browse through many recommendations

### Analysis Dashboard
- **Size Indicator**: Deck progress toward 40 cards
- **Creature Count**: Ratio and percentage
- **Mana Curve**: Average converted mana cost
- **Color Analysis**: Current deck colors
- **Theme Detection**: Identified synergies
- **Refresh Button**: Manual update option

## 🎯 Tips & Tricks

### Quick Actions
- **Add cards faster**: Press Enter after typing card name
- **Fuzzy matching**: Type partial names (e.g., "Jet" for "Jetmir")
- **Multiple matches**: System shows dialog with options
- **Save frequently**: Use Save Deck button during draft

### Deck Building
- **Follow recommendations**: Top 3 cards usually best picks
- **Monitor balance**: Check analysis after 5-10 cards
- **Trust your instincts**: Algorithm is guide, not gospel
- **Update frequently**: Rate cards after each pick

### Performance
- **First set load**: ~30 seconds (one-time)
- **Ratings computation**: ~2-5 seconds (normal)
- **Set switching**: <1 second after first load
- **Card addition**: Instant

## 🔧 Keyboard Shortcuts

| Action | How |
|--------|-----|
| Add card | Type name + Press Enter |
| Select recommendation | Type number + Press Tab + Enter |
| Scroll results | Mouse wheel or Page Up/Down |
| Remove card | Select + Click "Remove Selected" |

## 💾 Saving & Loading Decks

### Save Current Deck
1. Click "Save Deck" button
2. Enter filename in dialog (e.g., "MOM_Draft_11_14")
3. File saved to `cache/` directory
4. Status message confirms success

### Load Saved Deck
1. Click "Load Deck" button
2. Select deck from list
3. Click "Load" in dialog
4. Set automatically loads
5. Cards populate your deck

### Deck File Format
- Location: `cache/*.deck`
- Format: JSON with metadata
- Contains: Set name, cards, timestamp
- Portable: Can be backed up and shared

## ⚠️ Common Issues

### "Failed to load sets"
- **Cause**: Internet connection issue
- **Fix**: Check connection, try again
- **Info**: Only needed first time per set

### "Card not found"
- **Cause**: Typo or card in different set
- **Fix**: Try partial name or check set
- **Info**: Shows suggestions on multiple matches

### "Application is slow"
- **Cause**: First time loading set
- **Fix**: Wait ~30 seconds for first load
- **Info**: Subsequent loads use cache and are instant

### "GUI won't start"
- **Cause**: tkinter not installed
- **Fix (Windows)**: tkinter included with Python
- **Fix (Linux)**: `sudo apt-get install python3-tk`
- **Fix (Mac)**: Should be included, reinstall Python if needed

## 🎨 Interface Customization

### Colors
The interface uses a standard theme. To customize:
1. Edit `gui.py` 
2. Look for `tag_config` sections
3. Modify color codes (hex format: `#RRGGBB`)

### Window Size
Default: 1400x900 pixels
To change:
1. Edit `gui.py`
2. Find `self.root.geometry("1400x900")`
3. Modify dimensions

### Font
To change fonts:
1. Edit `gui.py`
2. Look for `font=("Arial", 11, "bold")`
3. Modify font name or size

## 📚 Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| **Ease of Use** | Easy | Moderate |
| **Visual Feedback** | Excellent | Basic |
| **Speed** | Fast | Fast |
| **Features** | All | All |
| **Learning Curve** | 5 min | 10 min |
| **Customization** | Limited | Full |
| **Recommended For** | Most users | Power users |

## 🚀 Advanced Usage

### Batch Operations
- Save multiple deck variations
- Load decks for comparison
- Analyze different set combinations

### Draft Tracking
- Save deck after each set completion
- Create timestamped backups
- Review your picks later

### Integration
- GUI and CLI work independently
- Share same cache and save files
- Can switch between interfaces

## 📞 Getting Help

**Within the app**:
- Hover over elements for tooltips
- Status bar shows current operation
- Error dialogs explain problems

**External**:
- See README.md for full documentation
- Check EXAMPLE_USAGE.md for workflows
- Review DEVELOPER.md for technical details

## ✨ Keyboard Tips

### Text Entry
- Click field and type
- Use backspace to delete
- Fuzzy matching works automatically

### Lists
- Click to select
- Scroll with mouse wheel
- Double-click for quick actions

### Buttons
- Left-click to activate
- Tab to navigate
- Enter to activate focused button

---

**Version**: 1.0
**Last Updated**: November 14, 2025
**Status**: ✅ Ready to use

Start with the GUI for the best experience! Type `python gui.py` to launch.
