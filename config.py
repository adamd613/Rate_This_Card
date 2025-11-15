"""
Configuration file for MTG Draft Rater
Customize the application behavior here
"""

# ==========================================
# RATING WEIGHTS
# ==========================================
# Adjust how much each factor affects the final rating

RATING_WEIGHTS = {
    # Mana curve analysis (base ±2.0)
    "mana_curve_perfect_fit": 2.0,
    "mana_curve_good_fit": 1.0,
    "mana_curve_crowded": -1.5,
    
    # Color analysis (base ±1.5)
    "color_perfect_fit": 1.5,
    "color_good_fit": 0.5,
    "color_conflict": -2.0,
    "colorless_bonus": 0.5,
    
    # Balance analysis (base ±1.5)
    "creature_needed": 1.5,
    "spell_needed": 1.5,
    "balance_penalty": -1.0,
    
    # Power level (base 0-1.5)
    "removal_spell": 1.5,
    "card_draw": 1.0,
    "good_value": 1.5,
    "great_value": 0.5,
    "poor_value": -1.0,
    
    # Synergies (variable)
    "keyword_synergy": 1.0,
    "creature_type_synergy": 0.5,
    "theme_synergy": 0.5,
}

# ==========================================
# IDEAL DECK COMPOSITION
# ==========================================

# Target creature ratio (0.65 = 65% creatures)
TARGET_CREATURE_RATIO = 0.65

# Target spell ratio (0.35 = 35% spells)
TARGET_SPELL_RATIO = 0.35

# Ideal mana curve distribution (CMC -> count for 40-card deck)
IDEAL_MANA_CURVE = {
    0: 0,      # 0-drops
    1: 2.5,    # 1-drops (2-3 cards)
    2: 3.5,    # 2-drops (3-4 cards)
    3: 3.0,    # 3-drops (3 cards)
    4: 2.5,    # 4-drops (2-3 cards)
    5: 2.0,    # 5-drops (2 cards)
    6: 1.5,    # 6-drops (1-2 cards)
}

# Threshold for mana curve adjustment
# How far from ideal before penalty kicks in
MANA_CURVE_TOLERANCE = 1

# ==========================================
# DISPLAY SETTINGS
# ==========================================

# Number of top recommendations to display initially
TOP_RECOMMENDATIONS_DISPLAY = 20

# Number of recommendations per "more" command
RECOMMENDATIONS_PER_PAGE = 20

# Use colored terminal output
USE_COLOR = True

# ==========================================
# API SETTINGS
# ==========================================

# Scryfall API base URL
SCRYFALL_API_URL = "https://api.scryfall.com"

# Cache directory for set data
CACHE_DIRECTORY = "cache"

# Cache expiration time in seconds (set to 0 for no expiration)
# 7 days = 604800 seconds
CACHE_EXPIRATION = 604800

# ==========================================
# KEYWORD ANALYSIS
# ==========================================

# Keywords to track for synergy detection
TRACKED_KEYWORDS = [
    "flying", "lifelink", "vigilance", "haste", "deathtouch", "double strike",
    "trample", "shroud", "indestructible", "regenerate", "menace", "hexproof",
    "flash", "prowess", "drain", "ramp", "tutor", "draw", "discard",
    "mill", "etb", "enter the battlefield", "sacrifice", "token", "scry",
    "surveil", "adapt", "mutate", "kicker", "spell mastery", "aftermath",
    "flashback", "madness", "delve", "revolt", "enrage", "proliferate",
    "graveyard", "recurring", "protection", "evasion", "bounce", "counterspell",
    "removal", "wrath", "board wipe", "pump", "cantrip", "value"
]

# Synergy keywords (get big boost when detected together)
SYNERGY_KEYWORDS = {
    "flying": 1.0,
    "sacrifice": 1.0,
    "token": 1.0,
    "graveyard": 0.75,
    "proliferate": 0.75,
    "mill": 0.75,
    "draw": 0.75,
    "counterspell": 0.75,
}

# ==========================================
# CREATURE TYPE TRACKING
# ==========================================

# Creature types to track (enable tribal synergies)
TRACKED_CREATURE_TYPES = [
    "human", "elf", "goblin", "zombie", "spirit", "beast", "dragon",
    "faerie", "vampire", "werewolf", "merfolk", "wizard", "cleric",
    "warrior", "knight", "rogue", "scout", "soldier", "cat", "dog",
]

# Minimum creature type count to boost synergy
CREATURE_TYPE_SYNERGY_THRESHOLD = 2

# ==========================================
# SET-SPECIFIC SETTINGS
# ==========================================

# You can define set-specific rating adjustments here
# Format: "SET_CODE": {"adjustment_type": value}
SET_SPECIFIC_RATINGS = {
    # Example: Enhance creature types in specific sets
    "MOM": {
        "phyrexian_boost": 0.5,  # Boost phyrexian creatures
    },
    "STX": {
        "lesson_boost": 0.3,  # Boost lesson cards
        "school_matters": 0.5,  # School payoff cards
    },
}

# ==========================================
# RARITY WEIGHTS
# ==========================================

# Bonus for different rarities
RARITY_WEIGHTS = {
    "common": 0.0,
    "uncommon": 0.2,
    "rare": 0.5,
    "mythic": 0.5,
}

# ==========================================
# FUZZY MATCHING
# ==========================================

# Maximum Levenshtein distance for card name matching
MAX_MATCH_DISTANCE = 3

# Minimum substring match percentage
MIN_SUBSTRING_MATCH = 0.6

# ==========================================
# LOGGING
# ==========================================

# Enable debug logging
DEBUG_MODE = False

# Log file location (set to None to disable)
LOG_FILE = None

# ==========================================
# EXPERIMENTAL FEATURES
# ==========================================

# Enable draft prediction (experimental)
ENABLE_DRAFT_PREDICTION = False

# Enable metagame analysis (experimental)
ENABLE_METAGAME_ANALYSIS = False

# Enable ML-based ratings (experimental)
ENABLE_ML_RATINGS = False

# ==========================================
# DEFAULTS
# ==========================================

# Default deck size (typically 40 for limited)
DEFAULT_DECK_SIZE = 40

# Default minimum deck size (can go lower in some formats)
MIN_DECK_SIZE = 40

# Default maximum deck size
MAX_DECK_SIZE = 100

# Number of lands to suggest
SUGGESTED_LAND_COUNT = 8

# ==========================================
# QUALITY OF LIFE
# ==========================================

# Show rating breakdown on card details
SHOW_RATING_BREAKDOWN = True

# Automatically suggest next 5 cards after adding
AUTO_SUGGEST_AFTER_ADD = False

# Warn if deck is imbalanced
WARN_ON_IMBALANCED = True

# ==========================================
# ADVANCED
# ==========================================

# Performance optimization: cache analysis results
CACHE_ANALYSIS_RESULTS = True

# Performance optimization: limit rating calculations
# Set to 0 for no limit
MAX_CARDS_TO_RATE = 0

# Enable advanced statistics
SHOW_ADVANCED_STATS = False

# ==========================================
# Integration Options
# ==========================================

# Auto-save deck every N cards
AUTO_SAVE_INTERVAL = 5  # Save every 5 cards added

# Export format preferences
EXPORT_FORMATS = ["mtga", "arena", "decklist"]
