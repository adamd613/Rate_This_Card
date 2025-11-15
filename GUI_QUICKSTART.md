# GUI Interface Guide

## Quick Start

Start the GUI immediately:

```bash
python gui.py
```

Or use the launcher to choose interface:

```bash
python launcher.py
```

## What's New

The graphical interface provides:

✨ **Modern GUI** - Beautiful, intuitive interface
✨ **Real-time Feedback** - Instant deck analysis updates
✨ **Color-Coded Ratings** - Visual indication of card quality
✨ **Easy Card Management** - Drag-and-drop alternative
✨ **Built-in Dialogs** - Save/load with visual selection
✨ **Live Statistics** - Always visible deck analysis

## Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│ Set Selection Bar                                       │
│ [Search Set] [Select from Dropdown] [Load]            │
├──────────────────────┬─────────────────────────────────┤
│ Deck Management      │ Recommendations               │
│ Add: [Card Entry]    │ [Rate Cards Button]          │
│                      │                               │
│ [Card List]          │ Top 20 Recommendations:      │
│ 1. Card A            │ 1.  9.5/10 - Excellent!    │
│ 2. Card B            │ 2.  9.0/10 - Good          │
│ 3. Card C            │ 3.  8.5/10 - Good          │
│                      │ ...                          │
│ [Remove] [Save]      │ Add #: [_] [Add]            │
│         [Load]       │                              │
├──────────────────────┴─────────────────────────────────┤
│ Deck Analysis: 5/40 | Creatures: 4 | Avg CMC: 2.3    │
└─────────────────────────────────────────────────────────┘
```

## Key Features

### 1. Set Selection
- Search by name or code
- Dropdown with all 1000+ MTG sets
- Automatic filtering as you type
- One-click loading

### 2. Deck Management
- Add cards with partial name matching
- Visual card list with numbering
- Remove individual cards or clear all
- Real-time deck size counter

### 3. Card Ratings
- Click "Rate Cards" for AI recommendations
- Color-coded results (Green/Blue/Orange/Red)
- Shows 20 best recommendations
- Add recommendations directly from results

### 4. Live Statistics
- Creatures vs spells ratio
- Average mana cost (CMC)
- Color distribution
- Detected synergies and themes

### 5. Deck Persistence
- Save decks to file
- Load saved decks with visual selection
- Automatic set loading when deck loaded
- All cards restored in order

## Color-Coded Ratings

- 🟢 **9-10 (Green)**: Excellent - Must pick!
- 🔵 **7-8 (Blue)**: Good - Solid choice
- 🟠 **5-6 (Orange)**: Okay - Fills a role
- 🔴 **<4 (Red)**: Weak - Consider passing

## Usage Workflow

1. **Load a set**
   - Type set name or code
   - Click "Load Set"

2. **Add your cards**
   - Type card name
   - Press Enter or click Add
   - See deck build up in real-time

3. **Get recommendations**
   - Click "Rate Cards"
   - See top picks color-coded
   - Monitor deck stats below

4. **Pick and repeat**
   - Choose from recommendations
   - Or manually add cards
   - Watch analysis update

5. **Save when done**
   - Click "Save Deck"
   - Name your deck
   - Restore later anytime

## Shortcuts

- **Enter key**: Add card immediately
- **Click card**: Select for removal
- **Clear All**: Wipe entire deck
- **Refresh Stats**: Manual update (automatic too)

## Troubleshooting

### GUI won't start
- Check Python 3.8+ installed
- Windows: tkinter included
- Linux: `sudo apt-get install python3-tk`
- Mac: Reinstall Python

### Slow first load
- First set load: 20-30 seconds (normal)
- Uses Scryfall API
- Cached after first load
- Subsequent loads: <1 second

### Cards won't add
- Check spelling (fuzzy matching available)
- Verify card in selected set
- Try partial name
- Use dropdown on match dialog

### Deck not saving
- Check write permissions
- Verify `cache/` directory exists
- Enough disk space available
- Try different filename

## Tips

- **Fuzzy matching**: Type "Jet" for "Jetmir"
- **Multiple matches**: Dialog shows options
- **Real-time analysis**: Stats update with each card
- **Bookmark top 20**: Check multiple times during draft
- **Save frequently**: Don't lose your work!

## Performance

- **Set load (first)**: 20-30 seconds
- **Set load (cached)**: <1 second
- **Card rating**: 2-5 seconds
- **UI updates**: Instant
- **Memory usage**: ~50 MB

## Advanced

### Change Window Size
Edit `gui.py`:
```python
self.root.geometry("1400x900")  # Change to your preference
```

### Customize Colors
Edit `gui.py`:
```python
self.rec_text.tag_config("excellent", foreground="#00AA00")
```

### Add More Features
- Extend `MTGDraftRaterGUI` class
- Add new panel for filters
- Custom sort options
- Export formats

## Comparison: GUI vs CLI

| Feature | GUI | CLI |
|---------|-----|-----|
| Ease | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Features | All | All |
| Speed | Fast | Fast |
| Visual | Excellent | Basic |
| Setup | 0 sec | 0 sec |

Both interfaces share the same engine - use whichever you prefer!

## Getting Help

- **In-app**: Status messages and error dialogs
- **GUI_GUIDE.md**: Comprehensive GUI documentation
- **README.md**: General features
- **DEVELOPER.md**: Technical details

## Files

- `gui.py` - Main GUI application
- `launcher.py` - Choose CLI or GUI
- `start_gui.py` - Direct GUI launcher
- `GUI_GUIDE.md` - Full GUI documentation

---

**Ready?** Type: `python gui.py`

Enjoy the graphical experience! 🎴✨
