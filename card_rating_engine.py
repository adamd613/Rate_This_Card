"""
Card rating and analysis engine for MTG draft
"""
from typing import List, Dict, Any, Set
import re
from collections import Counter

class CardRatingEngine:
    """Analyzes and rates cards based on deck composition"""
    
    def __init__(self, set_cards: List[Dict[str, Any]]):
        """Initialize the rating engine with all cards from the set"""
        self.all_cards = set_cards
        self.card_lookup = {card["name"].lower(): card for card in set_cards}
        
        # Pre-process creature types and keywords for faster lookup
        self._creature_type_cache = {}
        self._keyword_cache = {}
        self._power_toughness_cache = {}
        for card in set_cards:
            card_name = card["name"]
            self._creature_type_cache[card_name] = self._extract_creature_types(card["type_line"])
            self._keyword_cache[card_name] = set(card.get("keywords", []))
            if card.get("is_creature"):
                try:
                    self._power_toughness_cache[card_name] = (
                        float(card.get("power", 0)),
                        float(card.get("toughness", 0))
                    )
                except (ValueError, TypeError):
                    self._power_toughness_cache[card_name] = (0, 0)
    
    def rate_cards(self, selected_cards: List[str], format_legality: str = "draft") -> List[tuple]:
        """
        Rate all cards in the set based on existing deck composition.
        Returns list of tuples: (card_name, rating, explanation)
        Includes cards already in the deck.
        """
        # Parse selected cards
        deck_cards = self._parse_selected_cards(selected_cards)
        if not deck_cards:
            return []
        
        # Analyze current deck state
        deck_analysis = self._analyze_deck(deck_cards)
        
        # Rate each card in the set (including those already in deck)
        ratings = []
        for card in self.all_cards:
            rating, explanation = self._rate_card(card, deck_cards, deck_analysis)
            ratings.append((card["name"], rating, explanation, card))
        
        # Sort by rating (descending)
        ratings.sort(key=lambda x: x[1], reverse=True)
        
        return ratings
    
    def _parse_selected_cards(self, card_names: List[str]) -> List[Dict[str, Any]]:
        """Convert card names to full card objects"""
        deck_cards = []
        for name in card_names:
            name_lower = name.lower().strip()
            if name_lower in self.card_lookup:
                deck_cards.append(self.card_lookup[name_lower])
            else:
                # Try fuzzy matching
                match = self._fuzzy_match_card(name_lower)
                if match:
                    deck_cards.append(match)
        
        return deck_cards
    
    def _fuzzy_match_card(self, card_name: str) -> Dict[str, Any] or None:
        """Attempt fuzzy matching for card names"""
        card_name = card_name.strip().lower()
        
        # Direct substring match
        for name, card in self.card_lookup.items():
            if card_name in name or name in card_name:
                return card
        
        # Levenshtein distance (simple version)
        min_distance = float('inf')
        best_match = None
        for name, card in self.card_lookup.items():
            distance = levenshtein_distance(card_name, name)
            if distance < min_distance and distance < 3:
                min_distance = distance
                best_match = card
        
        return best_match
    
    def _analyze_deck(self, deck_cards: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the current deck composition"""
        analysis = {
            "count": len(deck_cards),
            "creatures": 0,
            "spells": 0,
            "lands": 0,
            "cmc_distribution": Counter(),
            "colors": Counter(),
            "color_identity": set(),
            "keywords": Counter(),
            "mana_curve": {},
            "avg_cmc": 0,
            "synergies": [],
        }
        
        total_cmc = 0
        creature_count = 0
        
        for card in deck_cards:
            if card["is_creature"]:
                analysis["creatures"] += 1
                creature_count += 1
            elif card["is_instant"] or card["is_sorcery"]:
                analysis["spells"] += 1
            
            if card["is_land"]:
                analysis["lands"] += 1
            
            cmc = card.get("cmc", 0)
            total_cmc += cmc
            analysis["cmc_distribution"][int(cmc)] += 1
            
            # Build mana curve data - simplified
            mana_bin = min(int(cmc), 6) if int(cmc) <= 5 else "6+"
            analysis["mana_curve"][mana_bin] = analysis["mana_curve"].get(mana_bin, 0) + 1
            
            # Color analysis
            colors = card.get("colors", [])
            for color in colors:
                analysis["colors"][color] += 1
            for color in card.get("color_identity", []):
                analysis["color_identity"].add(color)
            
            # Keyword analysis - use pre-computed cache
            card_name = card["name"]
            for keyword in self._keyword_cache.get(card_name, set()):
                analysis["keywords"][keyword] += 1
        
        if len(deck_cards) > 0:
            analysis["avg_cmc"] = total_cmc / len(deck_cards)
        
        # Detect synergies
        analysis["synergies"] = self._detect_synergies(deck_cards, analysis)
        
        return analysis
    
    def _detect_synergies(self, deck_cards: List[Dict[str, Any]], analysis: Dict) -> List[str]:
        """Detect synergies and themes in the deck"""
        synergies = []
        keyword_counts = analysis["keywords"]
        
        # Check keyword frequencies - early exit for common patterns
        keyword_checks = [
            ("flying", 3, "flying theme"),
            ("lifelink", 2, "lifelink synergy"),
            ("token", 2, "token generation"),
            ("sacrifice", 2, "sacrifice synergy"),
            ("graveyard", 2, "graveyard synergy"),
            ("proliferate", 1, "proliferate theme"),
            ("mill", 2, "mill synergy"),
            ("draw", 3, "card draw theme"),
            ("counterspell", 2, "control theme"),
        ]
        
        for keyword, threshold, label in keyword_checks:
            if keyword_counts.get(keyword, 0) >= threshold:
                synergies.append(label)
        
        # Color-based synergies
        colors = list(analysis["color_identity"])
        if len(colors) == 1:
            synergies.append(f"mono-{self._color_name(colors[0])} deck")
        elif len(colors) == 2:
            color_pair = "".join(sorted(colors))
            synergies.append(f"{color_pair} colors")
        
        # Creature type detection - use cached types
        creature_types = []
        for card in deck_cards:
            creature_types.extend(self._creature_type_cache.get(card["name"], []))
        
        type_counts = Counter(creature_types)
        for ctype, count in type_counts.most_common(3):
            if count >= 2:
                synergies.append(f"{ctype} synergy")
        
        return synergies
    
    def _extract_creature_types(self, type_line: str) -> List[str]:
        """Extract creature types from type line"""
        if "—" not in type_line:
            return []
        
        creature_part = type_line.split("—")[1].strip()
        types = [t.strip().lower() for t in creature_part.split()]
        return types
    
    def _rate_card(self, card: Dict[str, Any], deck_cards: List[Dict[str, Any]], 
                   analysis: Dict[str, Any]) -> tuple:
        """
        Rate a single card based on deck composition.
        Returns (rating, explanation)
        """
        rating = 5.0  # Base rating
        reasons = []
        
        # 1. Mana curve analysis (very important in limited)
        mana_curve_score = self._rate_mana_curve_fit(card, analysis)
        rating += mana_curve_score
        if mana_curve_score > 1:
            reasons.append(f"good mana curve fit ({mana_curve_score:+.1f})")
        elif mana_curve_score < -1:
            reasons.append(f"mana curve already crowded ({mana_curve_score:+.1f})")
        
        # 2. Color synergy
        color_score = self._rate_color_fit(card, analysis)
        rating += color_score
        if color_score > 0.5:
            reasons.append(f"color synergy ({color_score:+.1f})")
        elif color_score < -0.5:
            reasons.append(f"color conflict ({color_score:+.1f})")
        
        # 3. Creature/Spell balance
        balance_score = self._rate_deck_balance(card, analysis)
        rating += balance_score
        if balance_score > 0.5:
            reasons.append(f"balances deck ({balance_score:+.1f})")
        elif balance_score < -0.5:
            reasons.append(f"throws off balance ({balance_score:+.1f})")
        
        # 4. Synergy with existing cards
        synergy_score = self._rate_synergies(card, deck_cards, analysis)
        rating += synergy_score
        if synergy_score > 1:
            reasons.append(f"strong synergies ({synergy_score:+.1f})")
        elif synergy_score > 0:
            reasons.append(f"some synergies ({synergy_score:+.1f})")
        
        # 5. Power level in limited
        power_score = self._rate_limited_power(card)
        rating += power_score
        if power_score > 1:
            reasons.append(f"strong limited card ({power_score:+.1f})")
        
        # 6. Deck completion bonus
        deck_size_penalty = (40 - analysis["count"]) / 40.0  # Bonus to fill deck
        completion_score = 0.5 * deck_size_penalty
        rating += completion_score
        
        # 7. Rarity factor (rare/mythic often stronger but less available)
        if card["rarity"] == "rare" or card["rarity"] == "mythic":
            reasons.append("rare/mythic power level")
        
        # Clamp rating between 1 and 10
        rating = max(1.0, min(10.0, rating))
        
        explanation = ", ".join(reasons) if reasons else "fills a slot"
        
        return round(rating, 1), explanation
    
    def _rate_mana_curve_fit(self, card: Dict[str, Any], analysis: Dict) -> float:
        """Rate how well the card fits the current mana curve"""
        cmc = card.get("cmc", 0)
        curve = analysis["cmc_distribution"]
        
        # Ideal draft deck has: 2-3 1-drops, 3-4 2-drops, 2-3 3-drops, 2-3 4-drops, etc.
        ideal_counts = {
            0: 0,
            1: 2.5,
            2: 3.5,
            3: 3,
            4: 2.5,
            5: 2,
            6: 1.5
        }
        
        cmc_bin = int(cmc) if int(cmc) <= 6 else 6
        current_count = curve.get(cmc_bin, 0)
        ideal_count = ideal_counts.get(cmc_bin, 1.5)
        
        # Boost if we need cards at this cmc, penalize if we have too many
        if current_count < ideal_count - 1:
            return 2.0
        elif current_count < ideal_count:
            return 1.0
        elif current_count == ideal_count:
            return 0.0
        else:
            return -1.5
    
    def _rate_color_fit(self, card: Dict[str, Any], analysis: Dict) -> float:
        """Rate how well the card's color aligns with the deck"""
        card_colors = set(card["colors"])
        deck_colors = analysis["color_identity"]
        
        # If no colors in deck yet, any color is fine
        if not deck_colors:
            return 0.5 if not card_colors else 0.3
        
        # Perfect fit if card is in deck colors
        if card_colors and card_colors.issubset(deck_colors):
            return 1.5
        
        # Mono-colored card outside colors is bad
        if len(card_colors) == 1 and not card_colors.issubset(deck_colors):
            return -2.0
        
        # Colorless is always okay
        if not card_colors:
            return 0.5
        
        # Some colors overlap - acceptable
        if card_colors & deck_colors:
            return 0.0
        
        # No colors overlap - bad
        return -1.5
    
    def _rate_deck_balance(self, card: Dict[str, Any], analysis: Dict) -> float:
        """Rate creature/spell balance"""
        # In limited, typically want 13-16 creatures, 6-8 tricks/removal, 5-8 utility
        total_non_land = analysis["creatures"] + analysis["spells"]
        
        creature_ratio = analysis["creatures"] / max(1, total_non_land) if total_non_land > 0 else 0.5
        ideal_creature_ratio = 0.65  # ~65% creatures
        
        if card["is_creature"]:
            if creature_ratio < ideal_creature_ratio - 0.1:
                return 1.5
            elif creature_ratio < ideal_creature_ratio + 0.1:
                return 0.5
            else:
                return -1.0
        else:
            if creature_ratio > ideal_creature_ratio + 0.1:
                return 1.5
            elif creature_ratio > ideal_creature_ratio - 0.1:
                return 0.5
            else:
                return -0.5
    
    def _rate_synergies(self, card: Dict[str, Any], deck_cards: List[Dict[str, Any]], 
                        analysis: Dict) -> float:
        """Rate synergies with existing cards"""
        synergy_score = 0.0
        deck_keywords = analysis["keywords"]
        
        # Check keyword overlap - use cached keywords
        card_name = card["name"]
        card_keywords = self._keyword_cache.get(card_name, set())
        
        for keyword in card_keywords:
            if deck_keywords.get(keyword, 0) > 0:
                synergy_score += 1.0  # Big boost for keyword synergies
        
        # Check creature type synergies - use cached types
        if card["is_creature"]:
            card_types = set(self._creature_type_cache.get(card_name, []))
            
            # Pre-compute creature count instead of iterating
            for existing_card in deck_cards:
                if existing_card["is_creature"]:
                    existing_types = set(self._creature_type_cache.get(existing_card["name"], []))
                    if card_types & existing_types:
                        synergy_score += 0.5
                        break  # Only count once per creature type match
        
        # Quick keyword synergy checks
        draw_bonus = 0.5 if "draw" in card_keywords and deck_keywords.get("draw", 0) > 0 else 0
        sacrifice_bonus = 1.0 if "sacrifice" in card_keywords and deck_keywords.get("sacrifice", 0) > 0 else 0
        synergy_score += draw_bonus + sacrifice_bonus
        
        # Evasion synergy - simplified
        evasion_keywords = {"flying", "menace", "evasion"}
        if card_keywords & evasion_keywords:
            if deck_keywords.get("draw", 0) > 0 or deck_keywords.get("flying", 0) > 1:
                synergy_score += 0.5
        
        return synergy_score
    
    def _rate_limited_power(self, card: Dict[str, Any]) -> float:
        """Rate the power level of a card in limited"""
        score = 0.0
        
        # Creatures with good stats - use cached data
        if card["is_creature"]:
            card_name = card["name"]
            if card_name in self._power_toughness_cache:
                power, toughness = self._power_toughness_cache[card_name]
                cmc = card.get("cmc", 0)
                
                # Power/toughness per mana spent
                total_stats = power + toughness
                value = total_stats / max(1, cmc)
                
                if value >= 2.0:  # Excellent value
                    score += 1.5
                elif value >= 1.5:  # Good value
                    score += 0.5
                elif value < 0.8:  # Poor value
                    score -= 1.0
                
                # Evasive creatures are better
                card_keywords = self._keyword_cache.get(card_name, set())
                if card_keywords & {"flying", "menace", "trample"}:
                    score += 0.5
        
        # Removal spells are always good
        if card["is_instant"] or card["is_sorcery"]:
            oracle = card.get("oracle_text", "").lower()
            # Use tuple lookup for faster word checking
            if any(word in oracle for word in ("destroy", "exile", "damage", "discard", "counter")):
                score += 1.5
            elif "draw" in oracle:
                score += 1.0
            elif any(phrase in oracle for phrase in ("can't", "prevent")):
                score += 0.5
        
        return score
    
    def _color_name(self, color_code: str) -> str:
        """Convert color code to name"""
        color_map = {"W": "white", "U": "blue", "B": "black", "R": "red", "G": "green"}
        return color_map.get(color_code, "colorless")


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
