# MTG Draft Rater - Example Usage

This document shows what the application looks like in action.

## Starting the Application

```
$ python main.py

╔════════════════════════════════════════╗
║     MTG DRAFT DECK RATING ENGINE       ║
║                                        ║
║  Craft the perfect draft deck with AI  ║
║  card ratings based on synergy,        ║
║  mana curve, and metagame analysis     ║
╚════════════════════════════════════════╝

=== MTG Draft Deck Rater ===
1. Select a set to draft from
2. Add/update selected cards
3. Rate remaining cards
4. View deck statistics
5. Save deck
6. Load deck
7. Exit

Enter your choice (1-7):
```

## Selecting a Set

```
Enter your choice (1-7): 1

Fetching available MTG sets...

Available sets:
 1. Zendikar Rising                    (ZNR)
 2. Throne of Eldraine                 (ELD)
 3. Theros Beyond Death                (THB)
... and more

Enter set code (e.g., MOM) or search term: MOM

Fetching March of the Machine cards from Scryfall...
✓ Loaded 254 cards from March of the Machine
Ready to build your deck! Start by adding cards.
```

## Adding Cards During Draft

```
Enter your choice (1-7): 2

Currently selected cards (0/40):
  (none)

Commands:
  'add' - Add a card
  'remove N' - Remove card at position N
  'clear' - Clear all cards
  'done' - Return to main menu

Enter command: add
Enter card name: Jetmir, Nexus of Revels
✓ Added Jetmir, Nexus of Revels

Enter command: add
Enter card name: Anointed Peacekeeper
✓ Added Anointed Peacekeeper

Enter command: add
Enter card name: Bloodghast
✓ Added Bloodghast

Enter command: add
Enter card name: Execution Sentence
✓ Added Execution Sentence

Enter command: add
Enter card name: Territorial Kavu
✓ Added Territorial Kavu

Enter command: done
```

## Getting Card Recommendations

```
Enter your choice (1-7): 3

Analyzing your deck and rating cards...

Top 20 recommendations for your deck:

 1.  9.5/10 Cleansing Wildfire         [1R]            Sorcery
      → good mana curve fit (+2.0), strong limited card (+1.5)
 2.  9.2/10 Territorial Kavu           [1RG]           Creature — Kavu
      → balances deck (+1.0), creature synergy (+0.5)
 3.  9.0/10 Combat Courier             [W]             Creature — Human
      → good mana curve fit (+2.0), balances deck (+1.0)
 4.  8.8/10 Archangel of Tithes        [1WW]           Creature — Angel
      → color synergy (+1.5), strong limited card (+1.0)
 5.  8.5/10 Spell Queller              [1U]            Creature — Faerie Wizard
      → good mana curve fit (+1.5), color synergy (+1.0)
 6.  8.3/10 Aurelion                   [2W]            Creature — Dragon
      → creature synergy (+0.5), strong limited card (+1.0)
 7.  8.1/10 Skyclave Apparition        [1W]            Creature — Spirit
      → balances deck (+1.5), good mana curve fit (+1.0)
 8.  8.0/10 Insidious Roots            [1G]            Enchantment — Aura
      → color synergy (+1.5), some synergies (+0.5)
 9.  7.9/10 Bitterblossom              [1B]            Enchantment
      → token generation synergy (+1.0), strong limited card (+0.8)
10.  7.7/10 Unholy Heat                [R]             Instant
      → good mana curve fit (+2.0)
11.  7.5/10 Murktide                   [4U]            Creature — Dragon
      → mana curve already crowded (-1.0), strong limited card (+2.0)
12.  7.3/10 Omnath, Locus of Creation  [2GG]           Creature — Elemental
      → color synergy (+1.5), strong limited card (+1.5)
13.  7.1/10 Dragon's Rage Channeler    [R]             Creature — Human Shaman
      → good mana curve fit (+2.0)
14.  7.0/10 Counterspell               [UU]            Instant
      → throws off balance (-0.5), strong limited card (+1.5)
15.  6.9/10 Dress Down                 [1W]            Instant
      → good mana curve fit (+1.5)
16.  6.7/10 Recycling Beast            [2G]            Creature — Beast
      → color synergy (+1.0), good mana curve fit (+1.0)
17.  6.5/10 Misty Rainforest           [0]             Land — Forest Island
      → balances deck (+0.5), flexible (+0.2)
18.  6.3/10 Growth Spiral              [1G]            Instant
      → card draw synergy (+1.0), some synergies (+0.3)
19.  6.1/10 Hydroid Krasis             [XGU]           Creature — Jellyfish Hydra Beast
      → strong limited card (+1.5), mana curve already crowded (-0.5)
20.  5.9/10 Countervailing Winds       [3U]            Instant
      → throws off balance (-1.0), color conflict (-0.5)

Options: 'add N' (add card N), 'more' (show more), 'details N' (see card details), 'done'

Command: details 1
```

## Viewing Card Details

```
============================================================
Cleansing Wildfire
Sorcery
Mana Cost: [1R]

Exile target land. Its controller may search their library for a basic land card and put it onto the battlefield tapped. If that player does, they shuffle their library.

Keywords: land destruction, ramp acceleration
============================================================
```

## Viewing Deck Statistics

```
Enter your choice (1-7): 4

============================================================
DECK STATISTICS - March of the Machine
============================================================

Deck Size: 15/40 cards
Creatures: 8 (53%)
Spells: 7
Average CMC: 2.31

Mana Curve:
  0: (0)
  1: ███████ (4)
  2: ███████████ (7)
  3: ███ (2)
  4: ██ (1)
  5: █ (1)
  6+: (0)

Colors: white, red, green

Detected Themes/Synergies:
  • WRG colors
  • token generation
  • land synergy
  • removal spells

============================================================
```

## Saving Your Deck

```
Enter your choice (1-7): 5

Enter filename (without extension): MOM_Draft_2024_11_14
✓ Deck saved to cache/MOM_Draft_2024_11_14.deck
```

## Loading a Saved Deck

```
Enter your choice (1-7): 6

Available decks:
  1. MOM_Draft_2024_11_14
  2. DMU_Draft_Previous

Select deck (number): 1

Loading March of the Machine...
✓ Deck loaded: 15 cards
```

## Analysis Features Explained

### Mana Curve Fit
Shows how well a card fills gaps in your mana curve. The application aims for:
- 2-3 one-mana spells
- 3-4 two-mana spells
- 2-3 three-mana spells
- And so on

### Color Synergy
Evaluates how well a card's color aligns with your current colors:
- +1.5 if card is in your main colors
- -2.0 if mono-colored outside your colors
- +0.5 if colorless (always flexible)

### Creature/Spell Balance
Maintains roughly 65% creatures and 35% non-creature spells (optimal for limited).

### Synergies
Detects keyword overlaps (flying, sacrifice, card draw, etc.) and creature types.

### Limited Power Level
Prioritizes:
- Removal spells
- Card draw
- Efficient creatures (good power/toughness for cost)

## Tips and Tricks

1. **Update frequently**: The more cards you add, the better the recommendations
2. **Check "more" for budget picks**: Not always top-rated cards are the best picks
3. **Review statistics**: Ensure your deck is balanced before finalizing
4. **Save intermediate drafts**: You can load and continue later
5. **Use fuzzy matching**: Type partial names like "Jetm" instead of full name

## Keyboard Shortcuts and Commands

| Context | Command | Effect |
|---------|---------|--------|
| Main Menu | 1 | Select set |
| Main Menu | 2 | Add/modify cards |
| Main Menu | 3 | Get recommendations |
| Main Menu | 4 | View statistics |
| Main Menu | 5 | Save deck |
| Main Menu | 6 | Load deck |
| Main Menu | 7 | Exit |
| Card Manager | add | Add a card |
| Card Manager | remove N | Remove card at position N |
| Card Manager | clear | Clear entire deck |
| Card Manager | done | Return to menu |
| Ratings View | add N | Add recommended card N |
| Ratings View | details N | View card N details |
| Ratings View | more | Show next 20 cards |
| Ratings View | done | Return to menu |

## Understanding Ratings

- **9-10**: Excellent picks - strong in limited, good synergies
- **7-8**: Good picks - fills curve well, decent power level
- **5-6**: Situational - might be needed, fills a gap
- **3-4**: Weak picks - consider carefully
- **1-2**: Poor picks - likely won't help your deck

The rating algorithm considers many factors beyond just raw card power - it's specifically tuned for limited draft gameplay.
