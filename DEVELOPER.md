# Developer Documentation

## Project Architecture

### Overview
The MTG Draft Rater is a modular Python application designed to rate and recommend cards for MTG draft decks. It consists of three main components:

```
┌─────────────────────────────────────────────────────┐
│              main.py (CLI Interface)                │
│    - User interaction, menu system, I/O handling    │
└──────────────────┬──────────────────┬──────────────┘
                   │                  │
        ┌──────────▼─────────┐   ┌────▼──────────────┐
        │  scryfall_api.py   │   │ card_rating_      │
        │                    │   │ engine.py         │
        │  - API Integration │   │                   │
        │  - Data Fetching   │   │  - Card Analysis  │
        │  - Caching         │   │  - Rating Logic   │
        │  - Parsing         │   │  - Synergy Detect │
        └────────────────────┘   └───────────────────┘
```

## Module Documentation

### scryfall_api.py

**Purpose**: Interface with the Scryfall REST API to fetch and parse MTG card data.

**Key Classes**:
- `ScryfallAPI`: Static methods for API interaction

**Key Methods**:

- `get_set_codes() -> List[Dict[str, str]]`
  - Fetches all available MTG sets from Scryfall
  - Returns: List of sets with code and name
  - API Endpoint: `/sets`

- `get_set_cards(set_code: str) -> List[Dict[str, Any]]`
  - Fetches all cards in a specific set
  - Handles pagination automatically
  - Returns: Raw card data from Scryfall
  - API Endpoint: `/cards/search?q=set:{code}`

- `parse_card_data(card: Dict) -> Dict[str, Any]`
  - Extracts relevant card attributes
  - Simplifies nested Scryfall data structure
  - Returns: Structured card object

**Data Structure** (parsed card):
```python
{
    "name": str,                 # Card name
    "set_code": str,             # Set code
    "type_line": str,            # Full type line (e.g., "Creature — Elf Druid")
    "oracle_text": str,          # Card ability text
    "mana_cost": str,            # Mana cost string (e.g., "{1}{W}{B}")
    "cmc": float,                # Converted mana cost
    "is_creature": bool,         # Whether it's a creature
    "is_instant": bool,          # Whether it's an instant
    "is_sorcery": bool,          # Whether it's a sorcery
    "is_enchantment": bool,      # Whether it's an enchantment
    "is_artifact": bool,         # Whether it's an artifact
    "is_land": bool,             # Whether it's a land
    "power": str or None,        # Power (creatures only)
    "toughness": str or None,    # Toughness (creatures only)
    "colors": List[str],         # Color codes (W/U/B/R/G)
    "color_identity": List[str], # All colors in mana cost
    "rarity": str,               # Card rarity
    "oracle_text_lower": str,    # Lowercase oracle text
    "keywords": List[str],       # Extracted keywords
    "image_url": str,            # Card image URL
    "scryfall_uri": str          # Scryfall card page URL
}
```

### card_rating_engine.py

**Purpose**: Analyze deck composition and rate cards based on multiple factors.

**Key Classes**:
- `CardRatingEngine`: Main rating engine

**Initialization**:
```python
engine = CardRatingEngine(all_cards_in_set)
```

**Key Methods**:

- `rate_cards(selected_cards: List[str]) -> List[tuple]`
  - Main entry point for card rating
  - Parameters: List of card names already selected
  - Returns: List of (name, rating, explanation, card_data) tuples, sorted by rating
  - Example output: `[("Creature A", 8.5, "good mana curve fit", {...}), ...]`

**Rating Algorithm**:

The engine rates cards on a 1-10 scale by analyzing:

1. **Mana Curve Fit** (±2.0 points)
   - Checks current distribution vs. ideal
   - Ideal: 2-3 of each 1-4 drop, tapering for higher
   - Big boost if filling a gap, penalty if crowded

2. **Color Synergy** (±1.5 points)
   - Analyzes deck color identity
   - Perfect fit if card is in main colors
   - Heavy penalty for off-color mono-colored cards
   - Flexible cards (colorless) always acceptable

3. **Creature/Spell Balance** (±1.5 points)
   - Targets ~65% creatures, ~35% spells
   - Boosts creatures if ratio too low
   - Boosts spells if ratio too high

4. **Synergy Detection** (0-3+ points)
   - Keyword overlaps (flying, sacrifice, token, etc.)
   - Creature type matches
   - Theme synergies

5. **Limited Power Level** (0-1.5 points)
   - Removal spells highly valued
   - Card draw valuable
   - Efficient creatures (stats/cost ratio)

6. **Completion Bonus** (0-1 points)
   - Encourages filling the 40-card deck

**Example Rating Factors**:
```
Card: "Counterspell"
Base: 5.0
+ Mana curve fit: +2.0 (fills low curve)
+ Color synergy: +1.5 (in main colors)
- Balance: -0.5 (already have many spells)
+ Power level: +1.5 (excellent removal)
+ Synergy: +0.5 (synergizes with control theme)
= Final: 10.0/10
```

**Internal Methods**:

- `_analyze_deck(deck_cards) -> Dict[str, Any]`
  - Generates comprehensive deck statistics
  - Returns analysis object with:
    - Creature/spell counts
    - CMC distribution and curve
    - Color information
    - Detected keywords and synergies

- `_detect_synergies(deck_cards, analysis) -> List[str]`
  - Identifies themes and synergies
  - Checks keyword frequencies
  - Detects color patterns
  - Finds creature type overlaps

- `_rate_X(card, ...) -> float`
  - Individual rating functions:
    - `_rate_mana_curve_fit()`
    - `_rate_color_fit()`
    - `_rate_deck_balance()`
    - `_rate_synergies()`
    - `_rate_limited_power()`

### main.py

**Purpose**: CLI interface and user interaction layer.

**Key Classes**:
- `MTGDraftRater`: Main application controller

**Key Methods**:

- `run()`: Main application loop
- `_select_set()`: Set selection interface
- `_load_set()`: Load cards from Scryfall
- `_add_cards()`: Card management interface
- `_rate_cards()`: Display ratings and recommendations
- `_view_statistics()`: Display deck analysis
- `_save_deck()`: Persist deck to file
- `_load_deck()`: Load saved deck

**UI Features**:
- Colored terminal output (using colorama)
- Fuzzy card name matching
- Interactive menus
- Card detail viewing
- Batch operations

## Data Flow

### Typical User Session

```
1. User selects set
   ↓
2. Check cache, fetch if needed
   ↓
3. Parse all cards into engine
   ↓
4. User adds cards
   ↓
5. User requests ratings
   ↓
6. Engine analyzes current deck
   ↓
7. Engine rates all remaining cards
   ↓
8. Results sorted and displayed
   ↓
9. User selects cards to add
   ↓
10. Repeat from step 4
```

### API Integration Flow

```
Scryfall API
    ↓
Raw card JSON
    ↓
parse_card_data()
    ↓
Structured card object
    ↓
CardRatingEngine
    ↓
Analyzed and rated
```

## Caching System

The application caches:

1. **Set Data** (`cache/{SET_CODE}.json`)
   - All cards from a set
   - Indexed by card name
   - TTL: Permanent (set data doesn't change)

2. **Decks** (`cache/{filename}.deck`)
   - Selected cards
   - Set information
   - Format: JSON with metadata

## Performance Considerations

### Time Complexity
- Set loading: O(n) where n = cards in set (~500)
- Card rating: O(m × n) where m = selected cards, n = remaining cards
- Typical times:
  - First set load: 20-30 seconds (API calls)
  - Subsequent loads: <1 second (cached)
  - Card rating: 2-5 seconds (computation)

### Memory Usage
- Typical set: ~10-20 MB (300-500 cards)
- Application: ~50 MB total with dependencies

### Optimization Opportunities
- Implement LRU cache for fuzzy matching
- Pre-compute keyword analysis
- Use numpy for rating calculations
- Lazy-load card details on demand

## Extension Points

### Adding New Rating Factors

To add a new rating factor:

1. Create method in `CardRatingEngine`:
   ```python
   def _rate_new_factor(self, card, deck_cards, analysis) -> float:
       """Calculate bonus/penalty for new factor"""
       score = 0.0
       # Logic here
       return score
   ```

2. Call in `_rate_card()`:
   ```python
   new_score = self._rate_new_factor(card, deck_cards, analysis)
   rating += new_score
   if new_score != 0:
       reasons.append(f"new factor ({new_score:+.1f})")
   ```

### Adding New Set Filters

Modify `_rate_limited_power()` or add set-specific logic:
```python
def _rate_for_set(self, card, set_code) -> float:
    """Set-specific rating adjustments"""
    if set_code == "MOM":
        if "phyrexian" in card["type_line"].lower():
            return 1.0  # Boost phyrexian in MOM
    return 0.0
```

### Integrating with Other APIs

The API layer is abstracted in `scryfall_api.py`. To support other sources:

1. Create new API class with same interface
2. Implement `get_set_codes()`, `get_set_cards()`, `parse_card_data()`
3. Update `main.py` to instantiate correct API

## Testing

### Unit Tests

Create `tests/test_rating_engine.py`:
```python
def test_mana_curve_rating():
    cards = [...]  # Test cards
    engine = CardRatingEngine(cards)
    analysis = engine._analyze_deck(cards[:5])
    assert analysis["cmc_distribution"][1] == 2
```

### Integration Tests

Test full workflows:
```python
def test_full_draft_session():
    engine = CardRatingEngine(set_cards)
    ratings = engine.rate_cards(["Card A", "Card B"])
    assert len(ratings) > 0
    assert all(1 <= r[1] <= 10 for r in ratings)
```

### Performance Profiling

```python
import cProfile
cProfile.run('engine.rate_cards(selected_cards)')
```

## Known Issues and Limitations

1. **No predictive analysis** - Doesn't predict future picks
2. **Limited draft context** - Assumes unknown future cards
3. **No MTGA integration** - Can't connect to Arena directly
4. **Keyword detection** - Basic regex-based, not comprehensive
5. **No P1P1 bias** - Treats all picks equally regardless of signal

## Future Enhancement Ideas

### Short Term
- [ ] Better keyword extraction (parse more complex abilities)
- [ ] Creature type database (enable tribal synergies)
- [ ] Draft format support (sealed, cube, etc.)
- [ ] Import from Arena/Cockatrice

### Medium Term
- [ ] Machine learning model for ratings
- [ ] Integration with draft tracking (17lands, etc.)
- [ ] Web interface
- [ ] Real-time deck optimization

### Long Term
- [ ] Network effect analysis
- [ ] Multi-user draft analysis
- [ ] AI drafting opponent
- [ ] Mobile app

## Dependencies

- **requests**: HTTP library for API calls
- **colorama**: Terminal color output

### Optional Dependencies
- **numpy**: For advanced numerical analysis
- **matplotlib**: For visualization
- **flask**: For web interface (future)

## Code Style

Follow PEP 8:
- 4-space indentation
- Docstrings for all functions
- Type hints for clarity
- Constants in UPPER_CASE

## Contributing

1. Fork and create feature branch
2. Make changes following code style
3. Add tests for new features
4. Verify with `test_application.py`
5. Submit pull request

## License

This tool uses Scryfall API. See https://scryfall.com/ for terms of service.
