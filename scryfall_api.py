"""
MTG Set data fetcher using the Scryfall API
"""
import requests
from typing import List, Dict, Any
import json

class ScryfallAPI:
    """Interface with Scryfall API to fetch MTG data"""
    
    BASE_URL = "https://api.scryfall.com"
    
    @staticmethod
    def get_set_codes() -> List[Dict[str, str]]:
        """Fetch all available MTG sets"""
        try:
            response = requests.get(f"{ScryfallAPI.BASE_URL}/sets")
            response.raise_for_status()
            sets_data = response.json()
            
            # Return list of sets with code and name
            return [{"code": s["code"].upper(), "name": s["name"]} for s in sets_data["data"]]
        except requests.RequestException as e:
            print(f"Error fetching sets: {e}")
            return []
    
    @staticmethod
    def get_set_cards(set_code: str) -> List[Dict[str, Any]]:
        """Fetch all cards from a specific set"""
        cards = []
        page = 1
        
        try:
            while True:
                url = f"{ScryfallAPI.BASE_URL}/cards/search"
                params = {
                    "q": f"set:{set_code.lower()}",
                    "page": page,
                    "unique": "prints"  # Get only one print version of each card
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if "data" in data:
                    cards.extend(data["data"])
                
                # Check if there are more pages
                if not data.get("has_more", False):
                    break
                
                page += 1
                
        except requests.RequestException as e:
            print(f"Error fetching cards for set {set_code}: {e}")
        
        return cards
    
    @staticmethod
    def parse_card_data(card: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant card data for analysis"""
        
        # Parse mana cost
        mana_cost = card.get("mana_cost", "")
        converted_mana_cost = card.get("cmc", 0)
        
        # Parse card type
        type_line = card.get("type_line", "")
        is_creature = "Creature" in type_line
        is_instant = "Instant" in type_line
        is_sorcery = "Sorcery" in type_line
        is_enchantment = "Enchantment" in type_line
        is_artifact = "Artifact" in type_line
        is_land = "Land" in type_line
        
        # Parse creature stats
        power = card.get("power")
        toughness = card.get("toughness")
        
        # Parse abilities
        oracle_text = card.get("oracle_text", "").lower()
        
        # Parse colors
        colors = card.get("colors", [])
        color_identity = card.get("color_identity", [])
        
        # Rarity
        rarity = card.get("rarity", "common")
        
        return {
            "name": card.get("name", "Unknown"),
            "set_code": card.get("set", ""),
            "type_line": type_line,
            "oracle_text": card.get("oracle_text", ""),
            "mana_cost": mana_cost,
            "cmc": converted_mana_cost,
            "is_creature": is_creature,
            "is_instant": is_instant,
            "is_sorcery": is_sorcery,
            "is_enchantment": is_enchantment,
            "is_artifact": is_artifact,
            "is_land": is_land,
            "power": power,
            "toughness": toughness,
            "colors": colors,
            "color_identity": color_identity,
            "rarity": rarity,
            "oracle_text_lower": oracle_text,
            "keywords": extract_keywords(oracle_text),
            "image_url": card.get("image_uris", {}).get("normal", "") if card.get("image_uris") else "",
            "scryfall_uri": card.get("scryfall_uri", "")
        }

def extract_keywords(oracle_text: str) -> List[str]:
    """Extract relevant keywords from oracle text"""
    keywords = []
    common_keywords = [
        "flying", "lifelink", "vigilance", "haste", "deathtouch", "double strike",
        "trample", "shroud", "indestructible", "regenerate", "menace", "hexproof",
        "flash", "prowess", "drain", "ramp", "tutor", "draw", "discard",
        "mill", "etb", "enter the battlefield", "sacrifice", "token", "scry",
        "surveil", "adapt", "mutate", "kicker", "spell mastery", "aftermath",
        "flashback", "madness", "delve", "revolt", "enrage", "proliferate",
        "graveyard", "recurring", "protection", "evasion", "bounce", "counterspell"
    ]
    
    for keyword in common_keywords:
        if keyword in oracle_text:
            keywords.append(keyword)
    
    return keywords
