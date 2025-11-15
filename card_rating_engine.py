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
    
    def rate_cards(self, selected_cards: List[str], format_legality: str = "draft") -> List[tuple]:
        """
        Rate all cards in the set based on existing deck composition.
        Returns list of tuples: (card_name, rating, explanation)
        """
        # Parse selected cards
        deck_cards = self._parse_selected_cards(selected_cards)
        if not deck_cards:
            return []
        
        # Analyze current deck state
        deck_analysis = self._analyze_deck(deck_cards)
        
        # Rate each card in the set
        ratings = []
        for card in self.all_cards:
            if card["name"].lower() not in [c["name"].lower() for c in deck_cards]:
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
            "power_values": [],
            "avg_cmc": 0,
            "creature_count": 0,
            "instant_sorcery_count": 0,
            "synergies": [],
        }
        
        total_cmc = 0
        
        for card in deck_cards:
            if card["is_creature"]:
                analysis["creatures"] += 1
                analysis["creature_count"] += 1
                if card.get("power"):
                    try:
                        analysis["power_values"].append(float(card["power"]))
                    except (ValueError, TypeError):
                        pass
            elif card["is_instant"] or card["is_sorcery"]:
                analysis["instant_sorcery_count"] += 1
                analysis["spells"] += 1
            
            if card["is_land"]:
                analysis["lands"] += 1
            
            cmc = card.get("cmc", 0)
            total_cmc += cmc
            analysis["cmc_distribution"][int(cmc)] += 1
            
            # Build mana curve data
            if int(cmc) <= 5:
                mana_bin = int(cmc)
            else:
                mana_bin = "6+"
            analysis["mana_curve"][mana_bin] = analysis["mana_curve"].get(mana_bin, 0) + 1
            
            # Color analysis
            for color in card["colors"]:
                analysis["colors"][color] += 1
            for color in card["color_identity"]:
                analysis["color_identity"].add(color)
            
            # Keyword analysis
            for keyword in card.get("keywords", []):
                analysis["keywords"][keyword] += 1
        
        if len(deck_cards) > 0:
            analysis["avg_cmc"] = total_cmc / len(deck_cards)
        
        # Detect synergies
        analysis["synergies"] = self._detect_synergies(deck_cards, analysis)
        
        return analysis
    
    def _detect_synergies(self, deck_cards: List[Dict[str, Any]], analysis: Dict) -> List[str]:
        """Detect synergies and themes in the deck"""
        synergies = []
        
        # Check keyword frequencies
        keyword_counts = analysis["keywords"]
        if keyword_counts.get("flying", 0) >= 3:
            synergies.append("flying theme")
        if keyword_counts.get("lifelink", 0) >= 2:
            synergies.append("lifelink synergy")
        if keyword_counts.get("token", 0) >= 2:
            synergies.append("token generation")
        if keyword_counts.get("sacrifice", 0) >= 2:
            synergies.append("sacrifice synergy")
        if keyword_counts.get("graveyard", 0) >= 2:
            synergies.append("graveyard synergy")
        if keyword_counts.get("proliferate", 0) >= 1:
            synergies.append("proliferate theme")
        if keyword_counts.get("mill", 0) >= 2:
            synergies.append("mill synergy")
        if keyword_counts.get("draw", 0) >= 3:
            synergies.append("card draw theme")
        if keyword_counts.get("counterspell", 0) >= 2:
            synergies.append("control theme")
        
        # Color-based synergies
        colors = list(analysis["color_identity"])
        if len(colors) == 1:
            synergies.append(f"mono-{self._color_name(colors[0])} deck")
        elif len(colors) == 2:
            color_pair = "".join(sorted(colors))
            synergies.append(f"{color_pair} colors")
        
        # Creature type detection
        creature_types = []
        for card in deck_cards:
            types = self._extract_creature_types(card["type_line"])
            creature_types.extend(types)
        
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
        
        # Check keyword overlap
        card_keywords = set(card.get("keywords", []))
        deck_keywords = analysis["keywords"]
        
        for keyword in card_keywords:
            if keyword in deck_keywords and deck_keywords[keyword] > 0:
                synergy_score += 1.0  # Big boost for keyword synergies
        
        # Check creature type synergies
        if card["is_creature"]:
            card_types = set(self._extract_creature_types(card["type_line"]))
            
            for existing_card in deck_cards:
                if existing_card["is_creature"]:
                    existing_types = set(self._extract_creature_types(existing_card["type_line"]))
                    shared_types = card_types & existing_types
                    if shared_types:
                        synergy_score += 0.5
        
        # Check for card draw/advantage engines
        if "draw" in card_keywords and "draw" in analysis["keywords"]:
            synergy_score += 0.5
        
        # Check for sacrifice synergies
        if "sacrifice" in card_keywords and "sacrifice" in analysis["keywords"]:
            synergy_score += 1.0
        
        # Evasion synergy with combat tricks
        if ("flying" in card_keywords or "evasion" in card_keywords or "menace" in card_keywords):
            if analysis["keywords"].get("draw", 0) > 0 or analysis["keywords"].get("flying", 0) > 1:
                synergy_score += 0.5
        
        return synergy_score
    
    def _rate_limited_power(self, card: Dict[str, Any]) -> float:
        """Rate the power level of a card in limited"""
        score = 0.0
        
        # Creatures with good stats
        if card["is_creature"]:
            try:
                power = float(card.get("power", 0))
                toughness = float(card.get("toughness", 0))
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
                if card.get("keywords") and any(e in card.get("keywords", []) for e in ["flying", "menace", "trample"]):
                    score += 0.5
                
            except (ValueError, TypeError):
                pass
        
        # Removal spells are always good
        if card["is_instant"] or card["is_sorcery"]:
            oracle = card.get("oracle_text", "").lower()
            if any(word in oracle for word in ["destroy", "exile", "damage", "discard", "counter"]):
                score += 1.5
            elif "draw" in oracle:
                score += 1.0
            elif "can't" in oracle or "prevent" in oracle:
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
