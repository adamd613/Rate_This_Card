# MTG DRAFT RATER - QUICK REFERENCE CARD

## 🚀 QUICK START (Copy & Paste)

```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Test
python test_application.py
```

## 📋 MAIN MENU COMMANDS

| # | Command | What It Does |
|---|---------|------------|
| 1 | Select set | Choose which MTG set to draft |
| 2 | Add cards | Add cards to your deck |
| 3 | Rate cards | Get AI recommendations (⭐ MOST IMPORTANT) |
| 4 | Statistics | View deck analysis |
| 5 | Save deck | Save your deck to file |
| 6 | Load deck | Load a saved deck |
| 7 | Exit | Quit application |

## 💬 ADD CARDS COMMANDS

| Command | Does |
|---------|------|
| `add` | Add a single card |
| `remove N` | Remove card at position N |
| `clear` | Remove all cards |
| `done` | Return to main menu |

## ⭐ RATE CARDS COMMANDS

| Command | Does |
|---------|------|
| `add N` | Add recommended card N |
| `details N` | See card details |
| `more` | Show next 20 cards |
| `done` | Return to main menu |

## 📊 RATING SCALE

- **9-10** 🟢 **EXCELLENT** - Take it!
- **7-8** 🟡 **GOOD** - Solid pick
- **5-6** 🟡 **OKAY** - Fills slot
- **3-4** 🟠 **WEAK** - Consider passing
- **1-2** 🔴 **BAD** - Probably pass

## 🎯 TYPICAL DRAFT SESSION

```
1. python main.py
   ↓
2. Menu → 1 (Select set)
   ↓
3. Type: "MOM" (or any set code)
   ↓
4. Wait: 20-30 seconds (first time)
   ↓
5. Menu → 2 (Add cards)
   ↓
6. Type: "add" then card name
   ↓
7. Repeat: Add 2-3 cards
   ↓
8. Menu → 3 (Rate cards)
   ↓
9. See: Top recommendations
   ↓
10. Type: "add 1" (add top pick)
    ↓
11. Repeat from step 5
    ↓
12. When done → Menu → 5 (Save)
```

## 🔍 CARD SEARCH TIPS

- **Partial names work**: "Jet" finds "Jetmir"
- **Fuzzy matching**: "Jethro" finds "Jetmir"
- **Case insensitive**: "jetmir" = "Jetmir"
- **Copy from Google**: Paste full names

## 📈 RATING FACTORS (Why is card rated X/10?)

✓ **Mana Curve** - Does deck need cards at this cost?
✓ **Color Match** - Is it the right colors?
✓ **Creature Ratio** - Do you need creatures or spells?
✓ **Synergies** - Does it combo with your cards?
✓ **Power Level** - Is it good for limited?
✓ **Deck Progress** - Do you need more cards?

## 🛠️ TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python 3.8+ from python.org |
| "Could not fetch sets" | Check internet connection |
| "Card not found" | Try partial name or check set |
| "App is slow" | First load = 20-30s (normal). Cached = <1s |
| "ImportError: requests" | Run: `pip install requests` |

## 📁 FILE LOCATIONS

| File | Purpose |
|------|---------|
| `main.py` | Run this to start app |
| `cache/` | Where set data is stored |
| `cache/*.deck` | Your saved decks |
| `config.py` | Customize ratings here |
| `START_HERE.md` | Read first |
| `README.md` | Full documentation |

## 🎓 DOCUMENTATION LINKS

| Need | File |
|------|------|
| Quick start | START_HERE.md |
| Full features | README.md |
| Example session | EXAMPLE_USAGE.md |
| How it works | DEVELOPER.md |
| File overview | PROJECT_STRUCTURE.md |

## ⚡ PRO TIPS

💡 **Update frequently** - Add cards every few picks for best recommendations
💡 **Check stats** - Ensure your deck is balanced
💡 **Review top 3** - Don't blindly take #1
💡 **Use details** - Check card text if unsure
💡 **Save often** - You can analyze drafts later

## 🎯 IDEAL DECK COMPOSITION

Target for 40-card deck:
- **Creatures**: ~26 (65%)
- **Spells**: ~14 (35%)
- **Lands**: Suggested 8-9 usually added separately

**Mana Curve**:
- 1-drop: 2-3 cards
- 2-drop: 3-4 cards
- 3-drop: 3 cards
- 4-drop: 2-3 cards
- 5-drop: 2 cards
- 6+: 1-2 cards

## 🎮 KEYBOARD SHORTCUTS

- `Ctrl+C` - Exit (gracefully stops)
- `Ctrl+L` - Clear screen (varies by terminal)
- Arrow keys - Browse text in some terminals

## 🌐 SUPPORTED SET CODES

Recent sets:
- `MOM` - March of the Machine
- `ONE` - Phyrexia: All Will Be One
- `DMU` - Dominaria United
- `BRO` - The Brothers' War
- `SIR` - Sire of Storms
- `LCI` - Lorcana
- `LTR` - Lord of the Rings

See full list by running app and searching!

## 💾 SAVING & LOADING DECKS

**Save deck:**
1. Menu → 5
2. Type filename: "MOM_Draft_11_14"
3. File saved to: cache/MOM_Draft_11_14.deck

**Load deck:**
1. Menu → 6
2. Select from list
3. Deck loaded!

## 🔧 CUSTOMIZATION

Edit `config.py` to change:
- Rating weights
- Creature ratio target
- Mana curve ideals
- Keywords to track
- Display colors
- And 40+ more options!

## 📞 GET HELP

1. **Quick questions**: Check START_HERE.md
2. **How to use**: Check README.md
3. **How it works**: Check DEVELOPER.md
4. **See examples**: Check EXAMPLE_USAGE.md
5. **Still stuck**: Check DELIVERY_CHECKLIST.md for complete feature list

## ✨ WHAT YOU GET

✅ Real MTG set data (1000+ sets)
✅ AI card recommendations (1-10 rating)
✅ Synergy detection
✅ Deck analysis
✅ Mana curve tracking
✅ Color optimization
✅ Save/load decks
✅ Colored terminal UI

## 🎉 YOU'RE READY!

Run: `python main.py`

Pick: Better cards, draft better decks!

---

**Printed:** November 14, 2025
**Application:** MTG Draft Deck Rating Engine v1.0
**Status:** ✅ Ready to use
