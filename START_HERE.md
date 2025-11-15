# 🎴 MTG DRAFT DECK RATING ENGINE - START HERE

Welcome! This is your guide to building the perfect MTG draft deck.

## ⚡ Quick Start (2 minutes)

```bash
# 1. Make sure you're in the project folder
cd "Rate_This_Card"

# 2. Run the application
python main.py

# 3. Select a set (e.g., "MOM" for March of the Machine)

# 4. Start adding cards as you draft

# 5. Get AI-powered card recommendations
```

## 🎯 What This Does

This application helps you during draft by:

1. **Analyzing your cards** - Looks at what you've picked so far
2. **Understanding synergies** - Detects themes and keyword overlaps
3. **Rating remaining cards** - Scores 1-10 based on deck fit
4. **Providing recommendations** - Shows you the best picks next

Example flow:
```
You pick: Jetmir, Anointed Peacekeeper, Bloodghast
↓
App analyzes: "White-red-green deck with creature theme"
↓
App rates cards: "This removal spell scores 9.5"
↓
You pick: Cleansing Wildfire
↓
Repeat!
```

## 📖 Learning Path

**New to the app? Follow this order:**

1. **First 5 minutes**
   - Run `python main.py`
   - Try selecting a set and adding a few cards
   - See what recommendations look like
   - Get comfortable with the interface

2. **Next 10 minutes**
   - Read `EXAMPLE_USAGE.md`
   - See what the output looks like
   - Understand what ratings mean (8+ is great, 5 is okay, <3 is weak)
   - Learn the commands

3. **During your first draft**
   - Select your set
   - Add cards as you pick them
   - Use "Rate cards" before each pick
   - Check statistics to monitor deck health

4. **Optimization (optional)**
   - Read `README.md` for full features
   - Check `DEVELOPER.md` to understand the algorithm
   - Edit `config.py` to customize ratings

## 🚀 Installation Check

Make sure everything works:

```bash
# Run this test
python test_application.py

# You should see:
# ✓ Test 1: Fetching available MTG sets...
# ✓ Test 2: Fetching cards from a set...
# ✓ Test 3: Parsing card data...
# ✓ Test 4: Testing card rating engine...
# ✓ Test 5: Performance check
# ✓ All tests passed!
```

If you see errors, your Python or internet connection might have issues.

## 💡 How It Works

### Rating Scale

- **9-10** 🟢 Excellent - Take it!
- **7-8** 🟡 Good - Solid pick
- **5-6** 🟡 Okay - Fills a slot
- **3-4** 🟠 Weak - Consider passing
- **1-2** 🔴 Bad - Probably pass

### What the Ratings Consider

Each card's score comes from:

✓ **Mana Curve** - Do you need cards at this cost?
✓ **Color Synergy** - Does it match your colors?
✓ **Creature Balance** - Do you need creatures or spells?
✓ **Synergies** - Does it work with your other cards?
✓ **Power Level** - Is it good for limited draft?
✓ **Deck Completion** - Do you need more cards?

Example: A flying creature at 2 mana that matches your colors scores high because it:
- Fits your mana curve perfectly (2-drop slot is open)
- Matches your colors (+1.5 points)
- Is a creature when you need more (+1.0 points)
- Has evasion (flying is valuable) (+0.5 points)
- Gets a completion bonus (filling your deck)

## 🎮 Basic Commands

```
Main Menu:
1 = Pick a set to draft from
2 = Add/remove cards from your deck
3 = Get card recommendations (most important!)
4 = View deck statistics
5 = Save your deck
6 = Load a saved deck
7 = Exit

When adding cards:
- Type "add" to add a card
- Type "remove 1" to remove the first card
- Type "done" to go back

When rating cards:
- Type "add 1" to add the top recommendation
- Type "details 1" to see card info
- Type "more" to see more recommendations
- Type "done" to go back
```

## 📊 Example Session

```
1. Start: python main.py
2. Menu: Select 1 (pick set)
3. Search: Type "MOM" (March of the Machine)
4. Wait: ~20 seconds to load (first time only)
5. Menu: Select 2 (add cards)
6. Add cards: "Jetmir" → "Anointed Peacekeeper" → "Bloodghast"
7. Menu: Select 3 (rate cards)
8. See: Top 20 recommendations ranked 1-10
9. Add best ones: "add 1", "add 2", "add 3"
10. Repeat: Every few picks, rate again
11. Save: When done, select 5 to save your deck
```

## 🆘 Troubleshooting

### "Could not fetch sets"
- Check your internet connection
- Try again in a few moments
- Scryfall servers might be temporarily down

### "Card not found"
- Try partial names (e.g., "Jet" for "Jetmir")
- Check the card is in the set
- Use fuzzy matching (it usually works)

### Application is slow
- First set load takes 20-30 seconds (normal)
- Rating takes 2-5 seconds (normal)
- Subsequent loads use cache and are instant

### Python not found
- Make sure Python 3.8+ is installed
- Try: `python --version`
- If error: Install Python from python.org

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete user guide with all features |
| **EXAMPLE_USAGE.md** | See what the app looks like in action |
| **DEVELOPER.md** | How the algorithm works (for nerds) |
| **config.py** | Customize ratings and behavior |
| **PROJECT_STRUCTURE.md** | Technical file overview |

## 🎓 Pro Tips

1. **Add cards frequently** - More data = better recommendations
2. **Check deck stats** - Make sure your balance is good
3. **Review suggestions** - Don't blindly take #1, see why each card ranks
4. **Use details view** - Check card text if you're unsure
5. **Save your drafts** - You can analyze them later

## ❓ FAQs

**Q: Does this work with real MTG sets?**
A: Yes! Uses actual Scryfall data for 1000+ sets.

**Q: Do I need internet?**
A: Yes for first load, then everything is cached locally.

**Q: Can I customize the ratings?**
A: Yes! Edit config.py to adjust weights and thresholds.

**Q: How accurate is this?**
A: Pretty good! Based on mana curve, colors, synergies, and limited power level analysis.

**Q: Can I use this with Arena?**
A: Not directly, but you can type in your picks manually.

**Q: What if I disagree with a rating?**
A: The algorithm is conservative - trust your judgment if you know better!

## 🚦 Your First Draft

1. **Before starting**
   - Have this app running
   - Have your set ready to draft

2. **During draft**
   - Add each card immediately after picking
   - Before each next pick, check ratings
   - Use recommendations as a guide
   - Trust your instincts if you disagree

3. **After draft**
   - Save your deck
   - Check statistics
   - Review how well the algorithm predicted

## 🎯 Next Steps

### Beginners
→ Run `python main.py` right now!

### Intermediate Users  
→ Read `EXAMPLE_USAGE.md` to see the full capabilities

### Advanced Users
→ Check `DEVELOPER.md` to understand/modify the algorithm

### Developers
→ Edit `card_rating_engine.py` to add new factors

## ✨ Key Features

✓ Real MTG set data (1000+ sets available)
✓ AI card rating based on 6 factors
✓ Synergy and theme detection
✓ Mana curve analysis
✓ Color synergy tracking
✓ Creature/spell balance
✓ Deck statistics
✓ Save/load functionality
✓ Fuzzy card search
✓ Beautiful colored output

## 🤝 Support

Having issues?
1. Check `README.md` Troubleshooting section
2. Run `python test_application.py` to verify setup
3. Review `EXAMPLE_USAGE.md` for expected behavior
4. Check `DEVELOPER.md` for technical details

---

**Ready? Type this now:**
```
python main.py
```

**Happy drafting! 🎴**
