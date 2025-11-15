# MTG Draft Deck Rating Engine

A comprehensive tool to craft the perfect MTG draft deck in real-time during drafting sessions.

## Features

### 🎯 Intelligent Card Rating System
- **Mana Curve Analysis**: Rates cards based on how they fit into your deck's mana curve
- **Color Synergy**: Analyzes color identity and penalizes off-color cards
- **Creature/Spell Balance**: Maintains optimal deck composition (~65% creatures in limited)
- **Synergy Detection**: Identifies keyword synergies, creature types, and theme synergies
- **Limited Format Power Level**: Evaluates cards specifically for limited draft gameplay
- **Metagame Awareness**: Considers set-specific themes and mechanics

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

## How to Use

### Installation

1. Navigate to the project directory:
```bash
cd "Rate_This_Card"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

Or if you have Python in your PATH:
```bash
python main.py
```

### Workflow During Draft

1. **Select a Set**: Choose which MTG set you're drafting from
   - Search by set code (e.g., MOM, DMU, BRO)
   - The app will fetch and cache all cards from that set

2. **Add Selected Cards**: Build your card list as you draft
   - Type card names as you pick them
   - Use fuzzy matching for quick input
   - View your current deck at any time

3. **Get Recommendations**: Ask for card ratings
   - See top 20 recommendations with ratings (1-10)
   - Understand why each card is recommended
   - Browse detailed card information
   - Add recommended cards directly

4. **Track Your Deck**: Monitor statistics
   - View mana curve
   - Check color distribution
   - See detected themes and synergies
   - Ensure creature/spell balance

5. **Save Your Work**: Keep your drafts
   - Save completed or in-progress decks
   - Load previous drafts to continue or analyze

## Rating Factors

Each card receives a 1-10 rating based on:

### Mana Curve Fit (±2.0 points)
- Cards at needed mana costs get big boosts
- Over-represented mana costs get penalties
- Aims for: 2-3 one-mana, 3-4 two-mana, etc.

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
- Rates removal spells highly
- Card draw is valuable
- Good stats-to-cost ratio

### Deck Completion (0-1 points)
- Bonus for cards when deck is under 40 cards
- Encourages filling your deck

## Example Session

```
=== MTG Draft Deck Rater ===
1. Select a set to draft from
2. Add/update selected cards
3. Rate remaining cards
4. View deck statistics
5. Save deck
6. Load deck
7. Exit

Enter your choice (1-7): 1

Available sets:
 1. March of the Machine (MOM)
 2. Phyrexia: All Will Be One (ONE)
 3. The Brothers' War (BRO)
... and more

Enter set code (e.g., MOM) or search term: MOM

Fetching March of the Machine cards from Scryfall...
✓ Loaded 254 cards from March of the Machine

Enter your choice (1-7): 2

Enter command: add
Enter card name: Jetmir, Nexus of Revels
✓ Added Jetmir, Nexus of Revels

Enter command: add
Enter card name: Anointed Peacekeeper
✓ Added Anointed Peacekeeper

Enter command: done

Enter your choice (1-7): 3

Analyzing your deck and rating cards...

Top 20 recommendations for your deck:

 1.  8.5/10 Gleaming Barrier         [1W]            Creature — Wall
      → good mana curve fit, color synergy
 2.  8.3/10 Intrepid Adversary       [1W]            Creature — Human
      → strong limited card, color synergy
 3.  8.1/10 Combat Courier           [W]             Creature — Human
      → good mana curve fit
...
```

## Caching

The application caches all fetched set data locally in the `cache/` directory:
- Set data is cached as JSON files (e.g., `MOM.json`)
- Decks are saved as `.deck` files
- First load of a set requires internet; subsequent loads are instant

## Troubleshooting

### "Could not fetch sets. Check your internet connection."
- Verify you have an active internet connection
- Scryfall API might be temporarily unavailable
- Try again in a few moments

### Card not found when adding
- Try typing partial card names
- The fuzzy matcher will find close matches
- Check spelling and set membership

### Application is slow
- First load of a set requires API calls (~20-30 seconds)
- Subsequent loads use cached data and are instant
- Ratings take a few seconds to compute (normal)

## Technical Details

### Architecture

- **`scryfall_api.py`**: Integrates with Scryfall REST API
- **`card_rating_engine.py`**: Implements rating algorithm
- **`main.py`**: CLI application and user interface

### API Integration

Uses the free **Scryfall API** (https://scryfall.com/docs/api):
- No authentication required
- Respects rate limiting
- Returns comprehensive card data

### Rating Algorithm

The rating engine considers:
1. **Mana Curve Distribution** - Ensures playable cards at each stage
2. **Color Constraints** - Optimizes for mana consistency
3. **Creature/Spell Split** - Maintains combat-focused strategy
4. **Keyword Synergies** - Amplifies theme payoffs
5. **Power Level** - Prioritizes efficient cards
6. **Creature Types** - Enables tribal synergies

## Tips for Best Results

1. **Add cards as you draft** - Update recommendations in real-time
2. **Review top 20 suggestions** - Usually contains best picks
3. **Check card details** - Understand the recommendations
4. **Use "View statistics"** - Monitor deck health
5. **Start with set's main themes** - Most sets have 2-3 main archetypes

## Known Limitations

- Ratings are for **Limited format** (can't account for unknown future cards)
- Card interactions are keyword-based (not exhaustive)
- Does not predict future picks
- Metagame shifts during a draft are not predicted
- No support for custom card data (only Scryfall)

## Requirements

- Python 3.8+
- Internet connection (first use per set)
- ~500MB disk space for full set cache

## License

This tool uses data from Scryfall, which is maintained by Scryfall LLC. See https://scryfall.com/ for more information.

## Future Enhancements

Possible improvements:
- [ ] Machine learning model for better ratings
- [ ] Support for sealed format
- [ ] Curve optimization suggestions
- [ ] Card combo database
- [ ] Graphical UI
- [ ] Integration with draft tracking websites
- [ ] Export to MTG Arena/Cockatrice
